from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "config" / "programmer_training_task_library.json"
SOURCES = ROOT / "config" / "knowledge_source_registry.json"
POLICY = ROOT / "config" / "programmer_golden_case_review_policy.json"
REFERENCE = ROOT / "training" / "programmer" / "min_reference_solutions.py"
REPORT_DIR = ROOT / "reports" / "programmer_training_gym"
REPORT = REPORT_DIR / "GOLDEN_CASE_CANDIDATES.json"
LATEST = REPORT_DIR / "LATEST_PROGRAMMER_GOLDEN_CANDIDATE_REVIEW.json"

TASK_TO_FUNCTION = {
    "PT-MIN-001": "sum_positive",
    "PT-MIN-002": "stable_unique",
    "PT-MIN-003": "parse_ints",
    "PT-MIN-004": "first_index",
    "PT-MIN-005": "chunked",
    "PT-MIN-006": "safe_ratio",
    "PT-MIN-007": "word_frequency",
    "PT-MIN-008": "merge_sorted",
}
HOLDOUT_FUNCTIONS = {"validate_port", "top_k_frequent", "redact_secret", "backoff_schedule"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def reference_functions_present() -> tuple[set[str], set[str]]:
    text = REFERENCE.read_text(encoding="utf-8")
    present = {name for name in TASK_TO_FUNCTION.values() if f"def {name}(" in text}
    holdout_present = {name for name in HOLDOUT_FUNCTIONS if f"def {name}(" in text}
    return present, holdout_present


def run_targeted_tests() -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_programmer_training_reference_solutions.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    output = (proc.stdout + "\n" + proc.stderr).strip()
    return proc.returncode == 0, output[-6000:]


def build_candidates(*, run_tests: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    started = time.perf_counter()
    library = load_json(TASKS)
    sources = load_json(SOURCES)
    policy = load_json(POLICY)
    aliases = source_alias_index(sources)
    present, holdout_present = reference_functions_present()
    train_tasks = [row for row in library.get("tasks", []) if isinstance(row, dict) and row.get("split") == "TRAIN"]

    validation_errors: list[str] = []
    if policy.get("policy_id") != "FATHER-PROGRAMMER-GOLDEN-CASE-REVIEW-001":
        validation_errors.append("unexpected golden review policy id")
    if len(train_tasks) != 8:
        validation_errors.append(f"expected 8 TRAIN tasks, got {len(train_tasks)}")
    if holdout_present:
        validation_errors.append("HOLDOUT implementations are present: " + ", ".join(sorted(holdout_present)))

    regression_pass = None
    regression_output = "NOT_RUN"
    if run_tests and not validation_errors:
        regression_pass, regression_output = run_targeted_tests()
        if not regression_pass:
            validation_errors.append("targeted regression tests failed")

    candidates: list[dict[str, Any]] = []
    for task in train_tasks:
        task_id = str(task.get("task_id") or "")
        function_name = TASK_TO_FUNCTION.get(task_id)
        resolved_sources: list[dict[str, str]] = []
        unresolved_sources: list[str] = []
        for source_ref in task.get("source_refs") or []:
            ref = str(source_ref)
            source_id = aliases.get(ref)
            if source_id:
                resolved_sources.append({"source_ref": ref, "source_id": source_id})
            else:
                unresolved_sources.append(ref)
        function_exists = bool(function_name and function_name in present)
        automated_pass = function_exists and not unresolved_sources and not holdout_present
        if run_tests:
            automated_pass = automated_pass and bool(regression_pass)
        state = "CANDIDATE_PASS_CRITIC_PENDING" if automated_pass else "CANDIDATE_FAIL"
        candidates.append({
            "record_type": "PROGRAMMER_GOLDEN_CASE_CANDIDATE",
            "task_id": task_id,
            "title": task.get("title"),
            "domain": task.get("domain"),
            "maturity_level": "MIN",
            "importance_class": "NECESSARY",
            "split": "TRAIN",
            "reference_function": function_name,
            "reference_solution_ref": f"training/programmer/min_reference_solutions.py#{function_name}" if function_name else None,
            "reference_solution_sha256": sha256_file(REFERENCE),
            "resolved_sources": resolved_sources,
            "unresolved_sources": unresolved_sources,
            "checks": {
                "reference_implementation_exists": function_exists,
                "holdout_implementation_absent": not holdout_present,
                "source_refs_resolved": not unresolved_sources,
                "targeted_regression_tests": "PASS" if regression_pass is True else "FAIL" if regression_pass is False else "NOT_RUN",
            },
            "state": state,
            "critic_review_state": "PENDING" if automated_pass else "BLOCKED",
            "training_ready": False,
            "promotion_block_reason": "CRITIC_REVIEW_AND_EXPLICIT_APPROVAL_REQUIRED" if automated_pass else "AUTOMATED_GATE_FAILED",
        })

    passed = sum(row["state"] == "CANDIDATE_PASS_CRITIC_PENDING" for row in candidates)
    failed = len(candidates) - passed
    summary = {
        "record_type": "PROGRAMMER_GOLDEN_CANDIDATE_REVIEW",
        "schema_version": "1.0",
        "status": "PASS" if failed == 0 and not validation_errors else "FAIL",
        "policy_id": policy.get("policy_id"),
        "tasks_total": len(candidates),
        "candidate_pass_total": passed,
        "candidate_fail_total": failed,
        "golden_approved_total": 0,
        "training_ready_total": 0,
        "holdout_implementation_leak_total": len(holdout_present),
        "targeted_regression_tests": "PASS" if regression_pass is True else "FAIL" if regression_pass is False else "NOT_RUN",
        "validation_errors": validation_errors,
        "reference_solution_sha256": sha256_file(REFERENCE),
        "source_registry_sha256": sha256_file(SOURCES),
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "elapsed_seconds": time.perf_counter() - started,
        "note": "Automated PASS creates candidates only. Golden approval still requires critic review and explicit promotion."
    }
    return summary, candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Review FATHER Programmer MIN reference solutions into Golden Case candidates.")
    parser.add_argument("--validate-only", action="store_true", help="Validate metadata/source bindings without executing pytest.")
    args = parser.parse_args()
    summary, candidates = build_candidates(run_tests=not args.validate_only)
    if not args.validate_only:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps({"summary": summary, "candidates": candidates}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
