import json
from pathlib import Path

from scripts import promote_programmer_min_golden_cases as promote

ROOT = Path(__file__).resolve().parents[1]


def test_critic_decisions_cover_only_train_and_pass_all_gates():
    assert promote.validate_critic_only() == []


def test_promotion_accepts_hash_bound_passing_candidates_and_exports_no_holdout(tmp_path):
    ref_sha = promote.sha256_file(promote.REFERENCE)
    source_sha = promote.sha256_file(promote.SOURCES)
    candidates = []
    for task_id, function_name in promote.TASK_TO_FUNCTION.items():
        candidates.append({
            "record_type": "PROGRAMMER_GOLDEN_CASE_CANDIDATE",
            "task_id": task_id,
            "split": "TRAIN",
            "reference_function": function_name,
            "state": "CANDIDATE_PASS_CRITIC_PENDING",
            "training_ready": False,
        })
    candidate_file = tmp_path / "GOLDEN_CASE_CANDIDATES.json"
    candidate_file.write_text(json.dumps({
        "summary": {
            "status": "PASS",
            "candidate_pass_total": 8,
            "candidate_fail_total": 0,
            "holdout_implementation_leak_total": 0,
            "targeted_regression_tests": "PASS",
            "targeted_regression_engine": "STDLIB_FALLBACK",
            "reference_solution_sha256": ref_sha,
            "source_registry_sha256": source_sha,
        },
        "candidates": candidates,
    }), encoding="utf-8")

    summary, golden, sft = promote.build_promotion(candidate_file)
    assert summary["status"] == "PASS", summary["validation_errors"]
    assert summary["golden_approved_total"] == 8
    assert summary["training_ready_total"] == 8
    assert summary["holdout_exported_total"] == 0
    assert len(golden) == 8
    assert len(sft) == 8
    assert all(row["state"] == "GOLDEN_APPROVED" for row in golden)
    assert all(row["training_ready"] is True for row in golden)
    assert all(row["split"] == "TRAIN" for row in golden)
    assert not any(row["task_id"] in {"PT-MIN-009", "PT-MIN-010", "PT-MIN-011", "PT-MIN-012"} for row in golden)
    assert all(row["split"] == "TRAIN" for row in sft)


def test_promotion_rejects_stale_reference_sha(tmp_path):
    source_sha = promote.sha256_file(promote.SOURCES)
    candidates = [
        {
            "task_id": task_id,
            "state": "CANDIDATE_PASS_CRITIC_PENDING",
            "training_ready": False,
        }
        for task_id in promote.TASK_TO_FUNCTION
    ]
    candidate_file = tmp_path / "STALE.json"
    candidate_file.write_text(json.dumps({
        "summary": {
            "status": "PASS",
            "candidate_pass_total": 8,
            "candidate_fail_total": 0,
            "holdout_implementation_leak_total": 0,
            "targeted_regression_tests": "PASS",
            "reference_solution_sha256": "0" * 64,
            "source_registry_sha256": source_sha,
        },
        "candidates": candidates,
    }), encoding="utf-8")
    summary, golden, sft = promote.build_promotion(candidate_file)
    assert summary["status"] == "FAIL"
    assert golden == []
    assert sft == []
    assert any("reference-solution SHA" in error for error in summary["validation_errors"])
