import hashlib

import pytest

from father_osint.acquisition import AcquisitionError
from father_osint.operator_import import OperatorImportArtifactFetcher


def test_operator_import_reads_exact_bytes_and_preserves_official_url(tmp_path):
    path = tmp_path / "DOC-RU-FZ-152-2006.html"
    payload = b"<html><body>official</body></html>"
    path.write_bytes(payload)
    url = "https://official.example/document"
    fetcher = OperatorImportArtifactFetcher({url: path})

    artifact = fetcher.fetch(url, timeout_seconds=1, max_bytes=10000)

    assert artifact.data == payload
    assert hashlib.sha256(artifact.data).hexdigest() == hashlib.sha256(payload).hexdigest()
    assert artifact.mime_type == "text/html"
    assert artifact.final_url == url


def test_operator_import_missing_mapping_fails_explicitly(tmp_path):
    fetcher = OperatorImportArtifactFetcher({})

    with pytest.raises(AcquisitionError, match="file is missing"):
        fetcher.fetch("https://official.example/missing", timeout_seconds=1, max_bytes=1000)


def test_operator_import_enforces_max_bytes(tmp_path):
    path = tmp_path / "large.html"
    path.write_bytes(b"x" * 101)
    url = "https://official.example/document"
    fetcher = OperatorImportArtifactFetcher({url: path})

    with pytest.raises(AcquisitionError, match="exceeds max_bytes"):
        fetcher.fetch(url, timeout_seconds=1, max_bytes=100)
