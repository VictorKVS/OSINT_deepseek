from pathlib import Path

from father_osint.relation_builders import (
    DEFINITION_VARIANCE_CANDIDATE,
    REQUIREMENT_OVERLAP_CANDIDATE,
    build_conflict_candidates,
    build_conflict_candidates_for_signatures,
    changed_document_conflict_signatures,
    conflict_candidate_signature,
    normalized_requirement_statement,
)


def _definition(document_id: str, definition_id: str, canonical_key: str, text: str) -> dict[str, object]:
    return {
        "definition_id": definition_id,
        "canonical_key": canonical_key,
        "definition": text,
        "lineage": {"document_id": document_id},
    }


def _requirement(document_id: str, requirement_id: str, statement: str) -> dict[str, object]:
    return {
        "requirement_id": requirement_id,
        "statement": statement,
        "lineage": {"document_id": document_id},
    }


def test_changed_document_conflict_signatures_use_union_not_only_membership_delta():
    affected = changed_document_conflict_signatures(
        old_definitions=[_definition("A", "d1", "personal_data", "old")],
        old_requirements=[_requirement("A", "r1", "Оператор обязан сделать X.")],
        new_definitions=[_definition("A", "d2", "personal_data", "new")],
        new_requirements=[_requirement("A", "r2", "Оператор обязан сделать X.")],
    )

    assert (DEFINITION_VARIANCE_CANDIDATE, "personal_data") in affected
    assert (
        REQUIREMENT_OVERLAP_CANDIDATE,
        normalized_requirement_statement(_requirement("A", "x", "Оператор обязан сделать X.")),
    ) in affected


def test_selective_conflict_rebuild_matches_full_new_d12():
    old_defs = [
        _definition("A", "a1", "k1", "Определение один"),
        _definition("B", "b1", "k1", "Определение два"),
        _definition("B", "b2", "k2", "Стабильное один"),
        _definition("C", "c2", "k2", "Стабильное два"),
    ]
    old_reqs = [
        _requirement("A", "ar1", "Обязан выполнить X."),
        _requirement("B", "br1", "Обязан выполнить X."),
        _requirement("B", "br2", "Обязан выполнить Y."),
        _requirement("C", "cr2", "Обязан выполнить Y."),
    ]
    new_defs = [
        _definition("A", "a1-new", "k1", "Определение изменено"),
        _definition("B", "b1", "k1", "Определение два"),
        _definition("B", "b2", "k2", "Стабильное один"),
        _definition("C", "c2", "k2", "Стабильное два"),
    ]
    new_reqs = [
        _requirement("A", "ar1-new", "Обязан выполнить X."),
        _requirement("B", "br1", "Обязан выполнить X."),
        _requirement("B", "br2", "Обязан выполнить Y."),
        _requirement("C", "cr2", "Обязан выполнить Y."),
    ]

    affected = changed_document_conflict_signatures(
        old_definitions=[row for row in old_defs if row["lineage"]["document_id"] == "A"],
        old_requirements=[row for row in old_reqs if row["lineage"]["document_id"] == "A"],
        new_definitions=[row for row in new_defs if row["lineage"]["document_id"] == "A"],
        new_requirements=[row for row in new_reqs if row["lineage"]["document_id"] == "A"],
    )
    canonical = build_conflict_candidates(old_defs, old_reqs)
    full_new = build_conflict_candidates(new_defs, new_reqs)
    old_statement_by_id = {
        str(row["requirement_id"]): normalized_requirement_statement(row)
        for row in old_reqs
    }

    reused = [
        row for row in canonical
        if conflict_candidate_signature(row, requirement_statement_by_id=old_statement_by_id) not in affected
    ]
    rebuilt = build_conflict_candidates_for_signatures(new_defs, new_reqs, affected)
    selective = reused + rebuilt

    assert sorted(selective, key=lambda row: row["candidate_id"]) == sorted(full_new, key=lambda row: row["candidate_id"])
    assert any(row.get("canonical_key") == "k2" for row in reused)


def test_dual_path_d12_runner_contract_is_selective_and_logged():
    script = Path("scripts/prove_pdn_dual_path_d12_d13.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_DUAL_PATH_D12_REBUILD.cmd").read_text(encoding="utf-8")

    assert "changed_document_conflict_signatures" in script
    assert "build_conflict_candidates_for_signatures" in script
    assert "unchanged_d12_conflict_payload_exact" in script
    assert "selective_d12_candidate_reuse_ratio" in script
    assert "d13_common_rebuild_in_both_paths" in script
    assert '"legal_truth_promoted": False' in script
    assert "PDN_DUAL_PATH_D12_REBUILD" in cmd
    assert "run_logged_python_sequence.ps1" in cmd
