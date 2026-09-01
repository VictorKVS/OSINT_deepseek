from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Mapping

from .acquisition import AcquisitionError, FetchedArtifact


class OperatorImportArtifactFetcher:
    """Read exact operator-saved bytes while preserving the approved official URL.

    This is a transport adapter, not a trust bypass. The caller is expected to
    wrap it in MarkerValidatingFetcher and then pass it through the normal
    AcquisitionService, which still applies source policy, final-host policy,
    SHA-256, versioning, audit, and D0-D3 state rules.
    """

    def __init__(self, files_by_url: Mapping[str, str | Path]) -> None:
        self.files_by_url = {str(url): Path(path) for url, path in files_by_url.items()}

    def fetch(self, url: str, *, timeout_seconds: float, max_bytes: int) -> FetchedArtifact:
        del timeout_seconds  # local exact-byte import is bounded by max_bytes, not network time
        path = self.files_by_url.get(url)
        if path is None:
            raise AcquisitionError("operator-assisted file is missing for this official URL")
        if not path.exists():
            raise AcquisitionError(f"operator-assisted file does not exist: {path}")
        if not path.is_file():
            raise AcquisitionError(f"operator-assisted path is not a file: {path}")

        size = path.stat().st_size
        if size <= 0:
            raise AcquisitionError("operator-assisted file is empty")
        if size > max_bytes:
            raise AcquisitionError(f"artifact exceeds max_bytes={max_bytes}")

        data = path.read_bytes()
        if len(data) != size:
            raise AcquisitionError("operator-assisted file changed while being read")

        mime_type, _ = mimetypes.guess_type(path.name)
        suffix = path.suffix.casefold()
        if suffix in {".html", ".htm"}:
            mime_type = "text/html"
        elif suffix == ".txt":
            mime_type = "text/plain"
        elif suffix == ".json":
            mime_type = "application/json"

        return FetchedArtifact(
            data=data,
            mime_type=mime_type or "application/octet-stream",
            final_url=url,
        )
