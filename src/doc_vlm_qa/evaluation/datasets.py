from __future__ import annotations

from pathlib import Path


def list_dataset_files(root: str | Path) -> list[Path]:
    return sorted(Path(root).glob("**/*"))
