import pytest

from father_osint.models import Material
from father_osint.reliability import (
    DurableObservationWriter,
    JsonCheckpointStore,
    SourceCheckpoint,
)


class RecordingStore:
    def __init__(self, events, fail=False):
        self.events = events
        self.fail = fail

    def save_material(self, material):
        self.events.append(("save", material.material_id))
        if self.fail:
            raise OSError("simulated durable storage failure")
        return False


class RecordingCheckpointStore(JsonCheckpointStore):
    def __init__(self, path, events):
        super().__init__(path)
        self.events = events

    def commit(self, checkpoint):
        self.events.append(("checkpoint", checkpoint.cursor))
        super().commit(checkpoint)


def make_material():
    return Material(
        source_type="telegram",
        source_locator="telegram://100/540",
        title="Evidence",
        raw_text="Observed evidence",
        metadata={"chat_id": "100", "message_id": "540"},
    )


def test_checkpoint_advances_only_after_successful_material_save(tmp_path):
    events = []
    checkpoints = RecordingCheckpointStore(tmp_path / "checkpoints.json", events)
    writer = DurableObservationWriter(RecordingStore(events), checkpoints)

    writer.save_then_checkpoint(
        material=make_material(),
        source_key="100",
        cursor="540",
    )

    assert events[0][0] == "save"
    assert events[1] == ("checkpoint", "540")
    assert checkpoints.load("telegram", "100").cursor == "540"


def test_failed_material_save_does_not_advance_checkpoint(tmp_path):
    events = []
    checkpoints = RecordingCheckpointStore(tmp_path / "checkpoints.json", events)
    checkpoints.commit(
        SourceCheckpoint(
            source_type="telegram",
            source_key="100",
            cursor="539",
        )
    )
    events.clear()
    writer = DurableObservationWriter(RecordingStore(events, fail=True), checkpoints)

    with pytest.raises(OSError, match="simulated durable storage failure"):
        writer.save_then_checkpoint(
            material=make_material(),
            source_key="100",
            cursor="540",
        )

    assert len(events) == 1
    assert events[0][0] == "save"
    assert checkpoints.load("telegram", "100").cursor == "539"


def test_checkpoint_survives_restart(tmp_path):
    path = tmp_path / "checkpoints.json"
    first_process = JsonCheckpointStore(path)
    writer = DurableObservationWriter(RecordingStore([]), first_process)
    writer.save_then_checkpoint(
        material=make_material(),
        source_key="100",
        cursor="540",
    )

    restarted_process = JsonCheckpointStore(path)
    checkpoint = restarted_process.load("telegram", "100")

    assert checkpoint is not None
    assert checkpoint.cursor == "540"
