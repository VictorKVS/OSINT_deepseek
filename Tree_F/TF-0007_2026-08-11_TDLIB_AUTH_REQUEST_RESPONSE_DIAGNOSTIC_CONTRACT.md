# TF-0007 — TDLib auth request-response diagnostic contract

```yaml
id: TF-0007
date: 2026-08-11
status: ACTIVE
stage: Stage 07 / M5 — Telegram Radar / POC-TD-01
change_class: TEST
supersedes: null
superseded_by: null
related_requirements: [POC-TD-01]
related_tests: [AUTH-RSP-01, AUTH-RSP-02, AUTH-RSP-03]
related_adrs: []
related_journal_entries: []
```

## EN

### Trigger / problem
A clean TDLib runtime with a fresh database-encryption key reaches `authorizationStateWaitPhoneNumber`, but after `setAuthenticationPhoneNumber` the current harness terminates with a bounded authorization-transition timeout.

Observed live evidence:

```text
authorizationStateWaitTdlibParameters
authorizationStateWaitPhoneNumber
TDLib timed out waiting for authorization transition after setAuthenticationPhoneNumber
```

The previous infinite wait defect is closed. The remaining question is now diagnostic: did `setAuthenticationPhoneNumber` itself return `Ok`, return a TDLib error, or fail to produce a correlated response?

### Requirement / ТЗ
`POC-TD-01 — Session bootstrap` requires a controlled local Telegram authorization reaching `authorizationStateReady`, with failures explicit and bounded and secrets kept outside Git/logs.

### Analysis / architecture / security / reuse review
Official TDLib behavior defines `setAuthenticationPhoneNumber` as a function returning `Ok`. After authorization steps, TDLib emits new authorization-state updates until `authorizationStateReady` is reached.

The current `run_local.py` sends auth requests with the raw bridge `send()` API and waits for authorization updates. This means an `Ok` response to the exact request is not correlated or reported, and diagnosis cannot distinguish:

- request accepted (`Ok`) but no later state update;
- request rejected with a TDLib error;
- no correlated request response within the allowed bound.

The repository already contains `TdJsonClient.call()`, which adds `@extra`, correlates responses, retains unrelated updates, surfaces TDLib errors structurally and provides a hard timeout. The next diagnostic increment should reuse that existing PoC primitive rather than invent a second correlation mechanism.

No product-domain contract change is authorized. No TDLib object may leak into `father_osint` domain semantics.

### Test contract before code

#### AUTH-RSP-01 — correlated Ok
Given `setAuthenticationPhoneNumber` is sent and TDLib returns a correlated `ok`, the diagnostic auth path must observe the `ok` without losing unrelated authorization updates.

#### AUTH-RSP-02 — correlated TDLib error
Given the request returns a correlated TDLib `error`, the harness must terminate explicitly with a redacted/safe diagnostic. No secret-bearing request body may be printed.

#### AUTH-RSP-03 — correlated request timeout
Given no correlated response arrives within the configured request timeout, the harness must terminate explicitly with a bounded timeout identifying the request type, not loop indefinitely.

### Decision
Before changing live authorization behavior, add deterministic tests for the request-response contract. Only after RED evidence is captured may the harness be changed to use the existing correlated `TdJsonClient` primitive for auth requests where technically applicable.

### WHY
Increasing the authorization-state timeout would only wait longer without answering the engineering question. Correlating the function response tells us whether TDLib accepted the phone request and sharply separates transport/network/API failures from state-update handling failures.

### Files/components affected
Expected test scope:

```text
tests/test_tdlib_poc_auth_request_response.py
poc/tdlib/client.py          # reuse, no change expected initially
poc/tdlib/run_local.py       # no implementation change until RED tests exist
```

### Verification / evidence
First gate:

```text
python -m pytest -q tests/test_tdlib_poc_auth_request_response.py
```

Expected pre-fix state: at least one new contract test is RED for the live harness integration while existing `TdJsonClient` unit behavior remains GREEN.

After implementation:

```text
python -m pytest -q tests/test_tdlib_poc_auth_request_response.py
python -m pytest -q
python scripts/run_dev_osint.py
python scripts/run_dev_pipeline.py
```

Then GitHub Actions DEV Verification and CodeQL must be SUCCESS before another live POC-TD-01 run is promoted.

### Result
`PARTIAL`

### New / changed risks
- Longer timeouts can mask a missing request-response diagnostic.
- Logging a raw TDLib auth request/response could expose phone/API/session-related data.
- Consuming correlated responses incorrectly could drop unrelated authorization updates.

### Registry changes
NONE at this test-contract stage.

### Rollback / replacement path
Tests/documentation can be superseded by a later diagnostic contract if TDLib behavior requires a different correlation boundary. Existing frozen product contracts are unaffected.

