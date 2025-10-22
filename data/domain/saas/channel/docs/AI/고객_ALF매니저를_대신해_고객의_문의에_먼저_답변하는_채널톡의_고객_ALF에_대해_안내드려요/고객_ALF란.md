---
title: 고객 ALF란?
path: AI반복되는 문의는 줄이고, 진짜 중요한 문제에 집중할 수 있는 AI 기능들을 소개합니다.12개의 아티클 > 고객 ALF매니저를 대신해 고객의 문의에 먼저 답변하는 채널톡의 고객 ALF에 대해 안내드려요8개의 아티클 > 고객 ALF란?고객 ALF의 정의와 설정 방법에 대해 안내드려요
source_url: https://docs.channel.io/help/ko/articles/%EA%B3%A0%EA%B0%9D-ALF%EB%9E%80-541f14b8
crawled_at: 2025-10-21 23:24:00
---

# 고객 ALF란?

**영상으로 배우고 싶다면?**

[ALF 완전정복 입문 코스

• 소요시간: 80분 • 난이도: 중-하 • 추천 대상: AI 를 통해 상담 효율화를 시작하고 싶은 분

![](https://cf.channel.io/thumb/200x200/pub-file/1/65fc447a2a0848daf5ec/tmp-2092756089)

![ALF 완전정복 입문 코스](https://cf.channel.io/thumb/1200x630,cover,webp/web_page/1/68ad87527c4582282495/tmp-1218438787.png)](https://docs.channel.io/channelcampus/ko/categories/ALF-완전정복-입문-코스-3e453b22)

---

[### 고객 ALF란?](#고객-alf란?)

고객 ALF는 고객의 문의를 이해하고 단순 문의를 대신 답변해 주는 채널톡의 AI 기능입니다. 상황에 따라 고객에게 필요한 기능을 스스로 제안할 수 있어요.

![](https://cf.channel.io/document/spaces/6/articles/23708/revisions/34564/usermedia/66b0d7326f8b7ab9c2f3)

* 기존에는 상담원이 확인하고 처리해야 했던 일들을 상담원 연결 전 ALF가 직접 응대합니다. 상담원은 단순 문의를 줄이고 시간을 확보할 수 있어요.
* 아래에 설명드리는 FAQ 커맨드, FAQ, RAG 들을 ALF가 직접 활용해서 상담을 미리 처리할 수 있어요.

[### 핵심 용어 정리](#핵심-용어-정리)

고객 ALF 더 잘 이해하고 활용하실 수 있도록 관련된 중요 용어들을 먼저 알려드릴게요.

* **커맨드** : 커맨드는 특정 작업을 수행할 수 있도록 하는 ‘명령어’입니다.

  * ALF가 커맨드 중에서 고객의 문의 내용을 처리하는 데 적합한 커맨드를 선택해 자동으로 대답할 수도 있고,
  * 고객이 / (슬래시) + 명령어를 입력해 커맨드를 수동으로 이용할 수도 있습니다.
* **카페24 허브** : 다양한 커맨드로 구성된 앱 중 하나로, ALF가 고객이 직접 주문 정보(주문 취소, 주문 목록, 발송 예정일 등)를 확인할 수 있게 하는 기능이에요. (→ [카페24 허브 가이드 확인하기)](https://docs.channel.io/help/ko/articles/657238c6)

![](https://cf.channel.io/document/spaces/6/usermedia/66b0d838317357bf1c24)

* **FAQ :** 고객이 자주 묻는 질문과, 질문에 대한 답변을 등록해 두시면 ALF가 대신 답변합니다. (→ [FAQ 가이드 보러 가기)](https://docs.channel.io/help/ko/articles/db21218c)

![](https://cf.channel.io/document/spaces/6/articles/45127/revisions/80294/usermedia/671f22a08e5ac97cd5fd)

* **RAG(검색 증강 생성)** : AI가 고객이 문의한 내용이 미리 등록된 매뉴얼(문서 또는 가이드)에 있는지 검색하고, 답변을 생성해 주는 기능이에요. (→ [RAG 가이드 보러 가기](https://docs.channel.io/help/ko/articles/90e99c8b-RAG))

![](https://cf.channel.io/document/spaces/6/articles/45127/revisions/80294/usermedia/671f22adb3ab76bc9a2e)

[### 고객 ALF 사용하기](#고객-alf-사용하기)

[#### 기본 설정](#기본-설정)

[AI 메뉴] - [고객 ALF] - [홈]에서 가이드와 튜토리얼, 성공사례를 참고하신 다음, [설정] 메뉴에서 기본적인 ALF 설정을 먼저 진행해 주세요. ([→ ALF 설정 가이드 보러 가기](https://docs.channel.io/help/ko/articles/ALF-%EC%84%A4%EC%A0%95-cb9b6a7a))

![](https://cf.channel.io/document/spaces/6/articles/45127/revisions/295892/usermedia/6821baa351f734ce0e4f)

[#### 활성화하기](#활성화하기)

* 고객 ALF는 워크플로우의 '액션'으로 활성화할 수 있기 때문에, 유료 플랜 + 워크플로우를 사용해야 설정이 가능합니다.
* 워크플로우 단계마다 ALF 사용 여부를 설정할 수 있습니다.

  * 활용 예시

    * 배송문의 같은 단순 문의에는 ALF 사용을 ON으로 설정하고,
    * 도입문의 같이 상담이 필요한 단계라면 ALF 사용을 OFF 해두시면 됩니다.

[ALF 사용 설정하기 - 워크플로우 연결

• 소요 시간: 10분 • 난이도: 중

![워크플로우 연결](https://cf.channel.io/thumb/200x200/pub-file/1/65fc447a2a0848daf5ec/tmp-2092756089)

워크플로우 연결

![ALF 사용 설정하기 - 워크플로우 연결](https://cf.channel.io/thumb/1200x630,cover,webp/web_page/1/68a2cb4f2ee114cc8eba/tmp-2309710135.png)](https://docs.channel.io/trainingcenter/ko/articles/alf-workflow-6810d35b)

![](https://cf.channel.io/document/spaces/6/articles/45127/revisions/295892/usermedia/6821bbd84669ec83bbd4)

[#### 유의사항](#유의사항)

* ALF는 생성형 AI로, 일부 부정확한 답변이 생성될 수 있어요. 민감한 내용은 담당자가 직접 안내하는 것을 권장합니다.

[### 고객 ALF 작동 알림 받기](#고객-alf-작동-알림-받기)

고객 ALF가 동작하는 단계에서 팀챗 메시지로 알림을 받아볼 수 있어요. 알림의 유저챗 링크를 클릭하여 ALF가 어떻게 상담하고 있는지 확인해 보세요.

상담 별 알림이 아닌 ALF가 보낸 메시지 별로 확인하고자 하신다면, [채널 설정] - [고객 ALF] - [ALF 통계]를 참고하실 수도 있습니다. (→ [ALF 통계 가이드 보러 가기](https://docs.channel.io/help/ko/articles/ALF-%ED%86%B5%EA%B3%84-dd674698))

![](https://cf.channel.io/document/spaces/6/articles/23708/revisions/34564/usermedia/66b0ddb7b88ac2d9653e)

1. 알림 받을 팀챗 내 그룹방 생성하기

   * 설정 경로: [팀챗] - [공개 그룹] - [+ 버튼] - [새 그룹 생성]

2. 워크플로우에서 ALF를 사용한 단계에 [액션] 설정하기

   * 설정 경로: [워크플로우] - [액션] - [팀챗 메시지 보내기]

   ![](https://cf.channel.io/document/spaces/6/articles/23708/revisions/38195/usermedia/66b4d3133fa5c094b706)

3. 알림을 모아 볼 공개 그룹을 선택 후, 알림과 함께 전달할 메시지가 있다면 함께 작성해 주세요.

![](https://cf.channel.io/document/spaces/6/usermedia/66b0dde83f28f8876047)

4. 고객 ALF가 실행될 때 알림이 전송됩니다.

![](https://cf.channel.io/document/spaces/6/usermedia/66b0ddfbb7e95ce1d37c)

[### ALF 미리보기](#alf-미리보기)

[AI 메뉴] - [고객 ALF] - [홈] 또는 [설정] 화면 우측 ALF 미리보기를 통해 과금없이 ALF를 테스트해볼 수 있어요.

[ALF 사용 설정하기 - 테스트하기

• 소요 시간: 5분 • 난이도: 하

![테스트하기](https://cf.channel.io/thumb/200x200/pub-file/1/65fc447a2a0848daf5ec/tmp-2092756089)

테스트하기

![ALF 사용 설정하기 - 테스트하기](https://cf.channel.io/thumb/1200x630,cover,webp/web_page/1/68a2cb095fed525e44b3/tmp-3623427833.png)](https://docs.channel.io/trainingcenter/ko/articles/alf-test-b5b85827)

![](https://cf.channel.io/document/spaces/6/articles/45127/revisions/488348/usermedia/68a2cb14b92d0e32a315)

* ALF 미리보기에서도 FAQ와 아티클을 참조하여 답변할 수 있습니다.

  * [AI 메뉴] - [고객 ALF] - [설정] - [ALF 기본 설정]에서 FAQ로 답변 및 아티클로 답변이 켜져있어야 하며 FAQ와 아티클이 공개 상태여야 합니다.
* 커맨드를 이용 중이라면 ALF 미리보기에서도 커맨드 목록을 추천할 수 있지만, 실제 커맨드는 동작하지 않습니다.
* 역할 설명, 맞춤형 설명 변경 후 저장하지 않은 상태에서도 테스트 해보실 수 있습니다.
* ALF 미리보기는 상담원 연결을 허용하지 않는 버전으로 동작합니다.