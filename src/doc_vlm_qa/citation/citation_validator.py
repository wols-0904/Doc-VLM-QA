from __future__ import annotations


def validate_citations(citations: list[int], total_pages: int) -> bool:
    return all(1 <= page <= total_pages for page in citations)
