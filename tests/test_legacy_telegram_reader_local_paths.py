from pathlib import Path

from legacy.telegram import simple_reader


def test_default_legacy_paths_live_beside_module():
    module_dir = Path(simple_reader.__file__).resolve().parent

    assert simple_reader.DEFAULT_CONFIG_PATH == module_dir / "config.yaml"
    assert simple_reader.DEFAULT_SESSION_PATH == module_dir / "reader_session"


def test_reader_uses_explicit_paths(monkeypatch, tmp_path):
    config_path = tmp_path / "config.yaml"
    session_path = tmp_path / "reader_session"
    synthetic_config = {
        "telegram": {
            "api_id": 123,
            "api_hash": "synthetic",
            "phone_number": "+10000000000",
            "channels": [],
            "collection": {"limit_per_channel": 100},
        }
    }

    monkeypatch.setattr(
        simple_reader.TelegramReader,
        "load_config",
        staticmethod(lambda _path: synthetic_config),
    )

    reader = simple_reader.TelegramReader(
        config_path=config_path,
        session_path=session_path,
    )

    assert reader.config_path == config_path
    assert reader.session_path == session_path
    assert reader.config["telegram"]["collection"]["limit_per_channel"] == 100
