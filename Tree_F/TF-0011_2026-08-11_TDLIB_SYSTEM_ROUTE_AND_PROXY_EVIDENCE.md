# TF-0011 — TDLib system route and proxy evidence / Доказательства системного маршрута и прокси TDLib

Status: PARTIAL
Date: 2026-08-11
Supersedes: none
Related: TF-0009, TF-0010

## EN

### Trigger / problem
Live TDLib authorization reaches `authorizationStateWaitPhoneNumber`, then `connectionStateConnecting`, and times out waiting for the response to `setAuthenticationPhoneNumber` even with a 30-second bounded window.

### New evidence
Windows network diagnostics show:

- DNS resolution for `telegram.org` and `web.telegram.org` succeeds to `149.154.167.99` (and IPv6 records).
- TCP connection attempts to `149.154.167.99` fail on ports 80, 443, and 5222.
- The tested path uses `InterfaceAlias = Wi-Fi` / source address `192.168.1.110`.
- WinHTTP proxy configuration reports direct access (no proxy server).
- Active network adapters visible to Windows are Wi-Fi plus VMware VMnet1/VMnet8; no conventional connected VPN/TUN adapter is visible in the captured adapter list.

### Decision
Do not modify TDLib authentication code.

Proceed with system route / VPN / proxy diagnostics before any further code changes.

### WHY
The current failure is consistent with an unavailable direct network path to Telegram rather than an authorization-state-machine defect. All tested direct TCP paths to the resolved Telegram IPv4 endpoint fail before application-level authentication can complete.

A browser-only VPN/proxy or application-specific tunnel would not automatically provide connectivity to a native TDLib process.

### Next evidence gate
Capture:

1. IPv4 default route and explicit route to `149.154.167.99`.
2. Windows VPN connection inventory.
3. process/environment proxy variables.
4. whether a VPN client exposes a system tunnel or only browser/application proxying.

Do not disable security controls or alter firewall policy until the path is understood.

## RU

### Причина / проблема
Живой запуск TDLib доходит до `authorizationStateWaitPhoneNumber`, затем показывает `connectionStateConnecting` и завершается по тайм-ауту ответа на `setAuthenticationPhoneNumber`, причём тот же результат получен и при ограниченном окне 30 секунд.

### Новые доказательства
Диагностика Windows показала:

- DNS для `telegram.org` и `web.telegram.org` работает и возвращает `149.154.167.99` (также есть IPv6-записи).
- TCP-подключение к `149.154.167.99` не проходит на портах 80, 443 и 5222.
- Проверяемый маршрут идёт через `Беспроводная сеть`, исходный адрес `192.168.1.110`.
- WinHTTP сообщает прямой доступ без прокси.
- Среди активных сетевых адаптеров видны Wi-Fi и VMware VMnet1/VMnet8; обычного подключённого VPN/TUN-адаптера в полученном списке нет.

### Решение
Код авторизации TDLib не меняем.

Следующий этап — диагностика системного маршрута, VPN и прокси до любых новых изменений кода.

### ПОЧЕМУ
Текущая ошибка уже хорошо согласуется с недоступностью прямого сетевого пути к Telegram, а не с дефектом state-machine авторизации. Все проверенные TCP-подключения к разрешённому IPv4-адресу Telegram падают до того, как может завершиться прикладная авторизация.

Если VPN работает только как расширение браузера или как прокси отдельного приложения, нативный процесс TDLib автоматически через него не пойдёт.

### Следующий Gate
Нужно получить:

1. маршрут по умолчанию IPv4 и отдельный маршрут к `149.154.167.99`;
2. список Windows VPN-подключений;
3. proxy-переменные окружения процесса;
4. понимание, создаёт ли используемый VPN системный туннель или работает только на уровне браузера/прокси.

До этого firewall и другие защитные настройки не отключаем и не меняем.
