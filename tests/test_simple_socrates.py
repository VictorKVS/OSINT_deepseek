from father_osint.analysis import SimpleAnalyst
from father_osint.models import Material, MaterialPackage, ResearchTask
from father_osint.socrates import SimpleSocrates


def test_socrates_passes_sourced_analysis_without_gaps():
    task = ResearchTask(question="Telegram", source_types=["telegram"])
    package = MaterialPackage(
        task_id=task.task_id,
        materials=[
            Material(
                source_type="telegram",
                source_locator="https://t.me/test/1",
                title="test",
                raw_text="signal",
            )
        ],
    )
    analysis = SimpleAnalyst().analyze(task, package)

    review = SimpleSocrates().review(task, package, analysis)

    assert review.status == "PASS"
    assert review.follow_up_task is None


def test_socrates_requests_missing_source_type():
    task = ResearchTask(question="Telegram", source_types=["telegram", "github"])
    package = MaterialPackage(
        task_id=task.task_id,
        materials=[
            Material(
                source_type="telegram",
                source_locator="https://t.me/test/1",
                title="test",
                raw_text="signal",
            )
        ],
    )
    analysis = SimpleAnalyst().analyze(task, package)

    review = SimpleSocrates().review(task, package, analysis)

    assert review.status == "RESEARCH_MORE"
    assert review.follow_up_task is not None
    assert review.follow_up_task.source_types == ["github"]
