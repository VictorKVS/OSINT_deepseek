from __future__ import annotations

from typing import Mapping, Sequence

from .acquisition import (
    AcquisitionError,
    ArtifactFetcher,
    FetchedArtifact,
    UrllibArtifactFetcher,
)
from .document_compiler import DocumentCompilerError, extract_visible_text


class MarkerValidatingFetcher:
    """Validate fetched official artifacts before AcquisitionService persists them.

    A successful HTTP response from an approved domain is not sufficient proof
    that the intended legal document was returned. The requested URL is mapped
    to required case-insensitive text markers. Missing markers fail closed.
    """

    def __init__(
        self,
        required_markers_by_url: Mapping[str, Sequence[str]],
        *,
        inner: ArtifactFetcher | None = None,
    ) -> None:
        self.required_markers_by_url = {
            str(url): tuple(marker.strip() for marker in markers if marker.strip())
            for url, markers in required_markers_by_url.items()
        }
        self.inner = inner or UrllibArtifactFetcher()

    @staticmethod
    def _normalized(value: str) -> str:
        return " ".join(value.casefold().replace("ё", "е").split())

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        markers = self.required_markers_by_url.get(url)
        if not markers:
            raise AcquisitionError("identity validation markers are not configured for this source URL")

        artifact = self.inner.fetch(
            url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
        try:
            text = extract_visible_text(artifact.data, artifact.mime_type)
        except DocumentCompilerError as exc:
            raise AcquisitionError(f"artifact identity validation cannot extract text: {exc}") from exc

        normalized_text = self._normalized(text)
        missing = [
            marker
            for marker in markers
            if self._normalized(marker) not in normalized_text
        ]
        if missing:
            joined = "; ".join(missing)
            raise AcquisitionError(f"artifact identity validation failed; missing markers: {joined}")

        return artifact
