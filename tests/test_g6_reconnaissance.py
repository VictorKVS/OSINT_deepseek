from father_osint.models import Material, MaterialPackage
from father_osint.protocol import ResearchRequest
from father_osint.search_planning import DeterministicTelegramSearchPlanner
from father_osint.reconnaissance import DeterministicTelegramReconnaissance


def _plan():
    req = ResearchRequest(objective="Map Telegram source landscape", research_questions=["What sources and terms recur?"], required_sufficiency="GOOD")
    return DeterministicTelegramSearchPlanner().plan(req).plan


def test_recon_builds_landscape_and_refined_plan():
    plan = _plan()
    materials = [
        Material(source_type="telegram", source_locator="telegram://1/1", title="A", raw_text="Alpha project update https://example.org/a", metadata={"chat_id":"1","forward_from":"OriginX"}),
        Material(source_type="telegram", source_locator="telegram://2/2", title="B", raw_text="Alpha beta project https://example.net/b", metadata={"chat_id":"2"}),
    ]
    package = MaterialPackage(task_id="task", materials=materials)
    result = DeterministicTelegramReconnaissance().run(plan, package)
    assert len(result.report.source_landscape) == 2
    assert result.report.domains
    assert result.report.forward_candidates[0]["origin"] == "OriginX"
    assert result.refined_plan.version == plan.version + 1
    assert result.refined_plan.search_plan_id == plan.search_plan_id
    assert result.decision_record.role_id == "OSINT_EXPERT"
    assert result.report.report_id in result.decision_record.output_refs


def test_recon_empty_sample_stops_explicitly():
    plan = _plan()
    package = MaterialPackage(task_id="task", materials=[])
    result = DeterministicTelegramReconnaissance().run(plan, package)
    assert result.report.stop_recommended is True
    assert result.report.marginal_value == "NONE"
    assert "empty" in result.report.gaps[0].lower()


def test_recon_low_marginal_value_when_no_novel_terms():
    plan = _plan()
    material = Material(source_type="telegram", source_locator="telegram://1/1", title="A", raw_text="alpha beta gamma delta", metadata={"chat_id":"1"})
    package = MaterialPackage(task_id="task", materials=[material])
    result = DeterministicTelegramReconnaissance().run(plan, package, previous_terms=["alpha","beta","gamma","delta"])
    assert result.report.marginal_value == "LOW"
    assert result.report.stop_recommended is True


def test_recon_is_bounded():
    plan = _plan()
    materials = [Material(source_type="telegram", source_locator=f"telegram://1/{i}", title="A", raw_text=f"term{i} evidence", metadata={"chat_id":"1"}) for i in range(10)]
    package = MaterialPackage(task_id="task", materials=materials)
    result = DeterministicTelegramReconnaissance().run(plan, package, sample_limit=3)
    assert len(result.report.sampled_material_refs) == 3
