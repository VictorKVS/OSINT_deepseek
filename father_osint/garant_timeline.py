from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from datetime import date


_RU_MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}

_ACT_RE = re.compile(
    r"^(?P<title>.+?)\s+от\s+(?P<day>\d{1,2})\s+"
    r"(?P<month>[а-яё]+)\s+(?P<year>\d{4})\s*г\.?\s*"
    r"(?:№|N)\s*(?P<number>[0-9A-Za-zА-Яа-яЁё\-–—]+)\s*$",
    re.IGNORECASE,
)

# Browser-saved GARANT HTML may collapse block boundaries so an amending act
# and its effective-rule text become one logical line. This tolerant matcher
# intentionally looks only for act identity metadata and does not mirror legal
# or commentary text.
_ACT_INLINE_RE = re.compile(
    r"(?P<title>(?:Федеральный\s+закон|Приказ\s+[^\n]{1,220}?))\s+от\s+"
    r"(?P<day>\d{1,2})\s+(?P<month>января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+"
    r"(?P<year>\d{4})\s*г\.?\s*(?:№|N)\s*"
    r"(?P<number>[0-9A-Za-zА-Яа-яЁё\-–—]+)",
    re.IGNORECASE,
)

_DATE_RE = re.compile(
    r"(?P<day>\d{1,2})\s+(?P<month>января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+(?P<year>\d{4})\s*г\.?'?",
    re.IGNORECASE,
)

_DAY_MONTH_RE = re.compile(
    r"(?P<day>\d{1,2})\s+(?P<month>января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)",
    re.IGNORECASE,
)

_YEAR_GROUP_RE = re.compile(r"(?P<body>.*?)(?P<year>\d{4})\s*г\.?", re.IGNORECASE)

_EFFECTIVE_INLINE_RE = re.compile(
    r"(?P<rule>Изменени[яе]\s+вступ\w*\s+в\s+сил\w*\s+.{0,500}?)"
    r"(?=(?:\s+См\.|\s+(?:Федеральный\s+закон|Приказ\s+)\b|$))",
    re.IGNORECASE,
)

_COMPACT_HISTORY_RE = re.compile(
    r"С\s+изменениями\s+и\s+дополнениями\s+от:\s*"
    r"(?P<history>.*?)"
    r"(?=(?:\s+Принят\b|\s+Одобрен\b|\s+См\.\s|\s+Глава\s+\d|\s+Статья\s+\d|\s+Президент\s+Российской\s+Федерации\b|$))",
    re.IGNORECASE | re.DOTALL,
)


def _stable_id(prefix: str, *parts: str) -> str:
    canonical = "\x1f".join(" ".join(part.split()).casefold() for part in parts)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20]
    return f"{prefix}-{digest}"


def _effective_date_basis(effective_rule: str, effective_dates: tuple[str, ...]) -> str:
    """Classify what A0/A1 evidence is needed without inferring a legal date."""

    if effective_dates:
        return "EXPLICIT_CALENDAR_DATE"
    normalized = effective_rule.casefold().replace("ё", "е")
    if "официального опубликован" in normalized:
        return "RELATIVE_TO_OFFICIAL_PUBLICATION"
    return "NON_CALENDAR_RULE"


@dataclass(frozen=True, slots=True)
class GarantAmendmentEvent:
    amending_act_title: str
    amending_act_number: str
    amending_act_date: str
    effective_dates: tuple[str, ...]
    effective_rule: str
    source_id: str = "SRC-RU-GARANT-001"
    evidence_state: str = "OFFICIAL_EVIDENCE_PENDING"

    @property
    def event_id(self) -> str:
        return _stable_id(
            "GTE",
            self.source_id,
            self.amending_act_title,
            self.amending_act_date,
            self.amending_act_number,
        )

    @property
    def effective_date_basis(self) -> str:
        return _effective_date_basis(self.effective_rule, self.effective_dates)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["event_id"] = self.event_id
        payload["effective_dates"] = list(self.effective_dates)
        payload["effective_date_basis"] = self.effective_date_basis
        return payload


@dataclass(frozen=True, slots=True)
class GarantAmendmentDateHint:
    amendment_date: str
    source_id: str = "SRC-RU-GARANT-001"
    evidence_state: str = "A2_NAVIGATION_HINT_ONLY"

    @property
    def hint_id(self) -> str:
        return _stable_id("GTH", self.source_id, self.amendment_date)

    def to_dict(self) -> dict[str, str]:
        return {
            "hint_id": self.hint_id,
            "amendment_date": self.amendment_date,
            "source_id": self.source_id,
            "evidence_state": self.evidence_state,
        }


