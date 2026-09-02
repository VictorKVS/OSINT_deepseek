from __future__ import annotations

import json
from pathlib import Path

import pytest

from screening_factory.demo import build_demo
from screening_factory.journal import HashChainJournal
from screening_factory.models import (
    CheckStream,
    JurisdictionScope,
    Observation,
    ObservationClass,
    Outcome,
    RiskTier,
    ScreeningDepth,
    ScreeningRequest,
    Subject,
    SubjectKind,
)
from screening_factory.planner import ScreeningPlanner, ScreeningPolicyError
from screening_factory.profiles import PROFILES, checks_for_profile
from screening_factory.registry import (
    AdapterDescriptor,
    AdapterPayload,
    AdapterRegistry,
    CallbackAdapter,
    SyntheticAdapter,
)
from screening_factory.report import HtmlDashboardBuilder, MarkdownReportBuilder
from screening_factory.runner import ScreeningFactoryRunner
from screening_factory.scheduler import RecheckScheduler
from screening_factory.sources import SOURCE_BY_ID


def ru_legal_request(*, depth: ScreeningDepth = ScreeningDepth.STANDARD) -> ScreeningRequest:
    return ScreeningRequest(
        subject=Subject(
            kind=SubjectKind.LEGAL_ENTITY,
            display_name="ООО Тест",
            country_code="RU",
            identifiers={"inn": "7700000000", "ogrn": "1027700000000"},
            known_regions=["Москва"],
        ),
        purpose="Проверка контрагента перед заключением договора.",
        legal_basis_note="Внутренняя проверка контрагента по открытым данным.",
        jurisdiction_scope=JurisdictionScope.RUSSIA,
        depth=depth,
    )


def foreign_person_request() -> ScreeningRequest:
    return ScreeningRequest(
        subject=Subject(
            kind=SubjectKind.PERSON,
            display_name="Alex Example",
            country_code="GB",
            date_of_birth="1980-01-01",
            citizenships=["GB"],
        ),
        purpose="Проверка руководителя иностранного контрагента.",
        legal_basis_note="Проверка по публичным источникам в рамках договорной оценки риска.",
        jurisdiction_scope=JurisdictionScope.FOREIGN,
        depth=ScreeningDepth.STANDARD,
    )


def registry_for_plan(plan, *, delay: float = 0.0, default_outcome: Outcome = Outcome.NO_HIT_IN_SCOPE):
    registry = AdapterRegistry()
    for item in plan.work_items:
        registry.register(
            SyntheticAdapter(
                f"SYN-{item.check_code}",
                (item.check_code,),
                outcome=default_outcome,
                delay_seconds=delay,
            )
        )
    return registry


def test_four_profiles_cover_all_five_streams():
    assert set(PROFILES) == {
        "RU_LEGAL_ENTITY", "FOREIGN_LEGAL_ENTITY", "RU_PERSON", "FOREIGN_PERSON"
    }
    for profile in PROFILES.values():
        streams = {check.stream for check in checks_for_profile(profile)}
        assert set(CheckStream).issubset(streams)


def test_ru_legal_profile_contains_core_due_diligence_checks():
    codes = set(PROFILES["RU_LEGAL_ENTITY"].check_codes)
    assert {"RU-LE-001", "RU-LE-006", "RU-LE-007", "RU-LE-009", "RU-LE-011", "SAN-001", "RED-002"}.issubset(codes)


def test_foreign_person_profile_contains_pep_transliteration_and_digital_checks():
    codes = set(PROFILES["FOREIGN_PERSON"].check_codes)
    assert {"IDN-002", "FOR-PER-001", "FOR-PER-003", "FOR-PER-005", "ADV-001", "RED-001"}.issubset(codes)


def test_scope_country_mismatch_is_rejected():
    with pytest.raises(ValueError):
        ScreeningRequest(
            subject=Subject(SubjectKind.LEGAL_ENTITY, "Wrong", "GB"),
            purpose="Достаточно длинная цель проверки.",
            legal_basis_note="Достаточно длинное основание проверки.",
            jurisdiction_scope=JurisdictionScope.RUSSIA,
        )


def test_active_actions_are_rejected_by_factory_policy():
    request = ru_legal_request()
    request.active_actions_allowed = True
    with pytest.raises(ScreeningPolicyError):
        ScreeningPlanner().build(request)


def test_person_without_identity_anchor_is_explicitly_blocked():
    request = ScreeningRequest(
        subject=Subject(SubjectKind.PERSON, "Иван Иванов", "RU"),
        purpose="Проверка кандидата для роли с повышенным риском.",
        legal_basis_note="Согласованный внутренний процесс проверки по открытым данным.",
        jurisdiction_scope=JurisdictionScope.RUSSIA,
        depth=ScreeningDepth.BASIC,
    )
    plan = ScreeningPlanner().build(request)
    item = next(item for item in plan.work_items if item.check_code == "RU-PER-001")
    assert item.state.value == "BLOCKED"
    assert plan.missing_identity_anchors


def test_work_item_ids_are_deterministic_for_same_request():
    request = ru_legal_request()
    planner = ScreeningPlanner()
    first = planner.build(request)
    second = planner.build(request)
    assert [(i.check_code, i.work_item_id) for i in first.work_items] == [
        (i.check_code, i.work_item_id) for i in second.work_items
    ]


def test_missing_adapter_is_visible_not_silently_skipped():
    request = ru_legal_request(depth=ScreeningDepth.BASIC)
    plan = ScreeningPlanner().build(request)
    run = ScreeningFactoryRunner(AdapterRegistry()).run(request, plan)
    assert any(result.outcome == Outcome.BLOCKED_NO_ADAPTER for result in run.results)
    assert run.summary.report_ready is False


