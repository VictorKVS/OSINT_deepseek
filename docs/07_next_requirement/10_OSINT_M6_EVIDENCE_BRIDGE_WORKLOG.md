# OSINT M6 Evidence Bridge — ход работ и бизнес-процесс

**Document ID:** OSINT-M6-EVIDENCE-BRIDGE-0001  
**Status:** ARCHITECTURE / WORKLOG — IMPLEMENTATION NOT STARTED  
**Date:** 2026-08-21  
**Branch:** agent/osint-m6-evidence-worklog  
**Baseline:** main @ c79401be7016c29f9a5ff64a879608defe569f50  
**Related:** docs/RESEARCH_HYPOTHESIS_ENGINE.md  
**Governing rule:** NO CODE BEFORE CONTRACT

## 1. Цель

Расширить существующий OSINT_deepseek подключаемым доказательным контуром:

OSINT → черновой аналитик → Главный доказательный аналитик → профильные эксперты → верификатор → человек → отчёт и база знаний.

Стабильный DEV v1 остаётся неизменным. M6 не создаёт вторую OSINT-систему и не переносит профессиональный анализ внутрь сборщиков.

## 2. Подтверждённое состояние репозитория

На момент аудита:

- OSINT_deepseek уже является поставщиком материалов для фабрики знаний FATHER;
- DEV v1 считается frozen baseline;
- текущая активная capability — M5 Telegram Radar;
- выполнение в основном синхронное через CLI;
- отдельные FastAPI, web UI, очередь задач и Trace Viewer отсутствуют;
- append-only JSONL, SHA-256, сохранение lineage и видимых отказов уже являются архитектурной основой;
- OSINT не устанавливает истину и не публикует знания автоматически.

Фактически подтверждённые основные модели DEV v1:

- ResearchTask;
- Material;
- MaterialPackage;
- ReviewCycle.evidence_package, использующий MaterialPackage.

Ранее предполагавшиеся ResearchRequest, AcquisitionReport и самостоятельный EvidencePackage в текущем коде не подтверждены. M6 не должен импортировать несуществующие сущности.

## 3. Граница решения

~~~mermaid
flowchart TD
    A["OSINT_deepseek DEV v1"] --> B["M6 Evidence Bridge"]
    B --> C["Evidence Platform"]
    C --> D["RAG"]
    D --> E["Professional agents"]
    E --> F["Human review"]
    F --> G["Knowledge Gate"]
    G --> H["Reports and Domain KB"]
~~~

### Не изменяем в MIN

- father_osint/models.py;
- father_osint/agent.py;
- father_osint/storage.py;
- father_osint/review_pipeline.py;
- текущую семантику ResearchTask, Material и MaterialPackage;
- canonical DEV runners;
- транспортно-независимый Telegram-контур.

### Добавляем композиционно

Предпочтительная форма — sibling package father_evidence_platform или независимый integration package, который читает публичные результаты OSINT через адаптеры.

~~~text
OSINT_deepseek/
├── father_osint/                  # frozen core
├── father_evidence_platform/      # additive layer
│   ├── api/
│   ├── domain/
│   ├── integration/
│   ├── registry/
│   ├── services/
│   ├── storage/
│   ├── web/
│   └── tests/
└── docs/
~~~

## 4. Бизнес-нотация

Основная процессная нотация — BPMN 2.0.

Дополнительные представления:

- DMN — выбор версии или архитектурного решения;
- C4 — техническая архитектура;
- ERD — данные платформы;
- event/span model — фактическая трассировка выполнения.

## 5. Участники BPMN

| Lane | Ответственность |
|---|---|
| Заказчик | Формулирует вопрос, принимает результат |
| FATHER Orchestrator | Управляет задачей, статусами и маршрутами |
| OSINT_deepseek | Ищет и получает материалы |
| Составной OSINT-аналитик | Готовит черновые материалы |
| Главный доказательный аналитик | Сравнивает, строит версии и заключение |
| Профильные эксперты | Проверяют отдельные аспекты |
| Верификатор / Socrates | Атакует допущения и проверяет доказательства |
| Человек | Утверждает или возвращает результат |
| Knowledge Gate | Публикует только утверждённые знания |

