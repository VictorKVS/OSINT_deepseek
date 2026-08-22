from pathlib import Path


def test_garant_152_odt_import_runner_prefers_downloaded_odt_and_identity_gate():
    script = Path("scripts/import_latest_garant_152_odt.py").read_text(encoding="utf-8")
    cmd = Path("RUN_IMPORT_GARANT_152_ODT.cmd").read_text(encoding="utf-8")

    assert 'Path.home() / "Downloads"' in script
    assert 'MARKERS = ("152-ФЗ", "О персональных данных")' in script
    assert "extract_odt_text" in script
    assert "sha256" in script
    assert "GARANT_ODT_IMPORTED" in script
    assert "scripts\\import_latest_garant_152_odt.py" in cmd
    assert "scripts\\run_pdn_garant_timeline.py" in cmd


def test_garant_152_edition_inventory_is_hash_deduped_and_metadata_only():
    script = Path("scripts/import_garant_152_editions.py").read_text(encoding="utf-8")
    cmd = Path("RUN_IMPORT_GARANT_152_EDITIONS.cmd").read_text(encoding="utf-8")

    assert 'Path.home() / "Downloads"' in script
    assert 'MARKERS = ("152-ФЗ", "О персональных данных")' in script
    assert "extract_odt_text" in script
    assert "parse_garant_timeline_text" in script
    assert "capture_sha256" in script
    assert "extracted_text_sha256" in script
    assert "unique_text_captures" in script
    assert "semantic_duplicate_captures" in script
    assert "semantic_group_size" in script
    assert "A2_WORKING_COPY_ONLY" in script
    assert "semantic_text_mirrored" in script
    assert "latest_amendment_hint" in script
    assert "edition-effective date" in script
    assert "scripts\\import_garant_152_editions.py" in cmd


def test_garant_152_edition_inventory_keeps_exact_bytes_local():
    script = Path("scripts/import_garant_152_editions.py").read_text(encoding="utf-8")

    assert '"data" / "knowledge_factory" / "garant_editions"' in script
    assert '"reports" / "pdn_timelines"' in script
    assert "GARANT_152_EDITION_INVENTORY.md" in script
    assert "garant_152_edition_inventory.jsonl" in script
    assert "Different ODT bytes may still contain identical extracted legal text" in script
