# 09. Acquisition Workbench M1 — спецификация первого рабочего контура

**Статус:** DRAFT / CONTRACT-ONLY  
**Связанные требования:** Issues #20, #21; `docs/OSINT_ACQUISITION_WORKBENCH_ARCHITECTURE.md`; competitor review 2026-09-01  
**Ограничение:** документ не изменяет замороженный DEV v1 и не разрешает сетевой либо активный сбор.

## 1. Цель M1

Проверить один полный, объяснимый путь от исходного объекта до формальной справки:

```text
SEED ENTITY
  → HUMAN-GOVERNED QUERY PLAN
  → FIVE STREAMS
  → ACQUISITION JOBS
  → SOURCE / CAPTURE / CLAIM
  → ENTITY RESOLUTION
  → RELATION
  → ANALYSIS ZOO / RED TEAM
  → REVIEWED FINDING
  → COVERAGE + RESEARCH GAPS
  → GRAPH / DOSSIER / REPORT
  → APPEND-ONLY SEARCH JOURNAL
```

M1 должен доказать не ширину числа подключённых источников, а управляемость процесса и воспроизводимость каждого существенного вывода.

## 2. Три равноправных представления

Рабочее место не является «Maltego, только красивее». Одна модель дела отображается тремя синхронизированными способами:

```text
SEARCH / TABLE
      ↕
GRAPH / MAP / TIMELINE
      ↕
DOSSIER / EVIDENCE / REPORT
```

- **Search / Table** — быстрый ввод известного идентификатора, фильтры, массовое выделение и cross-reference.
- **Graph / Map / Timeline** — связи, пути, временной порядок и география.
- **Dossier / Evidence / Report** — установленные обстоятельства, claims, ограничения, доказательства и официальный результат.

Переключение представления не создаёт копии сущности или отдельную «истину интерфейса».

