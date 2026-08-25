import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_SCRIPT = ROOT / "scripts" / "review_programmer_min_derived_candidates.py"
EXPANSION_SCRIPT = ROOT / "scripts" / "build_programmer_min_expansion.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synthetic_payloads():
    expansion = load_module(EXPANSION_SCRIPT, "programmer_min_expansion_for_review_test")
    parents = []
    for index, function_name in enumerate(expansion.BUGGY_IMPLEMENTATIONS, start=1):
        code = f"def {function_name}(*args, **kwargs):\n    return None"
        parents.append({
            "record_type": "PROGRAMMER_GOLDEN_CASE",
            "golden_case_id": f"GC-PT-MIN-{index:03d}",
            "task_id": f"PT-MIN-{index:03d}",
            "split": "TRAIN",
            "maturity_level": "MIN",
            "importance_class": "NECESSARY",
            "domain": "TEST_DOMAIN",
            "title": f"Seed {index}",
            "state": "GOLDEN_APPROVED",
            "training_ready": True,
            "reference_function": function_name,
            "decision_summary": "approved synthetic seed",
            "code": code,
            "holdout_dependency": False,
            "source_refs": [
                {"source_ref": "PYTHON_LANGUAGE_REFERENCE", "source_id": "SRC-PYTHON-LANGUAGE-3"}
            ],
        })
    derived = expansion.derive_tasks(parents)
    golden_payload = {
        "summary": {
            "status": "PASS",
            "golden_approved_total": 8,
            "holdout_exported_total": 0,
        },
        "golden_cases": parents,
    }
    derived_payload = {
        "summary": {
            "status": "PASS",
            "parent_golden_total": 8,
            "derived_candidates_total": 40,
            "holdout_derived_total": 0,
        },
        "tasks": derived,
    }
    return golden_payload, derived_payload


def test_derived_review_policy_and_mutation_quality_validate_without_runtime_artifacts():
    proc = subprocess.run(
        [sys.executable, str(REVIEW_SCRIPT), "--validate-policy-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "PASS"
    assert payload["mutation_quality_pass_total"] == 8
    assert payload["validation_errors"] == []


def test_synthetic_40_task_review_passes_and_keeps_training_ready_false(tmp_path):
    review = load_module(REVIEW_SCRIPT, "programmer_min_derived_review_test")
    golden_payload, derived_payload = synthetic_payloads()
    golden_path = tmp_path / "golden.json"
    derived_path = tmp_path / "derived.json"
    golden_path.write_text(json.dumps(golden_payload, ensure_ascii=False), encoding="utf-8")
    derived_path.write_text(json.dumps(derived_payload, ensure_ascii=False), encoding="utf-8")

    summary, reviewed = review.review(derived_path, golden_path)
    assert summary["status"] == "PASS", summary
    assert summary["tasks_total"] == 40
    assert summary["automated_pass_total"] == 40
    assert summary["automated_fail_total"] == 0
    assert summary["critic_pending_total"] == 40
    assert summary["training_ready_total"] == 0
    assert summary["holdout_leak_total"] == 0
    assert summary["mutation_quality_pass_total"] == 8
    assert all(row["state"] == "DERIVED_AUTOMATED_PASS_CRITIC_PENDING" for row in reviewed)
    assert all(row["training_ready"] is False for row in reviewed)


def test_parent_sha_mismatch_blocks_derived_review(tmp_path):
    review = load_module(REVIEW_SCRIPT, "programmer_min_derived_review_bad_sha_test")
    golden_payload, derived_payload = synthetic_payloads()
    derived_payload["tasks"][0]["parent_code_sha256"] = "0" * 64
    golden_path = tmp_path / "golden.json"
    derived_path = tmp_path / "derived.json"
    golden_path.write_text(json.dumps(golden_payload, ensure_ascii=False), encoding="utf-8")
    derived_path.write_text(json.dumps(derived_payload, ensure_ascii=False), encoding="utf-8")

    summary, reviewed = review.review(derived_path, golden_path)
    assert summary["status"] == "FAIL"
    assert summary["automated_fail_total"] >= 1
    assert any("parent code SHA mismatch" in err for row in reviewed for err in row["automated_review_errors"])


def test_one_click_derived_review_never_promotes_training_ready():
    text = (ROOT / "RUN_PROGRAMMER_MIN_DERIVED_REVIEW.cmd").read_text(encoding="utf-8")
    assert "review_programmer_min_derived_candidates.py" in text
    assert "critic review still required" in text
    assert "No derived task becomes training-ready here" in text
