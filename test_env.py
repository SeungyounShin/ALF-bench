#!/usr/bin/env python3
"""
Test script for Channel Talk environment.
Demonstrates agent-environment interaction with RAG tool usage.
"""

import os
from litellm import completion
from envs import ChannelEnv


def run_episode(env: ChannelEnv, scenario_id: str = None, verbose: bool = True):
    """
    Run one episode in the environment.

    Args:
        env: ChannelEnv instance
        scenario_id: Scenario to run (None for first)
        verbose: Whether to print detailed output
    """
    # Reset environment
    state = env.reset(scenario_id=scenario_id)

    if verbose:
        print("\n" + "=" * 80)
        print(f"Starting Episode: {state['scenario']['id']}")
        print(f"Difficulty: {state['scenario']['difficulty']}")
        print(f"Category: {state['scenario']['category']}")
        print("=" * 80)
        print(f"\n👤 User: {state['user_message']}\n")

    # Get available tools
    tools = env.get_available_tools()

    # Episode loop
    total_reward = 0.0
    done = False

    while not done:
        # Build messages for agent
        messages = [
            {
                "role": "system",
                "content": "당신은 채널톡 고객센터 상담원입니다. 고객의 질문에 정확하고 친절하게 답변해주세요. 필요한 경우 search_data 도구를 사용하여 문서를 검색할 수 있습니다.",
            }
        ]

        # Add conversation history
        for entry in state["conversation_history"]:
            # Add tool results if any
            if entry.get("tool_calls"):
                for tool_result in entry["tool_calls"]:
                    messages.append(
                        {
                            "role": "assistant",
                            "content": f"[검색 수행: {tool_result['query']}]",
                            "tool_calls": [
                                {
                                    "id": f"call_{len(messages)}",
                                    "type": "function",
                                    "function": {
                                        "name": "search_data",
                                        "arguments": f'{{"query": "{tool_result["query"]}"}}',
                                    },
                                }
                            ],
                        }
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": f"call_{len(messages)-1}",
                            "content": tool_result["results"],
                        }
                    )

            # Add agent message
            if entry.get("agent") and not entry["agent"].startswith("[검색 수행:"):
                messages.append({"role": "assistant", "content": entry["agent"]})

            # Add user message
            if entry.get("user"):
                messages.append({"role": "user", "content": entry["user"]})

        # Add current user message if not in history
        if not state["conversation_history"] or state["conversation_history"][-1].get(
            "user"
        ) != state["user_message"]:
            messages.append({"role": "user", "content": state["user_message"]})

        # Call LiteLLM with tools
        try:
            # GPT-5 only supports temperature=1
            temperature = 1.0 if "gpt-5" in env.agent_model else 0.7
            
            # Prepare completion params
            completion_params = {
                "model": env.agent_model,
                "messages": messages,
                "tools": tools,
                "temperature": temperature,
                # "max_tokens": 500,
            }
            
            # Add reasoning_effort for o1/o3 models
            # Options: "low", "medium", "high"
            if any(model in env.agent_model for model in ["o1", "o3", "gpt-5"]):
                completion_params["reasoning_effort"] = "high"  # or "low", "high"
            
            response = completion(**completion_params)

            # Extract response
            message_obj = response.choices[0].message

            # Handle tool calls if present
            final_response = response  # Keep track of final response
            
            if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:
                if verbose:
                    print(f"🔧 Tool Calls Detected ({len(message_obj.tool_calls)} calls)\n")
                
                # Add assistant's tool call message
                messages.append({
                    "role": "assistant",
                    "content": message_obj.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message_obj.tool_calls
                    ]
                })
                
                # Execute each tool call
                for tool_call in message_obj.tool_calls:
                    import json
                    func_args = json.loads(tool_call.function.arguments)
                    query = func_args.get("query", "")
                    
                    if verbose:
                        print(f"   🔍 Searching: {query}")
                    
                    # Execute search
                    results = env.search_tool.search(query, top_k=3)
                    formatted_results = env.search_tool.format_search_results(results)
                    
                    if verbose:
                        print(f"   📄 Found {len(results)} documents")
                        for i, result in enumerate(results, 1):
                            print(f"      {i}. {result['title']} (score: {result['score']:.3f})")
                        print()
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": formatted_results
                    })
                
                # Call LLM again with tool results
                if verbose:
                    print("🤖 Generating response with search results...\n")
                
                # Prepare completion params for second call
                completion_params_2 = {
                    "model": env.agent_model,
                    "messages": messages,
                    "temperature": temperature,
                    # "max_tokens": 500,
                }
                
                # Add reasoning_effort for o1/o3 models
                if any(model in env.agent_model for model in ["o1", "o3", "gpt-5"]):
                    completion_params_2["reasoning_effort"] = "high"
                
                final_response = completion(**completion_params_2)
                message_obj = final_response.choices[0].message

            # Print final agent message
            if verbose and message_obj.content:
                print(f"🤖 Agent: {message_obj.content}\n")

            # Step environment with FINAL response (after tool calls)
            action = {"policy": final_response}
            state, reward, done, info = env.step(action)
            total_reward += reward

            if verbose and not done:
                print(f"👤 User: {state['user_message']}\n")

        except Exception as e:
            print(f"\n❌ Error during agent response: {e}")
            # Provide fallback response
            action = {"message": "죄송합니다. 잠시 후 다시 시도해주세요."}
            state, reward, done, info = env.step(action)
            total_reward += reward

    # Episode finished
    if verbose:
        print("=" * 80)
        print(f"Episode finished!")
        print(f"Total turns: {info['turns_taken']}")
        print(f"User satisfied: {info['satisfied']}")
        print(f"Total reward: {total_reward:.3f}")

        # Print judge evaluation if available
        if info.get("judge_evaluation"):
            judge_eval = info["judge_evaluation"]
            print(f"\n📊 LLM-as-a-Judge Evaluation:")
            print(f"   Accuracy:      {judge_eval['accuracy']:.1f}/10")
            print(f"   Completeness:  {judge_eval['completeness']:.1f}/10")
            print(f"   Helpfulness:   {judge_eval['helpfulness']:.1f}/10")
            print(f"   Efficiency:    {judge_eval['efficiency']:.1f}/10")
            print(f"   Clarity:       {judge_eval['clarity']:.1f}/10")
            print(f"   Overall CSAT:  {judge_eval['overall_csat']:.1f}/10")
            print(f"\n   Reasoning: {judge_eval['reasoning']}")

        print("=" * 80)

    return total_reward, info


