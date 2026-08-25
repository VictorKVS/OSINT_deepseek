from pathlib import Path


def test_master_launcher_does_not_globally_stop_on_transport_diagnostic():
    text = Path("RUN_SECURITY_OFFICIAL_MASTER_DOWNLOAD.cmd").read_text(encoding="utf-8")
    assert "run_security_official_master_download_multiroute.py" in text
    assert "diagnose_security_official_transport.py" not in text
    assert "advisory per-route" in text
    assert "global stop gate" in text


def test_multiroute_wrapper_preserves_official_routes_and_fallback_evidence():
    text = Path("scripts/run_security_official_master_download_multiroute.py").read_text(encoding="utf-8")
    assert "official_routes" in text
    assert "route_attempts" in text
    assert "successful_route_index" in text
    assert "fallback_used" in text
    assert "ALL_OFFICIAL_ROUTES_FAILED" in text
    assert "PREFERRED_OFFICIAL_THEN_KNOWN_OFFICIAL_FALLBACK" in text
    assert "master.base._is_official" in text
    assert "master.merge_plan = merge_plan_multiroute" in text
    assert "master.acquire = acquire_multiroute" in text
