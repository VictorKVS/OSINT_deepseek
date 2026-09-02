from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapters import AdapterRegistry, SyntheticSourceAdapter
from .factory import DueDiligenceFactory
from .models import CaseIntake, Depth, JobState, ProfileId, SubjectSeed, Sufficiency
from .profiles import ProfileRegistry
from .runner import ParallelFactoryRunner


def build_demo_intake(profile_id: ProfileId) -> CaseIntake:
    if profile_id in {ProfileId.RU_ORG, ProfileId.INTL_ORG}:
        subject = SubjectSeed(
            original_value="Синтетическая организация Альфа",
            official_name="Синтетическая организация Альфа",
            jurisdiction="RU" if profile_id == ProfileId.RU_ORG else "GB",
            registration_or_tax_id="SYN-ORG-0001",
            incorporation_date="2026-01-01",
            official_domain="example.invalid",
            decisive_identifier_present=True,
        )
    else:
        subject = SubjectSeed(
            original_value="Иван Синтетический",
            full_name_original="Иван Синтетический",
            jurisdiction="RU" if profile_id == ProfileId.RU_PERSON else "GB",
            birth_date_or_year="1980",
            role_or_employer="Синтетическая организация Альфа",
            distinguishing_context="Synthetic fixture only",
            decisive_identifier_present=True,
        )
    return CaseIntake(
        case_id=f"CASE-DEMO-{profile_id.value}",
        profile_id=profile_id,
        purpose="Проверить повторяемость фабричного OSINT-контура на синтетических данных.",
        decision_context="Учебная проверка без принятия решения о реальном лице или организации.",
        requested_by="DEMO",
        owner_analyst="Главный аналитик",
        legal_basis_or_usage_note="Полностью синтетический fixture; реальные персональные данные не используются.",
        access_class="PUBLIC",
        retention_rule="May be retained as a regression fixture.",
        subject=subject,
        depth=Depth.STANDARD,
        required_sufficiency=Sufficiency.GOOD,
        allowed_jurisdictions=[subject.jurisdiction or "SYNTHETIC"],
        country_pack_id="GENERIC_INTL" if profile_id in {ProfileId.INTL_ORG, ProfileId.INTL_PERSON} else None,
    )


def demo(args: argparse.Namespace) -> int:
    profile_id = ProfileId(args.profile)
    intake = build_demo_intake(profile_id)
    profile = ProfileRegistry().get(profile_id)
    registry = AdapterRegistry()
    index = 0
    for families in profile.streams.values():
        for family in families:
            outcome = JobState.FOUND if index % 3 == 0 else JobState.NO_HIT
            values = (f"synthetic:{family}:candidate",) if outcome == JobState.FOUND else ()
            registry.register(SyntheticSourceAdapter(family, outcome, values, delay_ms=15))
            index += 1
    runner = ParallelFactoryRunner(registry, max_workers=args.workers)
    execution = DueDiligenceFactory(runner, store_root=args.root).execute(intake)
    summary = {
        "case_id": intake.case_id,
        "profile": profile_id.value,
        "jobs": len(execution.plan.jobs),
        "found": execution.coverage.found_total,
        "no_hit": execution.coverage.no_hit_total,
        "blocked": execution.coverage.blocked_total,
        "coverage_status": execution.coverage.status.value,
        "journal_valid": execution.journal_valid,
        "output": str(Path(args.root) / "cases" / intake.case_id),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if execution.journal_valid else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="osint-factory")
    sub = parser.add_subparsers(dest="command", required=True)
    demo_parser = sub.add_parser("demo", help="run an offline synthetic due-diligence factory case")
    demo_parser.add_argument("--profile", choices=[item.value for item in ProfileId], default="RU_ORG")
    demo_parser.add_argument("--root", default="runtime/osint-factory-demo")
    demo_parser.add_argument("--workers", type=int, default=5)
    demo_parser.set_defaults(func=demo)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
