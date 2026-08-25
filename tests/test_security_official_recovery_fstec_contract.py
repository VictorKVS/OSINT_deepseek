import json
from pathlib import Path


def test_fstec_recovery_registry_has_five_direct_pdf_routes():
    payload = json.loads(Path("config/security_official_route_recovery.json").read_text(encoding="utf-8"))
    routes = payload["routes"]
    expected = {
        "DOC-RU-FSTEC-235-2017",
        "DOC-RU-FSTEC-239-2017",
        "DOC-RU-FSTEC-240-2023",
        "DOC-RU-FSTEC-117-2025",
        "DOC-RU-FSTEC-230-2025",
    }
    assert set(routes) == expected
    for rows in routes.values():
        assert rows
        route = rows[0]
        assert route["url"].startswith("https://cdnstatic.rg.ru/")
        assert route["url"].endswith(".pdf")
        assert route["provenance_page"].startswith("https://rg.ru/documents/")
        assert route["artifact_kind"] == "PDF"
    assert payload["rules"]["strict_tls_required"] is True
    assert payload["rules"]["identity_review_required_before_legal_truth"] is True
    assert payload["rules"]["kb_auto_promotion"] is False


def test_fstec_recovery_runner_is_targeted_and_conservative():
    text = Path("scripts/run_security_official_recovery_fstec.py").read_text(encoding="utf-8")
    assert "TARGETED_RECOVERY_DIRECT_ARTIFACT_FIRST" in text
    assert "PROVISIONAL_ROUTE_METADATA_MATCH_NEEDS_CONTENT_REVIEW" in text
    assert 'result["document_identity_confirmed"] = False' in text
    assert 'meta["legal_truth_eligible"] = False' in text
    assert "artifact_pdf_magic_check" in text
    assert "route_registration_hint_match" in text


def test_fstec_recovery_launcher_exists():
    text = Path("RUN_SECURITY_OFFICIAL_RECOVERY_FSTEC.cmd").read_text(encoding="utf-8")
    assert "run_security_official_recovery_fstec.py" in text
    assert "LATEST_FSTEC_OFFICIAL_RECOVERY_RUN.json" in text
    assert "No -k / insecure mode" in text
