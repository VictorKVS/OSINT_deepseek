# TF-0008 — TDLib connection-state diagnostic test contract

```yaml
id: TF-0008
date: 2026-08-11
status: ACTIVE
supersedes: null
superseded_by: null
stage: Stage 07 / M5 — Telegram Radar / TDLib PoC
change_class: TEST
old_sha: 0e5daf22aa082c57e73d8a860aaccbb819a1c1d9
new_sha: pending
related_requirements:
  - POC-TD-01
related_tests:
  - AUTH-NET-01
  - AUTH-NET-02
related_adrs: []
related_journal_entries:
  - TF-0007
```

## EN

### Trigger / problem
The live PoC now proves that `setTdlibParameters` returns `ok`, but `setAuthenticationPhoneNumber` times out waiting for its correlated response. The failure boundary therefore moved from local bootstrap/database state to the first operation that requires Telegram-server interaction.

TDLib can emit `updateConnectionState` updates independently from authorization responses. The current harness retains unrelated updates while waiting for correlated responses, but does not surface connection-state evidence to the operator.

### Requirement / ТЗ
POC-TD-01 requires a controlled, observable, bounded authorization bootstrap. A timeout without network-state evidence is insufficient to distinguish local code defects from connectivity/environment problems.

### Analysis / architecture / security / reuse review
Official TDLib semantics separate authorization state from connection state. `setAuthenticationPhoneNumber` returns `Ok`, while connection progress is reported asynchronously through `updateConnectionState`.

The diagnostic must remain transport/runtime-only. No connection-state object may leak into FATHER domain contracts.

Only state type names may be printed. No endpoint, credential, phone number, API hash, DB key, proxy secret or session content may enter ordinary logs.

### Test contract before code

#### AUTH-NET-01 — connection state retained and surfaced
Given a correlated auth request is waiting and TDLib emits an unrelated `updateConnectionState`, the update must not be lost. The harness must surface a safe diagnostic containing only the connection-state type.

Examples of expected state types include:
- `connectionStateWaitingForNetwork`
- `connectionStateConnecting`
- `connectionStateConnectingToProxy`
- `connectionStateReady`
- `connectionStateUpdating`

#### AUTH-NET-02 — secrets are not surfaced
Connection diagnostics must not include auth request bodies, phone numbers, API credentials, database keys, proxy secrets or session data.

### Decision
Add tests first. Do not increase the timeout and do not add proxy/network configuration before connection-state evidence exists.

### WHY
A larger timeout would only make an unknown failure slower. Connection-state evidence tells us whether TDLib is waiting for network, attempting to connect, using a proxy path, or actually connected while the auth RPC remains unanswered.

### Files/components changed

#### Added
- `Tree_F/TF-0008_2026-08-11_TDLIB_CONNECTION_STATE_DIAGNOSTIC_TEST_CONTRACT.md`
- planned: `tests/test_tdlib_poc_connection_diagnostic.py`

#### Modified
- none before RED evidence

### Verification / evidence
Precondition evidence:
- targeted auth request-response tests: PASS (3/3)
- targeted auth transition tests: PASS (3/3)
- full local suite: PASS (48/48)
- GitHub Stage 06 DEV Verification on `0e5daf2`: SUCCESS
- GitHub CodeQL on `0e5daf2`: SUCCESS
- live `setTdlibParameters`: `ok`
- live `setAuthenticationPhoneNumber`: bounded correlated-response timeout

### Result
`PARTIAL`

### New / changed risks
- lack of network-state observability can cause wrong remediation decisions;
- increasing timeouts without evidence can hide connectivity defects;
- diagnostics must remain secret-safe.

### Registry changes
NONE pending RED/GREEN evidence.

### Rollback / replacement path
Tests and diagnostics remain PoC-only and can be removed without changing FATHER domain contracts.

### Next action / next gate
Add AUTH-NET-01/02 tests. Obtain RED evidence before changing `run_local.py`.

---

## RU

### Причина / проблема
Живой PoC теперь доказывает: `setTdlibParameters` возвращает `ok`, но `setAuthenticationPhoneNumber` завершается тайм-аутом ожидания именно коррелированного ответа. Значит, граница проблемы сместилась с локального запуска/БД на первую операцию, которая требует связи с серверами Telegram.

TDLib отдельно выдаёт `updateConnectionState`. Текущий клиент сохраняет такие посторонние updates во время ожидания ответа, но harness пока не показывает их оператору.

### Требование / ТЗ
POC-TD-01 требует контролируемой, наблюдаемой и ограниченной по времени авторизации. Просто timeout без сведений о состоянии сети недостаточен, чтобы отличить дефект нашего кода от проблемы соединения/окружения.

### Аналитика / архитектура / ИБ / повторное использование
В TDLib состояние авторизации и состояние соединения — разные сущности. `setAuthenticationPhoneNumber` должен вернуть `Ok`, а ход сетевого соединения приходит асинхронно через `updateConnectionState`.

Диагностика остаётся только внутри PoC/runtime. Никакие TDLib connection-state объекты не должны проникать в доменную модель FATHER.

В обычный вывод разрешено печатать только тип состояния. Нельзя выводить endpoint, номер телефона, API hash, DB key, proxy secret или session data.

### Контракт тестов до кода

#### AUTH-NET-01 — состояние соединения сохраняется и показывается
Если во время ожидания коррелированного auth-запроса TDLib выдаёт `updateConnectionState`, update не должен потеряться. Harness должен показать безопасную диагностику только с типом состояния соединения.

Возможные типы:
- `connectionStateWaitingForNetwork`
- `connectionStateConnecting`
- `connectionStateConnectingToProxy`
- `connectionStateReady`
- `connectionStateUpdating`

#### AUTH-NET-02 — секреты не выводятся
Диагностика соединения не должна содержать тела auth-запросов, номер телефона, API credentials, DB key, proxy secrets или session data.

### Решение
Сначала тесты. Не увеличиваем timeout и не добавляем proxy/network configuration до получения фактического connection-state evidence.

### ПОЧЕМУ
Увеличение timeout лишь замедлит неизвестную проблему. Состояние соединения покажет, ждёт ли TDLib сеть, пытается ли подключиться, идёт ли через proxy или уже имеет соединение, но auth RPC всё равно не отвечает.

### Изменённые файлы / компоненты

#### Добавлено
- `Tree_F/TF-0008_2026-08-11_TDLIB_CONNECTION_STATE_DIAGNOSTIC_TEST_CONTRACT.md`
- планируется: `tests/test_tdlib_poc_connection_diagnostic.py`

### Проверка / доказательства
Исходное состояние:
- auth request-response tests: PASS 3/3
- auth transition tests: PASS 3/3
- полный локальный suite: PASS 48/48
- GitHub Stage 06 DEV Verification на `0e5daf2`: SUCCESS
- GitHub CodeQL на `0e5daf2`: SUCCESS
- живой `setTdlibParameters`: `ok`
- живой `setAuthenticationPhoneNumber`: bounded timeout коррелированного ответа

### Результат
`PARTIAL`

### Новые / изменённые риски
- без состояния сети можно выбрать неправильное исправление;
- увеличение timeout без доказательств может скрывать сетевой дефект;
- диагностика обязана оставаться безопасной для секретов.

### Изменения реестров
NONE до RED/GREEN evidence.

### Откат / замена
Тесты и диагностика остаются в PoC и могут быть удалены без изменения доменных контрактов FATHER.

### Следующее действие / Gate
Добавить тесты AUTH-NET-01/02. Сначала получить RED, только потом менять `run_local.py`.
