from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.knowledge_factory import PipelineStage, StageState
from father_osint.knowledge_factory_store import KnowledgeFactoryStore

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
GRAPH_ROOT = STORE_ROOT / "graph"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "D13_QUALITY.json"
TARGETS = {
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
}


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    nodes_path = GRAPH_ROOT / "nodes.jsonl"
    edges_path = GRAPH_ROOT / "edges.jsonl"
    manifest_path = GRAPH_ROOT / "manifest.json"
    if not all(path.is_file() for path in (nodes_path, edges_path, manifest_path)):
        print("D13_GRAPH_INPUT_MISSING")
        return 2

    nodes = _read_jsonl(nodes_path)
    edges = _read_jsonl(edges_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    failures: list[str] = []

    node_ids = [str(row.get("node_id", "")) for row in nodes]
    edge_ids = [str(row.get("edge_id", "")) for row in edges]
    duplicate_nodes = sum(count - 1 for count in Counter(node_ids).values() if count > 1)
    duplicate_edges = sum(count - 1 for count in Counter(edge_ids).values() if count > 1)
    node_set = set(node_ids)
    missing_endpoints = sum(
        1 for edge in edges
        if str(edge.get("from_node")) not in node_set or str(edge.get("to_node")) not in node_set
    )
    invalid_candidate_states = sum(
        1 for row in nodes + edges
        if row.get("review_state") != "CANDIDATE_NEEDS_REVIEW" or row.get("promotion_state") != "NOT_PROMOTED"
    )

    if duplicate_nodes:
        failures.append("DUPLICATE_GRAPH_NODE_IDS")
    if duplicate_edges:
        failures.append("DUPLICATE_GRAPH_EDGE_IDS")
    if missing_endpoints:
        failures.append("GRAPH_EDGE_ENDPOINT_MISSING")
    if invalid_candidate_states:
        failures.append("GRAPH_REVIEW_OR_PROMOTION_STATE_INVALID")
    if manifest.get("autonomous_kb_promotion") is not False:
        failures.append("AUTONOMOUS_PROMOTION_NOT_BLOCKED")

    store = KnowledgeFactoryStore(STORE_ROOT)
    docs = {str(row.get("document_id")): row for row in store.list_documents() if row.get("document_id") in TARGETS}
    if set(docs) != TARGETS:
        failures.append("DOCUMENT_STAGE_INPUT_INCOMPLETE")
    bad_d13 = 0
    bad_d14 = 0
    bad_d15 = 0
    for row in docs.values():
        states = row.get("stage_states", {})
        if states.get(PipelineStage.D13_KNOWLEDGE_GRAPH_READY.value) != StageState.DONE.value:
            bad_d13 += 1
        if states.get(PipelineStage.D14_EXPERT_REVIEWED.value) != StageState.NEEDS_REVIEW.value:
            bad_d14 += 1
        if states.get(PipelineStage.D15_KB_READY.value) != StageState.NOT_DONE.value:
            bad_d15 += 1
    if bad_d13:
        failures.append("D13_NOT_DONE_FOR_ALL_DOCUMENTS")
    if bad_d14:
        failures.append("D14_NOT_NEEDS_REVIEW_FOR_ALL_DOCUMENTS")
    if bad_d15:
        failures.append("D15_PREMATURELY_ADVANCED")

    payload = {
        "summary": {
            "record_type": "D13_QUALITY",
            "quality_pass": not failures,
            "graph_nodes": len(nodes),
            "graph_edges": len(edges),
            "duplicate_nodes": duplicate_nodes,
            "duplicate_edges": duplicate_edges,
            "missing_endpoints": missing_endpoints,
            "invalid_candidate_states": invalid_candidate_states,
            "d13_bad_documents": bad_d13,
            "d14_bad_documents": bad_d14,
            "d15_bad_documents": bad_d15,
            "d14_state": "NEEDS_REVIEW",
            "d15_state": "BLOCKED",
            "failures": failures,
            "autonomous_kb_promotion": False,
        }
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
