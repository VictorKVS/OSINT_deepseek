from __future__ import annotations

import argparse
import ast
import hashlib
import json
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "config" / "programmer_training_task_library.json"
SOURCES = ROOT / "config" / "knowledge_source_registry.json"
CRITIC = ROOT / "config" / "programmer_min_critic_decisions.json"
REFERENCE = ROOT / "training" / "programmer" / "min_reference_solutions.py"
REPORT_DIR = ROOT / "reports" / "programmer_training_gym"
CANDIDATES = REPORT_DIR / "GOLDEN_CASE_CANDIDATES.json"
GOLDEN = REPORT_DIR / "GOLDEN_CASES_MIN.json"
SFT = REPORT_DIR / "SFT_MIN_GOLDEN.jsonl"
LATEST = REPORT_DIR / "LATEST_PROGRAMMER_MIN_GOLDEN_PROMOTION.json"

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


def function_sources(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    lines = text.splitlines()
    result: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and hasattr(node, "end_lineno"):
            result[node.name] = "\n".join(lines[node.lineno - 1: int(node.end_lineno)])
    return result


def validate_critic_only() -> list[str]:
    errors: list[str] = []
    library = load_json(TASKS)
    critic = load_json(CRITIC)
    sources = load_json(SOURCES)
    aliases = source_alias_index(sources)
    train_ids = {
        str(row.get("task_id"))
        for row in library.get("tasks", [])
        if isinstance(row, dict) and row.get("split") == "TRAIN"
    }
    holdout_ids = {
        str(row.get("task_id"))
        for row in library.get("tasks", [])
        if isinstance(row, dict) and row.get("split") == "HOLDOUT"
    }
    decisions = [row for row in critic.get("decisions", []) if isinstance(row, dict)]
    decision_ids = {str(row.get("task_id")) for row in decisions}
    if train_ids != set(TASK_TO_FUNCTION):
        errors.append("TRAIN task ids do not match promotion map")
    if decision_ids != train_ids:
        errors.append("critic decisions must cover every and only TRAIN task")
    if decision_ids & holdout_ids:
        errors.append("HOLDOUT task leaked into critic approvals")
    required_gates = {
        "requirements_satisfied",
        "edge_cases_adequately_covered",
        "algorithmic_choice_appropriate",
        "security_implications_reviewed",
        "decision_summary_source_traceable",
        "no_holdout_dependency",
    }
    for row in decisions:
        task_id = str(row.get("task_id") or "")
        if row.get("decision") != "APPROVE":
            errors.append(f"{task_id}: decision is not APPROVE")
        gates = row.get("gates") or {}
        if set(gates) != required_gates:
            errors.append(f"{task_id}: critic gates are incomplete")
        for gate, state in gates.items():
            if not str(state).startswith("PASS"):
                errors.append(f"{task_id}: critic gate {gate} did not pass")
        for ref in row.get("source_refs") or []:
            if str(ref) not in aliases:
                errors.append(f"{task_id}: unresolved critic source ref {ref}")
        if not str(row.get("decision_summary") or "").strip():
            errors.append(f"{task_id}: empty decision summary")
    return errors


def build_promotion(candidate_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    started = time.perf_counter()
    errors = validate_critic_only()
    library = load_json(TASKS)
    critic = load_json(CRITIC)
    candidate_payload = load_json(candidate_path)
    sources = load_json(SOURCES)
    aliases = source_alias_index(sources)
    code = function_sources(REFERENCE)

    task_index = {str(row["task_id"]): row for row in library.get("tasks", []) if isinstance(row, dict)}
    decision_index = {str(row["task_id"]): row for row in critic.get("decisions", []) if isinstance(row, dict)}
    candidates = [row for row in candidate_payload.get("candidates", []) if isinstance(row, dict)]
    candidate_index = {str(row.get("task_id")): row for row in candidates}
    summary_in = candidate_payload.get("summary") or {}

    current_ref_sha = sha256_file(REFERENCE)
    current_source_sha = sha256_file(SOURCES)
    if summary_in.get("status") != "PASS":
        errors.append("candidate summary is not PASS")
    if int(summary_in.get("candidate_fail_total") or 0) != 0:
        errors.append("candidate summary contains failed candidates")
    if int(summary_in.get("candidate_pass_total") or 0) != 8:
        errors.append("candidate summary does not contain 8 passing candidates")
    if summary_in.get("targeted_regression_tests") != "PASS":
        errors.append("targeted regression tests are not PASS")
    if int(summary_in.get("holdout_implementation_leak_total") or 0) != 0:
        errors.append("HOLDOUT implementation leakage detected")
    if summary_in.get("reference_solution_sha256") != current_ref_sha:
        errors.append("candidate artifact reference-solution SHA does not match current reference code")
    if summary_in.get("source_registry_sha256") != current_source_sha:
        errors.append("candidate artifact source-registry SHA does not match current source registry")

    golden: list[dict[str, Any]] = []
    sft: list[dict[str, Any]] = []
    for task_id, function_name in TASK_TO_FUNCTION.items():
        task = task_index.get(task_id)
        candidate = candidate_index.get(task_id)
        decision = decision_index.get(task_id)
        if not task or task.get("split") != "TRAIN":
            errors.append(f"{task_id}: missing TRAIN task")
            continue
        if not candidate or candidate.get("state") != "CANDIDATE_PASS_CRITIC_PENDING":
            errors.append(f"{task_id}: candidate is not pass/pending")
            continue
        if candidate.get("training_ready") is not False:
            errors.append(f"{task_id}: unexpected pre-promotion training_ready state")
        if not decision or decision.get("decision") != "APPROVE":
            errors.append(f"{task_id}: missing APPROVE critic decision")
            continue
        if function_name not in code:
            errors.append(f"{task_id}: reference function source missing")
            continue
        task_refs = [str(ref) for ref in task.get("source_refs") or []]
        decision_refs = [str(ref) for ref in decision.get("source_refs") or []]
        if task_refs != decision_refs:
            errors.append(f"{task_id}: critic source refs differ from task source refs")
        resolved = []
        for ref in task_refs:
            source_id = aliases.get(ref)
            if not source_id:
                errors.append(f"{task_id}: unresolved source ref during promotion: {ref}")
            else:
                resolved.append({"source_ref": ref, "source_id": source_id})
        golden_record = {
            "record_type": "PROGRAMMER_GOLDEN_CASE",
            "golden_case_id": f"GC-{task_id}",
            "golden_case_version": "1.0",
            "task_id": task_id,
            "split": "TRAIN",
            "maturity_level": "MIN",
            "importance_class": "NECESSARY",
            "domain": task.get("domain"),
            "title": task.get("title"),
            "state": "GOLDEN_APPROVED",
            "training_ready": True,
            "reference_function": function_name,
            "reference_solution_sha256": current_ref_sha,
            "source_registry_sha256": current_source_sha,
            "source_refs": resolved,
            "critic_decision_set": critic.get("decision_set_id"),
            "critic_decision": "APPROVE",
            "decision_summary": decision.get("decision_summary"),
            "code": code[function_name],
            "holdout_dependency": False,
        }
        golden.append(golden_record)
        constraints = "\n".join(f"- {item}" for item in task.get("constraints") or [])
        source_text = ", ".join(task_refs)
        assistant = (
            f"Краткое решение: {decision.get('decision_summary')}\n\n"
            f"```python\n{code[function_name]}\n```\n\n"
            f"Проверка: контракт и regression checks PASS. Источники: {source_text}."
        )
        sft.append({
            "record_type": "PROGRAMMER_SFT_EXAMPLE",
            "golden_case_id": f"GC-{task_id}",
            "messages": [
                {
                    "role": "system",
                    "content": "Ты FATHER Programmer. Решай задачу профессионально, кратко фиксируй решение и ограничения, пиши проверяемый код; не раскрывай длинную скрытую цепочку рассуждений."
                },
                {
                    "role": "user",
                    "content": f"{task.get('title')}\n\n{task.get('prompt')}\n\nИнтерфейс: {task.get('interface')}\nОграничения:\n{constraints}"
                },
                {"role": "assistant", "content": assistant},
            ],
            "source_refs": resolved,
            "split": "TRAIN",
            "maturity_level": "MIN",
        })

    if errors:
        golden = []
        sft = []
    summary = {
        "record_type": "PROGRAMMER_MIN_GOLDEN_PROMOTION",
        "schema_version": "1.0",
        "status": "PASS" if not errors else "FAIL",
        "critic_decision_set": critic.get("decision_set_id"),
        "candidate_artifact": candidate_path.relative_to(ROOT).as_posix() if candidate_path.is_relative_to(ROOT) else str(candidate_path),
        "candidate_regression_engine": summary_in.get("targeted_regression_engine"),
        "candidate_pass_total": int(summary_in.get("candidate_pass_total") or 0),
        "critic_approve_total": sum(row.get("decision") == "APPROVE" for row in decision_index.values()),
        "golden_approved_total": len(golden),
        "training_ready_total": len(sft),
        "holdout_exported_total": 0,
        "reference_solution_sha256": current_ref_sha,
        "source_registry_sha256": current_source_sha,
        "validation_errors": errors,
        "elapsed_seconds": time.perf_counter() - started,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "note": "Promotion is hash-bound to the local passing candidate artifact and explicit professor critic decisions. No model training is performed."
    }
    return summary, golden, sft


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote reviewed FATHER Programmer MIN candidates into Golden Cases and SFT records.")
    parser.add_argument("--candidate-file", default=str(CANDIDATES))
    parser.add_argument("--validate-critic-only", action="store_true")
    args = parser.parse_args()

    if args.validate_critic_only:
        errors = validate_critic_only()
        payload = {
            "record_type": "PROGRAMMER_MIN_CRITIC_VALIDATION",
            "status": "PASS" if not errors else "FAIL",
            "critic_approve_total": 8 if not errors else 0,
            "validation_errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not errors else 2

    candidate_path = Path(args.candidate_file)
    if not candidate_path.is_absolute():
        candidate_path = ROOT / candidate_path
    if not candidate_path.exists():
        payload = {
            "record_type": "PROGRAMMER_MIN_GOLDEN_PROMOTION",
            "status": "FAIL",
            "validation_errors": [f"candidate artifact not found: {candidate_path}"],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    summary, golden, sft = build_promotion(candidate_path)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    GOLDEN.write_text(json.dumps({"summary": summary, "golden_cases": golden}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with SFT.open("w", encoding="utf-8") as fh:
        for row in sft:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    LATEST.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
