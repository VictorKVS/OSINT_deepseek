from __future__ import annotations

from .models import CaseIntake, CoverageAssessment, FactoryPlan, IdentityDecision, JobResult


class MarkdownReportBuilder:
    def build(
        self,
        intake: CaseIntake,
        identity: IdentityDecision,
        plan: FactoryPlan,
        results: list[JobResult],
        coverage: CoverageAssessment,
    ) -> str:
        lines = [
            f"# Справка по фабричной проверке {intake.case_id}",
            "",
            f"- Профиль: `{intake.profile_id.value}`",
            f"- Глубина: `{intake.depth.value}`",
            f"- Статус Identity Lock: `{identity.status.value}`",
            f"- Итог покрытия: `{coverage.status.value}`",
            "",
            "## Объект и цель",
            "",
            f"**Объект:** {intake.subject.original_value}",
            f"**Цель:** {intake.purpose}",
            f"**Контекст решения:** {intake.decision_context}",
            "",
            "## Результаты источников",
            "",
            "| Поток | Источник/семейство | Статус | Наблюдений | Ограничение |",
            "|---|---|---:|---:|---|",
        ]
        jobs = {job.job_id: job for job in plan.jobs}
        for item in results:
            job = jobs[item.job_id]
            limitation = item.scoped_no_hit_note or "; ".join(item.limitations) or "—"
            lines.append(
                f"| {job.stream.value} | {item.source_family} | {item.state.value} | "
                f"{len(item.observations)} | {limitation} |"
            )
        lines += [
            "",
            "## Покрытие и блокирующие обстоятельства",
            "",
            f"- Обязательных заданий: {coverage.mandatory_total}",
            f"- Выполнено/зафиксировано: {coverage.attempted_total}",
            f"- FOUND: {coverage.found_total}",
            f"- NO_HIT: {coverage.no_hit_total}",
            f"- BLOCKED: {coverage.blocked_total}",
            f"- CONFLICT: {coverage.conflict_total}",
            f"- ERROR: {coverage.error_total}",
        ]
        if coverage.blocking_reasons:
            lines.append("- Блокирующие причины:")
            lines.extend(f"  - {item}" for item in coverage.blocking_reasons)
        else:
            lines.append("- Блокирующих причин на уровне технического покрытия не выявлено.")
        lines += [
            "",
            "## Обязательные оговорки",
            "",
            "- Результат инструмента является наблюдением или утверждением источника, а не установленным фактом.",
            "- `NO_HIT` не доказывает отсутствия факта.",
            "- Совпадение имени, адреса, домена или аккаунта само по себе не доказывает общий контроль или принадлежность.",
            "- Итоговое кадровое, договорное, санкционное или иное управленческое решение принимает уполномоченный человек.",
            "",
            "## Лист главного аналитика",
            "",
            "- [ ] Проверена идентификация объекта.",
            "- [ ] Проверены первичные источники существенных утверждений.",
            "- [ ] Разделены FACT / SOURCE_CLAIM / INFERENCE / HYPOTHESIS.",
            "- [ ] Проверены противоречия и альтернативные объяснения.",
            "- [ ] Проведена минимизация персональных данных.",
            "- [ ] Принято и подписано решение.",
            "",
        ]
        return "\n".join(lines)
