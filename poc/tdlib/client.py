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

    Unrelated updates are retained in a bounded buffer instead of silently
    discarded. If the buffer is saturated, the oldest update is dropped and the
    loss counter is incremented so the PoC can detect overload explicitly.
    """

    def __init__(self, bridge: TdJsonBridge, *, max_pending_updates: int = 1000) -> None:
        if max_pending_updates <= 0:
            raise ValueError("max_pending_updates must be > 0")
        self.bridge = bridge
        self.max_pending_updates = max_pending_updates
        self.pending_updates: deque[dict[str, Any]] = deque(maxlen=max_pending_updates)
        self.dropped_pending_updates = 0

    def _retain_update(self, response: dict[str, Any]) -> None:
        if len(self.pending_updates) >= self.max_pending_updates:
            self.dropped_pending_updates += 1
        self.pending_updates.append(response)

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
                self._retain_update(response)
                continue

            if response.get("@type") == "error":
                raise TdLibResponseError(response)
            return response

    def drain_pending_updates(self) -> list[dict[str, Any]]:
        result = list(self.pending_updates)
        self.pending_updates.clear()
        return result
