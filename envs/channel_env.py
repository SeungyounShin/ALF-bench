"""
Channel Talk Customer Service Environment.
Provides RL-style interface for agent-user interaction with RAG support.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from litellm import completion

from envs.tools import SearchData, SEARCH_DATA_TOOL
from envs.user_simulator import UserSimulator


class ChannelEnv:
    """
    Environment for Channel Talk customer service agent benchmarking.

    Supports:
    - Multi-turn conversations
    - RAG via search_data tool
    - User simulation based on scenarios
    - Conversation history tracking
    """

    def __init__(
        self,
        scenario_file: str = "data/domain/saas/channel/user_scenario.json",
        docs_dir: str = "data/domain/saas/channel/docs",
        agent_model: str = "gpt-4o",
        user_model: str = "gpt-4o",
        max_turns: int = 10,
        use_judge: bool = True,
        judge_model: str = "gpt-4o",
    ):
        """
        Initialize the environment.

        Args:
            scenario_file: Path to scenarios JSON file
            docs_dir: Path to documentation directory
            agent_model: LiteLLM model for the agent
            user_model: LiteLLM model for user simulation
            max_turns: Maximum conversation turns
            use_judge: Whether to use LLM-as-a-Judge for evaluation
            judge_model: LiteLLM model for judging
        """
        self.scenario_file = Path(scenario_file)
        self.agent_model = agent_model
        self.user_model = user_model
        self.max_turns = max_turns
        self.use_judge = use_judge
        self.judge_model = judge_model

        # Load scenarios
        with open(self.scenario_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.scenarios = data["scenarios"]

        # Initialize RAG tool
        self.search_tool = SearchData(docs_dir=docs_dir)

        # Initialize Judge if enabled
        self.judge = None
        if self.use_judge:
            from envs.judge import CSATJudge

            self.judge = CSATJudge(model=judge_model)

        # Environment state
        self.current_scenario = None
        self.user_simulator = None
        self.conversation_history = []
        self.turn_count = 0
        self.done = False

    def reset(self, scenario_id: Optional[str] = None) -> Dict:
        """
        Reset environment with a new scenario.

        Args:
            scenario_id: Specific scenario ID, or None for first scenario

        Returns:
            Initial state dict with:
                - scenario: Current scenario info
                - user_message: Initial user message
                - conversation_history: Empty list
                - turn: 0
        """
        # Select scenario
        if scenario_id:
            self.current_scenario = next(
                (s for s in self.scenarios if s["scenario_id"] == scenario_id), self.scenarios[0]
            )
        else:
            self.current_scenario = self.scenarios[0]

        # Initialize user simulator
        self.user_simulator = UserSimulator(
            scenario=self.current_scenario,
            model=self.user_model,
            max_turns=self.max_turns,
        )

        # Reset state
        self.conversation_history = []
        self.turn_count = 0
        self.done = False

        # Get initial user message
        initial_message = self.user_simulator.get_initial_message()

        state = {
            "scenario": {
                "id": self.current_scenario["scenario_id"],
                "difficulty": self.current_scenario["difficulty"],
                "category": self.current_scenario["category"],
            },
            "user_message": initial_message,
            "conversation_history": [],
            "turn": 0,
        }

        return state

    def step(self, action: Dict) -> Tuple[Dict, float, bool, Dict]:
        """
        Execute one step in the environment.

        Args:
            action: Agent's action dict with:
                - message: Agent's response message (optional if using policy)
                - policy: LiteLLM message object (optional)
                - tool_calls: Tool calls if any (optional)

        Returns:
            Tuple of (state, reward, done, info):
                - state: New state dict
                - reward: Reward for this step (0 for intermediate, 1 for success, -1 for failure)
                - done: Whether episode is finished
                - info: Additional information
        """
        if self.done:
            raise ValueError("Episode is done. Call reset() to start a new episode.")

        self.turn_count += 1

        # Extract agent message from action
        agent_message = None
        tool_calls = action.get("tool_calls", [])

        if "policy" in action:
            # Extract from LiteLLM response object
            policy = action["policy"]
            if hasattr(policy, "choices"):
                message_obj = policy.choices[0].message
                agent_message = message_obj.content or ""
                if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:
                    tool_calls = message_obj.tool_calls
            elif isinstance(policy, dict) and "content" in policy:
                agent_message = policy["content"]
        elif "message" in action:
            agent_message = action["message"]
        else:
            raise ValueError("Action must contain either 'message' or 'policy'")

        # Handle tool calls
        tool_results = []
        if tool_calls:
            for tool_call in tool_calls:
                if hasattr(tool_call, "function"):
                    # LiteLLM tool call object
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                else:
                    # Dict format
                    func_name = tool_call.get("name") or tool_call.get("function", {}).get("name")
                    func_args = tool_call.get("arguments") or tool_call.get("function", {}).get(
                        "arguments", {}
                    )
                    if isinstance(func_args, str):
                        func_args = json.loads(func_args)

                if func_name == "search_data":
                    query = func_args.get("query", "")
                    results = self.search_tool.search(query, top_k=3)
                    formatted_results = self.search_tool.format_search_results(results)
                    tool_results.append(
                        {
                            "tool": "search_data",
                            "query": query,
                            "results": formatted_results,
                        }
                    )

                    # If agent used search but didn't provide message, indicate search was performed
                    if not agent_message or agent_message.strip() == "":
                        agent_message = f"[검색 수행: {query}]"

        # Add to history
        self.conversation_history.append(
            {
                "turn": self.turn_count,
                "agent": agent_message,
                "tool_calls": tool_results,
            }
        )

        # Get user response
        user_response = self.user_simulator.respond(agent_message)
        user_message = user_response["message"]
        self.done = user_response["done"]
        satisfied = user_response["satisfied"]

        # Add user message to history
        self.conversation_history[-1]["user"] = user_message
        self.user_simulator.add_to_history(agent_message, user_message)

        # Calculate reward
        reward = 0.0
        judge_eval = None

        if self.done:
            if self.use_judge and self.judge:
                # Use LLM-as-a-Judge evaluation
                judge_eval = self.judge.evaluate_conversation(
                    scenario=self.current_scenario,
                    conversation_history=self.conversation_history,
                    user_satisfied=satisfied,
                )
                reward = self.judge.calculate_reward(judge_eval)
            else:
                # Simple binary reward
                if satisfied:
                    reward = 1.0  # Success
                else:
                    reward = -1.0  # Failed to satisfy user

        # Build new state
        state = {
            "scenario": {
                "id": self.current_scenario["scenario_id"],
                "difficulty": self.current_scenario["difficulty"],
                "category": self.current_scenario["category"],
            },
            "user_message": user_message,
            "conversation_history": self.conversation_history.copy(),
            "turn": self.turn_count,
        }

        # Info dict
        info = {
            "satisfied": satisfied,
            "tool_results": tool_results,
            "turns_taken": self.turn_count,
            "judge_evaluation": judge_eval,
        }

        return state, reward, self.done, info

    def get_available_tools(self) -> List[Dict]:
        """Get list of available tools for the agent."""
        return [SEARCH_DATA_TOOL]

    def render(self, mode: str = "human") -> Optional[str]:
        """
        Render the current state.

        Args:
            mode: Rendering mode ('human' for console, 'ansi' for string)

        Returns:
            String representation if mode='ansi', None otherwise
        """
        output = []
        output.append("=" * 80)
        output.append(
            f"Scenario: {self.current_scenario['scenario_id']} "
            f"({self.current_scenario['difficulty']}) - {self.current_scenario['category']}"
        )
        output.append(f"Turn: {self.turn_count}/{self.max_turns}")
        output.append("=" * 80)

        for entry in self.conversation_history:
            output.append(f"\n[Turn {entry['turn']}]")

            # Tool calls
            if entry.get("tool_calls"):
                for tool_call in entry["tool_calls"]:
                    output.append(f"🔧 Tool: {tool_call['tool']}")
                    output.append(f"   Query: {tool_call['query']}")

            # Agent message
            output.append(f"🤖 Agent: {entry['agent']}")

            # User message
            if "user" in entry:
                output.append(f"👤 User: {entry['user']}")

        output.append("\n" + "=" * 80)

        result = "\n".join(output)

        if mode == "human":
            print(result)
            return None
        else:
            return result