## 6. Основной BPMN-процесс

~~~mermaid
flowchart TD
    A["Получить задачу"] --> B["Уточнить цель и результат"]
    B --> C{"Задача понятна?"}
    C -- "Нет" --> D["Запросить уточнение"]
    D --> B
    C -- "Да" --> E["Сформировать Research Plan"]
    E --> F["OSINT-сбор"]
    F --> G["Черновой Evidence Pack"]
    G --> H{"Материалов достаточно?"}
    H -- "Нет" --> I["Открыть Research Gap"]
    I --> F
    H -- "Да" --> J["Главный аналитик"]
    J --> K["Сравнить claims и evidence"]
    K --> L["Сформировать версии и противоречия"]
    L --> M{"Нужна профильная экспертиза?"}
    M -- "Да" --> N["Параллельные экспертные задания"]
    N --> O["Объединить заключения"]
    M -- "Нет" --> P["Подготовить рекомендацию"]
    O --> P
    P --> Q["Socrates / Verifier"]
    Q --> R{"Проверка пройдена?"}
    R -- "Нет" --> S["Вернуть на доработку"]
    S --> J
    R -- "Да" --> T["Human review"]
    T --> U{"Утверждено?"}
    U -- "Нет" --> V["Зафиксировать замечания"]
    V --> J
    U -- "Да" --> W["Knowledge Gate"]
    W --> X["Отчёт и Domain KB"]
~~~

## 7. Составной аналитик OSINT

Составной аналитик работает быстро и массово. Его предел полномочий — DRAFT.

### Задачи

- классифицировать материалы;
- выделять определения и первичные утверждения;
- объединять очевидные дубликаты;
- отмечать возможные конфликты;
- формировать список неизвестного;
- готовить Evidence Pack;
- возвращать Research Gaps в OSINT.

### Он не должен

- утверждать истину;
- скрывать противоречия;
- превращать модельное предположение в факт;
- самостоятельно публиковать знания;
- заменять профессиональную экспертизу.

## 8. Главный доказательный аналитик

**Agent ID:** CHIEF-EVIDENCE-ANALYST-001  
**Класс:** professional reasoning agent  
**Полномочие:** VERIFIED / RECOMMENDED, но не HUMAN APPROVED.

### Миссия

Превращать черновые материалы OSINT, документы и существующие знания FATHER в проверяемые выводы, версии, теории, профессиональные отчёты и кандидаты в базу знаний.

### Входы

- Task Contract;
- Research Plan;
- черновой Evidence Pack;
- source/evidence locators;
- словарь;
- предыдущие решения;
- найденные конфликты;
- критерии результата;
- паспорта профильных экспертов.

### Обязательные выходы

- confirmed_facts;
- inferences;
- competing_versions;
- evidence_for/evidence_against;
- contradictions;
- assumptions;
- unknowns;
- recommended_version;
- rejected_versions;
- confidence rationale;
- falsification tests;
- research gaps;
- professional report;
- knowledge candidates.

### Запреты

- не придумывать источники и страницы;
- не выдавать гипотезу за факт;
- не скрывать evidence against;
- не устанавливать APPROVED;
- не публиковать результат без Knowledge Gate;
- не раскрывать скрытые рассуждения модели как доказательство.

## 9. Интеллектуальный цикл Главного аналитика

~~~mermaid
flowchart TD
    A["Task and Evidence Pack"] --> B["Проверить постановку"]
    B --> C["Оценить источники"]
    C --> D["Построить claim matrix"]
    D --> E["Разделить FACT / INFERENCE / HYPOTHESIS"]
    E --> F["Создать конкурирующие версии"]
    F --> G["Собрать evidence for / against"]
    G --> H["Запросить профильных экспертов"]
    H --> I["Попытаться опровергнуть лидирующую версию"]
    I --> J{"Доказательств достаточно?"}
    J -- "Нет" --> K["Research Gap"]
    K --> A
    J -- "Да" --> L["Recommendation and Report"]