@dataclass(frozen=True, slots=True)
class GarantTimelineCapture:
    document_id: str
    source_url: str
    observed_on: str
    events: tuple[GarantAmendmentEvent, ...]
    future_edition_signalled: bool
    amendment_date_hints: tuple[GarantAmendmentDateHint, ...] = ()
    source_role: str = "VERSION_TIMELINE_PROVIDER"
    semantic_text_mirrored: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "document_id": self.document_id,
            "source_url": self.source_url,
            "observed_on": self.observed_on,
            "source_role": self.source_role,
            "semantic_text_mirrored": self.semantic_text_mirrored,
            "future_edition_signalled": self.future_edition_signalled,
            "events": [event.to_dict() for event in self.events],
            "amendment_date_hints": [hint.to_dict() for hint in self.amendment_date_hints],
        }


def _normalize_lines(text: str) -> list[str]:
    return [" ".join(line.replace("\xa0", " ").split()) for line in text.splitlines() if line.strip()]


def _iso_date(day: str, month: str, year: str) -> str:
    month_number = _RU_MONTHS[month.casefold()]
    return date(int(year), month_number, int(day)).isoformat()


def _extract_explicit_dates(text: str) -> tuple[str, ...]:
    values: list[str] = []
    for match in _DATE_RE.finditer(text):
        value = _iso_date(match.group("day"), match.group("month"), match.group("year"))
        if value not in values:
            values.append(value)
    return tuple(values)


def _is_effective_rule(line: str) -> bool:
    lowered = line.casefold().replace("ё", "е")
    return "изменени" in lowered and "вступ" in lowered and "сил" in lowered


def _dedupe_events(events: list[GarantAmendmentEvent]) -> list[GarantAmendmentEvent]:
    deduped: list[GarantAmendmentEvent] = []
    seen: set[tuple[str, str]] = set()
    for event in events:
        key = (event.amending_act_date, event.amending_act_number.casefold())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(event)
    return deduped


def _recover_inline_events(text: str) -> list[GarantAmendmentEvent]:
    """Recover timeline metadata when browser HTML collapses logical lines.

    The scan is bounded to the text between consecutive act-identity matches.
    An event is emitted only when an explicit "Изменения вступ... в силу..."
    rule is present in the same segment. This avoids treating arbitrary legal
    citations inside the document body as amendment events.
    """

    flat = " ".join(text.replace("\xa0", " ").split())
    matches = list(_ACT_INLINE_RE.finditer(flat))
    events: list[GarantAmendmentEvent] = []

    for index, match in enumerate(matches):
        segment_end = matches[index + 1].start() if index + 1 < len(matches) else min(len(flat), match.end() + 1200)
        segment = flat[match.end():segment_end]
        rule_match = _EFFECTIVE_INLINE_RE.search(segment)
        if not rule_match:
            continue
        effective_rule = " ".join(rule_match.group("rule").split())
        events.append(
            GarantAmendmentEvent(
                amending_act_title=" ".join(match.group("title").split()),
                amending_act_number=match.group("number").strip(),
                amending_act_date=_iso_date(
                    match.group("day"),
                    match.group("month"),
                    match.group("year"),
                ),
                effective_dates=_extract_explicit_dates(effective_rule),
                effective_rule=effective_rule,
            )
        )

    return _dedupe_events(events)


def _extract_compact_amendment_date_hints(text: str) -> tuple[GarantAmendmentDateHint, ...]:
    """Parse GARANT's compact `С изменениями и дополнениями от:` date list.

    These are navigation hints only. A compact list does not identify the
    amending act or prove an effective date, so no official-evidence request is
    emitted from these hints alone.
    """

    flat = " ".join(text.replace("\xa0", " ").split())
    match = _COMPACT_HISTORY_RE.search(flat)
    if not match:
        return ()

    history = match.group("history")
    hints: list[GarantAmendmentDateHint] = []
    seen: set[str] = set()
    cursor = 0
    for year_match in _YEAR_GROUP_RE.finditer(history):
        group_text = history[cursor:year_match.end()]
        cursor = year_match.end()
        year = year_match.group("year")
        for date_match in _DAY_MONTH_RE.finditer(group_text):
            value = _iso_date(date_match.group("day"), date_match.group("month"), year)
            if value in seen:
                continue
            seen.add(value)
            hints.append(GarantAmendmentDateHint(amendment_date=value))
    return tuple(hints)


