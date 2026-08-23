from datetime import date
from pathlib import Path

from father_osint.freshness_checkpoint import (
    FreshnessCheckpoint,
    load_freshness_checkpoint,
    resolve_freshness_window,
    write_freshness_checkpoint,
)


def test_no_checkpoint_uses_bootstrap_backfill_not_fixed_recent_window():
    window = resolve_freshness_window(
        today=date(2026, 8, 23),
        bootstrap_lookback_days=90,
        checkpoint_overlap_days=3,
        checkpoint=None,
    )

    assert window.mode == "BOOTSTRAP_BACKFILL"
    assert window.publish_date_from == "2026-05-25"
    assert window.publish_date_to == "2026-08-23"
    assert window.checkpoint_publish_date_to is None


def test_checkpoint_window_replays_overlap_before_last_complete_watermark():
    checkpoint = FreshnessCheckpoint(
        watchlist_id="WATCH",
        source_key="SOURCE",
        last_complete_publish_date_to="2026-08-20",
        last_complete_observed_at="2026-08-20T12:00:00+00:00",
    )
    window = resolve_freshness_window(
        today=date(2026, 8, 23),
        bootstrap_lookback_days=90,
        checkpoint_overlap_days=3,
        checkpoint=checkpoint,
    )

    assert window.mode == "INCREMENTAL_FROM_CHECKPOINT"
    assert window.publish_date_from == "2026-08-17"
    assert window.publish_date_to == "2026-08-23"
    assert window.checkpoint_publish_date_to == "2026-08-20"


def test_checkpoint_persists_atomically_and_is_scoped_to_watchlist_and_source(tmp_path: Path):
    path = tmp_path / "freshness.json"
    written = write_freshness_checkpoint(
        path,
        watchlist_id="WATCH",
        source_key="SOURCE",
        publish_date_to="2026-08-23",
        observed_at="2026-08-23T19:00:00+00:00",
    )

    assert path.is_file()
    loaded = load_freshness_checkpoint(path, watchlist_id="WATCH", source_key="SOURCE")
    assert loaded == written
    assert load_freshness_checkpoint(path, watchlist_id="OTHER", source_key="SOURCE") is None
    assert load_freshness_checkpoint(path, watchlist_id="WATCH", source_key="OTHER") is None


def test_freshness_runner_never_advances_checkpoint_on_degraded_observation_contract():
    script = Path("scripts/run_pdn_freshness_discovery.py").read_text(encoding="utf-8")
    watchlist = Path("config/pdn_freshness_watchlist.json").read_text(encoding="utf-8")

    assert "load_freshness_checkpoint" in script
    assert "resolve_freshness_window" in script
    assert "write_freshness_checkpoint" in script
    assert "if observation_complete:" in script
    assert "degraded_run_did_not_advance" in script
    assert "WINDOW_MODE=" in script
    assert "CHECKPOINT_ADVANCED=" in script
    assert '"bootstrap_lookback_days": 90' in watchlist
    assert '"checkpoint_overlap_days": 3' in watchlist
