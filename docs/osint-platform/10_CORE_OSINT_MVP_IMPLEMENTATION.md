# 10. Core OSINT MVP v0.1 — исполняемый пассивный контур

**Статус:** IMPLEMENTED / REVIEW REQUIRED  
**Пакет:** `osint_workbench`  
**Требования:** Issues #20 и #21; Architecture Baseline `01…09`  
**Инвариант:** замороженный `father_osint` DEV v1 не изменён.

## Назначение

Первый рабочий вертикальный срез основных задач OSINT:

```text
SEED → FIVE-STREAM QUERY PLAN → PASSIVE COLLECTION / LOCAL INGEST
→ SOURCE + IMMUTABLE CAPTURE → CLAIM → ENTITY / RELATION
→ ENTITY RESOLUTION → ANALYSIS OPINIONS + DISSENT
→ HUMAN-APPROVED FINDING → COVERAGE + RESEARCH GAPS
→ DERIVED GRAPH → FORMAL REPORT → MONITOR SNAPSHOT
```

Хранилище пока файловое и понятное человеку: JSON-объекты, content-addressed raw evidence и append-only journal. PostgreSQL/Neo4j не требуются для запуска пилота.

## Реализовано

| Функция | Реализация | Защитное ограничение |
|---|---|---|
| Case/scope | цель, основание, доступ, jurisdictions, запреты | active actions выключены |
| Seed intake | исходный объект и aliases сохраняются как evidence | seed остаётся `CANDIDATE` |
| Query Planner | 5 потоков, варианты имени, зависимости, budget, stop conditions | human approval обязателен |
| Source Registry | первичность, bias, supports/does-not-support, legal note | `SOURCE ≠ FACT` |
| Evidence Vault | raw bytes, SHA-256, immutable capture metadata | `PROHIBITED` не принимается |
| Passive HTTP | один `GET`, проверка redirect/DNS/порта/размера | нет login/cookies/JS/crawl/scan |
| Extraction | URL, domain, IPv4, e-mail, phone, handle, BTC/ETH/TRON | только `MENTIONED_IN → DOCUMENT` |
| Entity Resolution | имя, identifiers, address, source quality, conflicts | `automatic_merge_performed=false` |
| Transform/Job | policy decision, input/output/run hashes, terminal result | arbitrary shell отсутствует |
| Journal | отдельный immutable JSON, sequence и SHA-256 chain | tampering обнаруживается |
| Coverage | 9 объяснимых измерений | не «вероятность истины» |
| Analysis Zoo | независимые family, opinions, consensus/dissent | `fact_promotion_allowed=false` |
| Graph | узлы, связи, evidence paths | `authoritative=false` |
| Report | формальная Markdown-справка | public export проходит gates |
| Monitor | snapshot и diff материалов/выводов/пробелов | сам сеть не собирает |
| API | read-only cases/objects/graph/report/metadata | loopback; writes = 405 |

## Пять потоков

1. `ENTITY_REGISTRY` — идентичность, реквизиты, роли, тёзки.
2. `BUSINESS_TRANSACTIONS_LOGISTICS` — деятельность, договоры, товары, платежи, маршруты.
3. `DIGITAL_FOOTPRINT` — домены, контакты, аккаунты и технические активы.
4. `LEGAL_SANCTIONS_ADVERSE` — суды, санкции, банкротство, регуляторы и процессуальный статус.
5. `RED_TEAM_SOURCE_QUALITY` — альтернативы, зависимые источники, хронология, false attribution и overclaiming.

Все потоки используют одно дело, один набор объектов и одну hash-цепочку журнала.

## Компоненты

```text
osint_workbench/
  canonical.py           canonical JSON, hashes, time, normalization
  policy.py              access/safety/export gates
  store_base.py          case/object persistence and atomic writes
  store_evidence.py      sources, captures, entities, claims, relations
  store_analysis.py      findings, gaps, journal and integrity checks
  store.py               public storage facade
  planner.py             deterministic five-stream planning
  http_collect.py        one-URL passive public HTTP GET
  extractor.py           deterministic identifier extraction
  resolution.py          explainable entity matching
  jobs.py                transform registry and acquisition manifests
  coverage.py            evidence coverage dimensions
  graph.py               non-authoritative evidence graph
  analysis_models.py     analyzer contracts
  analysis_builtins.py   lineage and contrarian analyzers
  analysis_zoo.py        independent opinions and dissent
  reporting.py           official report composer
  monitoring.py          snapshots and diffs
  service.py             loopback read-only API
  workflow.py            safe orchestration facade
  demo.py                synthetic vertical case
  cli_parser.py          command contracts
  cli_runtime.py         command execution
  cli.py                 public CLI facade
```

## Доказательственная дисциплина

```text
SOURCE → SOURCE_CAPTURE → CLAIM → ENTITY / RELATION
→ ANALYSIS_OPINION → CONSENSUS / DISSENT
→ HUMAN-APPROVED FINDING → COVERAGE / GAP → REPORT
```

Автоматически извлечённый e-mail, домен, телефон или кошелёк не связывается с лицом/компанией только по совместному упоминанию. Прямая атрибуция создаётся отдельно и требует доказательств.

## Аналитический «зоопарк»

Встроены два независимых безопасных анализатора:

- `builtin-evidence-lineage` / `DETERMINISTIC_RULE` — проверка provenance и captures;
- `builtin-graph-contrarian` / `GRAPH_ALGORITHM` — challenge candidate/disputed relations и причинного overclaiming.

Минимум две family; одинаковые модели не считаются независимыми. Opinion хранит supporting/contradicting refs, assumptions, limitations, components и SHA-256. Consensus не скрывает minority view. Remote analyzers не получают internal/restricted objects без отдельной политики.

## Пассивный HTTP-контур

Разрешён только один заранее заданный URL из утверждённого плана. Блокируются credentials в URL, схемы кроме HTTP(S), localhost/private/reserved IP, внутренние suffixes, порты кроме 80/443, redirect на запрещённый адрес и превышение лимита. Не реализованы crawling, login, cookie replay, JavaScript automation, CAPTCHA/robots bypass, port scanning и эксплуатация.

## Приёмочный срез

Синтетический кейс создаёт 3 sources, 3 captures, 9 entities, 5 claims, 5 relations, namesake match без merge, transform/job, human-approved finding, gap, coverage, 2 independent opinions, consensus, graph, report, monitor snapshot и 12 hash-chained journal events.

Локально: **14 tests PASS**; **50 generated objects PASS against 18 baseline schemas**; plan hash, journal chain и graph references PASS.

## Не входит

Production RBAC/ABAC, PostgreSQL/Neo4j/OpenSearch, distributed workers, browser extension auto-capture, OCR/media/document pipeline, конкретные государственные adapters, passive DNS/RDAP/certificate packs, Telegram integration, GraphSense backend, map/timeline UI, remote LLM execution и публичный deployment.

## Следующая очередь

```text
M1B authenticated persistence/command API
M1C browser evidence recorder
M2A official registry / sanctions / court source packs
M2B passive DNS/RDAP/certificate/archive adapters
M2C document parsing with stable locators
M2D React Search/Table ↔ Graph ↔ Dossier UI
M3 saved-search monitoring
M4 calibrated local analysis zoo
```
