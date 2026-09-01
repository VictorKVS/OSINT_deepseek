from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.delta_execution import execute_shadow_delta

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
GRAPH_ROOT = STORE_ROOT / "graph"
PLAN_REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_OBJECT_DELTA_PLAN.json"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_DELTA_SHADOW_EXECUTION.json"
DELTA_D14_PACKET = REPO_ROOT / "reports" / "pdn_live" / "P0_7_DELTA_D14_PACKET.json"
SHADOW_ROOT = REPO_ROOT / ".runtime" / "pdn_delta_shadow"


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    started = time.perf_counter()
    nodes_path = GRAPH_ROOT / "nodes.jsonl"
    edges_path = GRAPH_ROOT / "edges.jsonl"
    required = [nodes_path, edges_path, PLAN_REPORT]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.is_file()]
    if missing:
        print("DELTA_SHADOW_INPUT_MISSING=" + ",".join(missing))
        return 2

    nodes_before_sha = _sha256(nodes_path)
    edges_before_sha = _sha256(edges_path)
    nodes = _read_jsonl(nodes_path)
    edges = _read_jsonl(edges_path)
    plan_report = json.loads(PLAN_REPORT.read_text(encoding="utf-8"))
    delta = plan_report.get("delta")
    if not isinstance(delta, dict):
        print("DELTA_PLAN_INVALID")
        return 2

    execution = execute_shadow_delta(delta, graph_nodes=nodes, graph_edges=edges)

    SHADOW_ROOT.mkdir(parents=True, exist_ok=True)
    _write_jsonl(SHADOW_ROOT / "reused_nodes.jsonl", execution.reusable_nodes)
    _write_jsonl(SHADOW_ROOT / "reused_edges.jsonl", execution.reusable_edges)
    _write_jsonl(SHADOW_ROOT / "node_actions.jsonl", execution.node_actions)
    _write_jsonl(SHADOW_ROOT / "edge_actions.jsonl", execution.edge_actions)

    changed_document_ids = list(delta.get("changed_document_ids", []))
    d14_packet = {
        "record_type": "P0_7_DELTA_D14_PACKET",
        "packet_scope": "SHADOW_INVALIDATION_ONLY__NO_REBUILT_KNOWLEDGE_PROMOTED",
        "changed_document_ids": changed_document_ids,
        "node_actions": len(execution.node_actions),
        "edge_actions": len(execution.edge_actions),
        "cross_relation_ids_to_recheck": list(delta.get("cross_relation_ids", [])),
        "conflict_candidate_ids_to_recheck": list(delta.get("conflict_candidate_ids", [])),
        "review_state": "NEEDS_REVIEW",
        "delta_d14_required": True,
        "d15_blocked_until_review": True,
        "legal_truth_promoted": False,
    }
    DELTA_D14_PACKET.parent.mkdir(parents=True, exist_ok=True)
    DELTA_D14_PACKET.write_text(json.dumps(d14_packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    shadow_manifest = {
        "record_type": "P0_7_SHADOW_DELTA_MANIFEST",
        "source_graph_nodes_sha256": nodes_before_sha,
        "source_graph_edges_sha256": edges_before_sha,
        "changed_document_ids": changed_document_ids,
        "execution": execution.summary(),
        "canonical_graph_mutated": False,
        "source_bytes_mutated": False,
        "d15_blocked_until_review": True,
        "legal_truth_promoted": False,
    }
    (SHADOW_ROOT / "manifest.json").write_text(json.dumps(shadow_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    nodes_after_sha = _sha256(nodes_path)
    edges_after_sha = _sha256(edges_path)
    source_graph_immutable = nodes_before_sha == nodes_after_sha and edges_before_sha == edges_after_sha

    summary = execution.summary()
    acceptance = {
        "source_graph_immutable": source_graph_immutable,
        "node_plan_complete_and_disjoint": bool(summary["node_coverage_ok"] and summary["node_sets_disjoint"]),
        "edge_plan_complete_and_disjoint": bool(summary["edge_coverage_ok"] and summary["edge_sets_disjoint"]),
        "reused_node_payload_exact": bool(summary["reusable_node_payload_match"]),
        "reused_edge_payload_exact": bool(summary["reusable_edge_payload_match"]),
        "delta_d14_packet_ready": DELTA_D14_PACKET.is_file(),
        "d15_blocked_until_review": True,
        "network_used": False,
        "source_bytes_mutated": False,
        "legal_truth_promoted": False,
    }
    passed = all(
        acceptance[key]
        for key in (
            "source_graph_immutable",
            "node_plan_complete_and_disjoint",
            "edge_plan_complete_and_disjoint",
            "reused_node_payload_exact",
            "reused_edge_payload_exact",
            "delta_d14_packet_ready",
            "d15_blocked_until_review",
        )
    )

    result = {
        "record_type": "P0_7_DELTA_SHADOW_EXECUTION_PROOF",
        "fixture_scope": "CURRENT_REAL_D13_GRAPH_PLUS_SYNTHETIC_CHANGED_DOCUMENT_PLAN",
        "changed_document_ids": changed_document_ids,
        "canonical_graph": {
            "nodes_sha256_before": nodes_before_sha,
            "nodes_sha256_after": nodes_after_sha,
            "edges_sha256_before": edges_before_sha,
            "edges_sha256_after": edges_after_sha,
            "immutable": source_graph_immutable,
        },
        "shadow": {
            **summary,
            "runtime_root": SHADOW_ROOT.relative_to(REPO_ROOT).as_posix(),
            "delta_d14_packet": DELTA_D14_PACKET.relative_to(REPO_ROOT).as_posix(),
        },
        "acceptance": acceptance,
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"SOURCE_GRAPH_IMMUTABLE={str(source_graph_immutable).lower()}")
    print(f"PLAN_COVERAGE_NODES={str(summary['node_coverage_ok']).lower()}")
    print(f"PLAN_COVERAGE_EDGES={str(summary['edge_coverage_ok']).lower()}")
    print(f"REUSED_NODE_PAYLOAD_MATCH={str(summary['reusable_node_payload_match']).lower()}")
    print(f"REUSED_EDGE_PAYLOAD_MATCH={str(summary['reusable_edge_payload_match']).lower()}")
    print(f"SHADOW_REUSED_NODES={summary['reused_nodes']}")
    print(f"SHADOW_NODE_ACTIONS={summary['node_actions']}")
    print(f"SHADOW_REUSED_EDGES={summary['reused_edges']}")
    print(f"SHADOW_EDGE_ACTIONS={summary['edge_actions']}")
    print(f"DELTA_D14_PACKET_READY={str(DELTA_D14_PACKET.is_file()).lower()}")
    print("D15_BLOCKED_UNTIL_REVIEW=true")
    print("NETWORK_USED=false")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
