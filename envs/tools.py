"""
Tools for the Channel Talk environment.
Provides RAG-based search functionality over crawled documentation.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SearchData:
    """RAG tool for searching Channel Talk documentation."""

    def __init__(self, docs_dir: str = "data/domain/saas/channel/docs"):
        self.docs_dir = Path(docs_dir)
        self.documents = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self._load_documents()
        self._build_index()

    def _load_documents(self):
        """Load all markdown documents from the docs directory."""
        if not self.docs_dir.exists():
            raise ValueError(f"Documentation directory not found: {self.docs_dir}")

        for md_file in self.docs_dir.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse frontmatter
                frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
                if frontmatter_match:
                    frontmatter_text = frontmatter_match.group(1)
                    body = frontmatter_match.group(2)

                    # Extract title from frontmatter
                    title_match = re.search(r"^title:\s*(.+)$", frontmatter_text, re.MULTILINE)
                    title = title_match.group(1).strip() if title_match else md_file.stem

                    # Extract source URL
                    url_match = re.search(r"^source_url:\s*(.+)$", frontmatter_text, re.MULTILINE)
                    source_url = url_match.group(1).strip() if url_match else ""
                else:
                    title = md_file.stem
                    body = content
                    source_url = ""

                # Clean content
                clean_body = re.sub(r"!\[.*?\]\(.*?\)", "", body)  # Remove images
                clean_body = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", clean_body)  # Keep link text
                clean_body = re.sub(r"#{1,6}\s+", "", clean_body)  # Remove headers
                clean_body = " ".join(clean_body.split())  # Normalize whitespace

                self.documents.append(
                    {
                        "title": title,
                        "content": clean_body,
                        "file_path": str(md_file.relative_to(self.docs_dir)),
                        "source_url": source_url,
                    }
                )
            except Exception as e:
                print(f"Warning: Failed to load {md_file}: {e}")

        print(f"✅ Loaded {len(self.documents)} documents")

    def _build_index(self):
        """Build TF-IDF index for efficient search."""
        if not self.documents:
            raise ValueError("No documents loaded")

        corpus = [doc["title"] + " " + doc["content"] for doc in self.documents]
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words=None)
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        print(f"✅ Built search index with {self.tfidf_matrix.shape[1]} features")

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of relevant documents with scores
        """
        if not self.vectorizer or self.tfidf_matrix is None:
            raise ValueError("Search index not built")

        # Transform query
        query_vec = self.vectorizer.transform([query])

        # Calculate cosine similarity
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only return if there's some relevance
                doc = self.documents[idx].copy()
                doc["score"] = float(similarities[idx])
                # Truncate content for context window
                if len(doc["content"]) > 1000:
                    doc["content"] = doc["content"][:1000] + "..."
                results.append(doc)

        return results

    def format_search_results(self, results: List[Dict]) -> str:
        """Format search results as a string for LLM context."""
        if not results:
            return "검색 결과가 없습니다."

        formatted = "📚 검색된 문서:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. **{result['title']}** (관련도: {result['score']:.2f})\n"
            formatted += f"   {result['content']}\n"
            if result.get("source_url"):
                formatted += f"   출처: {result['source_url']}\n"
            formatted += "\n"

        return formatted


# Tool definition for LiteLLM
SEARCH_DATA_TOOL = {
    "type": "function",
    "function": {
        "name": "search_data",
        "description": "채널톡 문서에서 관련 정보를 검색합니다. 고객의 질문에 답변하기 위해 필요한 정보를 찾을 때 사용하세요.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색할 키워드 또는 질문",
                }
            },
            "required": ["query"],
        },
    },
}

