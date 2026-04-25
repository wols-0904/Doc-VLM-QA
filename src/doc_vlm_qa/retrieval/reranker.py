from __future__ import annotations

from doc_vlm_qa.utils.types import RetrievalHit


def rerank_hits(hits: list[RetrievalHit], top_k: int = 3) -> list[RetrievalHit]:
    return sorted(hits, key=lambda x: x.score, reverse=True)[:top_k]
