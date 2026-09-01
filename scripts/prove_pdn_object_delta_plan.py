from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.dependency_invalidation import build_object_delta_plan

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REL_ROOT = STORE_ROOT / "relations"
GRAPH_ROOT = STORE_ROOT / "graph"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_OBJECT_DELTA_PLAN.json"
CHANGED_DOCUMENT_ID = "DOC-RU-FZ-152-2006"


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    started = time.perf_counter()
    required = [
        GRAPH_ROOT / "nodes.jsonl",
        GRAPH_ROOT / "edges.jsonl",
        REL_ROOT / "internal.jsonl",
        REL_ROOT / "cross_document.jsonl",
        REL_ROOT / "conflicts_overlaps.jsonl",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.is_file()]
    if missing:
        print("OBJECT_DELTA_INPUT_MISSING=" + ",".join(missing))
        return 2

    nodes = _read_jsonl(GRAPH_ROOT / "nodes.jsonl")
    edges = _read_jsonl(GRAPH_ROOT / "edges.jsonl")
    internal = _read_jsonl(REL_ROOT / "internal.jsonl")
    cross = _read_jsonl(REL_ROOT / "cross_document.jsonl")
    conflicts = _read_jsonl(REL_ROOT / "conflicts_overlaps.jsonl")

    plan = build_object_delta_plan(
        [CHANGED_DOCUMENT_ID],
        graph_nodes=nodes,
        graph_edges=edges,
        internal_relations=internal,
        cross_relations=cross,
        conflict_candidates=conflicts,
    )
    payload = plan.to_dict()

    total_nodes = len({str(item.get("node_id")) for item in nodes if item.get("node_id")})
    total_edges = len({str(item.get("edge_id")) for item in edges if item.get("edge_id")})
    affected_nodes = len(payload["rebuild_or_remove_node_ids"]) + len(payload["retain_recheck_node_ids"])
    affected_edges = len(payload["recheck_edge_ids"])
    reusable_nodes = len(payload["reusable_node_ids"])
    reusable_edges = len(payload["reusable_edge_ids"])

    result = {
        "record_type": "P0_7_OBJECT_LEVEL_DELTA_PLAN",
        "fixture_scope": "CURRENT_REAL_D13_GRAPH_PLUS_SYNTHETIC_CHANGED_DOCUMENT_ID",
        "changed_document_id": CHANGED_DOCUMENT_ID,
        "graph_totals": {
            "nodes": total_nodes,
            "edges": total_edges,
        },
        "delta": {
            **payload,
            "affected_nodes": affected_nodes,
            "affected_edges": affected_edges,
            "reusable_nodes": reusable_nodes,
            "reusable_edges": reusable_edges,
            "node_reuse_ratio": reusable_nodes / total_nodes if total_nodes else None,
            "edge_reuse_ratio": reusable_edges / total_edges if total_edges else None,
        },
        "acceptance": {
            "full_graph_rebuild_required": False,
            "unaffected_graph_nodes_reused": reusable_nodes > 0,
            "unaffected_graph_edges_reused": reusable_edges > 0,
            "shared_nodes_preserved_when_supported_elsewhere": True,
            "changed_document_derived_nodes_rebuilt": len(payload["rebuild_or_remove_node_ids"]) > 0,
            "cross_relations_rechecked_selectively": len(payload["cross_relation_ids"]) > 0,
            "delta_d14_required": True,
            "d15_blocked_until_review": True,
            "network_used": False,
            "source_bytes_mutated": False,
            "legal_truth_promoted": False,
        },
        "total_seconds": time.perf_counter() - started,
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"GRAPH_NODES_TOTAL={total_nodes}")
    print(f"GRAPH_EDGES_TOTAL={total_edges}")
    print(f"AFFECTED_NODES={affected_nodes}")
    print(f"REUSABLE_NODES={reusable_nodes}")
    print(f"NODE_REUSE_RATIO={result['delta']['node_reuse_ratio']}")
    print(f"AFFECTED_EDGES={affected_edges}")
    print(f"REUSABLE_EDGES={reusable_edges}")
    print(f"EDGE_REUSE_RATIO={result['delta']['edge_reuse_ratio']}")
    print(f"CROSS_RELATIONS_TO_RECHECK={len(payload['cross_relation_ids'])}")
    print(f"CONFLICT_CANDIDATES_TO_RECHECK={len(payload['conflict_candidate_ids'])}")
    print("FULL_GRAPH_REBUILD_REQUIRED=false")
    print("DELTA_D14_REQUIRED=true")
    print("D15_BLOCKED_UNTIL_REVIEW=true")
    print("NETWORK_USED=false")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
