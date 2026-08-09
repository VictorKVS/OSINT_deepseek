from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from ..models import Material, ResearchTask


class FixtureCollector:
    """DEV-only collector that reads prepared JSON fixtures.

    This keeps the OSINT pipeline testable before real Telegram/Web/Tor transports
    are enabled. Each JSON item maps directly to a Material-like record.
    """

    def __init__(self, name: str, source_type: str, fixture_path: str | Path) -> None:
        self.name = name
        self.source_types = {source_type}
        self.source_type = source_type
        self.fixture_path = Path(fixture_path)

    def collect(self, task: ResearchTask) -> Iterable[Material]:
        if not self.fixture_path.exists():
            raise FileNotFoundError(f"Fixture not found: {self.fixture_path}")

        data = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        for item in data:
            text = item.get("raw_text") or ""
            haystack = " ".join(
                [
                    item.get("title", ""),
                    text,
                    " ".join(str(x) for x in item.get("tags", [])),
                ]
            ).lower()

            terms = [task.question, *task.topics]
            if terms and not any(term.lower() in haystack for term in terms if term.strip()):
                continue

            yield Material(
                source_type=self.source_type,
                source_locator=item["source_locator"],
                title=item.get("title") or item["source_locator"],
                raw_text=text or None,
                local_path=item.get("local_path"),
                published_at=item.get("published_at"),
                author=item.get("author"),
                metadata={
                    "dev_fixture": True,
                    "tags": item.get("tags", []),
                    **item.get("metadata", {}),
                },
            )
