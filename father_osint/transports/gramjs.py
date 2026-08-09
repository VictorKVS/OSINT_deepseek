from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from ..collectors.telegram import TelegramMessage
from ..models import ResearchTask


class GramJSTransport:
    """Telegram transport backed by a tiny Node/GramJS bridge.

    Secrets are read by the bridge from environment variables; they are never
    embedded in task payloads or source code.
    """

    def __init__(self, bridge_path: str | Path | None = None, timeout_seconds: int = 60) -> None:
        self.bridge_path = Path(bridge_path or "telegram_bridge/gramjs_search.mjs")
        self.timeout_seconds = timeout_seconds

    def search(self, task: ResearchTask) -> list[TelegramMessage]:
        if not self.bridge_path.exists():
            raise FileNotFoundError(f"GramJS bridge not found: {self.bridge_path}")

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
            stderr = proc.stderr.strip() or "unknown GramJS bridge error"
            raise RuntimeError(stderr)

        data = json.loads(proc.stdout or "[]")
        return [TelegramMessage(**item) for item in data]
