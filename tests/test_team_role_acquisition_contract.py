import json
from pathlib import Path


def test_team_role_registry_resolves_first_p0_profiles():
    registry = json.loads(Path("config/team_role_material_registry.json").read_text(encoding="utf-8"))
    roles = {row["role_id"]: row for row in registry["roles"]}
    for role_id in ("PROGRAMMER", "SYSTEM_ANALYST", "LEGAL_COMPLIANCE", "ML_LLM_ENGINEER"):
        assert role_id in roles
        assert roles[role_id]["priority"] == "P0"
        assert roles[role_id]["topics"]


def test_architect_is_not_reprocessed_by_universal_runner():
    text = Path("scripts/run_team_role_acquisition.py").read_text(encoding="utf-8")
    assert "ARCHITECT remains the proven reference" in text
    assert "RUN_ARCHITECT_TELEGRAM_ACQUISITION.cmd" in text


def test_role_targets_are_bounded_and_traceable():
    text = Path("scripts/run_team_role_acquisition.py").read_text(encoding="utf-8")
    assert "max_queries" in text
    assert 'target_id=f"{role[\'role_id\']}-TOPIC-{index:02d}"' in text
    assert "matched_target_ids" in text
    assert "matched_queries" in text


def test_universal_runner_reuses_proven_telegram_gates_and_deduplicates_before_download():
    py = Path("scripts/run_team_role_acquisition.py").read_text(encoding="utf-8")
    live = Path("scripts/run_team_role_acquisition_live.py").read_text(encoding="utf-8")
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
    assert "run_team_role_acquisition_live.py" in ps
    assert "--role $Role" in ps

    # Live telemetry is additive: the wrapper must delegate to the unchanged
    # universal acquisition implementation rather than duplicating semantics.
    assert "from scripts import run_team_role_acquisition as base" in live
    assert "report = await base._run(args)" in live
    assert "progress_callback" in live
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
