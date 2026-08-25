from __future__ import annotations

import hashlib
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
INPUT = REPORT_ROOT / "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json"
CASE_QUEUE = REPORT_ROOT / "PROGRAMMER_BOOK_MAIN_ANALYST_CASE_QUEUE.json"
CASE_HOLD = REPORT_ROOT / "PROGRAMMER_BOOK_MAIN_ANALYST_CASE_HOLD.json"
LATEST = REPORT_ROOT / "LATEST_PROGRAMMER_BOOK_MAIN_ANALYST_CASES.json"

TYPE_CAP = {
    "PATTERN_CANDIDATE": 45,
    "TRADEOFF_CANDIDATE": 45,
    "PRINCIPLE_CANDIDATE": 45,
    "DECISION_CRITERION_CANDIDATE": 45,
    "FAILURE_MODE_CANDIDATE": 40,
    "DEFINITION_CANDIDATE": 45,
    "CONCEPT_CANDIDATE": 35,
    "EXAMPLE_CANDIDATE": 30,
    "TERM_CANDIDATE": 30,
    "CLAIM_CANDIDATE": 35,
}

_STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "when", "then", "than", "are", "is", "to", "of", "a", "an",
    "как", "что", "это", "для", "при", "или", "если", "то", "на", "в", "и", "не", "с", "по", "из", "к", "от", "до",
}
_NEGATION_MARKERS = (" not ", " never ", " avoid ", " cannot ", " should not ", " не ", " нельзя ", " запрещ", " избег", " не следует ")
_POSITIVE_MARKERS = (" should ", " prefer ", " recommend", " use ", " следует ", " рекомендуется ", " предпочт", " использовать ", " применять ")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(value: str) -> str:
    value = value.casefold().replace("ё", "е")
    value = re.sub(r"[^0-9a-zа-я_+#.-]+", " ", value)
    return " ".join(value.split())


