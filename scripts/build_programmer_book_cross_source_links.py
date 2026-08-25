from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
INPUT = REPORT_ROOT / "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json"
LINKS_OUT = REPORT_ROOT / "PROGRAMMER_BOOK_CROSS_SOURCE_LINKS.json"
QUEUE_OUT = REPORT_ROOT / "PROGRAMMER_BOOK_CROSS_SOURCE_ANALYST_QUEUE.json"
LATEST = REPORT_ROOT / "LATEST_PROGRAMMER_BOOK_CROSS_SOURCE_LINKS.json"

# This pass creates review hypotheses only. Similarity never means semantic equivalence.
MIN_SCORE = 0.50
MAX_MATCHES_PER_CANDIDATE = 3
QUEUE_CAP = 160

_STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "when", "then", "than", "are", "is", "to", "of", "a", "an",
    "be", "by", "as", "or", "on", "in", "it", "its", "can", "could", "would", "should", "may", "might",
    "как", "что", "это", "для", "при", "или", "если", "то", "на", "в", "и", "не", "с", "по", "из", "к", "от", "до",
    "быть", "может", "могут", "следует", "нужно", "надо", "когда", "который", "которая", "которые",
}

_NEGATIVE = (" not ", " never ", " avoid ", " cannot ", " should not ", " anti-pattern ", " risk ", " failure ",
             " не ", " нельзя ", " избег", " не следует ", " риск ", " ошибка ", " антипаттерн ", " отказ ")
_POSITIVE = (" should ", " prefer ", " recommend", " use ", " adopt ", " следует ", " рекомендуется ",
             " предпочт", " использовать ", " применять ", " выбирать ")

_FAMILY = {
    "PATTERN_CANDIDATE": "DECISION",
    "TRADEOFF_CANDIDATE": "DECISION",
    "PRINCIPLE_CANDIDATE": "DECISION",
    "DECISION_CRITERION_CANDIDATE": "DECISION",
    "FAILURE_MODE_CANDIDATE": "DECISION",
    "CLAIM_CANDIDATE": "DECISION",
    "DEFINITION_CANDIDATE": "CONCEPT",
    "CONCEPT_CANDIDATE": "CONCEPT",
    "TERM_CANDIDATE": "CONCEPT",
    "EXAMPLE_CANDIDATE": "EXAMPLE",
}

