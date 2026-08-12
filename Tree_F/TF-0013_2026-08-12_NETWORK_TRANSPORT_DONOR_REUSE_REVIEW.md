# TF-0013 — Network Transport Donor / Reuse Review

Date: 2026-08-12
Status: ACTIVE / RESEARCH GATE
Scope: Windows network transport for Telegram/OSINT collectors

---

## ENGLISH

### Stage / milestone
Donor and reuse review before any new network-transport implementation.

### Trigger / problem
The current Windows host resolves Telegram DNS successfully but direct TCP connectivity to Telegram endpoints fails on ports 80, 443 and 5222. Both TDLib and the legacy Telethon reader fail at the network-connect stage. Existing browser access can therefore not be treated as evidence of system-wide connectivity.

### Decision
Do not write a custom VPN or proxy stack now. Evaluate mature upstream transports first and keep them as external dependencies unless a later product requirement proves that embedding/forking is necessary.

Current shortlist:

1. **AmneziaWG for Windows / amneziawg-windows-client** — primary Windows tunnel donor for PoC.
   - Official/recommended Windows client uses Wintun.
   - Repository is MIT-licensed.
   - Separate embeddable tunnel library is also MIT-licensed.
   - Attractive for future commercial/reuse isolation compared with GPL full clients.

2. **Amnezia VPN Client** — operational/manual validation candidate.
   - Full desktop/mobile client.
   - GPL-3.0.
   - Useful to prove that a Windows system tunnel fixes Telegram access before any integration work.
   - Current Windows split-tunneling issues exist, so VMware/LAN routes must be tested explicitly.

3. **Telegram MTProxy** — Telegram-only fallback.
   - Official Telegram MT-Proto proxy implementation.
   - Server-oriented Linux build/run model.
   - Appropriate when only Telegram transport needs bypass/proxy capability.
   - Not a general OSINT transport for web/GitHub/other collectors.

4. **sing-box** — universal proxy/TUN fallback candidate.
   - Mature universal proxy platform.
   - GPL-3.0-or-later style licensing constraints must be reviewed before embedded commercial reuse.
   - Potentially useful later for one policy layer covering SOCKS/TUN/other transports.

### WHY
The current failure is below TDLib/Telethon business logic. Rewriting authentication or collector code would not solve a blocked system network path. A reusable OSINT product should separate collector logic from transport policy.

Target architecture direction:

```text
FATHER OSINT
    |
    +-- NetworkPolicy / TransportSelector
    |      +-- DIRECT
    |      +-- SYSTEM_TUN
    |      +-- SOCKS5
    |      +-- MTProxy
    |      +-- future managed transport
    |
    +-- Telegram collector (TDLib / fallback)
    +-- Web collector
    +-- GitHub collector
    +-- other collectors
```

No automatic failover is approved yet. This record only defines the research boundary.

### Commercial / reuse review
- Prefer external dependency boundaries over copying VPN code into the repository.
- MIT AmneziaWG Windows components are materially easier to reuse than GPL full clients.
- GPL candidates can still be used operationally as external programs, but distribution/integration boundaries require legal review before commercial packaging.
- Network configuration, secrets, private keys, proxy credentials and session material must remain outside Git and Tree_F evidence.

### Risks
- Windows split tunneling may interfere with VMware VMnet1/VMnet8 or LAN access.
- DNS route and kill-switch behaviour can produce false positives/false negatives in collector health checks.
- A working browser VPN is not evidence that Python/TDLib has the same route.
- Full-tunnel validation can affect unrelated applications; PoC must be reversible.
- VPN/proxy credentials are secrets and must never be committed.

### Acceptance test / evidence for the next gate
No code integration is allowed until a manual Windows transport PoC passes all of the following:

1. Existing VMware adapters remain present and their local networks remain reachable.
2. A new tunnel/proxy path is observable in Windows routing or adapter state.
3. `Test-NetConnection telegram.org -Port 443` succeeds OR an equivalent transport-specific Telegram connectivity test succeeds through the selected donor.
4. Legacy Telethon `simple_reader.py` connects using the existing saved session and can fetch a controlled public-channel sample.
5. TDLib reaches `connectionStateReady` and continues authorization without the current network timeout.
6. After disconnecting the donor transport, the host returns to the original route state.
7. No secrets appear in logs or Git changes.

### Result
DEFERRED — donor selected for manual validation, integration not started.

### New risks
Windows split-tunneling regressions in current Amnezia releases are a specific review item. Do not enable application/site split tunneling during the first transport proof; start with a simple full-tunnel validation and verify VMware/LAN separately.

### Registry changes
- Add Network Transport Donor Review gate.
- Primary manual validation candidate: AmneziaWG/Amnezia Windows.
- Telegram-only fallback: MTProxy.
- Universal fallback candidate: sing-box.

### Next action / next reuse-review gate
Manual Windows tunnel proof. Only after PASS: write TF-0014 for integration requirements and security/test contract. No production code before TF-0014 acceptance criteria are approved.

---

## РУССКИЙ

### Этап / веха
Обзор доноров и повторного использования до любой новой реализации сетевого транспорта.

