from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.knowledge_factory import AuditEvent, DocumentRecord, DocumentVersion, PipelineStage, Role, StageState
from father_osint.knowledge_factory_store import KnowledgeFactoryStore

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REPORT_ROOT = REPO_ROOT / "reports" / "pdn_live"
PACKET = REPORT_ROOT / "D14_REVIEW_PACKET.json"
DECISIONS = REPORT_ROOT / "D14_DECISIONS.jsonl"
RESULT_JSON = REPORT_ROOT / "D14_REVIEW_RESULT.json"
RESULT_MD = REPORT_ROOT / "D14_REVIEW_RESULT.md"
PROMOTION_REQUEST = REPORT_ROOT / "D15_PROMOTION_REQUEST.json"
TARGETS = (
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _packet_hash(packet: dict[str, Any]) -> str:
    payload = dict(packet)
    expected = str(payload.pop("packet_sha256", ""))
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    actual = _sha256_bytes(raw)
    if actual != expected:
        raise ValueError("D14 packet SHA-256 does not match packet content")
    return actual


def _document(payload: dict[str, Any]) -> DocumentRecord:
    return DocumentRecord(
        title=str(payload["title"]),
        document_type=str(payload["document_type"]),
        workspace_id=str(payload.get("workspace_id", "default")),
        owner=str(payload.get("owner", "system")),
        jurisdiction=payload.get("jurisdiction"),
        language=str(payload.get("language", "ru")),
        topic_tags=list(payload.get("topic_tags", [])),
        versions=[DocumentVersion(**item) for item in payload.get("versions", [])],
        current_version_id=payload.get("current_version_id"),
        stage_states=dict(payload.get("stage_states", {})),
        document_id=str(payload["document_id"]),
        created_at=str(payload["created_at"]),
        updated_at=str(payload["updated_at"]),
    )


def main() -> int:
    if not PACKET.is_file() or not DECISIONS.is_file():
        print("D14_REVIEW_INPUT_MISSING: run RUN_PDN_KNOWLEDGE_FACTORY_AUTO.cmd first")
        return 2

    try:
        packet = _read_json(PACKET)
        packet_sha256 = _packet_hash(packet)
        decisions = _read_jsonl(DECISIONS)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"D14_REVIEW_INPUT_INVALID: {exc}")
        return 2

    items = {str(item["decision_id"]): item for item in packet.get("decision_items", [])}
    decision_by_id = {str(row.get("decision_id")): row for row in decisions}
    if not items or set(decision_by_id) != set(items):
        print("D14_DECISION_SET_MISMATCH")
        return 2
    if len(decisions) != len(decision_by_id):
        print("D14_DUPLICATE_DECISION_IDS")
        return 2

    unresolved: list[str] = []
    invalid: list[str] = []
    applied: list[dict[str, Any]] = []
    reviewers: set[str] = set()
    for decision_id, item in items.items():
        row = decision_by_id[decision_id]
        if row.get("packet_sha256") != packet_sha256:
            invalid.append(f"PACKET_HASH_MISMATCH:{decision_id}")
            continue
        decision = str(row.get("decision", "")).strip().upper()
        allowed = {str(value).upper() for value in item.get("allowed_decisions", [])}
        if decision in {"", "PENDING"}:
            unresolved.append(decision_id)
            continue
        if decision not in allowed:
            invalid.append(f"INVALID_DECISION:{decision_id}:{decision}")
            continue
        reviewer = str(row.get("reviewer", "")).strip()
        reason = str(row.get("reason", "")).strip()
        if not reviewer or not reason:
            invalid.append(f"REVIEWER_OR_REASON_MISSING:{decision_id}")
            continue
        reviewers.add(reviewer)
        if decision == "ESCALATE":
            unresolved.append(decision_id)
        applied.append({
            "decision_id": decision_id,
            "scope_type": item.get("scope_type"),
            "stage": item.get("stage"),
            "scope_key": item.get("scope_key"),
            "decision": decision,
            "reviewer": reviewer,
            "reason": reason,
        })

    if invalid:
        print("D14_DECISIONS_INVALID: " + ", ".join(invalid[:20]))
        return 2
    if unresolved:
        print(json.dumps({
            "record_type": "D14_REVIEW_HOLD",
            "resolved": len(items) - len(unresolved),
            "required": len(items),
            "unresolved_decision_ids": unresolved,
            "d14_state": "NEEDS_REVIEW",
            "d15_state": "BLOCKED",
            "autonomous_kb_promotion": False,
        }, ensure_ascii=False, indent=2))
        return 2

    accepted_rules = [row for row in applied if row["scope_type"] == "RULE_CLASS" and row["decision"] == "ACCEPT"]
    rejected_rules = [row for row in applied if row["scope_type"] == "RULE_CLASS" and row["decision"] == "REJECT"]
    conflict_decisions = [row for row in applied if row["scope_type"] != "RULE_CLASS"]

    decision_material = json.dumps(applied, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    decisions_sha256 = _sha256_bytes(decision_material)
    result = {
        "schema_version": "1.0",
        "record_type": "D14_EXPERT_REVIEW_RESULT",
        "corpus_id": packet.get("corpus_id"),
        "packet_sha256": packet_sha256,
        "decisions_sha256": decisions_sha256,
        "required_decisions": len(items),
        "resolved_decisions": len(applied),
        "reviewers": sorted(reviewers),
        "accepted_rule_classes": len(accepted_rules),
        "rejected_rule_classes": len(rejected_rules),
        "conflict_overlap_decisions": len(conflict_decisions),
        "decisions": applied,
        "d14_state": "VERIFIED",
        "d15_state": "NOT_DONE",
        "autonomous_kb_promotion": False,
    }
    RESULT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result_sha256 = _sha256_bytes(RESULT_JSON.read_bytes())

    promotion_request = {
        "schema_version": "1.0",
        "record_type": "D15_PROMOTION_REQUEST",
        "corpus_id": packet.get("corpus_id"),
        "d14_result_sha256": result_sha256,
        "packet_sha256": packet_sha256,
        "decisions_sha256": decisions_sha256,
        "accepted_rule_decision_ids": [row["decision_id"] for row in accepted_rules],
        "rejected_rule_decision_ids": [row["decision_id"] for row in rejected_rules],
        "conflict_overlap_decisions": conflict_decisions,
        "request_state": "AWAITING_EXPLICIT_D15_APPROVAL",
        "autonomous_kb_promotion": False,
    }
    PROMOTION_REQUEST.write_text(
        json.dumps(promotion_request, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    store = KnowledgeFactoryStore(STORE_ROOT)
    for document_id in TARGETS:
        payload = store.get_document(document_id)
        if not payload:
            print(f"D14_DOCUMENT_REGISTRY_MISSING:{document_id}")
            return 2
        document = _document(payload)
        document.set_stage_state(PipelineStage.D14_EXPERT_REVIEWED, StageState.VERIFIED)
        store.save_document(document)
    store.append_audit(AuditEvent(
        actor_id=",".join(sorted(reviewers)),
        actor_role=Role.REVIEWER.value,
        action="APPLY_D14_EXPERT_REVIEW_DECISIONS",
        object_type="CORPUS",
        object_id=str(packet.get("corpus_id")),
        result="SUCCESS",
        metadata={
            "packet_sha256": packet_sha256,
            "decisions_sha256": decisions_sha256,
            "result_sha256": result_sha256,
            "accepted_rule_classes": len(accepted_rules),
            "rejected_rule_classes": len(rejected_rules),
            "conflict_overlap_decisions": len(conflict_decisions),
            "autonomous_kb_promotion": False,
        },
    ))

    lines = [
        "# PDn D14 expert review result",
        "",
        f"- packet: `{packet_sha256}`",
        f"- decisions: `{decisions_sha256}`",
        f"- reviewers: {', '.join(sorted(reviewers))}",
        f"- resolved decisions: {len(applied)}/{len(items)}",
        f"- accepted rule classes: {len(accepted_rules)}",
        f"- rejected rule classes: {len(rejected_rules)}",
        f"- D12 decisions: {len(conflict_decisions)}",
        "- D14: **VERIFIED**",
        "- D15: **NOT_DONE — explicit approval required**",
        "",
        "| Decision | Scope | Result | Reviewer | Reason |",
        "|---|---|---|---|---|",
    ]
    for row in applied:
        reason = str(row["reason"]).replace("|", "\\|")
        lines.append(f"| `{row['decision_id']}` | {row['scope_type']} | **{row['decision']}** | {row['reviewer']} | {reason} |")
    RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({
        "record_type": "D14_REVIEW_APPLY_SUMMARY",
        "resolved_decisions": len(applied),
        "required_decisions": len(items),
        "accepted_rule_classes": len(accepted_rules),
        "rejected_rule_classes": len(rejected_rules),
        "conflict_overlap_decisions": len(conflict_decisions),
        "d14_state": "VERIFIED",
        "d15_state": "NOT_DONE",
        "promotion_request": PROMOTION_REQUEST.relative_to(REPO_ROOT).as_posix(),
        "autonomous_kb_promotion": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
