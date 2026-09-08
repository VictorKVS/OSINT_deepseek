from __future__ import annotations

import json
from pathlib import Path

from osint_factory.cli import main


def test_cli_demo_runs_offline(tmp_path: Path, capsys) -> None:
    code = main([
        "demo",
        "--profile",
        "RU_ORG",
        "--root",
        str(tmp_path),
        "--workers",
        "5",
    ])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["profile"] == "RU_ORG"
    assert payload["journal_valid"] is True
    assert (tmp_path / "cases" / payload["case_id"] / "05_report.md").is_file()
