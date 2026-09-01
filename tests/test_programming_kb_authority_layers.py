import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYERS = ROOT / "config" / "programming_kb_source_layers.json"
AUTHORITATIVE = ROOT / "scripts" / "acquire_programming_kb_authoritative_sources.py"
FACTORY = ROOT / "scripts" / "run_programming_kb_source_factory.py"
TEAM_BOOTSTRAP = ROOT / "scripts" / "run_team_role_acquisition.ps1"
ALGO_LAUNCHER = ROOT / "RUN_PROGRAMMER_ALGORITHM_TELEGRAM_PROBE.cmd"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_programming_kb_authority_layers_are_ordered_and_training_is_last():
    payload = json.loads(LAYERS.read_text(encoding="utf-8"))
    assert payload["layer_order"] == [
        "L1_RU_LAW_GOST_REGULATORS",
        "L2_LANGUAGE_PRIMARY_AUTHORITY",
        "L3_SCIENTIFIC_PROFESSIONAL_CONSENSUS",
        "L4_BOOKS_EDUCATIONAL_PRACTICE",
        "L5_WORLD_PRODUCTION_EVIDENCE",
        "L6_TASKS_AND_TRAINING",
    ]
    assert payload["layers"][-1]["state"] == "HOLD_UNTIL_L1_L5_MIN_GATES"


def test_primary_language_layer_uses_official_sources_and_rights_gates_iso_text():
    payload = json.loads(LAYERS.read_text(encoding="utf-8"))
    layer = next(row for row in payload["layers"] if row["layer_id"] == "L2_LANGUAGE_PRIMARY_AUTHORITY")
    targets = {row["source_id"]: row for row in layer["targets"]}
    assert targets["LANGSRC-PYTHON-REFERENCE"]["url"].startswith("https://docs.python.org/")
    assert targets["LANGSRC-GO-SPEC"]["url"] == "https://go.dev/ref/spec"
    assert targets["LANGSRC-RUST-REFERENCE"]["url"].startswith("https://doc.rust-lang.org/")
    assert targets["LANGSRC-ECMASCRIPT-SPEC"]["url"] == "https://tc39.es/ecma262/"
    assert targets["LANGSRC-CPP-STANDARD"]["acquisition"] == "PRIMARY_METADATA_AND_AUTHORIZED_STANDARD_COPY"
    assert targets["LANGSRC-C-STANDARD"]["rights_gate"]


def test_authoritative_acquisition_builds_l2_l3_l5_without_rights_gated_iso_fulltext():
    mod = load_module(AUTHORITATIVE, "programming_kb_authoritative_acquire")
    rows, gated = mod.build_targets()
    layers = {row["source_layer"] for row in rows}
    assert {"L2_LANGUAGE_PRIMARY_AUTHORITY", "L3_SCIENTIFIC_PROFESSIONAL_CONSENSUS", "L5_WORLD_PRODUCTION_EVIDENCE"}.issubset(layers)
    ids = {row["id"] for row in rows}
    assert "LANGSRC-CPP-STANDARD" not in ids
    assert "LANGSRC-C-STANDARD" not in ids
    gated_ids = {row.get("source_id") for row in gated}
    assert {"LANGSRC-CPP-STANDARD", "LANGSRC-C-STANDARD"}.issubset(gated_ids)
    assert len(rows) <= 30


def test_source_factory_executes_authority_layers_before_books_and_training():
    text = FACTORY.read_text(encoding="utf-8")
    assert text.index("RU_NORMATIVE_SCOPE_GATE") < text.index("AUTHORITATIVE_L2_L3_L5_ACQUISITION")
    assert text.index("AUTHORITATIVE_L2_L3_L5_ACQUISITION") < text.index("BOOKS_AND_OPEN_PAPERS_ACQUISITION")
    assert text.index("BOOKS_AND_OPEN_PAPERS_ACQUISITION") < text.index("KNOWLEDGE_DECOMPOSITION")
    assert text.index("KNOWLEDGE_DECOMPOSITION") < text.index("LAYER_READINESS_AUDIT")
    assert "programming_kb_min_ready" in text
    assert "PASS_BUILDING_KB" in text


def test_algorithm_telegram_probe_uses_existing_dpapi_bootstrap():
    bootstrap = TEAM_BOOTSTRAP.read_text(encoding="utf-8")
    launcher = ALGO_LAUNCHER.read_text(encoding="utf-8")
    assert "AlgorithmBibliographyProbe" in bootstrap
    assert "probe_programmer_algorithm_bibliography_telegram.py" in bootstrap
    assert "run_team_role_acquisition.ps1" in launcher
    assert "-AlgorithmBibliographyProbe" in launcher
    assert "--priority ALL" in launcher
    assert "TELEGRAM_API_HASH" not in launcher
