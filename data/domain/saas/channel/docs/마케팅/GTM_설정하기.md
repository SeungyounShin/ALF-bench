---
title: GTM 설정하기
path: 마케팅채널톡 마케팅 기능을 통해 고객에게 먼저 메시지를 보낼 수 있습니다. 쉽고 강력한 채널톡 마케팅 기능을 확인해보세요.9개의 아티클 > GTM 설정하기Google Tag Manager를 사이트에 설치하면, 다양한 마케팅 메시지를 설정할 수 있어요.
source_url: https://docs.channel.io/help/ko/articles/GTM-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0-a7f86e26
crawled_at: 2025-10-21 23:23:26
---

# GTM 설정하기

**GTM(Google Tag Manager)이란?**

구글 태그 매니저(GTM)는 구글(Google) 마케팅 플랫폼에서 제공하는 무료 서비스의 하나로, 코드를 수정하지 않고도 웹사이트에 심어진 태그를 관리하는 툴입니다. 다양한 마케팅을 뒷받침하는 강력한 도구에요.

[####](#)

**채널톡은 왜 GTM을 소개하나요?**

* 마케팅 캠페인을 만들 때 **시작 이벤트** 또는 추가 이벤트를 다양하게 설정할 수 있기 때문이에요.
* 특히, 빌더사 홈페이지에서 연동되는 고객 정보보다 더 많은 고객의 행동을 추적할 수 있게 도와줍니다. (예: 페이지 70% 스크롤 다운, 장바구니 버튼 클릭 등)

**참고 페이지**

* [구글 태그 매니저 공식 소개 확인하기](https://marketingplatform.google.com/intl/ko/about/tag-manager/)
* [구글 태그 매니저 공식 도움말 보러가기](https://support.google.com/tagmanager#topic=3441530)

[### GTM 설치하기](#gtm-설치하기)

GTM을 이용하려면, 채널톡을 설치한 사이트에 GTM을 설치해야 해요. 아래 과정을 따라 GTM을 설치해 주세요.

[#### 홈페이지에 GTM 설치하기](#홈페이지에-gtm-설치하기)

1. [태그 관리자 페이지에 로그인하신 다음 [계정 만들기] 버튼을 눌러주세요.](https://tagmanager.google.com/)

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112613931fed8f52)
2. 계정 정보를 입력해 주세요.

   * 계정 설정 : 기본적인 계정 내용을 기재해 주시면 됩니다.
   * 컨테이너 설정

     * 컨테이너는 하나의 작업 환경이라고 생각해 주시면 됩니다. 하나의 계정에 여러 개의 컨테이너를 만들 수 있어요. 작업자 또는 웹/앱 환경 별로 여러 개의 컨테이너를 만들 수 있어요.
     * 타겟 플랫폼은 웹사이트에 설치되기 때문에 '웹'으로 설정해 주시면 됩니다.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b11264ba9e64c5638)
3. 생성된 계정의 고유한 GTM 스크립트를 홈페이지 사이트에 삽입해 주세요.

   * 카페24 빌더사를 이용 중이시라면

     [쇼핑몰 설정] - [기본 설정] - [쇼핑몰 정보] - [검색 엔진 최적화(SEO)] - [고급 설정] - 코드 직접 입력’에 각각 head 영역, body 영역을 추가해 주시면 됩니다.

     ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1126767f520030ac)
   * 아임웹 빌더사를 이용 중이시라면

     [환경설정] - [SEO, 헤더 설정] 메뉴 내 ‘공통 코드 삽입’에서 Header Code, Body Code를 각각 입력해 주시면 됩니다.

     ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1126b4887c6a97bb)

[#### GTM에서 채널톡 템플릿 설치하기](#gtm에서-채널톡-템플릿-설치하기)

1. [템플릿] - [태그 템플릿] 영역 우측 상단 [갤러리 검색]을 눌러주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1126ec405422d9da)
2. 우측 상단 검색 아이콘을 눌러 ‘channel.io’를 찾은 다음, [작업 공간에 추가] 버튼을 눌러 템플릿을 추가해 주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b11273ee3bc752da6)
3. 추가되면 아래와 같이 보여집니다.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1127739d8d7fb810)