~~~

## 10. Классы аналитических результатов

| Класс | Значение |
|---|---|
| FACT | Непосредственно подтверждённое утверждение |
| INFERENCE | Вывод, логически следующий из указанных фактов |
| HYPOTHESIS | Проверяемое предположение |
| VERSION | Целостное конкурирующее объяснение |
| THEORY | Устойчивая модель с несколькими линиями доказательств |
| OPINION | Экспертная оценка |
| RECOMMENDATION | Предлагаемое действие |
| UNKNOWN | Данных недостаточно |
| CONFLICT | Надёжные источники расходятся |
| REJECTED_HYPOTHESIS | Проверенная и ослабленная/отклонённая гипотеза |

SUPPORTED не равно FACT. Высокий model score не заменяет доказательство.

## 11. DMN выбора версии

| Критерий | Вес MVP |
|---|---:|
| Доказательная поддержка | 30% |
| Надёжность и независимость источников | 20% |
| Непротиворечивость | 15% |
| Практическая применимость | 15% |
| Стоимость | 10% |
| Проверяемость | 10% |

Итоговый балл служит прозрачным сравнением, но не заменяет объяснение. Числовая confidence запрещена без определённой и откалиброванной модели.

## 12. Доказательный объектный поток

~~~mermaid
flowchart LR
    A["SOURCE"] --> B["EVIDENCE"]
    B --> C["CLAIM"]
    C --> D["HYPOTHESIS / VERSION"]
    D --> E["DECISION"]
    E --> F["TEST"]
    F --> G["RESULT"]
    G --> H["REPORT"]
    H --> I["KNOWLEDGE CANDIDATE"]
~~~

Обязательная трассировка:

SOURCE → EVIDENCE → CLAIM → VERSION → DECISION → TEST → RESULT → REPORT → KNOWLEDGE CANDIDATE.

## 13. M6 интеграционные компоненты

### EvidencePlatformTaskAdapter

Преобразует web/task request во внешний M6 Task Contract, затем — в существующий ResearchTask без изменения его семантики.

### MaterialPackageAdapter

Преобразует существующий MaterialPackage в версионированный Evidence Draft.

### Event Outbox

Append-only события M6. Повторная доставка не должна создавать повторные бизнес-объекты.

### AgentContractRegistry

Хранит версионированные паспорта:

- OSINT draft analyst;
- CHIEF-EVIDENCE-ANALYST-001;
- профильные эксперты;
- REVIEWER-001 / Socrates.

### RAGContextPackAdapter

Собирает только релевантные evidence, locators, определения, прошлые решения, конфликты и unknowns в пределах token budget.

### KnowledgeCandidateExporter

Формирует только DRAFT/VERIFIED candidate. Переход в APPROVED принадлежит человеку и Knowledge Gate.

## 14. Событийная трассировка

### Идентификаторы

- run_id — полный запуск;
- trace_id — сквозная трасса;
- span_id — отдельная операция;
- parent_span_id — родительская операция;
- correlation_id — одна бизнес-задача;
- task_id;
- source_id;
- material_id;
- package_id;
- evidence_id;
- agent_id;
- candidate_id.

### Основные события

~~~text
research.requested
search.plan.proposed
search.plan.approved
collection.started
source.attempted
source.failed
material.observed
payload.reused
material.package.ready
analysis.requested
analysis.draft.created
chief_analysis.started
version.proposed
contradiction.detected
expert.review.requested
expert.review.completed
verification.completed
human.review.requested
human.approved
human.rejected
knowledge.candidate.created
export.preview.created
export.blocked
export.completed
~~~

### Конверт события

~~~json
{
  "event_id": "EVT-000001",
  "event_type": "chief_analysis.started",
  "schema_version": "1.0",
  "occurred_at": "2026-08-21T00:00:00Z",
  "run_id": "RUN-000001",
  "trace_id": "TRACE-000001",
  "span_id": "SPAN-000010",
  "parent_span_id": "SPAN-000009",
  "correlation_id": "COR-000001",
  "task_id": "TASK-000001",
  "actor": {
    "type": "agent",
    "id": "CHIEF-EVIDENCE-ANALYST-001"
  },
  "input_refs": [],
  "output_refs": [],
  "payload_hash": "sha256:..."
}
~~~

