from __future__ import annotations

from typing import Any, Iterable

from .canonical import sha256_bytes, sha256_json, utc_now_iso
from .policy import authorize_transform
from .store import WorkbenchStore


class PassiveAcquisitionOrchestrator:
    """Govern and record passive/manual acquisition jobs.

    This increment intentionally does not execute arbitrary commands or network
    collectors. It records approved passive work, preserved raw output and the
    normalized object lineage. Real adapters can later implement the same
    contract behind isolated workers.
    """

    version = "passive-acquisition-orchestrator/0.1.0"

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store

    def register_transform(
        self,
        case_id: str,
        *,
        name: str,
        input_entity_types: Iterable[str],
        output_object_types: Iterable[str],
        source_id: str | None = None,
        execution_profile: str = "MANUAL_EXTERNAL",
        safety_class: str = "PASSIVE_PUBLIC",
        network_policy: str = "INTERNET_READ_ONLY",
        evidence_capture_mode: str = "FULL_CAPTURE",
        parser_version: str = "manual-normalizer/0.1.0",
        required_credentials: str = "NONE",
        max_requests: int = 10,
        per_seconds: int = 60,
        concurrency: int = 1,
        terms_note: str = "Use only lawfully accessible sources and respect source-specific terms.",
        enabled: bool = True,
    ) -> dict[str, Any]:
        case = self.store.get_case(case_id)
        if source_id is not None:
            self.store.get_object(case_id, "source", source_id)
        decision = authorize_transform(
            case_active_actions_allowed=case["scope"]["active_actions_allowed"],
            safety_class=safety_class,
            network_policy=network_policy,
            access_class=case["access_class"],
        )
        transform_id = self.store._allocate_id(case_id, "TRN")
        payload = {
            "schema_version": "father-osint.transform.v0.1",
            "transform_id": transform_id,
            "name": name,
            "version": "0.1.0",
            "input_entity_types": list(dict.fromkeys(item.upper() for item in input_entity_types)),
            "output_object_types": list(dict.fromkeys(item.upper() for item in output_object_types)),
            "source_id": source_id,
            "required_credentials": required_credentials.upper(),
            "legal_scope": {
                "allowed_case_types": [case["case_type"]],
                "allowed_access_classes": case["scope"]["allowed_source_classes"],
                "passive_only": safety_class.upper() == "PASSIVE_PUBLIC",
                "terms_note": terms_note,
            },
            "rate_limit": {
                "max_requests": max(0, int(max_requests)),
                "per_seconds": max(1, int(per_seconds)),
                "concurrency": max(1, int(concurrency)),
            },
            "parser_version": parser_version,
            "evidence_capture_mode": evidence_capture_mode.upper(),
            "execution_profile": execution_profile.upper(),
            "safety_class": safety_class.upper(),
            "network_policy": network_policy.upper(),
            "tool_adapter_id": None,
            "output_contract": "father-osint.entities-relations-sources.v0.1",
            "requires_human_approval": decision.human_approval_required,
            "enabled": bool(enabled and decision.decision != "DENY"),
            "health": "HEALTHY" if enabled and decision.decision != "DENY" else "DISABLED",
            "version_probe": None,
            "synthetic": case["synthetic"],
        }
        self.store.save_object(case_id, "transform", payload)
        return payload

    def record_completed_job(
        self,
        case_id: str,
        *,
        query_plan_id: str,
        pivot_id: str,
        stream: str,
        input_type: str,
        input_reference: str,
        raw_output: bytes,
        normalized_output: dict[str, Any],
        result_code: str,
        summary: str,
        source_id: str | None = None,
        transform_id: str | None = None,
        execution_profile: str = "MANUAL_EXTERNAL",
        safety_class: str = "PASSIVE_PUBLIC",
        network_policy: str = "INTERNET_READ_ONLY",
        source_ids: Iterable[str] = (),
        capture_ids: Iterable[str] = (),
        entity_ids: Iterable[str] = (),
        relation_ids: Iterable[str] = (),
        claim_ids: Iterable[str] = (),
        finding_ids: Iterable[str] = (),
        research_gap_ids: Iterable[str] = (),
        timeout_seconds: int = 600,
        attempt: int = 1,
        human_approval_obtained: bool = False,
        approved_by: str | None = None,
        parser_name: str = "manual-normalizer",
        parser_version: str = "0.1.0",
        error_code: str | None = None,
    ) -> dict[str, Any]:
        case = self.store.get_case(case_id)
        plan = self.store.get_object(case_id, "query_plan", query_plan_id)
        pivot = next((item for item in plan["pivots"] if item["pivot_id"] == pivot_id), None)
        if pivot is None:
            raise ValueError(f"pivot not found in query plan: {pivot_id}")
        if pivot["stream"] != stream.upper():
            raise ValueError("job stream does not match query-plan pivot")
        if source_id is not None:
            self.store.get_object(case_id, "source", source_id)
        if transform_id is not None:
            transform = self.store.get_object(case_id, "transform", transform_id)
            safety_class = transform["safety_class"]
            network_policy = transform["network_policy"]
            execution_profile = transform["execution_profile"]
        decision = authorize_transform(
            case_active_actions_allowed=case["scope"]["active_actions_allowed"],
            safety_class=safety_class,
            network_policy=network_policy,
            access_class=pivot["access_class"],
            human_approval_obtained=human_approval_obtained,
        )
        if decision.decision == "DENY":
            raise PermissionError(f"job denied: {', '.join(decision.reason_codes)}")
        if decision.decision == "REQUIRE_APPROVAL":
            raise PermissionError(f"job approval required: {', '.join(decision.reason_codes)}")

        now = utc_now_iso()
        raw_hash = sha256_bytes(raw_output)
        normalized_hash = sha256_json(normalized_output)
        manifest = {
            "case_id": case_id,
            "query_plan_id": query_plan_id,
            "pivot_id": pivot_id,
            "source_id": source_id,
            "transform_id": transform_id,
            "input_type": input_type.upper(),
            "input_reference": input_reference,
            "raw_output_hash": raw_hash,
            "normalized_output_hash": normalized_hash,
            "parser_name": parser_name,
            "parser_version": parser_version,
            "finished_at_utc": now,
        }
        job_id = self.store._allocate_id(case_id, "JOB")
        payload = {
            "schema_version": "father-osint.acquisition-job.v0.1",
            "job_id": job_id,
            "case_id": case_id,
            "query_plan_id": query_plan_id,
            "pivot_id": pivot_id,
            "stream": stream.upper(),
            "source_id": source_id,
            "transform_id": transform_id,
            "tool_adapter_id": None,
            "state": "REVIEWED",
            "execution_profile": execution_profile.upper(),
            "safety_class": safety_class.upper(),
            "authorization": {
                "case_scope_checked": True,
                "policy_decision": decision.decision,
                "human_approval_required": decision.human_approval_required,
                "human_approval_obtained": bool(human_approval_obtained),
                "approved_by": approved_by,
                "allowed_access_classes": case["scope"]["allowed_source_classes"],
            },
            "inputs": [
                {
                    "input_type": input_type.upper(),
                    "reference": input_reference,
                    "value_hash": sha256_bytes(input_reference.encode("utf-8")),
                }
            ],
            "schedule": {
                "queued_at_utc": now,
                "started_at_utc": now,
                "finished_at_utc": now,
                "timeout_seconds": max(1, int(timeout_seconds)),
                "attempt": max(1, int(attempt)),
            },
            "output": {
                "result_code": result_code.upper(),
                "summary": summary,
                "source_ids": list(dict.fromkeys(source_ids)),
                "capture_ids": list(dict.fromkeys(capture_ids)),
                "entity_ids": list(dict.fromkeys(entity_ids)),
                "relation_ids": list(dict.fromkeys(relation_ids)),
                "claim_ids": list(dict.fromkeys(claim_ids)),
                "finding_ids": list(dict.fromkeys(finding_ids)),
                "research_gap_ids": list(dict.fromkeys(research_gap_ids)),
                "error_code": error_code,
            },
            "parser": {
                "name": parser_name,
                "version": parser_version,
                "output_contract": "father-osint.entities-relations-sources.v0.1",
            },
            "raw_output_hash": raw_hash,
            "normalized_output_hash": normalized_hash,
            "run_manifest_hash": sha256_json(manifest),
            "synthetic": case["synthetic"],
        }
        self.store.save_object(case_id, "job", payload)
        self.store.append_journal(
            case_id,
            actor_id="passive-acquisition-orchestrator",
            actor_type="SYSTEM",
            action_type="COLLECT",
            stream=stream,
            query_plan_id=query_plan_id,
            job_id=job_id,
            query_or_action=pivot["query_or_action"],
            source_or_transform_ids=[item for item in (source_id, transform_id) if item],
            result_code=result_code,
            result_summary=summary,
            new_entities=entity_ids,
            new_relations=relation_ids,
            new_claims=claim_ids,
            new_findings=finding_ids,
            new_research_gaps=research_gap_ids,
            access_class=pivot["access_class"],
            actor_version=self.version,
        )
        return payload
