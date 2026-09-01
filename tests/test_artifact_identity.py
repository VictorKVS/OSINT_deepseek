import pytest

from father_osint.acquisition import AcquisitionError, FetchedArtifact
from father_osint.artifact_identity import MarkerValidatingFetcher


class StaticFetcher:
    def __init__(self, data: bytes, mime_type: str = "text/html"):
        self.data = data
        self.mime_type = mime_type

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        return FetchedArtifact(data=self.data, mime_type=self.mime_type, final_url=url)


def test_identity_markers_allow_expected_official_document():
    html = """
    <html><body>
    <h1>Федеральный закон № 152-ФЗ</h1>
    <p>О персональных данных</p>
    </body></html>
    """.encode("utf-8")
    fetcher = MarkerValidatingFetcher(
        {"https://official.example/152": ("152-ФЗ", "О персональных данных")},
        inner=StaticFetcher(html),
    )

    artifact = fetcher.fetch(
        "https://official.example/152",
        timeout_seconds=1,
        max_bytes=10000,
    )

    assert artifact.data == html


def test_identity_markers_reject_wrong_document_from_correct_domain():
    html = "<html><body>Service temporarily unavailable</body></html>".encode("utf-8")
    fetcher = MarkerValidatingFetcher(
        {"https://official.example/152": ("152-ФЗ", "О персональных данных")},
        inner=StaticFetcher(html),
    )

    with pytest.raises(AcquisitionError, match="missing markers"):
        fetcher.fetch(
            "https://official.example/152",
            timeout_seconds=1,
            max_bytes=10000,
        )


def test_identity_validation_requires_markers_for_live_url():
    fetcher = MarkerValidatingFetcher({}, inner=StaticFetcher(b"text", "text/plain"))

    with pytest.raises(AcquisitionError, match="not configured"):
        fetcher.fetch(
            "https://official.example/unregistered",
            timeout_seconds=1,
            max_bytes=10000,
        )
