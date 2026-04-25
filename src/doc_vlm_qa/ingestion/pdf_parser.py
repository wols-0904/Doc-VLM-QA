from __future__ import annotations

from pathlib import Path

from doc_vlm_qa.utils.types import DocumentPage


def extract_pdf_pages(pdf_path: str | Path) -> list[DocumentPage]:
    path = Path(pdf_path)
    return [DocumentPage(file_path=path, page_number=1, text="")]
