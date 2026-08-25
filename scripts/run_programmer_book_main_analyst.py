from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "reports" / "programming_kb_factory"
INPUT = REPORT_ROOT / "PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json"
OUTPUT_ROOT = REPORT_ROOT / "main_analyst"
LATEST = REPORT_ROOT / "LATEST_PROGRAMMER_BOOK_MAIN_ANALYST.json"
PROFESSOR_QUEUE = REPORT_ROOT / "PROGRAMMER_BOOK_PROFESSOR_REVIEW_QUEUE.json"

DEFAULT_BASE_URL = os.getenv("FATHER_LLM_BASE_URL", "http://127.0.0.1:1234/v1")
DEFAULT_MODEL = os.getenv("FATHER_MAIN_ANALYST_MODEL", "")
DEFAULT_BOOK_TITLE = "Software Architecture: The Hard Parts"

ALLOWED_DECISIONS = {
    "KEEP_CANDIDATE", "REFINE_CANDIDATE", "MERGE_EQUIVALENT",
    "HOLD_AMBIGUOUS", "HOLD_LOW_EVIDENCE",
}
ALLOWED_RELATIONS = {
    "SUPPORTS", "CONTRADICTS", "REFINES", "SPECIALIZES", "GENERALIZES",
    "USES_DIFFERENT_DEFINITION", "ALTERNATIVE_TO", "APPLIES_WHEN", "FAILS_WHEN",
}
ALLOWED_CONFIDENCE = {"LOW", "MEDIUM", "HIGH"}

SYSTEM_PROMPT = """Ты Главный аналитик FATHER Knowledge Factory.
Работай ТОЛЬКО с кандидатами знаний из переданного батча одной книги.
Запрещено добавлять факты из памяти, интернета или других книг.
Не объявляй утверждение истинным только потому, что оно есть в книге.
Не продвигай ничего в KB.

Нужно: выявлять смысловые повторы, уточнять формулировки без нового смысла,
выявлять отношения между кандидатами и отмечать неоднозначности.

Решения: KEEP_CANDIDATE, REFINE_CANDIDATE, MERGE_EQUIVALENT,
HOLD_AMBIGUOUS, HOLD_LOW_EVIDENCE.

Отношения: SUPPORTS, CONTRADICTS, REFINES, SPECIALIZES, GENERALIZES,
USES_DIFFERENT_DEFINITION, ALTERNATIVE_TO, APPLIES_WHEN, FAILS_WHEN.

Верни только JSON без markdown. Каждый candidate_id текущего батча должен быть
представлен ровно один раз в reviews. Все relations могут ссылаться только на
candidate_id из текущего батча.
"""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def review_id(row: dict[str, Any]) -> str:
    return str(row.get("candidate_id") or row.get("candidate_group_id") or "").strip()


def heading(row: dict[str, Any]) -> str:
    value = row.get("heading_path")
    if isinstance(value, list):
        text = " > ".join(str(x) for x in value if str(x).strip())
        return text or "(NO_HEADING)"
    return str(value or "(NO_HEADING)").strip() or "(NO_HEADING)"


def make_batches(candidates: list[dict[str, Any]], batch_size: int) -> list[dict[str, Any]]:
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        if not review_id(row):
            raise ValueError("candidate missing candidate_id/candidate_group_id")
        groups[heading(row)].append(row)
    batches: list[dict[str, Any]] = []
    seq = 0
    for group_heading in sorted(groups):
        rows = sorted(
            groups[group_heading],
            key=lambda row: (-int(row.get("review_score") or 0), str(row.get("candidate_type") or ""), review_id(row)),
        )
        for start in range(0, len(rows), batch_size):
            chunk = rows[start:start + batch_size]
            seq += 1
            digest = hashlib.sha256("\x1f".join(review_id(row) for row in chunk).encode("utf-8")).hexdigest()[:12]
            batches.append({"batch_id": f"B{seq:04d}-{digest}", "heading": group_heading, "candidates": chunk})
    return batches


