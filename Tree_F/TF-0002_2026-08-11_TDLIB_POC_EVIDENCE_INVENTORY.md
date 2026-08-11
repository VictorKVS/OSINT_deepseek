# TF-0002 — TDLib PoC Evidence Inventory / Инвентаризация доказательств TDLib PoC

```yaml
id: TF-0002
date: 2026-08-11
status: ACTIVE
supersedes: null
superseded_by: null
stage: Stage 07 / M5 Telegram Radar
change_class: POC
old_sha: null
new_sha: null
related_requirements:
  - REQ-M5-001
  - POC-M5-001
related_tests:
  - POC-TD-01
  - POC-TD-02
  - POC-TD-03
  - POC-TD-04
  - POC-TD-05
  - POC-TD-06
  - POC-TD-07
  - POC-TD-08
  - POC-TD-09
  - POC-TD-10
related_adrs: []
related_journal_entries:
  - docs/journal/2026-08-11_TREE_F_APPEND_ONLY_DEVELOPMENT_CORPUS.md
```

## EN

### Trigger / problem

TDLib PoC preparation already contains request builders, authorization handling, a synchronous JSON client, mapping logic, native-library verification and local Windows runtime evidence. The project now needs an evidence inventory before any further implementation so that code is not written for capabilities that are already proven and no capability is incorrectly promoted to PASS based on unit tests alone.

### Requirement / ТЗ

The approved PoC question remains:

> Can TDLib serve as a reliable, replaceable Telegram transport for FATHER OSINT Radar without changing the frozen `ResearchTask → TelegramCollector → Material → MaterialStore` contract?

The approved functional contract is `POC-TD-01` through `POC-TD-10` from `docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md`.

No production integration is authorized by this record.

### Analysis / architecture / security / reuse review

Current architecture remains correct: TDLib-specific code is isolated under `poc/tdlib/`; `father_osint/transports/` remains a protected transport-neutral extension boundary.

Existing implementation evidence reviewed:

- `poc/tdlib/auth.py` — explicit auth-state handling, no credential invention, fail-closed registration handling;
- `poc/tdlib/requests.py` — normalized public-chat request and bounded `getChatHistory` request builder;
- `poc/tdlib/client.py` — correlated synchronous call wrapper, hard timeout, structured TDLib errors, bounded pending-update buffer with observable drop counter;
- `poc/tdlib/mapping.py` — transport-neutral `TelegramMessage` mapping, stable ID requirement, text/caption and selected provenance metadata preservation;
- `poc/tdlib/tdjson_bridge.py` — exact tdjson path/hash verification and recursive sensitive-field redaction;
- `poc/tdlib/run_local.py` — local authorization bootstrap with native-log suppression and duplicate parameter initialization protection;
- unit tests under `tests/test_tdlib_poc_*.py` cover request, auth, timeout/error, buffering and mapping contracts;
- Windows runtime evidence proves the exact local TDLib binary can load and self-report the expected version/commit, but explicitly does not prove live Telegram authorization or collection.

Security/reuse interpretation:

- secrets/session state must remain outside Git;
- tdjson binary provenance is controlled only for the recorded local binary, not globally;
- no TDLib model may leak into the frozen domain contract;
- the acquisition transport remains reusable for multiple lawful research/radar products only if source IDs, message IDs, timestamps and provenance stay transport-neutral.

### Test contract before code

Status categories:

- `PASS` — reproducible evidence satisfies the complete PoC case;
- `PARTIAL` — implementation/unit evidence exists but the complete live/acceptance condition is not proven;
- `NOT TESTED` — no sufficient evidence for the case;
- `REWORK` — current implementation contradicts the approved contract.

Evidence inventory:

| ID | Capability | Current evidence | Status | Gap before PASS |
|---|---|---|---|---|
| POC-TD-01 | Session bootstrap | verified native Windows runtime; auth state machine; secured bootstrap harness; runtime reaches `authorizationStateWaitTdlibParameters` | PARTIAL | controlled live Telegram authorization must reach `authorizationStateReady`; redacted evidence required |
| POC-TD-02 | Public channel resolution | `searchPublicChat` request builder + locator normalization unit test | PARTIAL | live public channel must resolve to stable chat/channel ID and metadata |
| POC-TD-03 | Bounded history read | `getChatHistory` builder hard-bounds one TDLib request to `limit <= 100` | PARTIAL | live bounded history run must return no more than requested application bound and terminate predictably |
| POC-TD-04 | Stable message identity | mapping rejects messages without `chat_id`/`id`; transport-neutral ID mapping unit tests | PARTIAL | same live bounded window must be collected twice and IDs/content hash/provenance compared |
| POC-TD-05 | Restart/checkpoint behaviour | no complete checkpoint/restart evidence | NOT TESTED | Run A / restart / Run B with defined checkpoint/window and gap/replay analysis |
| POC-TD-06 | Invalid channel isolation | structured TDLib error surfaced by client unit test | PARTIAL | invalid source must fail while valid sources continue in one collection run |
| POC-TD-07 | Slow/timeout isolation | hard client timeout unit test | PARTIAL | per-source timeout must be demonstrated without blocking remaining sources or deadlocking |
| POC-TD-08 | Rate-limit/retry visibility | generic TDLib errors are structured; no approved FloodWait/retry evidence | PARTIAL | simulate or observe rate-limit condition; expose structured wait/retry state with bounded policy outside business logic |
| POC-TD-09 | Unicode/long-text integrity | Cyrillic/Unicode mapping unit test and caption preservation test | PARTIAL | live multilingual/long Telegram posts must prove no silent truncation and exact stored-byte hashing |
| POC-TD-10 | DEV v1 regression | frozen DEV v1 baseline was previously proven; TDLib PoC tests exist | PARTIAL | rerun complete current suite and both DEV runners at the current head after PoC changes |

No case is promoted to PASS solely because a request builder or unit test exists.

### Decision

The first mandatory next gate is `POC-TD-01 — controlled live session bootstrap`.

No new feature code is authorized yet. The existing bootstrap harness is sufficient for the next evidence-producing attempt unless analysis of the live run exposes a specific contract defect.

After `POC-TD-01` reaches PASS, proceed in dependency order to `POC-TD-02` and `POC-TD-03` because channel resolution and bounded history are prerequisites for meaningful identity, restart and multi-source tests.

### WHY

Live authorization is the narrowest missing prerequisite for all remaining Telegram-network cases. Adding history, checkpoint or multi-source code before proving a safe authenticated session would expand the PoC without evidence and violate `NO CODE BEFORE CONTRACT`.

The current inventory also distinguishes unit-contract evidence from operational evidence, preventing false confidence.

### Local sync / Git evidence

Before the next local evidence-producing run:

```powershell
cd G:\1\PX00
git status --short
git rev-parse HEAD
git pull
git rev-parse HEAD
git status --short
```

Record the current commit SHA in the live PoC report before authorization.

### Files/components changed

#### Added
- `Tree_F/TF-0002_2026-08-11_TDLIB_POC_EVIDENCE_INVENTORY.md`

#### Modified
- none

#### Removed
- none

#### Renamed / moved
- none

### Implementation summary

Documentation/evidence classification only. No product or PoC runtime code changed.

### Verification / evidence

Reviewed repository evidence includes:

- `docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md`;
- `docs/06_verification/19_TDLIB_WINDOWS_LOCAL_RUNTIME_EVIDENCE_2026-08-11.md`;
- `poc/tdlib/auth.py`;
- `poc/tdlib/client.py`;
- `poc/tdlib/mapping.py`;
- `poc/tdlib/requests.py`;
- `poc/tdlib/tdjson_bridge.py`;
- `poc/tdlib/run_local.py`;
- `tests/test_tdlib_poc_contract.py`;
- `tests/test_tdlib_poc_client.py`;
- `tests/test_tdlib_poc_mapping.py`.

### Result

`PARTIAL`

The PoC has strong preparation and unit-contract evidence, plus verified local native runtime evidence, but no complete live Telegram acquisition case is yet proven.

### New / changed risks

- unit tests may be mistaken for live acceptance evidence;
- live authorization may reveal auth-state/log/session defects not visible in fake-client tests;
- rate-limit/restart/multi-source behavior remains unknown;
- current regression status must be re-proven after subsequent PoC implementation changes.

### Registry changes

No new product opportunity. No security finding is closed by this inventory. Existing M5 states remain active.

### Rollback / replacement path

This record is append-only evidence. If the classification later changes, create a new TF record referencing this one; do not overwrite the historical inventory.

### Next action / next gate

1. synchronize local checkout;
2. prepare only the approved external environment variables/secrets;
3. execute `POC-TD-01` with the already verified tdjson binary/hash;
4. capture only redacted authorization state transitions, current repo SHA, TDLib version/build and final state;
5. if `authorizationStateReady` is reached without secret/session leakage, create the next TF evidence record and mark `POC-TD-01` PASS;
6. if it fails, classify the failure before changing code: requirement gap, environment issue, security issue or implementation defect.