## 3. Экран Workbench v1

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ CASE | IDENTIFY | INVESTIGATE | MONITOR | REPORT | access | readiness  │
├────────────────┬──────────────────────────────┬─────────────────────────┤
│ SEARCH/TABLE   │ GRAPH / MAP / TIMELINE       │ DOSSIER                 │
│ seeds          │ nodes, typed edges, paths    │ identity                │
│ entities       │ bounded expansion            │ claims / findings       │
│ source packs   │ shortest/common paths        │ evidence / limitations  │
│ bulk selection │ evidence-path highlighting   │ risks / contradictions  │
├────────────────┴──────────────────────────────┴─────────────────────────┤
│ JOBS | FIVE STREAMS | SOURCES | TOOLS | SEARCH JOURNAL | GAPS         │
└─────────────────────────────────────────────────────────────────────────┘
```

Для каждого узла, ребра и finding обязательна команда:

> **Почему система считает это установленным или связанным?**

Ответ строится только по сохранённой цепочке:

```text
SOURCE → SOURCE_CAPTURE → CLAIM → RELATION
→ ANALYSIS_OPINION / CONSENSUS → HUMAN-APPROVED FINDING
→ RISK / RECOMMENDATION
```

## 4. Ввод исходного объекта

M1 принимает один seed:

- ФИО;
- название организации;
- регистрационный номер / ИНН;
- адрес;
- домен;
- публичный аккаунт;
- криптокошелёк;
- документ.

До запуска поиска выполняются:

1. нормализация;
2. определение типа;
3. выделение юрисдикции;
4. поиск точных и вероятных совпадений;
5. создание кандидатов entity resolution;
6. показ противоречащих признаков;
7. запрет silent merge;
8. выбор режима `IDENTIFY / INVESTIGATE / MONITOR`.

## 5. Проектные временные SLO интерфейса

Это **проектные цели отклика**, а не измеренная производительность. Производственные сроки нельзя публиковать до появления телеметрии.

| От момента действия | Целевой результат |
|---|---|
| 0–0,5 с | интерфейс принимает seed и создаёт локальный draft |
| до 2 с | нормализация и первичная валидация формата |
| до 5 с | локальные candidate matches и известные связи из текущего case corpus |
| до 10 с | отображение предлагаемого query plan и пяти потоков |
| до 2 с после approval | jobs поставлены в очередь, пользователь видит первый status event |
| далее | внешние источники работают независимо; показываются `FOUND / NO_HIT / BLOCKED / CONFLICT / ERROR`, а не фиктивный общий процент |

Для fixture-only M1 допускается полностью детерминированный локальный прогон. Для браузеров, API, реестров и блокчейнов время завершения зависит от источника и измеряется отдельно.

## 6. Пять постоянных потоков

| Поток | Главный вопрос | Выход |
|---|---|---|
| `ENTITY_REGISTRY` | Кто это и не смешаны ли одноимённые объекты? | entities, identifiers, ownership/role claims, entity-match decisions |
| `BUSINESS_TRANSACTIONS_LOGISTICS` | Как реально движутся деньги, товар, услуга и управление? | contracts, flows, facilities, routes, economic-event candidates |
| `DIGITAL_FOOTPRINT` | Какие домены, почта, телефоны, аккаунты и инфраструктура связаны с объектом? | observables, captures, relations, historical changes |
| `LEGAL_SANCTIONS_ADVERSE` | Какие официальные правовые, санкционные и неблагоприятные сведения существуют? | source claims with exact status, dates and jurisdiction |
| `RED_TEAM_SOURCE_QUALITY` | Где тёзки, причинные ошибки, конфликт источников и переоценка? | dissent, contradictions, rejected inferences, research gaps |

Все потоки записывают результаты в один case graph и один hash-chained append-only journal. Отдельные тексты потоков не являются пятью независимыми итоговыми справками.

## 7. Машиночитаемые контракты M1

Добавлены:

| Schema | Назначение |
|---|---|
| `query-plan.schema.json` | план исследования, неизвестные, pivots, границы и approval |
| `acquisition-job.schema.json` | воспроизводимая задача сбора с policy decision и manifest hashes |
| `search-journal.schema.json` | append-only запись `FOUND / NO_HIT / BLOCKED / CONFLICT / ERROR` |
| `entity-match.schema.json` | объяснимое разрешение тёзок и запрет silent merge |
| `transform.schema.json` | evidence-first transform / source integration descriptor |
| `coverage.schema.json` | покрытие finding по отдельным доказательственным измерениям |
| `research-gap.schema.json` | что не проверено, почему важно и как влияет на отчёт |
| `graph-view.schema.json` | производный payload для графа и evidence-path, не источник истины |

Основные объекты baseline остаются неизменными:

```text
CASE / SOURCE / SOURCE_CAPTURE / CLAIM / ENTITY / RELATION
ANALYSIS_RUN / ANALYSIS_OPINION / CONSENSUS / FINDING
TOOL_ADAPTER / AUDIT_EVENT / EXPORT_MANIFEST
```

## 8. Query Planner

Planner не начинает широкое исследование самостоятельно. Он создаёт draft:

```yaml
objective:
known_fact_ids:
unknowns:
pivots:
legal_constraints:
stop_conditions:
expected_cost_time:
human_approval:
```

Каждый pivot содержит:

- поток;
- исходные entity IDs;
- source family;
- execution mode;
- ожидаемые типы результата;
- timeout и request budget;
- access class;
- dependencies;
- приоритет и status.

Оценка времени — design estimate либо телеметрическая оценка с явно указанным основанием. Она не выдаётся за фактический срок.

## 9. Transform SDK

Transform — не «ребро из воздуха». Его нормативная цепочка:

```text
ENTITY
  → TRANSFORM
  → ACQUISITION JOB
  → RAW EVIDENCE / CAPTURE
  → CLAIM
  → ENTITY / RELATION CANDIDATE
  → REVIEW
  → FINDING
  → JOURNAL
