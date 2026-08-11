# TF-0003 — TDLib authentication transition timeout defect

```yaml
id: TF-0003
date: 2026-08-11
status: ACTIVE
supersedes: null
superseded_by: null
stage: Stage 07 / M5 — Telegram Radar / TDLib PoC
change_class: DEFECT
old_sha: 5d0ecb9e7bdad86f26d7da05b53af06c9bc393a5
new_sha: null
related_requirements:
  - POC-TD-01
related_tests:
  - planned: auth request response correlation
  - planned: bounded auth state transition timeout
related_adrs: []
related_journal_entries:
  - docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md
  - Tree_F/TF-0002_2026-08-11_TDLIB_POC_EVIDENCE_INVENTORY.md
```

## EN

### Trigger / problem
A controlled live TDLib authorization run reached `authorizationStateWaitPhoneNumber` successfully using the verified Windows `tdjson.dll`, external API credentials, external database key and local runtime directory.

After `setAuthenticationPhoneNumber` was sent, no next authorization state or explicit request result became visible to the harness. The process remained in the receive loop until manually interrupted.

The behavior reproduced both with interactive hidden phone input and with `TELEGRAM_PHONE_NUMBER` supplied through the local environment.

### Requirement / ТЗ
`POC-TD-01 — Session bootstrap` requires the PoC to reach an authenticated ready state with bounded, observable behavior and without leaking secrets.

The M5 transport PoC also requires bounded execution and explicit failures. An indefinitely waiting authorization transition is therefore a contract defect even if the underlying cause is external network behavior.

### Analysis / architecture / security / reuse review
Official TDLib documentation states that `authorizationStateWaitPhoneNumber` requires the application to call `setAuthenticationPhoneNumber`. That function returns `Ok` on success, while authorization then progresses through subsequent authorization-state updates such as `authorizationStateWaitCode` before eventually reaching `authorizationStateReady`.

The current `run_local.py` sends authorization requests directly through `TdJsonBridge.send()` and then waits only for later authorization-state updates. It does not correlate and observe the direct response to `setAuthenticationPhoneNumber`.

Therefore the current harness cannot distinguish at least three materially different cases:

1. request returned `Ok`, but the next authorization-state update is delayed or blocked;
2. request returned a TDLib error that is not surfaced as the correlated response expected by the harness;
3. network/runtime progress stalled and no response/update arrives.

The repository already contains `TdJsonClient.call()`, which provides request correlation, explicit TDLib error surfacing and a hard timeout. The defect should be corrected by reusing that PoC primitive rather than creating a second request/timeout mechanism.

Security impact: failure diagnosis must not increase native TDLib verbosity to a level that can expose `api_hash`, phone number, authentication code, password or database-encryption key. Any new diagnostic output must remain redacted.

Reuse impact: bounded request/result handling is transport-runtime infrastructure and should remain isolated inside the PoC transport layer; no FATHER domain contract change is justified.

### Test contract before code
Before changing implementation, define tests that prove:

1. an auth request response is correlated and an `Ok` result is observable;
2. a TDLib `error` response is surfaced explicitly and safely;
3. if neither a request response nor required next authorization state appears within the configured deadline, the harness exits with a bounded diagnostic instead of waiting forever;
4. sensitive fields remain redacted;
5. existing TDLib PoC tests and frozen DEV v1 regression remain green.

### Decision
Do not repeat uncontrolled live authorization attempts.

Treat the reproduced behavior as a PoC defect and pause `POC-TD-01` at `PARTIAL` until response correlation and bounded auth-transition behavior are proven by tests and then implemented minimally.

### WHY
The system must not infer success or failure from silence. A production-quality transport candidate needs explicit request outcomes and bounded failure behavior. Reusing the existing `TdJsonClient.call()` is simpler and more consistent than adding ad-hoc waiting logic to `run_local.py`.

### Local sync / Git evidence
Observed working copy before this record:

```text
repository: G:\1\OSINT_deepseek_poc
branch: main
HEAD: 5d0ecb9e7bdad86f26d7da05b53af06c9bc393a5
working tree: clean
```

Observed live sequence:

```text
Created managed client
TDLib PoC local bootstrap started
verified tdjson SHA-256
authorizationStateWaitTdlibParameters
authorizationStateWaitPhoneNumber
<no bounded observable next result/state>
```

