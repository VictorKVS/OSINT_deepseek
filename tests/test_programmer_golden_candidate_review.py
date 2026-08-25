import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_golden_review_policy_requires_critic_and_explicit_promotion():
    policy = load("config/programmer_golden_case_review_policy.json")
    assert policy["status"] == "ACTIVE_MIN_FOUNDATION"
    assert policy["promotion_rules"]["automated_pass_is_not_golden"] is True
    assert policy["promotion_rules"]["critic_review_required"] is True
    assert policy["promotion_rules"]["holdout_never_exported_to_training"] is True
    assert "GOLDEN_APPROVED" in policy["states"]


def test_golden_candidate_validate_only_passes_and_preserves_holdout_isolation():
    script = ROOT / "scripts" / "review_programmer_golden_candidates.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--validate-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "PASS"
    assert payload["tasks_total"] == 8
    assert payload["candidate_pass_total"] == 8
    assert payload["candidate_fail_total"] == 0
    assert payload["golden_approved_total"] == 0
    assert payload["training_ready_total"] == 0
    assert payload["holdout_implementation_leak_total"] == 0
    assert payload["targeted_regression_tests"] == "NOT_RUN"
    assert payload["validation_errors"] == []


def test_stdlib_regression_verifier_passes_without_pytest_dependency():
    script = ROOT / "scripts" / "verify_programmer_min_reference_stdlib.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "PASS"
    assert payload["checks_total"] == 8
    assert payload["checks_passed"] == 8
    assert payload["checks_failed"] == 0
    assert payload["holdout_implementation_leak_total"] == 0


def test_golden_review_has_local_environment_fallback_but_does_not_mask_real_pytest_failures():
    text = (ROOT / "scripts" / "review_programmer_golden_candidates.py").read_text(encoding="utf-8")
    assert '"-c", "import pytest"' in text
    assert "STDLIB_FALLBACK" in text
    assert "If pytest exists and the tests" in text
    assert "no fallback is allowed" in text


def test_one_click_golden_review_runs_automated_tests_but_not_model_training():
    text = (ROOT / "RUN_PROGRAMMER_GOLDEN_CANDIDATES.cmd").read_text(encoding="utf-8")
    assert "review_programmer_golden_candidates.py" in text
    assert "critic approval still required" in text
    assert "finetune" not in text.casefold()
    assert "model training" not in text.casefold()
