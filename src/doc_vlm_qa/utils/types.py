from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class RouteMode(str, Enum):
    DIRECT_VLM = "direct_vlm"
    RETRIEVAL_QA = "retrieval_qa"


@dataclass(slots=True)
class DocumentPage:
    file_path: Path
    page_number: int
    text: str = ""
    image_path: Path | None = None


@dataclass(slots=True)
class RetrievalHit:
    page_number: int
    score: float
    content: str


@dataclass(slots=True)
class QAResponse:
    answer: str
    citations: list[int] = field(default_factory=list)
