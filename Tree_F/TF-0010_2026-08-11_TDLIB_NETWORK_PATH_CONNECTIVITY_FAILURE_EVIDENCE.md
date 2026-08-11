# TF-0010 — TDLib network-path connectivity failure evidence / Доказательство сетевой недоступности пути TDLib

## EN

### Date
2026-08-11

### Stage / milestone
Stage 07 / M5 — Telegram Radar / TDLib PoC network diagnostic gate

### Trigger / problem
Live TDLib runs reached `authorizationStateWaitPhoneNumber` and then `connectionStateConnecting`, but `setAuthenticationPhoneNumber` timed out with both 5-second and 30-second bounded request windows.

Direct Windows connectivity checks were then executed from the same host and route.

Observed:

- `Resolve-DnsName telegram.org` succeeded and resolved `149.154.167.99` plus IPv6.
- `Resolve-DnsName web.telegram.org` also succeeded.
- `Test-NetConnection telegram.org -Port 443` failed.
- `Test-NetConnection web.telegram.org -Port 443` failed.
- The active interface was Wi-Fi with source address `192.168.1.110`.

### Decision
Treat the current blocker as a network-path/connectivity problem until disproven.

Do not modify TDLib authorization logic while DNS succeeds but TCP/443 to Telegram fails from the same Windows host.

Proceed with route/VPN/firewall/proxy diagnostics and alternate allowed network-path validation.

### WHY
The current evidence separates application behavior from transport reachability:

1. TDLib runtime loads and verifies the approved binary.
2. `setTdlibParameters` returns `ok`.
3. TDLib reaches `authorizationStateWaitPhoneNumber`.
4. TDLib reports `connectionStateConnecting`.
5. Direct OS-level TCP connection to the resolved Telegram address on port 443 fails.

This is consistent with TDLib remaining in the connecting state and not receiving a response to the phone-number request.

Changing auth code or increasing timeouts further would not address an unreachable network path.

### Commercial / reuse review
No product-direction change.

The finding reinforces a reusable operational requirement: Telegram acquisition must expose network-state diagnostics and must support deployment environments where direct Telegram connectivity may be blocked or routed differently.

Future production design may need an explicitly configured and governed proxy/VPN path, but no such product decision is authorized by this evidence alone.

### Files/components affected
Documentation only in this record.

Protected product code remains unchanged pending network evidence.

### Acceptance test / evidence
Current evidence:

- TDLib: `connectionStateConnecting`
- auth request: bounded timeout after `setAuthenticationPhoneNumber`
- DNS: PASS
- TCP/443 to `telegram.org`: FAIL
- TCP/443 to `web.telegram.org`: FAIL

Next network evidence to collect:

- TCP/80 and TCP/5222 reachability
- active adapters and interface metrics
- Windows route table
- WinHTTP proxy state
- VPN/tunnel adapter presence
- comparison with an alternate known-good network path if available

### Result
PARTIAL — application defect is not currently indicated; network path remains the leading blocker.

### New risks
- VPN may be enabled at application/browser level but not system-wide.
- split tunneling may exclude TDLib traffic.
- local/endpoint firewall may block Telegram ranges or outbound ports.
- upstream ISP/network policy may block Telegram endpoints.
- a proxy may be required but not configured for TDLib.
- IPv4 and IPv6 routing may differ.

### Registry changes
Record network-path dependency risk for M5 PoC evidence. Do not mark TDLib unsuitable until tested through a confirmed reachable path.

### Next action / next reuse-review gate
Collect route/VPN/firewall/proxy evidence without changing TDLib code.

Next gate: determine whether TCP connectivity succeeds through any approved network path. If yes, repeat POC-TD-01 on that path. If no, design a separate proxy/network-access PoC contract before implementation.

---

## RU

### Дата
11.08.2026

### Этап / веха
Этап 07 / M5 — Telegram Radar / диагностика сетевого пути TDLib

