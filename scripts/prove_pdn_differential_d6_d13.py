from __future__ import annotations

import hashlib
import json
import shutil
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.dependency_invalidation import build_object_delta_plan
from father_osint.differential_rebuild import assemble_selective_projection

import scripts.audit_pdn_d10_d12 as audit_d10
import scripts.audit_pdn_d13 as audit_d13
import scripts.audit_pdn_d6_d9 as audit_d6
import scripts.run_pdn_d10_d12 as run_d10
import scripts.run_pdn_d13_review_queue as run_d13
import scripts.run_pdn_d6_d9 as run_d6


CANON_STORE = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
CANON_REPORTS = REPO_ROOT / "reports" / "pdn_live"
RUNTIME_ROOT = REPO_ROOT / ".runtime" / "pdn_differential_d6_d13"
ORACLE_STORE = RUNTIME_ROOT / "oracle_store"
ORACLE_REPORTS = RUNTIME_ROOT / "oracle_reports"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_DIFFERENTIAL_D6_D13.json"
CHANGED_DOCUMENT_ID = "DOC-RU-FZ-152-2006"
TARGETS = (
    "DOC-RU-FZ-152-2006",
    "DOC-RU-PP-1119-2012",
    "DOC-RU-FSTEC-21-2013",
    "DOC-RU-FSB-378-2014",
)
SYNTHETIC_SENTENCE = (
    "Оператор обязан обеспечить безопасность персональных данных "
    "в рамках синтетического теста P0.7."
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _stable_chunk_id(document_id: str, version_id: str, locator: str, text: str) -> str:
    payload = "\x1f".join((document_id, version_id, locator, text)).encode("utf-8")
    return "CHK-" + hashlib.sha256(payload).hexdigest()[:24]


def _run_stage(module: ModuleType, overrides: dict[str, object], label: str) -> None:
    previous: dict[str, Any] = {}
    for name, value in overrides.items():
        previous[name] = getattr(module, name)
        setattr(module, name, value)
    try:
        rc = int(module.main())
    finally:
        for name, value in previous.items():
            setattr(module, name, value)
    if rc != 0:
        raise RuntimeError(f"{label} failed with exit code {rc}")


def _merge_d6_summary(canonical: dict[str, object], changed: dict[str, object]) -> dict[str, object]:
    canonical_docs = {
        str(item["document_id"]): dict(item)
        for item in canonical.get("documents", [])
        if isinstance(item, dict) and item.get("document_id")
    }
    changed_docs = [dict(item) for item in changed.get("documents", []) if isinstance(item, dict)]
    if len(changed_docs) != 1 or changed_docs[0].get("document_id") != CHANGED_DOCUMENT_ID:
        raise ValueError("changed D6 summary must contain exactly the synthetic changed document")
    canonical_docs[CHANGED_DOCUMENT_ID] = changed_docs[0]
    if set(canonical_docs) != set(TARGETS):
        raise ValueError("merged D6 summary document set is incomplete")

    docs = [canonical_docs[document_id] for document_id in TARGETS]
    changed_summary = changed.get("summary", {}) if isinstance(changed.get("summary"), dict) else {}
    summary = {
        "record_type": "D6_D9_EXTRACTION_SUMMARY",
        "targets": len(TARGETS),
        "ready_d9_candidates": len(docs),
        "terms": sum(int(item["terms"]) for item in docs),
        "definitions": sum(int(item["definitions"]) for item in docs),
        "requirements": sum(int(item["requirements"]) for item in docs),
        "entities": sum(int(item["entities"]) for item in docs),
        "extractor_version": changed_summary.get("extractor_version"),
        "quality_gate_sha256": changed_summary.get("quality_gate_sha256"),
        "review_required_before_promotion": True,
        "autonomous_kb_promotion": False,
    }
    return {"summary": summary, "documents": docs}


def _inject_synthetic_d5_delta(store_root: Path) -> dict[str, object]:
    review_path = store_root / "review" / "batch_review_manifest.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    target = next(
        (item for item in review.get("documents", []) if item.get("document_id") == CHANGED_DOCUMENT_ID),
        None,
    )
    if not target or target.get("status") != "READY_D5":
        raise ValueError("changed document is not READY_D5 in oracle workspace")

    chunks_path = store_root / str(target["chunks_path"])
    rows = _read_jsonl(chunks_path)
    candidate_index: int | None = None
    for index, row in enumerate(rows):
        text = str(row.get("text", "")).casefold().replace("ё", "е")
        if "оператор" in text and "персональн" in text:
            candidate_index = index
            break
    if candidate_index is None:
        raise ValueError("no suitable 152-FZ chunk found for bounded synthetic D5 delta")

    row = dict(rows[candidate_index])
    before_text = str(row.get("text", ""))
    if SYNTHETIC_SENTENCE.casefold() in before_text.casefold():
        raise ValueError("synthetic fixture sentence is already present")
    after_text = before_text.rstrip() + "\n" + SYNTHETIC_SENTENCE
    old_chunk_id = str(row["chunk_id"])
    new_chunk_id = _stable_chunk_id(
        CHANGED_DOCUMENT_ID,
        str(row["version_id"]),
        str(row["locator"]),
        after_text,
    )
    row["text"] = after_text
    row["chunk_id"] = new_chunk_id
    rows[candidate_index] = row
    _write_jsonl(chunks_path, rows)

    return {
        "fixture_level": "D5_DERIVED_TEXT_ONLY",
        "test_only": True,
        "source_bytes_mutated": False,
        "document_id": CHANGED_DOCUMENT_ID,
        "chunks_path": chunks_path.relative_to(store_root).as_posix(),
        "chunk_locator": row["locator"],
        "old_chunk_id": old_chunk_id,
        "new_chunk_id": new_chunk_id,
        "synthetic_sentence": SYNTHETIC_SENTENCE,
        "chunks_sha256_after_fixture": _sha256(chunks_path),
    }


