"""
LLM-as-a-Judge for CSAT evaluation.
Evaluates agent performance based on reference answers.
"""

import json
import re
from typing import Any, Dict, List, Optional
from litellm import completion


class CSATJudge:
    """
    Evaluates agent-user conversations using LLM-as-a-judge.
    Provides CSAT-style metrics.
    """

    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize CSAT Judge.

        Args:
            model: LiteLLM model name for judging
        """
        self.model = model

    def evaluate_conversation(
        self,
        scenario: Dict,
        conversation_history: List[Dict],
        user_satisfied: bool,
    ) -> Dict:
        """
        Evaluate a complete conversation.

        Args:
            scenario: Scenario dict with user_scenario and reference_text
            conversation_history: List of conversation turns
            user_satisfied: Whether user ended with satisfaction

        Returns:
            Dict with evaluation metrics:
                - accuracy: Factual correctness (0-10)
                - completeness: Coverage of reference information (0-10)
                - helpfulness: Overall helpfulness (0-10)
                - efficiency: Efficiency of resolution (0-10)
                - clarity: Clarity of explanation (0-10)
                - overall_csat: Overall CSAT score (0-10)
                - reasoning: Explanation of scores
        """
        # Build conversation text
        conversation_text = self._format_conversation(conversation_history)

        # Build evaluation prompt
        prompt = f"""You are an expert evaluator assessing a customer service conversation.

**Scenario:**
{scenario['user_scenario']}

**Reference Answer (Ground Truth):**
{scenario['reference_text']}

**Actual Conversation:**
{conversation_text}

**User Satisfaction:** {"Satisfied (ended with ###STOP###)" if user_satisfied else "Not Satisfied"}

Please evaluate the agent's performance on the following dimensions (0-10 scale):

1. **Accuracy (정확성)**: Did the agent provide factually correct information compared to the reference answer?
2. **Completeness (완전성)**: Did the agent cover all key information from the reference answer?
3. **Helpfulness (도움성)**: Was the agent's response helpful in solving the user's problem?
4. **Efficiency (효율성)**: Did the agent resolve the issue efficiently without unnecessary back-and-forth?
5. **Clarity (명확성)**: Were the agent's explanations clear and easy to understand?
6. **Overall CSAT (전체 만족도)**: Overall customer satisfaction score.

Provide your evaluation in the following JSON format:
{{
  "accuracy": <score 0-10>,
  "completeness": <score 0-10>,
  "helpfulness": <score 0-10>,
  "efficiency": <score 0-10>,
  "clarity": <score 0-10>,
  "overall_csat": <score 0-10>,
  "reasoning": "<brief explanation of scores>"
}}

