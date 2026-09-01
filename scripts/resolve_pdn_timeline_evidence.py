from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from father_osint.timeline_evidence_resolution import resolve_official_evidence_requests

TIMELINE = REPO_ROOT / "reports" / "pdn_timelines" / "timeline_metadata.jsonl"
PROOFS = REPO_ROOT / "data" / "operator_import" / "timeline_official_evidence" / "verified_official_evidence.jsonl"
REPORT = REPO_ROOT / "reports" / "pdn_timelines" / "timeline_evidence_resolution.jsonl"


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    if not TIMELINE.is_file():
        print("TIMELINE_METADATA_MISSING")
        return 2
    if not PROOFS.is_file():
        print("VERIFIED_OFFICIAL_EVIDENCE_MISSING")
        return 2

    timeline_rows = _read_jsonl(TIMELINE)
    requests = [
        row for row in timeline_rows
        if row.get("record_type") == "OFFICIAL_EVIDENCE_REQUEST"
    ]
    proofs = [
        row for row in _read_jsonl(PROOFS)
        if row.get("record_type") == "VERIFIED_OFFICIAL_EVIDENCE"
    ]
    if not requests:
        print("OFFICIAL_EVIDENCE_REQUESTS_MISSING")
        return 2

    resolutions = resolve_official_evidence_requests(requests, official_proofs=proofs)
    confirmed = sum(row.get("status") == "OFFICIAL_EVIDENCE_CONFIRMED" for row in resolutions)
    pending = len(resolutions) - confirmed
    ready_for_rule_evaluation = sum(
        row.get("effective_date_resolution_state") == "READY_FOR_LEGAL_RULE_EVALUATION"
        for row in resolutions
    )

    summary = {
        "record_type": "TIMELINE_EVIDENCE_RESOLUTION_SUMMARY",
        "evidence_requests": len(requests),
        "verified_official_proof_records": len(proofs),
        "confirmed": confirmed,
        "pending": pending,
        "ready_for_legal_rule_evaluation": ready_for_rule_evaluation,
        "timeline_source_remains_non_evidentiary": True,
        "semantic_text_mirrored": False,
        "legal_truth_promoted": False,
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(summary, ensure_ascii=False, sort_keys=True) + "\n")
        for resolution in resolutions:
            handle.write(json.dumps(
                {"record_type": "TIMELINE_EVIDENCE_RESOLUTION", **resolution},
                ensure_ascii=False,
                sort_keys=True,
            ) + "\n")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"REPORT={REPORT.relative_to(REPO_ROOT).as_posix()}")
    return 0 if pending == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
