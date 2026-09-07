import json
from pathlib import Path


def test_investigation_product_baseline_exists_and_is_case_centric():
    text = Path("docs/10_investigation_workspace/README.md").read_text(encoding="utf-8")
    for token in (
        "CASE -> QUESTIONS -> HYPOTHESES",
        "Tool Router",
        "Graph Workspace",
        "Evidence Table",
        "Hypothesis Board",
        "Report Builder",
        "v1 acceptance gate",
    ):
        assert token in text


def test_investigation_tool_registry_is_bounded_and_has_status_policy():
    payload = json.loads(Path("config/investigation_tool_registry.json").read_text(encoding="utf-8"))
    assert payload["record_type"] == "INVESTIGATION_TOOL_REGISTRY"
    tools = payload["tools"]
    ids = [tool["tool_id"] for tool in tools]
    assert len(ids) == len(set(ids))
    assert "TELEGRAM_SEARCH" in ids
    assert "LOCAL_KB" in ids
    assert "BITCOIN_TRACE" in ids
    assert "TRON_TRACE" in ids
    assert "NARRATIVE_DRIFT" in ids
    for tool in tools:
        assert tool["status"] in {"READY", "NEEDS_CONFIG", "EXPERIMENTAL", "PLANNED", "OFFLINE", "BLOCKED_BY_POLICY"}
        assert tool["policy"]
        assert tool["requires_case"] is True
        assert tool["capabilities"]
        assert tool["outputs"]


def test_case_schema_requires_evidence_backed_investigation_objects():
    schema = json.loads(Path("schemas/investigation_case.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    for field in ("questions", "hypotheses", "entities", "relations", "findings", "evidence", "claims", "timeline", "conclusions"):
        assert field in required
    relation = schema["$defs"]["relation"]
    assert "evidence_ids" in relation["required"]
    assert relation["properties"]["evidence_ids"]["minItems"] == 1


def test_investigation_workspace_shell_has_three_projection_modes_and_trace():
    html = Path("osint_web/static/investigation.html").read_text(encoding="utf-8")
    for token in (
        "INVESTIGATION WORKSPACE",
        "CASE-2026-0001",
        "Questions & Hypotheses",
        "Investigation Canvas",
        "Graph",
        "Table",
        "Timeline",
        "SELECTED OBJECT",
        "CHAIN OF CUSTODY",
        "Evidence-backed edges only",
        "Telegram",
        "Bitcoin / TRON",
    ):
        assert token in html
