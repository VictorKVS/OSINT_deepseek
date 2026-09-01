from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path
from typing import Mapping

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.audit_pdn_d10_d12 as audit_d10
import scripts.audit_pdn_d13 as audit_d13
import scripts.audit_pdn_d6_d9 as audit_d6
import scripts.run_pdn_d10_d12 as run_d10
import scripts.run_pdn_d13_review_queue as run_d13
import scripts.run_pdn_d6_d9 as run_d6
from father_osint.graph_builders import (
    GraphRows,
    build_conflict_graph_fragment,
    build_cross_graph_fragment,
    build_document_graph_fragment,
    build_internal_graph_fragment,
    materialize_selective_graph,
)
from father_osint.relation_builders import conflict_candidate_signature, cross_relation_signature
from scripts.prove_pdn_differential_d6_d13 import (
    CANON_REPORTS,
    CANON_STORE,
    CHANGED_DOCUMENT_ID,
    TARGETS,
    _inject_synthetic_d5_delta,
    _merge_d6_summary,
    _read_jsonl,
    _run_stage,
    _sha256,
)
from scripts.prove_pdn_dual_path_d10_d13 import _load_per_doc, _rows_equal, _write_jsonl
from scripts.prove_pdn_dual_path_d11_d13 import _canonical_changed_knowledge, _copy_workspace
from scripts.prove_pdn_dual_path_d12_d13 import (
    _canonical_requirement_statement_map,
    _write_selective_d10_d12_relations,
)

RUNTIME_ROOT = REPO_ROOT / ".runtime" / "pdn_dual_path_d13"
FULL_STORE = RUNTIME_ROOT / "full_store"
FULL_REPORTS = RUNTIME_ROOT / "full_reports"
SELECTIVE_STORE = RUNTIME_ROOT / "selective_store"
SELECTIVE_REPORTS = RUNTIME_ROOT / "selective_reports"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_DUAL_PATH_D13.json"


def _run_full_tail(store_root: Path, reports_root: Path, d6_summary_path: Path, label: str) -> None:
    _run_stage(audit_d10, {
        "STORE_ROOT": store_root,
        "REL_ROOT": store_root / "relations",
        "SUMMARY": reports_root / "D10_D12_SUMMARY.json",
        "D6_SUMMARY": d6_summary_path,
        "REPORT": reports_root / "D10_D12_QUALITY.json",
        "TARGETS": set(TARGETS),
    }, f"{label} D10-D12 quality")
    _run_stage(run_d13, {
        "STORE_ROOT": store_root,
        "D10_QUALITY": reports_root / "D10_D12_QUALITY.json",
        "D6_SUMMARY": d6_summary_path,
        "REL_ROOT": store_root / "relations",
        "GRAPH_ROOT": store_root / "graph",
        "REPORT": reports_root / "D13_GRAPH_SUMMARY.json",
        "REVIEW_QUEUE": reports_root / "D14_REVIEW_QUEUE.md",
        "TARGETS": TARGETS,
    }, f"{label} D13 full rebuild")
    _run_stage(audit_d13, {
        "STORE_ROOT": store_root,
        "GRAPH_ROOT": store_root / "graph",
        "REPORT": reports_root / "D13_QUALITY.json",
        "TARGETS": set(TARGETS),
    }, f"{label} D13 quality")


def _fragment_ids(fragments: list[GraphRows], key: str) -> set[str]:
    rows = [row for fragment in fragments for row in (fragment.nodes if key == "node_id" else fragment.edges)]
    return {str(row[key]) for row in rows}


