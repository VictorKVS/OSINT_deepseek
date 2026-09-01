from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import sha256_text, utc_now_iso
from .policy import authorize_public_export, strictest_access_class
from .store import WorkbenchStore


@dataclass(slots=True)
class ReportBuildResult:
    case_id: str
    path: str
    sha256: str
    public_export: bool
    redacted: bool
    finding_count: int
    source_count: int


class OfficialReportComposer:
    """Generate an evidence-linked service report from reviewed structured objects."""

    version = "official-report-composer/0.1.0"

    def __init__(self, store: WorkbenchStore) -> None:
        self.store = store

    def build(
        self,
        case_id: str,
        *,
        public_export: bool = False,
        redacted: bool = True,
        report_name: str = "main_official_report.md",
    ) -> ReportBuildResult:
        case = self.store.get_case(case_id)
        findings = self.store.list_objects(case_id, "finding")
        sources = self.store.list_objects(case_id, "source")
        captures = self.store.list_objects(case_id, "capture")
        claims = self.store.list_objects(case_id, "claim")
        entities = self.store.list_objects(case_id, "entity")
        relations = self.store.list_objects(case_id, "relation")
        gaps = self.store.list_objects(case_id, "research_gap")
        coverages = self.store.list_objects(case_id, "coverage")
        journal_check = self.store.verify_journal(case_id)

        if any(not item.get("human_approved") for item in findings):
            raise PermissionError("report contains a finding without human approval")

        capture_source_ids = {item["source_id"] for item in captures if item.get("integrity_verified")}
        evidence_trace_complete = all(
            item["source_ids"] and item["claim_ids"] and set(item["source_ids"]) <= capture_source_ids
            for item in findings
        ) if findings else False
        contains_personal_data = any(item["access_class"] == "PUBLIC_WITH_PERSONAL_DATA" for item in entities)
        report_access = strictest_access_class(case["access_class"], *(item["access_class"] for item in [*findings, *sources, *entities]))
        republication = "ALLOWED"
        if any(item["republication_status"] == "PROHIBITED" for item in sources):
            republication = "PROHIBITED"
        elif any(item["republication_status"] == "UNKNOWN" for item in sources):
            republication = "UNKNOWN"
        elif any(item["republication_status"] in {"METADATA_ONLY", "REDACTED_ONLY"} for item in sources):
            republication = "REDACTED_ONLY"

        if public_export:
            decision = authorize_public_export(
                access_class=report_access,
                republication_status=republication,
                contains_personal_data=contains_personal_data,
                redacted=redacted,
                evidence_trace_complete=evidence_trace_complete,
                human_reviewed=bool(findings) and all(item["human_approved"] for item in findings),
            )
            if decision.decision != "ALLOW":
                raise PermissionError(f"public export denied: {', '.join(decision.reason_codes)}")

        source_by_id = {item["source_id"]: item for item in sources}
        claim_by_id = {item["claim_id"]: item for item in claims}
        coverage_by_finding = {item["finding_id"]: item for item in coverages}
        entity_by_id = {item["entity_id"]: item for item in entities}

        lines: list[str] = [
            "# СЛУЖЕБНАЯ АНАЛИТИЧЕСКАЯ СПРАВКА",
            "",
            f"**Дело:** `{case_id}`  ",
            f"**Объект:** {case['title']}  ",
            f"**Цель:** {case['purpose']}  ",
            f"**Режим доступа:** `{report_access}`  ",
            f"**Исполнитель/владелец:** {case['owner_role']}  ",
            f"**Сформировано:** {utc_now_iso()}  ",
            f"**Версия генератора:** `{self.version}`",
            "",
            "## 1. Основание и границы",
            "",
            case["legal_basis_or_usage_note"],
            "",
            "Допустимый объём: " + "; ".join(case["scope"]["allowed"]) + ".",
            "Исключено: " + "; ".join(case["scope"]["excluded"]) + ".",
            "",
            "## 2. Резюме для принятия решения",
            "",
        ]

        if not findings:
            lines.append("Проверенных выводов, утверждённых главным аналитиком, пока нет. Материал не готов для управленческого решения.")
        else:
            for item in findings:
                prefix = {
                    "FACT": "Установлено",
                    "INFERENCE": "Имеются основания полагать",
                    "HYPOTHESIS": "Проверяется версия",
                    "RISK": "Выявлен фактор риска",
                    "DECISION": "Предлагаемое решение",
                }[item["classification"]]
                lines.append(f"- **{prefix}:** {item['statement']} (`{item['finding_id']}`, {item['evidence_grade']}).")

        lines.extend(["", "## 3. Установленные обстоятельства", ""])
        facts = [item for item in findings if item["classification"] == "FACT"]
        if not facts:
            lines.append("Установленных фактов, прошедших человеческое утверждение, нет.")
        for item in facts:
            lines.extend(self._render_finding(item, source_by_id, claim_by_id, coverage_by_finding))

        lines.extend(["", "## 4. Аналитические выводы, риски и версии", ""])
        analytical = [item for item in findings if item["classification"] != "FACT"]
        if not analytical:
            lines.append("Отдельные выводы, риски и гипотезы не утверждены.")
        for item in analytical:
            lines.extend(self._render_finding(item, source_by_id, claim_by_id, coverage_by_finding))

        lines.extend(["", "## 5. Ключевые сущности и связи", ""])
        for entity in entities:
            label = entity["display_name"]
            if public_export and redacted and entity["access_class"] == "PUBLIC_WITH_PERSONAL_DATA":
                label = f"[РЕДАКТИРОВАНО: {entity['entity_type']}]"
            lines.append(f"- `{entity['entity_id']}` — **{entity['entity_type']}**: {label}; статус `{entity['status']}`.")
        if relations:
            lines.append("")
            for relation in relations:
                left = entity_by_id.get(relation["from_entity_id"], {}).get("display_name", relation["from_entity_id"])
                right = entity_by_id.get(relation["to_entity_id"], {}).get("display_name", relation["to_entity_id"])
                lines.append(
                    f"- `{relation['relation_id']}`: {left} — **{relation['relation_type']}** → {right}; "
                    f"статус `{relation['status']}`, доказательность `{relation['evidence_grade']}`."
                )
                for limitation in relation["not_implying"]:
                    lines.append(f"  - Не означает: {limitation}")

        lines.extend(["", "## 6. Противоречия и непроверенные вопросы", ""])
        open_gaps = [item for item in gaps if item["state"] not in {"RESOLVED", "WAIVED"}]
        if not open_gaps:
            lines.append("Открытых машиночитаемых пробелов исследования не зарегистрировано.")
        for gap in open_gaps:
            lines.append(
                f"- `{gap['research_gap_id']}` [{gap['priority']}/{gap['stream']}/{gap['state']}]: "
                f"{gap['question']} — {gap['why_matters']}"
            )
            for evidence in gap["evidence_needed"]:
                lines.append(f"  - Требуется: {evidence}")

        lines.extend(["", "## 7. Реестр источников", ""])
        if not sources:
            lines.append("Источники не зарегистрированы.")
        for source in sources:
            lines.append(
                f"- `{source['source_id']}` — {source['title']} ({source['publisher']}); "
                f"тип `{source['source_type']}`, уровень `{source['primary_level']}`, "
                f"оценка `{source['reliability_grade']}`; {source['url']}"
            )
            lines.append("  - Подтверждает: " + "; ".join(source["what_it_supports"]))
            lines.append("  - Не подтверждает: " + "; ".join(source["what_it_does_not_support"]))

        lines.extend(
            [
                "",
                "## 8. Контроль доказательств и аудита",
                "",
                f"- Сохранённых captures: **{len(captures)}**.",
                f"- Источников с целостным capture для выводов: **{len(capture_source_ids)}**.",
                f"- Полная трассировка каждого finding до capture: **{'ДА' if evidence_trace_complete else 'НЕТ'}**.",
                f"- Записей search journal: **{journal_check['entries']}**.",
                f"- Цепочка hash журнала: **{'PASS' if journal_check['valid'] else 'FAIL'}**.",
                "",
                "## 9. Ограничения",
                "",
                "- Публикация источника подтверждает факт публикации, но не автоматически истинность каждого содержащегося в нём утверждения.",
                "- Совпадение имени, адреса, IP, домена, контакта или кошелька не доказывает единый контроль без отдельной проверки.",
                "- `NO_HIT` означает отсутствие результата в проверенном объёме, а не доказанное отсутствие обстоятельства.",
                "- Автоматические модели и правила не создают `FACT`; факт требует человеческого утверждения.",
            ]
        )

        text = "\n".join(lines).rstrip() + "\n"
        report_dir = self.store.case_dir(case_id) / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        path = report_dir / report_name
        path.write_text(text, encoding="utf-8")
        digest = sha256_text(text)
        (path.with_suffix(path.suffix + ".sha256")).write_text(f"{digest}  {path.name}\n", encoding="utf-8")

        self.store.append_journal(
            case_id,
            actor_id="official-report-composer",
            actor_type="AGENT",
            action_type="EXPORT",
            stream="RED_TEAM_SOURCE_QUALITY",
            query_or_action=f"Generate {'public redacted' if public_export else 'internal'} service report",
            result_code="REVIEWED",
            result_summary=f"Generated {path.name}; SHA-256={digest}; findings={len(findings)}.",
            source_or_transform_ids=[item["source_id"] for item in sources],
            new_findings=[],
            next_pivots=[item["research_gap_id"] for item in open_gaps],
            access_class=report_access,
            actor_version=self.version,
        )
        return ReportBuildResult(
            case_id=case_id,
            path=str(path),
            sha256=digest,
            public_export=public_export,
            redacted=redacted,
            finding_count=len(findings),
            source_count=len(sources),
        )

    @staticmethod
    def _render_finding(
        finding: dict[str, Any],
        source_by_id: dict[str, dict[str, Any]],
        claim_by_id: dict[str, dict[str, Any]],
        coverage_by_finding: dict[str, dict[str, Any]],
    ) -> list[str]:
        lines = [f"### {finding['finding_id']} — {finding['statement']}", ""]
        lines.append(f"- Класс: `{finding['classification']}`; доказательность: `{finding['evidence_grade']}`.")
        lines.append(f"- Основание вывода: {finding['reasoning_summary']}")
        lines.append(f"- Red Team: `{finding['red_team_status']}`; утверждено: {finding['approved_by_role']}.")
        if finding["source_ids"]:
            lines.append("- Источники: " + ", ".join(
                f"`{source_id}` {source_by_id.get(source_id, {}).get('title', '')}".strip()
                for source_id in finding["source_ids"]
            ))
        if finding["claim_ids"]:
            lines.append("- Утверждения источников:")
            for claim_id in finding["claim_ids"]:
                claim = claim_by_id.get(claim_id)
                if claim:
                    lines.append(f"  - `{claim_id}`: {claim['statement']} ({claim['locator']}).")
        coverage = coverage_by_finding.get(finding["finding_id"])
        if coverage:
            lines.append(f"- Покрытие: `{coverage['overall_grade']}`; готовность: `{coverage['report_readiness']}`.")
        for alternative in finding["alternative_explanations"]:
            lines.append(f"- Альтернативное объяснение: {alternative}")
        for limitation in finding["limitations"]:
            lines.append(f"- Ограничение: {limitation}")
        lines.append("")
        return lines