### Причина / проблема
Живые запуски TDLib доходят до `authorizationStateWaitPhoneNumber`, затем показывают `connectionStateConnecting`, но `setAuthenticationPhoneNumber` завершается тайм-аутом как при 5-секундном, так и при 30-секундном ограниченном окне.

После этого на том же компьютере и через тот же маршрут были выполнены прямые проверки сети Windows.

Получено:

- `Resolve-DnsName telegram.org` успешно разрешает имя в `149.154.167.99` и IPv6-адрес;
- `Resolve-DnsName web.telegram.org` также работает;
- `Test-NetConnection telegram.org -Port 443` — FAIL;
- `Test-NetConnection web.telegram.org -Port 443` — FAIL;
- активный интерфейс — Wi-Fi, исходный адрес `192.168.1.110`.

### Решение
До появления обратных доказательств считать текущий блокер проблемой сетевого пути/доступности.

Не изменять логику авторизации TDLib, пока DNS работает, но TCP/443 до Telegram не проходит с того же Windows-хоста.

Продолжить диагностику маршрута, VPN, firewall и proxy, а затем проверить альтернативный разрешённый сетевой путь.

### ПОЧЕМУ
Текущая цепочка доказательств отделяет код приложения от сетевой доступности:

1. TDLib runtime загружается и SHA-256 библиотеки проверяется.
2. `setTdlibParameters` возвращает `ok`.
3. TDLib доходит до `authorizationStateWaitPhoneNumber`.
4. TDLib сообщает `connectionStateConnecting`.
5. Прямая TCP-проверка Windows до разрешённого адреса Telegram на порту 443 завершается неуспешно.

Это согласуется с тем, что TDLib остаётся в состоянии подключения и не получает ответ на запрос номера телефона.

Дальнейшее изменение auth-кода или простое увеличение timeout не исправит недоступный сетевой путь.

### Коммерческое / повторное использование
Направление продукта не меняется.

Вывод добавляет важное универсальное эксплуатационное требование: Telegram-транспорт должен показывать состояние сети и учитывать среды, где прямой доступ к Telegram блокируется или маршрутизируется отдельно.

В production в будущем может потребоваться явно управляемый proxy/VPN-путь, но по одному этому факту решение ещё не принимается.

### Затрагиваемые файлы / компоненты
На этом шаге только документация.

Рабочий код продукта не изменяется до получения сетевых доказательств.

### Приёмочные тесты / доказательства
Текущие доказательства:

- TDLib: `connectionStateConnecting`;
- auth request: bounded timeout после `setAuthenticationPhoneNumber`;
- DNS: PASS;
- TCP/443 до `telegram.org`: FAIL;
- TCP/443 до `web.telegram.org`: FAIL.

Следующие данные:

- доступность TCP/80 и TCP/5222;
- активные сетевые адаптеры и метрики интерфейсов;
- таблица маршрутизации Windows;
- WinHTTP proxy;
- наличие VPN/tunnel-адаптеров;
- сравнение с альтернативным заведомо рабочим сетевым путём, если он доступен.

### Результат
PARTIAL — признаков дефекта приложения сейчас нет; главным блокером остаётся сетевой путь.

### Новые риски
- VPN может работать только для браузера/отдельного приложения, но не системно;
- split tunneling может исключать трафик TDLib;
- локальный/endpoint firewall может блокировать диапазоны Telegram или исходящие порты;
- провайдер или сеть могут блокировать Telegram;
- TDLib может требовать proxy, который сейчас не настроен;
- IPv4 и IPv6 могут маршрутизироваться по-разному.

### Изменения реестров
Зафиксировать риск зависимости M5 PoC от сетевого пути. Не признавать TDLib непригодным, пока он не проверен через заведомо доступный маршрут.

### Следующее действие / следующий Gate
Собрать данные о маршрутах/VPN/firewall/proxy без изменения TDLib-кода.

Следующий Gate: определить, проходит ли TCP через любой разрешённый сетевой путь. Если да — повторить POC-TD-01 на нём. Если нет — сначала спроектировать отдельный PoC-контракт proxy/network access, а уже затем писать код.
