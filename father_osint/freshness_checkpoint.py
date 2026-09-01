from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class FreshnessCheckpoint:
    watchlist_id: str
    source_key: str
    last_complete_publish_date_to: str
    last_complete_observed_at: str

    @classmethod
    def from_mapping(cls, row: Mapping[str, object]) -> "FreshnessCheckpoint":
        checkpoint = cls(
            watchlist_id=str(row.get("watchlist_id") or "").strip(),
            source_key=str(row.get("source_key") or "").strip(),
            last_complete_publish_date_to=str(row.get("last_complete_publish_date_to") or "").strip(),
            last_complete_observed_at=str(row.get("last_complete_observed_at") or "").strip(),
        )
        if not checkpoint.watchlist_id or not checkpoint.source_key:
            raise ValueError("freshness checkpoint requires watchlist_id and source_key")
        date.fromisoformat(checkpoint.last_complete_publish_date_to)
        if not checkpoint.last_complete_observed_at:
            raise ValueError("freshness checkpoint requires last_complete_observed_at")
        return checkpoint

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FreshnessWindow:
    mode: str
    publish_date_from: str
    publish_date_to: str
    bootstrap_lookback_days: int
    checkpoint_overlap_days: int
    checkpoint_publish_date_to: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def load_freshness_checkpoint(
    path: Path,
    *,
    watchlist_id: str,
    source_key: str,
) -> FreshnessCheckpoint | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        checkpoint = FreshnessCheckpoint.from_mapping(payload)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return None
    if checkpoint.watchlist_id != watchlist_id or checkpoint.source_key != source_key:
        return None
    return checkpoint


def resolve_freshness_window(
    *,
    today: date,
    bootstrap_lookback_days: int,
    checkpoint_overlap_days: int,
    checkpoint: FreshnessCheckpoint | None,
) -> FreshnessWindow:
    if bootstrap_lookback_days < 1 or bootstrap_lookback_days > 3650:
        raise ValueError("bootstrap_lookback_days must be between 1 and 3650")
    if checkpoint_overlap_days < 0 or checkpoint_overlap_days > 30:
        raise ValueError("checkpoint_overlap_days must be between 0 and 30")

    if checkpoint is None:
        window_from = today - timedelta(days=bootstrap_lookback_days)
        return FreshnessWindow(
            mode="BOOTSTRAP_BACKFILL",
            publish_date_from=window_from.isoformat(),
            publish_date_to=today.isoformat(),
            bootstrap_lookback_days=bootstrap_lookback_days,
            checkpoint_overlap_days=checkpoint_overlap_days,
            checkpoint_publish_date_to=None,
        )

    checkpoint_to = date.fromisoformat(checkpoint.last_complete_publish_date_to)
    if checkpoint_to > today:
        raise ValueError("freshness checkpoint publish_date_to cannot be in the future")
    window_from = checkpoint_to - timedelta(days=checkpoint_overlap_days)
    return FreshnessWindow(
        mode="INCREMENTAL_FROM_CHECKPOINT",
        publish_date_from=window_from.isoformat(),
        publish_date_to=today.isoformat(),
        bootstrap_lookback_days=bootstrap_lookback_days,
        checkpoint_overlap_days=checkpoint_overlap_days,
        checkpoint_publish_date_to=checkpoint_to.isoformat(),
    )


def write_freshness_checkpoint(
    path: Path,
    *,
    watchlist_id: str,
    source_key: str,
    publish_date_to: str,
    observed_at: str | None = None,
) -> FreshnessCheckpoint:
    date.fromisoformat(publish_date_to)
    timestamp = observed_at or datetime.now(timezone.utc).isoformat()
    checkpoint = FreshnessCheckpoint(
        watchlist_id=watchlist_id,
        source_key=source_key,
        last_complete_publish_date_to=publish_date_to,
        last_complete_observed_at=timestamp,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(checkpoint.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)
    return checkpoint