Idempotency key:

event_type + aggregate_id + aggregate_version.

## 15. Диагностика агентов

~~~mermaid
flowchart TD
    A["Agent Registry"] --> B["Contract validation"]
    B --> C["Endpoint"]
    C --> D["Provider health"]
    D --> E["Model loaded"]
    E --> F["Context limits"]
    F --> G["Tool permissions"]
    G --> H["RAG available"]
    H --> I["Structured output"]
    I --> J["Test inference"]
~~~

Минимальные диагностические коды:

- AGENT_NOT_REGISTERED;
- AGENT_CONTRACT_INVALID;
- MODEL_ENDPOINT_REFUSED;
- MODEL_AUTH_FAILED;
- MODEL_NOT_LOADED;
- MODEL_CONTEXT_TOO_SMALL;
- RAG_UNAVAILABLE;
- VECTOR_INDEX_MISSING;
- EMBEDDING_MODEL_UNAVAILABLE;
- RAG_NO_HITS;
- CONTEXT_BUDGET_EXCEEDED;
- TOOL_PERMISSION_DENIED;
- STRUCTURED_OUTPUT_INVALID;
- CITATION_MISSING;
- CITATION_LOCATOR_INVALID;
- GROUNDING_FAILED;
- AGENT_TIMEOUT;
- RATE_LIMITED;
- HUMAN_REVIEW_REQUIRED.

Система должна показывать failed_stage, error_code, retryable и конкретное безопасное действие.

## 16. Web MVP

Первые пять экранов:

1. Dashboard — зависимости, агенты и последние runs.
2. New Run — постановка задачи и выбор процесса.
3. Run Detail / Trace Viewer — дерево spans и события в реальном времени.
4. RAG Inspector — запрос, top-k, scores, source и locator.
5. Review Queue — версии, отчёты и knowledge candidates.

Дополнительная панель Chief Analyst:

- сравнение claims;
- evidence for/against;
- competing versions;
- contradictions;
- confidence rationale;
- falsification tests;
- report builder.

## 17. API MVP

~~~text
POST /api/v1/runs
GET  /api/v1/runs/{run_id}
POST /api/v1/runs/{run_id}/start
GET  /api/v1/runs/{run_id}/events
POST /api/v1/osint/import
GET  /api/v1/sources
GET  /api/v1/agents
POST /api/v1/agents/{agent_id}/probe
POST /api/v1/rag/query
GET  /api/v1/traces/{trace_id}
POST /api/v1/reviews/{candidate_id}/approve
POST /api/v1/reviews/{candidate_id}/reject
POST /api/v1/exports/github/preview
GET  /health/live
GET  /health/ready
GET  /health/dependencies
~~~

Мутации должны принимать Idempotency-Key. Экспорт execute не входит в первый MIN без отдельного human approval.

## 18. Первый бизнес-тест

Тема первого нейтрального сценария:

**Какой стек выбрать для локального веб-приложения FATHER Knowledge Forge?**

Ожидаемый путь:

1. Task Contract;
2. Research Plan;
3. OSINT собирает 5–10 источников;
4. составной аналитик создаёт Evidence Draft;
5. Главный аналитик предлагает минимум три варианта;
6. DMN сравнивает варианты;
7. Socrates пытается опровергнуть лидирующее решение;
8. человек утверждает или возвращает;
9. система создаёт ADR и knowledge candidates;
10. весь путь виден в Trace Viewer.

## 19. Тесты MIN / MED / MAX

### MIN

- frozen core diff = 0;
- один MaterialPackage проходит adapter;
- один run имеет полную lineage;
- duplicate event не создаёт дубль;
- модель, выключенная намеренно, даёт точный error code;
- каждый claim содержит evidence locator или NEEDS_EVIDENCE;
- специалист и verifier не могут установить APPROVED;
- результат сохраняется после restart.

