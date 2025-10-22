"""
채널톡 문서 크롤러
https://docs.channel.io/help/ko 에서 문서를 구조화된 폴더로 크롤링하여 Markdown으로 저장
"""

import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


class ChannelDocsCrawler:
    """채널톡 문서 크롤러"""

    def __init__(
        self,
        base_url: str = "https://docs.channel.io/help/ko",
        output_dir: str = "data/domain/saas/channel/docs",
        delay: float = 1.0,
    ):
        """
        Args:
            base_url: 크롤링할 기본 URL
            output_dir: 저장할 디렉토리 경로
            delay: 요청 간 대기 시간 (초)
        """
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        self.visited_urls: Set[str] = set()

    def sanitize_filename(self, text: str) -> str:
        """파일명으로 사용할 수 있도록 텍스트를 정리"""
        # 특수문자 제거 및 공백을 언더스코어로 변경
        text = re.sub(r'[<>:"/\\|?*]', "", text)
        text = re.sub(r"\s+", "_", text.strip())
        # 너무 긴 파일명 제한
        if len(text) > 100:
            text = text[:100]
        return text

    def extract_short_category_name(self, full_title: str) -> str:
        """긴 카테고리명에서 짧은 이름 추출"""
        # 수동 매핑으로 간단한 카테고리명 추출
        mapping = {
            "채널톡_시작하기": "채널톡_시작하기",
            "채널_설정": "채널_설정",
            "개인_설정": "개인_설정",
            "팀_메신저": "팀_메신저",
            "고객_메신저": "고객_메신저",
            "고객_연락처": "고객_연락처",
            "워크플로우": "워크플로우",
            "오퍼레이션": "오퍼레이션",
            "마케팅": "마케팅",
            "외부서비스_연동": "외부서비스_연동",
            "AI": "AI",
            "앱스토어": "앱스토어",
            "미트": "미트",
            "구독_및_결제": "구독_및_결제",
            "도큐먼트": "도큐먼트",
        }
        
        # 매핑에서 찾기
        for key, value in mapping.items():
            if full_title.startswith(key):
                return value
        
        # 매핑에 없으면 "개의 아티클" 제거 후 첫 2단어
        text = re.sub(r"\d+개의_아티클.*$", "", full_title)
        parts = text.split("_")
        result = "_".join(parts[:2]) if len(parts) >= 2 else text
        
        return result.strip("_")

    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """URL에서 페이지 내용 가져오기"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")
            return None

    def extract_article_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """페이지에서 문서 링크 추출"""
        links = []
        seen_urls = set()
        
        # 모든 링크 찾기
        for link_tag in soup.find_all("a", href=True):
            href = link_tag["href"]
            
            # 상대 경로를 절대 경로로 변환
            full_url = urljoin(base_url, href)
            
            # docs.channel.io 도메인의 help/ko 링크만 필터링 (articles 또는 categories)
            if (
                "docs.channel.io" in full_url
                and "/help/ko/" in full_url
                and ("/articles/" in full_url or "/categories/" in full_url)
                and full_url not in seen_urls
            ):
                title = link_tag.get_text(strip=True)
                if title and len(title) > 0:
                    # URL에서 카테고리 타입 추출
                    category_type = "article" if "/articles/" in full_url else "category"
                    
                    links.append(
                        {
                            "url": full_url,
                            "title": title,
                            "category": category_type,
                            "type": category_type,
                        }
                    )
                    seen_urls.add(full_url)
        
        return links

    def convert_html_to_markdown(self, soup: BeautifulSoup) -> str:
        """HTML 콘텐츠를 Markdown으로 변환"""
        # 메인 콘텐츠 영역 찾기
        content_selectors = [
            ("article", {}),
            ("div", {"class": "article-content"}),
            ("div", {"class": "content"}),
            ("main", {}),
        ]
        
        content = None
        for tag, attrs in content_selectors:
            content = soup.find(tag, attrs)
            if content:
                break
        
        if not content:
            # 콘텐츠를 찾지 못한 경우 body 전체 사용
            content = soup.find("body")
        
        if not content:
            return ""
        
        # 불필요한 요소 제거
        for element in content.find_all(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Markdown으로 변환
        markdown_text = md(str(content), heading_style="ATX", bullets="*")
        
        # 여러 줄 공백 정리
        markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)
        
        return markdown_text.strip()

    def save_markdown(
        self, content: str, title: str, category: str, url: str, metadata: Optional[Dict] = None
    ):
        """Markdown 파일로 저장"""
        # 카테고리명 정리 (너무 긴 경우 짧게)
        short_category = self.extract_short_category_name(category)
        category_dir = self.output_dir / self.sanitize_filename(short_category)
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # 파일명 생성
        filename = self.sanitize_filename(title) + ".md"
        filepath = category_dir / filename
        
        # 메타데이터 추가
        frontmatter = f"""---