[### 트리거 설정하기](#트리거-설정하기)

트리거는 이벤트가 동작할 수 있는 실행 “조건”이에요.

예를 들어, ‘장바구니 담기’ 이벤트를 채널톡으로 보내기 위해서는 고객이 [장바구니] 버튼을 클릭해야 해요. ‘페이지 접속’ 이벤트는 고객이 페이지에 접속해야 발생하게 되어요. 고객이 장바구니 버튼을 클릭하는 것, 고객이 페이지에 접속하는 것을 트리거라고 생각해 주시면 됩니다.

채널톡에서 잘 활용할 수 있는 트리거는 스크롤(Scroll)트리거와 클릭(Click) 트리거가 있어요.

[#### 스크롤 트리거 만들기](#스크롤-트리거-만들기)

스크롤 트리거는 고객이 '스크롤' 행동을 추적하여 활용하는 트리거에요. 예를 들면, 고객이 ‘페이지의 스크롤을 25% 정도 내렸을 때’를 타겟할 수 있어요.

1. 왼쪽 트리거 메뉴 선택 → [새로 만들기]를 눌러주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1127a5e5ae8255f6)
2. 트리거의 이름을 입력한 다음, 트리거 구성 영역을 클릭 → 트리거 유형 중 "스크롤 깊이"를 선택해 주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1127d2394c733bad)
3. 세로 또는 가로 스크롤 깊이를 선택하고, 트리거 실행 조건 및 페이지 동작 조건을 설정 후 저장해 주세요.

   아래와 같이 설정했다면, GTM을 설치한 웹사이트의 모든 페이지에서 고객이 세로로 스크롤을 25% 정도 내렸을 때 트리거가 동작합니다.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b11280e1a07d5a328)

[#### 클릭 트리거 만들기](#클릭-트리거-만들기)

클릭 트리거는 고객의 '클릭'하는 행동을 추적하여 활용해요. 예를 들면, 고객이 ‘특정 버튼을 클릭했을 때’를 타겟 할 수 있어요.

클릭 트리거를 만들기 위해서는 클릭할 버튼 또는 영역을 특정해야 해요. 그중 많이 사용하는 것은 **url**(어떤 url 을 클릭했을 때), **class**(어떤 class 영역을 클릭했을 때), **id**(html 태그의 id 값)입니다.

사이트에서 클릭 트리거로 설정할 영역을 확인해 보면서 알아볼까요?

* 원하는 영역에서 **마우스 우클릭** → **검사**로 확인하거나
* 이용하고 계신 브라우저의 설정 → **개발자 도구** 내 Elements 항목에서 확인할 수 있어요.

예를 들어, 아래 이미지처럼 CART라는 버튼 위에서 마우스 우클릭 → 검사를 눌렀을 때 text 값과 ID 값이 확인되어요. text 값은 다른 영역에 같은 단어가 있을 경우 제대로 동작하지 않을 수 있어, ID 값으로 타겟하는 것을 권장 드리고 있어요.

* id 값을 활용한다면 : actionCart 값을 이용하면 됩니다.
* class 값이 확인된다면, 띄어쓰기 없이 완전한 형태의 값을 기재해 주셔야 해요(ex. sub\_cart).

자세한 내용은 아래 예시를 통해 설명드릴게요.

![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1128368209b1bb22)

[### 이벤트 만들어보기](#이벤트-만들어보기)

생성해 둔 트리거를 태그로 만들어야 채널톡 이벤트로 보낼 수 있는데요, 태그는 트리거가 발생했을 때 어떤 액션을 취할 것인지에 대한 “내용”이에요.

앞서 고객이 장바구니 버튼을 클릭해서 트리거가 동작(이벤트가 발생) 했다면, 이 이벤트를 전송해 주는 기능을 태그가 하게 됩니다.

앞서 만들어본 스크롤 트리거와 클릭 트리거를 태그로 만들어 이벤트로 설정해 볼까요?

[#### 우리 제품을 관심 있게 본 고객에게 말 걸기](#우리-제품을-관심-있게-본-고객에게-말-걸기)

'고객이 상품 페이지에서 스크롤을 30% 정도 내렸을 때'에 대한 이벤트를 생성해 봅시다.

[#### 1. 스크롤 트리거 생성하기](#1.-스크롤-트리거-생성하기)

1. 왼쪽 트리거 메뉴 선택 → [새로 만들기]를 눌러주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b11286b9ddd531081)
2. 트리거의 이름을 입력한 다음, 트리거 구성 영역을 클릭 → 트리거 유형 중 "스크롤 깊이"를 선택해 주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b11289b1c9fb8b762)
3. 세로 스크롤 깊이 30%를 선택, 트리거 실행 조건은 창 로드(gtm load)로 설정해 주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1128d260763aad88)

[#### 2. 태그 설정하기](#2.-태그-설정하기)

1. 태그 메뉴 선택 → 우측 [새로 만들기] 버튼을 눌러주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1129336f71412e7f)
2. 태그의 이름을 입력한 다음, 태그 구성 영역을 클릭 → 태그 유형 중 Channel.io 템플릿을 선택해 주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b11296494d7ebee86)
3. 아래와 같이 내용을 채워주세요

   * Action : 행동을 추적해서 보낼 수 있도록 **Track(Send Event)**로 설정해 주세요.
   * Event Name : 이벤트 내용을 알아보기 쉽게 설정해 주세요. (ex. scroll30)
   * Event Property

     * Key에는 url , Value 값은 옆의 더하기 표시를 눌러 Page URL 을 추가해 주세요.

     → 이렇게 하면 이벤트가 채널톡으로 보내질 때, 어떤 url에서 발생한 것인지 알 수 있어요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112995dd9cfeb7f9)

