from pathlib import Path


def test_official_transport_diagnostic_is_read_only_and_uses_three_authority_families():
    text = Path("scripts/diagnose_security_official_transport.py").read_text(encoding="utf-8")
    assert "READ_ONLY_NETWORK_PROBE" in text
    assert "publication.pravo.gov.ru" in text
    assert "government.ru" in text
    assert "protect.gost.ru" in text
    assert "UrllibArtifactFetcher" in text
    assert "CurlArtifactFetcher" in text
    assert "RobustOfficialArtifactFetcher" in text
    assert "write_bytes(" not in text
    assert "raw_path" not in text
    assert "normalized_path" not in text
    assert "insecure" not in text.casefold()
    assert "consultant.ru" not in text.casefold()


def test_official_transport_diagnostic_launcher_is_one_click_and_read_only():
    text = Path("RUN_SECURITY_OFFICIAL_TRANSPORT_DIAGNOSTIC.cmd").read_text(encoding="utf-8")
    assert "diagnose_security_official_transport.py" in text
    assert "READ ONLY" in text
    assert "LATEST_OFFICIAL_TRANSPORT_DIAGNOSTIC.json" in text
