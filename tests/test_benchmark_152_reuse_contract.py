from pathlib import Path


def test_152_reuse_benchmark_is_single_document_and_measures_download_compare_time():
    script = Path("scripts/benchmark_152_reuse.py").read_text(encoding="utf-8")
    cmd = Path("RUN_BENCHMARK_152_REUSE.cmd").read_text(encoding="utf-8")

    assert 'TARGET_ID = "DOC-RU-FZ-152-2006"' in script
    assert 'TARGET_NUMBER = "152-ФЗ"' in script
    assert 'TARGET_DATE = "27.07.2006"' in script
    assert 'DATASET = "irlspbru/RusLawOD"' in script
    assert "/filter?" in script
    assert "/search?" in script
    assert "ProviderUnavailable" in script
    assert "_http_json_with_retries" in script
    assert "duckdb_remote_parquet" in script
    assert 'DUCKDB_VERSION = "1.5.5"' in script
    assert "--target" in script
    assert ".runtime" in script
    assert "external_lookup_and_download" in script
    assert "dependency_setup" in script
    assert "content_compare" in script
    assert "TOTAL_SECONDS=" in script
    assert "DOWNLOAD_SECONDS=" in script
    assert "DEPENDENCY_SETUP_SECONDS=" in script
    assert "COMPARE_SECONDS=" in script
    assert "BOOTSTRAP_CORPUS_NOT_A0_PROOF" in script
    assert "legal_truth_promoted" in script
    assert "scripts\\benchmark_152_reuse.py" in cmd
