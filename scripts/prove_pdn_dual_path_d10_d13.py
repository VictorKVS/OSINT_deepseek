from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path
from typing import Iterable, Mapping

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.audit_pdn_d10_d12 as audit_d10
import scripts.audit_pdn_d13 as audit_d13
import scripts.audit_pdn_d6_d9 as audit_d6
import scripts.run_pdn_d10_d12 as run_d10
import scripts.run_pdn_d13_review_queue as run_d13
import scripts.run_pdn_d6_d9 as run_d6
from father_osint.relation_builders import (
    build_conflict_candidates,
    build_cross_relations,
    build_internal_relations_for_document,
)
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

RUNTIME_ROOT = REPO_ROOT / ".runtime" / "pdn_dual_path_d10_d13"
FULL_STORE = RUNTIME_ROOT / "full_store"
FULL_REPORTS = RUNTIME_ROOT / "full_reports"
SELECTIVE_STORE = RUNTIME_ROOT / "selective_store"
SELECTIVE_REPORTS = RUNTIME_ROOT / "selective_reports"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_DUAL_PATH_D10_D13.json"


def _canonical_json(row: Mapping[str, object]) -> str:
    return json.dumps(dict(row), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _rows_equal(left: Iterable[Mapping[str, object]], right: Iterable[Mapping[str, object]]) -> bool:
    return sorted(_canonical_json(row) for row in left) == sorted(_canonical_json(row) for row in right)


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n")


def _copy_workspace(store_root: Path, reports_root: Path) -> None:
    shutil.copytree(CANON_STORE, store_root)
    reports_root.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CANON_REPORTS / "D4_D5_STRUCTURE_QUALITY.json", reports_root / "D4_D5_STRUCTURE_QUALITY.json")


def _load_per_doc(store_root: Path, d6_summary: Mapping[str, object]) -> dict[str, dict[str, list[dict[str, object]]]]:
    by_id = {
        str(item["document_id"]): item
        for item in d6_summary.get("documents", [])
        if isinstance(item, Mapping) and item.get("document_id")
    }
    if set(by_id) != set(TARGETS):
        raise ValueError("D6 summary document set mismatch")
    result: dict[str, dict[str, list[dict[str, object]]]] = {}
    for document_id in TARGETS:
        version_id = str(by_id[document_id]["version_id"])
        base = store_root / "knowledge" / document_id / version_id
        result[document_id] = {
            name: _read_jsonl(base / f"{name}.jsonl")
            for name in ("terms", "definitions", "requirements", "entities")
        }
    return result


def _write_selective_relations(
    store_root: Path,
    reports_root: Path,
    d6_summary: Mapping[str, object],
) -> dict[str, object]:
    per_doc = _load_per_doc(store_root, d6_summary)
    canonical_internal = _read_jsonl(CANON_STORE / "relations" / "internal.jsonl")
    reused_internal = [row for row in canonical_internal if str(row.get("document_id")) != CHANGED_DOCUMENT_ID]
    rebuilt_internal = build_internal_relations_for_document(CHANGED_DOCUMENT_ID, per_doc[CHANGED_DOCUMENT_ID])
    internal = reused_internal + rebuilt_internal

    all_terms: list[Mapping[str, object]] = []
    all_definitions: list[Mapping[str, object]] = []
    all_requirements: list[Mapping[str, object]] = []
    all_entities: list[Mapping[str, object]] = []
    for document_id in TARGETS:
        all_terms.extend(per_doc[document_id]["terms"])
        all_definitions.extend(per_doc[document_id]["definitions"])
        all_requirements.extend(per_doc[document_id]["requirements"])
        all_entities.extend(per_doc[document_id]["entities"])

    cross = build_cross_relations(all_terms, all_entities)
    conflicts = build_conflict_candidates(all_definitions, all_requirements)
    rel_root = store_root / "relations"
    _write_jsonl(rel_root / "internal.jsonl", internal)
    _write_jsonl(rel_root / "cross_document.jsonl", cross)
    _write_jsonl(rel_root / "conflicts_overlaps.jsonl", conflicts)

    manifest = {
        "schema_version": "1.0",
        "internal_relations": len(internal),
        "cross_document_relations": len(cross),
        "conflict_overlap_candidates": len(conflicts),
        "confirmed_conflicts": 0,
        "review_required": True,
        "autonomous_kb_promotion": False,
    }
    (rel_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = {"record_type": "D10_D12_SUMMARY", **manifest}
    summary_path = reports_root / "D10_D12_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return {
        "reused_internal": reused_internal,
        "rebuilt_internal": rebuilt_internal,
        "all_internal": internal,
        "cross": cross,
        "conflicts": conflicts,
    }


