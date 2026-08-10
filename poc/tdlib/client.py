from __future__ import annotations

import time
from collections import deque
from typing import Any
from uuid import uuid4

from poc.tdlib.tdjson_bridge import TdJsonBridge


class TdLibTimeoutError(TimeoutError):
    pass


class TdLibResponseError(RuntimeError):
    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response
        code = response.get("code")
        message = response.get("message")
        super().__init__(f"TDLib error code={code!r} message={message!r}")


class TdJsonClient:
    """Small synchronous facade over TDLib's async JSON interface for PoC use.

    Unrelated updates are retained instead of silently discarded so live-update
    experiments can consume them later.
    """

    def __init__(self, bridge: TdJsonBridge) -> None:
        self.bridge = bridge
        self.pending_updates: deque[dict[str, Any]] = deque()

    def call(self, request: dict[str, Any], *, timeout_seconds: float = 10.0) -> dict[str, Any]:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")

        correlation_id = str(uuid4())
        payload = dict(request)
        payload["@extra"] = correlation_id
        self.bridge.send(payload)

        deadline = time.monotonic() + timeout_seconds
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TdLibTimeoutError(f"TDLib request timed out: {request.get('@type')}")

            response = self.bridge.receive(min(1.0, remaining))
            if response is None:
                continue

            if response.get("@extra") != correlation_id:
                self.pending_updates.append(response)
                continue

            if response.get("@type") == "error":
                raise TdLibResponseError(response)
            return response

    def drain_pending_updates(self) -> list[dict[str, Any]]:
        result = list(self.pending_updates)
        self.pending_updates.clear()
        return result
