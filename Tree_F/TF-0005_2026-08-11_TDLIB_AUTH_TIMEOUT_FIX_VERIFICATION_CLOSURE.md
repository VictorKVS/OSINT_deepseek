# TF-0005 — TDLIB AUTH TIMEOUT FIX VERIFICATION CLOSURE

```yaml
id: TF-0005
date: 2026-08-11
status: PASS
supersedes: null
superseded_by: null
stage: Stage 07 / M5 — Telegram Radar / TDLib PoC
change_class: TEST / CODE / DEFECT / VERIFICATION
old_sha: 53e4792
new_sha: 713bb6f
related_requirements: [REQ-M5-001, POC-TD-01]
related_tests: [AUTH-01, AUTH-02, AUTH-03]
related_adrs: []
related_journal_entries: [TF-0003, TF-0004]
```

## EN

### Trigger / problem
Live TDLib authorization reproducibly stalled after `authorizationStateWaitPhoneNumber`. The local harness could wait indefinitely after `setAuthenticationPhoneNumber`, violating the bounded-execution requirement of the M5 PoC.

### Requirement / ТЗ
`POC-TD-01 — Session bootstrap` requires controlled local authorization. M5 additionally requires bounded failure and explicit error handling; an auth transition must not hang indefinitely.

### Analysis / architecture / security / reuse review
The failure was isolated to the PoC harness. The frozen `TelegramCollector` and FATHER domain contracts were not changed. The remediation remained inside `poc/tdlib/run_local.py` and test code.

The defect was reproduced both with interactive input and with `TELEGRAM_PHONE_NUMBER` supplied through the environment, proving that the failure was not caused by `getpass` input handling.

The production-side fix introduced a bounded authorization-transition receive budget. A secondary Windows-only regression failure was then identified in a path assertion and corrected in test code only.

No TDLib-specific model was introduced into upper product layers.

### Test contract before code
The approved pre-code contract was:

- `AUTH-01`: after `setAuthenticationPhoneNumber`, lack of progress must terminate explicitly by timeout rather than loop forever;
- `AUTH-02`: a TDLib authorization error must terminate explicitly and safely;
- `AUTH-03`: a successful authorization-state transition must remain processable.

### Decision
Close the unbounded authorization-transition defect as fixed and verified.

Keep `POC-TD-01` itself open until a live Telegram session reaches `authorizationStateReady`.

### WHY
A bounded failure is a prerequisite for a reliable transport. Converting an indefinite hang into an explicit timeout improves diagnosability and prevents one authorization request from blocking the PoC indefinitely without changing product architecture.

### Files/components changed

#### Added
- `Tree_F/TF-0003_2026-08-11_TDLIB_AUTH_TRANSITION_TIMEOUT_DEFECT.md`
- `Tree_F/TF-0004_2026-08-11_TDLIB_AUTH_TRANSITION_TEST_CONTRACT.md`
- `tests/test_tdlib_poc_auth_transition.py`

#### Modified
- `poc/tdlib/run_local.py`
- `tests/test_tdlib_poc_auth_transition.py`
- `tests/test_tdlib_poc_contract.py`

#### Removed
- NONE

#### Renamed / moved
- NONE

### Implementation summary
`run_local.py` now applies a bounded authorization transition budget after secret-bearing auth requests. If no new authorization state or explicit TDLib error appears before the budget is exhausted, the harness exits with a diagnostic `SystemExit` instead of waiting indefinitely.

Invalid `TELEGRAM_API_ID` input now also fails with a controlled message rather than an unhandled Python traceback.

The Windows path assertion was made platform-neutral without changing production behavior.

### Verification / evidence
RED evidence:

```text
FAILED tests/test_tdlib_poc_auth_transition.py::test_auth_01_post_phone_transition_is_bounded
RuntimeError: TEST_GUARD_UNBOUNDED_RECEIVE
1 failed, 2 passed
```

After the production fix, the test guard itself was found to trigger too early relative to the deterministic receive budget. The guard was corrected without changing production code.

Targeted GREEN evidence:

```text
python -m pytest -q tests/test_tdlib_poc_auth_transition.py
3 passed in 1.16s
```

Windows regression observation before portability correction:

```text
44 passed, 1 failed
```

