from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO_ROOT / "reports" / "osint_control_center" / "downloads"


class DownloadProgressRegistry:
    """Per-role live acquisition state for the OSINT Control Center.

    Each acquisition process writes its own JSON file, so parallel roles do not
    contend on one registry. Writes are atomic (temporary file + replace).
    """

    def __init__(self, role_id: str, *, root: Path | None = None) -> None:
        self.role_id = role_id.upper().strip()
        self.root = root or DEFAULT_ROOT
        self.path = self.root / f"{self.role_id}.json"
        self._lock = threading.Lock()
        self._last_flush = 0.0
        self.payload: dict[str, Any] = {
            "schema_version": "1.0",
            "record_type": "ACQUISITION_DOWNLOAD_PROGRESS",
            "stage": "STAGE_1_ACQUISITION",
            "role_id": self.role_id,
            "state": "PLANNED",
            "started_at_epoch": None,
            "updated_at_epoch": time.time(),
            "finished_at_epoch": None,
            "items_total": 0,
            "queued_total": 0,
            "downloading_total": 0,
            "hashing_total": 0,
            "downloaded_total": 0,
            "reused_total": 0,
            "failed_total": 0,
            "bytes_received_total": 0,
            "bytes_expected_total": 0,
            "overall_progress_pct": 0.0,
            "items": {},
        }

    def start(self, items: list[dict[str, Any]] | None = None) -> None:
        now = time.time()
        with self._lock:
            self.payload["state"] = "RUNNING"
            self.payload["started_at_epoch"] = now
            self.payload["updated_at_epoch"] = now
            self.payload["finished_at_epoch"] = None
            self.payload["items"] = {}
            for row in items or []:
                self._ensure_item_locked(str(row["item_id"]), row, now)
            self._recount()
            self._flush_locked(force=True)

    def ensure_item(self, item_id: str, **fields: Any) -> None:
        now = time.time()
        with self._lock:
            self._ensure_item_locked(str(item_id), fields, now)
            self.payload["state"] = "RUNNING"
            if self.payload.get("started_at_epoch") is None:
                self.payload["started_at_epoch"] = now
            self.payload["updated_at_epoch"] = now
            self._recount()
            self._flush_locked(force=True)

    def _ensure_item_locked(self, item_id: str, fields: dict[str, Any], now: float) -> None:
        if item_id in self.payload["items"]:
            row = self.payload["items"][item_id]
            for key, value in fields.items():
                if value is not None:
                    row[key] = value
            return
        row = {"item_id": item_id, **dict(fields)}
        row.setdefault("status", "QUEUED")
        row.setdefault("bytes_received", 0)
        row.setdefault("total_bytes", row.get("file_size") or 0)
        row.setdefault("progress_pct", 0.0)
        row.setdefault("speed_bytes_per_second", 0.0)
        row.setdefault("started_at_epoch", None)
        row.setdefault("updated_at_epoch", now)
        row.setdefault("finished_at_epoch", None)
        row.setdefault("sha256", None)
        row.setdefault("local_path", None)
        row.setdefault("error", None)
        self.payload["items"][item_id] = row

    def update(self, item_id: str, *, status: str | None = None, bytes_received: int | None = None,
               total_bytes: int | None = None, sha256: str | None = None, local_path: str | None = None,
               error: str | None = None, force: bool = False) -> None:
        now = time.time()
        with self._lock:
            row = self.payload["items"].get(str(item_id))
            if row is None:
                return
            if status is not None and status != row.get("status"):
                row["status"] = status
                if status == "DOWNLOADING" and not row.get("started_at_epoch"):
                    row["started_at_epoch"] = now
                if status in {"DOWNLOADED", "REUSED", "FAILED"}:
                    row["finished_at_epoch"] = now
            if bytes_received is not None:
                row["bytes_received"] = max(0, int(bytes_received))
            if total_bytes is not None:
                row["total_bytes"] = max(0, int(total_bytes))
            total = int(row.get("total_bytes") or 0)
            received = int(row.get("bytes_received") or 0)
            row["progress_pct"] = round(min(100.0, (received / total * 100.0) if total else (100.0 if row.get("status") in {"DOWNLOADED", "REUSED"} else 0.0)), 2)
            started = row.get("started_at_epoch")
            if started and now > started and received:
                row["speed_bytes_per_second"] = round(received / (now - float(started)), 2)
            if sha256 is not None:
                row["sha256"] = sha256
            if local_path is not None:
                row["local_path"] = local_path
            if error is not None:
                row["error"] = error
            row["updated_at_epoch"] = now
            self.payload["updated_at_epoch"] = now
            self._recount()
            self._flush_locked(force=force or (now - self._last_flush >= 0.25))

    def finish(self) -> None:
        with self._lock:
            self.payload["state"] = "PASS" if int(self.payload.get("failed_total") or 0) == 0 else "PASS_WITH_ERRORS"
            self.payload["finished_at_epoch"] = time.time()
            self.payload["updated_at_epoch"] = self.payload["finished_at_epoch"]
            self._recount()
            self._flush_locked(force=True)

    def _recount(self) -> None:
        items = list(self.payload.get("items", {}).values())
        self.payload["items_total"] = len(items)
        for status, key in (
            ("QUEUED", "queued_total"),
            ("DOWNLOADING", "downloading_total"),
            ("HASHING", "hashing_total"),
            ("DOWNLOADED", "downloaded_total"),
            ("REUSED", "reused_total"),
            ("FAILED", "failed_total"),
        ):
            self.payload[key] = sum(1 for row in items if row.get("status") == status)
        received = sum(int(row.get("bytes_received") or 0) for row in items)
        expected = sum(int(row.get("total_bytes") or 0) for row in items)
        self.payload["bytes_received_total"] = received
        self.payload["bytes_expected_total"] = expected
        if expected:
            pct = min(100.0, received / expected * 100.0)
        elif items:
            terminal = sum(1 for row in items if row.get("status") in {"DOWNLOADED", "REUSED", "FAILED"})
            pct = terminal / len(items) * 100.0
        else:
            pct = 0.0
        self.payload["overall_progress_pct"] = round(pct, 2)

    def flush(self, *, force: bool = False) -> None:
        with self._lock:
            self._flush_locked(force=force)

    def _flush_locked(self, *, force: bool) -> None:
        now = time.time()
        if not force and now - self._last_flush < 0.25:
            return
        self.root.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(f".json.{os.getpid()}.tmp")
        tmp.write_text(json.dumps(self.payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, self.path)
        self._last_flush = now
