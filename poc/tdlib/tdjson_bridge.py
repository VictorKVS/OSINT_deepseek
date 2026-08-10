from __future__ import annotations

import ctypes
import hashlib
import hmac
import json
import os
from pathlib import Path
from typing import Any


SENSITIVE_KEYS = {
    "api_hash",
    "phone_number",
    "email_address",
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


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_library(path: str | Path, expected_sha256: str) -> str:
    """Verify the exact native tdjson binary before loading it."""
    file_path = Path(path).expanduser().resolve()
    if not file_path.is_file():
        raise RuntimeError(f"TDLib tdjson library not found: {file_path}")
    expected = expected_sha256.strip().lower()
    if len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected):
        raise RuntimeError("TDJSON_SHA256 must be a 64-character hexadecimal SHA-256 digest")
    actual = sha256_file(file_path)
    if not hmac.compare_digest(actual, expected):
        raise RuntimeError(
            f"TDLib tdjson SHA-256 mismatch for {file_path.name}: expected {expected}, got {actual}"
        )
    return str(file_path)


class TdJsonBridge:
    """Minimal ctypes wrapper for TDLib's JSON C interface.

    PoC-only. Live use requires an explicit local library path and a verified
    SHA-256 digest. This prevents silently loading an arbitrary tdjson from PATH.
    """

    def __init__(
        self,
        library_path: str | None = None,
        expected_sha256: str | None = None,
    ) -> None:
        resolved = library_path or os.getenv("TDJSON_LIBRARY")
        expected = expected_sha256 or os.getenv("TDJSON_SHA256")
        if not resolved:
            raise RuntimeError("Set TDJSON_LIBRARY to the exact local tdjson library path")
        if not expected:
            raise RuntimeError("Set TDJSON_SHA256 to the approved tdjson binary SHA-256")

        load_target = verify_library(resolved, expected)
        self.library_path = load_target
        self.library_sha256 = expected.strip().lower()
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
