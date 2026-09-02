from __future__ import annotations

import json
from pathlib import Path

import pytest

from osint_factory.adapters import AdapterRegistry, SyntheticSourceAdapter
from osint_factory.coverage import CoverageAssessor
from osint_factory.factory import DueDiligenceFactory
from osint_factory.identity import IdentityLocker
from osint_factory.journal import HashChainJournal
from osint_factory.models import (
    CaseIntake,
    CoverageStatus,
    Depth,
    IdentityStatus,
    JobState,
    ProfileId,
    SubjectSeed,
    Sufficiency,
)
from osint_factory.planner import FactoryPlanner
from osint_factory.profiles import CountryPackRegistry, ProfileRegistry
from osint_factory.runner import ParallelFactoryRunner


def org_intake(profile_id: ProfileId = ProfileId.RU_ORG, *, depth: Depth = Depth.STANDARD) -> CaseIntake:
    intl = profile_id == ProfileId.INTL_ORG
    return CaseIntake(
        case_id=f"CASE-{profile_id.value}-0001",
        profile_id=profile_id,
        purpose="Проверка синтетической организации перед тестовым договорным решением.",
        decision_context="Синтетический regression fixture, решение по реальной организации не принимается.",
        requested_by="TEST",
        owner_analyst="MAIN_ANALYST",
        legal_basis_or_usage_note="Synthetic public fixture used only for regression testing.",
        access_class="PUBLIC",
        retention_rule="Retain as regression fixture.",
        subject=SubjectSeed(
            original_value="Synthetic Alpha LLC",
            official_name="Synthetic Alpha LLC",
            jurisdiction="GB" if intl else "RU",
            registration_or_tax_id="SYN-001",
            decisive_identifier_present=True,
        ),
        depth=depth,
        required_sufficiency=Sufficiency.GOOD,
        allowed_jurisdictions=["GB" if intl else "RU"],
        country_pack_id="UK" if intl else None,
    )


def person_intake(profile_id: ProfileId = ProfileId.RU_PERSON, *, candidate_count: int = 1) -> CaseIntake:
    intl = profile_id == ProfileId.INTL_PERSON
    return CaseIntake(
        case_id=f"CASE-{profile_id.value}-0001",
        profile_id=profile_id,
        purpose="Проверка синтетического лица перед тестовым деловым решением.",
        decision_context="Синтетический regression fixture, решение по реальному лицу не принимается.",
        requested_by="TEST",
        owner_analyst="MAIN_ANALYST",
        legal_basis_or_usage_note="Synthetic public fixture used only for regression testing.",
        access_class="PUBLIC",
        retention_rule="Retain as regression fixture.",
        subject=SubjectSeed(
            original_value="Synthetic Person",
            full_name_original="Synthetic Person",
            jurisdiction="GB" if intl else "RU",
            birth_date_or_year="1980",
            role_or_employer="Synthetic Alpha LLC",
            distinguishing_context="Synthetic fixture",
            candidate_count=candidate_count,
            decisive_identifier_present=candidate_count == 1,
        ),
        depth=Depth.STANDARD,
        required_sufficiency=Sufficiency.GOOD,
        allowed_jurisdictions=["GB" if intl else "RU"],
        country_pack_id="UK" if intl else None,
    )


def registry_for_plan(plan, *, found_every: int = 3, delay_ms: int = 0) -> AdapterRegistry:
    registry = AdapterRegistry()
    for index, job in enumerate(plan.jobs):
        outcome = JobState.FOUND if index % found_every == 0 else JobState.NO_HIT
        values = (f"synthetic:{job.source_family}",) if outcome == JobState.FOUND else ()
        registry.register(SyntheticSourceAdapter(job.source_family, outcome, values, delay_ms=delay_ms))
    return registry


def test_four_profiles_exist_and_cover_five_streams() -> None:
    registry = ProfileRegistry()
    assert {item.profile_id for item in registry.all()} == set(ProfileId)
    for profile in registry.all():
        assert set(profile.streams) == set(__import__("osint_factory.models", fromlist=["Stream"]).Stream)


def test_ru_organization_identity_lock_uses_registration_id() -> None:
    intake = org_intake()
    profile = ProfileRegistry().get(intake.profile_id)
    decision = IdentityLocker().lock(intake, profile)
    assert decision.status == IdentityStatus.LOCKED
    assert decision.entity_key and decision.entity_key.startswith("ENT-")
    assert decision.automatic_merge_performed is False


def test_person_with_one_name_and_no_distinguishers_is_held() -> None:
    intake = person_intake()
    intake.subject.birth_date_or_year = None
    intake.subject.role_or_employer = None
    intake.subject.distinguishing_context = None
    intake.subject.city_or_region = None
    profile = ProfileRegistry().get(intake.profile_id)
    decision = IdentityLocker().lock(intake, profile)
    assert decision.status == IdentityStatus.HOLD_MISSING_IDENTIFIERS
    assert "at_least_two_person_distinguishers" in decision.missing_identifiers


def test_multiple_person_candidates_without_decisive_identifier_are_held() -> None:
    intake = person_intake(candidate_count=3)
    profile = ProfileRegistry().get(intake.profile_id)
    decision = IdentityLocker().lock(intake, profile)
    assert decision.status == IdentityStatus.HOLD_CONFLICT
    assert decision.automatic_merge_performed is False


def test_international_profile_requires_country_pack() -> None:
    intake = org_intake(ProfileId.INTL_ORG)
    intake.country_pack_id = None
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    with pytest.raises(ValueError, match="country_pack_id"):
        FactoryPlanner().build(intake, profile, identity)


