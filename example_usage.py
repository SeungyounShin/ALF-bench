#!/usr/bin/env python3
"""
Simple example of using ChannelEnv with a custom agent.
"""

import os
from litellm import completion
from envs import ChannelEnv


def simple_agent_loop():
    """Simple example with direct message action."""
    env = ChannelEnv(max_turns=5)
    state = env.reset(scenario_id="scenario_001")

    print(f"👤 User: {state['user_message']}\n")

    done = False
    while not done:
        # Simple hardcoded response (not recommended for real use)
        action = {
            "message": "설치 스크립트는 [채널 설정] - [일반 설정] - [버튼 설치 및 설정] - [채널톡 버튼 설치]에서 확인하실 수 있습니다."
        }

        state, reward, done, info = env.step(action)

        if not done:
            print(f"🤖 Agent: {action['message']}")
            print(f"👤 User: {state['user_message']}\n")

    print(f"✅ Episode finished. Reward: {reward}, Satisfied: {info['satisfied']}")


def agent_with_rag():
    """Example with RAG tool usage."""
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY to run this example")
        return

    env = ChannelEnv(
        agent_model="gpt-4o",
        user_model="gpt-4o",
        judge_model="gpt-4o",
        max_turns=10,
        use_judge=True,
    )

    state = env.reset(scenario_id="scenario_002")
    print(f"Scenario: {state['scenario']['id']} ({state['scenario']['difficulty']})")
    print(f"👤 User: {state['user_message']}\n")

    tools = env.get_available_tools()
    done = False

    while not done:
        # Build messages
        messages = [
            {
                "role": "system",
                "content": "당신은 채널톡 고객센터 상담원입니다. 고객의 질문에 정확하고 친절하게 답변해주세요. 필요한 경우 search_data 도구를 사용하여 문서를 검색할 수 있습니다.",
            }
        ]

        # Add conversation history
        for entry in state["conversation_history"]:
            if entry.get("agent"):
                messages.append({"role": "assistant", "content": entry["agent"]})
            if entry.get("user"):
                messages.append({"role": "user", "content": entry["user"]})

        # Add current user message
        if (
            not state["conversation_history"]
            or state["conversation_history"][-1].get("user") != state["user_message"]
        ):
            messages.append({"role": "user", "content": state["user_message"]})

        # Call LiteLLM
        # GPT-5 only supports temperature=1
        temperature = 1.0 if "gpt-5" in env.agent_model else 0.7
        
        # Prepare completion params
        completion_params = {
            "model": env.agent_model,
            "messages": messages,
            "tools": tools,
            "temperature": temperature,
            # "max_tokens": 2048,
        }
        
        # Add reasoning_effort for o1/o3 models
        # Options: "low", "medium", "high"
        if any(model in env.agent_model for model in ["o1", "o3"]):
            completion_params["reasoning_effort"] = "medium"
        
        response = completion(**completion_params)

        # Extract message
        message_obj = response.choices[0].message
        final_response = response  # Keep track of final response

        # Handle tool calls if present
        if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:
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
                
                print(f"   🔍 Searching: {query}")
                
                # Execute search
                results = env.search_tool.search(query, top_k=3)
                formatted_results = env.search_tool.format_search_results(results)
                
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
            print("🤖 Generating response with search results...\n")
            
            # Prepare completion params for second call
            completion_params_2 = {
                "model": env.agent_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 2048,
            }
            
            # Add reasoning_effort for o1/o3 models
            if any(model in env.agent_model for model in ["o1", "o3"]):
                completion_params_2["reasoning_effort"] = "medium"
            
            final_response = completion(**completion_params_2)
            message_obj = final_response.choices[0].message

        # Print final agent message
        if message_obj.content:
            print(f"🤖 Agent: {message_obj.content}\n")

        # Step environment with FINAL response (after tool calls)
        action = {"policy": final_response}
        state, reward, done, info = env.step(action)

        if not done:
            print(f"👤 User: {state['user_message']}\n")

    print(f"\n{'='*60}")
    print(f"✅ Episode finished!")
    print(f"   Turns: {info['turns_taken']}")
    print(f"   Satisfied: {info['satisfied']}")
    print(f"   Reward: {reward:.3f}")

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

    print(f"{'='*60}")


if __name__ == "__main__":
    print("Example 1: Simple agent with hardcoded response")
    print("=" * 60)
    simple_agent_loop()

    print("\n\n")

    print("Example 2: Agent with RAG tool")
    print("=" * 60)
    agent_with_rag()

