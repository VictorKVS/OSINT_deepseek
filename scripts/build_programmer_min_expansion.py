from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "programmer_min_expansion_policy.json"
GOLDEN = ROOT / "reports" / "programmer_training_gym" / "GOLDEN_CASES_MIN.json"
REPORT_DIR = ROOT / "reports" / "programmer_training_gym"
OUT_TASKS = REPORT_DIR / "MIN_DERIVED_TASKS.json"
OUT_PROMPTS = REPORT_DIR / "MIN_DERIVED_PROMPTS.jsonl"
LATEST = REPORT_DIR / "LATEST_PROGRAMMER_MIN_EXPANSION.json"

MODES = (
    "IMPLEMENT_VARIANT",
    "REPAIR_BUG",
    "WRITE_TESTS",
    "CODE_REVIEW",
    "EDGE_CASE_ANALYSIS",
)

BUGGY_IMPLEMENTATIONS: dict[str, str] = {
    "sum_positive": "def sum_positive(values):\n    return sum(values)",
    "stable_unique": "def stable_unique(values):\n    return list(set(values))",
    "parse_ints": "def parse_ints(items):\n    return [int(item) for item in items if isinstance(item, (int, str))]",
    "first_index": "def first_index(sorted_values, target):\n    lo, hi = 0, len(sorted_values) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if sorted_values[mid] == target:\n            return mid\n        if sorted_values[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1",
    "chunked": "def chunked(values, size):\n    return [values[i:i + size] for i in range(0, len(values), size)]",
    "safe_ratio": "def safe_ratio(numerator, denominator, default=None):\n    return numerator / denominator",
    "word_frequency": "def word_frequency(words):\n    counts = {}\n    for word in words:\n        key = word.lower()\n        counts[key] = counts.get(key, 0) + 1\n    return counts",
    "merge_sorted": "def merge_sorted(left, right):\n    return sorted(left + right)",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_policy(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if policy.get("policy_id") != "FATHER-PROGRAMMER-MIN-EXPANSION-001":
        errors.append("unexpected expansion policy id")
    derivation = policy.get("derivation") or {}
    if tuple(derivation.get("modes") or []) != MODES:
        errors.append("derivation modes differ from executable contract")
    if int(derivation.get("tasks_per_parent") or 0) != len(MODES):
        errors.append("tasks_per_parent must equal derivation mode count")
    if int(derivation.get("expected_total") or 0) != 40:
        errors.append("expected_total must be 40 for the MIN expansion seed")
    rules = policy.get("derived_candidate_rules") or {}
    if rules.get("training_ready_default") is not False:
        errors.append("derived candidates must default to training_ready=false")
    if rules.get("critic_review_required_before_training_export") is not True:
        errors.append("critic review must be required before derived training export")
    if rules.get("no_auto_promotion") is not True:
        errors.append("derived tasks must not auto-promote")
    return errors


def validate_golden_payload(payload: dict[str, Any], policy: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    summary = payload.get("summary") or {}
    cases = [row for row in payload.get("golden_cases", []) if isinstance(row, dict)]
    req = policy.get("parent_requirements") or {}
    expected = int(req.get("golden_cases_required") or 0)
    if summary.get("status") != req.get("promotion_summary_status"):
        errors.append("golden promotion summary is not PASS")
    if int(summary.get("golden_approved_total") or 0) != expected:
        errors.append(f"expected {expected} approved goldens in summary")
    if int(summary.get("holdout_exported_total") or 0) != int(req.get("holdout_exported_total") or 0):
        errors.append("golden summary reports HOLDOUT export")
    if len(cases) != expected:
        errors.append(f"expected {expected} golden case records, got {len(cases)}")
    ids: set[str] = set()
    for row in cases:
        gid = str(row.get("golden_case_id") or "")
        if not gid or gid in ids:
            errors.append(f"invalid or duplicate golden_case_id: {gid!r}")
        ids.add(gid)
        if row.get("state") != req.get("state"):
            errors.append(f"{gid}: parent state is not GOLDEN_APPROVED")
        if row.get("training_ready") is not True:
            errors.append(f"{gid}: parent is not training_ready")
        if row.get("split") != req.get("split"):
            errors.append(f"{gid}: parent is not TRAIN")
        if row.get("holdout_dependency") is not False:
            errors.append(f"{gid}: parent has HOLDOUT dependency")
        if not str(row.get("code") or "").strip():
            errors.append(f"{gid}: parent code is empty")
        if not row.get("source_refs"):
            errors.append(f"{gid}: parent source refs are empty")
        fn = str(row.get("reference_function") or "")
        if fn not in BUGGY_IMPLEMENTATIONS:
            errors.append(f"{gid}: no deterministic bug mutation registered for {fn}")
    return errors, cases


def prompt_for(parent: dict[str, Any], mode: str, derived_id: str) -> str:
    title = str(parent.get("title") or parent.get("task_id") or parent.get("golden_case_id"))
    fn = str(parent.get("reference_function") or "")
    code = str(parent.get("code") or "")
    buggy = BUGGY_IMPLEMENTATIONS.get(fn, "")
    decision = str(parent.get("decision_summary") or "")
    if mode == "IMPLEMENT_VARIANT":
        body = (
            f"Реализуй задачу заново по контракту исходного Golden Case: {title}. "
            "Не копируй эталон дословно. Сохрани наблюдаемое поведение, ограничения и требуемую сложность. "
            "Дай краткий план, код и набор проверок."
        )
    elif mode == "REPAIR_BUG":
        body = (
            f"Ниже дефектная реализация задачи {title}. Найди конкретный дефект, исправь код и предложи regression tests.\n\n"
            f"```python\n{buggy}\n```"
        )
    elif mode == "WRITE_TESTS":
        body = (
            f"Для задачи {title} спроектируй компактный набор тестов: normal, boundary, invalid/failure where applicable, "
            "а также проверки немодификации входов и сложности, если это часть контракта. Код эталона не переписывай."
        )
    elif mode == "CODE_REVIEW":
        body = (
            f"Проведи code review дефектной реализации задачи {title}. Сопоставь её с контрактом и инженерным решением: {decision}. "
            "Перечисли дефекты по важности и предложи минимально достаточное исправление.\n\n"
            f"```python\n{buggy}\n```"
        )
    elif mode == "EDGE_CASE_ANALYSIS":
        body = (
            f"Для Golden Case {title} выпиши граничные случаи, инварианты и возможные ошибки реализации. "
            "Для каждого укажи конкретную проверку. Используй эталон только как доказательную опору, а не как текст для копирования.\n\n"
            f"Reference implementation:\n```python\n{code}\n```"
        )
    else:
        raise ValueError(mode)
    return f"Derived task {derived_id}\nMode: {mode}\nParent: {parent.get('golden_case_id')}\n\n{body}"


def derive_tasks(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    derived: list[dict[str, Any]] = []
    for parent_index, parent in enumerate(sorted(cases, key=lambda row: str(row.get("golden_case_id"))), start=1):
        parent_code = str(parent.get("code") or "")
        parent_sha = sha256_text(parent_code)
        for mode_index, mode in enumerate(MODES, start=1):
            derived_id = f"PT-MIN-DER-{parent_index:02d}-{mode_index:02d}"
            derived.append({
                "record_type": "PROGRAMMER_DERIVED_TASK_CANDIDATE",
                "task_id": derived_id,
                "split": "TRAIN",
                "maturity_level": "MIN",
                "importance_class": "NECESSARY",
                "synthetic_derivation": True,
                "derivation_mode": mode,
                "parent_golden_case_id": parent.get("golden_case_id"),
                "parent_task_id": parent.get("task_id"),
                "parent_reference_function": parent.get("reference_function"),
                "parent_code_sha256": parent_sha,
                "domain": parent.get("domain"),
                "source_refs": parent.get("source_refs"),
                "prompt": prompt_for(parent, mode, derived_id),
                "expected_evidence": [
                    "parent golden remains hash-compatible",
                    "response satisfies parent contract",
                    "no HOLDOUT dependency",
                    "source refs remain traceable",
                    "automated checks and critic review before training export",
                ],
                "state": "DERIVED_CANDIDATE_PENDING",
                "training_ready": False,
                "promotion_block_reason": "DERIVED_AUTOMATED_AND_CRITIC_REVIEW_REQUIRED",
            })
    return derived


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand 8 reviewed Programmer MIN Golden Cases into 40 derived training candidates.")
    parser.add_argument("--golden-file", default=str(GOLDEN))
    parser.add_argument("--validate-policy-only", action="store_true")
    args = parser.parse_args()

    started = time.perf_counter()
    policy = load_json(POLICY)
    errors = validate_policy(policy)
    if args.validate_policy_only:
        payload = {
            "record_type": "PROGRAMMER_MIN_EXPANSION_POLICY_VALIDATION",
            "status": "PASS" if not errors else "FAIL",
            "validation_errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not errors else 2

    golden_path = Path(args.golden_file)
    if not golden_path.is_absolute():
        golden_path = ROOT / golden_path
    if not golden_path.exists():
        errors.append(f"golden artifact not found: {golden_path}")
        cases: list[dict[str, Any]] = []
    else:
        golden_payload = load_json(golden_path)
        golden_errors, cases = validate_golden_payload(golden_payload, policy)
        errors.extend(golden_errors)

    derived = derive_tasks(cases) if not errors else []
    ids = [str(row.get("task_id")) for row in derived]
    mode_counts = Counter(str(row.get("derivation_mode")) for row in derived)
    parent_counts = Counter(str(row.get("parent_golden_case_id")) for row in derived)
    if derived:
        if len(derived) != 40:
            errors.append(f"expected 40 derived tasks, got {len(derived)}")
        if len(ids) != len(set(ids)):
            errors.append("derived task ids are not unique")
        if set(mode_counts) != set(MODES) or any(mode_counts[mode] != 8 for mode in MODES):
            errors.append("expected exactly 8 tasks per derivation mode")
        if len(parent_counts) != 8 or any(count != 5 for count in parent_counts.values()):
            errors.append("expected exactly 5 derived tasks per parent Golden Case")
        if any(row.get("training_ready") is not False for row in derived):
            errors.append("derived candidates must not be training_ready")
        if any(str(row.get("parent_task_id") or "").startswith("PT-MIN-00") and int(str(row.get("parent_task_id"))[-3:]) >= 9 for row in derived if str(row.get("parent_task_id") or "").startswith("PT-MIN-")):
            errors.append("HOLDOUT parent detected in derived corpus")

    if errors:
        derived = []
    summary = {
        "record_type": "PROGRAMMER_MIN_GOLDEN_EXPANSION",
        "schema_version": "1.0",
        "status": "PASS" if not errors else "FAIL",
        "policy_id": policy.get("policy_id"),
        "parent_golden_total": len(cases) if not errors else 0,
        "derived_candidates_total": len(derived),
        "training_ready_total": 0,
        "golden_approved_total": 0,
        "holdout_derived_total": 0,
        "mode_counts": dict(sorted(mode_counts.items())) if not errors else {},
        "validation_errors": errors,
        "elapsed_seconds": time.perf_counter() - started,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "note": "Derived tasks expand skill modes from reviewed Golden parents. They are not training-ready until their own automated and critic review gates pass.",
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_TASKS.write_text(json.dumps({"summary": summary, "tasks": derived}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with OUT_PROMPTS.open("w", encoding="utf-8") as fh:
        for row in derived:
            fh.write(json.dumps({
                "record_type": "PROGRAMMER_DERIVED_PROMPT",
                "task_id": row["task_id"],
                "derivation_mode": row["derivation_mode"],
                "parent_golden_case_id": row["parent_golden_case_id"],
                "messages": [
                    {"role": "system", "content": "Ты FATHER Programmer. Выполняй инженерную задачу проверяемо, кратко фиксируй решение и опирайся на указанный контракт и источники."},
                    {"role": "user", "content": row["prompt"]},
                ],
                "source_refs": row["source_refs"],
                "training_ready": False,
            }, ensure_ascii=False, sort_keys=True) + "\n")
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
