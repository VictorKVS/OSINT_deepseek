from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from .canonical import normalize_name
from .policy import strictest_access_class
from .store import WorkbenchStore

EMAIL_RE = re.compile(r"(?<![\w.+-])([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63})(?![\w.-])", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>\]\[(){}\"']+", re.IGNORECASE)
DOMAIN_RE = re.compile(r"(?<![@\w.-])((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63})(?![\w.-])", re.IGNORECASE)
IPV4_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
HANDLE_RE = re.compile(r"(?<![\w@])@([A-Za-z0-9_]{4,32})(?!\w)")
PHONE_RE = re.compile(r"(?<!\d)(\+?\d[\d ()-]{8,}\d)(?!\d)")
ETH_RE = re.compile(r"(?<![A-Fa-f0-9])(0x[A-Fa-f0-9]{40})(?![A-Fa-f0-9])")
TRON_RE = re.compile(r"(?<![A-Za-z0-9])(T[1-9A-HJ-NP-Za-km-z]{33})(?![A-Za-z0-9])")
BTC_RE = re.compile(r"(?<![A-Za-z0-9])((?:bc1)[ac-hj-np-z02-9]{11,71}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})(?![A-Za-z0-9])", re.IGNORECASE)


@dataclass(slots=True)
class ExtractionResult:
    source_id: str
    capture_id: str
    document_entity_id: str
    entity_ids: list[str]
    claim_ids: list[str]
    relation_ids: list[str]
    indicators: list[dict[str, str]]
    result_code: str