def main():
    """Main function to test the environment."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Set it to use GPT models.")
        print("   Example: export OPENAI_API_KEY='your-key-here'")
        return

    # Initialize environment
    print("🚀 Initializing Channel Talk Environment...")
    env = ChannelEnv(
        agent_model="gpt-4o",
        user_model="gpt-4.1",
        judge_model="gpt-5",
        max_turns=10,
        use_judge=True,
    )

    # Run episodes for each scenario
    results = []
    for scenario in env.scenarios:
        print(f"\n\n{'='*80}")
        print(f"Running Scenario: {scenario['scenario_id']}")
        print(f"{'='*80}")

        reward, info = run_episode(env, scenario_id=scenario["scenario_id"], verbose=True)
        results.append(
            {
                "scenario_id": scenario["scenario_id"],
                "difficulty": scenario["difficulty"],
                "reward": reward,
                "satisfied": info["satisfied"],
                "turns": info["turns_taken"],
                "judge_eval": info.get("judge_evaluation"),
            }
        )

    # Print summary
    print("\n\n" + "=" * 80)
    print("📊 SUMMARY - LLM-as-a-Judge Evaluation")
    print("=" * 80)

    # Detailed results per scenario
    for result in results:
        status = "✅" if result["satisfied"] else "❌"
        print(f"\n{status} {result['scenario_id']} ({result['difficulty']})")
        print(f"   Reward: {result['reward']:.3f} | Turns: {result['turns']}")

        if result.get("judge_eval"):
            je = result["judge_eval"]
            print(f"   📈 Metrics:")
            print(
                f"      Accuracy: {je['accuracy']:.1f} | Completeness: {je['completeness']:.1f} | "
                f"Helpfulness: {je['helpfulness']:.1f}"
            )
            print(
                f"      Efficiency: {je['efficiency']:.1f} | Clarity: {je['clarity']:.1f} | "
                f"CSAT: {je['overall_csat']:.1f}"
            )

    # Overall statistics
    print("\n" + "=" * 80)
    print("📊 Overall Statistics")
    print("=" * 80)

    avg_reward = sum(r["reward"] for r in results) / len(results)
    success_rate = sum(1 for r in results if r["satisfied"]) / len(results) * 100
    avg_turns = sum(r["turns"] for r in results) / len(results)

    print(f"Average Reward:     {avg_reward:.3f}")
    print(f"Success Rate:       {success_rate:.1f}%")
    print(f"Average Turns:      {avg_turns:.1f}")

    # Average judge metrics
    judge_results = [r for r in results if r.get("judge_eval")]
    if judge_results:
        avg_accuracy = sum(r["judge_eval"]["accuracy"] for r in judge_results) / len(judge_results)
        avg_completeness = sum(r["judge_eval"]["completeness"] for r in judge_results) / len(
            judge_results
        )
        avg_helpfulness = sum(r["judge_eval"]["helpfulness"] for r in judge_results) / len(
            judge_results
        )
        avg_efficiency = sum(r["judge_eval"]["efficiency"] for r in judge_results) / len(
            judge_results
        )
        avg_clarity = sum(r["judge_eval"]["clarity"] for r in judge_results) / len(judge_results)
        avg_csat = sum(r["judge_eval"]["overall_csat"] for r in judge_results) / len(judge_results)

        print(f"\n📊 Average LLM-as-a-Judge Metrics:")
        print(f"   Accuracy:       {avg_accuracy:.2f}/10")
        print(f"   Completeness:   {avg_completeness:.2f}/10")
        print(f"   Helpfulness:    {avg_helpfulness:.2f}/10")
        print(f"   Efficiency:     {avg_efficiency:.2f}/10")
        print(f"   Clarity:        {avg_clarity:.2f}/10")
        print(f"   Overall CSAT:   {avg_csat:.2f}/10")

    print("=" * 80)


if __name__ == "__main__":
    main()

