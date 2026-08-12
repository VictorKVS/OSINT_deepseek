from __future__ import annotations

import runpy
from pathlib import Path


def test_live_telegram_runner_bootstraps_repo_root_without_running_main(monkeypatch):
    script = Path("scripts/run_live_telegram_material.py").resolve()

    monkeypatch.setattr("sys.argv", [str(script), "--help"])

    namespace = runpy.run_path(str(script), run_name="m5_probe")

    assert namespace["REPO_ROOT"] == script.parents[1]
    assert namespace["DEFAULT_CONFIG"] == script.parents[1] / "legacy/telegram/config.yaml"
    assert namespace["DEFAULT_SESSION"] == script.parents[1] / "legacy/telegram/reader_session"
    assert namespace["DEFAULT_OUTPUT"] == script.parents[1] / "data/m5_live_telegram"