class DeterministicIdentifierExtractor:
    """Extract machine-checkable public identifiers without inventing attribution.

    New identifiers are connected to the captured document using MENTIONED_IN.
    The extractor deliberately does not connect an e-mail, domain, phone or
    wallet directly to a seed person/company merely because both occur in the
    same document. Such attribution requires a separate reviewed relation.
    """

    version = "identifier-extractor/0.1.0"

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store

    def extract_capture(
        self,
        case_id: str,
        *,
        source_id: str,
        capture_id: str,
        query_plan_id: str | None = None,
        job_id: str | None = None,
    ) -> ExtractionResult:
        source = self.store.get_object(case_id, "source", source_id)
        capture = self.store.get_object(case_id, "capture", capture_id)
        if capture["source_id"] != source_id:
            raise ValueError("capture/source lineage mismatch")
        raw = self.store.read_capture_bytes(case_id, capture_id)
        text = raw.decode("utf-8", errors="replace")

        document = self.store.create_entity(
            case_id,
            entity_type="DOCUMENT",
            display_name=source["title"],
            source_ids=[source_id],
            identifiers=[
                {
                    "type": "CAPTURE_ID",
                    "value": capture_id,
                    "masked": False,
                    "source_ids": [source_id],
                }
            ],
            attributes={
                "capture_id": capture_id,
                "capture_sha256": capture["sha256"],
                "source_url": source["url"],
                "mime_type": capture["mime_type"],
            },
            access_class=capture["access_class"],
            status="CONFIRMED",
        )

        indicators = self._collect_indicators(text)
        entity_ids: list[str] = [document["entity_id"]]
        claim_ids: list[str] = []
        relation_ids: list[str] = []

        for indicator in indicators:
            entity = self._find_or_create_indicator_entity(case_id, source, capture, indicator)
            if entity["entity_id"] not in entity_ids:
                entity_ids.append(entity["entity_id"])
            statement = f"The preserved source capture contains {indicator['kind']} identifier {indicator['value']}."
            claim = self.store.create_claim(
                case_id,
                source_ids=[source_id],
                statement=statement,
                locator=f"capture:{capture_id}; regex:{indicator['kind']}",
                subject_entity_ids=[entity["entity_id"]],
                representation="STRUCTURED_EXTRACTION",
                predicate="MENTIONED_IN",
                object_entity_ids=[document["entity_id"]],
                access_class=entity["access_class"],
                limitations=[
                    "Text occurrence does not establish ownership, control, authorship or current validity.",
                    "Attribution requires independent evidence and human review.",
                ],
            )
            relation = self.store.create_relation(
                case_id,
                from_entity_id=entity["entity_id"],
                relation_type="MENTIONED_IN",
                to_entity_id=document["entity_id"],
                source_ids=[source_id],
                claim_ids=[claim["claim_id"]],
                evidence_grade="D_LEAD",
                status="CANDIDATE",
                not_implying=[
                    "Ownership or control by any person or organization mentioned in the same document.",
                    "Current validity or exclusive use of the identifier.",
                    "Wrongdoing or causal relationship.",
                ],
            )
            claim_ids.append(claim["claim_id"])
            relation_ids.append(relation["relation_id"])

        result_code = "FOUND" if indicators else "NO_HIT"
        self.store.append_journal(
            case_id,
            actor_id="deterministic-identifier-extractor",
            actor_type="AGENT",
            action_type="PARSE",
            stream="DIGITAL_FOOTPRINT",
            query_plan_id=query_plan_id,
            job_id=job_id,
            query_or_action=f"Extract identifiers from {capture_id}",
            source_or_transform_ids=[source_id],
            result_code=result_code,
            result_summary=(
                f"Extracted {len(indicators)} identifiers and created evidence-linked candidate objects."
                if indicators
                else "No supported identifier pattern was found in the captured text."
            ),
            new_entities=entity_ids,
            new_relations=relation_ids,
            new_claims=claim_ids,
            next_pivots=["Review attribution before creating direct entity-to-identifier relations"] if indicators else [],
            access_class=strictest_access_class(source["access_class"], capture["access_class"]),
            actor_version=self.version,
        )
        return ExtractionResult(
            source_id=source_id,
            capture_id=capture_id,
            document_entity_id=document["entity_id"],
            entity_ids=entity_ids,
            claim_ids=claim_ids,
            relation_ids=relation_ids,
            indicators=indicators,
            result_code=result_code,
        )

    @staticmethod
    def _collect_indicators(text: str) -> list[dict[str, str]]:
        found: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()

        def add(kind: str, value: str) -> None:
            value = value.strip().rstrip(".,;:")
            key = (kind, value.casefold())
            if value and key not in seen:
                seen.add(key)
                found.append({"kind": kind, "value": value})

        for value in EMAIL_RE.findall(text):
            add("EMAIL", value.lower())
        for url in URL_RE.findall(text):
            host = (urlparse(url).hostname or "").lower()
            if host:
                add("DOMAIN", host)
            add("URL", url)
        for value in DOMAIN_RE.findall(text):
            add("DOMAIN", value.lower())
        for value in IPV4_RE.findall(text):
            try:
                ipaddress.ip_address(value)
            except ValueError:
                continue
            add("IPV4", value)
        for value in HANDLE_RE.findall(text):
            add("PUBLIC_HANDLE", f"@{value}")
        for value in PHONE_RE.findall(text):
            digits = re.sub(r"\D", "", value)
            if 10 <= len(digits) <= 15:
                add("PHONE", f"+{digits}" if value.strip().startswith("+") else digits)
        for value in ETH_RE.findall(text):
            add("WALLET_ETH", value)
        for value in TRON_RE.findall(text):
            add("WALLET_TRON", value)
        for value in BTC_RE.findall(text):
            add("WALLET_BTC", value)
        return found

    def _find_or_create_indicator_entity(
        self,
        case_id: str,
        source: dict[str, Any],
        capture: dict[str, Any],
        indicator: dict[str, str],
    ) -> dict[str, Any]:
        kind = indicator["kind"]
        value = indicator["value"]
        normalized = normalize_name(value)
        for entity in self.store.list_objects(case_id, "entity"):
            for identifier in entity.get("identifiers", []):
                if identifier.get("type") == kind and normalize_name(str(identifier.get("value", ""))) == normalized:
                    return entity

        if kind == "DOMAIN":
            entity_type = "DOMAIN"
            access_class = source["access_class"]
        elif kind in {"EMAIL", "PHONE", "PUBLIC_HANDLE"}:
            entity_type = "ACCOUNT"
            access_class = strictest_access_class(source["access_class"], "PUBLIC_WITH_PERSONAL_DATA")
        else:
            entity_type = "ASSET"
            access_class = source["access_class"]
        return self.store.create_entity(
            case_id,
            entity_type=entity_type,
            display_name=value,
            source_ids=[source["source_id"]],
            identifiers=[
                {
                    "type": kind,
                    "value": value,
                    "masked": False,
                    "source_ids": [source["source_id"]],
                }
            ],
            attributes={
                "indicator_kind": kind,
                "capture_ids": [capture["capture_id"]],
                "automated_extraction": True,
                "attribution_status": "UNRESOLVED",
            },
            access_class=access_class,
            status="CANDIDATE",
        )
