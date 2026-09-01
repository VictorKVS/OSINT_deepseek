from __future__ import annotations

import argparse
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
D14_RESULT = REPORT_ROOT / "D14_REVIEW_RESULT.json"
PROMOTION_REQUEST = REPORT_ROOT / "D15_PROMOTION_REQUEST.json"
KB_READY_ROOT = STORE_ROOT / "kb_ready"
TARGETS = (
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    parser = argparse.ArgumentParser(description="Explicit human-gated D15 KB-ready promotion")
    parser.add_argument("--approve", action="store_true", help="Explicitly authorize D15 promotion")
    parser.add_argument("--reviewer", required=True, help="Human/system owner identity authorizing D15")
    args = parser.parse_args()

    if not args.approve:
        print("D15_EXPLICIT_APPROVAL_REQUIRED: pass --approve")
        return 2
    reviewer = args.reviewer.strip()
    if not reviewer:
        print("D15_REVIEWER_REQUIRED")
        return 2
    if not D14_RESULT.is_file() or not PROMOTION_REQUEST.is_file():
        print("D15_INPUT_MISSING: complete D14 first")
        return 2

    result = _read_json(D14_RESULT)
    request = _read_json(PROMOTION_REQUEST)
    result_sha256 = _sha256_file(D14_RESULT)
    if request.get("d14_result_sha256") != result_sha256:
        print("D15_D14_RESULT_HASH_MISMATCH")
        return 2
    if result.get("d14_state") != "VERIFIED":
        print("D15_BLOCKED_D14_NOT_VERIFIED")
        return 2
    if request.get("request_state") != "AWAITING_EXPLICIT_D15_APPROVAL":
        print("D15_PROMOTION_REQUEST_STATE_INVALID")
        return 2

    decisions = list(result.get("decisions", []))
    rule_decisions = [row for row in decisions if row.get("scope_type") == "RULE_CLASS"]
    rejected = [row for row in rule_decisions if row.get("decision") != "ACCEPT"]
    if rejected:
        print("D15_BLOCKED_REJECTED_OR_UNACCEPTED_RULES: " + ", ".join(str(row.get("decision_id")) for row in rejected))
        return 2
    unresolved_conflicts = [
        row for row in decisions
        if row.get("scope_type") != "RULE_CLASS"
        and row.get("decision") not in {"CONFIRMED_CONFLICT", "NOT_CONFLICT", "OVERLAP_ONLY"}
    ]
    if unresolved_conflicts:
        print("D15_BLOCKED_UNRESOLVED_D12_DECISIONS")
        return 2

    store = KnowledgeFactoryStore(STORE_ROOT)
    documents: list[dict[str, Any]] = []
    for document_id in TARGETS:
        payload = store.get_document(document_id)
        if not payload:
            print(f"D15_DOCUMENT_REGISTRY_MISSING:{document_id}")
            return 2
        document = _document(payload)
        if document.stage_states.get(PipelineStage.D14_EXPERT_REVIEWED.value) != StageState.VERIFIED.value:
            print(f"D15_DOCUMENT_D14_NOT_VERIFIED:{document_id}")
            return 2
        document.set_stage_state(PipelineStage.D15_KB_READY, StageState.VERIFIED)
        store.save_document(document)
        documents.append({
            "document_id": document_id,
            "version_id": document.current_version_id,
            "d15_state": "VERIFIED",
        })

    KB_READY_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": "1.0",
        "record_type": "D15_KB_READY_MANIFEST",
        "corpus_id": request.get("corpus_id"),
        "documents": documents,
        "d14_result_sha256": result_sha256,
        "packet_sha256": request.get("packet_sha256"),
        "decisions_sha256": request.get("decisions_sha256"),
        "accepted_rule_decision_ids": request.get("accepted_rule_decision_ids", []),
        "conflict_overlap_decisions": request.get("conflict_overlap_decisions", []),
        "approved_by": reviewer,
        "approval_mode": "EXPLICIT_OPERATOR_COMMAND",
        "kb_ready": True,
        "autonomous_kb_promotion": False,
    }
    manifest_path = KB_READY_ROOT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_sha256 = _sha256_file(manifest_path)

    store.append_audit(AuditEvent(
        actor_id=reviewer,
        actor_role=Role.SYSTEM_OWNER.value,
        action="PROMOTE_CORPUS_D15_KB_READY",
        object_type="CORPUS",
        object_id=str(request.get("corpus_id")),
        result="SUCCESS",
        metadata={
            "manifest_path": manifest_path.relative_to(STORE_ROOT).as_posix(),
            "manifest_sha256": manifest_sha256,
            "approval_mode": "EXPLICIT_OPERATOR_COMMAND",
            "autonomous_kb_promotion": False,
        },
    ))

    print(json.dumps({
        "record_type": "D15_PROMOTION_SUMMARY",
        "documents": len(documents),
        "d15_state": "VERIFIED",
        "kb_ready": True,
        "approved_by": reviewer,
        "manifest": manifest_path.relative_to(REPO_ROOT).as_posix(),
        "manifest_sha256": manifest_sha256,
        "autonomous_kb_promotion": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
