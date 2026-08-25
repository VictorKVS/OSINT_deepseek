from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config" / "programmer_training_gym_policy.json"
TASKS = ROOT / "config" / "programmer_training_task_library.json"
REPORT_DIR = ROOT / "reports" / "programmer_training_gym"

ALLOWED_SPLITS = {"TRAIN", "HOLDOUT"}
ALLOWED_MATURITY = {"MIN", "MEDIUM", "MAX"}
ALLOWED_IMPORTANCE = {"NECESSARY", "DESIRABLE", "INTERESTING_LATER"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate(policy: dict[str, Any], library: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if policy.get("policy_id") != "FATHER-PROGRAMMER-TRAINING-GYM-001":
        errors.append("unexpected training policy id")
    if library.get("role_id") != "PROGRAMMER":
        errors.append("task library role must be PROGRAMMER")
    if library.get("maturity_level") not in ALLOWED_MATURITY:
        errors.append("invalid library maturity_level")
    if library.get("importance_class") not in ALLOWED_IMPORTANCE:
        errors.append("invalid library importance_class")

    tasks = library.get("tasks") or []
    if not isinstance(tasks, list) or not tasks:
        errors.append("task library is empty")
        return errors

    ids: set[str] = set()
    split_counts: Counter[str] = Counter()
    for index, task in enumerate(tasks, start=1):
        if not isinstance(task, dict):
            errors.append(f"task #{index} is not an object")
            continue
        task_id = str(task.get("task_id") or "")
        if not task_id:
            errors.append(f"task #{index} has no task_id")
        elif task_id in ids:
            errors.append(f"duplicate task_id: {task_id}")
        else:
            ids.add(task_id)
        split = str(task.get("split") or "")
        if split not in ALLOWED_SPLITS:
            errors.append(f"{task_id}: invalid split {split!r}")
        else:
            split_counts[split] += 1
        for required in ("domain", "title", "prompt", "interface", "constraints", "competencies", "source_refs", "evaluation"):
            if required not in task:
                errors.append(f"{task_id}: missing {required}")
        source_refs = task.get("source_refs") or []
        if not isinstance(source_refs, list) or not source_refs:
            errors.append(f"{task_id}: source_refs must be non-empty")
        evaluation = task.get("evaluation") or {}
        if not isinstance(evaluation, dict) or evaluation.get("kind") != "PURE_FUNCTION":
            errors.append(f"{task_id}: MIN seed requires PURE_FUNCTION evaluation")

    expected = library.get("split_policy") or {}
    for split in ALLOWED_SPLITS:
        if split in expected and int(expected[split]) != split_counts[split]:
            errors.append(f"split count mismatch for {split}: expected {expected[split]}, got {split_counts[split]}")
    if expected.get("no_overlap") is not True:
        errors.append("split policy must require no_overlap")
    return errors


def training_prompt(task: dict[str, Any]) -> dict[str, Any]:
    source_refs = ", ".join(str(x) for x in task.get("source_refs") or [])
    constraints = "\n".join(f"- {x}" for x in task.get("constraints") or [])
    return {
        "record_type": "PROGRAMMER_TRAINING_PROMPT",
        "task_id": task["task_id"],
        "split": "TRAIN",
        "maturity_level": "MIN",
        "importance_class": "NECESSARY",
        "domain": task["domain"],
        "system": (
            "Ты FATHER Programmer. Решай задачу профессионально и проверяемо. "
            "Сначала дай краткий план и явно укажи важные допущения, затем реализацию и тестовые идеи. "
            "Не выдавай длинную скрытую цепочку рассуждений. Учитывай указанные ограничения и источники."
        ),
        "user": (
            f"Задача: {task['title']}\n\n{task['prompt']}\n\n"
            f"Интерфейс: {task['interface']}\n\nОграничения:\n{constraints}\n\n"
            f"Источник/основание для проверки: {source_refs}"
        ),
        "golden_answer_ref": None,
        "training_ready": False,
        "block_reason": "GOLDEN_CASE_NOT_APPROVED"
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the FATHER Programmer MIN training-gym manifest and prompt set.")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    started = time.perf_counter()
    policy = load_json(POLICY)
    library = load_json(TASKS)
    errors = validate(policy, library)
    tasks = [row for row in library.get("tasks", []) if isinstance(row, dict)]
    train = [row for row in tasks if row.get("split") == "TRAIN"]
    holdout = [row for row in tasks if row.get("split") == "HOLDOUT"]

    summary = {
        "record_type": "PROGRAMMER_TRAINING_GYM_BUILD",
        "schema_version": "1.0",
        "status": "PASS" if not errors else "FAIL",
        "policy_id": policy.get("policy_id"),
        "library_id": library.get("library_id"),
        "maturity_level": library.get("maturity_level"),
        "importance_class": library.get("importance_class"),
        "tasks_total": len(tasks),
        "train_tasks_total": len(train),
        "holdout_tasks_total": len(holdout),
        "golden_cases_total": 0,
        "training_examples_total": 0,
        "domains": dict(sorted(Counter(str(row.get("domain")) for row in tasks).items())),
        "validation_errors": errors,
        "speedup_vs_1_stream_pct": None,
        "eta_seconds": None,
        "elapsed_seconds": time.perf_counter() - started,
        "note": "No model quality or training speed is claimed; this run only validates and packages the MIN task corpus."
    }

    if not args.validate_only:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(REPORT_DIR / "TASK_MANIFEST.json", {
            "library_id": library.get("library_id"),
            "tasks": [
                {
                    "task_id": row.get("task_id"),
                    "split": row.get("split"),
                    "domain": row.get("domain"),
                    "title": row.get("title"),
                    "competencies": row.get("competencies"),
                    "source_refs": row.get("source_refs")
                }
                for row in tasks
            ]
        })
        with (REPORT_DIR / "TRAIN_PROMPTS.jsonl").open("w", encoding="utf-8") as fh:
            for row in train:
                fh.write(json.dumps(training_prompt(row), ensure_ascii=False, sort_keys=True) + "\n")
        write_json(REPORT_DIR / "HOLDOUT_MANIFEST.json", {
            "record_type": "PROGRAMMER_HOLDOUT_MANIFEST",
            "warning": "Repository holdout is excluded from training export but is not secret. A private external holdout is required before real model promotion.",
            "tasks": [
                {"task_id": row.get("task_id"), "domain": row.get("domain"), "title": row.get("title")}
                for row in holdout
            ]
        })
        write_json(REPORT_DIR / "GOLDEN_CASE_QUEUE.json", {
            "record_type": "PROGRAMMER_GOLDEN_CASE_QUEUE",
            "state": "AWAITING_REFERENCE_SOLUTIONS_AND_REVIEW",
            "tasks": [
                {
                    "task_id": row.get("task_id"),
                    "required_checks": ["correctness", "requirements", "security_if_applicable", "source_alignment", "critic_review"]
                }
                for row in train
            ]
        })
        write_json(REPORT_DIR / "LATEST_PROGRAMMER_TRAINING_GYM_BUILD.json", summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
