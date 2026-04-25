from __future__ import annotations

from doc_vlm_qa.utils.types import RetrievalHit


def map_hits_to_pages(hits: list[RetrievalHit]) -> list[int]:
    return sorted({hit.page_number for hit in hits})
