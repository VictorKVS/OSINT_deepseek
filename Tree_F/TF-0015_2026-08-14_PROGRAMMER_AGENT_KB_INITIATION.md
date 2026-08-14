# TF-0015 — PROGRAMMER AGENT / PROGRAMMING_KB INITIATION

```yaml
id: TF-0015
date: 2026-08-14
status: ACTIVE
supersedes: null
superseded_by: null
stage: parallel FATHER expert-agent research track; M5 critical path unchanged
change_class: REQ
old_sha: null
new_sha: null
related_requirements:
  - USER-REQ-2026-08-14-PROGRAMMER-AGENT-KB
related_tests: []
related_adrs: []
related_journal_entries:
  - J-020
```

## EN

### Trigger / problem

FATHER needs a Programmer Agent that can receive approved tasks from Architect/Analyst, implement them, and justify material engineering decisions with traceable sources, alternatives, risks and verification evidence.

A generic coding LLM is insufficient because citation quantity does not prove correctness, version-sensitive advice decays, performance/reliability claims are context dependent, and popular architecture choices can add unjustified complexity.

### Requirement / ТЗ

Create a dedicated FATHER Programmer Agent research track and start building PROGRAMMING_KB before executable agent code.

The track must:
- use scientific, consensus/textbook, specification and verified practice evidence;
- preserve exact source/version/freshness metadata;
- distinguish authoritative evidence from secondary/community material;
- require alternatives and risks for material decisions;
- use local experiment/benchmark evidence when the deciding claim is context-dependent;
- preserve rejected alternatives and revisit conditions;
- integrate later with Architect, Analyst, Security, DevSecOps, Test and Principal Critic roles.

### Analysis / architecture / security / reuse review

Existing FATHER rules already require requirement-first development, reuse review, acceptance evidence and `NO CODE BEFORE CONTRACT`.

The Programmer Agent is therefore started as documentation/knowledge governance only. No executable programmer-agent service, microservice or orchestration code is authorized by this record.

The knowledge track is placed under `docs/father_agents/programmer/` while the append-only decision is recorded in `Tree_F`.

Initial verified authoritative source anchors:
- IEEE Computer Society SWEBOK Guide V4.0a;
- ISO/IEC 25010:2023;
- NIST SP 800-218 SSDF v1.1 FINAL;
- NIST SP 800-218 Rev.1 SSDF v1.2 DRAFT (monitor only);
- OWASP ASVS 5.0.0;
- SLSA v1.2 APPROVED;
- OpenSSF Scorecard.

Security rule: source content is referenced and summarized within license/copyright limits; copyrighted standards/books are not copied wholesale into the repository.

Reuse value: the evidence model is intentionally generic enough to later support Architecture, Security, DevSecOps, Reliability and other FATHER expert knowledge bases without forcing them into the programmer-specific ontology.

### Test contract before code

Before executable Programmer Agent code is authorized, the documentation/evidence design must demonstrate at minimum:
1. one D2 engineering decision traceable from requirement to alternatives, sources, risks, experiment and final decision;
2. a 12-domain coverage matrix with explicit gaps;
3. source freshness/supersession handling;
4. counter-evidence and revisit semantics;
5. an evaluation corpus capable of detecting citation theater and unnecessary complexity.

### Decision

Start PROGRAMMING_KB as a parallel research/product track with four initial documents:
- product boundary/passport;
- evidence model;
- verified source register seed;
- measurable roadmap.

Keep the current OSINT M5 delivery critical path unchanged.

### WHY

The simplest safe next step is to stabilize the knowledge and decision contract before building another agent runtime. Separating the evidence model from implementation prevents the project from hard-coding uncalibrated trust scores, framework preferences or arbitrary agent decomposition.

### Local sync / Git evidence

This change is created through the connected GitHub workflow on branch:

```text
agent/programmer-agent-kb-seed
```

Local Windows users should synchronize after merge using the repository's standard Tree_F procedure.

### Files/components changed

