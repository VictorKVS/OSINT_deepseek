from pathlib import Path

from father_osint.relation_builders import (
    CROSS_ENTITY_RELATION,
    CROSS_TERM_RELATION,
    build_cross_relations,
    build_cross_relations_for_signatures,
    changed_document_cross_relation_signatures,
    cross_relation_signature,
)


def _row(document_id: str, canonical_key: str) -> dict[str, object]:
    return {
        "canonical_key": canonical_key,
        "lineage": {"document_id": document_id},
    }


def test_changed_document_cross_signatures_track_membership_gain_loss_only():
    affected = changed_document_cross_relation_signatures(
        old_terms=[_row("A", "stable"), _row("A", "lost")],
        old_entities=[_row("A", "entity-stable")],
        new_terms=[_row("A", "stable"), _row("A", "gained")],
        new_entities=[_row("A", "entity-stable"), _row("A", "entity-gained")],
    )

    assert (CROSS_TERM_RELATION, "stable") not in affected
    assert (CROSS_ENTITY_RELATION, "entity-stable") not in affected
    assert affected == {
        (CROSS_TERM_RELATION, "lost"),
        (CROSS_TERM_RELATION, "gained"),
        (CROSS_ENTITY_RELATION, "entity-gained"),
    }


def test_selective_cross_signature_rebuild_matches_full_new_d11():
    old_terms = [
        _row("A", "stable"),
        _row("A", "lost"),
        _row("B", "stable"),
        _row("B", "lost"),
        _row("B", "gained"),
        _row("C", "stable"),
    ]
    old_entities = [
        _row("A", "entity-stable"),
        _row("B", "entity-stable"),
        _row("B", "entity-gained"),
    ]
    new_terms = [
        _row("A", "stable"),
        _row("A", "gained"),
        _row("B", "stable"),
        _row("B", "lost"),
        _row("B", "gained"),
        _row("C", "stable"),
    ]
    new_entities = [
        _row("A", "entity-stable"),
        _row("A", "entity-gained"),
        _row("B", "entity-stable"),
        _row("B", "entity-gained"),
    ]

    affected = changed_document_cross_relation_signatures(
        old_terms=[row for row in old_terms if row["lineage"]["document_id"] == "A"],
        old_entities=[row for row in old_entities if row["lineage"]["document_id"] == "A"],
        new_terms=[row for row in new_terms if row["lineage"]["document_id"] == "A"],
        new_entities=[row for row in new_entities if row["lineage"]["document_id"] == "A"],
    )
    canonical = build_cross_relations(old_terms, old_entities)
    full_new = build_cross_relations(new_terms, new_entities)

    reused = [row for row in canonical if cross_relation_signature(row) not in affected]
    rebuilt = build_cross_relations_for_signatures(new_terms, new_entities, affected)
    selective = reused + rebuilt

    assert sorted(selective, key=lambda row: row["relation_id"]) == sorted(full_new, key=lambda row: row["relation_id"])
    assert any(row["canonical_key"] == "stable" for row in reused)
    assert all(cross_relation_signature(row) not in affected for row in reused)


def test_dual_path_d11_runner_contract_is_bounded_selective_and_logged():
    script = Path("scripts/prove_pdn_dual_path_d11_d13.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_DUAL_PATH_D11_REBUILD.cmd").read_text(encoding="utf-8")

    assert "changed_document_cross_relation_signatures" in script
    assert "build_cross_relations_for_signatures" in script
    assert "unchanged_d11_cross_payload_exact" in script
    assert "selective_d11_relation_reuse_ratio" in script
    assert "d12_d13_common_rebuild_in_both_paths" in script
    assert '"legal_truth_promoted": False' in script
    assert "PDN_DUAL_PATH_D11_REBUILD" in cmd
    assert "run_logged_python_sequence.ps1" in cmd