title: {title}
category: {category}
source_url: {url}
crawled_at: {time.strftime('%Y-%m-%d %H:%M:%S')}
---

"""
        
        # 파일 저장
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter)
            f.write(f"# {title}\n\n")
            f.write(content)
        
        print(f"✅ Saved: {filepath.relative_to(self.output_dir)}")

    def crawl_article(self, article_info: Dict[str, str]):
        """개별 문서 크롤링"""
        url = article_info["url"]
        
        # 이미 방문한 URL은 스킵
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        
        print(f"📄 Crawling: {article_info['title']} ({url})")
        
        # 페이지 가져오기
        soup = self.get_page_content(url)
        if not soup:
            return
        
        # 제목 추출 (h1 태그 우선)
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else article_info["title"]
        
        # HTML을 Markdown으로 변환
        markdown_content = self.convert_html_to_markdown(soup)
        
        if markdown_content:
            # 저장
            self.save_markdown(
                content=markdown_content,
                title=title,
                category=article_info["category"],
                url=url,
            )
        
        # 요청 간 대기
        time.sleep(self.delay)

    def crawl(self):
        """전체 문서 크롤링 시작"""
        print(f"🚀 Starting crawl from {self.base_url}")
        print(f"📁 Output directory: {self.output_dir}")
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 메인 페이지에서 링크 추출
        soup = self.get_page_content(self.base_url)
        if not soup:
            print("❌ Failed to fetch main page")
            return
        
        # 모든 문서 링크 추출
        all_links = self.extract_article_links(soup, self.base_url)
        print(f"📚 Found {len(all_links)} links (articles + categories)")
        
        # 카테고리와 문서 분리
        category_links = [link for link in all_links if link["type"] == "category"]
        article_links = [link for link in all_links if link["type"] == "article"]
        
        print(f"  └─ {len(category_links)} categories, {len(article_links)} articles")
        
        # 카테고리 페이지에서 추가 문서 링크 수집
        for i, category_info in enumerate(category_links, 1):
            print(f"\n📂 [{i}/{len(category_links)}] Exploring category: {category_info['title']}")
            category_soup = self.get_page_content(category_info["url"])
            if category_soup:
                category_articles = self.extract_article_links(
                    category_soup, category_info["url"]
                )
                # article 타입만 추가
                new_articles = [
                    link for link in category_articles if link["type"] == "article"
                ]
                # 카테고리명 업데이트
                for article in new_articles:
                    article["category"] = category_info["title"]
                
                article_links.extend(new_articles)
                print(f"  └─ Found {len(new_articles)} articles")
            
            time.sleep(self.delay)
        
        # 중복 제거
        seen = set()
        unique_articles = []
        for article in article_links:
            if article["url"] not in seen:
                unique_articles.append(article)
                seen.add(article["url"])
        
        article_links = unique_articles
        print(f"\n📄 Total unique articles to crawl: {len(article_links)}")
        
        # 각 문서 크롤링
        for i, article_info in enumerate(article_links, 1):
            print(f"\n[{i}/{len(article_links)}]")
            self.crawl_article(article_info)
        
        print(f"\n✨ Crawling completed! Total pages crawled: {len(self.visited_urls)}")
        print(f"📁 Files saved to: {self.output_dir.absolute()}")


def main():
    """메인 실행 함수"""
    crawler = ChannelDocsCrawler(
        base_url="https://docs.channel.io/help/ko",
        output_dir="data/domain/saas/channel/docs",
        delay=1.0,  # 1초 대기 (서버 부하 방지)
    )
    crawler.crawl()


if __name__ == "__main__":
    main()

