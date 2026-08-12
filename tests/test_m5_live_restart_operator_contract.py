from pathlib import Path


def test_live_runner_exposes_checkpoint_restart_controls():
    source = Path("scripts/run_live_telegram_material.py").read_text(encoding="utf-8")

    assert "--checkpoint" in source
    assert "--resume" in source
    assert "DurableObservationWriter" in source
    assert "JsonCheckpointStore" in source
    assert "save_then_checkpoint" in source


def test_live_runner_reports_restart_reconciliation():
    source = Path("scripts/run_live_telegram_material.py").read_text(encoding="utf-8")

    for field in (
        '"checkpoint_enabled"',
        '"resume_requested"',
        '"resumed_sources"',
        '"checkpoint_commits"',
        '"restart_reconciliation_passed"',
    ):
        assert field in source