def parse_garant_timeline_text(
    *,
    document_id: str,
    source_url: str,
    observed_on: str,
    text: str,
) -> GarantTimelineCapture:
    """Extract amendment/version metadata from a locally supplied GARANT page.

    The parser intentionally captures only temporal/legal metadata: amending act
    identity, act date, effective-date expressions and future-edition signals.
    If a downloaded working copy contains only GARANT's compact amendment-date
    list, those dates are kept as A2 navigation hints and are not promoted to
    verified amendment events.
    """

    if not document_id.strip() or not source_url.strip() or not observed_on.strip():
        raise ValueError("document_id, source_url and observed_on are required")

    lines = _normalize_lines(text)
    events: list[GarantAmendmentEvent] = []

    for index, line in enumerate(lines):
        match = _ACT_RE.match(line)
        if not match:
            continue

        effective_rule = ""
        effective_dates: tuple[str, ...] = ()
        for follower in lines[index + 1:index + 5]:
            if _is_effective_rule(follower):
                effective_rule = follower
                effective_dates = _extract_explicit_dates(follower)
                break
            if _ACT_RE.match(follower):
                break

        if not effective_rule:
            continue

        events.append(
            GarantAmendmentEvent(
                amending_act_title=match.group("title").strip(),
                amending_act_number=match.group("number").strip(),
                amending_act_date=_iso_date(
                    match.group("day"),
                    match.group("month"),
                    match.group("year"),
                ),
                effective_dates=effective_dates,
                effective_rule=effective_rule,
            )
        )

    deduped = _dedupe_events(events)
    if not deduped:
        deduped = _recover_inline_events(text)

    amendment_date_hints = _extract_compact_amendment_date_hints(text)

    future_signal = any(
        "будущ" in line.casefold().replace("ё", "е") and "редакц" in line.casefold().replace("ё", "е")
        for line in lines
    )

    return GarantTimelineCapture(
        document_id=document_id,
        source_url=source_url,
        observed_on=observed_on,
        events=tuple(deduped),
        future_edition_signalled=future_signal,
        amendment_date_hints=amendment_date_hints,
    )


def _required_official_evidence(event: GarantAmendmentEvent) -> list[str]:
    requirements = [
        "AMENDING_ACT_IDENTITY",
        "AMENDING_ACT_OFFICIAL_TEXT",
        "EFFECTIVE_RULE",
    ]
    if event.effective_date_basis == "EXPLICIT_CALENDAR_DATE":
        requirements.append("EXPLICIT_EFFECTIVE_DATE")
    elif event.effective_date_basis == "RELATIVE_TO_OFFICIAL_PUBLICATION":
        requirements.append("OFFICIAL_PUBLICATION_DATE")
    else:
        requirements.append("EFFECTIVE_DATE_RESOLUTION")
    return requirements


def official_evidence_requests(
    capture: GarantTimelineCapture,
    *,
    source_capture_sha256: str | None = None,
) -> tuple[dict[str, object], ...]:
    """Convert detailed timeline events into traceable A0/A1 evidence requests.

    Compact amendment-date hints are intentionally excluded because a date alone
    does not establish the identity of the amending act.
    """

    requests: list[dict[str, object]] = []
    for event in capture.events:
        request_id = _stable_id("OER", capture.document_id, event.event_id)
        request: dict[str, object] = {
            "evidence_request_id": request_id,
            "timeline_event_id": event.event_id,
            "document_id": capture.document_id,
            "amending_act_title": event.amending_act_title,
            "amending_act_number": event.amending_act_number,
            "amending_act_date": event.amending_act_date,
            "effective_dates": list(event.effective_dates),
            "effective_rule": event.effective_rule,
            "effective_date_basis": event.effective_date_basis,
            "required_official_evidence": _required_official_evidence(event),
            "locator_strategy": "SEARCH_A0_A1_BY_ACT_IDENTITY",
            "timeline_source_id": event.source_id,
            "timeline_source_url": capture.source_url,
            "timeline_observed_on": capture.observed_on,
            "required_evidence_tier": "A0_OR_A1",
            "status": "EVIDENCE_PENDING",
        }
        if source_capture_sha256 is not None:
            normalized_hash = source_capture_sha256.strip().lower()
            if len(normalized_hash) != 64 or any(ch not in "0123456789abcdef" for ch in normalized_hash):
                raise ValueError("source_capture_sha256 must be a 64-character hexadecimal digest")
            request["timeline_source_capture_sha256"] = normalized_hash
        requests.append(request)
    return tuple(requests)
