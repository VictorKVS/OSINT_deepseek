from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from typing import Any, Mapping

from .pravo_publication import MAX_JSON_BYTES, PravoPublicationClient, PravoPublicationError, PravoPublicationHit


@dataclass(frozen=True, slots=True)
class FreshnessWatchTarget:
    document_id: str
    query_text: str
    query_basis: str
    secondary_markers: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, row: Mapping[str, object]) -> "FreshnessWatchTarget":
        document_id = str(row.get("document_id") or "").strip()
        query_text = str(row.get("query_text") or "").strip()
        query_basis = str(row.get("query_basis") or "").strip()
        raw_markers = row.get("secondary_markers") or []
        if not isinstance(raw_markers, list):
            raise ValueError("secondary_markers must be a list when present")
        secondary_markers = tuple(str(value).strip() for value in raw_markers if str(value).strip())
        if not document_id or not query_text or not query_basis:
            raise ValueError("freshness watch target requires document_id, query_text and query_basis")
        return cls(
            document_id=document_id,
            query_text=query_text,
            query_basis=query_basis,
            secondary_markers=secondary_markers,
        )


@dataclass(frozen=True, slots=True)
class FreshnessTargetObservation:
    document_id: str
    query_text: str
    query_basis: str
    status: str
    candidate_events: tuple[dict[str, object], ...]
    discovery_url: str | None
    transport: str | None
    transport_failures: tuple[str, ...]
    metadata_only: bool = True
    exact_bytes_acquired: bool = False
    d2_d3_promoted: bool = False
    current_claim_allowed: bool = False
    legal_truth_promoted: bool = False
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def load_watchlist(payload: Mapping[str, object]) -> tuple[FreshnessWatchTarget, ...]:
    rows = payload.get("targets")
    if not isinstance(rows, list) or not rows:
        raise ValueError("freshness watchlist targets must be a non-empty list")
    targets = tuple(FreshnessWatchTarget.from_mapping(row) for row in rows if isinstance(row, Mapping))
    if len(targets) != len(rows):
        raise ValueError("freshness watchlist contains a non-object target")
    ids = [target.document_id for target in targets]
    if len(ids) != len(set(ids)):
        raise ValueError("freshness watchlist document_id values must be unique")
    return targets


def _iso_date(value: str) -> str:
    return date.fromisoformat(value).isoformat()


class PravoReferenceDiscovery:
    """Discovery-only adapter for recent publication events referencing a target act.

    It intentionally reuses PravoPublicationClient transport, host/TLS policy and
    item model. Results are metadata candidates only: they cannot prove current
    legal state or create a new DocumentVersion without later exact acquisition.
    """

    def __init__(self, client: PravoPublicationClient | None = None) -> None:
        self.client = client or PravoPublicationClient()

    def search_recent_reference(
        self,
        target: FreshnessWatchTarget,
        *,
        publish_date_from: str,
        publish_date_to: str,
        timeout_seconds: float = 12.0,
        page_size: int = 30,
    ) -> FreshnessTargetObservation:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        if page_size not in {10, 30, 100, 200}:
            raise ValueError("page_size must be one of 10, 30, 100, 200")
        publish_from = _iso_date(publish_date_from)
        publish_to = _iso_date(publish_date_to)
        if publish_from > publish_to:
            raise ValueError("publish_date_from must not be after publish_date_to")

        # Reuse the official client URL builder and transport boundary instead of
        # creating another downloader/HTTP stack. DocumentText/PublishDate* are
        # public API parameters also used by the reviewed law-parser donor.
        url = self.client._url(
            "api/Documents",
            {
                "DocumentText": target.query_text,
                "PublishDateFrom": publish_from,
                "PublishDateTo": publish_to,
                "PageSize": page_size,
                "Index": 1,
            },
        )
        payload = self.client.transport.get_json(
            url,
            timeout_seconds=timeout_seconds,
            max_bytes=MAX_JSON_BYTES,
        )
        items = payload.get("items") or []
        if not isinstance(items, list):
            raise PravoPublicationError("api/Documents items must be a list")
        hits = [PravoPublicationHit.from_api(item) for item in items if isinstance(item, dict)]
        candidates = tuple(
            {
                "eo_number": hit.eo_number,
                "number": hit.number,
                "title": hit.title,
                "document_date": hit.document_date,
                "publish_date": hit.publish_date,
                "pdf_file_length": hit.pdf_file_length,
                "zip_file_length": hit.zip_file_length,
                "candidate_only": True,
            }
            for hit in hits
        )
        transport = getattr(self.client.transport, "last_transport", None)
        failures = tuple(str(value) for value in (getattr(self.client.transport, "last_failures", []) or []))
        return FreshnessTargetObservation(
            document_id=target.document_id,
            query_text=target.query_text,
            query_basis=target.query_basis,
            status="CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION" if candidates else "NO_CANDIDATE_IN_WINDOW",
            candidate_events=candidates,
            discovery_url=url,
            transport=str(transport) if transport else None,
            transport_failures=failures,
        )


def degraded_observation(
    target: FreshnessWatchTarget,
    *,
    status: str,
    error: str,
) -> FreshnessTargetObservation:
    if status not in {"DEGRADED_SOURCE_CIRCUIT_OPEN", "DEGRADED_SOURCE_UNAVAILABLE", "SKIPPED_AFTER_SOURCE_FAILURE"}:
        raise ValueError("invalid degraded freshness status")
    return FreshnessTargetObservation(
        document_id=target.document_id,
        query_text=target.query_text,
        query_basis=target.query_basis,
        status=status,
        candidate_events=(),
        discovery_url=None,
        transport=None,
        transport_failures=(),
        error=error,
    )
