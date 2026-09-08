import json
from pathlib import Path


SCHEMAS = Path("schemas")


def _load(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def test_tool_adapter_declares_typed_io_edges_and_execution_controls():
    schema = _load("father_analyst_tool_adapter.schema.json")
    required = set(schema["required"])
    for field in (
        "tool_id",
        "execution_profile",
        "input_types",
        "output_types",
        "possible_edge_types",
        "network_policy",
        "legal_mode",
        "parallelism_class",
        "rate_limit_policy",
        "cost_policy",
        "normalizer_version",
        "health_check",
    ):
        assert field in required
    assert "WALLET" in schema["$defs"]["entityType"]["enum"]
    assert "DOMAIN" in schema["$defs"]["entityType"]["enum"]
    assert "EMAIL" in schema["$defs"]["entityType"]["enum"]


def test_observation_contract_keeps_possible_edges_candidate_only():
    schema = _load("father_analyst_observation.schema.json")
    required = set(schema["required"])
    for field in (
        "observation_id",
        "case_id",
        "tool_run_id",
        "tool_id",
        "source_locator",
        "raw_artifact_ref",
        "independence_group",
        "state",
    ):
        assert field in required
    edge = schema["properties"]["possible_edges"]["items"]
    assert edge["properties"]["state"]["const"] == "CANDIDATE"
    assert "basis_observation_ids" in edge["required"]


def test_analysis_packet_is_local_context_budget_contract():
    schema = _load("father_analyst_analysis_packet.schema.json")
    required = set(schema["required"])
    assert {"evidence_refs", "excerpts", "max_chars", "actual_chars", "source_versions"} <= required
    assert schema["properties"]["max_chars"]["maximum"] == 200000
    assert "SOCRATES" in schema["properties"]["role"]["enum"]
    assert "MAIN_ANALYST" in schema["properties"]["role"]["enum"]


def test_promotion_request_requires_human_pass_and_blocks_direct_kb_write():
    schema = _load("father_analyst_promotion_request.schema.json")
    required = set(schema["required"])
    assert {"review_decision", "reviewed_by", "reviewed_at", "evidence_bindings", "request_sha256"} <= required
    assert schema["properties"]["review_decision"]["const"] == "PASS"
    assert schema["properties"]["direct_kb_write_allowed"]["const"] is False
    assert schema["properties"]["evidence_bindings"]["minItems"] == 1


def test_codex_master_plan_preserves_canonical_pipeline():
    text = Path("docs/11_unified_analyst/CODEX_MASTER_PLAN.md").read_text(encoding="utf-8")
    for token in (
        "TOOL FACTORY / WORKERS",
        "RAW ARTIFACT VAULT",
        "EVIDENCE LAYER",
        "ANALYSIS ZOO",
        "REASONING GRAPH",
        "SOCRATES",
        "HUMAN REVIEW",
        "D14 -> D15",
        "KNOWLEDGE BASE",
    ):
        assert token in text
