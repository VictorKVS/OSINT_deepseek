from __future__ import annotations

import hashlib
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
INPUT = REPORT_ROOT / "PROGRAMMER_BOOK_ARCHITECTURE_CANDIDATES.json"
DEEP_SUMMARY = REPORT_ROOT / "LATEST_PROGRAMMER_BOOK_DEEP_ANALYSIS.json"
QUEUE = REPORT_ROOT / "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json"
HOLD = REPORT_ROOT / "PROGRAMMER_BOOK_CANDIDATES_HOLD.json"
LATEST = REPORT_ROOT / "LATEST_PROGRAMMER_BOOK_REDUCTION.json"

TYPE_WEIGHT = {
    "PATTERN_CANDIDATE": 100,
    "TRADEOFF_CANDIDATE": 98,
    "PRINCIPLE_CANDIDATE": 96,
    "DECISION_CRITERION_CANDIDATE": 94,
    "FAILURE_MODE_CANDIDATE": 92,
    "DEFINITION_CANDIDATE": 82,
    "CONCEPT_CANDIDATE": 74,
    "EXAMPLE_CANDIDATE": 68,
    "TERM_CANDIDATE": 58,
    "CLAIM_CANDIDATE": 40,
}

TYPE_CAP = {
    "PATTERN_CANDIDATE": 180,
    "TRADEOFF_CANDIDATE": 180,
    "PRINCIPLE_CANDIDATE": 180,
    "DECISION_CRITERION_CANDIDATE": 180,
    "FAILURE_MODE_CANDIDATE": 140,
    "DEFINITION_CANDIDATE": 220,
    "CONCEPT_CANDIDATE": 120,
    "EXAMPLE_CANDIDATE": 120,
    "TERM_CANDIDATE": 160,
    "CLAIM_CANDIDATE": 160,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(value: str) -> str:
    return " ".join(value.casefold().replace("ё", "е").split())


def stable_key(candidate: dict[str, Any]) -> str:
    payload = "\x1f".join(
        [
            str(candidate.get("candidate_type") or ""),
            norm(str(candidate.get("statement") or "")),
        ]
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def score(candidate: dict[str, Any], support_count: int) -> int:
    ctype = str(candidate.get("candidate_type") or "UNKNOWN")
    value = TYPE_WEIGHT.get(ctype, 20)
    confidence = str(candidate.get("confidence") or "LOW").upper()
    if confidence == "HIGH":
        value += 12
    elif confidence == "MEDIUM":
        value += 7

    statement = str(candidate.get("statement") or "").strip()
    if 60 <= len(statement) <= 700:
        value += 6
    elif len(statement) < 25:
        value -= 12
    elif len(statement) > 1400:
        value -= 8

    if candidate.get("heading_path"):
        value += 4
    value += min(24, max(0, support_count - 1) * 8)
    return value


def main() -> int:
    started = time.perf_counter()
    if not INPUT.is_file():
        print(json.dumps({"status": "INPUT_MISSING", "input": INPUT.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))
        return 2

    payload = load_json(INPUT)
    raw_candidates = [row for row in payload.get("candidates", []) if isinstance(row, dict)]

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in raw_candidates:
        grouped[stable_key(candidate)].append(candidate)

    deduped: list[dict[str, Any]] = []
    duplicate_rows_total = 0
    for key, rows in grouped.items():
        duplicate_rows_total += max(0, len(rows) - 1)
        exemplar = dict(rows[0])
        sources = sorted({str(row.get("target_id") or "") for row in rows if str(row.get("target_id") or "")})
        exemplar["candidate_group_id"] = key
        exemplar["supporting_source_ids"] = sources
        exemplar["supporting_source_count"] = len(sources)
        exemplar["duplicate_observations_collapsed"] = max(0, len(rows) - 1)
        exemplar["review_score"] = score(exemplar, len(sources))
        exemplar["review_status"] = "QUEUED_CANDIDATE"
        exemplar["kb_auto_promotion"] = False
        deduped.append(exemplar)

    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in deduped:
        by_type[str(row.get("candidate_type") or "UNKNOWN")].append(row)

    queue_rows: list[dict[str, Any]] = []
    hold_rows: list[dict[str, Any]] = []
    selected_counts: Counter[str] = Counter()
    held_counts: Counter[str] = Counter()

    for ctype, rows in sorted(by_type.items()):
        rows.sort(
            key=lambda row: (
                -int(row.get("review_score") or 0),
                -int(row.get("supporting_source_count") or 0),
                str(row.get("target_id") or ""),
                str(row.get("candidate_id") or row.get("candidate_group_id") or ""),
            )
        )
        cap = TYPE_CAP.get(ctype, 80)
        for index, row in enumerate(rows):
            if index < cap:
                row["review_priority_rank_within_type"] = index + 1
                row["review_status"] = "MAIN_ANALYST_REVIEW_REQUIRED"
                queue_rows.append(row)
                selected_counts[ctype] += 1
            else:
                row["review_status"] = "HELD_LOW_PRIORITY_NOT_DISCARDED"
                hold_rows.append(row)
                held_counts[ctype] += 1

    queue_rows.sort(
        key=lambda row: (
            -int(row.get("review_score") or 0),
            str(row.get("candidate_type") or ""),
            str(row.get("target_id") or ""),
        )
    )

    deep = load_json(DEEP_SUMMARY) if DEEP_SUMMARY.is_file() else {}
    queue_payload = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE",
        "knowledge_base_id": "PROGRAMMING_KB",
        "state": "MAIN_ANALYST_REVIEW_REQUIRED",
        "kb_auto_promotion": False,
        "candidates_total": len(queue_rows),
        "candidate_type_counts": dict(sorted(selected_counts.items())),
        "parser_gap_total_upstream": int(deep.get("parser_gap_total") or 0),
        "text_too_small_total_upstream": int(deep.get("text_too_small_total") or 0),
        "candidates": queue_rows,
    }
    hold_payload = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_CANDIDATES_HOLD",
        "state": "HELD_LOW_PRIORITY_NOT_DISCARDED",
        "kb_auto_promotion": False,
        "candidates_total": len(hold_rows),
        "candidate_type_counts": dict(sorted(held_counts.items())),
        "candidates": hold_rows,
    }

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    QUEUE.write_text(json.dumps(queue_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    HOLD.write_text(json.dumps(hold_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - started
    summary = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_CANDIDATE_REDUCTION",
        "status": "PASS",
        "input_candidates_total": len(raw_candidates),
        "exact_duplicate_observations_collapsed_total": duplicate_rows_total,
        "deduplicated_candidates_total": len(deduped),
        "main_analyst_queue_total": len(queue_rows),
        "held_low_priority_total": len(hold_rows),
        "queue_reduction_pct_vs_input": round((1 - len(queue_rows) / len(raw_candidates)) * 100, 2) if raw_candidates else 0.0,
        "queue_type_counts": dict(sorted(selected_counts.items())),
        "held_type_counts": dict(sorted(held_counts.items())),
        "parser_gap_total_upstream": int(deep.get("parser_gap_total") or 0),
        "text_too_small_total_upstream": int(deep.get("text_too_small_total") or 0),
        "review_gate": "MAIN_ANALYST_REVIEW_REQUIRED",
        "kb_auto_promotion": False,
        "elapsed_seconds": elapsed,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "queue": QUEUE.relative_to(ROOT).as_posix(),
        "hold": HOLD.relative_to(ROOT).as_posix(),
        "note": "Low-priority candidates are held, not deleted. Exact normalized duplicates are collapsed with source support preserved. No semantic equivalence is asserted by this deterministic pass.",
    }
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Queue: {QUEUE.relative_to(ROOT).as_posix()}")
    print(f"Hold: {HOLD.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