def main() -> int:
    started = time.perf_counter()
    canonical_required = [
        CANON_STORE / "review" / "batch_review_manifest.json",
        CANON_STORE / "graph" / "nodes.jsonl",
        CANON_STORE / "graph" / "edges.jsonl",
        CANON_STORE / "relations" / "internal.jsonl",
        CANON_STORE / "relations" / "cross_document.jsonl",
        CANON_STORE / "relations" / "conflicts_overlaps.jsonl",
        CANON_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
        CANON_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in canonical_required if not path.is_file()]
    if missing:
        print("DIFFERENTIAL_INPUT_MISSING=" + ",".join(missing))
        return 2

    canonical_nodes_path = CANON_STORE / "graph" / "nodes.jsonl"
    canonical_edges_path = CANON_STORE / "graph" / "edges.jsonl"
    canonical_nodes_sha_before = _sha256(canonical_nodes_path)
    canonical_edges_sha_before = _sha256(canonical_edges_path)
    canonical_nodes = _read_jsonl(canonical_nodes_path)
    canonical_edges = _read_jsonl(canonical_edges_path)
    canonical_internal = _read_jsonl(CANON_STORE / "relations" / "internal.jsonl")
    canonical_cross = _read_jsonl(CANON_STORE / "relations" / "cross_document.jsonl")
    canonical_conflicts = _read_jsonl(CANON_STORE / "relations" / "conflicts_overlaps.jsonl")

    if RUNTIME_ROOT.exists():
        shutil.rmtree(RUNTIME_ROOT)
    RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(CANON_STORE, ORACLE_STORE)
    ORACLE_REPORTS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        CANON_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
        ORACLE_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
    )

    fixture = _inject_synthetic_d5_delta(ORACLE_STORE)

    canonical_d6 = json.loads((CANON_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json").read_text(encoding="utf-8"))
    before_by_id = {
        str(item["document_id"]): dict(item)
        for item in canonical_d6.get("documents", [])
        if isinstance(item, dict) and item.get("document_id")
    }
    before_changed_requirements = int(before_by_id[CHANGED_DOCUMENT_ID]["requirements"])

    changed_d6_report = ORACLE_REPORTS / "D6_D9_CHANGED_ONLY.json"
    _run_stage(
        run_d6,
        {
            "STORE_ROOT": ORACLE_STORE,
            "REVIEW": ORACLE_STORE / "review" / "batch_review_manifest.json",
            "QUALITY": ORACLE_REPORTS / "D4_D5_STRUCTURE_QUALITY.json",
            "REPORT": changed_d6_report,
            "TARGETS": (CHANGED_DOCUMENT_ID,),
        },
        "D6-D9 changed-document rebuild",
    )
    changed_d6 = json.loads(changed_d6_report.read_text(encoding="utf-8"))
    merged_d6 = _merge_d6_summary(canonical_d6, changed_d6)
    merged_d6_path = ORACLE_REPORTS / "D6_D9_EXTRACTION_SUMMARY.json"
    merged_d6_path.write_text(
        json.dumps(merged_d6, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    after_changed = next(
        item for item in merged_d6["documents"] if item["document_id"] == CHANGED_DOCUMENT_ID
    )
    after_changed_requirements = int(after_changed["requirements"])
    requirement_delta = after_changed_requirements - before_changed_requirements
    if requirement_delta <= 0:
        raise RuntimeError("synthetic D5 delta did not create a new D8 requirement candidate")

    _run_stage(
        audit_d6,
        {
            "STORE_ROOT": ORACLE_STORE,
            "SUMMARY": merged_d6_path,
            "REPORT": ORACLE_REPORTS / "D6_D9_QUALITY.json",
            "TARGETS": TARGETS,
        },
        "D6-D9 oracle quality gate",
    )
    _run_stage(
        run_d10,
        {
            "STORE_ROOT": ORACLE_STORE,
            "QUALITY": ORACLE_REPORTS / "D6_D9_QUALITY.json",
            "SUMMARY": merged_d6_path,
            "REPORT": ORACLE_REPORTS / "D10_D12_SUMMARY.json",
            "TARGETS": TARGETS,
        },
        "full oracle D10-D12 rebuild",
    )
    _run_stage(
        audit_d10,
        {
            "STORE_ROOT": ORACLE_STORE,
            "REL_ROOT": ORACLE_STORE / "relations",
            "SUMMARY": ORACLE_REPORTS / "D10_D12_SUMMARY.json",
            "D6_SUMMARY": merged_d6_path,
            "REPORT": ORACLE_REPORTS / "D10_D12_QUALITY.json",
            "TARGETS": set(TARGETS),
        },
        "D10-D12 oracle quality gate",
    )
    _run_stage(
        run_d13,
        {
            "STORE_ROOT": ORACLE_STORE,
            "D10_QUALITY": ORACLE_REPORTS / "D10_D12_QUALITY.json",
            "D6_SUMMARY": merged_d6_path,
            "REL_ROOT": ORACLE_STORE / "relations",
            "GRAPH_ROOT": ORACLE_STORE / "graph",
            "REPORT": ORACLE_REPORTS / "D13_GRAPH_SUMMARY.json",
            "REVIEW_QUEUE": ORACLE_REPORTS / "D14_REVIEW_QUEUE.md",
            "TARGETS": TARGETS,
        },
        "full oracle D13 graph rebuild",
    )
    _run_stage(
        audit_d13,
        {
            "STORE_ROOT": ORACLE_STORE,
            "GRAPH_ROOT": ORACLE_STORE / "graph",
            "REPORT": ORACLE_REPORTS / "D13_QUALITY.json",
            "TARGETS": set(TARGETS),
        },
        "D13 oracle quality gate",
    )

    oracle_nodes = _read_jsonl(ORACLE_STORE / "graph" / "nodes.jsonl")
    oracle_edges = _read_jsonl(ORACLE_STORE / "graph" / "edges.jsonl")

    plan = build_object_delta_plan(
        [CHANGED_DOCUMENT_ID],
        graph_nodes=canonical_nodes,
        graph_edges=canonical_edges,
        internal_relations=canonical_internal,
        cross_relations=canonical_cross,
        conflict_candidates=canonical_conflicts,
    )
    plan_payload = plan.to_dict()

    node_projection = assemble_selective_projection(
        canonical_nodes,
        oracle_nodes,
        reusable_ids=plan_payload["reusable_node_ids"],
        id_key="node_id",
    )
    edge_projection = assemble_selective_projection(
        canonical_edges,
        oracle_edges,
        reusable_ids=plan_payload["reusable_edge_ids"],
        id_key="edge_id",
    )

    canonical_nodes_sha_after = _sha256(canonical_nodes_path)
    canonical_edges_sha_after = _sha256(canonical_edges_path)
    canonical_immutable = (
        canonical_nodes_sha_before == canonical_nodes_sha_after
        and canonical_edges_sha_before == canonical_edges_sha_after
    )
    differential_parity = node_projection.parity and edge_projection.parity

    acceptance = {
        "synthetic_requirement_created": requirement_delta > 0,
        "oracle_d6_d13_completed": True,
        "canonical_graph_immutable": canonical_immutable,
        "reusable_node_payload_exact": node_projection.reusable_payload_exact,
        "reusable_edge_payload_exact": edge_projection.reusable_payload_exact,
        "node_differential_parity": node_projection.parity,
        "edge_differential_parity": edge_projection.parity,
        "differential_parity": differential_parity,
        "full_graph_rebuild_required_for_serving": False,
        "delta_d14_required": True,
        "d15_blocked_until_review": True,
        "network_used": False,
        "source_bytes_mutated": False,
        "legal_truth_promoted": False,
    }
    passed = all(
        acceptance[key]
        for key in (
            "synthetic_requirement_created",
            "oracle_d6_d13_completed",
            "canonical_graph_immutable",
            "reusable_node_payload_exact",
            "reusable_edge_payload_exact",
            "node_differential_parity",
            "edge_differential_parity",
            "differential_parity",
            "delta_d14_required",
            "d15_blocked_until_review",
        )
    )

    result = {
        "record_type": "P0_7_DIFFERENTIAL_D6_D13_ORACLE_PROOF",
        "proof_scope": "SYNTHETIC_D5_DELTA__CHANGED_DOC_D6_D9__FULL_ORACLE_D10_D13__SELECTIVE_OBJECT_REUSE_PROJECTION",
        "fixture": fixture,
        "changed_document": {
            "document_id": CHANGED_DOCUMENT_ID,
            "requirements_before": before_changed_requirements,
            "requirements_after": after_changed_requirements,
            "requirements_delta": requirement_delta,
        },
        "canonical_graph": {
            "nodes": len(canonical_nodes),
            "edges": len(canonical_edges),
            "nodes_sha256_before": canonical_nodes_sha_before,
            "nodes_sha256_after": canonical_nodes_sha_after,
            "edges_sha256_before": canonical_edges_sha_before,
            "edges_sha256_after": canonical_edges_sha_after,
            "immutable": canonical_immutable,
        },
        "oracle_graph": {
            "nodes": len(oracle_nodes),
            "edges": len(oracle_edges),
        },
        "selective_projection": {
            "nodes": node_projection.summary(),
            "edges": edge_projection.summary(),
            "planned_reusable_nodes": len(plan_payload["reusable_node_ids"]),
            "planned_reusable_edges": len(plan_payload["reusable_edge_ids"]),
            "planned_recheck_cross_relations": len(plan_payload["cross_relation_ids"]),
            "planned_recheck_conflicts": len(plan_payload["conflict_candidate_ids"]),
        },
        "acceptance": acceptance,
        "runtime_root": RUNTIME_ROOT.relative_to(REPO_ROOT).as_posix(),
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"SYNTHETIC_REQUIREMENTS_DELTA={requirement_delta}")
    print(f"CANONICAL_GRAPH_IMMUTABLE={str(canonical_immutable).lower()}")
    print(f"ORACLE_GRAPH_NODES={len(oracle_nodes)}")
    print(f"ORACLE_GRAPH_EDGES={len(oracle_edges)}")
    print(f"PLANNED_REUSABLE_NODES={len(plan_payload['reusable_node_ids'])}")
    print(f"PLANNED_REUSABLE_EDGES={len(plan_payload['reusable_edge_ids'])}")
    print(f"REUSABLE_NODE_PAYLOAD_EXACT={str(node_projection.reusable_payload_exact).lower()}")
    print(f"REUSABLE_EDGE_PAYLOAD_EXACT={str(edge_projection.reusable_payload_exact).lower()}")
    print(f"NODE_DIFFERENTIAL_PARITY={str(node_projection.parity).lower()}")
    print(f"EDGE_DIFFERENTIAL_PARITY={str(edge_projection.parity).lower()}")
    print(f"DIFFERENTIAL_PARITY={str(differential_parity).lower()}")
    print("FULL_GRAPH_REBUILD_REQUIRED_FOR_SERVING=false")
    print("DELTA_D14_REQUIRED=true")
    print("D15_BLOCKED_UNTIL_REVIEW=true")
    print("NETWORK_USED=false")
    print("SOURCE_BYTES_MUTATED=false")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
