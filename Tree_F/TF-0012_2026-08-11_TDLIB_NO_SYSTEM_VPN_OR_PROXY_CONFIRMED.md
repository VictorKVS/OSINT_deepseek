# TF-0012 — TDLib: no system VPN/proxy confirmed

## EN

**Date:** 2026-08-11  
**Status:** PASS — diagnostic evidence captured  
**Supersedes:** none  
**Related:** TF-0009, TF-0010, TF-0011

### Trigger / problem
TDLib reached `connectionStateConnecting` but did not reach `connectionStateReady`. Direct TCP tests to Telegram failed on ports 80, 443, and 5222.

### Evidence
Windows host evidence showed:

- default IPv4 route: `0.0.0.0/0 -> 192.168.1.1` via Wi-Fi;
- `Get-VpnConnection` returned no configured Windows VPN connections;
- `Get-VpnConnection -AllUserConnection` returned no configured all-user VPN connections;
- no environment variables matching `PROXY` or `VPN` were present;
- WinHTTP proxy mode was direct access;
- `curl.exe -I https://telegram.org --connect-timeout 10` timed out;
- direct TCP probes to `149.154.167.99` on 80, 443, and 5222 failed;
- DNS resolution for Telegram succeeded.

### Decision
Do not change TDLib authorization code.

Treat the current blocker as a host/network-path issue until evidence proves otherwise.

The next diagnostic gate is to identify whether browser access, if available, is provided by an application-local proxy/VPN, browser extension, split-tunnel product, or another mechanism not visible as a Windows VPN interface or WinHTTP proxy.

### WHY
TDLib and `curl.exe` are both system processes. Both use the host network path and currently fail to reach Telegram while DNS succeeds. The evidence does not support an authentication-state-machine defect as the primary cause.

### Acceptance / next evidence
Capture:

1. WinINET / user proxy configuration;
2. active processes and services related to VPN/proxy/TUN/WireGuard/OpenVPN;
3. active network adapters after the user's VPN is enabled;
4. if a local proxy is exposed, its type and local endpoint without storing credentials;
5. repeat `Test-NetConnection telegram.org -Port 443` after a system-level route/proxy is available.

### Result
PASS — absence of a usable system VPN/proxy path is evidenced for the current host state.

---

## RU

**Дата:** 11.08.2026  
**Статус:** PASS — диагностические доказательства собраны  
**Связано с:** TF-0009, TF-0010, TF-0011

### Причина / проблема
TDLib дошёл до `connectionStateConnecting`, но не достигает `connectionStateReady`. Прямые TCP-проверки Telegram не проходят на портах 80, 443 и 5222.

### Доказательства
На Windows подтверждено:

- маршрут по умолчанию: `0.0.0.0/0 -> 192.168.1.1` через Wi-Fi;
- `Get-VpnConnection` не показывает Windows VPN-подключений;
- `Get-VpnConnection -AllUserConnection` также пуст;
- переменные окружения `PROXY` / `VPN` отсутствуют;
- WinHTTP настроен на прямой доступ;
- `curl.exe -I https://telegram.org --connect-timeout 10` завершается тайм-аутом;
- TCP к `149.154.167.99` на 80, 443 и 5222 не проходит;
- DNS Telegram при этом работает.

### Решение
Код авторизации TDLib не менять.

Считать текущий блокер проблемой сетевого пути хоста, пока новые доказательства не покажут обратное.

Следующий Gate — определить, чем именно обеспечивается доступ браузера, если он работает: локальным proxy/VPN приложения, расширением браузера, split-tunnel продуктом или иным механизмом, который не виден как Windows VPN-интерфейс или WinHTTP proxy.

### ПОЧЕМУ
И TDLib, и `curl.exe` являются системными процессами и используют сетевой путь Windows. Оба сейчас не могут достичь Telegram, хотя DNS работает. Эти данные не подтверждают, что основной дефект находится в state-machine авторизации.

### Следующие доказательства
Нужно снять:

1. настройки WinINET / пользовательского proxy;
2. процессы и службы VPN/proxy/TUN/WireGuard/OpenVPN;
3. активные сетевые адаптеры при включённом VPN;
4. при наличии локального proxy — его тип и локальный endpoint без сохранения учётных данных;
5. повторить `Test-NetConnection telegram.org -Port 443` после появления системного маршрута/proxy.

### Результат
PASS — отсутствие рабочего системного VPN/proxy для текущего состояния хоста доказано.
