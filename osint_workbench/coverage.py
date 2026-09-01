from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from .canonical import utc_now_iso
from .store import WorkbenchStore


class EvidenceCoverageAssessor:
    version = "evidence-coverage/0.1.0"

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store

    def assess(self, case_id: str, finding_id: str) -> dict[str, Any]:
        finding = self.store.get_object(case_id, "finding", finding_id)
        sources = [self.store.get_object(case_id, "source", item) for item in finding["source_ids"]]
        claims = [self.store.get_object(case_id, "claim", item) for item in finding["claim_ids"]]
        entities = [self.store.get_object(case_id, "entity", item) for item in finding["entity_ids"]]
        relations = [
            item for item in self.store.list_objects(case_id, "relation")
            if set(item["claim_ids"]) & set(finding["claim_ids"])
        ]
        captures = [
            item for item in self.store.list_objects(case_id, "capture")
            if item["source_id"] in finding["source_ids"]
        ]
        gaps = [
            item for item in self.store.list_objects(case_id, "research_gap")
            if finding_id in item.get("subject_refs", []) or set(finding["entity_ids"]) & set(item.get("subject_refs", []))
        ]

        def dimension(name: str, status: str, refs: list[str], gap_ids: list[str], note: str, weight: float = 1.0) -> dict[str, Any]:
            return {
                "dimension": name,
                "status": status,
                "weight": weight,
                "evidence_refs": list(dict.fromkeys(refs)),
                "research_gap_ids": list(dict.fromkeys(gap_ids)),
                "note": note,
            }

        identity_status = "COVERED" if entities and all(item["status"] in {"CONFIRMED", "REVIEWED"} for item in entities) else "PARTIAL"
        identity_refs = [item["entity_id"] for item in entities]

        authoritative = [item for item in sources if item["primary_level"] == "PRIMARY" and item["reliability_grade"] == "A_CONFIRMED"]
        source_authority_status = "COVERED" if authoritative else "PARTIAL" if sources else "MISSING"

        domains = {(urlparse(item["url"]).hostname or item["publisher"]).casefold() for item in sources}
        source_independence_status = "COVERED" if len(domains) >= 2 else "PARTIAL" if domains else "MISSING"

        direct_claims = [item for item in claims if item["representation"] in {"EXACT_QUOTE", "STRUCTURED_EXTRACTION"}]
        directness_status = "COVERED" if direct_claims and authoritative else "PARTIAL" if claims else "MISSING"

        corroboration_status = "COVERED" if len(domains) >= 2 else "PARTIAL" if sources else "MISSING"

        temporal_refs = [item["relation_id"] for item in relations if item.get("valid_from") or item.get("valid_to")]
        temporal_status = "COVERED" if temporal_refs else "PARTIAL" if relations else "NOT_APPLICABLE"

        contradiction_gap_ids = [item["research_gap_id"] for item in gaps if item["state"] == "CONFLICT"]
        disputed_relations = [item["relation_id"] for item in relations if item["status"] == "DISPUTED"]
        contradictions_status = "CONFLICT" if contradiction_gap_ids or disputed_relations else "COVERED"

        access_blocked = any(item["access_class"] == "PROHIBITED" for item in [*sources, *claims, *entities, finding])
        access_status = "CONFLICT" if access_blocked else "COVERED"

        integrity_failures: list[str] = []
        for capture in captures:
            if not capture.get("integrity_verified"):
                integrity_failures.append(capture["capture_id"])
                continue
            try:
                self.store.read_capture_bytes(case_id, capture["capture_id"])
            except Exception:
                integrity_failures.append(capture["capture_id"])
        capture_status = "CONFLICT" if integrity_failures else "COVERED" if captures else "MISSING"

        linked_gap_ids = [item["research_gap_id"] for item in gaps if item["state"] not in {"RESOLVED", "WAIVED"}]
        dimensions = [
            dimension("IDENTITY_RESOLUTION", identity_status, identity_refs, linked_gap_ids, "Entity status and match review determine identity coverage."),
            dimension("SOURCE_AUTHORITY", source_authority_status, [item["source_id"] for item in sources], linked_gap_ids, "Primary A-grade sources provide the strongest authority signal."),
            dimension("SOURCE_INDEPENDENCE", source_independence_status, [item["source_id"] for item in sources], linked_gap_ids, "Distinct publishers/domains are a proxy only; editorial independence still requires review."),
            dimension("DIRECTNESS", directness_status, [item["claim_id"] for item in direct_claims], linked_gap_ids, "Directness combines representation type with primary-source status."),
            dimension("CORROBORATION", corroboration_status, [item["source_id"] for item in sources], linked_gap_ids, "Corroboration requires more than repeated copies of the same source."),
            dimension("TEMPORAL_ALIGNMENT", temporal_status, temporal_refs, linked_gap_ids, "Event, effective, publication and collection dates should remain distinct."),
            dimension("CONTRADICTIONS", contradictions_status, disputed_relations, contradiction_gap_ids, "Open conflicts and disputed relations limit report readiness."),
            dimension("ACCESS_LEGALITY", access_status, [item["source_id"] for item in sources], linked_gap_ids, "No PROHIBITED object may support a report."),
            dimension("CAPTURE_INTEGRITY", capture_status, [item["capture_id"] for item in captures], linked_gap_ids, "Content-addressed captures are re-hashed before assessment."),
        ]

        # The contract stores GAP object references here; explanatory text stays
        # in dimension notes and the report, never masquerading as an object ID.
        decisive_gaps: list[str] = list(dict.fromkeys(linked_gap_ids))

        if access_blocked or integrity_failures:
            overall_grade = "BLOCKED"
        elif not sources or not claims or not captures:
            overall_grade = "INSUFFICIENT"
        elif source_authority_status == "COVERED" and directness_status == "COVERED" and contradictions_status == "COVERED":
            overall_grade = "STRONG" if identity_status == "COVERED" else "ADEQUATE"
        elif capture_status == "COVERED":
            overall_grade = "ADEQUATE"
        else:
            overall_grade = "WEAK"

        if any(item["report_effect"] == "BLOCKS_REPORT" and item["state"] not in {"RESOLVED", "WAIVED"} for item in gaps):
            report_readiness = "NOT_READY"
        elif overall_grade in {"BLOCKED", "INSUFFICIENT", "WEAK"}:
            report_readiness = "NOT_READY"
        elif any(item["report_effect"] == "LIMITS_REPORT" and item["state"] not in {"RESOLVED", "WAIVED"} for item in gaps):
            report_readiness = "READY_WITH_LIMITATION"
        else:
            report_readiness = "READY"

        coverage_id = self.store._allocate_id(case_id, "COV")
        payload = {
            "schema_version": "father-osint.coverage.v0.1",
            "coverage_id": coverage_id,
            "case_id": case_id,
            "finding_id": finding_id,
            "evaluated_at_utc": utc_now_iso(),
            "policy_version": self.version,
            "dimensions": dimensions,
            "overall_grade": overall_grade,
            "report_readiness": report_readiness,
            "decisive_gaps": list(dict.fromkeys(decisive_gaps)),
            "explanation": "Coverage is decomposed by evidence dimension; no opaque confidence percentage is used.",
            "human_review": {
                "status": "APPROVED" if finding["human_approved"] else "PENDING",
                "reviewer_role": finding.get("approved_by_role"),
                "reviewed_at_utc": finding.get("approved_at_utc"),
            },
            "synthetic": self.store.get_case(case_id)["synthetic"],
        }
        self.store.save_object(case_id, "coverage", payload)
        self.store.append_journal(
            case_id,
            actor_id="evidence-coverage-assessor",
            actor_type="AGENT",
            action_type="ANALYZE",
            stream="RED_TEAM_SOURCE_QUALITY",
            query_or_action=f"Assess evidence coverage for {finding_id}",
            result_code="REVIEWED",
            result_summary=f"Coverage={overall_grade}; report_readiness={report_readiness}.",
            new_findings=[],
            confidence_changes=[
                {
                    "subject_ref": finding_id,
                    "from": None,
                    "to": {"STRONG": 1.0, "ADEQUATE": 0.75, "WEAK": 0.4, "INSUFFICIENT": 0.2, "BLOCKED": 0.0}[overall_grade],
                    "reason": "Normalized coverage indicator for change tracking; not a truth probability.",
                    "source_ids": list(finding["source_ids"]),
                }
            ],
            next_pivots=payload["decisive_gaps"],
            access_class=finding["access_class"],
            actor_version=self.version,
        )
        return payload
