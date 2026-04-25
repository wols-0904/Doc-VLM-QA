from __future__ import annotations

from pathlib import Path


def vlm_answer(question: str, image_paths: list[str | Path]) -> str:
    return f"VLM answer: {question} (images={len(image_paths)})"
