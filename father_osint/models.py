from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class ResearchTask:
    question: str
    topics: list[str] = field(default_factory=list)
    source_types: list[str] = field(default_factory=lambda: ["telegram", "github", "web"])
    date_from: str | None = None
    date_to: str | None = None
    max_items: int = 50
    depth: str = "NORMAL"
    stop_when_enough: str | None = None
    requested_by: str = "analyst"
    task_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def __post_init__(self) -> None:
        allowed = {"FAST", "NORMAL", "DEEP", "CRITICAL"}
        self.depth = self.depth.upper()
        if self.depth not in allowed:
            raise ValueError(f"depth must be one of {sorted(allowed)}")
        if not self.question.strip():
            raise ValueError("question must not be empty")
        if self.max_items <= 0:
            raise ValueError("max_items must be > 0")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Material:
    source_type: str
    source_locator: str
    title: str
    raw_text: str | None = None
    local_path: str | None = None
    published_at: str | None = None
    author: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    material_id: str = field(default_factory=lambda: str(uuid4()))
    collected_at: str = field(default_factory=utc_now_iso)
    content_hash: str | None = None

    def __post_init__(self) -> None:
        if not self.source_type.strip():
            raise ValueError("source_type must not be empty")
        if not self.source_locator.strip():
            raise ValueError("source_locator must not be empty")
        if not self.title.strip():
            self.title = self.source_locator
        if self.raw_text is None and self.local_path is None:
            raise ValueError("material must contain raw_text or local_path")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MaterialPackage:
    task_id: str
    materials: list[Material] = field(default_factory=list)
    payloads_reused: int = 0
    collection_errors: list[str] = field(default_factory=list)
    notes: str = ""
    stop_reason: str = "completed"
    package_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["materials"] = [m.to_dict() for m in self.materials]
        return data
