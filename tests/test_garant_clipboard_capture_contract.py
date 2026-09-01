from pathlib import Path


def test_garant_clipboard_capture_watcher_is_local_and_fail_closed():
    script = Path("scripts/capture_garant_clipboard.ps1").read_text(encoding="utf-8")

    assert "Get-Clipboard" in script
    assert "Set-Clipboard" not in script
    assert "identity_markers=PASS" in script
    assert "Timed out waiting for a valid GARANT clipboard capture" in script
    assert "data\\operator_import\\garant_timeline" in script
    assert "change_heading" in script
    assert "compact_history" in script
    assert "effective_phrase" in script
    assert "timeline_detail_candidate=YES" in script
    assert "requests.get" not in script
    assert "Invoke-WebRequest" not in script


def test_one_click_152_capture_runner_exists():
    cmd = Path("RUN_CAPTURE_GARANT_152.cmd")
    assert cmd.is_file()
    content = cmd.read_text(encoding="utf-8")
    assert "scripts\\capture_garant_clipboard.ps1" in content
    assert "DOC-RU-FZ-152-2006" in content
    assert "RUN_PDN_GARANT_TIMELINE.cmd" in content
