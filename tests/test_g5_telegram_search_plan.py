from father_osint.protocol import ResearchRequest
from father_osint.search_planning import DeterministicTelegramSearchPlanner


def request(level="GOOD"):
    return ResearchRequest(
        objective="Understand significant topics discussed in selected Telegram sources",
        research_questions=[
            "Which topics are repeatedly discussed?",
            "Which claims are repeated across sources?",
        ],
        required_sufficiency=level,
        time_window={"from": "2026-08-01", "to": "2026-08-13"},
        acceptance_criteria=[
            "Report source coverage",
            "Separate repost propagation from independent corroboration",
        ],
    )


def test_planner_builds_auditable_telegram_plan():
    planned = DeterministicTelegramSearchPlanner().plan(request())

    plan = planned.plan
    assert plan.source_classes == ["telegram"]
    assert plan.expected_sufficiency == "GOOD"
    assert plan.knowledge_refs
    assert plan.algorithm_version == "telegram-search-plan-v1"
    assert "counter_evidence_keyword_search" in plan.methods
    assert any("repost" in item.lower() for item in plan.verification_approach)
    assert any("coverage" in item.lower() for item in plan.expected_coverage)


def test_planner_records_decision_lineage():
    req = request()
    planned = DeterministicTelegramSearchPlanner().plan(req)

    record = planned.decision_record
    assert record.role_id == "OSINT_EXPERT"
    assert req.request_id in record.input_refs
    assert planned.plan.search_plan_id in record.output_refs
    assert record.knowledge_refs == planned.plan.knowledge_refs
    assert record.algorithm_version == planned.plan.algorithm_version


def test_good_or_desirable_plan_warns_telegram_may_be_insufficient_alone():
    for level in ("GOOD", "DESIRABLE"):
        plan = DeterministicTelegramSearchPlanner().plan(request(level)).plan
        assert any("additional source classes" in item for item in plan.limitations)


def test_plan_rejects_post_count_as_sufficiency():
    plan = DeterministicTelegramSearchPlanner().plan(request()).plan
    assert any("post count" in item.lower() for item in plan.alternatives_considered)


def test_plan_preserves_analyst_question_as_information_gap():
    req = request("MINIMUM")
    plan = DeterministicTelegramSearchPlanner().plan(req).plan

    for question in req.research_questions:
        assert any(question in gap for gap in plan.information_gaps)
