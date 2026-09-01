from __future__ import annotations

from typing import Any

from .canonical import sha256_json, utc_now_iso
from .store import WorkbenchStore


class CaseMonitor:
    """Create deterministic case snapshots and explain changes over time.

    This monitor does not fetch external data itself. Collectors update the case;
    the monitor records which evidence, entities, relations, findings and gaps
    changed between reviewed snapshots.
    """

    version = "case-monitor/0.1.0"

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store

    def snapshot(self, case_id: str, *, label: str = "manual") -> dict[str, Any]:
        previous_items = self.store.list_objects(case_id, "monitor_snapshot")
        previous = previous_items[-1] if previous_items else None
        journal = self.store.verify_journal(case_id)
        captures = self.store.list_objects(case_id, "capture")
        current_state = {
            "sources": {
                item["source_id"]: {
                    "status": item.get("status"),
                    "accessed_at_utc": item.get("accessed_at_utc"),
                    "reliability_grade": item.get("reliability_grade"),
                }
                for item in self.store.list_objects(case_id, "source")
            },
            "captures": {
                item["capture_id"]: {
                    "source_id": item["source_id"],
                    "sha256": item["sha256"],
                    "integrity_verified": item.get("integrity_verified"),
                }
                for item in captures
            },
            "entities": {
                item["entity_id"]: {"status": item["status"], "type": item["entity_type"]}
                for item in self.store.list_objects(case_id, "entity")
            },
            "relations": {
                item["relation_id"]: {"status": item["status"], "type": item["relation_type"]}
                for item in self.store.list_objects(case_id, "relation")
            },
            "findings": {
                item["finding_id"]: {
                    "classification": item["classification"],
                    "evidence_grade": item["evidence_grade"],
                    "red_team_status": item["red_team_status"],
                }
                for item in self.store.list_objects(case_id, "finding")
            },
            "research_gaps": {
                item["research_gap_id"]: {
                    "state": item["state"],
                    "priority": item["priority"],
                    "report_effect": item["report_effect"],
                }
                for item in self.store.list_objects(case_id, "research_gap")
            },
            "journal_head_hash": journal["head_hash"],
        }
        prior_state = (previous or {}).get("state", {})
        changes = self._diff(prior_state, current_state)
        snapshot_id = self.store._allocate_id(case_id, "MON")
        payload = {
            "schema_version": "father-osint.monitor-snapshot.v0.1",
            "snapshot_id": snapshot_id,
            "case_id": case_id,
            "label": label,
            "created_at_utc": utc_now_iso(),
            "previous_snapshot_id": previous.get("snapshot_id") if previous else None,
            "state": current_state,
            "changes": changes,
            "state_sha256": sha256_json(current_state),
            "journal_integrity_valid": journal["valid"],
            "synthetic": self.store.get_case(case_id)["synthetic"],
        }
        self.store.save_object(case_id, "monitor_snapshot", payload)
        change_count = sum(len(value) for value in changes.values())
        self.store.append_journal(
            case_id,
            actor_id="case-monitor",
            actor_type="AGENT",
            action_type="MONITOR",
            stream="RED_TEAM_SOURCE_QUALITY",
            query_or_action=f"Create case snapshot: {label}",
            result_code="FOUND" if change_count else "NO_HIT",
            result_summary=f"Snapshot {snapshot_id}: {change_count} material change item(s); journal integrity={journal['valid']}.",
            next_pivots=["Review changed findings and blocking gaps"] if change_count else [],
            access_class=self.store.get_case(case_id)["access_class"],
            actor_version=self.version,
        )
        return payload

    @staticmethod
    def _diff(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {
            "added": [],
            "removed": [],
            "changed": [],
        }
        sections = ("sources", "captures", "entities", "relations", "findings", "research_gaps")
        for section in sections:
            old = previous.get(section, {}) if isinstance(previous.get(section, {}), dict) else {}
            new = current.get(section, {}) if isinstance(current.get(section, {}), dict) else {}
            for key in sorted(set(new) - set(old)):
                result["added"].append(f"{section}:{key}")
            for key in sorted(set(old) - set(new)):
                result["removed"].append(f"{section}:{key}")
            for key in sorted(set(old) & set(new)):
                if old[key] != new[key]:
                    result["changed"].append(f"{section}:{key}")
        if previous and previous.get("journal_head_hash") != current.get("journal_head_hash"):
            result["changed"].append("journal:head_hash")
        return result