---

## RU

### Причина / проблема

Подготовка PoC TDLib уже содержит построители запросов, обработку авторизации, синхронный JSON-клиент, преобразование Telegram-сообщений, проверку нативной библиотеки и подтверждённый локальный Windows runtime. Перед дальнейшей разработкой нужно провести инвентаризацию доказательств, чтобы не писать повторно то, что уже доказано, и не объявлять `PASS` там, где есть только unit-тест.

### Требование / ТЗ

Утверждённый вопрос PoC остаётся прежним:

> Может ли TDLib быть надёжным и заменяемым Telegram-транспортом FATHER OSINT Radar без изменения замороженного контракта `ResearchTask → TelegramCollector → Material → MaterialStore`?

Функциональный контракт — `POC-TD-01` ... `POC-TD-10` из `docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md`.

Эта запись не разрешает production-интеграцию.

### Аналитика / архитектура / ИБ / повторное использование

Текущая архитектурная граница правильная: весь TDLib-специфичный код остаётся в `poc/tdlib/`, а `father_osint/transports/` остаётся защищённой транспортно-независимой границей.

Проверено существующее доказательство:

- `auth.py` — явная обработка состояний авторизации, отсутствие выдумывания credential, fail-closed для регистрации нового аккаунта;
- `requests.py` — нормализация публичного locator и ограниченный `getChatHistory`;
- `client.py` — correlation ID, жёсткий timeout, структурированные TDLib errors, ограниченный буфер update с видимым счётчиком потерь;
- `mapping.py` — перевод в транспортно-независимый `TelegramMessage`, обязательные стабильные ID, сохранение текста/caption и части provenance metadata;
- `tdjson_bridge.py` — точный путь + SHA-256 для `tdjson` и рекурсивное скрытие чувствительных полей;
- `run_local.py` — локальный auth bootstrap, подавление чувствительных native logs, защита от двойного `setTdlibParameters`;
- `tests/test_tdlib_poc_*.py` — unit-контракты запросов, auth, timeout/error, buffering и mapping;
- Windows runtime evidence доказывает, что конкретная собранная библиотека TDLib загружается и сообщает ожидаемые version/commit, но прямо не доказывает live Telegram authorization и сбор данных.

ИБ/reuse вывод:

- secrets/session остаются вне Git;
- provenance `tdjson` доказан только для конкретной зафиксированной локальной сборки;
- модели TDLib не должны проникать в замороженный доменный контракт;
- транспорт останется повторно используемым для разных законных OSINT/radar продуктов только при сохранении transport-neutral ID и provenance.

### Контракт тестов до кода

Статусы:

- `PASS` — полностью воспроизводимое доказательство всего PoC-case;
- `PARTIAL` — код/unit evidence есть, но полное live/acceptance условие не доказано;
- `NOT TESTED` — достаточного доказательства нет;
- `REWORK` — реализация противоречит утверждённому контракту.

Инвентаризация:

| ID | Возможность | Что уже доказано | Статус | Чего не хватает до PASS |
|---|---|---|---|---|
| POC-TD-01 | Запуск сессии | проверенный Windows runtime; state machine auth; защищённый bootstrap; runtime доходит до `authorizationStateWaitTdlibParameters` | PARTIAL | live Telegram authorization до `authorizationStateReady` + только redacted evidence |
| POC-TD-02 | Разрешение публичного канала | builder `searchPublicChat` и unit-тест нормализации locator | PARTIAL | живой публичный канал должен вернуть стабильный chat/channel ID |
| POC-TD-03 | Ограниченное чтение истории | `getChatHistory` ограничен на один запрос `limit <= 100` | PARTIAL | живой bounded-run: не больше заданного application bound и предсказуемое завершение |
| POC-TD-04 | Стабильность message identity | mapping требует `chat_id` + `id`; unit mapping IDs | PARTIAL | два чтения одного live window и сравнение IDs/hash/provenance |
| POC-TD-05 | Restart/checkpoint | полного доказательства нет | NOT TESTED | Run A → restart → Run B с определённым checkpoint/window и анализом gap/replay |
| POC-TD-06 | Изоляция неверного канала | unit-клиент выдаёт структурированную TDLib error | PARTIAL | неверный источник должен упасть отдельно, а валидные продолжить один общий run |
| POC-TD-07 | Timeout/медленный источник | жёсткий timeout unit-тестом | PARTIAL | доказать per-source timeout без блокировки остальных и deadlock |
| POC-TD-08 | Rate-limit/retry | generic TDLib errors структурированы | PARTIAL | получить/смоделировать rate-limit и доказать structured wait + bounded retry вне business logic |
| POC-TD-09 | Unicode/длинный текст | Cyrillic/Unicode mapping и caption unit-тесты | PARTIAL | live multilingual/long posts без silent truncation + exact stored-byte hash |
| POC-TD-10 | Регрессия DEV v1 | baseline ранее доказан; TDLib PoC unit-тесты есть | PARTIAL | полный текущий `pytest` + оба DEV runner на актуальном head после PoC изменений |