No credentials, phone number, authentication code, password or database key are stored in this record.

### Files/components changed

#### Added
- `Tree_F/TF-0003_2026-08-11_TDLIB_AUTH_TRANSITION_TIMEOUT_DEFECT.md`

#### Modified
- NONE

#### Removed
- NONE

#### Renamed / moved
- NONE

### Implementation summary
No product or PoC runtime code changed in this step. This record captures the defect, analysis and test contract before code.

### Verification / evidence
Evidence is the reproduced local live-auth behavior plus existing repository contracts in:

- `poc/tdlib/run_local.py`
- `poc/tdlib/client.py`
- `tests/test_tdlib_poc_client.py`
- `docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md`

Official TDLib API documentation was checked for `authorizationStateWaitPhoneNumber`, `setAuthenticationPhoneNumber` and the authorization flow.

### Result
`PARTIAL`

### New / changed risks
- unbounded authorization wait can make PoC execution hang indefinitely;
- direct request failures may be diagnostically ambiguous when request responses are not correlated;
- increasing TDLib logging to debug this defect could leak secrets and is prohibited;
- external Telegram connectivity may still be the underlying runtime cause and must be distinguished from harness defects.

### Registry changes
No product-registry change. Keep `POC-TD-01` in `PARTIAL` state.

### Rollback / replacement path
This record is append-only. If later analysis disproves the diagnosis, create a new TF record and supersede this one rather than rewriting the history.

### Next action / next gate
1. add tests for auth request correlation and bounded state-transition timeout;
2. run those tests and confirm they fail for the missing behavior;
3. implement the minimum harness change using the existing `TdJsonClient.call()` or an equivalent single bounded abstraction;
4. run TDLib PoC tests plus full frozen DEV v1 regression;
5. retry one controlled live authorization run;
6. only then decide whether `POC-TD-01` can become `PASS`.

---

## RU

### Причина / проблема
Контролируемый живой запуск TDLib успешно дошёл до `authorizationStateWaitPhoneNumber` с проверенным Windows `tdjson.dll`, локально заданными API-данными, внешним ключом базы и отдельным runtime-каталогом.

После отправки `setAuthenticationPhoneNumber` harness не показал ни следующего состояния авторизации, ни явного результата самого запроса. Процесс остался в цикле ожидания до ручного прерывания.

Поведение воспроизвелось и при скрытом интерактивном вводе номера, и при передаче `TELEGRAM_PHONE_NUMBER` через локальную переменную окружения.

### Требование / ТЗ
`POC-TD-01 — Session bootstrap` требует, чтобы PoC дошёл до authenticated ready state, работал ограниченно по времени, был наблюдаемым и не раскрывал секреты.

В M5 также прямо требуется bounded execution и явные ошибки. Поэтому бесконечное ожидание перехода авторизации — дефект контракта независимо от того, вызвана ли первопричина нашей обвязкой или внешней сетью.

### Аналитика / архитектура / ИБ / повторное использование
По официальной документации TDLib состояние `authorizationStateWaitPhoneNumber` требует вызвать `setAuthenticationPhoneNumber`. Этот вызов возвращает `Ok` при успехе, после чего авторизация продолжается через последующие состояния, например `authorizationStateWaitCode`, и в итоге должна прийти к `authorizationStateReady`.

Текущий `run_local.py` отправляет auth-запросы напрямую через `TdJsonBridge.send()` и затем ждёт только будущие auth-state updates. Он не связывает запрос `setAuthenticationPhoneNumber` с прямым ответом на этот запрос.

Из-за этого сейчас невозможно отличить как минимум три разных случая:

1. запрос вернул `Ok`, но следующее состояние задерживается или блокируется;
2. запрос вернул TDLib-ошибку, но harness не показал её как коррелированный ответ;
3. сеть/runtime зависли и вообще не пришло ни ответа, ни следующего update.

В репозитории уже есть `TdJsonClient.call()`, который умеет коррелировать запрос/ответ, явно поднимать TDLib error и имеет жёсткий timeout. Поэтому исправление должно переиспользовать этот PoC-примитив, а не создавать второй механизм ожидания.

