from pathlib import Path


def test_pravo_publication_probe_is_metadata_only_and_fail_closed():
    module = Path("father_osint/pravo_publication.py").read_text(encoding="utf-8")
    script = Path("scripts/probe_pravo_publication_152.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PROBE_PRAVO_PUBLICATION_152.cmd").read_text(encoding="utf-8")

    assert 'DEFAULT_BASE_URL = "https://publication.pravo.gov.ru"' in module
    assert '"NumberSearchType": 0' in module
    assert '"Number": number' in module
    assert '"PageSize": page_size' in module
    assert '"Index": page' in module
    assert '"api/Documents"' in module
    assert '"api/Document"' in module
    assert '"File/Pdf"' in module
    assert '"File/Zip"' in module
    assert "metadata candidates only" in module
    assert "ResilientJsonTransport" in module
    assert "CurlJsonTransport" in module
    assert "primary_timeout_cap_seconds" in module
    assert "curl_https" in module
    assert "downgraded transport" in module

    assert 'TARGET_NUMBER = "152-ФЗ"' in script
    assert 'TARGET_DATE = "2006-07-27"' in script
    assert "authorize_external_asset" in script
    assert '"proof_acquisition"' in script
    assert '"metadata_only": True' in script
    assert '"d2_d3_promoted": False' in script
    assert '"legal_truth_promoted": False' in script
    assert "EXACT_IDENTITY_HITS=" in script
    assert "NEXT_ACTION=" in script
    assert "TRANSPORT=" in script
    assert "TRANSPORT_FAILURES=" in script
    assert "load_source_health" in script
    assert "write_source_health" in script
    assert "COOLDOWN_SECONDS = 30 * 60" in script
    assert "CIRCUIT_OPEN=" in script
    assert "NETWORK_SKIPPED=" in script
    assert "timeout_seconds=12.0" in script
    assert "scripts\\probe_pravo_publication_152.py" in cmd
