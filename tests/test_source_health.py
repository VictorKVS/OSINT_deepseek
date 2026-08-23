from pathlib import Path

from father_osint.source_health import load_source_health, write_source_health


def test_source_health_opens_and_expires_circuit(tmp_path: Path):
    path = tmp_path / "source.json"
    state = write_source_health(
        path,
        source_key="source-a",
        status="FAILED",
        cooldown_seconds=60,
        error="timeout",
        now_epoch=1000.0,
    )
    assert state.circuit_open(1030.0) is True
    assert state.remaining_seconds(1030.0) == 30.0
    assert state.circuit_open(1061.0) is False

    loaded = load_source_health(path, source_key="source-a")
    assert loaded is not None
    assert loaded.error == "timeout"


def test_success_closes_circuit(tmp_path: Path):
    path = tmp_path / "source.json"
    write_source_health(
        path,
        source_key="source-a",
        status="OK",
        cooldown_seconds=0,
        now_epoch=1000.0,
    )
    loaded = load_source_health(path, source_key="source-a")
    assert loaded is not None
    assert loaded.circuit_open(1001.0) is False
