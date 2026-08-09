from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


def test_run_dev_osint_entrypoint_executes_from_repository_root() -> None:
    result = _run("scripts/run_dev_osint.py")
    assert result.returncode == 0, result.stderr or result.stdout


def test_run_dev_pipeline_entrypoint_executes_from_repository_root() -> None:
    result = _run("scripts/run_dev_pipeline.py")
    assert result.returncode == 0, result.stderr or result.stdout
