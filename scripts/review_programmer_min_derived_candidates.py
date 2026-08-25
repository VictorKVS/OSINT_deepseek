from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "programmer_min_derived_review_policy.json"
SOURCES = ROOT / "config" / "knowledge_source_registry.json"
DERIVED = ROOT / "reports" / "programmer_training_gym" / "MIN_DERIVED_TASKS.json"
GOLDEN = ROOT / "reports" / "programmer_training_gym" / "GOLDEN_CASES_MIN.json"
EXPANSION_SCRIPT = ROOT / "scripts" / "build_programmer_min_expansion.py"
REFERENCE = ROOT / "training" / "programmer" / "min_reference_solutions.py"
REPORT_DIR = ROOT / "reports" / "programmer_training_gym"
REVIEWED = REPORT_DIR / "MIN_DERIVED_AUTOMATED_REVIEW.json"
LATEST = REPORT_DIR / "LATEST_PROGRAMMER_MIN_DERIVED_REVIEW.json"

HOLDOUT_IDS = {"PT-MIN-009", "PT-MIN-010", "PT-MIN-011", "PT-MIN-012"}
HOLDOUT_FUNCTIONS = {"validate_port", "top_k_frequent", "redact_secret", "backoff_schedule"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_alias_index(payload: dict[str, Any]) -> dict[str, str]:
    index: dict[str, str] = {}
    for row in payload.get("sources", []):
        if not isinstance(row, dict):
            continue
        source_id = str(row.get("source_id") or "")
        if source_id:
            index[source_id] = source_id
        for alias in row.get("aliases") or []:
            index[str(alias)] = source_id
    return index


def load_expansion_module():
    spec = importlib.util.spec_from_file_location("father_programmer_min_expansion", EXPANSION_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load expansion module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_python_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    marker = "```python"
    cursor = 0
    while True:
        start = text.find(marker, cursor)
        if start < 0:
            break
        body_start = start + len(marker)
        end = text.find("```", body_start)
        if end < 0:
            break
        blocks.append(text[body_start:end].strip())
        cursor = end + 3
    return blocks


def mutation_quality(expansion) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    states: dict[str, str] = {}
    buggy: dict[str, str] = dict(expansion.BUGGY_IMPLEMENTATIONS)
    expected = {
        "sum_positive",
        "stable_unique",
        "parse_ints",
        "first_index",
        "chunked",
        "safe_ratio",
        "word_frequency",
        "merge_sorted",
    }
    if set(buggy) != expected:
        errors.append("mutation registry does not cover exactly the 8 MIN Golden functions")
        return states, errors

    for name, source in buggy.items():
        try:
            ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"{name}: mutation is not syntactically valid: {exc}")
            states[name] = "FAIL_SYNTAX"
            continue
        if f"def {name}(" not in source:
            errors.append(f"{name}: mutation does not define the expected function")
            states[name] = "FAIL_FUNCTION_IDENTITY"
            continue

        # Deterministic evidence that every mutation contains a real contract defect.
        if name == "sum_positive":
            ok = "return sum(values)" in source
            reason = "includes negative values instead of summing only positives"
        elif name == "stable_unique":
            ok = "set(values)" in source
            reason = "set conversion does not preserve the first-seen order contract"
        elif name == "parse_ints":
            ok = "int(item)" in source and "isinstance(item, (int, str))" in source
            reason = "accepts bool through int and can raise on malformed strings"
        elif name == "first_index":
            ok = "return mid" in source
            reason = "returns an arbitrary matching midpoint rather than the leftmost match"
        elif name == "chunked":
            ok = "range(0, len(values), size)" in source and "size <= 0" not in source
            reason = "does not enforce the explicit size<=0 ValueError contract"
        elif name == "safe_ratio":
            ok = "return numerator / denominator" in source and "denominator == 0" not in source
            reason = "raises on zero denominator instead of returning default"
        elif name == "word_frequency":
            ok = ".lower()" in source
            reason = "normalizes case although the contract requires preserving it"
        elif name == "merge_sorted":
            ok = "sorted(" in source
            reason = "violates the explicit no-sorted linear merge contract"
        else:
            ok = False
            reason = "unregistered mutation rule"

        if not ok:
            errors.append(f"{name}: mutation defect is not provable by the registered contract check")
            states[name] = "FAIL_NOT_PROVEN"
        else:
            states[name] = f"PASS: {reason}"
    return states, errors


def normalize_parent_sources(parent: dict[str, Any]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for row in parent.get("source_refs") or []:
        if isinstance(row, dict):
            out.append((str(row.get("source_ref") or ""), str(row.get("source_id") or "")))
        else:
            out.append((str(row), ""))
    return out


def review(derived_path: Path, golden_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    started = time.perf_counter()
    policy = load_json(POLICY)
    sources = load_json(SOURCES)
    derived_payload = load_json(derived_path)
    golden_payload = load_json(golden_path)
    expansion = load_expansion_module()
    aliases = source_alias_index(sources)

    errors: list[str] = []
    if policy.get("policy_id") != "FATHER-PROGRAMMER-MIN-DERIVED-REVIEW-001":
        errors.append("unexpected derived review policy id")
    expected = policy.get("expected") or {}
    modes = tuple(expected.get("modes") or [])
    if modes != tuple(expansion.MODES):
        errors.append("review policy modes differ from executable expansion modes")

    mutation_states, mutation_errors = mutation_quality(expansion)
    errors.extend(mutation_errors)

    source_summary = derived_payload.get("summary") or {}
    tasks = [row for row in derived_payload.get("tasks", []) if isinstance(row, dict)]
    golden_summary = golden_payload.get("summary") or {}
    parents = [row for row in golden_payload.get("golden_cases", []) if isinstance(row, dict)]
    parent_index = {str(row.get("golden_case_id") or ""): row for row in parents}

    if source_summary.get("status") != "PASS":
        errors.append("derived source artifact summary is not PASS")
    if golden_summary.get("status") != "PASS":
        errors.append("Golden parent artifact summary is not PASS")
    if int(golden_summary.get("golden_approved_total") or 0) != int(expected.get("parents_total") or 0):
        errors.append("Golden parent count does not match review policy")
    if len(parents) != int(expected.get("parents_total") or 0):
        errors.append("Golden artifact does not contain the expected parent records")

    task_ids = [str(row.get("task_id") or "") for row in tasks]
    if len(tasks) != int(expected.get("tasks_total") or 0):
        errors.append(f"expected {expected.get('tasks_total')} derived tasks, got {len(tasks)}")
    if len(task_ids) != len(set(task_ids)):
        errors.append("derived task ids are not unique")

    mode_counts = Counter(str(row.get("derivation_mode") or "") for row in tasks)
    parent_counts = Counter(str(row.get("parent_golden_case_id") or "") for row in tasks)
    for mode in modes:
        if mode_counts[mode] != int(expected.get("tasks_per_mode") or 0):
            errors.append(f"{mode}: expected {expected.get('tasks_per_mode')} tasks, got {mode_counts[mode]}")
    if set(mode_counts) != set(modes):
        errors.append("unexpected derivation mode present")
    for parent_id in parent_index:
        if parent_counts[parent_id] != int(expected.get("tasks_per_parent") or 0):
            errors.append(f"{parent_id}: expected {expected.get('tasks_per_parent')} derived tasks, got {parent_counts[parent_id]}")
    if set(parent_counts) != set(parent_index):
        errors.append("derived corpus parent set differs from Golden parent set")

    reviewed: list[dict[str, Any]] = []
    for task in tasks:
        task_id = str(task.get("task_id") or "")
        mode = str(task.get("derivation_mode") or "")
        parent_id = str(task.get("parent_golden_case_id") or "")
        parent = parent_index.get(parent_id)
        task_errors: list[str] = []

        if task.get("split") != "TRAIN":
            task_errors.append("derived task is not TRAIN")
        if task.get("state") != "DERIVED_CANDIDATE_PENDING":
            task_errors.append("derived task state is not pending")
        if task.get("training_ready") is not False:
            task_errors.append("training_ready must remain false")
        if not parent:
            task_errors.append("parent Golden Case not found")
        else:
            parent_code = str(parent.get("code") or "")
            if task.get("parent_code_sha256") != sha256_text(parent_code):
                task_errors.append("parent code SHA mismatch")
            if parent.get("state") != "GOLDEN_APPROVED" or parent.get("training_ready") is not True:
                task_errors.append("parent is not approved/training-ready Golden")
            if parent.get("split") != "TRAIN" or parent.get("holdout_dependency") is not False:
                task_errors.append("parent violates TRAIN/HOLDOUT isolation")
            if task.get("parent_task_id") != parent.get("task_id"):
                task_errors.append("parent task id mismatch")
            if task.get("parent_reference_function") != parent.get("reference_function"):
                task_errors.append("parent reference function mismatch")

            inherited = normalize_parent_sources(parent)
            task_sources: list[tuple[str, str]] = []
            for row in task.get("source_refs") or []:
                if isinstance(row, dict):
                    task_sources.append((str(row.get("source_ref") or ""), str(row.get("source_id") or "")))
                else:
                    task_sources.append((str(row), ""))
            if task_sources != inherited:
                task_errors.append("derived source refs differ from parent source refs")
            for ref, source_id in task_sources:
                resolved = aliases.get(ref)
                if not resolved:
                    task_errors.append(f"unresolved source ref: {ref}")
                elif source_id and source_id != resolved:
                    task_errors.append(f"source id mismatch for {ref}")

        prompt = str(task.get("prompt") or "")
        if task_id not in prompt or f"Mode: {mode}" not in prompt or f"Parent: {parent_id}" not in prompt:
            task_errors.append("prompt identity header mismatch")

        text_for_leak = json.dumps(task, ensure_ascii=False)
        if any(value in text_for_leak for value in HOLDOUT_IDS | HOLDOUT_FUNCTIONS):
            task_errors.append("HOLDOUT identifier/function leaked into derived task")

        blocks = extract_python_blocks(prompt)
        parent_fn = str(task.get("parent_reference_function") or "")
        buggy_expected = expansion.BUGGY_IMPLEMENTATIONS.get(parent_fn)
        if mode in {"REPAIR_BUG", "CODE_REVIEW"}:
            if len(blocks) != 1:
                task_errors.append("repair/review prompt must contain exactly one Python mutation block")
            else:
                try:
                    ast.parse(blocks[0])
                except SyntaxError:
                    task_errors.append("mutation block is not syntactically valid")
                if buggy_expected is None or blocks[0].strip() != str(buggy_expected).strip():
                    task_errors.append("mutation block differs from registered deterministic mutation")
        elif mode == "EDGE_CASE_ANALYSIS":
            if len(blocks) != 1:
                task_errors.append("edge-case prompt must contain exactly one reference code block")
            elif parent and blocks[0].strip() != str(parent.get("code") or "").strip():
                task_errors.append("edge-case reference code differs from Golden parent")
        elif mode in {"IMPLEMENT_VARIANT", "WRITE_TESTS"}:
            if blocks:
                task_errors.append("implement/tests prompt must not expose parent or mutation code")

        passed = not task_errors
        reviewed.append({
            **task,
            "automated_review_state": "PASS" if passed else "FAIL",
            "automated_review_errors": task_errors,
            "state": "DERIVED_AUTOMATED_PASS_CRITIC_PENDING" if passed else "DERIVED_CANDIDATE_FAIL",
            "critic_review_state": "PENDING" if passed else "BLOCKED",
            "training_ready": False,
            "promotion_block_reason": "DERIVED_CRITIC_REVIEW_REQUIRED" if passed else "DERIVED_AUTOMATED_REVIEW_FAILED",
        })

    pass_total = sum(row.get("automated_review_state") == "PASS" for row in reviewed)
    fail_total = len(reviewed) - pass_total
    if fail_total:
        errors.append(f"{fail_total} derived candidates failed their per-task automated review")

    summary = {
        "record_type": "PROGRAMMER_MIN_DERIVED_CANDIDATE_REVIEW",
        "schema_version": "1.0",
        "status": "PASS" if not errors else "FAIL",
        "policy_id": policy.get("policy_id"),
        "tasks_total": len(reviewed),
        "automated_pass_total": pass_total,
        "automated_fail_total": fail_total,
        "critic_pending_total": pass_total,
        "training_ready_total": 0,
        "holdout_leak_total": sum(
            1 for row in reviewed if any(value in json.dumps(row, ensure_ascii=False) for value in HOLDOUT_IDS | HOLDOUT_FUNCTIONS)
        ),
        "mode_counts": dict(sorted(mode_counts.items())),
        "parent_counts": dict(sorted(parent_counts.items())),
        "mutation_quality_pass_total": sum(str(value).startswith("PASS") for value in mutation_states.values()),
        "mutation_quality": mutation_states,
        "validation_errors": errors,
        "elapsed_seconds": time.perf_counter() - started,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "note": "Automated review qualifies derived tasks for critic review only. No derived task is training-ready or Golden-approved at this stage.",
    }
    return summary, reviewed


def main() -> int:
    parser = argparse.ArgumentParser(description="Review 40 FATHER Programmer MIN derived candidates before critic/model generation.")
    parser.add_argument("--derived-file", default=str(DERIVED))
    parser.add_argument("--golden-file", default=str(GOLDEN))
    parser.add_argument("--validate-policy-only", action="store_true")
    args = parser.parse_args()

    if args.validate_policy_only:
        policy = load_json(POLICY)
        errors: list[str] = []
        if policy.get("policy_id") != "FATHER-PROGRAMMER-MIN-DERIVED-REVIEW-001":
            errors.append("unexpected derived review policy id")
        expansion = load_expansion_module()
        mutation_states, mutation_errors = mutation_quality(expansion)
        errors.extend(mutation_errors)
        payload = {
            "record_type": "PROGRAMMER_MIN_DERIVED_REVIEW_POLICY_VALIDATION",
            "status": "PASS" if not errors else "FAIL",
            "mutation_quality_pass_total": sum(str(value).startswith("PASS") for value in mutation_states.values()),
            "validation_errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not errors else 2

    derived_path = Path(args.derived_file)
    golden_path = Path(args.golden_file)
    if not derived_path.is_absolute():
        derived_path = ROOT / derived_path
    if not golden_path.is_absolute():
        golden_path = ROOT / golden_path
    missing = [str(path) for path in (derived_path, golden_path) if not path.exists()]
    if missing:
        payload = {
            "record_type": "PROGRAMMER_MIN_DERIVED_CANDIDATE_REVIEW",
            "status": "FAIL",
            "validation_errors": [f"required artifact not found: {path}" for path in missing],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    summary, reviewed = review(derived_path, golden_path)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWED.write_text(json.dumps({"summary": summary, "tasks": reviewed}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
