from __future__ import annotations


def exact_match(pred: str, gold: str) -> float:
    return float(pred.strip() == gold.strip())
