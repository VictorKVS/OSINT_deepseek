from pathlib import Path


def test_prebuilt_db_semantic_audit_separates_version_quality_and_hot_path():
    script = Path("scripts/audit_152_prebuilt_db_semantics.py").read_text(encoding="utf-8")
    cmd = Path("RUN_AUDIT_152_PREBUILT_DB_SEMANTICS.cmd").read_text(encoding="utf-8")

    assert "PRAGMA quick_check" in script
    assert "integrity_check_excluded_from_hot_path" in script
    assert "HOT_ITERATIONS = 100" in script
    assert "query_p50_ms" in script
    assert "query_p95_ms" in script
    assert "version_scope_mismatch_with_father_base_publication" in script
    assert "whole_document_similarity_is_not_a_valid_quality_gate_when_versions_differ" in script
    assert "article_comparisons" in script
    assert "duplicate_content_rows" in script
    assert "provision_count_consistent" in script
    assert '"legal_truth_promoted": False' in script
    assert "HOT_QUERY_P50_MS=" in script
    assert "ARTICLE_SEQUENCE_MEDIAN=" in script
    assert "scripts\\audit_152_prebuilt_db_semantics.py" in cmd