def test_parallel_factory_reaches_multiple_workers():
    request = ru_legal_request(depth=ScreeningDepth.STANDARD)
    plan = ScreeningPlanner().build(request)
    registry = registry_for_plan(plan, delay=0.03)
    run = ScreeningFactoryRunner(registry, max_workers=5).run(request, plan)
    assert run.summary.peak_parallelism >= 2
    assert len(run.results) == len(plan.work_items)


def test_multiple_adapter_conflict_is_preserved():
    request = ru_legal_request(depth=ScreeningDepth.BASIC)
    plan = ScreeningPlanner().build(request)
    registry2 = AdapterRegistry()
    for item in plan.work_items:
        if item.check_code != "SAN-001":
            registry2.register(SyntheticAdapter(f"SYN-{item.check_code}", (item.check_code,), outcome=Outcome.NO_HIT_IN_SCOPE))
    registry2.register(SyntheticAdapter("SAN-FOUND", ("SAN-001",), outcome=Outcome.FOUND))

    def conflict_callback(request, item):
        return AdapterPayload(
            outcome=Outcome.CONFLICT,
            source_attempts=[{"source_id": "SRC-SAN-2", "status": "CONFLICT", "scope": "fixture"}],
            conflicts=["Alias matches, but date of birth contradicts the candidate"],
            human_review_required=True,
        )

    registry2.register(CallbackAdapter(
        AdapterDescriptor(
            "SAN-CONFLICT", "Synthetic sanctions conflict", ("SAN-001",), "SYNTHETIC",
            "FIXTURE_ONLY", ("SRC-SAN-2",),
        ),
        conflict_callback,
    ))
    run = ScreeningFactoryRunner(registry2).run(request, plan)
    sanctions = next(result for result in run.results if result.check_code == "SAN-001")
    assert sanctions.outcome == Outcome.CONFLICT
    assert sanctions.conflicts
    assert sanctions.human_review_required


def test_no_hit_semantics_are_written_to_report():
    request = ru_legal_request(depth=ScreeningDepth.BASIC)
    plan = ScreeningPlanner().build(request)
    run = ScreeningFactoryRunner(registry_for_plan(plan)).run(request, plan)
    report = MarkdownReportBuilder().build(run)
    assert "NO_HIT_IN_SCOPE" in report
    assert "не доказательство отсутствия" in report


def test_dashboard_contains_status_checkboxes():
    request = ru_legal_request(depth=ScreeningDepth.BASIC)
    plan = ScreeningPlanner().build(request)
    run = ScreeningFactoryRunner(registry_for_plan(plan)).run(request, plan)
    html = HtmlDashboardBuilder().build(run)
    assert "Screening Factory M3" in html
    assert "Адаптер" in html
    assert "Evidence" in html
    assert "Review" in html


def test_hash_chain_detects_tampering(tmp_path: Path):
    journal = HashChainJournal(tmp_path / "journal.jsonl")
    journal.append("ONE", case_id="CASE-1", request_id="REQ-1", actor="TEST", payload={"value": 1})
    journal.append("TWO", case_id="CASE-1", request_id="REQ-1", actor="TEST", payload={"value": 2})
    ok, errors = journal.verify()
    assert ok and not errors

    lines = (tmp_path / "journal.jsonl").read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0])
    first["payload"]["value"] = 999
    lines[0] = json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    (tmp_path / "journal.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    ok, errors = journal.verify()
    assert not ok
    assert errors


def test_recheck_scheduler_shortens_blocking_gap_interval():
    scheduler = RecheckScheduler()
    normal = scheduler.next_due("2026-09-03T00:00:00+00:00", RiskTier.HIGH)
    blocked = scheduler.next_due(
        "2026-09-03T00:00:00+00:00", RiskTier.HIGH, unresolved_blocking_gap=True
    )
    assert normal.interval_days == 90
    assert blocked.interval_days == 14


def test_active_adapter_is_blocked_even_if_registered():
    request = ru_legal_request(depth=ScreeningDepth.BASIC)
    plan = ScreeningPlanner().build(request)
    blocked_registry = AdapterRegistry()
    for item in plan.work_items:
        if item.check_code == "SAN-001":
            blocked_registry.register(CallbackAdapter(
                AdapterDescriptor(
                    "ACTIVE-SAN", "Unsafe active adapter", ("SAN-001",), "KALI", "ACTIVE_AUTHORIZED", ("SRC-X",)
                ),
                lambda request, item: AdapterPayload(outcome=Outcome.NO_HIT_IN_SCOPE),
            ))
        else:
            blocked_registry.register(SyntheticAdapter(f"SYN-{item.check_code}", (item.check_code,), outcome=Outcome.NO_HIT_IN_SCOPE))
    run = ScreeningFactoryRunner(blocked_registry).run(request, plan)
    sanctions = next(result for result in run.results if result.check_code == "SAN-001")
    assert sanctions.outcome == Outcome.BLOCKED_POLICY


def test_official_source_registry_contains_primary_core_sources():
    for source_id in ["RU-FNS-EGRUL", "RU-FEDRESURS", "UN-CONSOLIDATED", "US-OFAC", "UK-SANCTIONS", "WB-DEBARRED"]:
        assert source_id in SOURCE_BY_ID
        assert SOURCE_BY_ID[source_id].canonical_url.startswith("https://")


def test_offline_demo_produces_complete_artifact_set(tmp_path: Path):
    summary = build_demo(tmp_path / "demo")
    assert summary["journal_verified"] is True
    assert summary["work_items"] > 0
    for name in ["request.json", "plan.json", "run.json", "report.md", "dashboard.html", "journal.jsonl"]:
        assert (tmp_path / "demo" / name).is_file()