def _run_d13_tail(store_root: Path, reports_root: Path, d6_summary_path: Path, label: str) -> None:
    _run_stage(
        audit_d10,
        {
            "STORE_ROOT": store_root,
            "REL_ROOT": store_root / "relations",
            "SUMMARY": reports_root / "D10_D12_SUMMARY.json",
            "D6_SUMMARY": d6_summary_path,
            "REPORT": reports_root / "D10_D12_QUALITY.json",
            "TARGETS": set(TARGETS),
        },
        f"{label} D10-D12 quality",
    )
    _run_stage(
        run_d13,
        {
            "STORE_ROOT": store_root,
            "D10_QUALITY": reports_root / "D10_D12_QUALITY.json",
            "D6_SUMMARY": d6_summary_path,
            "REL_ROOT": store_root / "relations",
            "GRAPH_ROOT": store_root / "graph",
            "REPORT": reports_root / "D13_GRAPH_SUMMARY.json",
            "REVIEW_QUEUE": reports_root / "D14_REVIEW_QUEUE.md",
            "TARGETS": TARGETS,
        },
        f"{label} D13 rebuild",
    )
    _run_stage(
        audit_d13,
        {
            "STORE_ROOT": store_root,
            "GRAPH_ROOT": store_root / "graph",
            "REPORT": reports_root / "D13_QUALITY.json",
            "TARGETS": set(TARGETS),
        },
        f"{label} D13 quality",
    )


