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
