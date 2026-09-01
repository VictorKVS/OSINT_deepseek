import json
from pathlib import Path


def _registry():
    return json.loads(Path("config/team_role_material_registry.json").read_text(encoding="utf-8"))


def test_team_role_registry_has_proven_architect_reference_and_raw_metrics_only():
    registry = _registry()
    reference = registry["reference_run"]
    assert reference["role_id"] == "ARCHITECT"
    assert reference["status"] == "PROVEN_REFERENCE"
    metrics = reference["observed_metrics"]
    assert metrics["lessons_total"] == 31
    assert metrics["lessons_missing_primary_sources"] == 24
    assert metrics["search_hits_total"] == 204
    assert metrics["downloaded_total"] == 7
    assert metrics["payload_reused_total"] == 2
    assert metrics["errors_total"] == 0
    assert metrics["speedup_vs_1_stream_pct"] is None


def test_team_role_registry_uses_exactly_five_active_streams_with_unique_roles():
    registry = _registry()
    streams = registry["streams"]
    assert [stream["stream_id"] for stream in streams] == [1, 2, 3, 4, 5]
    assigned = [role for stream in streams for role in stream["roles"]]
    assert len(assigned) == len(set(assigned))
    role_ids = {role["role_id"] for role in registry["roles"]}
    assert set(assigned).issubset(role_ids)
    assert "ARCHITECT" not in assigned


def test_team_role_registry_keeps_acquisition_and_promotion_fail_closed():
    registry = _registry()
    policy = registry["global_policy"]
    assert policy["max_parallel_streams"] == 5
    assert policy["auto_join_channels"] is False
    assert policy["access_control_bypass"] is False
    assert policy["paywall_bypass"] is False
    assert policy["commit_downloaded_payloads_to_git"] is False
    assert policy["sha256_required"] is True
    assert policy["provenance_required"] is True
    assert policy["kb_auto_promotion"] is False


def test_every_non_reference_role_has_topics_material_types_and_maturity_path():
    registry = _registry()
    roles = [role for role in registry["roles"] if role["role_id"] != "ARCHITECT"]
    assert roles
    for role in roles:
        assert role["state"]
        assert role["priority"] in {"P0", "P1", "P2"}
        assert len(role["topics"]) >= 10
        assert len(role["material_types"]) >= 4
    assert set(registry["maturity_gates"]) == {"MIN", "MEDIUM", "MAX"}
