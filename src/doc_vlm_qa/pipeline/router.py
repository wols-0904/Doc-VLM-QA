from __future__ import annotations

from doc_vlm_qa.utils.types import RouteMode


def choose_route(num_files: int, total_pages: int, max_direct_files: int = 1, max_direct_pages: int = 1) -> RouteMode:
    if num_files <= max_direct_files and total_pages <= max_direct_pages:
        return RouteMode.DIRECT_VLM
    return RouteMode.RETRIEVAL_QA
