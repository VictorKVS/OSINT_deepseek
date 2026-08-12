from __future__ import annotations

import json

from father_osint.models import Material
from father_osint.storage import MaterialStore


def test_same_payload_reuses_raw_blob_but_preserves_each_observation(tmp_path):
    store = MaterialStore(tmp_path / "store")

    first = Material(
        source_type="telegram",
        source_locator="telegram://durov/540",
        title="Pavel Durov",
        raw_text="same Telegram payload",
        metadata={"chat_id": "durov", "message_id": "540"},
    )
    second = Material(
        source_type="telegram",
        source_locator="telegram://durov/540",
        title="Pavel Durov",
        raw_text="same Telegram payload",
        metadata={"chat_id": "durov", "message_id": "540"},
    )

    assert store.save_material(first) is False
    assert store.save_material(second) is True

    assert first.content_hash == second.content_hash
    assert first.local_path == second.local_path

    raw_files = list(store.raw_dir.glob("*.txt"))
    assert len(raw_files) == 1

    records = [
        json.loads(line)
        for line in store.materials_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(records) == 2
    assert records[0]["material_id"] != records[1]["material_id"]
    assert records[0]["content_hash"] == records[1]["content_hash"]
