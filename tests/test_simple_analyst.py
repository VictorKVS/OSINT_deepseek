from father_osint.analysis import SimpleAnalyst
from father_osint.models import Material, MaterialPackage, ResearchTask


def test_simple_analyst_summarizes_materials():
    task = ResearchTask(
        question="Compare Telegram transports",
        topics=["TDLib", "Teleproto"],
        source_types=["telegram", "github"],
    )
    package = MaterialPackage(
        task_id=task.task_id,
        materials=[
            Material(
                source_type="telegram",
                source_locator="https://t.me/example/1",
                title="Telegram signal",
                raw_text="TDLib is being discussed as a transport candidate",
                metadata={"candidate": "TDLib"},
            ),
            Material(
                source_type="github",
                source_locator="https://github.com/example/repo",
                title="Repository",
                raw_text="Teleproto repository is active",
                metadata={"candidate": "Teleproto"},
            ),
        ],
    )

    analysis = SimpleAnalyst().analyze(task, package)

    assert "Collected 2 material" in analysis.summary
    assert analysis.candidates == ["TDLib", "Teleproto"]
    assert analysis.gaps == []
    assert analysis.follow_up_task is None


def test_simple_analyst_requests_follow_up_for_missing_source():
    task = ResearchTask(
        question="Find evidence",
        source_types=["telegram", "github"],
    )
    package = MaterialPackage(
        task_id=task.task_id,
        materials=[
            Material(
                source_type="telegram",
                source_locator="https://t.me/example/1",
                title="Telegram signal",
                raw_text="signal",
            )
        ],
    )

    analysis = SimpleAnalyst().analyze(task, package)

    assert analysis.gaps
    assert analysis.follow_up_task is not None
    assert analysis.follow_up_task.source_types == ["github"]