Ни один пункт нельзя переводить в `PASS` только потому, что существует request builder или unit-тест.

### Решение

Первый обязательный следующий Gate — `POC-TD-01 — controlled live session bootstrap`.

Новый feature-code пока не разрешён. Имеющегося bootstrap harness достаточно для следующей попытки получения доказательства, если live-run не выявит конкретный дефект контракта.

После PASS `POC-TD-01` идём по зависимостям: `POC-TD-02`, затем `POC-TD-03`. Без разрешения канала и bounded history бессмысленно переходить к identity, restart и multi-source tests.

### ПОЧЕМУ

Live authorization — самая узкая недостающая предпосылка для всех остальных сетевых Telegram-тестов. Писать history/checkpoint/multi-source код до безопасной рабочей сессии означало бы расширять PoC без доказательств и нарушать `NO CODE BEFORE CONTRACT`.

Инвентаризация также отделяет unit-contract evidence от operational evidence и не позволяет создать ложное ощущение готовности.

### Локальная синхронизация / Git-доказательства

Перед следующим live-run:

```powershell
cd G:\1\PX00
git status --short
git rev-parse HEAD
git pull
git rev-parse HEAD
git status --short
```

Перед авторизацией записать текущий commit SHA в PoC report.

### Изменённые файлы / компоненты

#### Добавлено
- `Tree_F/TF-0002_2026-08-11_TDLIB_POC_EVIDENCE_INVENTORY.md`

#### Изменено
- нет

#### Удалено
- нет

#### Переименовано / перемещено
- нет

### Кратко о реализации

Только классификация документации и доказательств. Код продукта и PoC runtime не изменялся.

### Проверка / доказательства

Проверены:

- `docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md`;
- `docs/06_verification/19_TDLIB_WINDOWS_LOCAL_RUNTIME_EVIDENCE_2026-08-11.md`;
- `poc/tdlib/auth.py`;
- `poc/tdlib/client.py`;
- `poc/tdlib/mapping.py`;
- `poc/tdlib/requests.py`;
- `poc/tdlib/tdjson_bridge.py`;
- `poc/tdlib/run_local.py`;
- `tests/test_tdlib_poc_contract.py`;
- `tests/test_tdlib_poc_client.py`;
- `tests/test_tdlib_poc_mapping.py`.

### Результат

`PARTIAL`

Подготовка PoC сильная: есть unit-contract evidence и подтверждённый локальный native runtime. Но пока не доказан ни один полный live Telegram acquisition case.

### Новые / изменённые риски

- unit-тесты могут ошибочно приниматься за live acceptance evidence;
- live authorization может выявить auth/log/session дефекты, которых не видно на fake-клиенте;
- rate-limit/restart/multi-source остаются неизвестными;
- regression нужно заново доказывать после последующих изменений PoC-кода.

### Изменения реестров

Новой product opportunity нет. Ни один security finding этой инвентаризацией не закрывается. Состояния M5 остаются активными.

### Откат / замена

Запись является append-only evidence. Если классификация изменится, создаётся следующий TF с ссылкой на TF-0002; историческую запись не перезаписываем.

### Следующее действие / Gate

1. синхронизировать локальный checkout;
2. подготовить только утверждённые внешние environment variables/secrets;
3. выполнить `POC-TD-01` на уже проверенной `tdjson` binary/hash;
4. сохранить только redacted auth state transitions, repo SHA, TDLib version/build и финальное состояние;
5. если получен `authorizationStateReady` без утечки secret/session — создать следующий TF evidence record и перевести `POC-TD-01` в PASS;
6. если run падает — сначала классифицировать причину: gap ТЗ, environment, security или defect реализации, и только затем менять код.
