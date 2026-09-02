from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from .models import utc_now_iso


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class HashChainJournal:
    """Append-only JSONL journal with per-entry SHA-256 chaining."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def entries(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    def append(
        self,
        event_type: str,
        *,
        case_id: str,
        request_id: str,
        actor: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        prior = self.entries()
        previous_hash = prior[-1]["entry_hash"] if prior else "GENESIS"
        base = {
            "sequence": len(prior) + 1,
            "timestamp_utc": utc_now_iso(),
            "event_type": event_type,
            "case_id": case_id,
            "request_id": request_id,
            "actor": actor,
            "previous_hash": previous_hash,
            "payload": payload,
        }
        digest = hashlib.sha256(canonical_json(base).encode("utf-8")).hexdigest()
        entry = dict(base, entry_hash=digest)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(entry) + "\n")
        return entry

    def verify(self) -> tuple[bool, list[str]]:
        errors: list[str] = []
        previous_hash = "GENESIS"
        for expected_sequence, entry in enumerate(self.entries(), start=1):
            if entry.get("sequence") != expected_sequence:
                errors.append(
                    f"sequence mismatch at entry {expected_sequence}: {entry.get('sequence')}"
                )
            if entry.get("previous_hash") != previous_hash:
                errors.append(f"previous_hash mismatch at entry {expected_sequence}")
            stored_hash = entry.get("entry_hash")
            base = {key: value for key, value in entry.items() if key != "entry_hash"}
            actual_hash = hashlib.sha256(canonical_json(base).encode("utf-8")).hexdigest()
            if stored_hash != actual_hash:
                errors.append(f"entry_hash mismatch at entry {expected_sequence}")
            previous_hash = stored_hash or "INVALID"
        return (not errors, errors)