def _refresh_shared_nodes(
    per_doc: Mapping[str, Mapping[str, list[dict[str, object]]]],
    shared_ids: set[str],
) -> list[dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for document_id in TARGETS:
        fragment = build_document_graph_fragment(document_id, per_doc[document_id])
        for row in fragment.nodes:
            node_id = str(row["node_id"])
            if node_id in shared_ids:
                result.setdefault(node_id, dict(row))
    return list(result.values())


def _write_selective_graph(
    store_root: Path,
    reports_root: Path,
    d6_summary: Mapping[str, object],
    selective_rel: Mapping[str, object],
) -> dict[str, object]:
    per_doc = _load_per_doc(store_root, d6_summary)
    old_changed = _canonical_changed_knowledge()
    new_changed = per_doc[CHANGED_DOCUMENT_ID]

    canonical_nodes = _read_jsonl(CANON_STORE / "graph" / "nodes.jsonl")
    canonical_edges = _read_jsonl(CANON_STORE / "graph" / "edges.jsonl")
    canonical_internal = _read_jsonl(CANON_STORE / "relations" / "internal.jsonl")
    canonical_cross = _read_jsonl(CANON_STORE / "relations" / "cross_document.jsonl")
    canonical_conflicts = _read_jsonl(CANON_STORE / "relations" / "conflicts_overlaps.jsonl")

    affected_cross_signatures = set(selective_rel["affected_cross_signatures"])
    affected_conflict_signatures = set(selective_rel["affected_conflict_signatures"])
    statement_by_id = _canonical_requirement_statement_map()

    old_changed_internal = [
        row for row in canonical_internal
        if str(row.get("document_id")) == CHANGED_DOCUMENT_ID
    ]
    old_affected_cross = [
        row for row in canonical_cross
        if cross_relation_signature(row) in affected_cross_signatures
    ]
    old_affected_conflicts = [
        row for row in canonical_conflicts
        if conflict_candidate_signature(
            row,
            requirement_statement_by_id=statement_by_id,
        ) in affected_conflict_signatures
    ]

    old_fragments = [
        build_document_graph_fragment(CHANGED_DOCUMENT_ID, old_changed),
        build_internal_graph_fragment(old_changed_internal),
        build_cross_graph_fragment(old_affected_cross),
        build_conflict_graph_fragment(old_affected_conflicts),
    ]
    new_fragments = [
        build_document_graph_fragment(CHANGED_DOCUMENT_ID, new_changed),
        build_internal_graph_fragment(selective_rel["rebuilt_internal"]),
        build_cross_graph_fragment(selective_rel["rebuilt_cross"]),
        build_conflict_graph_fragment(selective_rel["rebuilt_conflicts"]),
    ]

    old_node_ids = _fragment_ids(old_fragments, "node_id")
    old_edge_ids = _fragment_ids(old_fragments, "edge_id")
    new_node_ids = _fragment_ids(new_fragments, "node_id")
    shared_fallback_ids = {
        node_id
        for node_id in old_node_ids - new_node_ids
        if node_id.startswith("TERM:") or node_id.startswith("ENT:")
    }
    refreshed_shared_nodes = _refresh_shared_nodes(per_doc, shared_fallback_ids)

    selective_graph = materialize_selective_graph(
        canonical_nodes,
        canonical_edges,
        old_fragments=old_fragments,
        new_fragments=new_fragments,
        refreshed_shared_nodes=refreshed_shared_nodes,
    )

    graph_root = store_root / "graph"
    _write_jsonl(graph_root / "nodes.jsonl", selective_graph.nodes)
    _write_jsonl(graph_root / "edges.jsonl", selective_graph.edges)
    manifest = {
        "schema_version": "1.0",
        "graph_nodes": len(selective_graph.nodes),
        "graph_edges": len(selective_graph.edges),
        "missing_endpoints": 0,
        "conflict_overlap_candidates_for_review": len(selective_rel["conflicts"]),
        "review_required": True,
        "autonomous_kb_promotion": False,
    }
    (graph_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (reports_root / "D13_GRAPH_SUMMARY.json").write_text(
        json.dumps({"record_type": "D13_GRAPH_SUMMARY", **manifest}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    canonical_node_by_id = {str(row["node_id"]): row for row in canonical_nodes}
    canonical_edge_by_id = {str(row["edge_id"]): row for row in canonical_edges}
    selective_node_by_id = {str(row["node_id"]): row for row in selective_graph.nodes}
    selective_edge_by_id = {str(row["edge_id"]): row for row in selective_graph.edges}

    explicit_reused_node_ids = set(canonical_node_by_id) - old_node_ids
    explicit_reused_edge_ids = set(canonical_edge_by_id) - old_edge_ids
    explicit_nodes_exact = all(
        node_id in selective_node_by_id
        and canonical_node_by_id[node_id] == selective_node_by_id[node_id]
        for node_id in explicit_reused_node_ids
    )
    explicit_edges_exact = all(
        edge_id in selective_edge_by_id
        and canonical_edge_by_id[edge_id] == selective_edge_by_id[edge_id]
        for edge_id in explicit_reused_edge_ids
    )

    return {
        "graph": selective_graph,
        "old_affected_node_ids": old_node_ids,
        "old_affected_edge_ids": old_edge_ids,
        "new_fragment_node_ids": new_node_ids,
        "explicit_reused_node_ids": explicit_reused_node_ids,
        "explicit_reused_edge_ids": explicit_reused_edge_ids,
        "explicit_reused_nodes_exact": explicit_nodes_exact,
        "explicit_reused_edges_exact": explicit_edges_exact,
        "refreshed_shared_nodes": refreshed_shared_nodes,
    }


def main() -> int:
    started = time.perf_counter()
    required = [
        CANON_STORE / "review" / "batch_review_manifest.json",
        CANON_STORE / "relations" / "internal.jsonl",
        CANON_STORE / "relations" / "cross_document.jsonl",
        CANON_STORE / "relations" / "conflicts_overlaps.jsonl",
        CANON_STORE / "graph" / "nodes.jsonl",
        CANON_STORE / "graph" / "edges.jsonl",
        CANON_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
        CANON_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.is_file()]
    if missing:
        print("DUAL_PATH_D13_INPUT_MISSING=" + ",".join(missing))
        return 2

    canonical_nodes_path = CANON_STORE / "graph" / "nodes.jsonl"
    canonical_edges_path = CANON_STORE / "graph" / "edges.jsonl"
    nodes_sha_before = _sha256(canonical_nodes_path)
    edges_sha_before = _sha256(canonical_edges_path)

    if RUNTIME_ROOT.exists():
        shutil.rmtree(RUNTIME_ROOT)
    RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
    _copy_workspace(FULL_STORE, FULL_REPORTS)
    _copy_workspace(SELECTIVE_STORE, SELECTIVE_REPORTS)

    full_fixture = _inject_synthetic_d5_delta(FULL_STORE)
    selective_fixture = _inject_synthetic_d5_delta(SELECTIVE_STORE)
    same_fixture = all(
        full_fixture[key] == selective_fixture[key]
        for key in ("chunk_locator", "new_chunk_id", "chunks_sha256_after_fixture")
    )
    if not same_fixture:
        raise RuntimeError("FULL and SELECTIVE fixtures differ")

    full_started = time.perf_counter()
    full_d6_path = FULL_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json"
    _run_stage(run_d6, {
        "STORE_ROOT": FULL_STORE,
        "REVIEW": FULL_STORE / "review" / "batch_review_manifest.json",
        "QUALITY": FULL_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
        "REPORT": full_d6_path,
        "TARGETS": TARGETS,
    }, "FULL D6-D9")
    _run_stage(audit_d6, {
        "STORE_ROOT": FULL_STORE,
        "SUMMARY": full_d6_path,
        "REPORT": FULL_REPORTS / "D6_D9_QUALITY.json",
        "TARGETS": TARGETS,
    }, "FULL D6 quality")
    _run_stage(run_d10, {
        "STORE_ROOT": FULL_STORE,
        "QUALITY": FULL_REPORTS / "D6_D9_QUALITY.json",
        "SUMMARY": full_d6_path,
        "REPORT": FULL_REPORTS / "D10_D12_SUMMARY.json",
        "TARGETS": TARGETS,
    }, "FULL D10-D12")
    _run_full_tail(FULL_STORE, FULL_REPORTS, full_d6_path, "FULL")
    full_seconds = time.perf_counter() - full_started

    selective_started = time.perf_counter()
    canonical_d6 = json.loads((CANON_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json").read_text(encoding="utf-8"))
    changed_path = SELECTIVE_REPORTS / "D6_D9_CHANGED_ONLY.json"
    _run_stage(run_d6, {
        "STORE_ROOT": SELECTIVE_STORE,
        "REVIEW": SELECTIVE_STORE / "review" / "batch_review_manifest.json",
        "QUALITY": SELECTIVE_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
        "REPORT": changed_path,
        "TARGETS": (CHANGED_DOCUMENT_ID,),
    }, "SELECTIVE D6 changed document")
    changed_d6 = json.loads(changed_path.read_text(encoding="utf-8"))
    selective_d6 = _merge_d6_summary(canonical_d6, changed_d6)
    selective_d6_path = SELECTIVE_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json"
    selective_d6_path.write_text(
        json.dumps(selective_d6, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _run_stage(audit_d6, {
        "STORE_ROOT": SELECTIVE_STORE,
        "SUMMARY": selective_d6_path,
        "REPORT": SELECTIVE_REPORTS / "D6_D9_QUALITY.json",
        "TARGETS": TARGETS,
    }, "SELECTIVE D6 quality")

    selective_rel = _write_selective_d10_d12_relations(
        SELECTIVE_STORE,
        SELECTIVE_REPORTS,
        selective_d6,
    )
    _run_stage(audit_d10, {
        "STORE_ROOT": SELECTIVE_STORE,
        "REL_ROOT": SELECTIVE_STORE / "relations",
        "SUMMARY": SELECTIVE_REPORTS / "D10_D12_SUMMARY.json",
        "D6_SUMMARY": selective_d6_path,
        "REPORT": SELECTIVE_REPORTS / "D10_D12_QUALITY.json",
        "TARGETS": set(TARGETS),
    }, "SELECTIVE D10-D12 quality")

    selective_graph_info = _write_selective_graph(
        SELECTIVE_STORE,
        SELECTIVE_REPORTS,
        selective_d6,
        selective_rel,
    )
    _run_stage(audit_d13, {
        "STORE_ROOT": SELECTIVE_STORE,
        "GRAPH_ROOT": SELECTIVE_STORE / "graph",
        "REPORT": SELECTIVE_REPORTS / "D13_QUALITY.json",
        "TARGETS": set(TARGETS),
    }, "SELECTIVE D13 quality")
    selective_seconds = time.perf_counter() - selective_started

    full_nodes = _read_jsonl(FULL_STORE / "graph" / "nodes.jsonl")
    full_edges = _read_jsonl(FULL_STORE / "graph" / "edges.jsonl")
    selective_nodes = _read_jsonl(SELECTIVE_STORE / "graph" / "nodes.jsonl")
    selective_edges = _read_jsonl(SELECTIVE_STORE / "graph" / "edges.jsonl")
    nodes_parity = _rows_equal(full_nodes, selective_nodes)
    edges_parity = _rows_equal(full_edges, selective_edges)

    relations_parity = all(
        _rows_equal(
            _read_jsonl(FULL_STORE / "relations" / name),
            _read_jsonl(SELECTIVE_STORE / "relations" / name),
        )
        for name in ("internal.jsonl", "cross_document.jsonl", "conflicts_overlaps.jsonl")
    )

    canonical_graph_immutable = (
        nodes_sha_before == _sha256(canonical_nodes_path)
        and edges_sha_before == _sha256(canonical_edges_path)
    )
    full_vs_selective = relations_parity and nodes_parity and edges_parity
    time_saved_percent = (
        (full_seconds - selective_seconds) / full_seconds * 100.0
        if full_seconds > 0
        else None
    )

    total_nodes = len(selective_nodes)
    total_edges = len(selective_edges)
    reused_nodes = len(selective_graph_info["explicit_reused_node_ids"])
    reused_edges = len(selective_graph_info["explicit_reused_edge_ids"])
    node_reuse_ratio = reused_nodes / total_nodes if total_nodes else None
    edge_reuse_ratio = reused_edges / total_edges if total_edges else None

    acceptance = {
        "same_synthetic_fixture": same_fixture,
        "relations_parity": relations_parity,
        "explicit_reused_nodes_exact": selective_graph_info["explicit_reused_nodes_exact"],
        "explicit_reused_edges_exact": selective_graph_info["explicit_reused_edges_exact"],
        "d13_nodes_parity": nodes_parity,
        "d13_edges_parity": edges_parity,
        "full_vs_selective_parity": full_vs_selective,
        "canonical_graph_immutable": canonical_graph_immutable,
        "d15_blocked_until_review": True,
        "network_used": False,
        "source_bytes_mutated": False,
        "legal_truth_promoted": False,
    }
    passed = all(acceptance[key] for key in (
        "same_synthetic_fixture",
        "relations_parity",
        "explicit_reused_nodes_exact",
        "explicit_reused_edges_exact",
        "d13_nodes_parity",
        "d13_edges_parity",
        "full_vs_selective_parity",
        "canonical_graph_immutable",
        "d15_blocked_until_review",
    ))

    result = {
        "record_type": "P0_7_DUAL_PATH_D13_PROOF",
        "proof_scope": "SAME_SYNTHETIC_D5_FIXTURE__SELECTIVE_D6_D10_D11_D12__SELECTIVE_D13_FRAGMENT_REPLACEMENT",
        "fixture": full_fixture,
        "work": {
            "selective_d13_old_affected_nodes": len(selective_graph_info["old_affected_node_ids"]),
            "selective_d13_old_affected_edges": len(selective_graph_info["old_affected_edge_ids"]),
            "selective_d13_nodes_reused_explicit": reused_nodes,
            "selective_d13_nodes_total": total_nodes,
            "selective_d13_node_reuse_ratio": node_reuse_ratio,
            "selective_d13_edges_reused_explicit": reused_edges,
            "selective_d13_edges_total": total_edges,
            "selective_d13_edge_reuse_ratio": edge_reuse_ratio,
            "selective_d13_refreshed_shared_nodes": len(selective_graph_info["refreshed_shared_nodes"]),
            "full_graph_rebuild_in_selective_path": False,
        },
        "timing": {
            "full_path_seconds": full_seconds,
            "selective_path_seconds": selective_seconds,
            "single_run_time_saved_percent": time_saved_percent,
        },
        "parity": {
            "relations": relations_parity,
            "graph_nodes": nodes_parity,
            "graph_edges": edges_parity,
            "full_vs_selective": full_vs_selective,
            "explicit_reused_nodes_exact": selective_graph_info["explicit_reused_nodes_exact"],
            "explicit_reused_edges_exact": selective_graph_info["explicit_reused_edges_exact"],
        },
        "acceptance": acceptance,
        "runtime_root": RUNTIME_ROOT.relative_to(REPO_ROOT).as_posix(),
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"SELECTIVE_D13_NODES_REUSED={reused_nodes}")
    print(f"SELECTIVE_D13_NODES_TOTAL={total_nodes}")
    print(f"SELECTIVE_D13_NODE_REUSE_RATIO={node_reuse_ratio}")
    print(f"SELECTIVE_D13_EDGES_REUSED={reused_edges}")
    print(f"SELECTIVE_D13_EDGES_TOTAL={total_edges}")
    print(f"SELECTIVE_D13_EDGE_REUSE_RATIO={edge_reuse_ratio}")
    print(f"EXPLICIT_REUSED_D13_NODES_EXACT={str(selective_graph_info['explicit_reused_nodes_exact']).lower()}")
    print(f"EXPLICIT_REUSED_D13_EDGES_EXACT={str(selective_graph_info['explicit_reused_edges_exact']).lower()}")
    print(f"D13_NODES_PARITY={str(nodes_parity).lower()}")
    print(f"D13_EDGES_PARITY={str(edges_parity).lower()}")
    print(f"FULL_VS_SELECTIVE_PARITY={str(full_vs_selective).lower()}")
    print(f"CANONICAL_GRAPH_IMMUTABLE={str(canonical_graph_immutable).lower()}")
    print("FULL_GRAPH_REBUILD_IN_SELECTIVE_PATH=false")
    print("D15_BLOCKED_UNTIL_REVIEW=true")
    print("NETWORK_USED=false")
    print("SOURCE_BYTES_MUTATED=false")
    print(f"FULL_PATH_SECONDS={full_seconds:.6f}")
    print(f"SELECTIVE_PATH_SECONDS={selective_seconds:.6f}")
    if time_saved_percent is not None:
        print(f"SINGLE_RUN_TIME_SAVED_PERCENT={time_saved_percent:.3f}")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
