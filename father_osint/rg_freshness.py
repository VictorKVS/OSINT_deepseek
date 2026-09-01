from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import date
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from typing import Sequence
from urllib.parse import urljoin, urlparse

from .acquisition import ArtifactFetcher
from .freshness_discovery import FreshnessWatchTarget
from .official_transport import CurlArtifactFetcher


RG_INDEX_URL = "https://www.rg.ru/doc"
RG_ANNOUNCEMENT_FEED_URL = "https://rg.ru/xml/index.xml"
RG_ALLOWED_HOSTS = {"rg.ru", "www.rg.ru"}
MAX_INDEX_BYTES = 8 * 1024 * 1024
MAX_FEED_BYTES = 4 * 1024 * 1024
_DOCUMENT_DATE_RE = re.compile(r"/documents/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/")


def _norm(value: object) -> str:
    return " ".join(
        str(value or "")
        .casefold()
        .replace("ё", "е")
        .replace("–", "-")
        .replace("—", "-")
        .split()
    )


def _approved_rg_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").casefold() in RG_ALLOWED_HOSTS


def _date_from_rg_url(url: str) -> str | None:
    match = _DOCUMENT_DATE_RE.search(urlparse(url).path)
    if match is None:
        return None
    try:
        return date(
            int(match.group("year")),
            int(match.group("month")),
            int(match.group("day")),
        ).isoformat()
    except ValueError:
        return None


def _date_from_feed_text(value: str | None) -> str | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw).date().isoformat()
    except (TypeError, ValueError, OverflowError):
        pass
    try:
        return date.fromisoformat(raw[:10]).isoformat()
    except ValueError:
        return None


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].casefold()


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
    publish_date: str | None = None
    discovery_channel: str = "DOCUMENT_INDEX"
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


@dataclass(frozen=True, slots=True)
class RgFeedScanResult:
    source_key: str
    feed_url: str
    status: str
    candidates: tuple[RgIndexCandidate, ...]
    items_total: int
    rg_links_total: int
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
        if not _approved_rg_url(url):
            continue
        if "/documents/" not in urlparse(url).path:
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
                    publish_date=_date_from_rg_url(url),
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


def scan_rg_announcement_feed_xml(
    data: bytes,
    *,
    targets: Sequence[FreshnessWatchTarget],
    feed_url: str = RG_ANNOUNCEMENT_FEED_URL,
    publish_date_from: str | None = None,
    publish_date_to: str | None = None,
) -> RgFeedScanResult:
    """Parse only title/link/date metadata from RG's documented announcement XML feed.

    The feed is a navigation surface, not a complete historical archive. It can
    surface candidates but can never advance the primary freshness checkpoint.
    Full article text is neither mirrored nor promoted here.
    """

    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError("RG announcement feed is invalid XML") from exc

    if publish_date_from is not None:
        publish_date_from = date.fromisoformat(publish_date_from).isoformat()
    if publish_date_to is not None:
        publish_date_to = date.fromisoformat(publish_date_to).isoformat()
    if publish_date_from and publish_date_to and publish_date_from > publish_date_to:
        raise ValueError("publish_date_from must not be after publish_date_to")

    items: list[tuple[str, str, str, str | None]] = []
    rg_links_total = 0
    for item in root.iter():
        if _local_name(item.tag) not in {"item", "entry"}:
            continue
        title = ""
        description = ""
        link = ""
        published_text: str | None = None
        for child in list(item):
            name = _local_name(child.tag)
            text = " ".join("".join(child.itertext()).split())
            if name == "title" and not title:
                title = text
            elif name in {"description", "summary"} and not description:
                description = text
            elif name in {"pubdate", "published", "updated", "date"} and published_text is None:
                published_text = text
            elif name == "link" and not link:
                link = str(child.attrib.get("href") or text or "").strip()
        if not link:
            continue
        absolute = urljoin(feed_url, link)
        if not _approved_rg_url(absolute):
            continue
        rg_links_total += 1
        publish_date = _date_from_rg_url(absolute) or _date_from_feed_text(published_text)
        if publish_date_from and publish_date and publish_date < publish_date_from:
            continue
        if publish_date_to and publish_date and publish_date > publish_date_to:
            continue
        items.append((absolute, title, description, publish_date))

    candidates: list[RgIndexCandidate] = []
    seen: set[tuple[str, str]] = set()
    for target in targets:
        normalized_markers = [(_norm(marker), marker) for marker in _target_markers(target) if _norm(marker)]
        for url, title, description, publish_date in items:
            searchable = _norm(f"{title} {description}")
            matched = next((raw for normalized, raw in normalized_markers if normalized in searchable), None)
            if matched is None:
                continue
            pair = (target.document_id, url)
            if pair in seen:
                continue
            seen.add(pair)
            candidates.append(
                RgIndexCandidate(
                    document_id=target.document_id,
                    title=title,
                    url=url,
                    matched_marker=matched,
                    source_key="rg-official-announcement-feed",
                    publish_date=publish_date,
                    discovery_channel="ANNOUNCEMENT_XML_FEED",
                )
            )

    return RgFeedScanResult(
        source_key="rg-official-announcement-feed",
        feed_url=feed_url,
        status="CANDIDATE_EVENTS_PENDING_EXACT_ACQUISITION" if candidates else "NO_CANDIDATE_IN_CURRENT_FEED",
        candidates=tuple(candidates),
        items_total=len(items),
        rg_links_total=rg_links_total,
        transport="provided_xml",
    )


class RgAnnouncementFeedDiscovery:
    """Secondary candidate-only route over RG's documented XML announcements."""

    def __init__(
        self,
        *,
        fetcher: ArtifactFetcher | None = None,
        feed_url: str = RG_ANNOUNCEMENT_FEED_URL,
    ) -> None:
        if not _approved_rg_url(feed_url):
            raise ValueError("RG feed URL must stay on an approved HTTPS rg.ru host")
        self.fetcher = fetcher or CurlArtifactFetcher()
        self.feed_url = feed_url

    def scan(
        self,
        *,
        targets: Sequence[FreshnessWatchTarget],
        publish_date_from: str | None = None,
        publish_date_to: str | None = None,
        timeout_seconds: float = 8.0,
    ) -> RgFeedScanResult:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        fetched = self.fetcher.fetch(
            self.feed_url,
            timeout_seconds=timeout_seconds,
            max_bytes=MAX_FEED_BYTES,
        )
        final_url = fetched.final_url or self.feed_url
        if not _approved_rg_url(final_url):
            raise ValueError(f"RG feed redirected off-policy: {final_url}")
        result = scan_rg_announcement_feed_xml(
            fetched.data,
            targets=targets,
            feed_url=final_url,
            publish_date_from=publish_date_from,
            publish_date_to=publish_date_to,
        )
        return RgFeedScanResult(
            source_key=result.source_key,
            feed_url=final_url,
            status=result.status,
            candidates=result.candidates,
            items_total=result.items_total,
            rg_links_total=result.rg_links_total,
            transport=type(self.fetcher).__name__,
        )


class RgDocumentIndexDiscovery:
    """Legacy secondary candidate route over the RG document index.

    Kept as a bounded fallback/reference parser because some workstations return
    HTTP 401 for /doc. The documented XML announcement feed is preferred for
    automated discovery. Neither route can advance the primary checkpoint.
    """

    def __init__(
        self,
        *,
        fetcher: ArtifactFetcher | None = None,
        index_url: str = RG_INDEX_URL,
    ) -> None:
        if not _approved_rg_url(index_url):
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
        if not _approved_rg_url(final_url):
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
