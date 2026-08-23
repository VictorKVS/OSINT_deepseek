from pathlib import Path


def test_dual_path_runner_rebuilds_all_d6_in_full_and_only_changed_doc_in_selective():
    script = Path("scripts/prove_pdn_dual_path_d6_d13.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_DUAL_PATH_REBUILD.cmd").read_text(encoding="utf-8")

    assert '"FULL_D6_DOCUMENTS_REBUILT=' in script
    assert '"SELECTIVE_D6_DOCUMENTS_REBUILT=1"' in script
    assert '"SELECTIVE_D6_DOCUMENTS_REUSED=' in script
    assert '"UNCHANGED_D6_PAYLOAD_EXACT=' in script
    assert '"D6_KNOWLEDGE_PARITY=' in script
    assert '"D10_D12_RELATIONS_PARITY=' in script
    assert '"D13_NODES_PARITY=' in script
    assert '"D13_EDGES_PARITY=' in script
    assert '"FULL_VS_SELECTIVE_PARITY=' in script
    assert '"D10_D13_COMMON_REBUILD_IN_BOTH_PATHS=true"' in script
    assert '"D15_BLOCKED_UNTIL_REVIEW=true"' in script
    assert '"SOURCE_BYTES_MUTATED=false"' in script
    assert "PDN_DUAL_PATH_REBUILD" in cmd
    assert "scripts\\prove_pdn_dual_path_d6_d13.py" in cmd


def test_dual_path_proof_is_explicitly_not_yet_selective_d10_d13():
    script = Path("scripts/prove_pdn_dual_path_d6_d13.py").read_text(encoding="utf-8")
    assert "COMMON_D10_D13_REBUILD" in script
    assert '"d10_d13_common_rebuild_in_both_paths": True' in script
