from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class SourceHealthState:
    source_key: str
    status: str
    observed_at_epoch: float
    observed_at: str
    cooldown_seconds: float
    error: str | None = None

    @property
    def retry_after_epoch(self) -> float:
        return self.observed_at_epoch + self.cooldown_seconds

    def circuit_open(self, now_epoch: float | None = None) -> bool:
        now = time.time() if now_epoch is None else float(now_epoch)
        return self.status == "FAILED" and now < self.retry_after_epoch

    def remaining_seconds(self, now_epoch: float | None = None) -> float:
        now = time.time() if now_epoch is None else float(now_epoch)
        return max(0.0, self.retry_after_epoch - now) if self.circuit_open(now) else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_key": self.source_key,
            "status": self.status,
            "observed_at_epoch": self.observed_at_epoch,
            "observed_at": self.observed_at,
            "cooldown_seconds": self.cooldown_seconds,
            "retry_after_epoch": self.retry_after_epoch,
            "error": self.error,
        }


def _utc_iso(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat()


def load_source_health(path: Path, *, source_key: str) -> SourceHealthState | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if payload.get("source_key") != source_key:
        return None
    try:
        return SourceHealthState(
            source_key=source_key,
            status=str(payload["status"]),
            observed_at_epoch=float(payload["observed_at_epoch"]),
            observed_at=str(payload["observed_at"]),
            cooldown_seconds=float(payload.get("cooldown_seconds", 0.0)),
            error=str(payload["error"]) if payload.get("error") is not None else None,
        )
    except (KeyError, TypeError, ValueError):
        return None


def write_source_health(
    path: Path,
    *,
    source_key: str,
    status: str,
    cooldown_seconds: float,
    error: str | None = None,
    now_epoch: float | None = None,
) -> SourceHealthState:
    if status not in {"OK", "FAILED"}:
        raise ValueError("status must be OK or FAILED")
    if cooldown_seconds < 0:
        raise ValueError("cooldown_seconds must be >= 0")
    epoch = time.time() if now_epoch is None else float(now_epoch)
    state = SourceHealthState(
        source_key=source_key,
        status=status,
        observed_at_epoch=epoch,
        observed_at=_utc_iso(epoch),
        cooldown_seconds=float(cooldown_seconds),
        error=error,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)
    return state
