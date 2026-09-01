# FATHER OSINT Platform — Architecture Baseline v0.1 + Acquisition Workbench M1

**Статус:** DRAFT / CONTRACT-ONLY  
**Дата baseline:** 2026-09-01; M1 increment: 2026-09-02  
**Связанные требования:** GitHub Issues #20 и #21  
**Ограничение:** замороженный DEV v1 не изменяется; пакет не вводит production-код и не разрешает активное воздействие на внешние системы.

## Назначение

Пакет определяет следующий слой `OSINT_deepseek`: официальное ведение дел, доказательственную трассировку, управляемый аналитический «зоопарк», acquisition/query planning, разрешение сущностей, безопасное подключение инструментов, формирование служебных справок и контролируемый экспорт.

```text
SEED → QUERY PLAN → FIVE STREAMS → ACQUISITION JOBS
→ SOURCE → SOURCE_CAPTURE → CLAIM → ENTITY / RELATION
→ INDEPENDENT ANALYSIS OPINIONS → CONSENSUS / DISAGREEMENT
→ HUMAN-REVIEWED FACT | INFERENCE | HYPOTHESIS
→ COVERAGE / RESEARCH GAPS → RISK → DECISION
→ GRAPH / DOSSIER / REPORT / EXPORT
```

## Неподвижные принципы

1. Коллектор возвращает материал, а не истину.
2. Оригинал и его хеш важнее любой сводки.
3. `SOURCE`, `CLAIM`, `FACT`, `INFERENCE` и `HYPOTHESIS` — разные объекты.
4. Ни одна LLM, модель, алгоритм, transform или инструмент не создаёт `FACT` напрямую.
5. Каждый существенный вывод открывается до источника и сохранённой копии.
6. Публичный GitHub хранит код, схемы, методику, синтетические/редактированные примеры, хеши и реестры — не сырые чувствительные доказательства.
7. Инструмент не становится разрешённым только потому, что установлен в Kali.
8. Query Planner предлагает план; broad collection проходит policy decision и human governance.
9. Entity Resolution не выполняет silent merge.
10. `NO_HIT` не означает доказанное отсутствие обстоятельства в мире.
11. Research gaps и dissent не скрываются ради красивого отчёта.
12. Все ручные и автоматические действия записываются в append-only journal.
13. Официальный экспорт проходит правовые, доказательственные и редакционные ворота.
14. DEV v1 остаётся контрольной линией и не меняется этим baseline.

## Рабочая модель интерфейса

```text
SEARCH / TABLE
      ↕
GRAPH / MAP / TIMELINE
      ↕
DOSSIER / EVIDENCE / REPORT
```

Каждый узел, ребро и finding должен отвечать на вопрос: **«Почему система считает это установленным или связанным?»**

## Состав пакета

| Раздел | Содержание |
|---|---|
| `01_VISION_AND_SCOPE.md` | цель, границы и роли |
| `02_CASE_EVIDENCE_MODEL.md` | модель дела и доказательств |
| `03_DATA_LEGAL_POLICY.md` | классификация, минимизация, экспорт |
| `04_ANALYSIS_ZOO_ORCHESTRATION.md` | управляемый ансамбль анализаторов |
| `05_SYSTEM_ARCHITECTURE.md` | компоненты и доверительные границы |
| `06_THREAT_MODEL.md` | угрозы и меры защиты |
| `07_REPORTING_STANDARD.md` | официальный пакет документов |
| `08_MVP_ACCEPTANCE.md` | вертикальный MVP и приёмочные ворота |
| `09_ACQUISITION_WORKBENCH_M1.md` | экран, five-stream workflow, проектные SLO и M1 contracts |
| `adr/` | архитектурные решения |
| `schemas/` | 21 JSON Schema Draft 2020-12 |
| `fixtures/CASE-SYNTH-0001/` | 29 проверяемых синтетических JSON fixtures и redacted report |
| `validation/` | schema, hash-chain и reference-integrity проверки |

## Контракты M1

Новый increment добавляет:

- `QUERY_PLAN`;
- `ACQUISITION_JOB`;
- `SEARCH_JOURNAL`;
- `ENTITY_MATCH`;
- `TRANSFORM`;
- `COVERAGE`;
- `RESEARCH_GAP`;
- `GRAPH_VIEW`.

Они расширяют, но не заменяют baseline-объекты `CASE / SOURCE / CAPTURE / CLAIM / ENTITY / RELATION / OPINION / CONSENSUS / FINDING / AUDIT / EXPORT`.

## Синтетический вертикальный пример

`CASE-SYNTH-0001` демонстрирует:

- один seed-объект;
- пять аналитических потоков;
- evidence-first transform;
- acquisition job;
- namesake/entity-resolution decision;
- `FOUND` и `NO_HIT` как разные терминальные результаты;
- research gap;
- coverage assessment;
- derived graph payload;
- evidence path;
- пять journal events с последовательностью и hash chain;
- узкий human-approved finding без расширения смысла источника.

## Проверка

```powershell
cd docs\osint-platform\validation
python -m pip install -r requirements.txt
python validate_contracts.py
```

Ожидаемый результат текущего пакета:

```text
21 schemas meta-validated
29 fixtures schema-validated
query-plan hash PASS
journal hash chain PASS
graph references PASS
```

## Не входит

- изменение `father_osint`, collectors, storage, pipeline или transports;
- production browser recorder и реальные credentials;
- сетевой сбор и публикация реальных материалов расследований;
- Neo4j/PostgreSQL/LLM runtime;
- unrestricted shell;
- активное сканирование, exploitation или credential attacks;
- автономная атрибуция;
- automatic public publication;
- утверждение производительности без телеметрии.

## Следующий implementation gate после review

```text
M1A read-only fixture API
→ M1B Search/Table + Graph + Dossier viewer
→ M1C evidence-path drawer + gaps + journal
→ M1D one passive local transform
→ M1E isolated synthetic browser-recorder prototype
```
