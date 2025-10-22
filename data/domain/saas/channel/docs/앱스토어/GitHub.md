---
title: GitHub
path: 앱스토어다양한 커맨드를 가진 앱이 모여있는 스토어입니다. 자유롭게 앱을 제작하고 등록할 수 있고, 다른 사람들이 등록한 앱을 연동해보실 수 있도록 제공될 예정이에요.5개의 아티클 > GitHubGitHub 앱을 설치해 이벤트를 채널톡과 연동해 보세요. 팀챗과 GitHub를 연결해 팀의 협업을 한층 더 강화할 수 있습니다.
source_url: https://docs.channel.io/help/ko/articles/GitHub-5c755cd0
crawled_at: 2025-10-21 23:24:23
---

# GitHub

[### 주요 기능](#주요-기능)

1. **PR(Pull Request) 및 Issue 이벤트 전송**

GitHub에서 발생하는 PR, Issue 이벤트를 실시간으로 채널톡 팀챗에 전송할 수 있습니다. 구성원들이 코드 리뷰 및 문제 해결에 대한 즉각적인 알림을 받아 효율적으로 협업할 수 있어요.

![](https://cf.channel.io/document/spaces/6/articles/306/revisions/997/usermedia/666698a1ac97a59045d0)

1. **Release 이벤트 전송**

GitHub에서 발생하는 Release 이벤트를 실시간으로 채널톡 팀챗에 전송할 수 있습니다. 구성원들은 새로운 버전의 소프트웨어 출시 및 업데이트에 대한 알림을 받아 프로젝트의 상태를 파악하고 조치할 수 있어요.

![](https://cf.channel.io/document/spaces/6/articles/306/revisions/997/usermedia/666698b48063ce2ba691)

[### 사용 방법](#사용-방법)

1. **앱스토어 앱 설치하기**

[채널 설정] - [연동] - [앱스토어]에서 GitHub 앱을 설치해 주세요.

![](https://cf.channel.io/document/spaces/6/articles/306/revisions/997/usermedia/666698cbdfecf5ab4f9f)

2. **GitHub 앱 설치하기**

아래 링크를 통해 GitHub 앱을 설치해 주세요.

<https://github.com/apps/channeltalk>

3. **GitHub 커스텀 프로퍼티 설정하기**

GitHub 이벤트를 채널과 팀챗에 연결하기 위해서 아래 3가지 custom property 설정이 필요합니다.

* cht\_channel\_id
* cht\_group\_id
* cht\_release\_group\_id

레포지토리(Repository)마다 cht\_group\_id를 설정해, 채널톡으로 PR, Issue 알림을 받을 팀챗 그룹을 다르게 설정할 수 있습니다. Release에 대한 알림은 cht\_release\_group\_id을 팀별로 설정해 팀챗 알림으로 받아보실 수 있어요

![](https://cf.channel.io/document/spaces/6/articles/306/revisions/997/usermedia/666699203a929e6f542b)

ID 지정 시 필요한 채널 아이디, 팀챗 그룹 아이디 값은 브라우저를 통해 실행한 채널톡의 URL에서 확인하실 수 있습니다.

![](https://cf.channel.io/document/spaces/6/articles/306/revisions/997/usermedia/66669934c1c3ed85f2b0)

4. **채널 매니저 프로필 설정하기**

GitHub에서 이용하는 유저이름을 기반으로 채널톡에서 이용하는 매니저 이름을 태그하기 위해, 매니저 프로필에 GitHub 유저 이름을 등록해야 합니다. github-username을 키값으로 하여 GitHub 유저이름을 입력해 주세요.

* 데이터 키 : github-username
* 값 : GitHub에서 이용하는 유저 이름

![](https://cf.channel.io/document/spaces/6/articles/306/revisions/997/usermedia/666699a047dcc8924f9c)