from __future__ import annotations

from pathlib import Path


def render_page_images(pdf_path: str | Path, output_dir: str | Path) -> list[Path]:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return []
