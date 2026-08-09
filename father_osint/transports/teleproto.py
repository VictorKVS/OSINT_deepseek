from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from ..collectors.telegram import TelegramMessage
from ..models import ResearchTask


class TeleprotoTransport:
    """Telegram MTProto transport backed by a Node/teleproto bridge."""

    def __init__(self, bridge_path: str | Path | None = None, timeout_seconds: int = 90) -> None:
        self.bridge_path = Path(bridge_path or "telegram_bridge/teleproto_search.mjs")
        self.timeout_seconds = timeout_seconds

    def search(self, task: ResearchTask) -> list[TelegramMessage]:
        if not self.bridge_path.exists():
            raise FileNotFoundError(f"teleproto bridge not found: {self.bridge_path}")

        payload = {
            "question": task.question,
            "topics": task.topics,
            "date_from": task.date_from,
            "date_to": task.date_to,
            "max_items": task.max_items,
        }

        proc = subprocess.run(
            ["node", str(self.bridge_path)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=self.timeout_seconds,
            env=os.environ.copy(),
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or "teleproto bridge failed")

        data = json.loads(proc.stdout or "[]")
        return [TelegramMessage(**item) for item in data]
