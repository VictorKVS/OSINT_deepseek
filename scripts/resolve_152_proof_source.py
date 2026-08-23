from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.document_compiler import DocumentCompilerError, extract_visible_text
from father_osint.source_health import load_source_health

TARGET_ID = "DOC-RU-FZ-152-2006"
REVIEW = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch" / "review" / "batch_review_manifest.json"
SOURCE_PACK = REPO_ROOT / "config" / "pdn_official_source_pack.json"
LOCAL_A0_CAPTURE = REPO_ROOT / "data" / "operator_import" / "pdn_official_source_pack" / f"{TARGET_ID}.html"
HEALTH = REPO_ROOT / ".runtime" / "source_health" / "publication-pravo-official-api.json"
SOURCE_KEY = "publication-pravo-official-api"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "RESOLVE_152_PROOF_SOURCE.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def _marker_results(visible_text: str, markers: list[str]) -> dict[str, bool]:
    normalized = _norm(visible_text)
    return {marker: _norm(marker) in normalized for marker in markers}


def _identity_result(data: bytes, source_doc: dict[str, object]) -> tuple[bool, dict[str, bool], dict[str, bool], str | None]:
    """Re-run the same visible-text identity semantics used by the accepted D0-D3 inventory.

    The preserved operator capture is HTML. Raw-byte substring checks are invalid
    because tags/entities can split visible phrases. Identity must be evaluated
    over extracted visible text with whitespace/case/ё normalization, exactly as
    the original source-pack inventory did before accepting the capture.
    """
    try:
        visible_text = extract_visible_text(data, "text/html")
    except (DocumentCompilerError, UnicodeError, ValueError) as exc:
        return False, {}, {}, f"VISIBLE_TEXT_EXTRACTION_FAILED: {exc}"

    primary = [str(value) for value in source_doc.get("primary_identity_markers", [])]
    secondary = [str(value) for value in source_doc.get("identity_markers", [])]
    primary_results = _marker_results(visible_text, primary)
    secondary_results = _marker_results(visible_text, secondary)
    identity_pass = bool(primary_results) and all(primary_results.values()) and all(secondary_results.values())
    return identity_pass, primary_results, secondary_results, None


def main() -> int:
    started = time.perf_counter()
    missing = [str(path.relative_to(REPO_ROOT)) for path in (REVIEW, SOURCE_PACK, LOCAL_A0_CAPTURE) if not path.is_file()]
    if missing:
        result = {
            "record_type": "RESOLVE_152_PROOF_SOURCE",
            "target_document_id": TARGET_ID,
            "proof_available": False,
            "resolution": "BLOCKED_LOCAL_EVIDENCE_MISSING",
            "missing": missing,
            "network_used": False,
            "legal_truth_promoted": False,
            "total_seconds": time.perf_counter() - started,
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    target = next((item for item in review.get("documents", []) if item.get("document_id") == TARGET_ID), None)
    if not target:
        print("TARGET_MISSING_FROM_REVIEW_MANIFEST")
        return 2

    source_pack = json.loads(SOURCE_PACK.read_text(encoding="utf-8"))
    source_doc = next((item for item in source_pack.get("documents", []) if item.get("document_id") == TARGET_ID), None)
    if not source_doc:
        print("TARGET_MISSING_FROM_SOURCE_PACK")
        return 2

    data = LOCAL_A0_CAPTURE.read_bytes()
    expected_sha = str(target.get("artifact_sha256") or "")
    actual_sha = hashlib.sha256(data).hexdigest()
    sha_match = bool(expected_sha) and expected_sha == actual_sha
    identity_pass, primary_results, secondary_results, identity_error = _identity_result(data, source_doc)
    proof_available = sha_match and identity_pass

    health = load_source_health(HEALTH, source_key=SOURCE_KEY)
    circuit_open = bool(health and health.circuit_open())
    retry_after = health.remaining_seconds() if health else 0.0

    result = {
        "record_type": "RESOLVE_152_PROOF_SOURCE",
        "target_document_id": TARGET_ID,
        "proof_available": proof_available,
        "resolution": "LOCAL_A0_VERIFIED_CACHE" if proof_available else "BLOCKED_LOCAL_A0_VERIFICATION_FAILED",
        "local_a0": {
            "path": LOCAL_A0_CAPTURE.relative_to(REPO_ROOT).as_posix(),
            "bytes": len(data),
            "sha256": actual_sha,
            "expected_sha256": expected_sha,
            "sha256_match": sha_match,
            "identity_method": "EXTRACT_VISIBLE_TEXT__PRIMARY_AND_SECONDARY__NORMALIZED",
            "primary_identity_markers": primary_results,
            "secondary_identity_markers": secondary_results,
            "identity_error": identity_error,
            "identity_pass": identity_pass,
            "publication_anchor": source_doc.get("publication_anchor"),
        },
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
        "d2_d3_existing_evidence_reused": proof_available,
        "new_d2_d3_promotion": False,
        "legal_truth_promoted": False,
        "total_seconds": time.perf_counter() - started,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"PROOF_AVAILABLE={str(proof_available).lower()}")
    print(f"RESOLUTION={result['resolution']}")
    print(f"LOCAL_A0_SHA_MATCH={str(sha_match).lower()}")
    print(f"LOCAL_A0_IDENTITY_PASS={str(identity_pass).lower()}")
    print(f"API_CIRCUIT_OPEN={str(circuit_open).lower()}")
    print(f"API_REQUIRED_FOR_SERVING={str(result['api_required_for_serving']).lower()}")
    print("NETWORK_USED=false")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    return 0 if proof_available else 2


if __name__ == "__main__":
    raise SystemExit(main())