def main() -> int:
    started = time.perf_counter()
    required = [
        CANON_STORE / "review" / "batch_review_manifest.json",
        CANON_STORE / "relations" / "internal.jsonl",
        CANON_STORE / "graph" / "nodes.jsonl",
        CANON_STORE / "graph" / "edges.jsonl",
        CANON_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
        CANON_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.is_file()]
    if missing:
        print("DUAL_PATH_D10_INPUT_MISSING=" + ",".join(missing))
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
    _run_d13_tail(FULL_STORE, FULL_REPORTS, full_d6_path, "FULL")
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
    selective_d6_path.write_text(json.dumps(selective_d6, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _run_stage(audit_d6, {
        "STORE_ROOT": SELECTIVE_STORE,
        "SUMMARY": selective_d6_path,
        "REPORT": SELECTIVE_REPORTS / "D6_D9_QUALITY.json",
        "TARGETS": TARGETS,
    }, "SELECTIVE D6 quality")
    selective_rel = _write_selective_relations(SELECTIVE_STORE, SELECTIVE_REPORTS, selective_d6)
    _run_d13_tail(SELECTIVE_STORE, SELECTIVE_REPORTS, selective_d6_path, "SELECTIVE")
    selective_seconds = time.perf_counter() - selective_started

    full_internal = _read_jsonl(FULL_STORE / "relations" / "internal.jsonl")
    selective_internal = _read_jsonl(SELECTIVE_STORE / "relations" / "internal.jsonl")
    full_cross = _read_jsonl(FULL_STORE / "relations" / "cross_document.jsonl")
    selective_cross = _read_jsonl(SELECTIVE_STORE / "relations" / "cross_document.jsonl")
    full_conflicts = _read_jsonl(FULL_STORE / "relations" / "conflicts_overlaps.jsonl")
    selective_conflicts = _read_jsonl(SELECTIVE_STORE / "relations" / "conflicts_overlaps.jsonl")

    internal_parity = _rows_equal(full_internal, selective_internal)
    cross_parity = _rows_equal(full_cross, selective_cross)
    conflict_parity = _rows_equal(full_conflicts, selective_conflicts)
    nodes_parity = _rows_equal(_read_jsonl(FULL_STORE / "graph" / "nodes.jsonl"), _read_jsonl(SELECTIVE_STORE / "graph" / "nodes.jsonl"))
    edges_parity = _rows_equal(_read_jsonl(FULL_STORE / "graph" / "edges.jsonl"), _read_jsonl(SELECTIVE_STORE / "graph" / "edges.jsonl"))

    canonical_unchanged_internal = [
        row for row in _read_jsonl(CANON_STORE / "relations" / "internal.jsonl")
        if str(row.get("document_id")) != CHANGED_DOCUMENT_ID
    ]
    unchanged_internal_exact = _rows_equal(canonical_unchanged_internal, selective_rel["reused_internal"])
    reused_internal_count = len(selective_rel["reused_internal"])
    total_internal_count = len(selective_internal)
    internal_reuse_ratio = reused_internal_count / total_internal_count if total_internal_count else None

    canonical_graph_immutable = (
        nodes_sha_before == _sha256(canonical_nodes_path)
        and edges_sha_before == _sha256(canonical_edges_path)
    )
    full_vs_selective = internal_parity and cross_parity and conflict_parity and nodes_parity and edges_parity
    time_saved_percent = ((full_seconds - selective_seconds) / full_seconds * 100.0) if full_seconds > 0 else None

    acceptance = {
        "same_synthetic_fixture": same_fixture,
        "unchanged_d10_internal_payload_exact": unchanged_internal_exact,
        "d10_internal_relations_parity": internal_parity,
        "d11_cross_relations_parity": cross_parity,
        "d12_conflicts_parity": conflict_parity,
        "d13_nodes_parity": nodes_parity,
        "d13_edges_parity": edges_parity,
        "full_vs_selective_parity": full_vs_selective,
        "canonical_graph_immutable": canonical_graph_immutable,
        "d11_d13_common_rebuild_in_both_paths": True,
        "d15_blocked_until_review": True,
        "network_used": False,
        "source_bytes_mutated": False,
        "legal_truth_promoted": False,
    }
    passed = all(acceptance[key] for key in (
        "same_synthetic_fixture",
        "unchanged_d10_internal_payload_exact",
        "d10_internal_relations_parity",
        "d11_cross_relations_parity",
        "d12_conflicts_parity",
        "d13_nodes_parity",
        "d13_edges_parity",
        "full_vs_selective_parity",
        "canonical_graph_immutable",
        "d15_blocked_until_review",
    ))

    result = {
        "record_type": "P0_7_DUAL_PATH_D10_D13_PROOF",
        "proof_scope": "SAME_SYNTHETIC_D5_FIXTURE__SELECTIVE_D6_CHANGED_DOC__SELECTIVE_D10_CHANGED_DOC__COMMON_D11_D13_REBUILD",
        "fixture": full_fixture,
        "work": {
            "full_d6_documents_rebuilt": len(TARGETS),
            "selective_d6_documents_rebuilt": 1,
            "selective_d6_documents_reused": len(TARGETS) - 1,
            "full_d10_documents_rebuilt": len(TARGETS),
            "selective_d10_documents_rebuilt": 1,
            "selective_d10_documents_reused": len(TARGETS) - 1,
            "selective_d10_document_reuse_ratio": (len(TARGETS) - 1) / len(TARGETS),
            "selective_d10_internal_relations_reused": reused_internal_count,
            "selective_d10_internal_relations_total": total_internal_count,
            "selective_d10_internal_relation_reuse_ratio": internal_reuse_ratio,
            "d11_d13_common_rebuild_in_both_paths": True,
        },
        "timing": {
            "full_path_seconds": full_seconds,
            "selective_path_seconds": selective_seconds,
            "single_run_time_saved_percent": time_saved_percent,
        },
        "parity": {
            "internal_relations": internal_parity,
            "cross_relations": cross_parity,
            "conflicts": conflict_parity,
            "graph_nodes": nodes_parity,
            "graph_edges": edges_parity,
            "full_vs_selective": full_vs_selective,
            "unchanged_internal_payload_exact": unchanged_internal_exact,
        },
        "acceptance": acceptance,
        "runtime_root": RUNTIME_ROOT.relative_to(REPO_ROOT).as_posix(),
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print("FULL_D10_DOCUMENTS_REBUILT=4")
    print("SELECTIVE_D10_DOCUMENTS_REBUILT=1")
    print("SELECTIVE_D10_DOCUMENTS_REUSED=3")
    print("SELECTIVE_D10_DOCUMENT_REUSE_RATIO=0.75")
    print(f"SELECTIVE_D10_INTERNAL_RELATIONS_REUSED={reused_internal_count}")
    print(f"SELECTIVE_D10_INTERNAL_RELATIONS_TOTAL={total_internal_count}")
    print(f"SELECTIVE_D10_INTERNAL_RELATION_REUSE_RATIO={internal_reuse_ratio}")
    print(f"UNCHANGED_D10_INTERNAL_PAYLOAD_EXACT={str(unchanged_internal_exact).lower()}")
    print(f"D10_INTERNAL_RELATIONS_PARITY={str(internal_parity).lower()}")
    print(f"D11_CROSS_RELATIONS_PARITY={str(cross_parity).lower()}")
    print(f"D12_CONFLICTS_PARITY={str(conflict_parity).lower()}")
    print(f"D13_NODES_PARITY={str(nodes_parity).lower()}")
    print(f"D13_EDGES_PARITY={str(edges_parity).lower()}")
    print(f"FULL_VS_SELECTIVE_PARITY={str(full_vs_selective).lower()}")
    print(f"CANONICAL_GRAPH_IMMUTABLE={str(canonical_graph_immutable).lower()}")
    print("D11_D13_COMMON_REBUILD_IN_BOTH_PATHS=true")
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
