# TF-0004 — TDLib authorization transition test contract

```yaml
id: TF-0004
date: 2026-08-11
status: ACTIVE
supersedes: null
superseded_by: null
stage: Stage 07 / M5 Telegram Radar / POC-TD-01
change_class: TEST
related_requirements: [POC-TD-01]
related_tests: [AUTH-01, AUTH-02, AUTH-03]
related_adrs: []
related_journal_entries: [TF-0003]
```

## EN

### Trigger / problem
Live TDLib authorization reproducibly reaches `authorizationStateWaitPhoneNumber` and then can remain in the receive loop indefinitely after a locally supplied phone number.

### Requirement / ТЗ
`POC-TD-01` requires bounded, observable session bootstrap to `authorizationStateReady`, with explicit failures and no secret leakage.

### Analysis / architecture / security / reuse review
The existing PoC already has a correlation-aware bounded `TdJsonClient.call()` facade, while `run_local.py` currently sends authorization requests directly through the bridge and then waits for authorization-state updates. The live run proves the post-phone transition is not bounded. The fix must remain inside the PoC harness and must not change frozen FATHER domain contracts.

### Test contract before code

**AUTH-01 — bounded post-phone transition**

Given the harness has reached `authorizationStateWaitPhoneNumber` and has sent `setAuthenticationPhoneNumber`, when no further TDLib response/state arrives, then the harness must terminate with an explicit bounded timeout instead of waiting forever.

**AUTH-02 — explicit TDLib error**

Given TDLib returns an error after the phone-number request, the harness must terminate explicitly and must not expose secret-bearing request values.

**AUTH-03 — successful transition remains supported**

Given TDLib advances from `authorizationStateWaitPhoneNumber` to a later authorization state, the harness must continue processing that state rather than treating the transition as a failure.

### Decision
Add regression tests against the current harness before implementation changes. The tests must use a fake bridge and deterministic responses; no live Telegram credentials are used in unit tests.

### WHY
A live hang is insufficient as a permanent regression guard. The expected bounded behavior must be executable and repeatable in CI before the implementation is changed.

### Files/components changed

#### Added
- `Tree_F/TF-0004_2026-08-11_TDLIB_AUTH_TRANSITION_TEST_CONTRACT.md`
- `tests/test_tdlib_poc_auth_transition.py`

#### Modified
- NONE at test-contract stage.

### Verification / evidence
Expected RED step:

```text
python -m pytest -q tests/test_tdlib_poc_auth_transition.py
```

At least `AUTH-01` must fail against the pre-fix harness, demonstrating that no bounded post-phone transition timeout exists.

### Result
`PARTIAL` — contract defined; RED execution evidence pending.

### New / changed risks
- A naive timeout fix could hide a real TDLib error or race with a legitimate slow transition.
- Authorization secrets must not enter assertion output or logs.

### Registry changes
NONE.

### Rollback / replacement path
Test-only change can be reverted without product impact. Any later implementation must remain isolated under `poc/tdlib/`.

### Next action / next gate
Run the new test file and capture RED evidence. Only after RED is confirmed may the minimal harness implementation be changed.

---

## RU

### Причина / проблема
Живой запуск TDLib воспроизводимо доходит до `authorizationStateWaitPhoneNumber`, после чего при уже переданном локальном номере может бесконечно оставаться в цикле `receive()`.

### Требование / ТЗ
`POC-TD-01` требует ограниченный по времени и наблюдаемый запуск сессии до `authorizationStateReady`, с явными ошибками и без утечки секретов.

### Аналитика / архитектура / ИБ / повторное использование
В PoC уже есть `TdJsonClient.call()` с корреляцией запроса/ответа и timeout. Но `run_local.py` авторизационные запросы отправляет напрямую через bridge и затем ждёт новые состояния авторизации. Живой тест доказал, что переход после номера сейчас не ограничен по времени. Исправление должно остаться внутри PoC и не менять замороженные доменные контракты FATHER.

### Контракт тестов до кода

**AUTH-01 — ограниченный переход после номера**

Если harness дошёл до `authorizationStateWaitPhoneNumber`, отправил `setAuthenticationPhoneNumber`, но дальнейшего ответа/состояния нет, программа обязана завершиться по явному timeout, а не ждать бесконечно.

**AUTH-02 — явная ошибка TDLib**

Если TDLib возвращает ошибку после запроса номера, harness должен завершиться явно и не раскрывать чувствительные значения запроса.

**AUTH-03 — успешный переход не ломается**

Если TDLib после `authorizationStateWaitPhoneNumber` переходит в следующее состояние авторизации, harness должен продолжить его обработку, а не считать переход ошибкой.

### Решение
До изменения реализации добавить регрессионные тесты существующего harness. Тесты используют fake bridge и детерминированные ответы; реальные Telegram credentials в unit-тестах не используются.

### ПОЧЕМУ
Живого зависания недостаточно как постоянного доказательства. Ожидаемое bounded-поведение должно быть исполнимым и воспроизводимым в CI до исправления реализации.

### Изменённые файлы / компоненты

#### Добавлено
- `Tree_F/TF-0004_2026-08-11_TDLIB_AUTH_TRANSITION_TEST_CONTRACT.md`
- `tests/test_tdlib_poc_auth_transition.py`

#### Изменено
- НИЧЕГО на этапе test contract.

### Проверка / доказательства
Ожидаемый RED-шаг:

```text
python -m pytest -q tests/test_tdlib_poc_auth_transition.py
```

Как минимум `AUTH-01` должен упасть на текущем harness и тем самым доказать отсутствие bounded timeout после отправки номера.

### Результат
`PARTIAL` — контракт определён; RED-доказательство ещё нужно получить.

### Новые / изменённые риски
- Наивное добавление timeout может скрыть реальную TDLib-ошибку или конфликтовать с легитимно медленным переходом.
- Секреты авторизации не должны попадать в вывод assertion/log.

### Изменения реестров
NONE.

### Откат / замена
Тестовую запись можно откатить без влияния на продукт. Последующее исправление остаётся только в `poc/tdlib/`.

### Следующее действие / Gate
Запустить новый тестовый файл и получить RED-доказательство. Только после подтверждённого RED разрешено минимально менять harness.