[#### 3. 트리거 선택하기](#3.-트리거-선택하기)

앞서 만들어 둔 스크롤 트리거를 불러와주신 다음, 저장하면 완성된 이벤트를 확인할 수 있어요.

![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b1129d3e72f29ff57)

[#### 4. 미리보기 및 제출하기](#4.-미리보기-및-제출하기)

새 창으로 열리는 나의 데모 사이트에서 실제로 이벤트를 발생시켜 보실 수 있어요.

미리보기를 누르면 Tag Assistant 창이 열리는데, 이때 GTM이 설치된 웹사이트 주소를 입력하고 connect를 누르면 됩니다.

![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112a0b7f0670bb0f)

* 연결이 완료되면 이벤트를 테스트할 수 있는 사이트가 새 창으로 열리게 되어요.
* 지정했던 트리거 행동을 직접 실행해 보세요.
* 실제로 트리거가 잘 작동하면, Tags Not Fired → Fired로 이동하게 됩니다.

![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112a3b4c31f910e5)

미리보기 테스트를 완료하셨다면, 원래 창으로 돌아와 [제출] 버튼을 눌러주세요. 필요에 따라 버전 정보를 입력한 후, 게시를 누르면 적용이 완료됩니다.

![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112a7082ab07d2a8)

[#### 5. 캠페인 설정하기](#5.-캠페인-설정하기)

마케팅 시작 이벤트 목록에서 앞서 설정했던 이벤트를 시작 이벤트로 설정한 다음, 메시지를 작성해 퍼블리시 해주시면 됩니다.

설정한 메시지는 고객이 사이트에서 스크롤을 30% 내렸을 때 전송되게 되어요.

* 게시 직후 바로 채널톡 시작 이벤트에서 확인되지는 않습니다.
* 채널톡 마케팅 이벤트 목록에 보여지려면, 실제로 사이트에서 이벤트가 발생해야 해요. 목록에서 보일 수 있도록 트리거 행동을 계속 진행해 주세요.

![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112aa90b2e1044d4)

[#### 장바구니에 물건을 담은 고객에게 메시지 보내기](#장바구니에-물건을-담은-고객에게-메시지-보내기)

'고객이 [장바구니] 버튼을 클릭했을 때'에 대한 이벤트를 생성해 봅시다.

[#### 1. 클릭 트리거 생성하기](#1.-클릭-트리거-생성하기)

1. 트리거의 이름을 입력한 다음, 트리거 구성 영역을 클릭 → 트리거 유형 중 "모든 요소"를 선택해 주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112ae43af7d51d05)
2. 트리거 구성 내용을 설정해 주세요.

   1. '일부 클릭'을 선택
   2. 확인한 값을 선택해 **포함 또는 같음** 조건으로 추가
   3. 저장 버튼을 눌러 저장

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112b1e7db959c2d8)

   만약 버튼에서 ID 값이 확인되었다면, Click ID를 선택하고 우측에 ID 값을 입력해 주시면 되고, class 값이 확인되었다면 class값을 입력해 주시면 되어요.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112b61ecc407ca59)

   Click 요소가 목록에서 보이지 않는다면, 아래 '기본 제공 변수 선택'을 눌러 Click 요소를 선택해 주시면 됩니다.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112baf6462e13568)

[#### 2. 태그 설정하기](#2.-태그-설정하기)

1. 태그의 이름을 설정해 주세요.
2. 태그 구성 내용을 작성해 주세요.

   * 태그 유형 : Channel.io 템플릿을 선택해 주세요.
   * Action : 행동을 추적해서 보낼 수 있도록 **Track(Send Event)**로 설정해 주세요.
   * Event Name : 영어와 숫자로 알아보기 쉽게 설정해 주세요.
   * Event Property

     * Key에는 url , Value 값은 옆의 더하기 표시를 눌러 Page URL 을 추가해 주세요.
3. 앞서 설정했던 Click 트리거를 불러와 주세요.
4. 우측 상단의 저장 버튼을 눌러 생성해 주시면 됩니다.

   ![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112c54225b7abb1a)

[#### 3. 미리보기 및 제출하기](#3.-미리보기-및-제출하기)

위에서 살펴본 "우리 제품을 관심 있게 본 고객에게 말 걸기" 케이스의 '4. 미리보기 및 제출하기' 와 동일합니다.

[#### 4. 캠페인 메시지 설정하기](#4.-캠페인-메시지-설정하기)

마케팅 시작 이벤트 목록에서 앞서 설정했던 이벤트를 시작 이벤트로 설정한 다음, 메시지를 작성해 퍼블리시 해주시면 됩니다.

설정한 메시지는 고객이 장바구니 담기 버튼을 눌렀을 때 전송되게 되어요.

![](https://cf.channel.io/document/spaces/6/articles/35/revisions/100/usermedia/662b112c81f7da4f757e)