def test_country_pack_registry_contains_ru_generic_eu_uk_us() -> None:
    assert CountryPackRegistry().all_ids() == ["EU", "GENERIC_INTL", "RU", "UK", "US"]


def test_standard_plan_generates_all_five_streams_and_stable_ids() -> None:
    intake = org_intake()
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    planner = FactoryPlanner()
    plan_a = planner.build(intake, profile, identity)
    plan_b = planner.build(intake, profile, identity)
    assert {job.stream for job in plan_a.jobs} == set(profile.streams)
    assert [job.job_id for job in plan_a.jobs] == [job.job_id for job in plan_b.jobs]
    assert all(job.active_actions_allowed is False for job in plan_a.jobs)


def test_screening_still_represents_all_five_streams() -> None:
    intake = org_intake(depth=Depth.SCREENING)
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    plan = FactoryPlanner().build(intake, profile, identity)
    assert {job.stream.value for job in plan.jobs} == {
        "ENTITY_REGISTRY",
        "BUSINESS_FINANCIAL_OPERATIONS",
        "DIGITAL_FOOTPRINT",
        "LEGAL_SANCTIONS_ADVERSE",
        "RED_TEAM_SOURCE_QUALITY",
    }


def test_enhanced_plan_adds_source_families() -> None:
    intake = org_intake(depth=Depth.ENHANCED)
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    plan = FactoryPlanner().build(intake, profile, identity)
    families = {job.source_family for job in plan.jobs}
    assert set(profile.enhanced_source_families) <= families


def test_no_hit_requires_scoped_note() -> None:
    from osint_factory.models import JobResult

    with pytest.raises(ValueError, match="scoped_no_hit_note"):
        JobResult(
            case_id="CASE-1",
            job_id="JOB-1",
            source_family="SOURCE",
            state=JobState.NO_HIT,
        )


def test_parallel_runner_preserves_plan_order_and_isolates_missing_adapters() -> None:
    intake = org_intake()
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    plan = FactoryPlanner().build(intake, profile, identity)
    registry = AdapterRegistry()
    first = plan.jobs[0]
    registry.register(SyntheticSourceAdapter(first.source_family, JobState.FOUND, ("value",), delay_ms=5))
    run = ParallelFactoryRunner(registry, max_workers=5).run(intake, plan)
    assert [item.job_id for item in run.results] == [job.job_id for job in plan.jobs]
    assert run.results[0].state == JobState.FOUND
    assert all(item.state == JobState.BLOCKED for item in run.results[1:])


def test_coverage_ready_when_every_job_has_found_or_scoped_no_hit() -> None:
    intake = org_intake()
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    plan = FactoryPlanner().build(intake, profile, identity)
    registry = registry_for_plan(plan)
    results = ParallelFactoryRunner(registry, max_workers=5).run(intake, plan).results
    assessment = CoverageAssessor().assess(plan, results)
    assert assessment.status == CoverageStatus.READY_FOR_HUMAN_REVIEW
    assert assessment.ready_for_human_review is True
    assert assessment.no_hit_total > 0


def test_coverage_blocks_unconnected_mandatory_source() -> None:
    intake = org_intake()
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    plan = FactoryPlanner().build(intake, profile, identity)
    results = ParallelFactoryRunner(AdapterRegistry(), max_workers=5).run(intake, plan).results
    assessment = CoverageAssessor().assess(plan, results)
    assert assessment.ready_for_human_review is False
    assert assessment.blocked_total == len(plan.jobs)


def test_hash_chain_detects_tampering() -> None:
    journal = HashChainJournal("CASE-1")
    journal.append("CREATED", "TEST", {"a": 1})
    journal.append("PLANNED", "TEST", {"b": 2})
    assert journal.verify() == (True, "PASS")
    journal.entries[0].payload["a"] = 999
    valid, message = journal.verify()
    assert valid is False
    assert "event_hash mismatch" in message


def test_end_to_end_factory_persists_auditable_package(tmp_path: Path) -> None:
    intake = org_intake()
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    plan = FactoryPlanner().build(intake, profile, identity)
    registry = registry_for_plan(plan, delay_ms=1)
    factory = DueDiligenceFactory(
        ParallelFactoryRunner(registry, max_workers=5),
        store_root=tmp_path,
    )
    execution = factory.execute(intake)
    case_dir = tmp_path / "cases" / intake.case_id
    assert execution.journal_valid is True
    assert execution.coverage.ready_for_human_review is True
    assert (case_dir / "00_case_intake.json").is_file()
    assert (case_dir / "02_factory_plan.json").is_file()
    assert (case_dir / "05_report.md").is_file()
    assert (case_dir / "06_journal.jsonl").is_file()
    report = (case_dir / "05_report.md").read_text(encoding="utf-8")
    assert "NO_HIT" in report
    assert "не доказывает отсутствия факта" in report
    journal_lines = (case_dir / "06_journal.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(journal_lines) >= len(plan.jobs) + 4
    assert all(json.loads(line)["case_id"] == intake.case_id for line in journal_lines)


def test_full_person_international_execution(tmp_path: Path) -> None:
    intake = person_intake(ProfileId.INTL_PERSON)
    profile = ProfileRegistry().get(intake.profile_id)
    identity = IdentityLocker().lock(intake, profile)
    plan = FactoryPlanner().build(intake, profile, identity)
    registry = registry_for_plan(plan)
    execution = DueDiligenceFactory(
        ParallelFactoryRunner(registry, max_workers=5),
        store_root=tmp_path,
    ).execute(intake)
    assert execution.identity.status == IdentityStatus.LOCKED
    assert execution.plan.country_pack_id == "UK"
    assert execution.coverage.status == CoverageStatus.READY_FOR_HUMAN_REVIEW
