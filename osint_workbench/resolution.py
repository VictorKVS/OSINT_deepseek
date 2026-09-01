from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from .canonical import normalize_name, sha256_json, utc_now_iso
from .store import WorkbenchStore

_GRADE_SCORE = {
    "A_CONFIRMED": 1.0,
    "B_HIGHLY_PROBABLE": 0.8,
    "C_ANALYTICAL_HYPOTHESIS": 0.45,
    "D_LEAD": 0.2,
}


class ExplainableEntityResolver:
    """Create a reviewable entity-match proposal; never merge automatically."""

    version = "entity-resolver/0.1.0"
    ruleset_hash = sha256_json(
        {
            "version": version,
            "weights": {
                "exact_identifier": 0.45,
                "name_similarity": 0.25,
                "address_overlap": 0.15,
                "source_quality": 0.15,
            },
            "automatic_merge": False,
        }
    )

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store

    def compare(
        self,
        case_id: str,
        entity_a_id: str,
        entity_b_id: str,
        *,
        query_plan_id: str | None = None,
        job_id: str | None = None,
    ) -> dict[str, Any]:
        if entity_a_id == entity_b_id:
            raise ValueError("entity comparison requires two distinct records")
        a = self.store.get_object(case_id, "entity", entity_a_id)
        b = self.store.get_object(case_id, "entity", entity_b_id)

        exact_identifier, identifier_support, identifier_conflicts = self._identifier_feature(a, b)
        name_similarity = self._name_similarity(a, b)
        address_overlap = self._address_overlap(a, b)
        source_quality = self._source_quality(case_id, a, b)
        temporal_consistency = self._temporal_consistency(a, b)

        weighted: list[tuple[float, float]] = []
        for value, weight in (
            (exact_identifier, 0.45),
            (name_similarity, 0.25),
            (address_overlap, 0.15),
            (source_quality, 0.15),
        ):
            if value is not None:
                weighted.append((value, weight))
        probability = sum(value * weight for value, weight in weighted) / sum(weight for _, weight in weighted)
        if exact_identifier != 1.0:
            probability = min(probability, 0.95)
        probability = round(max(0.0, min(1.0, probability)), 4)

        supporting: list[dict[str, Any]] = []
        if identifier_support:
            supporting.append(
                {
                    "feature": "exact_identifier",
                    "description": f"Shared exact identifier(s): {', '.join(identifier_support)}",
                    "source_ids": sorted(set(a["source_ids"] + b["source_ids"])),
                }
            )
        if name_similarity >= 0.85:
            supporting.append(
                {
                    "feature": "name_similarity",
                    "description": f"Normalized name similarity is {name_similarity:.3f}.",
                    "source_ids": sorted(set(a["source_ids"] + b["source_ids"])),
                }
            )
        if address_overlap == 1.0:
            supporting.append(
                {
                    "feature": "address_overlap",
                    "description": "At least one normalized address value overlaps.",
                    "source_ids": sorted(set(a["source_ids"] + b["source_ids"])),
                }
            )

        contradicting: list[dict[str, Any]] = []
        if a["entity_type"] != b["entity_type"]:
            contradicting.append(
                {
                    "feature": "entity_type_conflict",
                    "description": f"Entity types differ: {a['entity_type']} versus {b['entity_type']}.",
                    "source_ids": sorted(set(a["source_ids"] + b["source_ids"])),
                }
            )
        for conflict in identifier_conflicts:
            contradicting.append(
                {
                    "feature": "identifier_conflict",
                    "description": conflict,
                    "source_ids": sorted(set(a["source_ids"] + b["source_ids"])),
                }
            )
        if name_similarity < 0.5:
            contradicting.append(
                {
                    "feature": "low_name_similarity",
                    "description": f"Normalized name similarity is only {name_similarity:.3f}.",
                    "source_ids": sorted(set(a["source_ids"] + b["source_ids"])),
                }
            )
        # The schema and policy require an explicit reason why automation is not decisive.
        contradicting.append(
            {
                "feature": "identity_not_proven",
                "description": "Heuristic similarity is not decisive evidence of identity; no automatic merge is permitted.",
                "source_ids": [],
            }
        )

        if probability >= 0.8 and not identifier_conflicts and a["entity_type"] == b["entity_type"]:
            status = "PROBABLE_MATCH"
        elif probability < 0.35 or identifier_conflicts or a["entity_type"] != b["entity_type"]:
            status = "NEEDS_REVIEW"
        else:
            status = "CANDIDATE"

        missing = [
            "Independent authoritative identifier linking both records.",
            "Human review of source scope, dates and namesake risk.",
        ]
        if exact_identifier is None:
            missing.append("Comparable stable identifier such as registry number or verified account ID.")
        if address_overlap is None:
            missing.append("Comparable address or location evidence.")

        entity_match_id = self.store._allocate_id(case_id, "EMATCH")
        payload = {
            "schema_version": "father-osint.entity-match.v0.1",
            "entity_match_id": entity_match_id,
            "case_id": case_id,
            "entity_a_id": entity_a_id,
            "entity_b_id": entity_b_id,
            "status": status,
            "same_entity_probability": probability,
            "features": {
                "exact_identifier": exact_identifier,
                "name_similarity": round(name_similarity, 4),
                "address_overlap": address_overlap,
                "temporal_consistency": temporal_consistency,
                "source_quality": source_quality,
            },
            "supporting_features": supporting,
            "contradicting_features": contradicting,
            "missing_decisive_evidence": missing,
            "method": {
                "engine": "deterministic-explainable-resolver",
                "version": self.version,
                "ruleset_or_model_hash": self.ruleset_hash,
            },
            "human_review": {
                "required": True,
                "status": "PENDING",
                "reviewer_role": None,
                "reviewed_at_utc": None,
                "decision_note": "No automatic merge; analyst must confirm SAME or DISTINCT.",
            },
            "automatic_merge_performed": False,
            "created_at_utc": utc_now_iso(),
            "synthetic": self.store.get_case(case_id)["synthetic"],
        }
        self.store.save_object(case_id, "entity_match", payload)
        self.store.append_journal(
            case_id,
            actor_id="explainable-entity-resolver",
            actor_type="AGENT",
            action_type="RESOLVE_ENTITY",
            stream="ENTITY_REGISTRY",
            query_plan_id=query_plan_id,
            job_id=job_id,
            query_or_action=f"Compare {entity_a_id} with {entity_b_id}",
            result_code="FOUND",
            result_summary=f"Created {status} proposal with score {probability}; automatic merge=false.",
            new_entities=[],
            confidence_changes=[
                {
                    "subject_ref": entity_match_id,
                    "from": None,
                    "to": probability,
                    "reason": "Deterministic feature comparison; not a calibrated truth probability.",
                    "source_ids": sorted(set(a["source_ids"] + b["source_ids"])),
                }
            ],
            next_pivots=missing,
            access_class=self.store.get_case(case_id)["access_class"],
            actor_version=self.version,
        )
        return payload

    @staticmethod
    def _all_names(entity: dict[str, Any]) -> list[str]:
        return [entity["display_name"], *entity.get("aliases", [])]

    def _name_similarity(self, a: dict[str, Any], b: dict[str, Any]) -> float:
        values = [
            SequenceMatcher(None, normalize_name(left), normalize_name(right)).ratio()
            for left in self._all_names(a)
            for right in self._all_names(b)
            if normalize_name(left) and normalize_name(right)
        ]
        return max(values) if values else 0.0

    @staticmethod
    def _identifier_feature(a: dict[str, Any], b: dict[str, Any]) -> tuple[float | None, list[str], list[str]]:
        by_type_a: dict[str, set[str]] = {}
        by_type_b: dict[str, set[str]] = {}
        for entity, target in ((a, by_type_a), (b, by_type_b)):
            for item in entity.get("identifiers", []):
                kind = str(item.get("type", "")).upper()
                value = normalize_name(str(item.get("value", "")))
                if kind and value:
                    target.setdefault(kind, set()).add(value)
        comparable = sorted(set(by_type_a) & set(by_type_b))
        if not comparable:
            return None, [], []
        shared: list[str] = []
        conflicts: list[str] = []
        for kind in comparable:
            overlap = by_type_a[kind] & by_type_b[kind]
            if overlap:
                shared.extend(f"{kind}:{value}" for value in sorted(overlap))
            elif kind in {"REGISTRY_ID", "INN", "VAT", "EORI", "PASSPORT", "CAPTURE_ID"}:
                conflicts.append(f"Stable identifier {kind} has different values.")
        if shared:
            return 1.0, shared, conflicts
        return 0.0, [], conflicts

    @staticmethod
    def _address_overlap(a: dict[str, Any], b: dict[str, Any]) -> float | None:
        def values(entity: dict[str, Any]) -> set[str]:
            result: set[str] = set()
            attributes = entity.get("attributes", {})
            for key in ("address", "registered_address", "location"):
                value = attributes.get(key)
                if isinstance(value, str) and value.strip():
                    result.add(normalize_name(value))
            for item in entity.get("identifiers", []):
                if str(item.get("type", "")).upper() in {"ADDRESS", "REGISTERED_ADDRESS"}:
                    result.add(normalize_name(str(item.get("value", ""))))
            return {value for value in result if value}
        left, right = values(a), values(b)
        if not left or not right:
            return None
        return 1.0 if left & right else 0.0

    @staticmethod
    def _temporal_consistency(a: dict[str, Any], b: dict[str, Any]) -> float | None:
        left = a.get("attributes", {}).get("valid_period")
        right = b.get("attributes", {}).get("valid_period")
        if not isinstance(left, dict) or not isinstance(right, dict):
            return None
        # MVP records that periods are comparable; detailed interval arithmetic is a later increment.
        return 0.5

    def _source_quality(self, case_id: str, a: dict[str, Any], b: dict[str, Any]) -> float | None:
        scores: list[float] = []
        for source_id in sorted(set(a["source_ids"] + b["source_ids"])):
            source = self.store.get_object(case_id, "source", source_id)
            scores.append(_GRADE_SCORE.get(source.get("reliability_grade", "D_LEAD"), 0.2))
        return round(sum(scores) / len(scores), 4) if scores else None
