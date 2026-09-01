from pathlib import Path

from father_osint.relation_builders import build_internal_relations_for_document


def _lineage(document_id: str, chunk_id: str) -> dict[str, str]:
    return {
        "document_id": document_id,
        "version_id": "v1",
        "chunk_id": chunk_id,
        "chunk_locator": "x",
        "structure_node_id": "s1",
        "artifact_sha256": "a" * 64,
        "source_text_sha256": "b" * 64,
    }


def test_internal_relations_are_document_local_and_deterministic():
    payload = {
        "terms": [],
        "definitions": [
            {
                "definition_id": "DEF-1",
                "canonical_key": "personal_data",
                "lineage": _lineage("DOC:A", "CHK-1"),
            }
        ],
        "requirements": [
            {
                "requirement_id": "REQ-1",
                "lineage": _lineage("DOC:A", "CHK-2"),
            }
        ],
        "entities": [
            {
                "entity_mention_id": "ENT-1",
                "canonical_key": "personal_data_operator",
                "lineage": _lineage("DOC:A", "CHK-2"),
            }
        ],
    }

    first = build_internal_relations_for_document("DOC:A", payload)
    second = build_internal_relations_for_document("DOC:A", payload)

    assert first == second
    assert len(first) == 2
    assert {row["relation_type"] for row in first} == {"TERM_DEFINED_BY", "REQUIREMENT_MENTIONS_ENTITY"}
    assert {row["document_id"] for row in first} == {"DOC:A"}
    assert all(row["review_state"] == "CANDIDATE_NEEDS_REVIEW" for row in first)
    assert all(row["promotion_state"] == "NOT_PROMOTED" for row in first)


def test_dual_path_d10_runner_contract_is_selective_and_logged():
    script = Path("scripts/prove_pdn_dual_path_d10_d13.py").read_text(encoding="utf-8")
    cmd = Path("RUN_PDN_DUAL_PATH_D10_REBUILD.cmd").read_text(encoding="utf-8")

    assert "build_internal_relations_for_document" in script
    assert "canonical_internal" in script
    assert 'str(row.get("document_id")) != CHANGED_DOCUMENT_ID' in script
    assert '"selective_d10_documents_rebuilt": 1' in script
    assert '"selective_d10_documents_reused": len(TARGETS) - 1' in script
    assert '"d11_d13_common_rebuild_in_both_paths": True' in script
    assert '"full_vs_selective_parity": full_vs_selective' in script
    assert '"d15_blocked_until_review": True' in script
    assert "run_logged_python_sequence.ps1" in cmd
    assert "PDN_DUAL_PATH_D10_REBUILD" in cmd