ИБ: для диагностики нельзя повышать нативный TDLib log level до уровня, где могут появиться `api_hash`, номер телефона, код входа, пароль или ключ БД. Новый диагностический вывод должен оставаться redacted.

Повторное использование: bounded request/result handling — инфраструктура transport/runtime и должна оставаться внутри PoC transport layer. Менять доменный контракт FATHER для этого не нужно.

### Контракт тестов до кода
До изменения реализации должны появиться тесты, доказывающие:

1. auth-запрос коррелируется, а ответ `Ok` наблюдаем;
2. TDLib `error` явно и безопасно выводится;
3. если ни ответ на запрос, ни нужное следующее состояние не пришли в заданный срок, harness завершается ограниченной диагностикой вместо бесконечного ожидания;
4. чувствительные поля остаются скрыты;
5. существующие TDLib PoC-тесты и замороженный DEV v1 остаются зелёными.

### Решение
Не повторяем бесконтрольные live-authorization запуски.

Считаем поведение воспроизводимым дефектом PoC и оставляем `POC-TD-01` в состоянии `PARTIAL`, пока response correlation и bounded auth-transition не будут сначала доказаны тестами, а затем реализованы минимальным изменением.

### ПОЧЕМУ
Система не должна угадывать успех или ошибку по молчанию. Кандидат production transport обязан иметь явный результат запроса и ограниченное поведение при отказе. Переиспользовать существующий `TdJsonClient.call()` проще и архитектурно чище, чем добавлять ещё один самодельный timeout в `run_local.py`.

### Локальная синхронизация / Git-доказательства
Рабочее состояние перед этой записью:

```text
repository: G:\1\OSINT_deepseek_poc
branch: main
HEAD: 5d0ecb9e7bdad86f26d7da05b53af06c9bc393a5
working tree: clean
```

Наблюдаемая последовательность live-run:

```text
Created managed client
TDLib PoC local bootstrap started
verified tdjson SHA-256
authorizationStateWaitTdlibParameters
authorizationStateWaitPhoneNumber
<дальше нет ограниченного по времени явного результата/состояния>
```

Секреты, номер телефона, коды, пароль и ключ БД в запись не включены.

### Изменённые файлы / компоненты

#### Добавлено
- `Tree_F/TF-0003_2026-08-11_TDLIB_AUTH_TRANSITION_TIMEOUT_DEFECT.md`

#### Изменено
- НЕТ

#### Удалено
- НЕТ

#### Переименовано / перемещено
- НЕТ

### Кратко о реализации
Код продукта и PoC runtime на этом шаге не менялся. Сначала зафиксированы дефект, аналитика и контракт тестов.

### Проверка / доказательства
Доказательства: воспроизведённый live-auth сценарий и существующие файлы:

- `poc/tdlib/run_local.py`
- `poc/tdlib/client.py`
- `tests/test_tdlib_poc_client.py`
- `docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md`

Также сверена официальная документация TDLib по `authorizationStateWaitPhoneNumber`, `setAuthenticationPhoneNumber` и общему auth flow.

### Результат
`PARTIAL`

### Новые / изменённые риски
- ожидание авторизации может зависнуть без ограничения времени;
- ошибка прямого TDLib-запроса может быть диагностически неотличима от сетевого зависания без correlation;
- попытка повысить verbosity TDLib для диагностики может раскрыть секреты и запрещена;
- первопричиной всё ещё может быть внешняя доступность Telegram, и её нужно отделить от дефекта harness.

### Изменения реестров
Изменений Product Registry нет. `POC-TD-01` остаётся `PARTIAL`.

### Откат / замена
Запись append-only. Если дальнейшая проверка опровергнет гипотезу, создаём новый TF-файл и связываем его через supersede, а не переписываем историю.

### Следующее действие / Gate
1. добавить тесты response correlation и bounded state-transition timeout;
2. запустить их и убедиться, что отсутствующее поведение выявляется тестом;
3. реализовать минимальное исправление на базе существующего `TdJsonClient.call()` или единой эквивалентной bounded abstraction;
4. прогнать TDLib PoC tests и полный frozen DEV v1 regression;
5. выполнить один контролируемый повторный live authorization run;
6. только после этого решать, переводить ли `POC-TD-01` в `PASS`.
