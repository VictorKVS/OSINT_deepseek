from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from father_osint.agent import OSINTAgent
from father_osint.models import Material, ResearchTask
from father_osint.review_pipeline import DevReviewPipeline
from father_osint.storage import MaterialStore


class StagedCollector:
    """Return telegram in the first call and github in the second call."""

    name = "staged"
    source_types = {"telegram", "github"}

    def __init__(self) -> None:
        self.calls = 0

    def collect(self, task):
        self.calls += 1
        if self.calls == 1 and "telegram" in task.source_types:
            yield Material(
                source_type="telegram",
                source_locator="https://t.me/example/1",
                title="Telegram evidence",
                raw_text="telegram payload",
            )
        elif self.calls >= 2 and "github" in task.source_types:
            yield Material(
                source_type="github",
                source_locator="https://github.com/example/repo",
                title="GitHub evidence",
                raw_text="github payload",
            )


def test_ac11_follow_up_cycles_review_cumulative_evidence(tmp_path: Path):
    agent = OSINTAgent(MaterialStore(tmp_path / "store"), [StagedCollector()])
    task = ResearchTask(
        question="evidence",
        source_types=["telegram", "github"],
        max_items=10,
    )

    result = DevReviewPipeline(agent, max_cycles=3).run(task)

    assert len(result.cycles) == 2
    assert result.stop_reason == "review_passed"
    assert result.final_review is not None
    assert result.final_review.status == "PASS"

    observed_types = {
        material.source_type
        for cycle in result.cycles
        for material in cycle.package.materials
    }
    assert observed_types == {"telegram", "github"}


def test_ac12_equal_payload_preserves_observations_and_counts_payload_reuse(tmp_path: Path):
    class DuplicatePayloadCollector:
        name = "dup"
        source_types = {"web"}

        def collect(self, task):
            yield Material(
                source_type="web",
                source_locator="https://a.example/item",
                title="A",
                raw_text="same bytes",
            )
            yield Material(
                source_type="web",
                source_locator="https://b.example/item",
                title="B",
                raw_text="same bytes",
            )

    store = MaterialStore(tmp_path / "store")
    package = OSINTAgent(store, [DuplicatePayloadCollector()]).run(
        ResearchTask(question="same", source_types=["web"])
    )

    assert len(package.materials) == 2
    assert package.payloads_reused == 1
    assert len(list(store.raw_dir.glob("*.txt"))) == 1
    assert len(list(store.iter_materials())) == 2


def test_ac13_file_only_material_gets_sha256_of_original_bytes(tmp_path: Path):
    source = tmp_path / "artifact.bin"
    payload = b"\x00original artifact\xff"
    source.write_bytes(payload)

    material = Material(
        source_type="file",
        source_locator="file://artifact.bin",
        title="artifact",
        local_path=str(source),
    )
    store = MaterialStore(tmp_path / "store")

    reused = store.save_material(material)

    assert reused is False
    assert material.content_hash == hashlib.sha256(payload).hexdigest()
    assert material.local_path == str(source)


def test_ac13_missing_file_reference_fails_explicitly(tmp_path: Path):
    material = Material(
        source_type="file",
        source_locator="file://missing.bin",
        title="missing",
        local_path=str(tmp_path / "missing.bin"),
    )

    with pytest.raises(FileNotFoundError):
        MaterialStore(tmp_path / "store").save_material(material)
