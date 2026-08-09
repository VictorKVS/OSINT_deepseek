from pathlib import Path

from father_osint.agent import OSINTAgent
from father_osint.collectors.dev import FixtureCollector
from father_osint.models import ResearchTask
from father_osint.review_pipeline import DevReviewPipeline
from father_osint.storage import MaterialStore


def test_pipeline_stops_when_review_passes(tmp_path: Path):
    fixture = tmp_path / "telegram.json"
    fixture.write_text(
        '[{"source_locator":"https://t.me/test/1","title":"Test","raw_text":"TDLib signal"}]',
        encoding="utf-8",
    )
    agent = OSINTAgent(
        MaterialStore(tmp_path / "store"),
        collectors=[FixtureCollector("telegram_dev", "telegram", fixture)],
    )
    task = ResearchTask(question="TDLib", source_types=["telegram"], max_items=10)

    result = DevReviewPipeline(agent, max_cycles=3).run(task)

    assert len(result.cycles) == 1
    assert result.stop_reason == "review_passed"
    assert result.final_review is not None
    assert result.final_review.status == "PASS"
    assert result.cycles[-1].analysis.gaps == []


def test_pipeline_is_bounded_when_follow_up_never_resolves(tmp_path: Path):
    agent = OSINTAgent(MaterialStore(tmp_path / "store"), collectors=[])
    task = ResearchTask(question="Need GitHub data", source_types=["github"], max_items=10)

    result = DevReviewPipeline(agent, max_cycles=2).run(task)

    assert len(result.cycles) == 2
    assert result.stop_reason == "max_cycles_reached"
    assert result.final_review is not None
    assert result.final_review.follow_up_task is not None
