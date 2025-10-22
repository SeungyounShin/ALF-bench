"""
User simulator that follows scenarios and evaluates agent responses.
"""

import json
from typing import Dict, List, Optional
from litellm import completion


class UserSimulator:
    """Simulates a user following a scenario."""

    def __init__(
        self,
        scenario: Dict,
        model: str = "gpt-4o",
        max_turns: int = 10,
    ):
        """
        Initialize user simulator.

        Args:
            scenario: Scenario dict with user_scenario and reference_text
            model: LiteLLM model name for user simulation
            max_turns: Maximum number of conversation turns
        """
        self.scenario = scenario
        self.model = model
        self.max_turns = max_turns
        self.turn_count = 0
        self.conversation_history = []
        self.is_satisfied = False

    def get_initial_message(self) -> str:
        """Get the initial user message based on the scenario."""
        return self.scenario["user_scenario"]

    def respond(self, agent_message: str) -> Dict:
        """
        Generate user response based on agent's message.

        Args:
            agent_message: The agent's response

        Returns:
            Dict with:
                - message: User's response
                - done: Whether the conversation should end
                - satisfied: Whether user is satisfied with the answer
        """
        self.turn_count += 1

        # Build prompt for user simulator
        system_prompt = f"""You are simulating a customer asking questions to a customer service agent.

Your scenario: {self.scenario['user_scenario']}

Reference answer (what you want to know): {self.scenario['reference_text']}

Instructions:
1. If the agent's answer covers the key information in the reference answer, express satisfaction and end with "###STOP###"
2. If the answer is incomplete or unclear, ask follow-up questions to get more specific information. Do NOT include ###STOP###.
3. If the answer is wrong or unhelpful, express confusion and rephrase your question. Do NOT include ###STOP###.
4. Keep responses natural and conversational in Korean.
5. IMPORTANT: Only output "###STOP###" at the end of your message when you are satisfied with the answer.
6. Maximum {self.max_turns} turns - if not satisfied by then, end with ###STOP### anyway.

Current turn: {self.turn_count}/{self.max_turns}

Example responses:
- Not satisfied: "그럼 구체적으로 어디서 찾을 수 있나요?"
- Satisfied: "감사합니다. 이제 이해했어요! ###STOP###"
"""

        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history
        for entry in self.conversation_history:
            messages.append({"role": "assistant", "content": entry["agent"]})
            if "user" in entry:
                messages.append({"role": "user", "content": entry["user"]})

        # Add latest agent message
        messages.append({"role": "assistant", "content": agent_message})

        # Add instruction for response
        messages.append(
            {
                "role": "user",
                "content": "Respond to the agent's message. If satisfied, say so and thank them. If not, ask for clarification or more details.",
            }
        )

        # Generate response
        try:
            # GPT-5 only supports temperature=1
            temperature = 1.0 if "gpt-5" in self.model else 0.7
            
            # Prepare completion params
            completion_params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                # "max_tokens": 200,
            }
            
            # Add reasoning_effort for o1/o3 models
            if any(model in self.model for model in ["o1", "o3", "gpt-5"]):
                completion_params["reasoning_effort"] = "low"  # User simulator uses low effort
            
            response = completion(**completion_params)
            user_message = response.choices[0].message.content
            
            # Handle None or empty response
            if user_message is None:
                user_message = "죄송합니다만, 다시 설명해주시겠어요?"
                print(f"⚠️  Warning: User simulator returned None, using fallback")

            # Check for STOP token
            if "###STOP###" in user_message:
                self.is_satisfied = True
                done = True
                # Remove the STOP token from the message for cleaner output
                user_message = user_message.replace("###STOP###", "").strip()
            elif self.turn_count >= self.max_turns:
                # Force stop if max turns reached
                done = True
                self.is_satisfied = False
            else:
                done = False

            return {
                "message": user_message,
                "done": done,
                "satisfied": self.is_satisfied,
            }

        except Exception as e:
            print(f"Error in user simulation: {e}")
            return {
                "message": "죄송합니다만, 다시 설명해주시겠어요?",
                "done": False,
                "satisfied": False,
            }

    def add_to_history(self, agent_message: str, user_message: Optional[str] = None):
        """Add exchange to conversation history."""
        entry = {"agent": agent_message}
        if user_message:
            entry["user"] = user_message
        self.conversation_history.append(entry)