### Next action / next gate
Create `AUTH-RSP-01..03` tests before modifying `run_local.py`.

---

## RU

### Причина / проблема
На новой чистой TDLib runtime-базе с новым ключом программа уверенно доходит до `authorizationStateWaitPhoneNumber`, но после `setAuthenticationPhoneNumber` заканчивает работу по ограниченному timeout перехода авторизации.

Живое доказательство:

```text
authorizationStateWaitTdlibParameters
authorizationStateWaitPhoneNumber
TDLib timed out waiting for authorization transition after setAuthenticationPhoneNumber
```

Предыдущий дефект бесконечного ожидания уже закрыт. Теперь вопрос другой: вернул ли сам `setAuthenticationPhoneNumber` ответ `Ok`, вернул ли TDLib ошибку, либо коррелированный ответ вообще не пришёл.

### Требование / ТЗ
`POC-TD-01 — Session bootstrap` требует контролируемой локальной авторизации Telegram до `authorizationStateReady`. Ошибки должны быть явными и ограниченными по времени, секреты не должны попадать в Git и обычные логи.

### Аналитика / архитектура / ИБ / повторное использование
По официальному контракту TDLib `setAuthenticationPhoneNumber` является функцией, которая возвращает `Ok`. После шагов авторизации TDLib выдаёт новые обновления состояния до `authorizationStateReady`.

Сейчас `run_local.py` отправляет auth-запросы через обычный `bridge.send()` и ждёт только обновления состояния. Поэтому ответ именно на конкретный запрос не коррелируется и не показывается. Мы не можем различить три ситуации:

- запрос принят (`Ok`), но следующее auth-state не пришло;
- TDLib отклонил запрос с ошибкой;
- коррелированный ответ на запрос не пришёл в установленный срок.

В PoC уже есть `TdJsonClient.call()`: он добавляет `@extra`, связывает ответ с запросом, сохраняет посторонние updates, явно поднимает TDLib error и имеет жёсткий timeout. Следующий диагностический шаг должен переиспользовать этот механизм, а не создавать второй.

Доменные контракты продукта не меняем. TDLib-объекты не должны попадать выше транспортной границы.

### Контракт тестов до кода

#### AUTH-RSP-01 — коррелированный Ok
Если на `setAuthenticationPhoneNumber` приходит связанный ответ `ok`, диагностический auth-путь обязан его увидеть и не потерять посторонние auth-updates.

#### AUTH-RSP-02 — коррелированная TDLib-ошибка
Если на запрос приходит связанный `error`, harness должен завершиться явно и безопасно, без печати секретного тела запроса.

#### AUTH-RSP-03 — timeout ответа запроса
Если связанный ответ не приходит за установленное время, harness должен завершиться по bounded timeout с указанием типа запроса, а не ждать бесконечно.

### Решение
До изменения живой авторизации сначала добавить детерминированные тесты контракта request-response. Только после получения RED-доказательства разрешается менять harness и подключать уже существующий `TdJsonClient` для auth-запросов там, где это технически корректно.

### ПОЧЕМУ
Простое увеличение timeout заставит нас лишь дольше ждать и не ответит, принял ли TDLib номер. Корреляция ответа функции сразу разделяет проблемы API/номера/сети и проблемы обработки последующего auth-state.

### Изменённые файлы / компоненты
Ожидаемая область:

```text
tests/test_tdlib_poc_auth_request_response.py
poc/tdlib/client.py          # переиспользуем, сначала без изменения
poc/tdlib/run_local.py       # не меняем до RED-тестов
```

### Проверка / доказательства
Первый Gate:

```text
python -m pytest -q tests/test_tdlib_poc_auth_request_response.py
```

До исправления ожидаем хотя бы один RED-тест интеграции harness, при этом существующие unit-тесты `TdJsonClient` должны оставаться GREEN.

После реализации:

```text
python -m pytest -q tests/test_tdlib_poc_auth_request_response.py
python -m pytest -q
python scripts/run_dev_osint.py
python scripts/run_dev_pipeline.py
```

После этого обязательны SUCCESS в GitHub Actions DEV Verification и CodeQL, и только затем новый живой запуск POC-TD-01.

### Результат
`PARTIAL`

### Новые / изменённые риски
- увеличение timeout может скрыть отсутствие диагностики ответа запроса;
- вывод сырого auth-запроса/ответа TDLib может раскрыть чувствительные данные;
- неправильная корреляция может потерять посторонние auth-updates.

### Изменения реестров
NONE на этапе test contract.

### Откат / замена
Тестовый контракт может быть superseded следующим документом, если фактическое поведение TDLib потребует другой границы корреляции. Замороженный продуктовый контракт не затрагивается.

### Следующее действие / Gate
Создать тесты `AUTH-RSP-01..03` до изменения `run_local.py`.
