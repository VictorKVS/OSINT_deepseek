from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPEN_SCRIPT = ROOT / "scripts" / "acquire_programming_kb_open_sources.py"
OWNED_SCRIPT = ROOT / "scripts" / "download_programming_kb_owned_telegram_books.py"
PROCESS_SCRIPT = ROOT / "scripts" / "process_programming_kb_sources.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_source_factory_policy_blocks_commercial_telegram_auto_download():
    policy = json.loads((ROOT / "config" / "programming_kb_source_factory_policy.json").read_text(encoding="utf-8"))
    rights = policy["rights_policy"]
    assert rights["telegram_candidate_is_not_license_evidence"] is True
    assert rights["commercial_fulltext_auto_download"] is False
    assert rights["commercial_fulltext_requires_explicit_user_owned_or_authorized_assertion"] is True
    assert rights["explicit_owned_ids_env"] == "FATHER_OWNED_BOOK_IDS"
    assert policy["promotion"]["kb_auto_promotion"] is False
    assert policy["promotion"]["training_auto_export"] is False


def test_open_acquisition_selects_only_open_routes_and_is_bounded():
    mod = load_module(OPEN_SCRIPT, "programming_kb_open_acquire")
    rows = mod.build_open_targets()
    assert len(rows) == 6
    assert {row["id"] for row in rows} == {"BOOK-004", "BOOK-008", "WORK-001", "WORK-002", "WORK-003", "WORK-004"}
    assert all(row["route"] in mod.OPEN_ROUTES for row in rows)
    proc = subprocess.run(
        [sys.executable, str(OPEN_SCRIPT), "--validate-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "PASS"
    assert payload["targets_total"] == 6


def test_owned_telegram_queue_is_empty_without_explicit_user_assertion(monkeypatch):
    mod = load_module(OWNED_SCRIPT, "programming_kb_owned_tg")
    monkeypatch.delenv("FATHER_OWNED_BOOK_IDS", raising=False)
    assert mod.owned_ids() == set()
    queue, errors = mod.build_queue()
    assert queue == []
    assert errors == []


def test_html_extractor_produces_clean_text(tmp_path):
    mod = load_module(PROCESS_SCRIPT, "programming_kb_processor")
    path = tmp_path / "sample.html"
    path.write_text("<html><body><h1>Algorithms</h1><p>Binary search requires ordered data.</p><script>ignore()</script></body></html>", encoding="utf-8")
    text, engine = mod.extract_text(path)
    assert engine == "STDLIB_HTML_PARSER"
    assert "Algorithms" in text
    assert "Binary search requires ordered data." in text
    assert "ignore()" not in text


def test_processor_validate_only_passes_without_local_sources():
    proc = subprocess.run(
        [sys.executable, str(PROCESS_SCRIPT), "--validate-only"],
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


def test_one_click_factory_keeps_training_on_hold():
    text = (ROOT / "RUN_PROGRAMMING_KB_SOURCE_FACTORY.cmd").read_text(encoding="utf-8")
    assert "Commercial Telegram books are NOT auto-downloaded" in text
    assert "No model training" in text
    assert "No KB auto-promotion" in text
    assert "FATHER_OWNED_BOOK_IDS" in text
