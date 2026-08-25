import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "programmer_algorithm_bibliography_targets.json"
RUNNER = ROOT / "scripts" / "probe_programmer_algorithm_bibliography_telegram.py"
LAUNCHER = ROOT / "RUN_PROGRAMMER_ALGORITHM_TELEGRAM_PROBE.cmd"


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_algorithm_bibliography_wave_is_bounded_probe_only_and_five_streams():
    payload = load_registry()
    policy = payload["policy"]
    targets = payload["targets"]
    assert payload["registry_id"] == "PROGRAMMER-ALGORITHM-BIBLIOGRAPHY-PROBE-001"
    assert policy["probe_only"] is True
    assert policy["download"] is False
    assert policy["max_parallel_streams"] == 5
    assert len(targets) == 31
    ids = [row["id"] for row in targets]
    assert len(ids) == len(set(ids))
    assert all(row["query_variants"] for row in targets)


def test_requested_algorithm_books_and_python_track_are_present():
    targets = load_registry()["targets"]
    titles = {row["title"] for row in targets}
    assert any("Grokking Algorithms" in title for title in titles)
    assert "Introduction to Algorithms, Third Edition" in titles
    assert any("The Algorithm Design Manual" in title for title in titles)
    assert "Algorithms + Data Structures = Programs" in titles
    assert "Analysis of Algorithms: An Active Learning Approach" in titles
    assert any("Алгоритмы в задачах и примерах" in title for title in titles)
    assert any("Algorithms in C++, Parts 1-4" in title for title in titles)
    knuth = [row for row in targets if row["track"] == "KNUTH"]
    assert {row["id"] for row in knuth} == {"KNUTH-001", "KNUTH-002", "KNUTH-003", "KNUTH-004A", "KNUTH-004B"}
    python_rows = [row for row in targets if row["track"] == "PYTHON"]
    assert len(python_rows) == 5
    assert all("Python" in row["language_focus"] for row in python_rows)


def test_language_specific_analogs_cover_java_cpp_go_and_rust():
    tracks = {row["track"] for row in load_registry()["targets"]}
    assert {"JAVA", "CPP", "GO", "RUST"}.issubset(tracks)


def test_algorithm_probe_runner_and_launcher_never_download():
    runner = RUNNER.read_text(encoding="utf-8")
    launcher = LAUNCHER.read_text(encoding="utf-8")
    assert "downloaded_total" in runner
    assert '"probe_only": True' in runner
    assert "download_media" not in runner
    assert "--priority ALL" in launcher
    assert "no book download" in launcher
