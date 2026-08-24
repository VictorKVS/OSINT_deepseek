import json
from pathlib import Path


def test_global_development_traceability_standard_is_mandatory():
    standard = json.loads(Path("config/development_traceability_standard.json").read_text(encoding="utf-8"))
    assert standard["status"] == "MANDATORY"
    assert standard["scope"] == "ALL_FATHER_DEVELOPMENTS"
    assert "TRACEABILITY_PLAN.md" in standard["required_artifacts"]
    assert "command_id" in standard["required_runtime_fields"]
    assert "parent_command_id" in standard["required_runtime_fields"]
    assert "evidence_refs" in standard["required_runtime_fields"]
    assert standard["acceptance_gate"]["unlinked_command_or_output_is_a_traceability_defect"] is True


def test_osint_control_center_has_project_traceability_plan_and_runtime_trace():
    plan = Path("osint_web/TRACEABILITY_PLAN.md").read_text(encoding="utf-8")
    app = Path("osint_web/app.py").read_text(encoding="utf-8")
    html = Path("osint_web/static/index.html").read_text(encoding="utf-8")
    assert "FATHER-OSINT" in plan
    assert "command_id" in plan and "parent_command_id" in plan
    assert "TRACE_PATH" in app and "trace_events.jsonl" in app
    assert '"trace_id"' in app and '"correlation_id"' in app and '"task_id"' in app and '"command_id"' in app
    assert 'parsed.path == "/api/traces"' in app
    assert "Трассировка команд" in html


def test_stage_1_acquisition_exposes_live_download_progress():
    helper = Path("scripts/download_progress_registry.py").read_text(encoding="utf-8")
    wrapper = Path("scripts/run_team_role_acquisition_live.py").read_text(encoding="utf-8")
    ps1 = Path("scripts/run_team_role_acquisition.ps1").read_text(encoding="utf-8")
    app = Path("osint_web/app.py").read_text(encoding="utf-8")
    html = Path("osint_web/static/index.html").read_text(encoding="utf-8")
    js = Path("osint_web/static/app.js").read_text(encoding="utf-8")

    assert "STAGE_1_ACQUISITION" in helper
    for status in ("QUEUED", "DOWNLOADING", "HASHING", "DOWNLOADED", "REUSED", "FAILED"):
        assert status in helper
    assert "overall_progress_pct" in helper
    assert "speed_bytes_per_second" in helper
    assert "progress_callback" in wrapper
    assert "run_team_role_acquisition_live.py" in ps1
    assert 'parsed.path == "/api/downloads"' in app
    assert "Список скачивания и прогресс" in html
    assert "renderDownloads" in js
    assert "progress-fill" in js
    assert "fmtSpeed" in js


def test_download_progress_registry_is_per_role_and_atomic():
    helper = Path("scripts/download_progress_registry.py").read_text(encoding="utf-8")
    assert 'f"{self.role_id}.json"' in helper
    assert "os.replace(tmp, self.path)" in helper
    assert "0.25" in helper
