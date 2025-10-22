# ALF-Bench: Customer Service Agent Benchmark

현실적인 Customer Service Agent 벤치마크. RAG, multi-turn 대화, tool 사용, 그리고 multimodal 상호작용에 초점을 맞춥니다.

## 🎯 연구 목표

기존 벤치마크(TAU2, VITA)와 달리, 실제 고객 서비스 환경에서 가장 많이 발생하는 **RAG 기반 문의 응대**에 집중:

- **RAG (Retrieval-Augmented Generation)**: 문서 검색을 통한 정확한 답변
- **Multi-turn Conversations**: 실제 상담처럼 여러 턴의 대화
- **Tool Use**: `search_data` 도구를 활용한 문서 검색
- **Multi-modal**: 텍스트뿐만 아니라 이미지 캡처 등 다양한 입력 (계획)

## 📊 연구 질문

1. **벤치마크 구축**: 현실적인 고객 서비스 시나리오 데이터셋
2. **모델 평가**: GPT-4, Gemini, Qwen 등 다양한 모델의 성능 비교
3. **LLM-as-a-Judge 검증**: LLM이 평가한 CSAT vs 실제 CSAT의 신뢰성
4. **추가 변인**: 어떤 요소가 벤치마크 신뢰성에 영향을 미치는가?

## 🏗️ 프로젝트 구조

```
alf-bench/
├── data/
│   └── domain/
│       └── saas/
│           └── channel/
│               ├── docs/              # 크롤링된 채널톡 문서 (계층 구조)
│               └── user_scenario.json # 시나리오 정의
├── crawlers/
│   └── channel_crawler.py             # 채널톡 문서 크롤러
├── envs/
│   ├── channel_env.py                 # RL-style Environment
│   ├── tools.py                       # RAG tool (search_data)
│   └── user_simulator.py              # User 시뮬레이터
├── test_env.py                        # 환경 테스트 스크립트
├── pyproject.toml                     # 프로젝트 설정
└── README.md
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# Python 3.10+ 필요
uv sync

# OpenAI API 키 설정 (GPT 모델 사용 시)
export OPENAI_API_KEY='your-key-here'
```

### 2. 문서 크롤링 (선택사항)

이미 크롤링된 문서가 포함되어 있지만, 최신 문서를 다시 크롤링하려면:

```bash
./run_crawler_v2.sh
```

### 3. 환경 테스트

```bash
uv run python test_env.py
```

## 🎮 Environment 사용법

### 기본 사용

```python
from envs import ChannelEnv

# Environment 초기화
env = ChannelEnv(
    agent_model="gpt-4o-mini",
    user_model="gpt-4o-mini",
    max_turns=10
)

# Episode 시작
state = env.reset(scenario_id="scenario_001")
print(f"User: {state['user_message']}")

# Agent-Environment 상호작용
done = False
while not done:
    # Agent의 action
    action = {
        "message": "답변 메시지",
        "tool_calls": [...]  # 선택사항
    }
    
    # Environment step
    state, reward, done, info = env.step(action)
    
    if not done:
        print(f"User: {state['user_message']}")
```

### LiteLLM Policy 사용

```python
from litellm import completion
from envs import ChannelEnv

env = ChannelEnv()
state = env.reset()

# LiteLLM으로 Agent 정책 생성
messages = [
    {"role": "system", "content": "당신은 채널톡 상담원입니다."},
    {"role": "user", "content": state["user_message"]}
]

response = completion(
    model="gpt-4o-mini",
    messages=messages,
    tools=env.get_available_tools(),
    temperature=0.7
)

# Policy를 action으로 전달
action = {"policy": response}
state, reward, done, info = env.step(action)
```

### RAG Tool 사용

Environment는 자동으로 `search_data` tool을 제공합니다:

```python
tools = env.get_available_tools()
# [
#   {
#     "type": "function",
#     "function": {
#       "name": "search_data",
#       "description": "채널톡 문서에서 관련 정보를 검색합니다.",
#       "parameters": {...}
#     }
#   }
# ]

# LiteLLM이 tool을 호출하면 자동으로 처리됨
response = completion(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

action = {"policy": response}
state, reward, done, info = env.step(action)
# info['tool_results']에 검색 결과 포함
```

## 📝 시나리오 구조

`data/domain/saas/channel/user_scenario.json`:

```json
{
  "scenarios": [
    {
      "scenario_id": "scenario_001",
      "difficulty": "easy",
      "category": "채널톡_설치",
      "user_scenario": "User LLM에게 주는 instruction",
      "reference_text": "Agent 평가를 위한 정답 내용",
      "source_documents": ["참조 문서 경로"]
    }
  ]
}
```

## 🔧 Environment API

### `ChannelEnv`

**초기화**:
```python
env = ChannelEnv(
    scenario_file="data/domain/saas/channel/user_scenario.json",
    docs_dir="data/domain/saas/channel/docs",
    agent_model="gpt-4o-mini",
    user_model="gpt-4o-mini",
    max_turns=10
)
```

**메서드**:
- `reset(scenario_id=None)`: Episode 시작, 초기 state 반환
- `step(action)`: Action 실행, (state, reward, done, info) 반환
- `get_available_tools()`: 사용 가능한 도구 목록 반환
- `render(mode="human")`: 현재 상태 출력

**State 구조**:
```python
{
    "scenario": {
        "id": "scenario_001",
        "difficulty": "easy",
        "category": "채널톡_설치"
    },
    "user_message": "사용자 메시지",
    "conversation_history": [...],
    "turn": 3
}
```

**Action 구조**:
```python
# 방법 1: 직접 메시지
action = {
    "message": "답변 내용"
}

# 방법 2: LiteLLM policy 사용 (권장)
action = {
    "policy": litellm_response_object
}
```

**Reward**:
- `1.0`: 사용자 만족, 성공
- `0.0`: 중간 턴
- `-1.0`: 최대 턴 도달, 사용자 불만족

## 📚 참고 자료

- [채널톡 공식 문서](https://docs.channel.io/help/ko)
- [LiteLLM 문서](https://docs.litellm.ai/)

## 🔬 향후 계획

- [ ] 더 많은 시나리오 추가 (현재 3개 → 50개+)
- [ ] 이미지 multimodal 지원
- [ ] 실제 CSAT 데이터 수집 및 LLM-as-a-Judge 비교
- [ ] 다양한 모델 벤치마크 결과 공개
- [ ] 다른 도메인(e-commerce, SaaS 등) 확장

## 📄 라이선스

MIT License

## 👥 Contributors

- Seungyoun Shin (robin@channel.io)
