from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class InMemoryIndex:
    ids: list[int] = field(default_factory=list)
    vectors: list[list[float]] = field(default_factory=list)
    payloads: list[str] = field(default_factory=list)

    def add(self, idx: int, vector: list[float], payload: str) -> None:
        self.ids.append(idx)
        self.vectors.append(vector)
        self.payloads.append(payload)

    def clear(self) -> None:
        self.ids.clear()
        self.vectors.clear()
        self.payloads.clear()
