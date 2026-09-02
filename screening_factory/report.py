from __future__ import annotations

from collections import defaultdict
from html import escape
from pathlib import Path

from .models import FactoryRun, Outcome
from .profiles import CHECK_BY_CODE


class MarkdownReportBuilder:
    """Build a traceable, decision-oriented Russian screening report."""

    def build(self, run: FactoryRun) -> str:
        request = run.request
        subject = request.subject
        lines = [
            "# Справка Screening Factory M3",
            "",
            f"**Дело:** `{request.case_id}`  ",
            f"**Запрос:** `{request.request_id}`  ",
            f"**Объект:** {subject.display_name}  ",
            f"**Тип:** `{subject.kind.value}`  ",
            f"**Страна:** `{subject.country_code}`  ",
            f"**Профиль:** `{run.plan.profile_id}`  ",
            f"**Глубина:** `{request.depth.value}`  ",
            f"**Риск:** `{request.risk_tier.value}`  ",
            "",
            "## 1. Цель, основание и границы",
            "",
            f"**Цель:** {request.purpose}",
            "",
            f"**Основание использования данных:** {request.legal_basis_note}",
            "",
            "Контур выполняет только пассивные проверки по разрешённым классам источников. "
            "Вывод инструмента является наблюдением или сообщением источника и не становится фактом без проверки.",
            "",
            "## 2. Производственный итог",
            "",
            f"- Проверок в плане: **{run.summary.total}**",
            f"- Пиковая параллельность: **{run.summary.peak_parallelism}**",
            f"- Длительность прогона: **{run.summary.duration_ms} мс**",
            f"- Готовность к итоговому решению: **{'ДА' if run.summary.report_ready else 'НЕТ'}**",
            "",
            "### Статусы",
            "",
        ]
        for name, count in run.summary.counts_by_outcome.items():
            lines.append(f"- `{name}`: {count}")

        lines.extend(["", "### Блокирующие пробелы", ""])
        if run.summary.blocking_gaps:
            lines.extend(f"- {item}" for item in run.summary.blocking_gaps)
        else:
            lines.append("- Не выявлены.")

        lines.extend([
            "",
            "## 3. Матрица проверок",
            "",
            "| Код | Проверка | Поток | Результат | Адаптер | Evidence | Review |",
            "|---|---|---|---|---|---:|---|",
        ])
        for result in run.results:
            definition = CHECK_BY_CODE[result.check_code]
            lines.append(
                "| {code} | {title} | {stream} | {outcome} | {adapter} | {evidence} | {review} |".format(
                    code=result.check_code,
                    title=definition.title_ru.replace("|", "\\|"),
                    stream=definition.stream.value,
                    outcome=result.outcome.value,
                    adapter=result.adapter_id or "—",
                    evidence=len(result.evidence_refs),
                    review="ТРЕБУЕТСЯ" if result.human_review_required else "—",
                )
            )

        by_stream: dict[str, list] = defaultdict(list)
        for result in run.results:
            by_stream[CHECK_BY_CODE[result.check_code].stream.value].append(result)
        lines.extend(["", "## 4. Результаты по пяти потокам", ""])
        for stream, results in sorted(by_stream.items()):
            lines.extend([f"### {stream}", ""])
            for result in results:
                definition = CHECK_BY_CODE[result.check_code]
                lines.append(f"#### `{result.check_code}` — {definition.title_ru}")
                lines.append("")
                lines.append(f"**Статус:** `{result.outcome.value}`")
                lines.append("")
                if result.observations:
                    lines.append("**Наблюдения:**")
                    lines.extend(f"- {obs.statement}" for obs in result.observations)
                    lines.append("")
                if result.conflicts:
                    lines.append("**Противоречия:**")
                    lines.extend(f"- {item}" for item in result.conflicts)
                    lines.append("")
                if result.limitations:
                    lines.append("**Ограничения:**")
                    lines.extend(f"- {item}" for item in result.limitations)
                    lines.append("")
                if result.next_actions:
                    lines.append("**Следующие действия:**")
                    lines.extend(f"- {item}" for item in result.next_actions)
                    lines.append("")

        lines.extend([
            "## 5. Правило NO_HIT",
            "",
            "`NO_HIT_IN_SCOPE` означает только, что сведения не выявлены в зафиксированных источниках, "
            "запросах и временном диапазоне. Это **не доказательство отсутствия** факта или связи.",
            "",
            "## 6. Контроль качества",
            "",
            "Перед выпуском решения главный аналитик обязан проверить идентичность объекта, точность процессуальных "
            "статусов, применимость юрисдикции, независимость источников, противоречия, минимизацию персональных данных "
            "и соответствие каждого вывода сохранённым доказательствам.",
            "",
            "## 7. Что стоит улучшить",
            "",
            "| Что стоит улучшить | Как улучшить | Приоритет |",
            "|---|---|---|",
        ])
        missing_adapters = [r for r in run.results if r.outcome == Outcome.BLOCKED_NO_ADAPTER]
        if missing_adapters:
            lines.append(
                f"| Подключение источников ({len(missing_adapters)} проверок без адаптера) | "
                "Реализовать и откалибровать официальные read-only адаптеры; сохранять сырой ответ и SHA-256 | P0 |"
            )
        if run.plan.missing_identity_anchors:
            lines.append(
                "| Идентификация объекта | Получить законный сильный идентификатор и провести отдельную проверку тёзок | P0 |"
            )
        if any(r.human_review_required for r in run.results):
            lines.append(
                "| Очередь экспертного рассмотрения | Добавить reviewer assignment, SLA и подписанное решение | P0 |"
            )
        lines.append(
            "| Производственная телеметрия | Накапливать фактический throughput, retries, false positives и долю повторной работы | P1 |"
        )
        lines.extend([
            "",
            "## 8. Резолюция",
            "",
            "- [ ] Личность/организация разрешена без критического конфликта.",
            "- [ ] Санкционные совпадения подтверждены либо отклонены по идентификаторам.",
            "- [ ] Судебные и регуляторные сведения переданы с точным статусом.",
            "- [ ] Все существенные выводы имеют `source_id` и `evidence_ref`.",
            "- [ ] Red Team и правовая/редакционная проверка завершены.",
            "- [ ] Итоговое решение подписано уполномоченным сотрудником.",
            "",
        ])
        return "\n".join(lines)

    def write(self, run: FactoryRun, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.build(run), encoding="utf-8")
        return target


