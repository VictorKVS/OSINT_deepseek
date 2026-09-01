import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_training_policy_keeps_current_standards_outside_weights():
    policy = load("config/programmer_training_gym_policy.json")
    assert policy["status"] == "ACTIVE_MIN_FOUNDATION"
    assert policy["model_strategy"]["train_from_scratch"] is False
    assert "standards and specifications" in policy["model_strategy"]["retrieval_keeps_current"]
    assert policy["dataset_rules"]["train_and_holdout_must_not_overlap"] is True
    assert policy["dataset_rules"]["holdout_tasks_must_not_be_exported_to_training"] is True
    assert policy["execution_policy"]["model_generated_code_requires_sandbox_before_unattended_execution"] is True
    assert policy["dataset_rules"]["long_private_chain_of_thought_is_not_training_target"] is True


def test_min_task_library_has_12_unique_tasks_with_8_4_split():
    library = load("config/programmer_training_task_library.json")
    tasks = library["tasks"]
    assert library["maturity_level"] == "MIN"
    assert library["importance_class"] == "NECESSARY"
    assert len(tasks) == 12
    ids = [row["task_id"] for row in tasks]
    assert len(ids) == len(set(ids))
    assert sum(row["split"] == "TRAIN" for row in tasks) == 8
    assert sum(row["split"] == "HOLDOUT" for row in tasks) == 4
    assert all(row["source_refs"] for row in tasks)
    assert all(row["evaluation"]["kind"] == "PURE_FUNCTION" for row in tasks)


def test_every_training_source_ref_resolves_to_verified_knowledge_registry_alias():
    library = load("config/programmer_training_task_library.json")
    registry = load("config/knowledge_source_registry.json")
    resolved = set()
    for source in registry["sources"]:
        assert source["status"]
        assert source["canonical_url"].startswith("https://")
        resolved.add(source["source_id"])
        resolved.update(source.get("aliases") or [])
    refs = {ref for task in library["tasks"] for ref in task["source_refs"]}
    assert refs <= resolved, f"unresolved source refs: {sorted(refs - resolved)}"


def test_builder_validates_seed_without_generating_answers():
    script = ROOT / "scripts" / "build_programmer_training_gym.py"
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
    assert payload["tasks_total"] == 12
    assert payload["train_tasks_total"] == 8
    assert payload["holdout_tasks_total"] == 4
    assert payload["golden_cases_total"] == 0
    assert payload["training_examples_total"] == 0
    assert payload["speedup_vs_1_stream_pct"] is None
    assert payload["eta_seconds"] is None


def test_one_click_training_gym_is_build_only_not_model_training():
    text = (ROOT / "RUN_PROGRAMMER_TRAINING_GYM.cmd").read_text(encoding="utf-8")
    assert "build_programmer_training_gym.py" in text
    assert "No model training is performed yet" in text
    assert "llama" not in text.casefold()
    assert "finetune" not in text.casefold()
