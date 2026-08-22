from pathlib import Path


def test_official_source_pack_d4_d5_runner_uses_normal_operator_conveyor():
    cmd = Path("RUN_PDN_OFFICIAL_SOURCE_PACK_D4_D5.cmd").read_text(encoding="utf-8")

    assert "scripts\\run_pdn_operator_import.py" in cmd
    assert "data\\operator_import\\pdn_official_source_pack" in cmd
    assert "data\\knowledge_factory\\pdn_official_batch" in cmd
    assert "reports\\pdn_live" in cmd
    assert "D4-D5" in cmd
    assert "normal conveyor" in cmd
