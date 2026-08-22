from pathlib import Path


def test_official_source_pack_d4_d5_runner_uses_normal_operator_conveyor():
    cmd = Path("RUN_PDN_OFFICIAL_SOURCE_PACK_D4_D5.cmd").read_text(encoding="utf-8")

    assert "scripts\\run_pdn_operator_import.py" in cmd
    assert "data\\operator_import\\pdn_official_source_pack" in cmd
    assert "data\\knowledge_factory\\pdn_official_batch" in cmd
    assert "reports\\pdn_live" in cmd
    assert "D4-D5" in cmd
    assert "normal conveyor" in cmd


def test_operator_import_resolves_relative_cli_paths_before_repo_relative_inventory():
    script = Path("scripts/run_pdn_operator_import.py").read_text(encoding="utf-8")

    assert "def _repo_path" in script
    assert "if not path.is_absolute()" in script
    assert "path = REPO_ROOT / path" in script
    assert "registry_path = _repo_path(args.registry)" in script
    assert "inbox = _repo_path(args.inbox)" in script
    assert "root = _repo_path(args.root)" in script
    assert "export_review = _repo_path(args.export_review)" in script
    assert "candidates = [inbox /" in script
    assert "path.relative_to(REPO_ROOT).as_posix()" in script


def test_d4_d5_quality_audit_is_fail_closed_and_metadata_only():
    script = Path("scripts/audit_pdn_d4_d5_structure.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_OFFICIAL_SOURCE_PACK_D4_D5_QUALITY.cmd").read_text(encoding="utf-8")

    assert "D4_D5_STRUCTURE_QUALITY" in script
    assert "orphan_parent_count" in script
    assert "duplicate_locator_count" in script
    assert "body_fallback_count" in script
    assert "article_points_outside_articles" in script
    assert "semantic_extraction_performed" in script
    assert "scripts\\audit_pdn_d4_d5_structure.py" in cmd