### MED

Всё MIN плюс:

- несколько источников;
- один подтверждённый конфликт;
- out-of-order event buffering;
- повтор после restart;
- два специализированных агента;
- retrieval metrics;
- воспроизводимое сравнение версий;
- analyst loop возвращает Research Gap.

### MAX

Всё MED плюс:

- A/B моделей и chunking;
- property-based event tests;
- signed trace/export manifest;
- continuous red-team;
- граф SOURCE→EVIDENCE→CLAIM→VERSION→TEST;
- измерение времени, стоимости и повторного использования;
- независимая экспертная проверка.

## 20. Acceptance Gates

| Gate | Условие |
|---|---|
| G0 Contract | Схемы и статусы утверждены |
| G1 Baseline | DEV v1 не изменён |
| G2 Lineage | Полная цепочка source-to-result |
| G3 Evidence | Claim имеет locator либо NEEDS_EVIDENCE |
| G4 Analysis | Есть альтернативные версии и evidence against |
| G5 Verification | Есть falsification/negative test |
| G6 Human | APPROVED возможен только человеком |
| G7 Web | Run и ошибка видны в UI |
| G8 Restart | Состояние восстанавливается без дублей |
| G9 Release | MIN полностью зелёный |

## 21. План реализации

### R0 — документ и контракты

- утвердить BPMN;
- утвердить роли;
- утвердить event envelope;
- утвердить Agent Contract;
- утвердить Evidence Draft и Chief Analysis Result;
- создать regression fixtures.

### R1 — диагностируемый вертикальный срез

- additive adapters;
- event outbox;
- SQLite metadata;
- Agent Registry;
- health/probe;
- один synthetic MaterialPackage;
- один Chief Analyst contract;
- Trace Viewer;
- human review;
- один MIN acceptance test.

### R2 — RAG и реальный OSINT пакет

- parser derivatives;
- index version;
- RAG Inspector;
- locator verification;
- Research Gap feedback;
- два агента;
- MED tests.

### R3 — профессиональная платформа

- профильные эксперты;
- отчёты и ADR;
- A/B;
- knowledge graph;
- cost/latency telemetry;
- mature web UI.

## 22. Ход работы

| Дата | Событие | Результат |
|---|---|---|
| 2026-08-21 | Выбрана BPMN 2.0 | Зафиксирован основной бизнес-процесс |
| 2026-08-21 | Разделены аналитические роли | OSINT analyst = DRAFT; Chief Analyst = VERIFIED/RECOMMENDED |
| 2026-08-21 | Выполнен read-only аудит | Подтверждены реальные DEV v1 модели и frozen boundary |
| 2026-08-21 | Спроектирован M6 Bridge | Адаптеры, события, RAG, Agent Registry |
| 2026-08-21 | Спроектирована диагностика | Послойные health checks и error codes |
| 2026-08-21 | Определён Web MVP | 5 экранов |
| 2026-08-21 | Определены gates | MIN/MED/MAX и human approval |
| 2026-08-21 | Реализация | NOT STARTED |

## 23. Открытые решения

1. Размещать father_evidence_platform внутри репозитория или отдельным репозиторием.
2. Выбрать server-rendered Jinja/HTMX или React для R1.
3. Выбрать SQLite + local vector store для MIN.
4. Зафиксировать JSON Schema Agent Contract.
5. Выбрать первый synthetic fixture.
6. Утвердить переход от M5 Telegram Radar к M6.
7. Определить владельца human approval.

## 24. Текущий вывод

M6 должен стать диагностируемым доказательным мостом между существующим OSINT_deepseek и профессиональной фабрикой знаний FATHER.

Правильный порядок:

**CONTRACT → FIXTURE → TRACE → AGENT DIAGNOSTICS → RAG → CHIEF ANALYST → HUMAN REVIEW → KNOWLEDGE GATE**

До прохождения MIN запрещено массовое формирование базы знаний или автономная публикация выводов.
