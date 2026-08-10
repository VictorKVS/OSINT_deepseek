from __future__ import annotations

import hashlib

import pytest

from father_osint.agent import safe_collector_error
from poc.tdlib.tdjson_bridge import redact, verify_library


def test_native_library_hash_must_match(tmp_path):
    library = tmp_path / "tdjson.dll"
    library.write_bytes(b"approved-test-binary")
    expected = hashlib.sha256(b"approved-test-binary").hexdigest()

    assert verify_library(library, expected) == str(library.resolve())

    with pytest.raises(RuntimeError, match="SHA-256 mismatch"):
        verify_library(library, "0" * 64)


def test_native_library_hash_rejects_malformed_digest(tmp_path):
    library = tmp_path / "tdjson.dll"
    library.write_bytes(b"x")
    with pytest.raises(RuntimeError, match="64-character"):
        verify_library(library, "not-a-sha")


def test_redactor_covers_current_tdlib_credentials():
    payload = {
        "api_hash": "secret-api-hash",
        "database_encryption_key": "db-key",
        "phone_number": "+10000000000",
        "email_address": "person@example.test",
        "code": {"@type": "emailAddressAuthenticationCode", "code": "1234"},
        "password": "2fa",
    }
    safe = redact(payload)
    assert safe["api_hash"] == "<redacted>"
    assert safe["database_encryption_key"] == "<redacted>"
    assert safe["phone_number"] == "<redacted>"
    assert safe["email_address"] == "<redacted>"
    assert safe["code"] == "<redacted>"
    assert safe["password"] == "<redacted>"


def test_collector_error_does_not_echo_exception_payload():
    secret = "TELEGRAM_API_HASH=must-not-leak"
    result = safe_collector_error("telegram", RuntimeError(secret))
    assert result == "telegram: RuntimeError"
    assert secret not in result
