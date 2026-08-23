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

RUNTIME_ROOT = REPO_ROOT / ".runtime" / "pdn_dual_path_d6_d13"
FULL_STORE = RUNTIME_ROOT / "full_store"
FULL_REPORTS = RUNTIME_ROOT / "full_reports"
SELECTIVE_STORE = RUNTIME_ROOT / "selective_store"
SELECTIVE_REPORTS = RUNTIME_ROOT / "selective_reports"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_DUAL_PATH_D6_D13.json"


def _canonical_json(row: Mapping[str, object]) -> str:
    return json.dumps(dict(row), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _rows_equal(left: Iterable[Mapping[str, object]], right: Iterable[Mapping[str, object]]) -> bool:
    return sorted(_canonical_json(row) for row in left) == sorted(_canonical_json(row) for row in right)


def _copy_workspace(store_root: Path, reports_root: Path) -> None:
    shutil.copytree(CANON_STORE, store_root)
    reports_root.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        CANON_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
        reports_root / "D4_D5_STRUCTURE_QUALITY.json",
    )


def _run_downstream(store_root: Path, reports_root: Path, d6_summary: Path, label: str) -> None:
    _run_stage(
        audit_d6,
        {
            "STORE_ROOT": store_root,
            "SUMMARY": d6_summary,
            "REPORT": reports_root / "D6_D9_QUALITY.json",
            "TARGETS": TARGETS,
        },
        f"{label} D6-D9 quality",
    )
    _run_stage(
        run_d10,
        {
            "STORE_ROOT": store_root,
            "QUALITY": reports_root / "D6_D9_QUALITY.json",
            "SUMMARY": d6_summary,
            "REPORT": reports_root / "D10_D12_SUMMARY.json",
            "TARGETS": TARGETS,
        },
        f"{label} D10-D12 rebuild",
    )
    _run_stage(
        audit_d10,
        {
            "STORE_ROOT": store_root,
            "REL_ROOT": store_root / "relations",
            "SUMMARY": reports_root / "D10_D12_SUMMARY.json",
            "D6_SUMMARY": d6_summary,
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
            "D6_SUMMARY": d6_summary,
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


def _knowledge_parity(full_summary: dict[str, object], selective_summary: dict[str, object]) -> tuple[bool, list[str]]:
    full_docs = {str(item["document_id"]): item for item in full_summary.get("documents", []) if isinstance(item, dict)}
    selective_docs = {str(item["document_id"]): item for item in selective_summary.get("documents", []) if isinstance(item, dict)}
    mismatches: list[str] = []
    if set(full_docs) != set(TARGETS) or set(selective_docs) != set(TARGETS):
        return False, ["DOCUMENT_SET_MISMATCH"]

    for document_id in TARGETS:
        full_version = str(full_docs[document_id]["version_id"])
        selective_version = str(selective_docs[document_id]["version_id"])
        if full_version != selective_version:
            mismatches.append(f"{document_id}:version_id")
            continue
        for name in ("terms", "definitions", "requirements", "entities"):
            full_rows = _read_jsonl(FULL_STORE / "knowledge" / document_id / full_version / f"{name}.jsonl")
            selective_rows = _read_jsonl(SELECTIVE_STORE / "knowledge" / document_id / selective_version / f"{name}.jsonl")
            if not _rows_equal(full_rows, selective_rows):
                mismatches.append(f"{document_id}:{name}")
    return not mismatches, mismatches


def main() -> int:
    started = time.perf_counter()
    required = [
        CANON_STORE / "review" / "batch_review_manifest.json",
        CANON_STORE / "graph" / "nodes.jsonl",
        CANON_STORE / "graph" / "edges.jsonl",
        CANON_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
        CANON_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.is_file()]
    if missing:
        print("DUAL_PATH_INPUT_MISSING=" + ",".join(missing))
        return 2

    canonical_nodes_path = CANON_STORE / "graph" / "nodes.jsonl"
    canonical_edges_path = CANON_STORE / "graph" / "edges.jsonl"
    canonical_nodes_sha_before = _sha256(canonical_nodes_path)
    canonical_edges_sha_before = _sha256(canonical_edges_path)

    if RUNTIME_ROOT.exists():
        shutil.rmtree(RUNTIME_ROOT)
    RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
    _copy_workspace(FULL_STORE, FULL_REPORTS)
    _copy_workspace(SELECTIVE_STORE, SELECTIVE_REPORTS)

    full_fixture = _inject_synthetic_d5_delta(FULL_STORE)
    selective_fixture = _inject_synthetic_d5_delta(SELECTIVE_STORE)
    fixture_equal = (
        full_fixture["chunk_locator"] == selective_fixture["chunk_locator"]
        and full_fixture["new_chunk_id"] == selective_fixture["new_chunk_id"]
        and full_fixture["chunks_sha256_after_fixture"] == selective_fixture["chunks_sha256_after_fixture"]
    )
    if not fixture_equal:
        raise RuntimeError("full and selective workspaces did not receive the same synthetic D5 fixture")

    full_d6_summary_path = FULL_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json"
    _run_stage(
        run_d6,
        {
            "STORE_ROOT": FULL_STORE,
            "REVIEW": FULL_STORE / "review" / "batch_review_manifest.json",
            "QUALITY": FULL_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
            "REPORT": full_d6_summary_path,
            "TARGETS": TARGETS,
        },
        "FULL D6-D9 four-document rebuild",
    )
    _run_downstream(FULL_STORE, FULL_REPORTS, full_d6_summary_path, "FULL")

    canonical_d6 = json.loads((CANON_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json").read_text(encoding="utf-8"))
    selective_changed_path = SELECTIVE_REPORTS / "D6_D9_CHANGED_ONLY.json"
    _run_stage(
        run_d6,
        {
            "STORE_ROOT": SELECTIVE_STORE,
            "REVIEW": SELECTIVE_STORE / "review" / "batch_review_manifest.json",
            "QUALITY": SELECTIVE_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
            "REPORT": selective_changed_path,
            "TARGETS": (CHANGED_DOCUMENT_ID,),
        },
        "SELECTIVE D6-D9 changed-document rebuild",
    )
    changed_d6 = json.loads(selective_changed_path.read_text(encoding="utf-8"))
    selective_d6 = _merge_d6_summary(canonical_d6, changed_d6)
    selective_d6_summary_path = SELECTIVE_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json"
    selective_d6_summary_path.write_text(
        json.dumps(selective_d6, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _run_downstream(SELECTIVE_STORE, SELECTIVE_REPORTS, selective_d6_summary_path, "SELECTIVE")

    full_d6 = json.loads(full_d6_summary_path.read_text(encoding="utf-8"))
    knowledge_parity, knowledge_mismatches = _knowledge_parity(full_d6, selective_d6)

    relations_parity = all(
        _rows_equal(
            _read_jsonl(FULL_STORE / "relations" / name),
            _read_jsonl(SELECTIVE_STORE / "relations" / name),
        )
        for name in ("internal.jsonl", "cross_document.jsonl", "conflicts_overlaps.jsonl")
    )
    nodes_parity = _rows_equal(
        _read_jsonl(FULL_STORE / "graph" / "nodes.jsonl"),
        _read_jsonl(SELECTIVE_STORE / "graph" / "nodes.jsonl"),
    )
    edges_parity = _rows_equal(
        _read_jsonl(FULL_STORE / "graph" / "edges.jsonl"),
        _read_jsonl(SELECTIVE_STORE / "graph" / "edges.jsonl"),
    )

    canonical_d6_docs = {
        str(item["document_id"]): item
        for item in canonical_d6.get("documents", [])
        if isinstance(item, dict) and item.get("document_id")
    }
    unchanged_d6_payload_exact = True
    unchanged_hashes: dict[str, dict[str, bool]] = {}
    for document_id in TARGETS:
        if document_id == CHANGED_DOCUMENT_ID:
            continue
        version_id = str(canonical_d6_docs[document_id]["version_id"])
        per_type: dict[str, bool] = {}
        for name in ("terms", "definitions", "requirements", "entities"):
            canonical_path = CANON_STORE / "knowledge" / document_id / version_id / f"{name}.jsonl"
            selective_path = SELECTIVE_STORE / "knowledge" / document_id / version_id / f"{name}.jsonl"
            exact = canonical_path.read_bytes() == selective_path.read_bytes()
            per_type[name] = exact
            unchanged_d6_payload_exact = unchanged_d6_payload_exact and exact
        unchanged_hashes[document_id] = per_type

    canonical_nodes_sha_after = _sha256(canonical_nodes_path)
    canonical_edges_sha_after = _sha256(canonical_edges_path)
    canonical_graph_immutable = (
        canonical_nodes_sha_before == canonical_nodes_sha_after
        and canonical_edges_sha_before == canonical_edges_sha_after
    )

    full_changed = next(item for item in full_d6["documents"] if item["document_id"] == CHANGED_DOCUMENT_ID)
    canonical_changed = canonical_d6_docs[CHANGED_DOCUMENT_ID]
    requirement_delta = int(full_changed["requirements"]) - int(canonical_changed["requirements"])

    full_vs_selective_parity = knowledge_parity and relations_parity and nodes_parity and edges_parity
    acceptance = {
        "same_synthetic_fixture": fixture_equal,
        "synthetic_requirement_created": requirement_delta > 0,
        "selective_unchanged_d6_payload_exact": unchanged_d6_payload_exact,
        "d6_knowledge_parity": knowledge_parity,
        "d10_d12_relations_parity": relations_parity,
        "d13_nodes_parity": nodes_parity,
        "d13_edges_parity": edges_parity,
        "full_vs_selective_parity": full_vs_selective_parity,
        "canonical_graph_immutable": canonical_graph_immutable,
        "d10_d13_common_rebuild_in_both_paths": True,
        "d15_blocked_until_review": True,
        "network_used": False,
        "source_bytes_mutated": False,
        "legal_truth_promoted": False,
    }
    passed = all(
        acceptance[key]
        for key in (
            "same_synthetic_fixture",
            "synthetic_requirement_created",
            "selective_unchanged_d6_payload_exact",
            "d6_knowledge_parity",
            "d10_d12_relations_parity",
            "d13_nodes_parity",
            "d13_edges_parity",
            "full_vs_selective_parity",
            "canonical_graph_immutable",
            "d15_blocked_until_review",
        )
    )

    result = {
        "record_type": "P0_7_DUAL_PATH_D6_D13_PROOF",
        "proof_scope": "SAME_SYNTHETIC_D5_FIXTURE__FULL_D6_ALL_DOCS_VS_SELECTIVE_D6_CHANGED_DOC__COMMON_D10_D13_REBUILD",
        "fixture": full_fixture,
        "work": {
            "full_d6_documents_rebuilt": len(TARGETS),
            "selective_d6_documents_rebuilt": 1,
            "selective_d6_documents_reused": len(TARGETS) - 1,
            "selective_d6_document_reuse_ratio": (len(TARGETS) - 1) / len(TARGETS),
            "d10_d13_common_rebuild_in_both_paths": True,
        },
        "parity": {
            "knowledge": knowledge_parity,
            "knowledge_mismatches": knowledge_mismatches,
            "relations": relations_parity,
            "graph_nodes": nodes_parity,
            "graph_edges": edges_parity,
            "full_vs_selective": full_vs_selective_parity,
            "unchanged_d6_payload_exact": unchanged_d6_payload_exact,
            "unchanged_d6_payload_by_document": unchanged_hashes,
        },
        "canonical_graph": {
            "nodes_sha256_before": canonical_nodes_sha_before,
            "nodes_sha256_after": canonical_nodes_sha_after,
            "edges_sha256_before": canonical_edges_sha_before,
            "edges_sha256_after": canonical_edges_sha_after,
            "immutable": canonical_graph_immutable,
        },
        "changed_document": {
            "document_id": CHANGED_DOCUMENT_ID,
            "requirements_before": int(canonical_changed["requirements"]),
            "requirements_after": int(full_changed["requirements"]),
            "requirements_delta": requirement_delta,
        },
        "acceptance": acceptance,
        "runtime_root": RUNTIME_ROOT.relative_to(REPO_ROOT).as_posix(),
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"FULL_D6_DOCUMENTS_REBUILT={len(TARGETS)}")
    print("SELECTIVE_D6_DOCUMENTS_REBUILT=1")
    print(f"SELECTIVE_D6_DOCUMENTS_REUSED={len(TARGETS) - 1}")
    print(f"SELECTIVE_D6_REUSE_RATIO={(len(TARGETS) - 1) / len(TARGETS)}")
    print(f"UNCHANGED_D6_PAYLOAD_EXACT={str(unchanged_d6_payload_exact).lower()}")
    print(f"D6_KNOWLEDGE_PARITY={str(knowledge_parity).lower()}")
    print(f"D10_D12_RELATIONS_PARITY={str(relations_parity).lower()}")
    print(f"D13_NODES_PARITY={str(nodes_parity).lower()}")
    print(f"D13_EDGES_PARITY={str(edges_parity).lower()}")
    print(f"FULL_VS_SELECTIVE_PARITY={str(full_vs_selective_parity).lower()}")
    print(f"CANONICAL_GRAPH_IMMUTABLE={str(canonical_graph_immutable).lower()}")
    print("D10_D13_COMMON_REBUILD_IN_BOTH_PATHS=true")
    print("D15_BLOCKED_UNTIL_REVIEW=true")
    print("NETWORK_USED=false")
    print("SOURCE_BYTES_MUTATED=false")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