#### Added
- `docs/father_agents/programmer/README.md`
- `docs/father_agents/programmer/01_PROGRAMMER_AGENT_PRODUCT_PASSPORT_V0_1.md`
- `docs/father_agents/programmer/02_PROGRAMMING_KB_EVIDENCE_MODEL_V0_1.md`
- `docs/father_agents/programmer/03_PROGRAMMING_KB_SOURCE_REGISTER_SEED_2026-08-14.md`
- `docs/father_agents/programmer/04_PROGRAMMING_KB_ROADMAP_V0_1.md`
- `Tree_F/TF-0015_2026-08-14_PROGRAMMER_AGENT_KB_INITIATION.md`
- `docs/journal/J-020_PROGRAMMER_AGENT_KB_TRACK_2026-08-14.md`

#### Modified
- `docs/DEVELOPMENT_JOURNAL.md`

#### Removed
- NONE

#### Renamed / moved
- NONE

### Implementation summary

Documentation and research governance only. No production/runtime code is added.

### Verification / evidence

Verified repository controls before the change:
- `Tree_F` is append-only engineering memory;
- next available TF identifier is TF-0015;
- FATHER current journal keeps M5 Telegram as active critical path;
- FATHER Agent Standard v1 keeps role boundaries narrow and prohibits agents from claiming unsupported truth.

Verified external source statuses on 2026-08-14 are recorded in the source register.

### Result

`PARTIAL`

The track is initialized; coverage matrix, source-card ingestion and evaluation corpus are still pending.

### New / changed risks
- KB may become a citation/link dump instead of executable engineering knowledge.
- source freshness/version drift may silently corrupt recommendations.
- evidence bureaucracy may overwhelm simple tasks.
- uncalibrated numeric confidence could create false precision.
- scope may expand across languages before the decision machinery is proven.

Controls are defined in the evidence model and roadmap.

### Registry changes

New FATHER expert-agent research track: `Programmer Agent / PROGRAMMING_KB`.

### Rollback / replacement path

No runtime coupling exists. The track can be superseded by a later TF record; append-only history remains.

### Next action / next gate

Build the 12-domain coverage matrix from SWEBOK V4.0a and create the first canonical source cards for the MVP Python/backend stack.

---

## RU

### Причина / проблема

FATHER нужен Агент-программист, который получает утверждённые задачи от Архитектора/Аналитика, реализует их и способен доказательно объяснить существенные инженерные решения через источники, альтернативы, риски и результаты проверок.

Обычного coding-LLM недостаточно: количество ссылок не доказывает корректность, знания о версиях устаревают, производительность и надёжность зависят от среды, а популярные архитектурные решения могут лишь добавлять сложность.

### Требование / ТЗ

Создать отдельный исследовательский трек Агента-программиста FATHER и начать PROGRAMMING_KB до написания исполняемого кода агента.

Трек обязан:
- опираться на научные работы, консенсус/учебники, спецификации и проверенную практику;
- хранить точную версию, дату и актуальность источника;
- отличать нормативные/авторитетные источники от вторичных и форумных;
- требовать альтернативы и риски для существенных решений;
- требовать локальный эксперимент/benchmark, если решающий аргумент зависит от конкретной среды;
- хранить отвергнутые варианты и условия их повторного рассмотрения;
- позже интегрироваться с Архитектором, Аналитиком, ИБ, DevSecOps, тестированием и Principal Critic.

### Аналитика / архитектура / ИБ / повторное использование

Действующие правила FATHER уже требуют разработку от требования, reuse-review, приёмочные доказательства и `NO CODE BEFORE CONTRACT`.

Поэтому Агент-программист начинается только как документация и governance базы знаний. Эта запись не разрешает отдельный сервис, микросервис или runtime агента.

Основной материал размещён в `docs/father_agents/programmer/`, а неизменяемая история решения — в `Tree_F`.

Стартовые проверенные опорные источники:
- IEEE Computer Society SWEBOK Guide V4.0a;
- ISO/IEC 25010:2023;
- NIST SP 800-218 SSDF v1.1 FINAL;
- NIST SP 800-218 Rev.1 SSDF v1.2 DRAFT — только наблюдение за изменениями;
- OWASP ASVS 5.0.0;
- SLSA v1.2 APPROVED;
- OpenSSF Scorecard.

