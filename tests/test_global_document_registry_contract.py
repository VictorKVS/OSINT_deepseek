import json
from pathlib import Path

from scripts.build_global_document_registry import build


def test_global_document_registry_policy_is_mandatory_and_shared():
    policy = json.loads(Path("config/global_document_registry_policy.json").read_text(encoding="utf-8"))
    assert policy["status"] == "MANDATORY"
    assert policy["scope"] == "ALL_FATHER_KNOWLEDGE_BASES_AND_ROLES"
    assert policy["identity_rules"]["role_specific_document_copies_forbidden"] is True
    assert policy["acceptance_gates"]["library_orders_must_resolve_documents_via_global_registry"] is True
    assert "APPLICABILITY_BINDING" in policy["canonical_layers"]


def test_existing_domain_registries_are_import_sources_not_parallel_truths():
    sources = json.loads(Path("config/global_document_registry_sources.json").read_text(encoding="utf-8"))
    enabled = {row["source_id"] for row in sources["sources"] if row.get("enabled")}
    assert {
        "PDN_CURRENT",
        "PROGRAMMER_ESPD",
        "PROGRAMMER_AUTOMATED_SYSTEMS",
        "PROGRAMMER_RU_BASELINE",
        "PROGRAMMER_FSTEC_REGULATED",
        "PROGRAMMER_RU_NORMATIVE_SCOPE",
    } <= enabled


def test_builder_deduplicates_shared_documents_and_preserves_observations():
    registry, bindings, conflicts = build()
    ids = [row["document_id"] for row in registry["documents"]]
    assert len(ids) == len(set(ids))
    gost = [row for row in registry["documents"] if row.get("designation") == "ГОСТ 19.101-2024"]
    assert len(gost) == 1
    assert len(gost[0]["source_observations"]) >= 2
    assert any(row["document_id"] == "DOC-RU-FZ-152-2006" for row in registry["documents"])
    assert registry["acceptance"]["conflicting_current_status_total"] == 0
    assert registry["acceptance"]["binding_missing_document_total"] == 0
    assert conflicts["conflicts_total"] == registry["conflicts_total"]


def test_programmer_and_kb_use_bindings_to_shared_document_ids():
    registry, binding_payload, _ = build()
    known = {row["document_id"] for row in registry["documents"]}
    rows = binding_payload["bindings"]
    programmer = [row for row in rows if row["subject_type"] == "ROLE" and row["subject_id"] == "PROGRAMMER"]
    programming_kb = [row for row in rows if row["subject_type"] == "KNOWLEDGE_BASE" and row["subject_id"] == "PROGRAMMING_KB"]
    assert programmer
    assert programming_kb
    assert all(row["document_id"] in known for row in programmer + programming_kb)


def test_programmer_l1_laws_and_fstec_live_once_in_global_registry():
    registry, binding_payload, _ = build()
    documents = {row["document_id"]: row for row in registry["documents"]}
    assert "DOC-RU-FZ-162-2015" in documents
    assert "DOC-RU-FZ-187-2017" in documents
    assert "DOC-RU-FSTEC-117-2025" in documents
    assert "DOC-RU-FSTEC-137-2026" in documents
    assert documents["DOC-RU-FSTEC-117-2025"]["document_type"] == "REGULATOR_ACT"
    assert documents["DOC-RU-FSTEC-137-2026"]["legal_status"] == "FUTURE_EFFECTIVE"

    rows = binding_payload["bindings"]
    for document_id in ("DOC-RU-FZ-162-2015", "DOC-RU-FZ-187-2017", "DOC-RU-FSTEC-117-2025"):
        assert any(
            row["document_id"] == document_id
            and row["subject_type"] == "ROLE"
            and row["subject_id"] == "PROGRAMMER"
            for row in rows
        )
        assert any(
            row["document_id"] == document_id
            and row["subject_type"] == "KNOWLEDGE_BASE"
            and row["subject_id"] == "PROGRAMMING_KB"
            for row in rows
        )


def test_every_global_binding_has_two_axis_classification():
    _, binding_payload, _ = build()
    rows = binding_payload["bindings"]
    assert rows
    assert all(row["maturity_level"] in {"MIN", "MEDIUM", "MAX"} for row in rows)
    assert all(row["importance_class"] in {"NECESSARY", "DESIRABLE", "INTERESTING_LATER"} for row in rows)


def test_library_order_start_rebuilds_and_attaches_global_registry():
    text = Path("scripts/start_library_order.py").read_text(encoding="utf-8")
    assert "build_global_document_registry.py" in text
    assert "attach_global_registry" in text
    assert "resolved_document_refs" in text
    assert "STAGE_0_GLOBAL_DOCUMENT_REGISTRY_RESOLUTION" in text
    assert text.index("build_global_registry()") < text.index("create_cmd = [")


def test_library_order_policy_places_global_registry_before_role_regulatory_stage():
    policy = json.loads(Path("config/library_order_policy.json").read_text(encoding="utf-8"))
    assert policy["pipeline"][1] == "STAGE_0_GLOBAL_DOCUMENT_REGISTRY_RESOLUTION"
    assert policy["pipeline"][2] == "STAGE_0_RU_REGULATORY_BASELINE"
    assert policy["global_document_registry"]["runtime_registry"].endswith("GLOBAL_DOCUMENT_REGISTRY.json")