def http_json(url: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def discover_model(base_url: str, requested: str) -> tuple[str | None, list[str]]:
    if requested.strip():
        return requested.strip(), []
    payload = http_json(base_url.rstrip("/") + "/models", timeout=10)
    models = sorted(
        str(item.get("id") or "").strip()
        for item in payload.get("data", [])
        if isinstance(item, dict) and str(item.get("id") or "").strip()
    )
    return (models[0], models) if len(models) == 1 else (None, models)


def compact(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": review_id(row),
        "candidate_type": row.get("candidate_type"),
        "statement": row.get("statement"),
        "heading_path": row.get("heading_path"),
        "confidence": row.get("confidence"),
        "review_score": row.get("review_score"),
        "supporting_source_ids": row.get("supporting_source_ids") or [row.get("target_id")],
    }


def build_user_prompt(batch: dict[str, Any], book_title: str) -> str:
    body = {
        "book_title": book_title,
        "batch_id": batch["batch_id"],
        "heading": batch["heading"],
        "candidates": [compact(row) for row in batch["candidates"]],
        "required_output": {
            "schema_version": "1.0",
            "batch_id": batch["batch_id"],
            "topic": "краткая тема батча",
            "reviews": [{
                "candidate_id": "ID из входа",
                "decision": "одно допустимое решение",
                "canonical_statement": "уточненная формулировка без нового факта",
                "reason": "краткое обоснование только по текущему батчу",
                "relations": [{
                    "target_candidate_id": "другой ID текущего батча",
                    "type": "одно допустимое отношение",
                    "confidence": "LOW|MEDIUM|HIGH",
                    "reason": "краткое обоснование",
                }],
            }],
            "unresolved_questions": [],
            "kb_auto_promotion": False,
            "next_gate": "PROFESSOR_REVIEW_REQUIRED",
        },
    }
    return json.dumps(body, ensure_ascii=False, indent=2)


def extract_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        value = json.loads(cleaned)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start >= 0 and end > start:
        value = json.loads(cleaned[start:end + 1])
        if isinstance(value, dict):
            return value
    raise ValueError("model response does not contain JSON object")


def validate(result: dict[str, Any], batch: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {review_id(row) for row in batch["candidates"]}
    if result.get("batch_id") != batch["batch_id"]:
        errors.append("batch_id mismatch")
    if result.get("kb_auto_promotion") is not False:
        errors.append("kb_auto_promotion must be false")
    if result.get("next_gate") != "PROFESSOR_REVIEW_REQUIRED":
        errors.append("next_gate must be PROFESSOR_REVIEW_REQUIRED")
    reviews = result.get("reviews")
    if not isinstance(reviews, list):
        return errors + ["reviews must be list"]
    seen: list[str] = []
    for item in reviews:
        if not isinstance(item, dict):
            errors.append("review item must be object")
            continue
        cid = str(item.get("candidate_id") or "")
        seen.append(cid)
        if cid not in expected:
            errors.append(f"unknown candidate_id: {cid}")
        if item.get("decision") not in ALLOWED_DECISIONS:
            errors.append(f"invalid decision: {cid}")
        if not str(item.get("canonical_statement") or "").strip():
            errors.append(f"empty canonical_statement: {cid}")
        relations = item.get("relations", [])
        if not isinstance(relations, list):
            errors.append(f"relations not list: {cid}")
            continue
        for relation in relations:
            if not isinstance(relation, dict):
                errors.append(f"relation not object: {cid}")
                continue
            target = str(relation.get("target_candidate_id") or "")
            if target not in expected:
                errors.append(f"relation target outside batch: {target}")
            if target == cid:
                errors.append(f"self relation: {cid}")
            if relation.get("type") not in ALLOWED_RELATIONS:
                errors.append(f"invalid relation type: {cid}")
            if relation.get("confidence") not in ALLOWED_CONFIDENCE:
                errors.append(f"invalid relation confidence: {cid}")
    if set(seen) != expected or len(seen) != len(expected):
        errors.append("reviews must cover each candidate exactly once")
    return errors


def call_model(base_url: str, model: str, batch: dict[str, Any], book_title: str, timeout: int) -> tuple[dict[str, Any], dict[str, Any]]:
    payload = {
        "model": model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(batch, book_title)},
        ],
    }
    raw = http_json(base_url.rstrip("/") + "/chat/completions", payload=payload, timeout=timeout)
    choices = raw.get("choices") or []
    if not choices:
        raise ValueError("model response has no choices")
    content = str((choices[0].get("message") or {}).get("content") or "")
    usage = raw.get("usage") if isinstance(raw.get("usage"), dict) else {}
    return extract_object(content), usage


def safe_slug(value: str) -> str:
    result = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._-")
    return result[:80] or "model"


