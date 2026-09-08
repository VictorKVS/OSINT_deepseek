from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import utc_now_iso


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


@dataclass(slots=True)
class JournalEntry:
    sequence: int
    case_id: str
    event_type: str
    actor: str
    payload: dict[str, Any]
    previous_hash: str
    created_at_utc: str
    event_hash: str = ""

    def unsigned_payload(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "case_id": self.case_id,
            "event_type": self.event_type,
            "actor": self.actor,
            "payload": self.payload,
            "previous_hash": self.previous_hash,
            "created_at_utc": self.created_at_utc,
        }

    def to_dict(self) -> dict[str, Any]:
        data = self.unsigned_payload()
        data["event_hash"] = self.event_hash
        return data


@dataclass(slots=True)
class HashChainJournal:
    case_id: str
    entries: list[JournalEntry] = field(default_factory=list)

    def append(self, event_type: str, actor: str, payload: dict[str, Any]) -> JournalEntry:
        previous = self.entries[-1].event_hash if self.entries else "GENESIS"
        entry = JournalEntry(
            sequence=len(self.entries) + 1,
            case_id=self.case_id,
            event_type=event_type,
            actor=actor,
            payload=dict(payload),
            previous_hash=previous,
            created_at_utc=utc_now_iso(),
        )
        entry.event_hash = hashlib.sha256(canonical_json(entry.unsigned_payload()).encode("utf-8")).hexdigest()
        self.entries.append(entry)
        return entry

    def verify(self) -> tuple[bool, str]:
        previous = "GENESIS"
        for expected_sequence, entry in enumerate(self.entries, start=1):
            if entry.sequence != expected_sequence:
                return False, f"sequence mismatch at {expected_sequence}"
            if entry.previous_hash != previous:
                return False, f"previous_hash mismatch at {expected_sequence}"
            expected_hash = hashlib.sha256(
                canonical_json(entry.unsigned_payload()).encode("utf-8")
            ).hexdigest()
            if entry.event_hash != expected_hash:
                return False, f"event_hash mismatch at {expected_sequence}"
            previous = entry.event_hash
        return True, "PASS"

    def save_jsonl(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "".join(json.dumps(item.to_dict(), ensure_ascii=False) + "\n" for item in self.entries),
            encoding="utf-8",
        )
