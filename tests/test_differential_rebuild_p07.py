from pathlib import Path

from father_osint.differential_rebuild import assemble_selective_projection


def test_selective_projection_matches_oracle_when_reused_payload_is_stable():
    canonical = [
        {"node_id": "N1", "value": "stable"},
        {"node_id": "N2", "value": "old"},
    ]
    oracle = [
        {"node_id": "N1", "value": "stable"},
        {"node_id": "N2", "value": "new"},
        {"node_id": "N3", "value": "created"},
    ]

    result = assemble_selective_projection(
        canonical,
        oracle,
        reusable_ids=["N1"],
        id_key="node_id",
    )

    assert result.reusable_payload_exact is True
    assert result.parity is True
    assert [row["node_id"] for row in result.projection_rows] == ["N1", "N2", "N3"]


def test_selective_projection_detects_false_reuse_claim():
    canonical = [{"edge_id": "E1", "value": "old"}]
    oracle = [{"edge_id": "E1", "value": "new"}]

    result = assemble_selective_projection(
        canonical,
        oracle,
        reusable_ids=["E1"],
        id_key="edge_id",
    )

    assert result.reusable_payload_exact is False
    assert result.parity is False
    assert result.reusable_payload_mismatch_ids == ("E1",)


def test_p07_differential_runner_is_shadow_only_fail_closed_and_logged():
    script = Path("scripts/prove_pdn_differential_d6_d13.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_DIFFERENTIAL_REBUILD.cmd").read_text(encoding="utf-8")

    assert ".runtime\" / \"pdn_differential_d6_d13" in script
    assert 'CHANGED_DOCUMENT_ID = "DOC-RU-FZ-152-2006"' in script
    assert '"fixture_level": "D5_DERIVED_TEXT_ONLY"' in script
    assert '"source_bytes_mutated": False' in script
    assert "build_object_delta_plan" in script
    assert "assemble_selective_projection" in script
    assert "D6_D9_CHANGED_ONLY.json" in script
    assert "full oracle D10-D12 rebuild" in script
    assert "full oracle D13 graph rebuild" in script
    assert "DIFFERENTIAL_PARITY=" in script
    assert "FULL_GRAPH_REBUILD_REQUIRED_FOR_SERVING=false" in script
    assert "D15_BLOCKED_UNTIL_REVIEW=true" in script
    assert "LEGAL_TRUTH_PROMOTED=false" in script

    assert "run_logged_python_sequence.ps1" in cmd
    assert "PDN_DIFFERENTIAL_REBUILD" in cmd
    assert "scripts\\prove_pdn_differential_d6_d13.py" in cmd
