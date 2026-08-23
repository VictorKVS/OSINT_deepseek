from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.knowledge_factory import AuditEvent, DocumentRecord, DocumentVersion, PipelineStage, Role, StageState
from father_osint.knowledge_factory_store import KnowledgeFactoryStore
from father_osint.relation_builders import build_relation_sets

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
QUALITY = REPO_ROOT / "reports" / "pdn_live" / "D6_D9_QUALITY.json"
SUMMARY = REPO_ROOT / "reports" / "pdn_live" / "D6_D9_EXTRACTION_SUMMARY.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "D10_D12_SUMMARY.json"
TARGETS = (
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
)


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _document(payload: dict[str, object]) -> DocumentRecord:
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
    if not QUALITY.is_file():
        print("D6_D9_QUALITY_MISSING")
        return 2
    quality = json.loads(QUALITY.read_text(encoding="utf-8"))
    if quality.get("summary", {}).get("promotion_to_d10_allowed") is not True:
        print("D10_BLOCKED_BY_D6_D9_QUALITY_GATE")
        return 2
    if not SUMMARY.is_file():
        print("D6_D9_SUMMARY_MISSING")
        return 2

    d6_summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    by_id = {str(item.get("document_id")): item for item in d6_summary.get("documents", [])}
    if any(document_id not in by_id for document_id in TARGETS):
        print("D10_D12_INPUT_INCOMPLETE")
        return 2

    per_doc: dict[str, dict[str, list[dict[str, object]]]] = {}
    for document_id in TARGETS:
        version_id = str(by_id[document_id]["version_id"])
        base = STORE_ROOT / "knowledge" / document_id / version_id
        per_doc[document_id] = {
            "terms": _read_jsonl(base / "terms.jsonl"),
            "definitions": _read_jsonl(base / "definitions.jsonl"),
            "requirements": _read_jsonl(base / "requirements.jsonl"),
            "entities": _read_jsonl(base / "entities.jsonl"),
        }

    internal, cross, conflicts = build_relation_sets(per_doc)

    output_dir = STORE_ROOT / "relations"
    internal_path = output_dir / "internal.jsonl"
    cross_path = output_dir / "cross_document.jsonl"
    conflicts_path = output_dir / "conflicts_overlaps.jsonl"
    _write_jsonl(internal_path, internal)
    _write_jsonl(cross_path, cross)
    _write_jsonl(conflicts_path, conflicts)

    manifest = {
        "schema_version": "1.0",
        "internal_relations": len(internal),
        "cross_document_relations": len(cross),
        "conflict_overlap_candidates": len(conflicts),
        "confirmed_conflicts": 0,
        "review_required": True,
        "autonomous_kb_promotion": False,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    store = KnowledgeFactoryStore(STORE_ROOT)
    for document_id in TARGETS:
        payload = store.get_document(document_id)
        if not payload:
            raise RuntimeError(f"document registry missing: {document_id}")
        doc = _document(payload)
        doc.set_stage_state(PipelineStage.D10_INTERNAL_RELATIONS, StageState.DONE)
        doc.set_stage_state(PipelineStage.D11_CROSS_DOCUMENT_RELATIONS, StageState.DONE)
        doc.set_stage_state(PipelineStage.D12_CONFLICTS_OVERLAPS, StageState.DONE)
        store.save_document(doc)
    store.append_audit(AuditEvent(
        actor_id="pdn-d10-d12-deterministic",
        actor_role=Role.KNOWLEDGE_CURATOR.value,
        action="BUILD_RELATIONS_CONFLICT_CANDIDATES_D10_D12",
        object_type="CORPUS",
        object_id="PDN-OFFICIAL-SOURCE-PACK-001",
        result="SUCCESS",
        metadata={**manifest, "manifest_path": manifest_path.relative_to(STORE_ROOT).as_posix()},
    ))

    summary = {"record_type": "D10_D12_SUMMARY", **manifest}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
