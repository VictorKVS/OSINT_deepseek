# FATHER OSINT Intelligence Center — архитектурный контракт (Draft v0.1)

Статус: **UI prototype committed; backend integration not implemented**. Ветка `feature/osint-intelligence-center-ui`. Существующие Telegram Radar, секреты и сессии не изменяются.

## Цель
Единое рабочее место OSINT для поиска публичных источников, рейтингов, чтения архивов Telegram, экспериментов с Linux/Kali/Python/API инструментами, проверки качества, передачи доказательств в ALINA и построения графа знаний.

## Разделы интерфейса
1. Dashboard — состояние работ и доказательств.
2. Discovery — каталог и поиск публичных каналов.
3. Ranking — внешние показатели и независимая оценка качества.
4. Archive Reader — сообщения с permalink, датой, ID, происхождением и checkpoints.
5. Tool Zoo — реестр программ, версии, адаптеры, лицензии.
6. Visual ToolLab — типизированные входы/выходы, граф цепочек.
7. Experiment Lab — контрольные наборы, воспроизводимость, затраты.
8. Quality Benchmark — precision, recall, freshness, uniqueness, provenance, reproducibility.
9. Evidence Explorer — неизменяемые оригиналы и SHA-256.
10. ALINA Analyst — извлечение проверяемых утверждений, не подмена первоисточника.
11. Knowledge Graph — сущности и связи с доказательствами.
12. Privacy & Network Security — три профиля.

## Три профиля
- **OPEN**: прямой доступ только для разрешённых задач и разработки; сетевой сбор по отдельной политике.
- **VPN**: основной режим сбора; подтверждённый защищённый маршрут, DNS, IPv4/IPv6 и kill switch; fail closed при потере туннеля.
- **PARANOID**: изолированная VM/контейнер, минимальные разрешения, раздельные секреты/контексты, allowlist, подтверждение защищённого маршрута, fail closed.

SOCKS5 TCP-connect **не является** доказательством отсутствия DNS/IPv6/route leak. Переключение профиля в UI само по себе не меняет систему.

## Данные и контракты
- Source: source_id, type, handle, canonical_url, discovered_at, discovery_method, confidence.
- Post: source_id, message_id, published_at, edited_at?, permalink, text, attachment_refs, forwarded_from?, retrieved_at.
- Evidence: evidence_id, source_ref, sha256, acquisition_run_id, immutable_path, metadata.
- ToolAdapter: tool_id, version, runtime, input_schema, output_schema, network_policy, time_limit, resource_limit, license.
- Experiment: experiment_id, dataset_id, tool_graph, parameters, environment_hash, metrics, artifacts.
- Finding: claim, evidence_refs[], confidence, limitations, analyst_review_state.

Нельзя публиковать реальные оценки качества до запуска воспроизводимого теста. Отдельно хранить обнаруженные источники, результаты сбора и выводы модели.

## Гейты реализации
G0: UI-каркас и архитектурный контракт (текущая ветка).
G1: проверка UX/адаптивности/навигации.
G2: backend read-only API и импорт демонстрационных/разрешённых источников.
G3: Telegram Collector с checkpoints, rate limits, secret isolation и аудитом.
G4: Tool Adapter SDK + изолированные Linux workers + policy enforcement.
G5: Experiment Planner, метрики качества, тестовые наборы.
G6: ALINA, RAG, граф, трассировка доказательств.
G7: e2e, threat model, supply-chain review, доступность и эксплуатация.

## Локальный просмотр
Открыть `web/osint-intelligence-center/index.html` в браузере. Статический прототип без зависимостей, API и VPN. Для разработки использовать отдельную ветку и не переносить реальные секреты/сессии в Git.
