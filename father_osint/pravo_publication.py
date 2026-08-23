from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from typing import Any, Protocol

from .acquisition import ArtifactFetcher
from .official_transport import CurlArtifactFetcher


DEFAULT_BASE_URL = "https://publication.pravo.gov.ru"
MAX_JSON_BYTES = 5 * 1024 * 1024
OFFICIAL_API_HOST = "publication.pravo.gov.ru"


class PravoPublicationError(RuntimeError):
    pass


class JsonTransport(Protocol):
    def get_json(self, url: str, *, timeout_seconds: float, max_bytes: int) -> dict[str, Any]:
        ...


def _validate_final_url(final_url: str) -> None:
    parsed = urllib.parse.urlparse(final_url)
    if parsed.scheme != "https" or (parsed.hostname or "").casefold() != OFFICIAL_API_HOST:
        raise PravoPublicationError(
            f"official publication API redirected off-policy or downgraded transport: {final_url}"
        )


def _decode_json(raw: bytes) -> dict[str, Any]:
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PravoPublicationError("official publication API returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise PravoPublicationError("official publication API JSON root must be an object")
    return payload


class UrllibJsonTransport:
    user_agent = "FATHER-KnowledgeFactory/pravo-publication-discovery"

    def __init__(self) -> None:
        self.last_transport = "urllib_https"
        self.last_failures: list[str] = []

    def get_json(self, url: str, *, timeout_seconds: float, max_bytes: int) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                raw = response.read(max_bytes + 1)
                if len(raw) > max_bytes:
                    raise PravoPublicationError(f"JSON response exceeds max_bytes={max_bytes}")
                final_url = response.geturl()
        except PravoPublicationError:
            raise
        except Exception as exc:
            raise PravoPublicationError(f"official publication API urllib request failed: {exc}") from exc

        _validate_final_url(final_url)
        self.last_transport = "urllib_https"
        self.last_failures = []
        return _decode_json(raw)


class CurlJsonTransport:
    """HTTPS-only curl fallback for official publication metadata.

    No HTTP downgrade and no TLS bypass are allowed. This exists for
    workstation-specific Python/urllib networking failures only.
    """

    def __init__(self, artifact_fetcher: ArtifactFetcher | None = None) -> None:
        self.artifact_fetcher = artifact_fetcher or CurlArtifactFetcher()
        self.last_transport = "curl_https"
        self.last_failures: list[str] = []

    def get_json(self, url: str, *, timeout_seconds: float, max_bytes: int) -> dict[str, Any]:
        try:
            fetched = self.artifact_fetcher.fetch(
                url,
                timeout_seconds=timeout_seconds,
                max_bytes=max_bytes,
            )
        except Exception as exc:
            raise PravoPublicationError(f"official publication API curl request failed: {exc}") from exc
        final_url = fetched.final_url or url
        _validate_final_url(final_url)
        self.last_transport = "curl_https"
        self.last_failures = []
        return _decode_json(fetched.data)


class ResilientJsonTransport:
    """Bounded urllib -> curl HTTPS failover for metadata discovery.

    The primary urllib attempt is capped so a local WinError/SSL stall does not
    dominate the whole probe. The curl fallback receives the remaining timeout
    budget. Metadata still cannot satisfy D2/D3.
    """

    def __init__(
        self,
        *,
        primary: JsonTransport | None = None,
        fallback: JsonTransport | None = None,
        primary_timeout_cap_seconds: float = 8.0,
    ) -> None:
        if primary_timeout_cap_seconds <= 0:
            raise ValueError("primary_timeout_cap_seconds must be > 0")
        self.primary = primary or UrllibJsonTransport()
        self.fallback = fallback or CurlJsonTransport()
        self.primary_timeout_cap_seconds = float(primary_timeout_cap_seconds)
        self.last_transport: str | None = None
        self.last_failures: list[str] = []

    def get_json(self, url: str, *, timeout_seconds: float, max_bytes: int) -> dict[str, Any]:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        primary_timeout = min(float(timeout_seconds), self.primary_timeout_cap_seconds)
        failures: list[str] = []
        try:
            payload = self.primary.get_json(
                url,
                timeout_seconds=primary_timeout,
                max_bytes=max_bytes,
            )
            self.last_transport = getattr(self.primary, "last_transport", "primary")
            self.last_failures = failures
            return payload
        except Exception as exc:
            failures.append(f"primary={type(exc).__name__}: {exc}")

        fallback_timeout = max(1.0, float(timeout_seconds) - primary_timeout)
        try:
            payload = self.fallback.get_json(
                url,
                timeout_seconds=fallback_timeout,
                max_bytes=max_bytes,
            )
            self.last_transport = getattr(self.fallback, "last_transport", "fallback")
            self.last_failures = failures
            return payload
        except Exception as exc:
            failures.append(f"fallback={type(exc).__name__}: {exc}")
            self.last_transport = None
            self.last_failures = failures
            raise PravoPublicationError(
                "official publication API transports failed; " + "; ".join(failures)
            ) from exc


@dataclass(frozen=True, slots=True)
class PravoPublicationHit:
    eo_number: str
    number: str
    title: str
    document_date: str
    publish_date: str
    pdf_file_length: int | None
    zip_file_length: int | None
    raw: dict[str, Any]

    @classmethod
    def from_api(cls, item: dict[str, Any]) -> "PravoPublicationHit":
        return cls(
            eo_number=str(item.get("eoNumber") or "").strip(),
            number=str(item.get("number") or "").strip(),
            title=str(item.get("title") or item.get("complexName") or item.get("name") or "").strip(),
            document_date=str(item.get("documentDate") or item.get("documentDateShort") or "").strip(),
            publish_date=str(item.get("publishDateShort") or item.get("publishDate") or "").strip(),
            pdf_file_length=_optional_int(item.get("pdfFileLength")),
            zip_file_length=_optional_int(item.get("zipFileLength")),
            raw=dict(item),
        )


def _optional_int(value: object) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise PravoPublicationError(f"invalid file-length metadata: {value!r}") from exc


def _normalize_number(value: str) -> str:
    return (
        value.casefold()
        .replace("ё", "е")
        .replace("–", "-")
        .replace("—", "-")
        .replace(" ", "")
    )


def _normalize_date(value: str) -> str:
    raw = value.strip()
    if not raw:
        return ""
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            if fmt == "%Y-%m-%d":
                return date.fromisoformat(raw).isoformat()
            import datetime as _dt
            return _dt.datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return raw.casefold()


class PravoPublicationClient:
    """Read-only discovery adapter for publication.pravo.gov.ru.

    Search/detail records are metadata candidates only. Exact bytes must still
    pass the normal AcquisitionService evidence/hash/source-policy boundary.
    """

    def __init__(self, *, base_url: str = DEFAULT_BASE_URL, transport: JsonTransport | None = None) -> None:
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme != "https" or (parsed.hostname or "").casefold() != OFFICIAL_API_HOST:
            raise ValueError("base_url must be https://publication.pravo.gov.ru")
        self.base_url = base_url.rstrip("/")
        self.transport = transport or ResilientJsonTransport()

    def _url(self, path: str, params: dict[str, object]) -> str:
        query = urllib.parse.urlencode([(key, value) for key, value in params.items() if value is not None])
        return f"{self.base_url}/{path.lstrip('/')}?{query}"

    def _transport_meta(self) -> dict[str, Any]:
        return {
            "transport": getattr(self.transport, "last_transport", None),
            "transport_failures_before_success": list(getattr(self.transport, "last_failures", []) or []),
        }

    def search_documents(
        self,
        *,
        number: str,
        document_date_from: str | None = None,
        document_date_to: str | None = None,
        page_size: int = 30,
        page: int = 1,
        timeout_seconds: float = 30.0,
    ) -> tuple[list[PravoPublicationHit], dict[str, Any]]:
        if not number.strip():
            raise ValueError("number is required")
        if page_size not in {10, 30, 100, 200}:
            raise ValueError("page_size must be one of 10, 30, 100, 200")
        if page < 1:
            raise ValueError("page must be >= 1")
        params: dict[str, object] = {
            "NumberSearchType": 0,
            "Number": number,
            "DocumentDateFrom": document_date_from,
            "DocumentDateTo": document_date_to,
            "PageSize": page_size,
            "Index": page,
        }
        url = self._url("api/Documents", params)
        payload = self.transport.get_json(url, timeout_seconds=timeout_seconds, max_bytes=MAX_JSON_BYTES)
        items = payload.get("items") or []
        if not isinstance(items, list):
            raise PravoPublicationError("api/Documents items must be a list")
        hits = [PravoPublicationHit.from_api(item) for item in items if isinstance(item, dict)]
        meta = {"url": url, "item_count": len(hits), "metadata_only": True}
        meta.update(self._transport_meta())
        return hits, meta

    def get_document(self, eo_number: str, *, timeout_seconds: float = 30.0) -> dict[str, Any]:
        if not eo_number.strip():
            raise ValueError("eo_number is required")
        url = self._url("api/Document", {"eoNumber": eo_number})
        payload = self.transport.get_json(url, timeout_seconds=timeout_seconds, max_bytes=MAX_JSON_BYTES)
        payload = dict(payload)
        payload["_father_discovery_url"] = url
        payload["_father_metadata_only"] = True
        payload["_father_transport"] = getattr(self.transport, "last_transport", None)
        payload["_father_transport_failures_before_success"] = list(
            getattr(self.transport, "last_failures", []) or []
        )
        return payload

    def pdf_url(self, eo_number: str) -> str:
        if not eo_number.strip():
            raise ValueError("eo_number is required")
        return self._url("File/Pdf", {"eoNumber": eo_number})

    def zip_url(self, eo_number: str) -> str:
        if not eo_number.strip():
            raise ValueError("eo_number is required")
        return self._url("File/Zip", {"eoNumber": eo_number})

    @staticmethod
    def exact_identity_hits(hits: list[PravoPublicationHit], *, number: str, document_date: str) -> list[PravoPublicationHit]:
        target_number = _normalize_number(number)
        target_date = _normalize_date(document_date)
        result: list[PravoPublicationHit] = []
        for hit in hits:
            hit_date = _normalize_date(hit.document_date)
            if _normalize_number(hit.number) == target_number and hit_date == target_date:
                result.append(hit)
        return result
