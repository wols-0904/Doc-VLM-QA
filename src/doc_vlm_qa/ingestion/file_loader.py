from __future__ import annotations

from pathlib import Path


def normalize_uploaded_paths(paths: list[str]) -> list[Path]:
    return [Path(p).resolve() for p in paths]
