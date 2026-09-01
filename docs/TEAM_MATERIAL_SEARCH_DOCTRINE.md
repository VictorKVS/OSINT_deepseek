# FATHER — что ищем и как ищем

Status: ACTIVE SEARCH DOCTRINE

## 1. Единица поиска

Мы не ищем «книги для программиста», «материалы для аналитика» или «всё про RAG». Единица поиска — конкретная **ROLE_TOPIC** из `config/team_role_material_registry.json`.

Для каждой темы собирается не склад файлов, а **пакет знания**.

## 2. Что именно ищем по каждой теме

Минимальный пакет темы должен ответить на пять разных вопросов:

1. **AUTHORITATIVE_BASIS — на что опираемся?** Официальная документация, стандарт, спецификация, закон/регулятор, первичная публикация, model card или paper — в зависимости от профиля.
2. **CORE_CONCEPT — что это такое?** Термины, определения, модель, границы применимости.
3. **PRACTICAL_METHOD_OR_IMPLEMENTATION — как это делается?** Алгоритм, архитектурный паттерн, reference implementation, инструкция, шаблон.
4. **VALIDATION_OR_TEST — как доказать, что сделано правильно?** Тесты, acceptance criteria, benchmark, checklist, validation method.
5. **FAILURE_MODE_OR_ANTIPATTERN — где и почему это ломается?** Ошибки, ограничения, anti-pattern, incident/postmortem, контрпример.

После этого при необходимости добираются: шаблоны, case studies, trade-offs, version/change history и метрики.

## 3. Где ищем

Порядок источников нельзя менять местами только потому, что Telegram удобнее.

| Tier | Источник | Для чего |
|---|---|---|
| S0 | Официальные/стандарты/регулятор/первичный paper | определения, требования, семантика, актуальная версия |
| S1 | Официальные project/vendor docs, maintainer repo | реализация и эксплуатационная семантика |
| S2 | Книги, курсы, авторские материалы | объяснения, модели мышления, систематизация |
| S3 | Кейсы, postmortem, benchmark, test suite | проверка, ограничения, ошибки, реальные trade-offs |
| S4 | Telegram/community | discovery и поиск кандидатов; не источник истины сам по себе |

Для права и нормативки S0 обязателен. Telegram/комментарий не может закрыть authoritative basis.

## 4. Как ищем — четыре прохода

### P1 ANCHOR

Цель: найти первичный источник и каноническую терминологию.

Запросы: `{topic}`, `{topic} official documentation`, `{topic} specification`, `{topic} standard`, `{topic} current version`, `{topic} changelog`.

Telegram на этом проходе не нужен.

### P2 METHOD

Цель: найти методику, пример реализации и способ проверки.

Запросы: `{topic} implementation guide`, `{topic} best practices`, `{topic} reference implementation`, `{topic} checklist`, `{topic} testing`, `{topic} acceptance criteria`.

Здесь уже допустимы книги, курсы, GitHub и Telegram-кандидаты.

### P3 CHALLENGE

Цель: специально искать опровержения и границы метода.

Запросы: `{topic} anti-patterns`, `{topic} common mistakes`, `{topic} failure modes`, `{topic} incident`, `{topic} postmortem`, `{topic} tradeoffs`, `{topic} limitations`.

Это обязательный проход для зрелой базы знаний: без него мы получаем рекламную, а не инженерную картину.

### P4 GAP ONLY

После первых проходов широкого поиска больше нет. Ищутся только незакрытые измерения конкретных тем.

Пример: если по `async Python` уже есть Python docs и книга, но нет failure evidence, запрос строится только под `async Python deadlock starvation cancellation failure postmortem`, а не повторяется общий `async Python`.

## 5. Когда останавливаем поиск

Поиск прекращается, когда тема либо собрана, либо её пробел явно зафиксирован.

Для MIN по каждой P0-теме нужны:

- authoritative basis **или явный `AUTHORITATIVE_GAP`**;
- практический материал **или `PRACTICE_GAP`**;
- validation/failure evidence **или `VALIDATION_GAP`**;
- provenance и SHA-256 для скачанных артефактов.

После первого прохода ищутся только GAP. Один и тот же запрос без новых доказательств не повторяется. На одну GAP-тему допускается максимум два дополнительных целевых прохода; затем сохраняется GAP как реальный результат исследования.

## 6. Что Telegram делает и чего не делает

Telegram полезен для:

- обнаружения книг, лекций, PDF, презентаций и чеклистов;
- поиска редких примеров и практических материалов;
- нахождения кандидатов по failure/anti-pattern темам;
- восстановления пробелов после первичного поиска.

Telegram не используется для:

- подтверждения действующего закона;
- определения канонической семантики языка/API вместо официальной документации;
- автоматического повышения найденного утверждения до факта KB;
- бесконечного role-wide scraping.

## 7. Как это выглядит на PROGRAMMER

Например, тема `concurrency and async Python`.

Ищем не «ещё одну книгу Python», а пакет:

- S0: официальные Python docs по `asyncio`, task/cancellation/threading semantics;
- S1: reference examples и API behavior;
- S2: хороший учебный разбор event loop/concurrency;
- S3: deadlock/starvation/cancellation mistakes, tests/benchmarks;
- S4: Telegram только для добора недостающего материала.

Тема считается исследованной не по числу PDF, а по закрытию этих измерений.

## 8. Производственные метрики

Для каждого прогона считаются отдельно:

`topics_total`, `topics_with_authoritative_basis`, `topics_with_practice`, `topics_with_validation_or_failure`, `topics_complete_for_min`, `explicit_gaps_total`, `queries_total`, `search_hits_total`, `media_candidates_total`, `downloaded_total`, `payload_reused_total`, `useful_candidate_ratio`, `errors_total`, `bytes_downloaded`, `elapsed_seconds`, throughput.

`speedup_vs_1_stream_pct` считается только после реального однопоточного прогона той же очереди. ETA — только при достаточной телеметрии.

## 9. Практический вывод после первого PROGRAMMER Telegram run

Первый Telegram-проход дал 281 hit, 18 файлов-кандидатов, 13 новых загрузок и 5 reuse при 16 темах. Это хороший acquisition result, но он **не доказывает закрытие PROGRAMMER MIN**, пока не проверено распределение материалов по темам и наличие authoritative basis / practice / validation dimensions.

Поэтому следующий шаг — не запускать ещё один общий поиск, а построить coverage matrix и второй проход только по реальным GAP.
