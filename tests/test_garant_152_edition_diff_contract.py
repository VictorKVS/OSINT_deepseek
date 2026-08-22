from pathlib import Path


def test_garant_152_edition_diff_is_semantic_deduped_metadata_only():
    script = Path("scripts/diff_garant_152_editions.py").read_text(encoding="utf-8")
    cmd = Path("RUN_DIFF_GARANT_152_EDITIONS.cmd").read_text(encoding="utf-8")

    assert "extract_odt_text" in script
    assert "parse_legal_structure" in script
    assert "extracted_text" not in script
    assert "text_sha256" in script
    assert "modified_locators" in script
    assert "added_locators" in script
    assert "removed_locators" in script
    assert "A2_WORKING_DIFF_ONLY" in script
    assert "semantic_text_mirrored" in script
    assert "A2_LATEST_AMENDMENT_HINT_ONLY" in script
    assert "NEED_MORE_SEMANTIC_EDITIONS" in script
    assert "scripts\\diff_garant_152_editions.py" in cmd


def test_garant_152_edition_diff_reads_only_local_ignored_archive_and_exports_metadata():
    script = Path("scripts/diff_garant_152_editions.py").read_text(encoding="utf-8")

    assert '"data" / "knowledge_factory" / "garant_editions"' in script
    assert '"reports" / "pdn_timelines"' in script
    assert "garant_152_edition_diffs.jsonl" in script
    assert "GARANT_152_EDITION_DIFFS.md" in script
    assert "Only article/body locators and content hashes are compared" in script
