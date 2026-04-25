from __future__ import annotations

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = SentenceTransformer("BAAI/bge-small-zh-v1.5")


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """按固定窗口与重叠长度切分文本。"""
    if not text:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if overlap < 0:
        raise ValueError("overlap 不能小于 0")
    if overlap >= chunk_size:
        raise ValueError("overlap 必须小于 chunk_size")

    chunks: list[str] = []
    start = 0
    step = chunk_size - overlap

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += step

    return chunks


class DocumentRetriever:
    def __init__(self) -> None:
        self.index: faiss.IndexFlatL2 | None = None
        self.chunks: list[str] = []
        self.chunk_page_ids: list[int] = []

    def build_index(self, parsed_data: list[dict]) -> None:
        """从解析结果构建临时 FAISS 向量索引。"""
        self.chunks = []
        self.chunk_page_ids = []

        for item in parsed_data:
            page_id = int(item.get("page_id", 0))
            page_text = str(item.get("text", ""))
            page_chunks = chunk_text(page_text)
            for chunk in page_chunks:
                self.chunks.append(chunk)
                self.chunk_page_ids.append(page_id)

        if not self.chunks:
            self.index = None
            return

        embeddings = EMBEDDING_MODEL.encode(self.chunks, convert_to_numpy=True)
        embeddings = np.asarray(embeddings, dtype=np.float32)

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """在临时索引中检索最相关文本块。"""
        if not query.strip() or self.index is None or not self.chunks:
            return []

        if top_k <= 0:
            return []

        query_vec = EMBEDDING_MODEL.encode([query], convert_to_numpy=True)
        query_vec = np.asarray(query_vec, dtype=np.float32)

        k = min(top_k, len(self.chunks))
        distances, indices = self.index.search(query_vec, k)

        results: list[dict] = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx < 0:
                continue
            results.append(
                {
                    "chunk_text": self.chunks[idx],
                    "page_id": self.chunk_page_ids[idx],
                    "score": float(distance),
                }
            )

        return results