Be strict but fair. Consider:
- Whether the agent used search tools effectively
- Whether key information from reference was mentioned
- Whether the conversation flow was natural and efficient
"""

        try:
            # GPT-5 only supports temperature=1
            temperature = 1.0 if "gpt-5" in self.model else 0.3
            
            # Prepare completion params
            completion_params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are an expert customer service evaluator."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
                # "max_tokens": 800,
                "response_format": {"type": "json_object"},
            }
            
            # Add reasoning_effort for o1/o3 models
            if any(model in self.model for model in ["o1", "o3", "gpt-5"]):
                completion_params["reasoning_effort"] = "high"  # Judge uses high effort for accuracy
            
            response = completion(**completion_params)
            # import pdb; pdb.set_trace()

            result = self._parse_judge_response(response.choices[0].message)

            # Ensure all keys exist
            required_keys = [
                "accuracy",
                "completeness",
                "helpfulness",
                "efficiency",
                "clarity",
                "overall_csat",
                "reasoning",
            ]
            for key in required_keys:
                if key not in result:
                    result[key] = 0.0 if key != "reasoning" else "Evaluation failed"

            return result

        except Exception as e:
            print(f"❌ Judge evaluation failed: {e}")
            return {
                "accuracy": 0.0,
                "completeness": 0.0,
                "helpfulness": 0.0,
                "efficiency": 0.0,
                "clarity": 0.0,
                "overall_csat": 0.0,
                "reasoning": f"Evaluation error: {str(e)}",
            }

    def _parse_judge_response(self, message: Any) -> Dict:
        """Parse judge response, handling structured outputs from different models."""
        parsed_payload = getattr(message, "parsed", None)

        if parsed_payload is not None:
            if isinstance(parsed_payload, dict):
                return parsed_payload
            if isinstance(parsed_payload, list) and parsed_payload and isinstance(parsed_payload[0], dict):
                return parsed_payload[0]
            if hasattr(parsed_payload, "dict"):
                return parsed_payload.dict()
            if isinstance(parsed_payload, str):
                try:
                    return json.loads(parsed_payload)
                except json.JSONDecodeError:
                    pass

        content = getattr(message, "content", "") or ""

        if isinstance(content, list):
            extracted_parts: List[str] = []
            for part in content:
                if not isinstance(part, dict):
                    continue

                part_type = part.get("type")
                if part_type in {"text", "output_text"}:
                    extracted_parts.append(part.get("text", ""))
                elif part_type == "tool_result":
                    # tool_result payloads are dicts; try to pull text field if present
                    if isinstance(part.get("content"), list):
                        for inner in part["content"]:
                            if isinstance(inner, dict) and inner.get("type") in {"text", "output_text"}:
                                extracted_parts.append(inner.get("text", ""))
                elif part_type == "message" and "content" in part:
                    extracted_parts.append(str(part["content"]))

            content = "".join(extracted_parts)

        if not isinstance(content, str):
            raise ValueError("Unsupported judge response content type")

        content = content.strip()
        if not content:
            raise ValueError("Judge response did not contain any content")

        content = self._extract_json_blob(content)

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Judge returned invalid JSON: {content}") from exc

    def _format_conversation(self, conversation_history: List[Dict]) -> str:
        """Format conversation history for evaluation."""
        lines = []
        for entry in conversation_history:
            turn = entry.get("turn", 0)
            lines.append(f"\n[Turn {turn}]")

            # Tool calls
            if entry.get("tool_calls"):
                for tool_call in entry["tool_calls"]:
                    lines.append(f"🔧 Agent used tool: {tool_call['tool']}")
                    lines.append(f"   Query: {tool_call['query']}")

            # Agent message
            agent_msg = entry.get("agent", "")
            if agent_msg and not agent_msg.startswith("[검색 수행:"):
                lines.append(f"Agent: {agent_msg}")

            # User message
            if entry.get("user"):
                lines.append(f"User: {entry['user']}")

        return "\n".join(lines)

    def _extract_json_blob(self, text: str) -> str:
        """Return JSON object substring, removing code fences when present."""
        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines)

        match = re.search(r"{.*}", text, re.DOTALL)
        return match.group(0) if match else text

    def calculate_reward(self, evaluation: Dict) -> float:
        """
        Calculate normalized reward from evaluation.

        Args:
            evaluation: Evaluation dict from evaluate_conversation

        Returns:
            Reward score between -1 and 1
        """
        # Use weighted average of metrics
        weights = {
            "accuracy": 0.25,
            "completeness": 0.25,
            "helpfulness": 0.2,
            "efficiency": 0.15,
            "clarity": 0.15,
        }

        weighted_score = sum(
            evaluation.get(metric, 0) * weight for metric, weight in weights.items()
        )

        # Normalize to [-1, 1] range
        # 0-10 scale -> map 0-5 to [-1, 0] and 5-10 to [0, 1]
        if weighted_score < 5:
            reward = (weighted_score - 5) / 5  # Maps 0-5 to -1-0
        else:
            reward = (weighted_score - 5) / 5  # Maps 5-10 to 0-1

        return reward
