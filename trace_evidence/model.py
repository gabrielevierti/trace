from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any

@dataclass
class Artifact:
    id: str
    kind: str
    source: str
    name: str
    timestamp: str | None = None
    path: str | None = None
    sha256: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self): return asdict(self)

@dataclass
class Relationship:
    source_id: str
    target_id: str
    relation: str
    confidence: float
    basis: list[str]
    inferred: bool = True

    def to_dict(self): return asdict(self)
