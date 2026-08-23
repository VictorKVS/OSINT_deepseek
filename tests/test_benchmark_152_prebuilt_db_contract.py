from pathlib import Path


def test_prebuilt_russian_law_db_benchmark_is_reuse_first_and_fail_closed():
    script = Path("scripts/benchmark_152_prebuilt_mcp_db.py").read_text(encoding="utf-8")
    cmd = Path("RUN_BENCHMARK_152_PREBUILT_DB.cmd").read_text(encoding="utf-8")

    assert 'PACKAGE_SPEC = "@ansvar/russian-law-mcp@0.1.0"' in script
    assert 'PACKAGE_DB_MEMBER = "package/data/database.db"' in script
    assert "npm" in script.lower()
    assert "npm\", \"pack\"" in script
    assert "sqlite3.connect" in script
    assert "PRAGMA quick_check" in script
    assert "SELECT COUNT(*) FROM laws" in script
    assert "SELECT COUNT(*) FROM provisions" in script
    assert "TARGET_NUMBER" in script
    assert "REFERENCE_KB_NOT_A0_PROOF" in script
    assert '"legal_truth_promoted": False' in script
    assert "REUSED_LOCAL_PREBUILT_DB" in script
    assert "DOWNLOADED_PREBUILT_NPM_DB" in script
    assert "DB_QUERY_SECONDS=" in script
    assert "COMPARE_SECONDS=" in script
    assert "scripts\\benchmark_152_prebuilt_mcp_db.py" in cmd
