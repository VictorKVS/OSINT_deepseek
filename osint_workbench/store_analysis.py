from __future__ import annotations

from typing import Any, Iterable

from .canonical import sha256_json, utc_now_iso
from .policy import validate_access_class
from .store_base import (
    EVIDENCE_GRADES, GAP_PRIORITIES, GAP_STATES, JOURNAL_ACTIONS,
    JOURNAL_RESULTS, REPORT_EFFECTS, STREAMS, StoreError,
)


class AnalysisStoreMixin:
    def create_finding(
        self,
        case_id: str,
        *,
        classification: str,
        statement: str,
        evidence_grade: str,
        source_ids: Iterable[str],
        claim_ids: Iterable[str],
        entity_ids: Iterable[str],
        reasoning_summary: str,
        limitations: Iterable[str],
        approved_by_role: str,
        red_team_status: str = "PENDING",
        alternative_explanations: Iterable[str] = (),
        consensus_id: str | None = None,
        access_class: str = "PUBLIC",
    ) -> dict[str, Any]:
        classification = classification.upper()
        evidence_grade = evidence_grade.upper()
        if classification not in {"FACT", "INFERENCE", "HYPOTHESIS", "RISK", "DECISION"}:
            raise StoreError("unsupported finding classification")
        if evidence_grade not in EVIDENCE_GRADES:
            raise StoreError("unsupported evidence grade")
        red_team_status = red_team_status.upper()
        if red_team_status not in {"NOT_REQUIRED", "PENDING", "CHALLENGED", "PASSED", "REJECTED"}:
            raise StoreError("unsupported Red Team status")
        if len(statement.strip()) < 5 or len(reasoning_summary.strip()) < 5 or len(approved_by_role.strip()) < 3:
            raise StoreError("finding statement, reasoning or approver is too short")
        source_ids = list(dict.fromkeys(source_ids))
        claim_ids = list(dict.fromkeys(claim_ids))
        entity_ids = list(dict.fromkeys(entity_ids))
        if not source_ids or not claim_ids or not entity_ids:
            raise StoreError("finding requires source, claim and entity lineage")
        for source_id in source_ids:
            self.get_object(case_id, "source", source_id)
        for claim_id in claim_ids:
            self.get_object(case_id, "claim", claim_id)
        for entity_id in entity_ids:
            self.get_object(case_id, "entity", entity_id)
        finding_id = self._allocate_id(case_id, "FND")
        payload = {
            "schema_version": "father-osint.finding.v0.1",
            "finding_id": finding_id,
            "case_id": case_id,
            "classification": classification,
            "statement": statement.strip(),
            "evidence_grade": evidence_grade,
            "source_ids": source_ids,
            "claim_ids": claim_ids,
            "entity_ids": entity_ids,
            "consensus_id": consensus_id,
            "reasoning_summary": reasoning_summary.strip(),
            "alternative_explanations": list(alternative_explanations),
            "limitations": list(limitations),
            "red_team_status": red_team_status,
            "human_approved": True,
            "approved_by_role": approved_by_role.strip(),
            "approved_at_utc": utc_now_iso(),
            "access_class": validate_access_class(access_class),
        }
        return self.save_object(case_id, "finding", payload)

    def create_research_gap(
        self,
        case_id: str,
        *,
        subject_refs: Iterable[str],
        stream: str,
        question: str,
        why_matters: str,
        evidence_needed: Iterable[str],
        owner_role: str,
        priority: str = "P1",
        state: str = "NOT_CHECKED",
        planned_pivot_ids: Iterable[str] = (),
        blocking_reasons: Iterable[str] = (),
        report_effect: str = "LIMITS_REPORT",
    ) -> dict[str, Any]:
        stream = stream.upper()
        if stream not in STREAMS:
            raise StoreError(f"unsupported stream: {stream}")
        priority = priority.upper()
        state = state.upper()
        report_effect = report_effect.upper()
        if priority not in GAP_PRIORITIES or state not in GAP_STATES or report_effect not in REPORT_EFFECTS:
            raise StoreError("unsupported research-gap priority, state or report effect")
        if len(question.strip()) < 5 or len(why_matters.strip()) < 5 or len(owner_role.strip()) < 3:
            raise StoreError("research-gap question, rationale or owner is too short")
        evidence_items = list(evidence_needed)
        subjects = list(dict.fromkeys(subject_refs))
        if not evidence_items or not subjects:
            raise StoreError("research gap requires subject_refs and evidence_needed")
        research_gap_id = self._allocate_id(case_id, "GAP")
        payload = {
            "schema_version": "father-osint.research-gap.v0.1",
            "research_gap_id": research_gap_id,
            "case_id": case_id,
            "subject_refs": subjects,
            "stream": stream,
            "question": question.strip(),
            "why_matters": why_matters.strip(),
            "priority": priority,
            "state": state,
            "evidence_needed": evidence_items,
            "planned_pivot_ids": list(dict.fromkeys(planned_pivot_ids)),
            "blocking_reasons": list(blocking_reasons),
            "owner_role": owner_role.strip(),
            "opened_at_utc": utc_now_iso(),
            "resolved_at_utc": None,
            "resolved_by_finding_ids": [],
            "report_effect": report_effect,
            "synthetic": self.get_case(case_id)["synthetic"],
        }
        return self.save_object(case_id, "research_gap", payload)

    def append_journal(
        self,
        case_id: str,
        *,
        actor_id: str,
        actor_type: str,
        action_type: str,
        stream: str,
        query_or_action: str,
        result_code: str,
        result_summary: str,
        query_plan_id: str | None = None,
        job_id: str | None = None,
        source_or_transform_ids: Iterable[str] = (),
        new_entities: Iterable[str] = (),
        new_relations: Iterable[str] = (),
        new_claims: Iterable[str] = (),
        new_findings: Iterable[str] = (),
        new_research_gaps: Iterable[str] = (),
        confidence_changes: Iterable[dict[str, Any]] = (),
        next_pivots: Iterable[str] = (),
        access_class: str = "PUBLIC",
        actor_version: str = "0.1.0",
    ) -> dict[str, Any]:
        stream = stream.upper()
        if stream not in STREAMS:
            raise StoreError(f"unsupported stream: {stream}")
        actor_type = actor_type.upper()
        action_type = action_type.upper()
        result_code = result_code.upper()
        if actor_type not in {"HUMAN", "AGENT", "SYSTEM", "CONNECTOR", "RULE_ENGINE", "MODEL"}:
            raise StoreError(f"unsupported journal actor_type: {actor_type}")
        if action_type not in JOURNAL_ACTIONS or result_code not in JOURNAL_RESULTS:
            raise StoreError("unsupported journal action or result code")
        if not actor_id.strip() or len(query_or_action.strip()) < 2 or not result_summary.strip():
            raise StoreError("journal actor, action text and result summary are required")
        case_path = self.case_dir(case_id)
        journal_dir = case_path / self.OBJECT_DIRS["journal"]
        with self._lock:
            existing = [self._read_json(path) for path in sorted(journal_dir.glob("*.json"))]
            sequence = len(existing) + 1
            previous_hash = existing[-1]["entry_hash"] if existing else None
            journal_id = self._allocate_id(case_id, "JRN")
            payload = {
                "schema_version": "father-osint.search-journal.v0.1",
                "journal_id": journal_id,
                "case_id": case_id,
                "sequence": sequence,
                "timestamp_utc": utc_now_iso(),
                "actor": {"actor_id": actor_id, "actor_type": actor_type, "version": actor_version},
                "action_type": action_type,
                "stream": stream,
                "query_plan_id": query_plan_id,
                "job_id": job_id,
                "query_or_action": query_or_action,
                "source_or_transform_ids": list(dict.fromkeys(source_or_transform_ids)),
                "result_code": result_code,
                "result_summary": result_summary,
                "new_entities": list(dict.fromkeys(new_entities)),
                "new_relations": list(dict.fromkeys(new_relations)),
                "new_claims": list(dict.fromkeys(new_claims)),
                "new_findings": list(dict.fromkeys(new_findings)),
                "new_research_gaps": list(dict.fromkeys(new_research_gaps)),
                "confidence_changes": list(confidence_changes),
                "next_pivots": list(next_pivots),
                "access_class": validate_access_class(access_class),
                "previous_entry_hash": previous_hash,
                "entry_hash": "",
                "append_only": True,
                "synthetic": self.get_case(case_id)["synthetic"],
            }
            payload["entry_hash"] = sha256_json(payload, exclude_fields={"entry_hash"})
            path = journal_dir / f"{sequence:06d}_{journal_id}.json"
            self._atomic_write_json(path, payload, immutable=True)
        return payload

    def verify_journal(self, case_id: str) -> dict[str, Any]:
        entries = self.list_objects(case_id, "journal")
        failures: list[str] = []
        previous: str | None = None
        for expected_sequence, entry in enumerate(entries, start=1):
            if entry.get("sequence") != expected_sequence:
                failures.append(f"sequence {entry.get('sequence')} != {expected_sequence}")
            if entry.get("previous_entry_hash") != previous:
                failures.append(f"{entry.get('journal_id')}: previous hash mismatch")
            expected_hash = sha256_json(entry, exclude_fields={"entry_hash"})
            if entry.get("entry_hash") != expected_hash:
                failures.append(f"{entry.get('journal_id')}: entry hash mismatch")
            previous = entry.get("entry_hash")
        return {
            "case_id": case_id,
            "entries": len(entries),
            "valid": not failures,
            "failures": failures,
            "head_hash": previous,
        }

    def find_by_ref(self, case_id: str, object_id: str) -> tuple[str, dict[str, Any]]:
        """Resolve an object ID inside one case without crossing case boundaries."""
        prefix_map = {
            "QPLAN-": "query_plan",
            "SRC-": "source",
            "CAP-": "capture",
            "ENT-": "entity",
            "CLM-": "claim",
            "REL-": "relation",
            "FND-": "finding",
            "GAP-": "research_gap",
            "EMATCH-": "entity_match",
            "COV-": "coverage",
            "GVIEW-": "graph",
            "TRN-": "transform",
            "JOB-": "job",
            "ARUN-": "analysis_run",
            "OPN-": "analysis_opinion",
            "CNS-": "consensus",
            "MON-": "monitor_snapshot",
            "JRN-": "journal",
        }
        for prefix, kind in prefix_map.items():
            if object_id.startswith(prefix):
                return kind, self.get_object(case_id, kind, object_id)
        raise StoreError(f"unsupported object reference: {object_id}")

    def summary(self, case_id: str) -> dict[str, Any]:
        counts = {kind: len(self.list_objects(case_id, kind)) for kind in self.OBJECT_DIRS}
        journal = self.verify_journal(case_id)
        gaps = self.list_objects(case_id, "research_gap")
        return {
            "case": self.get_case(case_id),
            "counts": counts,
            "open_gap_ids": [item["research_gap_id"] for item in gaps if item["state"] not in {"RESOLVED", "WAIVED"}],
            "journal_integrity": journal,
        }