The only failure was a path separator assertion (`runtime/tdlib/db` versus Windows `runtime\\tdlib\\db`). The test was corrected to use platform-neutral `Path(...).parts` semantics.

Local DEV runner evidence:

```text
python scripts/run_dev_osint.py
errors=0
stop_reason=collectors_exhausted

python scripts/run_dev_pipeline.py
pipeline_stop=review_passed
socrates=PASS
```

GitHub Actions external verification for commit `713bb6fca420b0e6d1ed7c9a7abca6a01f8fe295`:

- `Stage 06 DEV Verification`: SUCCESS;
- `Security CodeQL`: SUCCESS.

The GitHub DEV workflow runs a clean Ubuntu / Python 3.12 checkout and executes package import, pytest collection, full pytest, `run_dev_osint.py`, and `run_dev_pipeline.py`.

### Result
`PASS`

The unbounded auth-transition defect is closed.

`POC-TD-01` remains `PARTIAL` because live `authorizationStateReady` evidence is still required.

### New / changed risks
- Risk of an indefinite post-auth-request receive loop: CONTROLLED for the current PoC harness.
- Platform-specific test assertion risk: CONTROLLED by platform-neutral path checks.
- Telegram connectivity / account / network transition after phone submission: still requires live evidence.

### Registry changes
No product capability promoted.

PoC defect state: CLOSED / CONTROLLED.

`POC-TD-01`: remains PARTIAL pending live ready-state evidence.

### Rollback / replacement path
The timeout behavior is isolated in the PoC harness and can be superseded by a future correlated asynchronous request/state controller without changing FATHER domain contracts.

### Next action / next gate
Repeat the controlled live `POC-TD-01` authorization using the verified local TDLib binary and external secrets.

Expected outcomes are now bounded:

1. transition to `authorizationStateWaitCode`, `authorizationStateWaitEmailCode`, `authorizationStateWaitPassword` or `authorizationStateReady`;
2. explicit TDLib error;
3. explicit authorization-transition timeout.

Do not advance to `POC-TD-02` until `authorizationStateReady` is demonstrated.

---

## RU

### Причина / проблема
Живая авторизация TDLib воспроизводимо останавливалась после `authorizationStateWaitPhoneNumber`. Локальный harness мог бесконечно ждать после `setAuthenticationPhoneNumber`, что нарушало обязательное требование M5 о bounded execution — ограниченном и объяснимом завершении операции.

### Требование / ТЗ
`POC-TD-01 — Session bootstrap` требует контролируемой локальной авторизации. M5 также требует ограниченного поведения при отказах и явной обработки ошибок: переход авторизации не должен зависать бесконечно.

### Аналитика / архитектура / ИБ / повторное использование
Проблема была локализована внутри PoC harness. Замороженные `TelegramCollector` и доменные контракты FATHER не менялись. Исправление осталось внутри `poc/tdlib/run_local.py` и тестов.

Дефект был воспроизведён как при интерактивном вводе номера, так и при передаче `TELEGRAM_PHONE_NUMBER` через переменную окружения. Это доказало, что причина не в `getpass`.

В рабочем PoC-коде был добавлен ограниченный budget ожидания перехода состояния авторизации. После этого обнаружился отдельный Windows-only FAIL в тесте пути; он был исправлен только в тестовом коде.

TDLib-специфичные модели в верхние продуктовые слои не попали.

### Контракт тестов до кода
До исправления были утверждены следующие тесты:

- `AUTH-01`: после `setAuthenticationPhoneNumber` отсутствие прогресса должно завершаться явным timeout, а не бесконечным циклом;
- `AUTH-02`: ошибка TDLib при авторизации должна завершаться явно и безопасно;
- `AUTH-03`: успешный переход состояния авторизации должен продолжать нормально обрабатываться.

### Решение
Закрыть дефект бесконечного ожидания перехода авторизации как исправленный и подтверждённый тестами.

При этом сам `POC-TD-01` не закрываем, пока живая Telegram-сессия не достигнет `authorizationStateReady`.

### ПОЧЕМУ
Ограниченное завершение при отказе — обязательное свойство надёжного транспорта. Замена бесконечного зависания на явный timeout улучшает диагностику и не позволяет одному auth-запросу блокировать PoC бесконечно, при этом архитектура продукта не меняется.

