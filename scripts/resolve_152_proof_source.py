from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.proof_resolution import resolve_local_official_proof
from father_osint.source_health import load_source_health

TARGET_ID = "DOC-RU-FZ-152-2006"
REVIEW = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch" / "review" / "batch_review_manifest.json"
SOURCE_PACK = REPO_ROOT / "config" / "pdn_official_source_pack.json"
LOCAL_A0_CAPTURE = REPO_ROOT / "data" / "operator_import" / "pdn_official_source_pack" / f"{TARGET_ID}.html"
HEALTH = REPO_ROOT / ".runtime" / "source_health" / "publication-pravo-official-api.json"
SOURCE_KEY = "publication-pravo-official-api"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "RESOLVE_152_PROOF_SOURCE.json"


def main() -> int:
    started = time.perf_counter()
    missing = [str(path.relative_to(REPO_ROOT)) for path in (REVIEW, SOURCE_PACK) if not path.is_file()]
    if missing:
        result = {
            "record_type": "RESOLVE_152_PROOF_SOURCE",
            "target_document_id": TARGET_ID,
            "proof_available": False,
            "resolution": "BLOCKED_LOCAL_EVIDENCE_MISSING",
            "missing": missing,
            "network_used": False,
            "api_required_for_serving": False,
            "new_d2_d3_promotion": False,
            "legal_truth_promoted": False,
            "total_seconds": time.perf_counter() - started,
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    target = next((item for item in review.get("documents", []) if item.get("document_id") == TARGET_ID), None)
    source_pack = json.loads(SOURCE_PACK.read_text(encoding="utf-8"))
    source_doc = next((item for item in source_pack.get("documents", []) if item.get("document_id") == TARGET_ID), None)
    if not target or not source_doc:
        print("TARGET_MISSING_FROM_CONTROL_REGISTRY")
        return 2

    local = resolve_local_official_proof(
        repo_root=REPO_ROOT,
        review_item=target,
        source_item=source_doc,
        local_path=LOCAL_A0_CAPTURE,
    )
    health = load_source_health(HEALTH, source_key=SOURCE_KEY)
    circuit_open = bool(health and health.circuit_open())
    retry_after = health.remaining_seconds() if health else 0.0

    result = {
        "record_type": "RESOLVE_152_PROOF_SOURCE",
        "target_document_id": TARGET_ID,
        "proof_available": local.proof_available,
        "resolution": local.resolution,
        "local_a0": local.to_dict(),
        "official_api_health": {
            "source_key": SOURCE_KEY,
            "circuit_open": circuit_open,
            "retry_after_seconds": retry_after,
            "last_error": health.error if health else None,
            "serving_dependency": False,
        },
        "network_used": False,
        "api_required_for_serving": False,
        "freshness_monitoring_degraded": circuit_open,
        "d2_d3_existing_evidence_reused": local.proof_available,
        "new_d2_d3_promotion": False,
        "legal_truth_promoted": False,
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"PROOF_AVAILABLE={str(local.proof_available).lower()}")
    print(f"RESOLUTION={local.resolution}")
    print(f"LOCAL_A0_SHA_MATCH={str(local.sha256_match).lower()}")
    print(f"LOCAL_A0_IDENTITY_PASS={str(local.identity_pass).lower()}")
    print(f"API_CIRCUIT_OPEN={str(circuit_open).lower()}")
    print("API_REQUIRED_FOR_SERVING=false")
    print("NETWORK_USED=false")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    return 0 if local.proof_available else 2


if __name__ == "__main__":
    raise SystemExit(main())
