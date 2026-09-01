import ast
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_programmer_min_expansion.py"


def load_module():
    spec = importlib.util.spec_from_file_location("programmer_min_expansion", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_expansion_policy_validates_without_local_golden_artifact():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--validate-policy-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "PASS"
    assert payload["validation_errors"] == []


def test_derive_tasks_creates_40_candidates_across_five_modes():
    mod = load_module()
    function_names = list(mod.BUGGY_IMPLEMENTATIONS)
    cases = []
    for index, name in enumerate(function_names, start=1):
        cases.append({
            "golden_case_id": f"GC-PT-MIN-{index:03d}",
            "task_id": f"PT-MIN-{index:03d}",
            "title": f"Seed {index}",
            "domain": "TEST_DOMAIN",
            "reference_function": name,
            "decision_summary": "approved seed",
            "code": f"def {name}(*args, **kwargs):\n    return None",
            "source_refs": [{"source_ref": "PYTHON_LANGUAGE_REFERENCE", "source_id": "SRC-PYTHON-LANGUAGE-3"}],
        })
    derived = mod.derive_tasks(cases)
    assert len(derived) == 40
    assert len({row["task_id"] for row in derived}) == 40
    assert Counter(row["derivation_mode"] for row in derived) == {mode: 8 for mode in mod.MODES}
    assert Counter(row["parent_golden_case_id"] for row in derived).most_common(1)[0][1] == 5
    assert all(row["split"] == "TRAIN" for row in derived)
    assert all(row["training_ready"] is False for row in derived)
    assert all(row["state"] == "DERIVED_CANDIDATE_PENDING" for row in derived)
    assert all(row["parent_code_sha256"] for row in derived)


def test_all_bug_mutations_are_syntactically_valid_and_cover_eight_goldens():
    mod = load_module()
    assert len(mod.BUGGY_IMPLEMENTATIONS) == 8
    for name, source in mod.BUGGY_IMPLEMENTATIONS.items():
        ast.parse(source)
        assert f"def {name}(" in source


def test_one_click_expansion_never_claims_training_ready():
    text = (ROOT / "RUN_PROGRAMMER_MIN_EXPANSION.cmd").read_text(encoding="utf-8")
    assert "build_programmer_min_expansion.py" in text
    assert "40 derived TRAIN candidates" in text
    assert "NOT training-ready" in text
    assert "HOLDOUT" in text
