from pathlib import Path


def test_downloads_intake_is_read_only_and_builds_semifabricates():
    text = Path("scripts/intake_windows_downloads.py").read_text(encoding="utf-8")
    assert "_LOCAL_DOWNLOADS_KB_INTAKE" in text
    assert "source_original_modified" in text
    assert '"kb_auto_promotion": False' in text
    assert "DeterministicKnowledgeAnalyst" in text
    assert "TASKS.jsonl" in text
    assert "CATALOG_REFERENCES.json" in text
    assert "Path.home()" in text
    assert "Downloads" in text
    assert "Загрузки" in text


def test_downloads_intake_launcher_exists():
    text = Path("RUN_DOWNLOADS_KB_INTAKE.cmd").read_text(encoding="utf-8")
    assert "intake_windows_downloads.py" in text
    assert "LATEST_DOWNLOADS_KB_INTAKE.json" in text
    assert "Originals are NEVER moved or deleted" in text


def test_local_model_pool_is_review_only():
    text = Path("config/local_model_semifabricate_pool.json").read_text(encoding="utf-8")
    assert '"all_applicable_models_participate": true' in text
    assert '"no_model_can_promote_legal_truth": true' in text
    assert '"review_status": "MAIN_ANALYST_REVIEW_REQUIRED"' in text
    assert "WHISPER-LARGE-V3-TURBO" in text
    assert "BGE-M3" in text
