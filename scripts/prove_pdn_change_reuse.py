from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.change_monitoring import (
    ChangeDisposition,
    build_bounded_dependency_cone,
    classify_observation,
    synthetic_new_version_sha,
)

STORE_ROOT = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch"
REVIEW = STORE_ROOT / "review" / "batch_review_manifest.json"
CAPTURE_ROOT = REPO_ROOT / "data" / "operator_import" / "pdn_official_source_pack"
CROSS = STORE_ROOT / "relations" / "cross_document.jsonl"
CONFLICTS = STORE_ROOT / "relations" / "conflicts_overlaps.jsonl"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "P0_7_CHANGE_REUSE_PROOF.json"
SIMULATED_TARGET = "DOC-RU-FZ-152-2006"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    started = time.perf_counter()
    if not REVIEW.is_file():
        print("REVIEW_MANIFEST_MISSING")
        return 2

    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    docs = list(review.get("documents", []))
    if not docs:
        print("REVIEW_MANIFEST_EMPTY")
        return 2

    observations = []
    integrity_drift = []
    unchanged = []
    expected_by_id: dict[str, str] = {}
    for item in docs:
        document_id = str(item.get("document_id") or "")
        expected_sha = str(item.get("artifact_sha256") or "")
        if not document_id or not expected_sha:
            print(f"REVIEW_DOCUMENT_INCOMPLETE: {document_id or '<missing>'}")
            return 2
        path = CAPTURE_ROOT / f"{document_id}.html"
        if not path.is_file():
            print(f"LOCAL_CAPTURE_MISSING: {path}")
            return 2
        observed_sha = _sha256(path)
        observation = classify_observation(
            document_id,
            expected_sha256=expected_sha,
            observed_sha256=observed_sha,
            immutable_local_artifact=True,
        )
        observations.append(observation.to_dict())
        expected_by_id[document_id] = expected_sha
        if observation.disposition == ChangeDisposition.UNCHANGED_REUSED:
            unchanged.append(document_id)
        else:
            integrity_drift.append(document_id)

    if SIMULATED_TARGET not in expected_by_id:
        print(f"SIMULATED_TARGET_MISSING: {SIMULATED_TARGET}")
        return 2

    synthetic_sha = synthetic_new_version_sha(SIMULATED_TARGET, expected_by_id[SIMULATED_TARGET])
    synthetic_observation = classify_observation(
        SIMULATED_TARGET,
        expected_sha256=expected_by_id[SIMULATED_TARGET],
        observed_sha256=synthetic_sha,
        immutable_local_artifact=False,
    )
    cross_relations = _read_jsonl(CROSS)
    conflicts = _read_jsonl(CONFLICTS)
    cone = build_bounded_dependency_cone(
        [SIMULATED_TARGET],
        cross_relations=cross_relations,
        conflict_candidates=conflicts,
    )

    total = len(docs)
    reuse_ratio = len(unchanged) / total if total else None
    result = {
        "record_type": "P0_7_CHANGE_MONITORING_REUSE_PROOF",
        "proof_scope": "REAL_UNCHANGED_LOCAL_EVIDENCE_PLUS_SYNTHETIC_NEW_VERSION_INVALIDATION_FIXTURE",
        "real_current_evidence": {
            "documents_total": total,
            "unchanged_reused": len(unchanged),
            "immutable_integrity_drift": len(integrity_drift),
            "reuse_ratio": reuse_ratio,
            "network_used": False,
            "observations": observations,
        },
        "synthetic_change_fixture": {
            "test_only": True,
            "writes_source_bytes": False,
            "creates_real_document_version": False,
            "document_id": SIMULATED_TARGET,
            "prior_sha256": expected_by_id[SIMULATED_TARGET],
            "synthetic_observed_sha256": synthetic_sha,
            "classification": synthetic_observation.disposition.value,
            "dependency_cone": cone,
        },
        "acceptance": {
            "unchanged_objects_reused": len(unchanged) == total,
            "immutable_evidence_intact": not integrity_drift,
            "changed_version_candidate_detected": synthetic_observation.disposition == ChangeDisposition.NEW_VERSION_CANDIDATE,
            "doc_local_invalidation_bounded_to_changed_documents": cone["doc_local_rebuild_document_ids"] == [SIMULATED_TARGET],
            "full_corpus_rebuild_required": cone["full_corpus_rebuild_required"],
            "delta_d14_required": cone["delta_d14_required"],
            "d15_blocked_until_review": cone["d15_blocked_until_review"],
            "new_d2_d3_promotion": False,
            "legal_truth_promoted": False,
        },
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"REAL_DOCUMENTS_TOTAL={total}")
    print(f"REAL_UNCHANGED_REUSED={len(unchanged)}")
    print(f"REAL_INTEGRITY_DRIFT={len(integrity_drift)}")
    print(f"REAL_REUSE_RATIO={reuse_ratio if reuse_ratio is not None else 'n/a'}")
    print(f"SIMULATED_CHANGED_DOCUMENTS=1")
    print(f"DOC_LOCAL_REBUILD_DOCUMENTS={len(cone['doc_local_rebuild_document_ids'])}")
    print(f"CROSS_SCOPE_DOCUMENTS={len(cone['cross_scope_document_ids'])}")
    print(f"FULL_CORPUS_REBUILD_REQUIRED={str(cone['full_corpus_rebuild_required']).lower()}")
    print(f"DELTA_D14_REQUIRED={str(cone['delta_d14_required']).lower()}")
    print(f"D15_BLOCKED_UNTIL_REVIEW={str(cone['d15_blocked_until_review']).lower()}")
    print("NETWORK_USED=false")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    print("LEGAL_TRUTH_PROMOTED=false")

    ok = all(
        (
            result["acceptance"]["unchanged_objects_reused"],
            result["acceptance"]["immutable_evidence_intact"],
            result["acceptance"]["changed_version_candidate_detected"],
            result["acceptance"]["doc_local_invalidation_bounded_to_changed_documents"],
            result["acceptance"]["full_corpus_rebuild_required"] is False,
            result["acceptance"]["delta_d14_required"],
            result["acceptance"]["d15_blocked_until_review"],
        )
    )
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
