---
title: RAG
path: AI반복되는 문의는 줄이고, 진짜 중요한 문제에 집중할 수 있는 AI 기능들을 소개합니다.12개의 아티클 > 고객 ALF매니저를 대신해 고객의 문의에 먼저 답변하는 채널톡의 고객 ALF에 대해 안내드려요8개의 아티클 > RAGALF가 도큐먼트 혹은 FAQ 데이터를 참조하여 고객 응대 시 활용하는 기능이에요.
source_url: https://docs.channel.io/help/ko/articles/RAG-90e99c8b
crawled_at: 2025-10-21 23:24:04
---

# RAG

**영상으로 배우고 싶다면?**

[ALF가 참조할 문서 만들기 - 아티클

• 소요 시간: 10-20분 • 난이도: 하

![아티클](https://cf.channel.io/thumb/200x200/pub-file/1/65fc447a2a0848daf5ec/tmp-2092756089)

아티클

![ALF가 참조할 문서 만들기 - 아티클](https://cf.channel.io/thumb/1200x630,cover,webp/web_page/1/68ad88084329d66ea94f/tmp-2587820091.png)](https://docs.channel.io/channelcampus/ko/articles/alf-article-0a1f7473)

---

[### RAG란?](#rag란?)

RAG(검색 증강 생성)는 Retrieval-Augmented Generation의 약자로, AI가 특정 데이터베이스에서 관련 정보를 검색하여 답변하는 기술이에요. 이로 인해 AI가 더 풍부하고 정교한 답변을 제공할 수 있어요.

현재 ALF는 채널톡의 문서 관리 기능인 ‘도큐먼트’와 질문과 답변을 저장하는 'FAQ'를 기반으로 답변을 생성할 수 있어요. 향후 PDF, 유저챗 등 다양한 데이터베이스를 기반으로 답변을 생성할 수 있도록 제공될 예정입니다.

* [도큐먼트 알아보기](https://docs.channel.io/help/ko/categories/83739bfc-%EB%8F%84%ED%81%90%EB%A8%BC%ED%8A%B8)
* [FAQ 알아보기](https://docs.channel.io/help/ko/articles/db21218c-FAQ)

![](https://cf.channel.io/document/spaces/6/articles/11946/revisions/38998/usermedia/66b5dc3faf8f77f2f641)

[#### RAG가 필요한 이유](#rag가-필요한-이유)

**ALF가 도큐먼트와 FAQ를 참조하여 답변해요**

ALF가 답변할 때 도큐먼트와 FAQ를 기반으로 답변을 생성하여 고객을 응대할 수 있어요. 또한 도큐먼트 스페이스별로 ALF 사용 여부와 범위를 선택하여 고객과 팀 업무에 어떤 정보를 제공하고 활용할지 컨트롤할 수 있어요. 아티클 내용만 업데이트하면 실시간으로 반영되니 더 정확하고 신뢰도 높은 정보를 제공할 수 있어요.

* [고객 ALF란?](https://docs.channel.io/help/ko/articles/%EA%B3%A0%EA%B0%9D-ALF%EB%9E%80-541f14b8)
* [팀 ALF란?](https://docs.channel.io/help/ko/articles/%ED%8C%80-ALF-c3ea989d)

![](https://cf.channel.io/document/spaces/6/articles/11946/revisions/336117/usermedia/684048428de58b081632)

**고객은 ALF 답변 정보의 출처를 확인하고 인용된 아티클을 바로 열람해요**

ALF가 FAQ를 기반으로 답변할 때는 답변의 출처로 매칭된 FAQ의 '대표 질문'이 보여요. ALF가 도큐먼트를 기반으로 답변할 때 ‘출처’와 함께 ‘아티클 링크’까지 제공해요. 고객은 인용된 부분 뿐 아니라 아티클 전문을 열람할 수 있어 아티클을 통해 직접 궁금증을 해소할 수 있어요.

![](https://cf.channel.io/document/spaces/6/articles/11946/revisions/15660/usermedia/668e727158bca5ef9463)

**매니저는 ALF 답변 시 인용된 아티클을 확인하고 바로 수정해요.**

ALF 답변에 인용된 아티클 중 업데이트가 필요한 내용이 발견되었다면, 번거롭게 다른 메뉴로 이동할 필요 없이 유저챗 화면 내에서도 실시간으로 수정하여 정보를 최신화할 수 있어요.

![](https://cf.channel.io/document/spaces/6/articles/11946/revisions/15660/usermedia/668fa0cdce3168ea8527)

[### 활용하기](#활용하기)

[#### 사전 준비](#사전-준비)

RAG는 도큐먼트에 등록된 아티클 내용 또는 FAQ에 등록한 질문과 답변을 기반으로 ALF가 답변하는 기능이기에 사전에 아티클과 FAQ 중 하나라도 등록되어야 합니다.

* [아티클 등록하기](https://docs.channel.io/help/ko/articles/be177b0b-%EC%95%84%ED%8B%B0%ED%81%B4-%EC%9E%91%EC%84%B1%ED%95%98%EA%B8%B0)
* [FAQ 등록하기](https://docs.channel.io/help/ko/articles/db21218c-FAQ#%EC%83%9D%EC%84%B1-%EB%B0%A9%EB%B2%95)

[#### 사용 설정](#사용-설정)

1. **ALF 활성화하기**

   * 워크플로우 설정 시 원하는 단계에 '고객 ALF 응대' 액션을 추가해 주세요. (→ [워크플로우 설정 가이드 보기](https://docs.channel.io/help/ko/categories/25f373c1-%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%9A%B0-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0))

![](https://cf.channel.io/document/spaces/6/usermedia/66c2d0f5f233725e0d05)

2. **AI 설정하기**

   * [AI] - [고객 ALF] - [설정] - [ALF 기본 설정] - [아티클로 답변] / [FAQ로 답변] 설정
   * 채널 내의 도큐먼트 아티클과 FAQ를 기반으로 ALF가 답변할지 설정할 수 있어요.

![](https://cf.channel.io/document/spaces/6/articles/11946/revisions/336117/usermedia/68404750e5ba9670130b)

3. **도큐먼트 스페이스 별 ALF 설정하기**

* [도큐먼트] - [스페이스 설정] - [일반] - [ALF 사용] - [고객 ALF / 팀 ALF] 활성화

  * 도큐먼트 내 스페이스 별로 ALF 참조 여부와, 범위 (고객 ALF 또는 팀 ALF)를 설정할 수 있어요.
* 웹사이트와 아티클이 모두 공개 상태여야 ALF가 해당 아티클을 참조하여 답변할 수 있어요.

![](https://cf.channel.io/document/spaces/6/articles/11946/revisions/336117/usermedia/68404814d2e68acd9969)

[### **자주 묻는 질문**](#자주-묻는-질문)

**ALF가 도큐먼트 내 이미지를 읽고 답변에 참조할 수 있나요?**

ALF가 도큐먼트 아티클에 기재된 이미지를 인식하고 이미지 내용을 바탕으로 고객에게 답변할 수 있어요. ALF가 답변 가능한 이미지 파일 확장자는 png, jpg, webp, gif (non-animated)입니다.

단, 이미지만 첨부되어 있고 관련 설명이 하나도 없다면 알프가 참조하여 답변을 할 수 없어요.

아티클에 이미지와 함께 관련 설명이 함께 기재되어 있어야 이미지를 알프가 잘 참조하여 답변을 할 수 있어요. 어떤 상황과 맥락에서 이용이 되는 이미지인지 인지할 수 있는 텍스트 설명도 함께 기재해 주세요.

예를 들어,

* 도큐먼트 아티클에 채널에 팀원을 초대하는 방법에 대한 이미지와 텍스트 설명이 기재되어 있다면
* 고객이 팀원을 초대 하는 방법을 물어보았을 때, 알프가 이미지를 읽고 고객에게 경로를 안내해 줄 수 있어요.

[(→ 이미지 답변 활용 예시 더 보러가기)](https://channel.io/ko/blog/articles/7cbf988a)