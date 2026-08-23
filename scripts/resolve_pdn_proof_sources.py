from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.proof_resolution import resolve_pack_from_files


REVIEW = REPO_ROOT / "data" / "knowledge_factory" / "pdn_official_batch" / "review" / "batch_review_manifest.json"
SOURCE_PACK = REPO_ROOT / "config" / "pdn_official_source_pack.json"
LOCAL_DIR = REPO_ROOT / "data" / "operator_import" / "pdn_official_source_pack"
REPORT = REPO_ROOT / "reports" / "pdn_live" / "RESOLVE_PDN_PROOF_SOURCES.json"


def main() -> int:
    missing = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REVIEW, SOURCE_PACK)
        if not path.is_file()
    ]
    if missing:
        result = {
            "record_type": "LOCAL_OFFICIAL_PROOF_PACK_RESOLUTION",
            "all_proofs_available": False,
            "proof_available": 0,
            "proof_blocked": None,
            "missing_inputs": missing,
            "network_used": False,
            "api_required_for_serving": False,
            "new_d2_d3_promotion": False,
            "legal_truth_promoted": False,
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    result = resolve_pack_from_files(
        repo_root=REPO_ROOT,
        review_path=REVIEW,
        source_pack_path=SOURCE_PACK,
        local_dir=LOCAL_DIR,
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f"DOCUMENTS_TOTAL={result['documents_total']}")
    print(f"PROOF_AVAILABLE={result['proof_available']}")
    print(f"PROOF_BLOCKED={result['proof_blocked']}")
    print(f"ALL_PROOFS_AVAILABLE={str(result['all_proofs_available']).lower()}")
    print("NETWORK_USED=false")
    print("API_REQUIRED_FOR_SERVING=false")
    print(f"TOTAL_SECONDS={result['total_seconds']:.6f}")
    throughput = result.get("throughput_docs_per_second")
    print(f"THROUGHPUT_DOCS_PER_SECOND={throughput:.3f}" if throughput is not None else "THROUGHPUT_DOCS_PER_SECOND=n/a")
    print("LEGAL_TRUTH_PROMOTED=false")
    return 0 if result["all_proofs_available"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