ИБ/юридическое правило: материалы источников цитируются и конспектируются в допустимых пределах; полные защищённые авторским правом стандарты и книги в репозиторий не копируются.

Модель доказательств проектируется повторно используемой для будущих Architecture/Security/DevSecOps/Reliability KB, но без насильственного объединения их предметной модели с PROGRAMMING_KB.

### Контракт тестов до кода

До разрешения исполняемого кода Агента-программиста необходимо доказать минимум:
1. один D2-кейс от требования через альтернативы, источники, риски и эксперимент до решения;
2. coverage matrix из 12 доменов с явными пробелами;
3. механизм актуальности и supersession источников;
4. counter-evidence и revisit semantics;
5. evaluation corpus, ловящий citation theater и ненужную сложность.

### Решение

Запустить PROGRAMMING_KB как параллельный исследовательский/продуктовый трек с четырьмя начальными документами: паспорт, модель доказательств, seed-реестр источников и измеримый roadmap.

Текущий критический путь OSINT M5 не меняется.

### ПОЧЕМУ

Наиболее простое безопасное действие — стабилизировать контракт знаний и инженерного решения до строительства очередного runtime. Это не позволит зашить в агента некалиброванные веса доверия, вкусовые предпочтения по фреймворкам или случайное дробление на множество агентов/сервисов.

### Локальная синхронизация / Git-доказательства

Изменение создано через подключённый GitHub workflow в ветке:

```text
agent/programmer-agent-kb-seed
```

После merge локальная Windows-копия синхронизируется по стандартной процедуре Tree_F.

### Изменённые файлы / компоненты

#### Добавлено
- `docs/father_agents/programmer/README.md`
- `docs/father_agents/programmer/01_PROGRAMMER_AGENT_PRODUCT_PASSPORT_V0_1.md`
- `docs/father_agents/programmer/02_PROGRAMMING_KB_EVIDENCE_MODEL_V0_1.md`
- `docs/father_agents/programmer/03_PROGRAMMING_KB_SOURCE_REGISTER_SEED_2026-08-14.md`
- `docs/father_agents/programmer/04_PROGRAMMING_KB_ROADMAP_V0_1.md`
- `Tree_F/TF-0015_2026-08-14_PROGRAMMER_AGENT_KB_INITIATION.md`
- `docs/journal/J-020_PROGRAMMER_AGENT_KB_TRACK_2026-08-14.md`

#### Изменено
- `docs/DEVELOPMENT_JOURNAL.md`

#### Удалено
- НЕТ

#### Переименовано / перемещено
- НЕТ

### Кратко о реализации

Только документы и правила исследовательского трека. Production/runtime-код не добавлялся.

### Проверка / доказательства

Перед изменением подтверждено:
- `Tree_F` является append-only инженерной памятью;
- следующий свободный идентификатор — TF-0015;
- текущий критический путь журнала — M5 Telegram;
- FATHER Agent Standard v1 удерживает узкие роли и не разрешает выдавать неподтверждённые выводы за истину.

Статусы внешних источников, проверенные 2026-08-14, занесены в seed-реестр.

### Результат

`PARTIAL`

Трек создан; coverage matrix, source-card ingestion и evaluation corpus ещё не выполнены.

### Новые / изменённые риски
- база может превратиться в склад ссылок;
- версии источников могут устаревать;
- тяжёлый evidence-процесс может мешать простым задачам;
- некалиброванная confidence-математика создаст ложную точность;
- преждевременное расширение языков размоет MVP.

Контроли определены в evidence model и roadmap.

### Изменения реестров

Новый исследовательский экспертный трек FATHER: `Programmer Agent / PROGRAMMING_KB`.

### Откат / замена

Runtime-связей нет. Направление может быть superseded следующей TF-записью без удаления истории.

### Следующее действие / Gate

Собрать 12-доменную coverage matrix по SWEBOK V4.0a и первые canonical source cards для Python/backend MVP-стека.
