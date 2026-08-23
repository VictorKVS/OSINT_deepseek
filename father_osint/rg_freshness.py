from __future__ import annotations

from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from typing import Iterable, Mapping, Sequence
from urllib.parse import urljoin, urlparse

from .acquisition import ArtifactFetcher
from .freshness_discovery import FreshnessWatchTarget
from .official_transport import CurlArtifactFetcher


RG_INDEX_URL = "https://www.rg.ru/doc"
RG_ALLOWED_HOSTS = {"rg.ru", "www.rg.ru"}
MAX_INDEX_BYTES = 8 * 1024 * 1024


def _norm(value: object) -> str:
    return " ".join(
        str(value or "")
        .casefold()
        .replace("ё", "е")
        .replace("–", "-")
        .replace("—", "-")
        .split()
    )


class _AnchorCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._href: str | None = None
        self._parts: list[str] = []
        self.anchors: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() != "a" or self._href is not None:
            return
        href = dict(attrs).get("href")
        if href:
            self._href = href
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._href is not None and data.strip():
            self._parts.append(data.strip())

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() != "a" or self._href is None:
            return
        text = " ".join(self._parts).strip()
        self.anchors.append((self._href, text))
        self._href = None
        self._parts = []


@dataclass(frozen=True, slots=True)
class RgIndexCandidate:
    document_id: str
    title: str
    url: str
    matched_marker: str
    source_key: str = "rg-official-doc-index"
    candidate_only: bool = True
    exact_bytes_acquired: bool = False
    d2_d3_promoted: bool = False
    current_claim_allowed: bool = False
    legal_truth_promoted: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RgIndexScanResult:
    source_key: str
    index_url: str
    status: str
    candidates: tuple[RgIndexCandidate, ...]
    anchors_total: int
    document_links_total: int
    transport: str
    metadata_only: bool = True
    coverage_complete_for_checkpoint: bool = False
    exact_bytes_acquired: bool = False
    d2_d3_promoted: bool = False
    current_claim_allowed: bool = False
    legal_truth_promoted: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            **asdict(self),
            "candidates": [candidate.to_dict() for candidate in self.candidates],
        }


def _target_markers(target: FreshnessWatchTarget) -> tuple[str, ...]:
    markers = tuple(value for value in target.secondary_markers if value.strip())
    if markers:
        return markers
    return (target.query_text,)


def scan_rg_document_index_html(
    data: bytes,
    *,
    targets: Sequence[FreshnessWatchTarget],
    index_url: str = RG_INDEX_URL,
) -> RgIndexScanResult:
    try:
        html = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("RG document index is not valid UTF-8") from exc

    parser = _AnchorCollector()
    parser.feed(html)

    document_links: list[tuple[str, str]] = []
    seen_urls: set[str] = set()
    for href, title in parser.anchors:
        url = urljoin(index_url, href)
        parsed = urlparse(url)
        if parsed.scheme != "https" or (parsed.hostname or "").casefold() not in RG_ALLOWED_HOSTS:
            continue
        if "/documents/" not in parsed.path:
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        document_links.append((url, title))

    candidates: list[RgIndexCandidate] = []
    seen_candidate_pairs: set[tuple[str, str]] = set()
    for target in targets:
        markers = _target_markers(target)
        normalized_markers = [(_norm(marker), marker) for marker in markers if _norm(marker)]
        for url, title in document_links:
            normalized_title = _norm(title)
            matched = next((raw for normalized, raw in normalized_markers if normalized in normalized_title), None)
            if matched is None:
                continue
            pair = (target.document_id, url)
            if pair in seen_candidate_pairs:
                continue
            seen_candidate_pairs.add(pair)
            candidates.append(
                RgIndexCandidate(
                    document_id=target.document_id,
                    title=title,
                    url=url,
                    matched_marker=matched,
                )
            )

    return RgIndexScanResult(
        source_key="rg-official-doc-index",
        index_url=index_url,
        status="CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION" if candidates else "NO_CANDIDATE_IN_CURRENT_INDEX",
        candidates=tuple(candidates),
        anchors_total=len(parser.anchors),
        document_links_total=len(document_links),
        transport="provided_html",
    )


class RgDocumentIndexDiscovery:
    """Secondary discovery-only route over the Russian Gazette document index.

    The RG index can surface candidate official-publication pages when the
    publication.pravo.gov.ru API is unavailable. It is intentionally not treated
    as complete backfill coverage and therefore can never advance the freshness
    checkpoint by itself. Exact article bytes must still pass normal acquisition
    and identity/hash gates before any new DocumentVersion exists.
    """

    def __init__(
        self,
        *,
        fetcher: ArtifactFetcher | None = None,
        index_url: str = RG_INDEX_URL,
    ) -> None:
        parsed = urlparse(index_url)
        if parsed.scheme != "https" or (parsed.hostname or "").casefold() not in RG_ALLOWED_HOSTS:
            raise ValueError("RG index URL must stay on an approved HTTPS rg.ru host")
        self.fetcher = fetcher or CurlArtifactFetcher()
        self.index_url = index_url

    def scan(
        self,
        *,
        targets: Sequence[FreshnessWatchTarget],
        timeout_seconds: float = 8.0,
    ) -> RgIndexScanResult:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        fetched = self.fetcher.fetch(
            self.index_url,
            timeout_seconds=timeout_seconds,
            max_bytes=MAX_INDEX_BYTES,
        )
        final_url = fetched.final_url or self.index_url
        parsed = urlparse(final_url)
        if parsed.scheme != "https" or (parsed.hostname or "").casefold() not in RG_ALLOWED_HOSTS:
            raise ValueError(f"RG discovery redirected off-policy: {final_url}")
        result = scan_rg_document_index_html(
            fetched.data,
            targets=targets,
            index_url=final_url,
        )
        return RgIndexScanResult(
            source_key=result.source_key,
            index_url=final_url,
            status=result.status,
            candidates=result.candidates,
            anchors_total=result.anchors_total,
            document_links_total=result.document_links_total,
            transport=type(self.fetcher).__name__,
        )
