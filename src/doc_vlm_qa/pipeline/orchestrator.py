from __future__ import annotations

from doc_vlm_qa.models.response_formatter import format_response
from doc_vlm_qa.pipeline.router import choose_route
from doc_vlm_qa.utils.types import QAResponse, RouteMode


def run_pipeline(question: str, num_files: int, total_pages: int) -> QAResponse:
    route = choose_route(num_files=num_files, total_pages=total_pages)
    if route == RouteMode.DIRECT_VLM:
        answer = f"[DIRECT_VLM] {question}"
        citations: list[int] = [1] if total_pages > 0 else []
    else:
        answer = f"[RETRIEVAL_QA] {question}"
        citations = [1] if total_pages > 0 else []
    return format_response(answer=answer, citations=citations)
