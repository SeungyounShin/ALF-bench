---
title: SAML SSO 로그인
path: 채널 설정채널의 프로필 설정부터 보안 설정까지. 채널톡의 설정 방법에 대해 알아보세요.14개의 아티클 > 보안 패키지엔터프라이즈 급 보안으로 고객과 정보를 안전하게 보호할 수 있습니다. 조직의 계정을 한 번에 관리 가능한 통합 인증 로그인 기능과, 채널의 부정 로그인을 방지할 수 있는 IP 주소 제한이 포함된 보안 패키지를 통해 채널을 더 안전하게 관리해보세요.2개의 아티클 > SAML SSO 로그인통합 인증 로그인으로 신뢰할 수 있는 하나의 로그인 계정을 통해 여러 애플리케이션에 접근할 수 있는 중앙화된 사용자 인증 서비스입니다.
source_url: https://docs.channel.io/help/ko/articles/SAML-SSO-%EB%A1%9C%EA%B7%B8%EC%9D%B8-cd70a19d
crawled_at: 2025-10-21 23:22:06
---

# SAML SSO 로그인

[### SAML이란?](#saml이란?)

사용자가 각각의 애플리케이션에 계정과 비밀번호를 입력하지 않고도 SAML SSO 로그인을 통해 여러 애플리케이션에 로그인이 가능합니다. 사용하는 서비스 별 계정 정보를 관리하고 입력하지 않아도 되기에 관리가 쉽고, 조직의 계정을 한 번에 관리할 수 있어 사용자, 관리자 모두 편의성 및 보안성이 높습니다.

SAML SSO 로그인은 엔터프라이즈 플랜 구독 시, '보안 패키지' 기능을 별도로 선불 충전 후 사용이 가능합니다. [(→ 가격 문의하기)](https://root.channel.io/)

[### SAML SSO 로그인의 장점](#saml-sso-로그인의-장점)

* 편리합니다.

  * 구성원은 여러 서비스에서 여러 개의 계정과 비밀번호를 기억할 필요없이, ID 공급자 서비스에 등록된 하나의 계정으로 모든 서비스를 관리할 수 있습니다.
  * 관리자는 신규 구성원을 손쉽게 채널에 초대할 수 있습니다. 개별 초대 링크를 공유하지 않고 ID 공급자에 등록하는 것만으로도 채널 초대가 가능합니다.
* 보안도가 높습니다.

  * ID 공급자 ↔ 채널 간의 암호화 된 로그인 인증 방식을 활용하여, 매니저 개개인의 정보 관리 보다 높은 수준의 보안이 보장됩니다.

[### 설정 방법](#설정-방법)

![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc3437356faacef)

[#### SAML SSO 활성화](#saml-sso-활성화)

SAML SSO 로그인을 사용하기 위해서 아래 3가지 항목이 설정되어야합니다.

* 상단의 SAML SSO 버튼 활성화

  ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc36db3da9e5c8d)
* 1개 이상의 인증된 도메인 등록
* SAML SSO 설정 값 입력

[#### 도메인 등록과 인증](#도메인-등록과-인증)

**도메인 인증이 왜 필요한가요?**

SAML SSO 로그인 시, 채널의 매니저를 [이메일 도메인]으로 식별, 관리합니다. 따라서, 해당 도메인을 채널이 소유하고 있음을 증명해야 합니다.

![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc39775fdb4c7e7)

* 도메인은 1개 이상 등록이 가능합니다.

  * 도메인은 다른 채널에 중복으로 등록 가능합니다.
* 커스텀 도메인 사용이 필요해요.

  * gmail.com / naver.com 와 같은 계정은 등록이 불가합니다.

[#### SAML SSO 설정](#saml-sso-설정)

소유자 역할 혹은 보안 및 개발 권한이 제공된 매니저만 설정이 가능합니다.

![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc3c8efc81c6599)

* 채널톡에서 확인한 SSO URL / Entity ID 값을 ID 공급자에 입력해주세요.

  1. SSO URL
  2. Entity ID
* ID 공급자에서 확인한 SSO URL / ID 공급자 Entity ID / Public certificate 값을 채널톡 설정 화면에 입력해주세요.

  3. ID 공급자 SSO URL
  4. ID 공급자 Entity ID
  5. Public certificate
  * [(→ Okta에서 확인하는 방법 알아보기)](https://docs.channel.io/help/ko/articles/cd70a19d#%EC%9E%90%EC%A3%BC-%EB%AC%BB%EB%8A%94-%EC%A7%88%EB%AC%B8)

[#### 이메일 로그인 허용과 매니저 자동 초대](#이메일-로그인-허용과-매니저-자동-초대)

![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc3efe18e3ff1c8)

**이메일 로그인**

SAML SSO 로그인 방식과, 기존 이메일+비밀번호 입력 로그인 방식을 함께 사용 가능합니다. 이메일 로그인 허용을 비활성화할 경우, SAML SSO 로그인이 설정된 채널 접근이 불가합니다.

![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc4279b04158598)

이메일 로그인 허용이 비활성화 상태라도, 채널의 소유자는 이메일 로그인이 가능합니다. 이는 ID 공급자에 긴급한 문제가 생겼을 경우 채널의 사용 자체가 불가능해지는 경우를 방지하기 위함입니다. SAML SSO 로그인에 문제가 생겼을 때 소유자가 이메일 로그인을 한 뒤, SAML SSO 로그인 설정 창에서 이메일 로그인을 허용하면, 일반 매니저도 이메일 로그인이 가능합니다.

**매니저 자동 초대**

![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc45ab2db2a7cb9)

매니저 자동 초대를 활성화하여 ID 공급자에 신규 등록된 팀원이 SAML SSO 로그인을 통해 채널에 자동으로 참여할 수 있습니다. 이를 통해, 구성원을 보다 편리하게 관리할 수 있습니다.

매니저 자동 초대를 비활성화 했다면, 기존과 같이 [채널 설정 > 팀원 구성 > 매니저 > + 새 매니저 초대하기]의 초대 링크를 통해 채널에 초대가 가능합니다.

[### SAML SSO 이용하기](#saml-sso-이용하기)

1. 채널톡 회원 가입 (계정 생성)

   * ID 공급자 계정과 동일한 이메일로 생성해주세요.

     ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc494badf4b00d4)
2. SAML SSO 로그인해주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc5365cd326f574)
3. 접속하시려는 채널을 선택해주세요.

   * 해당 채널이 SAML SSO 로그인 설정 되어있어야 목록에 보여집니다.

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc5575aa4216ec2)

4. 로그인 계정이 다를 경우

   * ID 공급자에 등록된 도메인을 확인 후 재로그인 해주세요.

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc575a0f1a00cb2)

[### Okta 설정 방법](#okta-설정-방법)

ID 공급자는 여러 서비스가 제공되고 있습니다. 예시는 Okta 서비스 등록 방법으로 작성되었어요. 다른 서비스를 이용 중이시라면 해당 서비스의 App 연동 방법을 참고하여 설정 부탁드립니다.

1. [Okta] - [Applications] - [Create App Intergration] 클릭

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc5a7d6bb39ee76)
2. App name에 [채널톡] 또는 [ChannelTalk] 입력 후 Next

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc5ccc1329837ca)
3. SAML 2.0 선택

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc6042d583ec40d)
4. 1~6번 정보만 입력 후 Next

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc6359879a0c45a)

   1) SAML SSO 설정 화면의 SSO URL 입력 (채널톡에서 확인)

   2) SAML SSO 설정 화면의 Entity ID 입력 (채널톡에서 확인)

   3) 입력하지 않음 (공란)

   4) EmailAddress 선택

   5) Email 선택

   6) Create and update 선택
5. [Sign On] - [More details] 클릭

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc65d43e9f4774f)
6. Sign on URL / Issuer / Signing Certificate 복사 후 채널톡 SAML SSO 설정 화면에 입력

   ![](https://cf.channel.io/document/spaces/6/articles/28/revisions/79/usermedia/662b0fc68c3cd3ff5184)