from types import SimpleNamespace

import pytest

from father_osint.acquisition import AcquisitionError, FetchedArtifact
from father_osint.official_transport import CurlArtifactFetcher, RobustOfficialArtifactFetcher


class RecordingFetcher:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def fetch(self, url, *, timeout_seconds, max_bytes):
        self.calls.append((url, timeout_seconds, max_bytes))
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def test_robust_transport_uses_bounded_minimum_timeout_and_primary_success():
    artifact = FetchedArtifact(b"official", "text/plain", "https://official.example/doc")
    primary = RecordingFetcher(artifact)
    fallback = RecordingFetcher(AcquisitionError("must not run"))
    fetcher = RobustOfficialArtifactFetcher(
        primary=primary,
        fallback=fallback,
        minimum_timeout_seconds=45,
    )

    result = fetcher.fetch(
        "https://official.example/doc",
        timeout_seconds=15,
        max_bytes=1000,
    )

    assert result is artifact
    assert primary.calls == [("https://official.example/doc", 45.0, 1000)]
    assert fallback.calls == []


def test_robust_transport_falls_back_after_primary_transport_failure():
    primary = RecordingFetcher(AcquisitionError("python certificate store failed"))
    artifact = FetchedArtifact(b"official", "text/html", "https://official.example/doc")
    fallback = RecordingFetcher(artifact)
    fetcher = RobustOfficialArtifactFetcher(
        primary=primary,
        fallback=fallback,
        minimum_timeout_seconds=30,
    )

    result = fetcher.fetch(
        "https://official.example/doc",
        timeout_seconds=10,
        max_bytes=1000,
    )

    assert result is artifact
    assert primary.calls[0][1] == 30.0
    assert fallback.calls[0][1] == 30.0


def test_robust_transport_reports_both_failures_without_weakening_policy():
    fetcher = RobustOfficialArtifactFetcher(
        primary=RecordingFetcher(AcquisitionError("urllib timeout")),
        fallback=RecordingFetcher(AcquisitionError("curl TLS failure")),
        minimum_timeout_seconds=1,
    )

    with pytest.raises(AcquisitionError, match="primary=.*urllib timeout.*fallback=.*curl TLS failure"):
        fetcher.fetch(
            "https://official.example/doc",
            timeout_seconds=1,
            max_bytes=1000,
        )


def test_curl_transport_keeps_tls_verification_and_public_redirect_cookie_engine(monkeypatch):
    observed = {}

    def fake_run(command, *, capture_output, text, timeout, check):
        observed["command"] = list(command)
        output_path = command[command.index("--output") + 1]
        with open(output_path, "wb") as handle:
            handle.write(b"official exact bytes")
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "FATHER_FINAL_URL=https://official.example/final\n"
                "FATHER_CONTENT_TYPE=text/html; charset=utf-8\n"
            ),
            stderr="",
        )

    monkeypatch.setattr("father_osint.official_transport.subprocess.run", fake_run)
    fetcher = CurlArtifactFetcher(executable="curl")

    result = fetcher.fetch(
        "https://official.example/start",
        timeout_seconds=5,
        max_bytes=1000,
    )

    command = observed["command"]
    assert "--fail" in command
    assert "--location" in command
    assert "--cookie" in command
    assert "--cookie-jar" in command
    assert "--insecure" not in command
    assert "-k" not in command
    assert "--user-agent" not in command
    assert result.data == b"official exact bytes"
    assert result.final_url == "https://official.example/final"
    assert result.mime_type == "text/html; charset=utf-8"
