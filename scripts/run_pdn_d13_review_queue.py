from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

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


def _stable_id(prefix: str, *parts: str) -> str:
    canonical = "\x1f".join(" ".join(str(part).split()).casefold() for part in parts)
    return f"{prefix}-{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:24]}"


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
    by_id = {str(item.get("document_id")): item for item in d6.get("documents", [])}
    if any(document_id not in by_id for document_id in TARGETS):
        print("D13_INPUT_INCOMPLETE")
        return 2

    nodes: dict[str, dict[str, object]] = {}
    edges: dict[str, dict[str, object]] = {}

    def add_node(node_id: str, node_type: str, **metadata: object) -> None:
        nodes.setdefault(node_id, {
            "node_id": node_id,
            "node_type": node_type,
            "metadata": metadata,
            "review_state": "CANDIDATE_NEEDS_REVIEW",
            "promotion_state": "NOT_PROMOTED",
        })

    def add_edge(edge_id: str, relation_type: str, from_node: str, to_node: str, **metadata: object) -> None:
        edges.setdefault(edge_id, {
            "edge_id": edge_id,
            "relation_type": relation_type,
            "from_node": from_node,
            "to_node": to_node,
            "metadata": metadata,
            "review_state": "CANDIDATE_NEEDS_REVIEW",
            "promotion_state": "NOT_PROMOTED",
        })

    definition_to_node: dict[str, str] = {}
    requirement_to_node: dict[str, str] = {}
    entity_mention_to_node: dict[str, str] = {}

    for document_id in TARGETS:
        doc_node = f"DOC:{document_id}"
        add_node(doc_node, "DOCUMENT", document_id=document_id)
        version_id = str(by_id[document_id]["version_id"])
        base = STORE_ROOT / "knowledge" / document_id / version_id
        terms = _read_jsonl(base / "terms.jsonl")
        definitions = _read_jsonl(base / "definitions.jsonl")
        requirements = _read_jsonl(base / "requirements.jsonl")
        entities = _read_jsonl(base / "entities.jsonl")

        for term in terms:
            term_node = f"TERM:{term['canonical_key']}"
            add_node(term_node, "TERM", canonical_key=term["canonical_key"], term=term["term"])
            add_edge(_stable_id("E13", doc_node, term_node, "mentions-term"), "DOCUMENT_MENTIONS_TERM", doc_node, term_node)
        for definition in definitions:
            def_node = f"DEF:{definition['definition_id']}"
            definition_to_node[str(definition["definition_id"])] = def_node
            add_node(def_node, "DEFINITION_CANDIDATE", definition_id=definition["definition_id"], canonical_key=definition["canonical_key"])
            add_edge(_stable_id("E13", doc_node, def_node, "contains-definition"), "DOCUMENT_CONTAINS_DEFINITION", doc_node, def_node)
        for requirement in requirements:
            req_node = f"REQ:{requirement['requirement_id']}"
            requirement_to_node[str(requirement["requirement_id"])] = req_node
            add_node(req_node, "REQUIREMENT_CANDIDATE", requirement_id=requirement["requirement_id"], modality=requirement["modality"])
            add_edge(_stable_id("E13", doc_node, req_node, "contains-requirement"), "DOCUMENT_CONTAINS_REQUIREMENT", doc_node, req_node)
        for entity in entities:
            ent_node = f"ENT:{entity['canonical_key']}"
            entity_mention_to_node[str(entity["entity_mention_id"])] = ent_node
            add_node(ent_node, "ENTITY_CANDIDATE", canonical_key=entity["canonical_key"], entity=entity["entity"], entity_kind=entity["entity_kind"])
            add_edge(_stable_id("E13", doc_node, ent_node, "mentions-entity"), "DOCUMENT_MENTIONS_ENTITY", doc_node, ent_node)

    internal = _read_jsonl(REL_ROOT / "internal.jsonl")
    cross = _read_jsonl(REL_ROOT / "cross_document.jsonl")
    conflicts = _read_jsonl(REL_ROOT / "conflicts_overlaps.jsonl")
    for relation in internal:
        if relation["relation_type"] == "TERM_DEFINED_BY":
            from_node = f"TERM:{relation['from_canonical_key']}"
            to_node = definition_to_node[str(relation["to_definition_id"])]
        else:
            from_node = requirement_to_node[str(relation["from_requirement_id"])]
            to_node = entity_mention_to_node[str(relation["to_entity_mention_id"])]
        add_edge(str(relation["relation_id"]), str(relation["relation_type"]), from_node, to_node, evidence_chunk_id=relation.get("evidence_chunk_id"))

    for relation in cross:
        docs = [f"DOC:{value}" for value in relation.get("document_ids", [])]
        for left_index, left in enumerate(docs):
            for right in docs[left_index + 1:]:
                edge_id = _stable_id("E13", relation["relation_id"], left, right)
                add_edge(edge_id, str(relation["relation_type"]), left, right, canonical_key=relation.get("canonical_key"))

    conflict_queue: list[dict[str, object]] = []
    for candidate in conflicts:
        conflict_node = f"CON:{candidate['candidate_id']}"
        add_node(conflict_node, "CONFLICT_OR_OVERLAP_CANDIDATE", candidate_id=candidate["candidate_id"], candidate_type=candidate["candidate_type"], confirmed_conflict=False)
        for document_id in candidate.get("document_ids", []):
            doc_node = f"DOC:{document_id}"
            add_edge(_stable_id("E13", conflict_node, doc_node), "CANDIDATE_INVOLVES_DOCUMENT", conflict_node, doc_node)
        conflict_queue.append(candidate)

    missing_endpoints = [
        edge_id for edge_id, edge in edges.items()
        if edge["from_node"] not in nodes or edge["to_node"] not in nodes
    ]
    if missing_endpoints:
        print("D13_GRAPH_ENDPOINT_FAILURE: " + ", ".join(missing_endpoints[:10]))
        return 2

    nodes_path = GRAPH_ROOT / "nodes.jsonl"
    edges_path = GRAPH_ROOT / "edges.jsonl"
    _write_jsonl(nodes_path, list(nodes.values()))
    _write_jsonl(edges_path, list(edges.values()))
    manifest = {
        "schema_version": "1.0",
        "graph_nodes": len(nodes),
        "graph_edges": len(edges),
        "missing_endpoints": 0,
        "conflict_overlap_candidates_for_review": len(conflict_queue),
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
        f"- conflict/overlap candidates: {len(conflict_queue)}",
        "- D14 state: **NEEDS_REVIEW**",
        "- D15 autonomous promotion: **blocked**",
        "",
        "| Candidate | Type | Documents | Confirmed conflict |",
        "|---|---|---|---|",
    ]
    for candidate in conflict_queue:
        docs = ", ".join(str(value) for value in candidate.get("document_ids", []))
        lines.append(f"| `{candidate['candidate_id']}` | {candidate['candidate_type']} | {docs or '—'} | no |")
    REVIEW_QUEUE.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"record_type": "D13_GRAPH_SUMMARY", **manifest, "d14_state": "NEEDS_REVIEW", "d15_state": "BLOCKED"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
