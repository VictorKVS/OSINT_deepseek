import json
from pathlib import Path


def test_profile_defines_exactly_five_distinct_analytics_streams():
    payload = json.loads(Path("config/security_legal_analytics_5stream.json").read_text(encoding="utf-8"))
    streams = payload["streams"]
    assert len(streams) == 5
    assert len({row["stream_id"] for row in streams}) == 5
    assert payload["workers"] == 5
    assert payload["mode"] == "EXISTING_CORPUS_ONLY"


def test_legal_gate_is_fail_closed_for_promotion():
    payload = json.loads(Path("config/security_legal_analytics_5stream.json").read_text(encoding="utf-8"))
    gate = payload["legal_gate"]
    assert gate["require_document_identity_confirmed_for_promotion"] is True
    assert gate["require_currentness_verified_for_promotion"] is True
    assert gate["allow_candidate_extraction_when_promotion_blocked"] is True
    assert payload["principles"]["kb_auto_promotion"] is False
    assert "DOC-RU-GOST-R-56939-2024" in gate["known_detail_page_only_ids"]


def test_runner_is_five_parallel_analysis_streams_not_downloader():
    text = Path("scripts/run_security_legal_analytics_5stream.py").read_text(encoding="utf-8")
    assert "ThreadPoolExecutor(max_workers=5" in text
    assert "S1_IDENTITY_CURRENTNESS" in text
    assert "S2_TERMS_SCOPE" in text
    assert "S3_REQUIREMENTS_OBLIGATIONS" in text
    assert "S4_RELATIONS_CONTRADICTIONS" in text
    assert "S5_APPLICABILITY_CONTROL_MAPPING" in text
    assert "urllib.request" not in text
    assert "download_media" not in text
    assert '"network_acquisition": False' in text
    assert '"kb_auto_promotion": False' in text


def test_contradictions_are_review_pairs_only():
    text = Path("scripts/run_security_legal_analytics_5stream.py").read_text(encoding="utf-8")
    assert '"verdict": "NOT_ASSERTED"' in text
    assert "M8_CONTRADICTION_VERIFICATION" in text
    assert "REVIEW_PAIRS_ONLY_NO_CONFLICT_ASSERTION_WITHOUT_M8" in text


def test_launcher_points_at_legal_analytics_runner():
    text = Path("RUN_SECURITY_LEGAL_ANALYTICS_5STREAM.cmd").read_text(encoding="utf-8")
    assert "run_security_legal_analytics_5stream.py" in text
    assert "Network acquisition: OFF" in text
    assert "KB auto-promotion: OFF" in text
