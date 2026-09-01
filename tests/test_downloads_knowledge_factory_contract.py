from pathlib import Path


def test_downloads_intake_is_local_fail_closed_and_non_destructive():
    text = Path("scripts/intake_downloads_knowledge_factory.py").read_text(encoding="utf-8")
    assert 'LIBRARY = ROOT / "_LOCAL_DOWNLOADS_KB_INTAKE"' in text
    assert '"source_files_modified": False' in text
    assert '"QUARANTINED_UNCLASSIFIED"' in text
    assert '"kb_auto_promotion": False' in text
    assert '"READY_FOR_MODEL_ROUTER"' in text


def test_local_model_plan_uses_capability_routing_and_semifabricates():
    text = Path("scripts/plan_local_model_semifabricates.py").read_text(encoding="utf-8")
    assert "local_model_capability_registry.json" in text
    assert '"LOCAL_MODEL_CHAMPION_CHALLENGER"' in text
    assert '"SEMIFABRICATE_ONLY"' in text
    assert '"MAIN_ANALYST_REVIEW_REQUIRED"' in text


def test_first_execution_pass_is_bounded_and_review_gated():
    text = Path("scripts/run_local_semifabricate_batch.py").read_text(encoding="utf-8")
    assert 'DEFAULT_STAGES = {"M5_TERMINOLOGY", "M6_KNOWLEDGE_EXTRACTION"}' in text
    assert 'default=2' in text
    assert '"MAIN_ANALYST_REVIEW_REQUIRED"' in text
    assert '"kb_auto_promotion": False' in text


def test_one_click_launcher_runs_intake_plan_and_small_batch():
    text = Path("RUN_DOWNLOADS_KNOWLEDGE_FACTORY.cmd").read_text(encoding="utf-8")
    assert "intake_downloads_knowledge_factory.py" in text
    assert "plan_local_model_semifabricates.py" in text
    assert "run_local_semifabricate_batch.py" in text
    assert "Source files are NEVER modified or deleted" in text
