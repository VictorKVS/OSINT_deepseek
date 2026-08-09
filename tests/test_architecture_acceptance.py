from pathlib import Path

from father_osint.agent import OSINTAgent
from father_osint.analysis import SimpleAnalyst
from father_osint.collectors.dev import FixtureCollector
from father_osint.models import Material, ResearchTask
from father_osint.review_pipeline import DevReviewPipeline
from father_osint.socrates import SimpleSocrates
from father_osint.storage import MaterialStore


class GoodCollector:
    name = "good"
    source_types = {"web"}

    def collect(self, task):
        yield Material(
            source_type="web",
            source_locator="https://example.test/good",
            title="Good material",
            raw_text="useful payload",
        )


class FailingCollector:
    name = "broken"
    source_types = {"web"}

    def collect(self, task):
        raise RuntimeError("simulated collector failure")


def test_ac05_collector_failure_isolated_and_visible(tmp_path: Path):
    """AC-05: one collector failure must not erase already collected material."""
    store = MaterialStore(tmp_path / "store")
    agent = OSINTAgent(store, [GoodCollector(), FailingCollector()])
    task = ResearchTask(question="evidence", source_types=["web"], max_items=10)

    package = agent.run(task)

    assert len(package.materials) == 1
    assert package.materials[0].source_locator == "https://example.test/good"
    assert package.collection_errors
    assert any("broken" in error for error in package.collection_errors)


def test_at04_restart_preserves_two_source_observations_for_same_payload(tmp_path: Path):
    """AT-04: restart must not convert payload deduplication into provenance loss."""
    store_path = tmp_path / "store"

    class SourceA:
        name = "a"
        source_types = {"web"}

        def collect(self, task):
            yield Material(
                source_type="web",
                source_locator="https://source-a.test/item",
                title="A",
                raw_text="shared payload",
            )

    class SourceB:
        name = "b"
        source_types = {"web"}

        def collect(self, task):
            yield Material(
                source_type="web",
                source_locator="https://source-b.test/item",
                title="B",
                raw_text="shared payload",
            )

    task_a = ResearchTask(question="shared", source_types=["web"])
    package_a = OSINTAgent(MaterialStore(store_path), [SourceA()]).run(task_a)
    assert len(package_a.materials) == 1

    # Simulate process restart by constructing a new store instance.
    task_b = ResearchTask(question="shared", source_types=["web"])
    restarted_store = MaterialStore(store_path)
    package_b = OSINTAgent(restarted_store, [SourceB()]).run(task_b)

    assert len(package_b.materials) == 1
    observations = list(restarted_store.iter_materials())
    assert {item["source_locator"] for item in observations} == {
        "https://source-a.test/item",
        "https://source-b.test/item",
    }
    assert len(list(restarted_store.raw_dir.glob("*.txt"))) == 1


def test_full_dev_review_pipeline_passes_with_complete_fixture(tmp_path: Path):
    """AC-08/09: full DEV path is bounded and can reach Socrates PASS."""
    fixture = tmp_path / "telegram.json"
    fixture.write_text(
        '[{"source_locator":"https://t.me/test/1","title":"TDLib","raw_text":"TDLib signal"}]',
        encoding="utf-8",
    )

    agent = OSINTAgent(
        MaterialStore(tmp_path / "store"),
        [FixtureCollector("telegram_dev", "telegram", fixture)],
    )
    pipeline = DevReviewPipeline(
        osint_agent=agent,
        analyst=SimpleAnalyst(),
        socrates=SimpleSocrates(),
        max_cycles=3,
    )
    task = ResearchTask(question="TDLib", source_types=["telegram"], max_items=10)

    result = pipeline.run(task)

    assert len(result.cycles) == 1
    assert result.stop_reason == "review_passed"
    assert result.final_review is not None
    assert result.final_review.status == "PASS"


def test_full_dev_review_pipeline_is_hard_bounded(tmp_path: Path):
    """AC-08: unresolved research cannot create an infinite loop."""
    agent = OSINTAgent(MaterialStore(tmp_path / "store"), collectors=[])
    pipeline = DevReviewPipeline(agent, max_cycles=2)
    task = ResearchTask(question="Need GitHub data", source_types=["github"])

    result = pipeline.run(task)

    assert len(result.cycles) == 2
    assert result.stop_reason == "max_cycles_reached"