_TYPE_WEIGHT = {
    "PATTERN_CANDIDATE": 12,
    "TRADEOFF_CANDIDATE": 12,
    "PRINCIPLE_CANDIDATE": 11,
    "DECISION_CRITERION_CANDIDATE": 11,
    "FAILURE_MODE_CANDIDATE": 10,
    "DEFINITION_CANDIDATE": 8,
    "CONCEPT_CANDIDATE": 7,
    "EXAMPLE_CANDIDATE": 6,
    "CLAIM_CANDIDATE": 5,
    "TERM_CANDIDATE": 4,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(value: str) -> str:
    value = value.casefold().replace("ё", "е")
    value = re.sub(r"[^0-9a-zа-я_+#.-]+", " ", value)
    return " ".join(value.split())


def tokens(value: str) -> set[str]:
    return {
        token
        for token in norm(value).split()
        if len(token) >= 4 and token not in _STOPWORDS and not token.isdigit()
    }


def heading_text(row: dict[str, Any]) -> str:
    heading = row.get("heading_path") or []
    if isinstance(heading, list):
        return " ".join(str(item) for item in heading if str(item).strip())
    return str(heading)


def candidate_source_ids(row: dict[str, Any]) -> set[str]:
    values = row.get("supporting_source_ids") or [row.get("target_id")]
    return {str(value) for value in values if str(value or "").strip()}


def candidate_id(row: dict[str, Any]) -> str:
    return str(row.get("candidate_group_id") or row.get("candidate_id") or "")


def weighted_jaccard(left: set[str], right: set[str], idf: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    union = left | right
    intersection = left & right
    denom = sum(idf.get(token, 1.0) for token in union)
    return (sum(idf.get(token, 1.0) for token in intersection) / denom) if denom else 0.0


def polarity(statement: str) -> tuple[bool, bool]:
    text = " " + norm(statement) + " "
    return any(marker in text for marker in _NEGATIVE), any(marker in text for marker in _POSITIVE)


def compatible(left: dict[str, Any], right: dict[str, Any]) -> bool:
    lt = str(left.get("candidate_type") or "UNKNOWN")
    rt = str(right.get("candidate_type") or "UNKNOWN")
    lf = _FAMILY.get(lt, lt)
    rf = _FAMILY.get(rt, rt)
    if lf == rf:
        return True
    # Examples may support a decision but are not linked to bare concept/term rows.
    return {lf, rf} == {"DECISION", "EXAMPLE"}


def pair_score(left: dict[str, Any], right: dict[str, Any], idf: dict[str, float]) -> tuple[float, dict[str, float]]:
    l_statement = tokens(str(left.get("statement") or ""))
    r_statement = tokens(str(right.get("statement") or ""))
    l_subject = tokens(str(left.get("subject") or ""))
    r_subject = tokens(str(right.get("subject") or ""))
    l_heading = tokens(heading_text(left))
    r_heading = tokens(heading_text(right))

    statement_similarity = weighted_jaccard(l_statement, r_statement, idf)
    subject_similarity = weighted_jaccard(l_subject, r_subject, idf)
    heading_similarity = weighted_jaccard(l_heading, r_heading, idf)
    shared_statement = len(l_statement & r_statement)

    exact_subject = bool(l_subject and r_subject and norm(str(left.get("subject") or "")) == norm(str(right.get("subject") or "")))
    same_type = str(left.get("candidate_type") or "") == str(right.get("candidate_type") or "")
    same_family = _FAMILY.get(str(left.get("candidate_type") or "")) == _FAMILY.get(str(right.get("candidate_type") or ""))

    score = (
        0.52 * statement_similarity
        + 0.25 * subject_similarity
        + 0.13 * heading_similarity
        + (0.12 if exact_subject else 0.0)
        + (0.06 if same_type else 0.0)
        + (0.03 if same_family else 0.0)
        + (0.04 if shared_statement >= 3 else 0.0)
    )
    return min(score, 1.0), {
        "statement_similarity": round(statement_similarity, 4),
        "subject_similarity": round(subject_similarity, 4),
        "heading_similarity": round(heading_similarity, 4),
        "shared_statement_tokens": float(shared_statement),
        "exact_subject_bonus": 1.0 if exact_subject else 0.0,
        "same_type_bonus": 1.0 if same_type else 0.0,
        "same_family_bonus": 1.0 if same_family else 0.0,
    }


def stable_link_id(left_id: str, right_id: str) -> str:
    a, b = sorted((left_id, right_id))
    return "PBX-" + hashlib.sha256(f"{a}\x1f{b}".encode("utf-8")).hexdigest()[:24]


def compact_candidate(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id(row),
        "candidate_type": row.get("candidate_type"),
        "statement": row.get("statement"),
        "subject": row.get("subject"),
        "heading_path": row.get("heading_path") or [],
        "target_id": row.get("target_id"),
        "supporting_source_ids": sorted(candidate_source_ids(row)),
        "source_locator": row.get("source_locator"),
        "source_text_sha256": row.get("source_text_sha256"),
        "translated_text_sha256": row.get("translated_text_sha256"),
        "review_score": int(row.get("review_score") or 0),
    }


def main() -> int:
    started = time.perf_counter()
    if not INPUT.is_file():
        print(json.dumps({"status": "INPUT_MISSING", "input": INPUT.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))
        return 2

    payload = load_json(INPUT)
    rows = [row for row in payload.get("candidates", []) if isinstance(row, dict) and candidate_id(row)]

    df: Counter[str] = Counter()
    token_cache: dict[str, set[str]] = {}
    for row in rows:
        cid = candidate_id(row)
        all_tokens = tokens(str(row.get("statement") or "")) | tokens(str(row.get("subject") or "")) | tokens(heading_text(row))
        token_cache[cid] = all_tokens
        for token in all_tokens:
            df[token] += 1
    total = max(1, len(rows))
    idf = {token: math.log((total + 1) / (count + 1)) + 1.0 for token, count in df.items()}

    matches_by_candidate: dict[str, list[tuple[float, dict[str, float], dict[str, Any]]]] = defaultdict(list)
    pairs_considered = 0
    pairs_above_threshold = 0

    for i, left in enumerate(rows):
        left_sources = candidate_source_ids(left)
        left_id = candidate_id(left)
        for right in rows[i + 1:]:
            right_id = candidate_id(right)
            right_sources = candidate_source_ids(right)
            if left_sources & right_sources:
                continue
            if not compatible(left, right):
                continue
            # Cheap conservative prefilter: require at least two lexical anchors, unless subjects exactly match.
            shared = token_cache[left_id] & token_cache[right_id]
            exact_subject = bool(
                str(left.get("subject") or "").strip()
                and norm(str(left.get("subject") or "")) == norm(str(right.get("subject") or ""))
            )
            if len(shared) < 2 and not exact_subject:
                continue
            pairs_considered += 1
            score, detail = pair_score(left, right, idf)
            if score < MIN_SCORE:
                continue
            pairs_above_threshold += 1
            matches_by_candidate[left_id].append((score, detail, right))
            matches_by_candidate[right_id].append((score, detail, left))

    selected_pair_ids: set[str] = set()
    links: list[dict[str, Any]] = []
    row_by_id = {candidate_id(row): row for row in rows}

    for cid, matches in matches_by_candidate.items():
        matches.sort(key=lambda item: (-item[0], -int(item[2].get("review_score") or 0), candidate_id(item[2])))
        for score, detail, other in matches[:MAX_MATCHES_PER_CANDIDATE]:
            other_id = candidate_id(other)
            link_id = stable_link_id(cid, other_id)
            if link_id in selected_pair_ids:
                continue
            selected_pair_ids.add(link_id)
            left = row_by_id[cid]
            right = other
            lneg, lpos = polarity(str(left.get("statement") or ""))
            rneg, rpos = polarity(str(right.get("statement") or ""))
            conflict_signal = (lneg and rpos) or (rneg and lpos)
            analyst_priority = int(round(score * 100)) + _TYPE_WEIGHT.get(str(left.get("candidate_type") or ""), 0) + _TYPE_WEIGHT.get(str(right.get("candidate_type") or ""), 0) + (8 if conflict_signal else 0)
            links.append({
                "link_id": link_id,
                "record_type": "PROGRAMMER_BOOK_CROSS_SOURCE_REVIEW_LINK",
                "similarity_score": round(score, 4),
                "similarity_components": detail,
                "semantic_equivalence_asserted": False,
                "conflict_asserted": False,
                "potential_conflict_signal": conflict_signal,
                "potential_conflict_basis": "HEURISTIC_POLARITY_DIFFERENCE" if conflict_signal else None,
                "analyst_priority_score": analyst_priority,
                "review_status": "MAIN_ANALYST_CROSS_SOURCE_REVIEW_REQUIRED",
                "kb_auto_promotion": False,
                "left": compact_candidate(left),
                "right": compact_candidate(right),
                "analyst_questions": [
                    "Do these statements address the same engineering decision context?",
                    "If yes, do they agree, complement, or genuinely conflict?",
                    "Which preconditions and constraints differ between the sources?",
                    "What trade-offs and failure modes change the preferred decision?",
                    "Is there enough evidence to draft a bounded Golden Candidate?",
                ],
            })

    links.sort(key=lambda row: (-int(row.get("analyst_priority_score") or 0), -float(row.get("similarity_score") or 0), str(row.get("link_id") or "")))
    queue = links[:QUEUE_CAP]

    source_pairs: Counter[str] = Counter()
    type_pairs: Counter[str] = Counter()
    for row in links:
        left = row["left"]
        right = row["right"]
        sp = " <> ".join(sorted((str(left.get("target_id") or ""), str(right.get("target_id") or ""))))
        source_pairs[sp] += 1
        tp = " <> ".join(sorted((str(left.get("candidate_type") or ""), str(right.get("candidate_type") or ""))))
        type_pairs[tp] += 1

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    LINKS_OUT.write_text(json.dumps({
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_CROSS_SOURCE_LINKS",
        "state": "REVIEW_HYPOTHESES_ONLY",
        "semantic_equivalence_asserted": False,
        "conflict_asserted": False,
        "kb_auto_promotion": False,
        "links_total": len(links),
        "links": links,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    QUEUE_OUT.write_text(json.dumps({
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_CROSS_SOURCE_ANALYST_QUEUE",
        "state": "MAIN_ANALYST_CROSS_SOURCE_REVIEW_REQUIRED",
        "semantic_equivalence_asserted": False,
        "conflict_asserted": False,
        "kb_auto_promotion": False,
        "queue_total": len(queue),
        "links": queue,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - started
    summary = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_CROSS_SOURCE_LINK_BUILD",
        "status": "PASS",
        "input_candidates_total": len(rows),
        "pairs_considered_total": pairs_considered,
        "pairs_above_threshold_total": pairs_above_threshold,
        "cross_source_links_total": len(links),
        "main_analyst_cross_source_queue_total": len(queue),
        "potential_conflict_links_total": sum(bool(row.get("potential_conflict_signal")) for row in links),
        "distinct_source_pairs_total": len(source_pairs),
        "top_source_pairs": dict(source_pairs.most_common(20)),
        "top_type_pairs": dict(type_pairs.most_common(20)),
        "minimum_similarity_score": MIN_SCORE,
        "max_matches_per_candidate": MAX_MATCHES_PER_CANDIDATE,
        "semantic_equivalence_asserted": False,
        "conflict_asserted": False,
        "review_gate": "MAIN_ANALYST_CROSS_SOURCE_REVIEW_REQUIRED",
        "kb_auto_promotion": False,
        "elapsed_seconds": elapsed,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "links": LINKS_OUT.relative_to(ROOT).as_posix(),
        "queue": QUEUE_OUT.relative_to(ROOT).as_posix(),
        "note": "Cross-source links are deterministic lexical review hypotheses only. They preserve candidate/source/hash provenance and do not assert semantic equivalence or contradiction.",
    }
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Links: {LINKS_OUT.relative_to(ROOT).as_posix()}")
    print(f"Queue: {QUEUE_OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
