from pathlib import Path


def test_control_center_binds_localhost_and_uses_action_allowlist():
    text = Path("osint_web/app.py").read_text(encoding="utf-8")
    assert 'OSINT_WEB_HOST", "127.0.0.1"' in text
    assert 'OSINT_WEB_PORT", "8765"' in text
    assert "ALLOWED_ACTIONS" in text
    assert '"ROLE_ACQUISITION"' in text
    assert '"TELEGRAM_QUERY_PROBE"' in text
    assert "shell=True" not in text
    assert "CREATE_NEW_CONSOLE" in text


def test_generic_search_is_probe_only_and_never_downloads():
    text = Path("scripts/probe_osint_query.py").read_text(encoding="utf-8")
    assert "client.iter_messages(None, search=query" in text
    assert '"probe_only": True' in text
    assert "download_media" not in text
    assert "join_channel" not in text.casefold()


def test_showcase_ui_exposes_search_metrics_streams_and_evidence_map():
    html = Path("osint_web/static/index.html").read_text(encoding="utf-8")
    js = Path("osint_web/static/app.js").read_text(encoding="utf-8")
    for token in ("OSINT Intelligence Console", "5 рабочих потоков", "Карта поиска", "Результаты поиска", "Библиография"):
        assert token in html
    assert "TELEGRAM_QUERY_PROBE" in js
    assert "REMAINING_P0_WINDOWS" in js
    assert "bibliography_availability_ratio" in js


def test_parallel_p0_windows_use_isolated_telethon_session_files():
    text = Path("RUN_REMAINING_P0_SEARCH_WINDOWS.cmd").read_text(encoding="utf-8")
    assert "system_analyst.session" in text
    assert "legal_compliance.session" in text
    assert "ml_llm_engineer.session" in text
    assert "TELEGRAM_SESSION_PATH" in text
    assert text.count("start \"FATHER") == 3
