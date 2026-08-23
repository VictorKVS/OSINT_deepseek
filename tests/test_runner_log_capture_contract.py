from pathlib import Path


def test_active_p0_runners_capture_full_local_transcripts_without_git_tracking():
    helper = Path("scripts/run_logged_python_sequence.ps1").read_text(encoding="utf-8")
    gitignore = Path(".gitignore").read_text(encoding="utf-8")

    assert "reports\\pdn_live\\run_logs" in helper
    assert "LATEST_RUN.txt" in helper
    assert "LATEST_{0}.txt" in helper
    assert "STARTED_LOCAL=" in helper
    assert "GIT_HEAD=" in helper
    assert "EXIT_CODE=" in helper
    assert "FULL_LOG=" in helper
    assert "LATEST_LOG=" in helper
    assert "Add-Content" in helper
    assert "reports/pdn_live/run_logs/" in gitignore

    runners = {
        "RUN_RESOLVE_PDN_PROOF_SOURCES.cmd": "RESOLVE_PDN_PROOF_SOURCES",
        "RUN_PDN_CHANGE_MONITOR.cmd": "PDN_CHANGE_MONITOR",
        "RUN_PDN_OBJECT_DELTA_PLAN.cmd": "PDN_OBJECT_DELTA_PLAN",
        "RUN_PDN_DELTA_SHADOW_EXECUTION.cmd": "PDN_DELTA_SHADOW_EXECUTION",
    }
    for path, run_id in runners.items():
        text = Path(path).read_text(encoding="utf-8")
        assert "run_logged_python_sequence.ps1" in text
        assert run_id in text
        assert "exit /b %ERRORLEVEL%" in text
