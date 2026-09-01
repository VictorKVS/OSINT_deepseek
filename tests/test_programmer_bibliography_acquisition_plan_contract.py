import json
from pathlib import Path


def test_programmer_bibliography_acquisition_registry_covers_all_targets():
    targets = json.loads(Path("config/programmer_bibliography_targets.json").read_text(encoding="utf-8"))
    registry = json.loads(Path("config/programmer_bibliography_acquisition_registry.json").read_text(encoding="utf-8"))
    target_ids = {row["id"] for row in targets["targets"]}
    registry_ids = {row["id"] for row in registry["targets"]}
    assert target_ids == registry_ids
    assert len(target_ids) == 20
    assert registry["policy"]["telegram_candidate_is_not_license_evidence"] is True
    assert registry["policy"]["commercial_fulltext_requires_user_license_or_owned_copy"] is True
    assert registry["policy"]["exact_edition_verification_required"] is True


def test_open_official_routes_are_explicit_and_commercial_routes_are_not_auto_ingest():
    registry = json.loads(Path("config/programmer_bibliography_acquisition_registry.json").read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in registry["targets"]}
    assert rows["BOOK-004"]["route"] == "OFFICIAL_OPEN_WEB"
    assert rows["BOOK-008"]["route"] == "OFFICIAL_OPEN_WEB"
    assert rows["WORK-001"]["route"] == "OFFICIAL_OPEN_PDF"
    assert rows["WORK-002"]["route"] == "OFFICIAL_OPEN_PDF"
    assert rows["WORK-004"]["route"] == "OFFICIAL_OPEN_PDF"
    assert rows["WORK-003"]["route"] == "OFFICIAL_REPOSITORY_DOWNLOAD"
    assert rows["BOOK-001"]["route"].startswith("COMMERCIAL_")
    assert rows["BOOK-011"]["route"].startswith("COMMERCIAL_")


def test_next_action_planner_never_downloads_or_promotes():
    text = Path("scripts/build_programmer_bibliography_acquisition_plan.py").read_text(encoding="utf-8")
    assert "ACQUIRE_FROM_OFFICIAL_SOURCE" in text
    assert "VERIFY_RIGHTS_AND_EXACT_EDITION_BEFORE_INGEST" in text
    assert "OFFICIAL_PURCHASE_OR_USER_OWNED_COPY_REQUIRED" in text
    assert '"kb_auto_promotion": False' in text
    assert "download_media" not in text
    assert "urllib" not in text
    assert "requests" not in text
