from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.benchmark_152_reuse import (
    CANDIDATE,
    REPORT,
    TARGET_DATE,
    TARGET_ID,
    TARGET_NUMBER,
    TARGET_TITLE_MARKER,
    _compare,
    _father_reference,
)

WARM_REPORT = REPO_ROOT / "reports" / "pdn_live" / "BENCHMARK_152_REUSE_WARM.json"


def main() -> int:
    total_started = time.perf_counter()
    if not CANDIDATE.is_file():
        print(f"CACHE_MISSING: {CANDIDATE}")
        return 2

    reference_started = time.perf_counter()
    father_text, father_meta = _father_reference()
    father_reference_seconds = time.perf_counter() - reference_started

    cache_started = time.perf_counter()
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    cache_load_seconds = time.perf_counter() - cache_started

    external_text = str(candidate.get("textIPS") or "")
    if not external_text.strip():
        print("CACHE_INVALID: missing textIPS")
        return 2

    compare_started = time.perf_counter()
    comparison = _compare(father_text, external_text)
    compare_seconds = time.perf_counter() - compare_started

    number_match = str(candidate.get("docNumberIPS", "")).strip() == TARGET_NUMBER
    date_match = str(candidate.get("docdateIPS", "")).strip() == TARGET_DATE
    title_match = TARGET_TITLE_MARKER in str(candidate.get("headingIPS") or "").casefold()
    identity_pass = number_match and date_match and title_match
    total_seconds = time.perf_counter() - total_started

    result = {
        "record_type": "REUSE_FIRST_BENCHMARK_152_FZ_WARM_CACHE",
        "target_document_id": TARGET_ID,
        "successful_provider": "local_verified_bootstrap_cache",
        "cache_path": CANDIDATE.relative_to(REPO_ROOT).as_posix(),
        "identity": {
            "number_match": number_match,
            "date_match": date_match,
            "title_marker_match": title_match,
            "identity_pass": identity_pass,
        },
        "father_reference": father_meta,
        "comparison": comparison,
        "timing_seconds": {
            "father_reference_load": father_reference_seconds,
            "cache_load": cache_load_seconds,
            "content_compare": compare_seconds,
            "total": total_seconds,
        },
        "interpretation": {
            "mode": "warm_reuse_after_one_successful_external_acquisition",
            "network_used": False,
            "legal_truth_promoted": False,
            "cold_report_path": REPORT.relative_to(REPO_ROOT).as_posix(),
        },
    }

    WARM_REPORT.parent.mkdir(parents=True, exist_ok=True)
    WARM_REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print("PROVIDER=local_verified_bootstrap_cache")
    print(f"TOTAL_SECONDS={total_seconds:.6f}")
    print(f"CACHE_LOAD_SECONDS={cache_load_seconds:.6f}")
    print(f"COMPARE_SECONDS={compare_seconds:.6f}")
    print(f"IDENTITY_PASS={str(identity_pass).lower()}")
    return 0 if identity_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
