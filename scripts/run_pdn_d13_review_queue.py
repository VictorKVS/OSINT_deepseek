from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.graph_builders import build_graph_rows
from father_osint.knowledge_factory import AuditEvent, DocumentRecord, DocumentVersion, PipelineStage, Role, StageState
from father_osint.knowledge_factory_store import KnowledgeFactoryStore

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
D10_QUALITY = REPO_ROOT / "reports" / "pdn_live" / "D10_D12_QUALITY.json"
D6_SUMMARY = REPO_ROOT / "reports" / "pdn_live" / "D6_D9_EXTRACTION_SUMMARY.json"
REL_ROOT = STORE_ROOT / "relations"
GRAPH_ROOT = STORE_ROOT / "graph"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "D13_GRAPH_SUMMARY.json"
REVIEW_QUEUE = REPO_ROOT / "reports" / "pdn_live" / "D14_REVIEW_QUEUE.md"
TARGETS = (
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
)


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n")


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


def _load_per_doc(d6: dict[str, object]) -> dict[str, dict[str, list[dict[str, object]]]]:
    by_id = {str(item.get("document_id")): item for item in d6.get("documents", [])}
    if any(document_id not in by_id for document_id in TARGETS):
        raise ValueError("D13_INPUT_INCOMPLETE")
    result: dict[str, dict[str, list[dict[str, object]]]] = {}
    for document_id in TARGETS:
        version_id = str(by_id[document_id]["version_id"])
        base = STORE_ROOT / "knowledge" / document_id / version_id
        result[document_id] = {
            name: _read_jsonl(base / f"{name}.jsonl")
            for name in ("terms", "definitions", "requirements", "entities")
        }
    return result


def main() -> int:
    if not D10_QUALITY.is_file():
        print("D10_D12_QUALITY_MISSING")
        return 2
    quality = json.loads(D10_QUALITY.read_text(encoding="utf-8"))
    if quality.get("summary", {}).get("promotion_to_d13_allowed") is not True:
        print("D13_BLOCKED_BY_D10_D12_QUALITY_GATE")
        return 2
    if not D6_SUMMARY.is_file():
        print("D6_D9_SUMMARY_MISSING")
        return 2

    d6 = json.loads(D6_SUMMARY.read_text(encoding="utf-8"))
    try:
        per_doc = _load_per_doc(d6)
        internal = _read_jsonl(REL_ROOT / "internal.jsonl")
        cross = _read_jsonl(REL_ROOT / "cross_document.jsonl")
        conflicts = _read_jsonl(REL_ROOT / "conflicts_overlaps.jsonl")
        graph = build_graph_rows(
            per_doc,
            internal,
            cross,
            conflicts,
            document_order=TARGETS,
        )
    except (KeyError, ValueError) as exc:
        print(f"D13_GRAPH_ENDPOINT_FAILURE: {exc}")
        return 2

    nodes = list(graph.nodes)
    edges = list(graph.edges)
    nodes_path = GRAPH_ROOT / "nodes.jsonl"
    edges_path = GRAPH_ROOT / "edges.jsonl"
    _write_jsonl(nodes_path, nodes)
    _write_jsonl(edges_path, edges)
    manifest = {
        "schema_version": "1.0",
        "graph_nodes": len(nodes),
        "graph_edges": len(edges),
        "missing_endpoints": 0,
        "conflict_overlap_candidates_for_review": len(conflicts),
        "review_required": True,
        "autonomous_kb_promotion": False,
    }
    manifest_path = GRAPH_ROOT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    store = KnowledgeFactoryStore(STORE_ROOT)
    for document_id in TARGETS:
        payload = store.get_document(document_id)
        if not payload:
            raise RuntimeError(f"document registry missing: {document_id}")
        doc = _document(payload)
        doc.set_stage_state(PipelineStage.D13_KNOWLEDGE_GRAPH_READY, StageState.DONE)
        doc.set_stage_state(PipelineStage.D14_EXPERT_REVIEWED, StageState.NEEDS_REVIEW)
        store.save_document(doc)
    store.append_audit(AuditEvent(
        actor_id="pdn-d13-graph-builder",
        actor_role=Role.KNOWLEDGE_CURATOR.value,
        action="BUILD_D13_GRAPH_AND_D14_REVIEW_QUEUE",
        object_type="CORPUS",
        object_id="PDN-OFFICIAL-SOURCE-PACK-001",
        result="SUCCESS",
        metadata={**manifest, "manifest_path": manifest_path.relative_to(STORE_ROOT).as_posix()},
    ))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({"record_type": "D13_GRAPH_SUMMARY", **manifest}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# PDn D14 expert review queue",
        "",
        "D13 graph is ready, but D14/D15 remain blocked until controlled review. No candidate below is a confirmed conflict by automation alone.",
        "",
        f"- graph nodes: {len(nodes)}",
        f"- graph edges: {len(edges)}",
        f"- conflict/overlap candidates: {len(conflicts)}",
        "- D14 state: **NEEDS_REVIEW**",
        "- D15 autonomous promotion: **blocked**",
        "",
        "| Candidate | Type | Documents | Confirmed conflict |",
        "|---|---|---|---|",
    ]
    for candidate in conflicts:
        docs = ", ".join(str(value) for value in candidate.get("document_ids", []))
        lines.append(f"| `{candidate['candidate_id']}` | {candidate['candidate_type']} | {docs or '—'} | no |")
    REVIEW_QUEUE.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"record_type": "D13_GRAPH_SUMMARY", **manifest, "d14_state": "NEEDS_REVIEW", "d15_state": "BLOCKED"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
