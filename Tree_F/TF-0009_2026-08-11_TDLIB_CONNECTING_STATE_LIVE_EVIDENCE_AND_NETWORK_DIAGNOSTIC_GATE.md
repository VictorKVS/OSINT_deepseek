# TF-0009 — TDLib `connectionStateConnecting` live evidence and network diagnostic gate

**Date / Дата:** 2026-08-11  
**Status / Статус:** ACTIVE / NEXT GATE  
**Scope / Область:** M5 Telegram Radar / TDLib PoC / POC-TD-01

---

## EN

### Requirement / observation

A controlled live Windows run after the correlated authorization-response refactor and connection-state diagnostics produced:

- `authorizationStateWaitTdlibParameters`;
- correlated `setTdlibParameters -> ok`;
- `authorizationStateWaitPhoneNumber`;
- `connectionStateConnecting`;
- bounded timeout waiting for the correlated response to `setAuthenticationPhoneNumber`.

No credentials, phone number, API hash, database key, or authentication code are recorded in this file.

### Interpretation

This narrows the fault domain materially:

1. TDLib native library loads and its approved SHA-256 is verified.
2. Local TDLib parameter initialization succeeds.
3. The encrypted runtime database is usable with the current key.
4. The phone-number authorization request is actually sent through the correlated request-response layer.
5. TDLib reports `connectionStateConnecting`, which means it is actively establishing a connection to Telegram servers rather than waiting for local network availability.
6. No correlated response to `setAuthenticationPhoneNumber` is observed within the current 5-second diagnostic timeout.

Per TDLib documentation, `connectionStateConnecting` means that a connection to Telegram servers is being established; `connectionStateReady` means that a working connection to Telegram servers exists. `updateConnectionState` is a human-readable diagnostic update and must not itself be treated as an authorization result.

### Decision / WHY

Do **not** modify authorization business logic and do **not** blindly increase the timeout yet.

The next gate is network-path and latency diagnostics. We need to determine whether:

- the Telegram connection becomes `connectionStateReady` if given a larger bounded diagnostic window;
- the host can establish outbound connectivity required by TDLib;
- VPN/firewall/proxy/routing conditions are delaying or blocking Telegram transport;
- or the request receives an explicit TDLib response once a working Telegram connection is established.

### Test-first next contract

Before changing production behavior, define diagnostics that preserve bounded execution:

- `NET-LIVE-01`: allow a configurable diagnostic auth-request timeout (for example 30 seconds) without changing the default production/PoC contract silently;
- `NET-LIVE-02`: surface the sequence of safe `connectionState...` values observed during that bounded window;
- `NET-LIVE-03`: if `connectionStateReady` is reached, require either correlated `Ok` / explicit TDLib error / bounded timeout for `setAuthenticationPhoneNumber`;
- `NET-LIVE-04`: never print secrets or raw request bodies;
- `NET-LIVE-05`: local/manual network probes are evidence only and must not become product dependencies.

### Current result

`POC-TD-01`: **PARTIAL**.

Authorization has not yet reached `authorizationStateReady`, but the failure is now bounded and localized to Telegram connectivity/request-response after local TDLib setup.

### Next gate

Run controlled local network diagnostics first. No new product code before the diagnostic contract is satisfied.

---

## RU

### Требование / наблюдение

Контролируемый живой запуск на Windows после перехода на коррелируемые auth-запросы и добавления диагностики состояния соединения дал следующую последовательность:

- `authorizationStateWaitTdlibParameters`;
- коррелируемый ответ `setTdlibParameters -> ok`;
- `authorizationStateWaitPhoneNumber`;
- `connectionStateConnecting`;
- ограниченный по времени timeout ожидания ответа на `setAuthenticationPhoneNumber`.

В этом документе не фиксируются номер телефона, API hash, ключ БД, коды авторизации или иные секреты.

### Интерпретация

Область неисправности существенно сузилась:

1. Нативная библиотека TDLib загружается, SHA-256 проверяется.
2. Локальные параметры TDLib принимаются успешно.
3. Зашифрованная runtime-БД открывается текущим ключом.
4. Запрос с номером телефона реально отправляется через коррелируемый request-response слой.
5. TDLib сообщает `connectionStateConnecting`, то есть пытается установить соединение с серверами Telegram, а не ожидает наличия локальной сети.
6. За текущие 5 секунд коррелируемый ответ на `setAuthenticationPhoneNumber` не получен.

По документации TDLib `connectionStateConnecting` означает установление соединения с серверами Telegram; `connectionStateReady` означает наличие рабочего соединения. `updateConnectionState` — диагностическое событие для человекочитаемого отображения состояния и не является результатом авторизации.

### Решение / WHY

**Не** меняем auth-бизнес-логику и **не** увеличиваем timeout вслепую.

Следующий Gate — диагностика сетевого пути и задержек. Нужно определить:

- достигает ли TDLib `connectionStateReady`, если дать больший, но ограниченный диагностический интервал;
- может ли Windows-хост установить нужные исходящие соединения;
- не мешают ли VPN, firewall, proxy или маршрутизация;
- появляется ли явный ответ TDLib на `setAuthenticationPhoneNumber` после установления рабочего соединения с Telegram.

### Следующий test-first контракт

До изменения production-поведения фиксируем диагностический контракт:

- `NET-LIVE-01`: разрешить конфигурируемый диагностический timeout auth-запроса (например 30 секунд), не меняя молча значение по умолчанию;
- `NET-LIVE-02`: безопасно показывать последовательность `connectionState...` в пределах этого интервала;
- `NET-LIVE-03`: если достигнут `connectionStateReady`, требовать `Ok`, явную TDLib error или bounded timeout для `setAuthenticationPhoneNumber`;
- `NET-LIVE-04`: не выводить секреты и сырые тела запросов;
- `NET-LIVE-05`: ручные сетевые проверки используются только как evidence и не становятся runtime-зависимостью продукта.

### Текущий результат

`POC-TD-01`: **PARTIAL**.

До `authorizationStateReady` мы ещё не дошли, однако проблема теперь ограничена по времени и локализована на участке сетевого соединения/ответа Telegram после успешной локальной инициализации TDLib.

### Следующий Gate

Сначала контролируемая локальная диагностика сети. Новый product-код до выполнения диагностического контракта не добавляем.
