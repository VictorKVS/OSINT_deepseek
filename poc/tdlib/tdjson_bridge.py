from __future__ import annotations

import ctypes
import json
import os
from ctypes.util import find_library
from pathlib import Path
from typing import Any


SENSITIVE_KEYS = {
    "api_hash",
    "phone_number",
    "code",
    "authentication_code",
    "password",
    "database_encryption_key",
    "encryption_key",
}


def redact(value: Any) -> Any:
    """Return a log-safe copy of nested TDLib data."""
    if isinstance(value, dict):
        return {
            key: ("<redacted>" if key.lower() in SENSITIVE_KEYS else redact(item))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


class TdJsonBridge:
    """Minimal ctypes wrapper for TDLib's current JSON C interface.

    PoC-only. It deliberately exposes generic JSON send/receive semantics and does
    not leak TDLib objects into father_osint domain contracts.
    """

    def __init__(self, library_path: str | None = None) -> None:
        resolved = library_path or os.getenv("TDJSON_LIBRARY") or find_library("tdjson")
        if not resolved:
            raise RuntimeError(
                "TDLib tdjson library not found. Set TDJSON_LIBRARY to the local built library path."
            )

        path = Path(resolved)
        # find_library may return a loader-resolvable soname rather than a filesystem path.
        load_target = str(path) if path.exists() else resolved
        self._lib = ctypes.CDLL(load_target)
        self._configure_signatures()
        self.client_id = int(self._lib.td_create_client_id())

    def _configure_signatures(self) -> None:
        self._lib.td_create_client_id.argtypes = []
        self._lib.td_create_client_id.restype = ctypes.c_int

        self._lib.td_send.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self._lib.td_send.restype = None

        self._lib.td_receive.argtypes = [ctypes.c_double]
        self._lib.td_receive.restype = ctypes.c_char_p

        self._lib.td_execute.argtypes = [ctypes.c_char_p]
        self._lib.td_execute.restype = ctypes.c_char_p

    @staticmethod
    def _encode(request: dict[str, Any]) -> bytes:
        return json.dumps(request, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

    @staticmethod
    def _decode(raw: bytes | None) -> dict[str, Any] | None:
        if raw is None:
            return None
        return json.loads(raw.decode("utf-8"))

    def send(self, request: dict[str, Any]) -> None:
        self._lib.td_send(self.client_id, self._encode(request))

    def receive(self, timeout_seconds: float = 1.0) -> dict[str, Any] | None:
        return self._decode(self._lib.td_receive(float(timeout_seconds)))

    def execute(self, request: dict[str, Any]) -> dict[str, Any] | None:
        return self._decode(self._lib.td_execute(self._encode(request)))
