from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import date
from typing import Iterable


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

_DATE_RE = re.compile(
    r"(?P<day>\d{1,2})\s+(?P<month>января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+(?P<year>\d{4})\s*г\.?'?",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class GarantAmendmentEvent:
    amending_act_title: str
    amending_act_number: str
    amending_act_date: str
    effective_dates: tuple[str, ...]
    effective_rule: str
    source_id: str = "SRC-RU-GARANT-001"
    evidence_state: str = "OFFICIAL_EVIDENCE_PENDING"

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["effective_dates"] = list(self.effective_dates)
        return payload


@dataclass(frozen=True, slots=True)
class GarantTimelineCapture:
    document_id: str
    source_url: str
    observed_on: str
    events: tuple[GarantAmendmentEvent, ...]
    future_edition_signalled: bool
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
    It does not mirror the legal text or GARANT commentary.
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

    deduped: list[GarantAmendmentEvent] = []
    seen: set[tuple[str, str]] = set()
    for event in events:
        key = (event.amending_act_date, event.amending_act_number.casefold())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(event)

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
    )


def official_evidence_requests(capture: GarantTimelineCapture) -> tuple[dict[str, object], ...]:
    """Convert timeline hints into evidence requests without promoting A2 metadata to proof."""

    requests: list[dict[str, object]] = []
    for event in capture.events:
        requests.append(
            {
                "document_id": capture.document_id,
                "amending_act_number": event.amending_act_number,
                "amending_act_date": event.amending_act_date,
                "effective_dates": list(event.effective_dates),
                "timeline_source_id": event.source_id,
                "required_evidence_tier": "A0_OR_A1",
                "status": "EVIDENCE_PENDING",
            }
        )
    return tuple(requests)