class HtmlDashboardBuilder:
    """Produce a dependency-free read-only facade with honest connection marks."""

    def build(self, run: FactoryRun) -> str:
        rows = []
        for result in run.results:
            definition = CHECK_BY_CODE[result.check_code]
            rows.append(
                "<tr>"
                f"<td><code>{escape(result.check_code)}</code></td>"
                f"<td>{escape(definition.title_ru)}</td>"
                f"<td>{escape(definition.stream.value)}</td>"
                f"<td><span class='status {escape(result.outcome.value.lower())}'>{escape(result.outcome.value)}</span></td>"
                f"<td>{'✅' if result.adapter_id else '⬜'} Адаптер<br><small>{escape(result.adapter_id or 'не подключён')}</small></td>"
                f"<td>{'✅' if result.evidence_refs else '⬜'} Evidence ({len(result.evidence_refs)})</td>"
                f"<td>{'⚠️ Review' if result.human_review_required else '✅ Review gate not raised'}</td>"
                "</tr>"
            )
        gaps = "".join(f"<li>{escape(item)}</li>" for item in run.summary.blocking_gaps) or "<li>Нет</li>"
        return f"""<!doctype html>
<html lang='ru'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Screening Factory M3</title>
<style>
:root {{ color-scheme: dark; font-family: Inter,Segoe UI,sans-serif; }}
body {{ margin:0; background:#0b1020; color:#eef2ff; }}
main {{ max-width:1500px; margin:auto; padding:28px; }}
h1 {{ margin:0 0 8px; }} .muted,small {{ color:#9aa7c7; }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px; margin:22px 0; }}
.card {{ background:#151c31; border:1px solid #2b3658; border-radius:14px; padding:16px; }}
.value {{ font-size:28px; font-weight:700; }}
table {{ width:100%; border-collapse:collapse; background:#11182a; }}
th,td {{ text-align:left; padding:10px; border-bottom:1px solid #293451; vertical-align:top; }}
th {{ position:sticky; top:0; background:#18213a; }}
.status {{ padding:4px 7px; border-radius:8px; background:#25304c; font-size:12px; }}
.found {{ background:#174b3b; }} .conflict,.error {{ background:#692d39; }}
.blocked_no_adapter,.blocked_policy,.blocked_missing_identifier {{ background:#5b4822; }}
section {{ margin-top:24px; }} code {{ color:#b9c8ff; }}
</style>
</head>
<body><main>
<h1>Screening Factory M3</h1>
<p class='muted'>{escape(run.request.subject.display_name)} · {escape(run.plan.profile_id)} · case {escape(run.request.case_id)}</p>
<div class='cards'>
<div class='card'><div class='muted'>Проверок</div><div class='value'>{run.summary.total}</div></div>
<div class='card'><div class='muted'>Параллельность</div><div class='value'>{run.summary.peak_parallelism}</div></div>
<div class='card'><div class='muted'>Время</div><div class='value'>{run.summary.duration_ms} ms</div></div>
<div class='card'><div class='muted'>Готовность</div><div class='value'>{'✅' if run.summary.report_ready else '⚠️'}</div></div>
</div>
<section><h2>Блокирующие пробелы</h2><ul>{gaps}</ul></section>
<section><h2>Производственная матрица</h2>
<table><thead><tr><th>Код</th><th>Проверка</th><th>Поток</th><th>Статус</th><th>Адаптер</th><th>Evidence</th><th>Review</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></section>
<section><p class='muted'>NO_HIT_IN_SCOPE не является доказательством отсутствия. Зеленая отметка показывает только выполненный технический этап.</p></section>
</main></body></html>"""

    def write(self, run: FactoryRun, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.build(run), encoding="utf-8")
        return target