### Изменённые файлы / компоненты

#### Добавлено
- `Tree_F/TF-0003_2026-08-11_TDLIB_AUTH_TRANSITION_TIMEOUT_DEFECT.md`
- `Tree_F/TF-0004_2026-08-11_TDLIB_AUTH_TRANSITION_TEST_CONTRACT.md`
- `tests/test_tdlib_poc_auth_transition.py`

#### Изменено
- `poc/tdlib/run_local.py`
- `tests/test_tdlib_poc_auth_transition.py`
- `tests/test_tdlib_poc_contract.py`

#### Удалено
- НИЧЕГО

#### Переименовано / перемещено
- НИЧЕГО

### Кратко о реализации
`run_local.py` теперь включает ограниченный budget ожидания перехода авторизации после отправки auth-запросов. Если до исчерпания budget не появляется новое состояние авторизации или явная ошибка TDLib, harness завершается диагностическим `SystemExit`, а не ждёт бесконечно.

Некорректный `TELEGRAM_API_ID` теперь также обрабатывается понятным сообщением без необработанного Python traceback.

Windows-проверка пути сделана кроссплатформенной без изменения production-поведения.

### Проверка / доказательства
RED-доказательство:

```text
FAILED tests/test_tdlib_poc_auth_transition.py::test_auth_01_post_phone_transition_is_bounded
RuntimeError: TEST_GUARD_UNBOUNDED_RECEIVE
1 failed, 2 passed
```

После исправления production-кода выяснилось, что тестовый guard сам срабатывал раньше предусмотренного детерминированного receive-budget. Guard был исправлен без изменения production-кода.

Целевой GREEN:

```text
python -m pytest -q tests/test_tdlib_poc_auth_transition.py
3 passed in 1.16s
```

Windows-регрессия до исправления переносимости:

```text
44 passed, 1 failed
```

Единственный FAIL был связан со слэшами пути (`runtime/tdlib/db` против Windows `runtime\\tdlib\\db`). Тест переведён на кроссплатформенную проверку через `Path(...).parts`.

Локальные DEV-runner:

```text
python scripts/run_dev_osint.py
errors=0
stop_reason=collectors_exhausted

python scripts/run_dev_pipeline.py
pipeline_stop=review_passed
socrates=PASS
```

Внешняя проверка GitHub Actions для коммита `713bb6fca420b0e6d1ed7c9a7abca6a01f8fe295`:

- `Stage 06 DEV Verification`: SUCCESS;
- `Security CodeQL`: SUCCESS.

GitHub DEV workflow выполняется на чистом Ubuntu / Python 3.12 и запускает импорт пакета, сбор pytest, полный pytest, `run_dev_osint.py` и `run_dev_pipeline.py`.

### Результат
`PASS`

Дефект бесконечного ожидания auth-перехода закрыт.

`POC-TD-01` остаётся `PARTIAL`, потому что ещё требуется живое доказательство `authorizationStateReady`.

### Новые / изменённые риски
- Риск бесконечного receive-loop после auth-запроса: КОНТРОЛИРУЕТСЯ для текущего PoC harness.
- Риск платформенно-зависимых assertions в тестах: КОНТРОЛИРУЕТСЯ кроссплатформенной проверкой пути.
- Переход Telegram после отправки номера — сеть / аккаунт / серверная реакция — всё ещё требует живого доказательства.

### Изменения реестров
Новая продуктовая возможность не утверждается.

Состояние PoC-дефекта: CLOSED / CONTROLLED.

`POC-TD-01`: остаётся PARTIAL до живого ready-state.

### Откат / замена
Timeout-поведение изолировано в PoC harness и в будущем может быть заменено полноценным коррелированным async request/state controller без изменения доменных контрактов FATHER.

### Следующее действие / Gate
Повторить контролируемый живой `POC-TD-01` с проверенным локальным TDLib binary и секретами вне Git.

Теперь возможные результаты ограничены и диагностируемы:

1. переход в `authorizationStateWaitCode`, `authorizationStateWaitEmailCode`, `authorizationStateWaitPassword` или `authorizationStateReady`;
2. явная ошибка TDLib;
3. явный timeout перехода авторизации.

До доказанного `authorizationStateReady` к `POC-TD-02` не переходим.
