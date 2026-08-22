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

    assert "def _resolve_repo_path" in script
    assert "if not path.is_absolute()" in script
    assert "path = REPO_ROOT / path" in script
    assert "inbox = _resolve_repo_path(args.inbox)" in script
    assert "root = _resolve_repo_path(args.root)" in script
    assert "export_review = _resolve_repo_path(args.export_review)" in script
    assert "path = existing[0].resolve()" in script
    assert "path.relative_to(REPO_ROOT).as_posix()" in script