### Причина / проблема
Текущий Windows-хост успешно разрешает DNS Telegram, но прямое TCP-соединение с Telegram не проходит на портах 80, 443 и 5222. И TDLib, и старый рабочий Telethon-reader падают именно на сетевом подключении. Поэтому доступ Telegram в браузере нельзя считать доказательством системного доступа для Python/TDLib.

### Решение
Сейчас не пишем собственный VPN или proxy-стек. Сначала проверяем зрелые upstream-решения и держим их внешними зависимостями, пока отдельное продуктовое требование не докажет необходимость встраивания или форка.

Текущий shortlist:

1. **AmneziaWG for Windows / amneziawg-windows-client** — основной кандидат Windows-туннеля для PoC.
   - Официальный Windows-клиент использует Wintun.
   - Репозиторий MIT.
   - Отдельная embeddable tunnel library также MIT.
   - Удобнее для будущего коммерческого переиспользования, чем полный GPL-клиент.

2. **Amnezia VPN Client** — кандидат для ручной эксплуатационной проверки.
   - Полный desktop/mobile клиент.
   - GPL-3.0.
   - Нужен прежде всего для доказательства, что системный Windows-туннель устраняет текущую сетевую проблему Telegram.
   - Есть актуальные Windows-проблемы split tunneling, поэтому VMware/LAN необходимо проверять отдельно.

3. **Telegram MTProxy** — Telegram-only fallback.
   - Официальная реализация Telegram MT-Proto proxy.
   - В первую очередь серверная Linux-модель.
   - Подходит, если обход/прокси нужен только Telegram.
   - Не является универсальным транспортом для остальных OSINT-источников.

4. **sing-box** — универсальный proxy/TUN fallback-кандидат.
   - Зрелая универсальная proxy-платформа.
   - GPL-ограничения нужно отдельно учитывать перед коммерческим встраиванием/распространением.
   - Может быть полезен позже как единый слой политики для SOCKS/TUN и других транспортов.

### ПОЧЕМУ
Текущий дефект находится ниже уровня логики TDLib/Telethon. Переписывание авторизации или collector-кода не устранит заблокированный сетевой путь. Для переиспользуемого OSINT-продукта collector должен быть отделён от транспортной политики.

Целевое архитектурное направление:

```text
FATHER OSINT
    |
    +-- NetworkPolicy / TransportSelector
    |      +-- DIRECT
    |      +-- SYSTEM_TUN
    |      +-- SOCKS5
    |      +-- MTProxy
    |      +-- future managed transport
    |
    +-- Telegram collector
    +-- Web collector
    +-- GitHub collector
    +-- другие collectors
```

Автоматическое переключение транспорта пока НЕ утверждено. Эта запись только определяет исследовательскую границу.

### Коммерческий / reuse review
- Предпочитаем внешнюю зависимость вместо копирования VPN-кода в наш репозиторий.
- MIT-компоненты AmneziaWG Windows проще для повторного использования, чем GPL-полные клиенты.
- GPL-решения можно использовать как внешние программы, но границы распространения/интеграции требуют отдельной юридической проверки перед коммерческой упаковкой.
- Конфигурация сети, приватные ключи, proxy credentials и Telegram sessions не должны попадать в Git или Tree_F.

### Риски
- Windows split tunneling может нарушить VMware VMnet1/VMnet8 или локальный LAN.
- DNS, маршруты и kill-switch могут давать ложные результаты health-check.
- Работающий browser VPN не означает, что Python/TDLib идёт тем же маршрутом.
- Full tunnel может затронуть другие приложения; PoC должен быть обратимым.
- VPN/proxy credentials являются секретами.

### Приёмочный тест / доказательство следующего Gate
Интеграционный код запрещён, пока ручной Windows transport PoC не выполнит всё ниже:

1. VMware VMnet1/VMnet8 остаются доступными.
2. Новый tunnel/proxy path наблюдается в Windows route/adapters.
3. `Test-NetConnection telegram.org -Port 443` становится успешным ИЛИ выбранный transport даёт эквивалентное доказательство доступа Telegram.
4. Старый `simple_reader.py` Telethon подключается с существующей session и получает контролируемую выборку публичного канала.
5. TDLib достигает `connectionStateReady` и проходит дальше текущего network timeout.
6. После отключения транспорта исходные маршруты Windows восстанавливаются.
7. Секреты не попадают в логи и Git diff.

### Результат
DEFERRED — донор выбран для ручной проверки, интеграция не начата.

### Новые риски
Свежие проблемы Windows split tunneling в Amnezia являются обязательным пунктом проверки. В первом PoC не используем split tunneling: сначала простой full-tunnel proof, затем отдельно проверяем VMware/LAN.

### Изменения реестра
- Добавлен Network Transport Donor Review gate.
- Основной кандидат ручной проверки: AmneziaWG/Amnezia Windows.
- Telegram-only fallback: MTProxy.
- Универсальный fallback: sing-box.

### Следующее действие / следующий reuse-review gate
Ручная проверка Windows tunnel. Только после PASS создаём TF-0014 с требованиями интеграции, security review и test contract. До этого production-код не меняем.
