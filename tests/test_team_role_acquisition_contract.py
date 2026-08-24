import json
from pathlib import Path

from scripts.run_team_role_acquisition import (
    TEAM_REGISTRY,
    _build_targets,
    _load_json,
    _resolve_role,
)


def test_team_role_registry_resolves_first_p0_profiles():
    registry = _load_json(TEAM_REGISTRY)
    expected = {
        "PROGRAMMER": "PROGRAMMING_KB",
        "SYSTEM_ANALYST": "SYSTEM_ANALYSIS_KB",
        "LEGAL_COMPLIANCE": "LEGAL_KB",
        "ML_LLM_ENGINEER": "AI_AGENTS_KB",
    }
    for role_id, kb_id in expected.items():
        role = _resolve_role(registry, role_id)
        assert role["knowledge_base_id"] == kb_id
        assert role["priority"] == "P0"
        assert role["topics"]


def test_architect_is_not_reprocessed_by_universal_runner():
    registry = _load_json(TEAM_REGISTRY)
    try:
        _resolve_role(registry, "ARCHITECT")
    except RuntimeError as exc:
        assert "proven reference" in str(exc)
    else:
        raise AssertionError("ARCHITECT must stay on the proven reference runner")


def test_role_targets_are_bounded_and_traceable():
    registry = _load_json(TEAM_REGISTRY)
    role = _resolve_role(registry, "PROGRAMMER")
    targets = _build_targets(role, max_queries=5)
    assert len(targets) == 5
    assert all(target.kind == "ROLE_TOPIC" for target in targets)
    assert all(target.target_id.startswith("PROGRAMMER-TOPIC-") for target in targets)
    assert all(target.query for target in targets)


def test_universal_runner_reuses_proven_telegram_gates_and_deduplicates_before_download():
    py = Path("scripts/run_team_role_acquisition.py").read_text(encoding="utf-8")
    ps = Path("scripts/run_team_role_acquisition.ps1").read_text(encoding="utf-8")
    cmd = Path("RUN_TEAM_ROLE_ACQUISITION.cmd").read_text(encoding="utf-8")

    assert "team_role_material_registry.json" in py
    assert "architect_telegram_downloads" in py
    assert "team_role_telegram" in py
    assert "destination.exists()" in py
    assert "existing local role payload" in py
    assert "SHA-256 already exists in Architect/team-role corpus" in py
    assert '"speedup_vs_1_stream_pct": None' in py
    assert '"kb_auto_promotion": False' in py
    assert "join_channel" not in py.casefold()
    assert "test_telegram_network_path.ps1" in ps
    assert "authorize_telethon_session.py" in ps
    assert "run_team_role_acquisition.py" in ps
    assert "--role $Role" in ps
    assert "RUN_TEAM_ROLE_ACQUISITION.cmd PROGRAMMER" in cmd


def test_team_role_payloads_are_gitignored():
    gitignore = Path(".gitignore").read_text(encoding="utf-8")
    assert "data/team_role_telegram/" in gitignore


def test_registry_global_policy_remains_fail_closed():
    registry = json.loads(Path("config/team_role_material_registry.json").read_text(encoding="utf-8"))
    policy = registry["global_policy"]
    assert int(policy["max_parallel_streams"]) == 5
    assert policy["auto_join_channels"] is False
    assert policy["access_control_bypass"] is False
    assert policy["paywall_bypass"] is False
    assert policy["commit_downloaded_payloads_to_git"] is False
    assert policy["sha256_required"] is True
    assert policy["provenance_required"] is True
    assert policy["kb_auto_promotion"] is False
