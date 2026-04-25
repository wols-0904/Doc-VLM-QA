from __future__ import annotations

from doc_vlm_qa.utils.types import RetrievalHit


def retrieve_top_k(_question: str, documents: list[str], k: int = 5) -> list[RetrievalHit]:
    return [RetrievalHit(page_number=i + 1, score=1.0, content=content) for i, content in enumerate(documents[:k])]
