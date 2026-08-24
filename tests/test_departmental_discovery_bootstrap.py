from pathlib import Path


def test_departmental_discovery_bootstraps_repo_root_before_package_import():
    text = Path("scripts/discover_security_departmental_orders.py").read_text(encoding="utf-8")
    repo_root_pos = text.index("REPO_ROOT = Path(__file__).resolve().parents[1]")
    sys_path_pos = text.index("sys.path.insert(0, str(REPO_ROOT))")
    package_import_pos = text.index("from father_osint.pravo_publication import")

    assert repo_root_pos < sys_path_pos < package_import_pos


def test_departmental_discovery_cmd_exports_repo_root_pythonpath():
    text = Path("RUN_SECURITY_DEPARTMENTAL_DISCOVERY.cmd").read_text(encoding="utf-8")
    assert 'set "PYTHONPATH=%CD%;%PYTHONPATH%"' in text
    assert "%PY% scripts\\discover_security_departmental_orders.py" in text


def test_departmental_discovery_preserves_verified_seeds_when_api_is_degraded():
    text = Path("scripts/discover_security_departmental_orders.py").read_text(encoding="utf-8")
    assert "DEGRADED_WITH_VERIFIED_SEED_FALLBACK" in text
    assert '"seed_candidate_total"' in text
    assert '"live_api_candidate_total"' in text
    assert '"candidate_origin": "VERIFIED_SEED"' in text
    assert "Exact bytes, SHA-256, legal status and replacement/amendment chain verification are required" in text


def test_departmental_discovery_reads_sectoral_kii_fallback_queue():
    text = Path("scripts/discover_security_departmental_orders.py").read_text(encoding="utf-8")
    assert "security_sectoral_kii_current_only_queue.json" in text
    assert '"sectoral_kii_queue"' in text

    queue = Path("config/security_sectoral_kii_current_only_queue.json").read_text(encoding="utf-8")
    for publication_number in (
        "0001202601160013",
        "0001202602070010",
        "0001202603070013",
        "0001202603240036",
        "0001202604010039",
    ):
        assert publication_number in queue