def stable_id(prefix: str, *parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return prefix + "-" + hashlib.sha256(payload).hexdigest()[:24]


def topic_basis(candidate: dict[str, Any]) -> tuple[str, str]:
    subject = str(candidate.get("subject") or "").strip()
    if 3 <= len(subject) <= 180:
        return "SUBJECT", norm(subject)

    heading_path = candidate.get("heading_path") or []
    if isinstance(heading_path, list):
        for heading in reversed(heading_path):
            text = str(heading or "").strip()
            if 3 <= len(text) <= 220:
                return "HEADING", norm(text)

    statement = norm(str(candidate.get("statement") or ""))
    tokens = [token for token in statement.split() if len(token) >= 4 and token not in _STOPWORDS]
    # Conservative lexical fingerprint only. This is not semantic equivalence.
    informative = sorted(dict.fromkeys(tokens), key=lambda token: (-len(token), token))[:5]
    if informative:
        return "LEXICAL_FINGERPRINT", " ".join(sorted(informative))
    return "FALLBACK", statement[:160]


def polarity_flags(statement: str) -> tuple[bool, bool]:
    text = " " + norm(statement) + " "
    negative = any(marker in text for marker in _NEGATION_MARKERS)
    positive = any(marker in text for marker in _POSITIVE_MARKERS)
    return negative, positive


def build_case(ctype: str, basis_kind: str, basis_value: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_ids = sorted({
        str(source_id)
        for row in rows
        for source_id in (row.get("supporting_source_ids") or [row.get("target_id")])
        if str(source_id or "").strip()
    })
    candidate_ids = [str(row.get("candidate_group_id") or row.get("candidate_id") or "") for row in rows]
    max_score = max((int(row.get("review_score") or 0) for row in rows), default=0)
    negative_seen = False
    positive_seen = False
    for row in rows:
        negative, positive = polarity_flags(str(row.get("statement") or ""))
        negative_seen = negative_seen or negative
        positive_seen = positive_seen or positive

    possible_conflict = negative_seen and positive_seen and len(rows) > 1
    case_score = max_score + min(30, max(0, len(source_ids) - 1) * 6) + (8 if possible_conflict else 0)

    statements = []
    for row in rows:
        statements.append({
            "candidate_id": str(row.get("candidate_group_id") or row.get("candidate_id") or ""),
            "candidate_type": ctype,
            "statement": row.get("statement"),
            "subject": row.get("subject"),
            "heading_path": row.get("heading_path") or [],
            "target_id": row.get("target_id"),
            "supporting_source_ids": row.get("supporting_source_ids") or [],
            "supporting_source_count": int(row.get("supporting_source_count") or 0),
            "review_score": int(row.get("review_score") or 0),
            "source_locator": row.get("source_locator"),
            "source_text_sha256": row.get("source_text_sha256"),
            "translated_text_sha256": row.get("translated_text_sha256"),
        })

    return {
        "case_id": stable_id("PBC", ctype, basis_kind, basis_value),
        "candidate_type": ctype,
        "topic_basis_kind": basis_kind,
        "topic_basis": basis_value,
        "candidate_count": len(rows),
        "candidate_ids": candidate_ids,
        "supporting_source_ids": source_ids,
        "supporting_source_count": len(source_ids),
        "cross_source_comparison": len(source_ids) >= 2,
        "potential_conflict_signal": possible_conflict,
        "potential_conflict_basis": "HEURISTIC_POLARITY_MIX_ONLY" if possible_conflict else None,
        "case_score": case_score,
        "review_status": "MAIN_ANALYST_CASE_REVIEW_REQUIRED",
        "analyst_questions": [
            "Do the statements describe the same decision context, or only share terminology?",
            "Which conditions make each recommendation applicable?",
            "Do sources actually agree, complement each other, or conflict?",
            "What trade-offs, failure modes, and evidence support the preferred formulation?",
            "Can a bounded Golden Candidate be formed without losing source-specific caveats?",
        ],
        "kb_auto_promotion": False,
        "statements": statements,
    }


def main() -> int:
    started = time.perf_counter()
    if not INPUT.is_file():
        print(json.dumps({"status": "INPUT_MISSING", "input": INPUT.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))
        return 2

    payload = load_json(INPUT)
    candidates = [row for row in payload.get("candidates", []) if isinstance(row, dict)]

    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        ctype = str(candidate.get("candidate_type") or "UNKNOWN")
        basis_kind, basis_value = topic_basis(candidate)
        grouped[(ctype, basis_kind, basis_value)].append(candidate)

    cases = [build_case(ctype, basis_kind, basis_value, rows) for (ctype, basis_kind, basis_value), rows in grouped.items()]
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        by_type[str(case.get("candidate_type") or "UNKNOWN")].append(case)

    queue: list[dict[str, Any]] = []
    hold: list[dict[str, Any]] = []
    queue_counts: Counter[str] = Counter()
    hold_counts: Counter[str] = Counter()

    for ctype, rows in sorted(by_type.items()):
        rows.sort(key=lambda row: (
            -int(row.get("case_score") or 0),
            -int(row.get("supporting_source_count") or 0),
            -int(row.get("candidate_count") or 0),
            str(row.get("case_id") or ""),
        ))
        cap = TYPE_CAP.get(ctype, 25)
        for index, row in enumerate(rows):
            if index < cap:
                row["review_rank_within_type"] = index + 1
                queue.append(row)
                queue_counts[ctype] += 1
            else:
                row["review_status"] = "HELD_CASE_NOT_DISCARDED"
                hold.append(row)
                hold_counts[ctype] += 1

    queue.sort(key=lambda row: (
        -int(row.get("case_score") or 0),
        -int(row.get("supporting_source_count") or 0),
        str(row.get("candidate_type") or ""),
        str(row.get("case_id") or ""),
    ))

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    CASE_QUEUE.write_text(json.dumps({
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_MAIN_ANALYST_CASE_QUEUE",
        "state": "MAIN_ANALYST_CASE_REVIEW_REQUIRED",
        "kb_auto_promotion": False,
        "cases_total": len(queue),
        "case_type_counts": dict(sorted(queue_counts.items())),
        "cases": queue,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CASE_HOLD.write_text(json.dumps({
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_MAIN_ANALYST_CASE_HOLD",
        "state": "HELD_CASE_NOT_DISCARDED",
        "kb_auto_promotion": False,
        "cases_total": len(hold),
        "case_type_counts": dict(sorted(hold_counts.items())),
        "cases": hold,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - started
    summary = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_MAIN_ANALYST_CASE_BUILD",
        "status": "PASS",
        "input_candidates_total": len(candidates),
        "comparison_cases_total": len(cases),
        "main_analyst_case_queue_total": len(queue),
        "held_case_total": len(hold),
        "candidate_to_case_reduction_pct": round((1 - len(queue) / len(candidates)) * 100, 2) if candidates else 0.0,
        "cross_source_cases_total": sum(bool(row.get("cross_source_comparison")) for row in cases),
        "potential_conflict_cases_total": sum(bool(row.get("potential_conflict_signal")) for row in cases),
        "queue_type_counts": dict(sorted(queue_counts.items())),
        "held_type_counts": dict(sorted(hold_counts.items())),
        "review_gate": "MAIN_ANALYST_CASE_REVIEW_REQUIRED",
        "semantic_equivalence_asserted": False,
        "conflict_asserted": False,
        "kb_auto_promotion": False,
        "elapsed_seconds": elapsed,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "queue": CASE_QUEUE.relative_to(ROOT).as_posix(),
        "hold": CASE_HOLD.relative_to(ROOT).as_posix(),
        "note": "Cases are conservative comparison bundles. Topic grouping does not assert semantic equivalence; potential conflict is a heuristic review signal only. All underlying candidate references and provenance are preserved.",
    }
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Case queue: {CASE_QUEUE.relative_to(ROOT).as_posix()}")
    print(f"Case hold: {CASE_HOLD.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
