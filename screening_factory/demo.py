from __future__ import annotations

import json
from pathlib import Path

from .journal import HashChainJournal
from .models import (
    JurisdictionScope,
    Outcome,
    RiskTier,
    ScreeningDepth,
    ScreeningRequest,
    Subject,
    SubjectKind,
)
from .planner import ScreeningPlanner
from .registry import AdapterRegistry, SyntheticAdapter
from .report import HtmlDashboardBuilder, MarkdownReportBuilder
from .runner import ScreeningFactoryRunner


def build_demo(output_dir: str | Path) -> dict[str, str | int | bool]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    subject = Subject(
        kind=SubjectKind.LEGAL_ENTITY,
        display_name="ООО «Синтетический Контрагент»",
        country_code="RU",
        identifiers={"inn": "7700000000", "ogrn": "1027700000000"},
        aliases=["Synthetic Counterparty LLC"],
        known_regions=["Москва"],
    )
    request = ScreeningRequest(
        subject=subject,
        purpose="Учебная проверка производственного контура без реальных внешних данных.",
        legal_basis_note="Полностью синтетический fixture; предназначен только для тестирования архитектуры.",
        jurisdiction_scope=JurisdictionScope.RUSSIA,
        depth=ScreeningDepth.STANDARD,
        risk_tier=RiskTier.MEDIUM,
        requested_by="FIXTURE_BUILDER",
    )
    plan = ScreeningPlanner().build(request)

    registry = AdapterRegistry()
    for index, item in enumerate(plan.work_items, start=1):
        outcome = Outcome.FOUND if index % 3 == 1 else Outcome.NO_HIT_IN_SCOPE
        registry.register(
            SyntheticAdapter(
                f"SYN-{item.check_code}",
                (item.check_code,),
                outcome=outcome,
                delay_seconds=0.01,
                observation_prefix="Синтетический контрольный результат",
            )
        )

    run = ScreeningFactoryRunner(registry, max_workers=5).run(request, plan)

    (output / "request.json").write_text(
        json.dumps(request.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output / "plan.json").write_text(
        json.dumps(plan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output / "run.json").write_text(
        json.dumps(run.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    MarkdownReportBuilder().write(run, output / "report.md")
    HtmlDashboardBuilder().write(run, output / "dashboard.html")

    journal = HashChainJournal(output / "journal.jsonl")
    journal.append(
        "SCREENING_REQUEST_CREATED",
        case_id=request.case_id,
        request_id=request.request_id,
        actor=request.requested_by,
        payload={"subject_id": subject.subject_id, "profile_id": plan.profile_id},
    )
    journal.append(
        "SCREENING_PLAN_CREATED",
        case_id=request.case_id,
        request_id=request.request_id,
        actor="SCREENING_PLANNER",
        payload={"plan_id": plan.plan_id, "work_items": len(plan.work_items)},
    )
    journal.append(
        "FACTORY_RUN_COMPLETED",
        case_id=request.case_id,
        request_id=request.request_id,
        actor="SCREENING_FACTORY",
        payload={"run_id": run.run_id, "summary": run.summary.to_dict()},
    )
    verified, errors = journal.verify()
    return {
        "case_id": request.case_id,
        "request_id": request.request_id,
        "plan_id": plan.plan_id,
        "run_id": run.run_id,
        "work_items": len(plan.work_items),
        "peak_parallelism": run.summary.peak_parallelism,
        "duration_ms": run.summary.duration_ms,
        "report_ready": run.summary.report_ready,
        "journal_verified": verified,
        "journal_errors": len(errors),
        "output_dir": str(output.resolve()),
    }