def build_professor_queue(run_dir: Path, batches: list[dict[str, Any]], book_title: str, model: str) -> bool:
    records = []
    for batch in batches:
        path = run_dir / f"{batch['batch_id']}.json"
        if not path.is_file():
            return False
        records.append(load_json(path))
    payload = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_PROFESSOR_REVIEW_QUEUE",
        "book_title": book_title,
        "main_analyst_model": model,
        "state": "PROFESSOR_REVIEW_REQUIRED",
        "kb_auto_promotion": False,
        "batches_total": len(records),
        "candidate_reviews_total": sum(len(row.get("reviews") or []) for row in records),
        "records": records,
    }
    PROFESSOR_QUEUE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Single-book Main Analyst for PROGRAMMING_KB.")
    parser.add_argument("--input", default=str(INPUT))
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--book-title", default=DEFAULT_BOOK_TITLE)
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--limit-batches", type=int, default=0, help="0 = all remaining batches")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--plan-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    source = Path(args.input)
    if not source.is_file():
        print(json.dumps({"status": "INPUT_MISSING", "input": str(source)}, ensure_ascii=False, indent=2))
        return 2
    payload = load_json(source)
    candidates = [row for row in payload.get("candidates", []) if isinstance(row, dict)]
    batches = make_batches(candidates, args.batch_size)
    plan = {
        "status": "PLAN_READY",
        "book_title": args.book_title,
        "candidates_total": len(candidates),
        "batches_total": len(batches),
        "batch_size_max": args.batch_size,
        "stream_mode": "1_STREAM_BASELINE",
        "kb_auto_promotion": False,
        "next_gate": "PROFESSOR_REVIEW_REQUIRED",
    }
    if args.plan_only:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    try:
        model, discovered = discover_model(args.base_url, args.model)
    except Exception as exc:
        print(json.dumps({**plan, "status": "BLOCKED", "reason": f"LLM_SERVER_UNAVAILABLE: {type(exc).__name__}: {exc}"}, ensure_ascii=False, indent=2))
        return 3
    if not model:
        print(json.dumps({**plan, "status": "BLOCKED", "reason": "MODEL_SELECTION_REQUIRED", "models_discovered": discovered}, ensure_ascii=False, indent=2))
        return 4

    run_dir = OUTPUT_ROOT / safe_slug(model)
    run_dir.mkdir(parents=True, exist_ok=True)
    completed_before = {path.stem for path in run_dir.glob("B*.json")}
    remaining = [batch for batch in batches if batch["batch_id"] not in completed_before]
    work = remaining if args.limit_batches <= 0 else remaining[:args.limit_batches]

    processed = reviewed = prompt_tokens = completion_tokens = 0
    failed_batch = None
    for index, batch in enumerate(work, 1):
        batch_started = time.perf_counter()
        print(f"main_analyst [{index}/{len(work)}] {batch['batch_id']} candidates={len(batch['candidates'])} heading={batch['heading']}")
        result = None
        usage: dict[str, Any] = {}
        last_error = ""
        for attempt in range(1, max(1, args.retries) + 1):
            try:
                candidate_result, candidate_usage = call_model(args.base_url, model, batch, args.book_title, args.timeout)
                errors = validate(candidate_result, batch)
                if errors:
                    raise ValueError("; ".join(errors))
                result, usage = candidate_result, candidate_usage
                break
            except Exception as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                print(f"retry={attempt} batch={batch['batch_id']} error={last_error}")
        if result is None:
            failed_batch = {"batch_id": batch["batch_id"], "error": last_error}
            break
        record = dict(result)
        record.update({
            "schema_version": "1.0",
            "record_type": "PROGRAMMER_BOOK_MAIN_ANALYST_BATCH_REVIEW",
            "book_title": args.book_title,
            "main_analyst_model": model,
            "kb_auto_promotion": False,
            "next_gate": "PROFESSOR_REVIEW_REQUIRED",
            "elapsed_seconds": round(time.perf_counter() - batch_started, 6),
            "usage": usage,
        })
        (run_dir / f"{batch['batch_id']}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        processed += 1
        reviewed += len(batch["candidates"])
        prompt_tokens += int(usage.get("prompt_tokens") or 0)
        completion_tokens += int(usage.get("completion_tokens") or 0)

    elapsed = time.perf_counter() - started
    completed_after = {path.stem for path in run_dir.glob("B*.json")}
    completed_total = sum(1 for batch in batches if batch["batch_id"] in completed_after)
    reviewed_total = sum(len(batch["candidates"]) for batch in batches if batch["batch_id"] in completed_after)
    remaining_total = len(batches) - completed_total
    throughput = reviewed / elapsed if reviewed and elapsed > 0 else None
    eta = round((elapsed / processed) * remaining_total, 3) if processed and remaining_total else None
    status = "PARTIAL_BLOCKED" if failed_batch else ("MAIN_ANALYST_COMPLETE" if remaining_total == 0 else "PASS")
    professor_ready = build_professor_queue(run_dir, batches, args.book_title, model) if status == "MAIN_ANALYST_COMPLETE" else False
    summary = {
        "schema_version": "1.0",
        "record_type": "PROGRAMMER_BOOK_MAIN_ANALYST_RUN",
        "status": status,
        "book_title": args.book_title,
        "model": model,
        "stream_mode": "1_STREAM_BASELINE",
        "candidates_total": len(candidates),
        "batches_total": len(batches),
        "batches_completed_total": completed_total,
        "batches_remaining_total": remaining_total,
        "candidates_reviewed_total": reviewed_total,
        "batches_processed_this_run": processed,
        "candidates_reviewed_this_run": reviewed,
        "elapsed_seconds": round(elapsed, 6),
        "throughput_candidates_per_second": round(throughput, 4) if throughput else None,
        "eta_seconds": eta,
        "speedup_vs_1_stream_pct": 0.0,
        "prompt_tokens_this_run": prompt_tokens or None,
        "completion_tokens_this_run": completion_tokens or None,
        "kb_auto_promotion": False,
        "next_gate": "PROFESSOR_REVIEW_REQUIRED",
        "professor_queue_ready": professor_ready,
        "output_dir": run_dir.relative_to(ROOT).as_posix(),
        "failed_batch": failed_batch,
    }
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 5 if failed_batch else 0


if __name__ == "__main__":
    raise SystemExit(main())