```

Descriptor фиксирует входы, выходы, источник, credentials mode, legal scope, rate limit, parser version, evidence capture mode, execution profile, safety class, network policy и health.

Присутствие бинарного файла в Kali не создаёт разрешённый transform.

## 10. Entity Resolution

Каждое вероятное совпадение хранит:

- exact identifier;
- name/transliteration similarity;
- address overlap;
- temporal consistency;
- source quality;
- supporting features;
- contradicting features;
- missing decisive evidence;
- method/version/hash;
- human decision.

В M1 `automatic_merge_performed` всегда `false`. Объединение или разделение сущностей оформляется отдельным reviewed audit event.

## 11. Evidence Coverage и Research Gaps

Один процент «уверенности» не используется как единственное объяснение. Coverage оценивается по измерениям:

- identity resolution;
- source authority;
- source independence;
- directness;
- corroboration;
- temporal alignment;
- contradictions;
- access legality;
- capture integrity.

Отдельный `RESEARCH_GAP` показывает:

- что не проверено;
- к какому entity/finding относится;
- какой поток ответственен;
- какие доказательства нужны;
- почему проверка заблокирована либо дала `NO_HIT`;
- блокирует ли пробел отчёт или только ограничивает формулировку.

`NO_HIT` означает отсутствие результата в конкретном проверенном источнике/корпусе, а не доказанное отсутствие обстоятельства в мире.

## 12. Управляемый аналитический «зоопарк»

После нормализации evidence bundle может параллельно обрабатываться:

- deterministic extractor;
- entity/link resolver;
- temporal checker;
- contradiction analyzer;
- graph algorithms;
- source-quality rules;
- локальными LLM разных семейств;
- media pipeline;
- legal/regulatory ruleset;
- contrarian / Red Team analyzer.

Результаты сохраняются раздельно как `ANALYSIS_OPINION`. Несколько экземпляров одной model family не считаются независимым подтверждением. Consensus сохраняет dissent. Только человек может утвердить `FACT`.

## 13. Синтетический демонстрационный сценарий

`CASE-SYNTH-0001` проходит пять потоков:

1. registry fixture создаёт `SRC-0001`, `CAP-0001`, `CLM-0001`, `ENT-0001`, `ENT-0002`, `REL-0001`;
2. business stream не находит подтверждения фактического присутствия и создаёт `GAP-SYNTH-0001`;
3. digital stream возвращает `NO_HIT` в пределах fixture corpus;
4. legal stream возвращает `NO_HIT` в пределах fixture corpus;
5. Red Team запрещает расширять регистрационную связь до утверждения о деятельности;
6. human review утверждает узкий `FND-0001`;
7. coverage маркирует finding `READY_WITH_LIMITATION`;
8. graph view показывает evidence path и открытый research gap;
9. пять journal events образуют hash chain.

## 14. Реальный пилот TECHNOSPETSTRADING

Реальный кейс не копируется в публичный fixture без отдельной классификации.

Разрешённая последовательность:

```text
restricted working case
  → source classification
  → capture and hash
  → minimization
  → fact/claim separation
  → legal/editorial review
  → redacted public graph fixture
```

В публичном репозитории допустимы только законно публикуемые source references, hashes, обезличенные identifiers, методика и redacted outputs. Raw captures, лишние ПДн и restricted originals остаются в закрытом Evidence Vault.

## 15. Acceptance gates M1

- [ ] Seed создаёт query-plan draft, но broad collection не запускается без policy decision.
- [ ] Пять потоков имеют отдельные jobs и терминальные статусы.
- [ ] `NO_HIT`, `BLOCKED`, `CONFLICT` и `ERROR` не смешиваются.
- [ ] Каждый `FOUND` связан с source/capture либо явно помечен как lead.
- [ ] Entity candidates не объединяются молча.
- [ ] Каждое ребро графа открывает evidence path или показывает отсутствие основания.
- [ ] Research gaps видны на entity, finding и report readiness.
- [ ] Analysis zoo не может записать `FACT`.
- [ ] Search journal имеет последовательность и hash chain.
- [ ] Public export блокирует restricted data и неподтверждённые обвинения.
- [ ] Все synthetic fixtures проходят JSON Schema Draft 2020-12.
- [ ] Изменения ограничены `docs/osint-platform/**`; DEV v1 не изменён.

## 16. Не входит в M1

- production browser extension;
- реальные API credentials;
- Neo4j/PostgreSQL deployment;
- mass cross-reference against external datasets;
- blockchain node/indexer;
- unrestricted terminal;
- active scanning or exploitation;
- autonomous attribution;
- automatic public publication;
- production performance claim without telemetry.

## 17. Следующий implementation gate

После утверждения contracts:

```text
M1A — read-only fixture API
M1B — Search/Table + Graph + Dossier viewer
M1C — evidence-path drawer + gaps + journal
M1D — one passive local transform
M1E — browser recorder prototype in isolated synthetic mode
```

Каждый следующий gate добавляется без изменения frozen DEV v1 либо после отдельного решения о его supersession.
