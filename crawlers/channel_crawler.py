"""
채널톡 문서 크롤러 V2 - 계층 구조 반영
https://docs.channel.io/help/ko 의 네비게이션 구조를 그대로 반영하여 크롤링
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md


class NavigationNode:
    """네비게이션 트리의 노드"""

    def __init__(self, title: str, url: Optional[str] = None, level: int = 0):
        self.title = title
        self.url = url
        self.level = level
        self.children: List[NavigationNode] = []
        self.parent: Optional[NavigationNode] = None

    def add_child(self, child: "NavigationNode"):
        child.parent = self
        self.children.append(child)

    def get_path(self) -> List[str]:
        """루트에서 현재 노드까지의 경로 반환"""
        path = []
        node = self
        while node.parent:
            path.insert(0, node.title)
            node = node.parent
        return path

    def __repr__(self):
        return f"<NavigationNode: {self.title} (level={self.level}, children={len(self.children)})>"


class ChannelDocsCrawlerV2:
    """채널톡 문서 크롤러 V2 - 계층 구조 반영"""

    def __init__(
        self,
        base_url: str = "https://docs.channel.io/help/ko",
        output_dir: str = "data/domain/saas/channel/docs",
        delay: float = 1.0,
    ):
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
        self.navigation_tree: Optional[NavigationNode] = None

    def clean_category_name(self, text: str) -> str:
        """카테고리명에서 설명 부분 제거하고 핵심만 추출"""
        # 수동 매핑
        mapping = {
            "채널톡 시작하기": "채널톡_시작하기",
            "채널톡 설치하기": "채널톡_설치하기",
            "채널톡 활용하기": "채널톡_활용하기",
            "채널톡 구독 이해하기": "채널톡_구독_이해하기",
            "채널 설정": "채널_설정",
            "개인 설정": "개인_설정",
            "팀 메신저": "팀_메신저",
            "고객 메신저": "고객_메신저",
            "고객 연락처": "고객_연락처",
            "워크플로우": "워크플로우",
            "오퍼레이션": "오퍼레이션",
            "마케팅": "마케팅",
            "외부서비스 연동": "외부서비스_연동",
            "AI": "AI",
            "앱스토어": "앱스토어",
            "미트": "미트",
            "구독 및 결제": "구독_및_결제",
            "도큐먼트": "도큐먼트",
            "SLA": "SLA",
            "채널엑스": "채널엑스",
        }
        
        # 매핑에서 찾기
        for key, value in mapping.items():
            if text.startswith(key):
                return value
        
        # 매핑에 없으면 긴 설명 제거
        # "XXX단골을 만드는..." -> "XXX"
        # "개의 아티클" 제거
        text = re.sub(r"\d+개의\s*아티클.*$", "", text)
        
        # 조사가 나오기 전까지만 추출 (을/를/의/는/이/가/에/로...)
        patterns = [
            r"^([가-힣\s]+?)(을|를|의|는|은|이|가|와|과|에|로|부터|까지|에서|으로|란,)",
            r"^([가-힣\s]+?)\s*([가-힣]+의|[가-힣]+은|[가-힣]+를)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                text = match.group(1).strip()
                break
        
        # 언더스코어로 변환
        text = re.sub(r"\s+", "_", text.strip())
        
        return text
    
    def sanitize_filename(self, text: str) -> str:
        """파일명/폴더명으로 사용할 수 있도록 텍스트를 정리"""
        # 먼저 카테고리명 정리 시도
        text = self.clean_category_name(text)
        
        # 특수문자 제거
        text = re.sub(r'[<>:"/\\|?*]', "", text)
        
        if len(text) > 100:
            text = text[:100]
        return text

    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """URL에서 페이지 내용 가져오기"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")
            return None

    def extract_navigation_structure(self, soup: BeautifulSoup) -> NavigationNode:
        """네비게이션 구조를 파싱하여 트리 구조로 변환"""
        root = NavigationNode("root", level=-1)
        nav = soup.find("nav", class_="Navigation_nav__AfW5N")

        if not nav:
            print("⚠️  Navigation not found")
            return root

        # 모든 OutlineItem 찾기
        items = nav.find_all("div", class_="OutlineItem_outline-item__zmH7D")
        
        stack = [root]  # 현재 레벨의 부모 노드 스택

        for item in items:
            # 인덴트 레벨 추출
            style = item.get("style", "")
            indent_match = re.search(r"--b-outline-item-indent:\s*(\d+)px", style)
            indent = int(indent_match.group(1)) if indent_match else 0
            level = indent // 24  # 24px per level (추정)

            # 텍스트 추출
            text_span = item.find("span", {"data-testid": "bezier-text"})
            if not text_span:
                continue

            title = text_span.get_text(strip=True)
            if not title:
                continue

            # URL 추출 (링크가 있는 경우)
            url = None
            link = item.find_parent("a", href=True)
            if link:
                url = urljoin(self.base_url, link["href"])

            # 노드 생성
            node = NavigationNode(title, url, level)

            # 스택에서 적절한 부모 찾기
            while len(stack) > 1 and stack[-1].level >= level:
                stack.pop()

            parent = stack[-1]
            parent.add_child(node)
            stack.append(node)

        return root

    def extract_navigation_structure_alt(self, soup: BeautifulSoup) -> NavigationNode:
        """대체 방법: 페이지의 모든 링크를 파싱하여 구조 생성"""
        root = NavigationNode("root", level=-1)
        
        # 모든 카테고리와 문서 링크 찾기
        all_links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "/help/ko/" not in href:
                continue
            
            full_url = urljoin(self.base_url, href)
            title = link.get_text(strip=True)
            
            if title and full_url:
                is_category = "/categories/" in full_url
                is_article = "/articles/" in full_url
                
                if is_category or is_article:
                    all_links.append({
                        "title": title,
                        "url": full_url,
                        "type": "category" if is_category else "article"
                    })

        # 중복 제거
        seen = set()
        unique_links = []
        for link in all_links:
            key = (link["title"], link["url"])
            if key not in seen:
                seen.add(key)
                unique_links.append(link)

        # 카테고리별로 그룹화
        current_category = None
        for link in unique_links:
            if link["type"] == "category":
                # 새 카테고리 노드
                node = NavigationNode(link["title"], link["url"], level=0)
                root.add_child(node)
                current_category = node
            elif link["type"] == "article" and current_category:
                # 현재 카테고리의 하위 문서
                node = NavigationNode(link["title"], link["url"], level=1)
                current_category.add_child(node)
            elif link["type"] == "article":
                # 카테고리 없는 최상위 문서
                node = NavigationNode(link["title"], link["url"], level=0)
                root.add_child(node)

        return root

    def print_navigation_tree(self, node: NavigationNode, indent: int = 0):
        """네비게이션 트리를 출력 (디버깅용)"""
        if node.title != "root":
            prefix = "  " * indent
            url_info = f" -> {node.url}" if node.url else ""
            print(f"{prefix}- {node.title}{url_info}")
        
        for child in node.children:
            self.print_navigation_tree(child, indent + 1)

    def convert_html_to_markdown(self, soup: BeautifulSoup) -> str:
        """HTML 콘텐츠를 Markdown으로 변환"""
        # 메인 콘텐츠 영역 찾기
        content_selectors = [
            ("article", {}),
            ("div", {"class": "article-content"}),
            ("main", {}),
        ]
        
        content = None
        for tag, attrs in content_selectors:
            content = soup.find(tag, attrs)
            if content:
                break
        
        if not content:
            content = soup.find("body")
        
        if not content:
            return ""
        
        # 불필요한 요소 제거
        for element in content.find_all(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Markdown으로 변환
        markdown_text = md(str(content), heading_style="ATX", bullets="*")
        markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)
        
        return markdown_text.strip()

    def save_markdown(self, content: str, title: str, path: List[str], url: str):
        """계층 구조를 반영하여 Markdown 파일로 저장"""
        # 경로 생성 (폴더명만 정리)
        dir_path = self.output_dir
        for folder in path[:-1]:  # 마지막은 파일명
            cleaned_folder = self.sanitize_filename(folder)
            dir_path = dir_path / cleaned_folder
        
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # 파일명 생성 (원본 제목 유지, 특수문자만 제거)
        filename = re.sub(r'[<>:"/\\|?*]', "", title)
        filename = re.sub(r"\s+", "_", filename.strip())
        if len(filename) > 100:
            filename = filename[:100]
        filename = filename + ".md"
        
        filepath = dir_path / filename
        
        # Frontmatter 생성
        frontmatter = f"""---
title: {title}
path: {' > '.join(path)}
source_url: {url}
crawled_at: {time.strftime('%Y-%m-%d %H:%M:%S')}
---

"""
        
        # 파일 저장
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter)
            f.write(f"# {title}\n\n")
            f.write(content)
        
        # 상대 경로 출력
        rel_path = filepath.relative_to(self.output_dir)
        print(f"✅ Saved: {rel_path}")

    def crawl_node(self, node: NavigationNode):
        """노드의 문서를 크롤링"""
        if not node.url:
            return
        
        if node.url in self.visited_urls:
            return
        
        self.visited_urls.add(node.url)
        
        # 경로 가져오기
        path = node.get_path()
        
        print(f"📄 Crawling: {' > '.join(path)}")
        
        # 페이지 가져오기
        soup = self.get_page_content(node.url)
        if not soup:
            return
        
        # 제목 추출 (h1 우선)
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else node.title
        
        # Markdown 변환
        markdown_content = self.convert_html_to_markdown(soup)
        
        if markdown_content:
            self.save_markdown(markdown_content, title, path, node.url)
        
        time.sleep(self.delay)

    def expand_category_node(self, node: NavigationNode):
        """카테고리 노드의 하위 문서 및 하위 카테고리를 찾아서 추가"""
        if not node.url or "/categories/" not in node.url:
            return
        
        # 카테고리 페이지 가져오기
        soup = self.get_page_content(node.url)
        if not soup:
            return
        
        # 하위 카테고리와 문서 링크 찾기
        article_links = []
        subcategory_links = []
        
        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(self.base_url, href)
            title = link.get_text(strip=True)
            
            if not title or full_url in self.visited_urls:
                continue
            
            # 하위 카테고리 (categories 링크)
            if "/categories/" in href and full_url != node.url:
                subcategory_links.append((title, full_url))
            # 문서 (articles 링크)
            elif "/articles/" in href:
                article_links.append((title, full_url))
        
        # 중복 제거 함수
        def deduplicate(links):
            seen = set()
            unique = []
            for title, url in links:
                if url not in seen:
                    seen.add(url)
                    unique.append((title, url))
            return unique
        
        unique_subcategories = deduplicate(subcategory_links)
        unique_articles = deduplicate(article_links)
        
        # 하위 카테고리를 자식 노드로 추가
        for title, url in unique_subcategories:
            child = NavigationNode(title, url, node.level + 1)
            node.add_child(child)
        
        # 문서를 자식 노드로 추가
        for title, url in unique_articles:
            child = NavigationNode(title, url, node.level + 1)
            node.add_child(child)
        
        # 발견 내역 출력
        if unique_subcategories or unique_articles:
            if unique_subcategories:
                print(f"  └─ Found {len(unique_subcategories)} subcategories in: {node.title}")
            if unique_articles:
                print(f"  └─ Found {len(unique_articles)} articles in: {node.title}")
        
        time.sleep(self.delay)

    def crawl_tree(self, node: NavigationNode):
        """트리를 재귀적으로 크롤링"""
        # 카테고리 노드라면 하위 문서들 확장
        if node.url and "/categories/" in node.url:
            self.expand_category_node(node)
        
        # 현재 노드 크롤링 (카테고리 페이지는 스킵)
        if node.url and "/articles/" in node.url:
            self.crawl_node(node)
        
        # 자식 노드들 크롤링
        for child in node.children:
            self.crawl_tree(child)

    def crawl(self):
        """전체 문서 크롤링 시작"""
        print(f"🚀 Starting hierarchical crawl from {self.base_url}")
        print(f"📁 Output directory: {self.output_dir}")
        
        # 출력 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 메인 페이지 가져오기
        soup = self.get_page_content(self.base_url)
        if not soup:
            print("❌ Failed to fetch main page")
            return
        
        # 네비게이션 구조 추출
        print("\n📊 Extracting navigation structure...")
        self.navigation_tree = self.extract_navigation_structure_alt(soup)
        
        # 구조 출력
        print("\n📋 Navigation structure:")
        self.print_navigation_tree(self.navigation_tree)
        
        # 카운트
        def count_nodes(node):
            count = 1 if node.url else 0
            for child in node.children:
                count += count_nodes(child)
            return count
        
        total_pages = count_nodes(self.navigation_tree)
        print(f"\n📚 Found {total_pages} pages to crawl\n")
        
        # 크롤링 시작
        self.crawl_tree(self.navigation_tree)
        
        print(f"\n✨ Crawling completed! Total pages crawled: {len(self.visited_urls)}")
        print(f"📁 Files saved to: {self.output_dir.absolute()}")
        
        # 구조를 JSON으로 저장
        self.save_structure_json()

    def save_structure_json(self):
        """네비게이션 구조를 JSON으로 저장"""
        
        def node_to_dict(node: NavigationNode) -> Dict:
            return {
                "title": node.title,
                "url": node.url,
                "level": node.level,
                "children": [node_to_dict(child) for child in node.children]
            }
        
        structure = node_to_dict(self.navigation_tree)
        
        json_path = self.output_dir.parent / "structure.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(structure, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Structure saved to: {json_path}")


def main():
    """메인 실행 함수"""
    crawler = ChannelDocsCrawlerV2(
        base_url="https://docs.channel.io/help/ko",
        output_dir="data/domain/saas/channel/docs",
        delay=1.0,
    )
    crawler.crawl()


if __name__ == "__main__":
    main()

