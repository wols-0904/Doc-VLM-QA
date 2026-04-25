from __future__ import annotations

from doc_vlm_qa.utils.types import QAResponse


def format_response(answer: str, citations: list[int]) -> QAResponse:
    return QAResponse(answer=answer, citations=sorted(set(citations)))
