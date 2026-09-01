# PROGRAMMING_KB — что скачивает и разбирает Фабрика знаний

Статус: P0 / Россия / MIN foundation.

Главный принцип: сначала строится доказательная `PROGRAMMING_KB`, затем задачи связываются с её узлами и только после этого разрешается обучение модели.

## 1. Российская нормативная база

Скачиваем или регистрируем один раз в Global Document Registry:

- Федеральный закон № 162-ФЗ о стандартизации — актуальный официальный текст, редакции, даты действия;
- все активные ЕСПД / ГОСТ 19 из `config/programmer_ru_espd_inventory.json` — сейчас каталог содержит 28 активных стандартов и 1 исторически заменённый;
- ГОСТ Р ИСО/МЭК 12207-2010 и актуальные российские стандарты жизненного цикла/инженерии ПО;
- ГОСТ Р 56923-2016 и связанные стандарты качества/инженерии ПО;
- ГОСТ Р 56939-2024, ГОСТ Р 58412-2019, ГОСТ Р 71207-2024 и связанные стандарты безопасной разработки, анализа и испытаний;
- условный слой ГОСТ 34: ГОСТ Р 59853-2021, ГОСТ 34.201-2020, ГОСТ Р 59793-2021, ГОСТ 34.602-2020, ГОСТ Р 59792-2021;
- ФСТЭК/КИИ/ПДн/ГИС — только по условиям применимости, через общий реестр документов, без копирования юридической истины в роль;
- отраслевые overlays: медицина, финансы, телеком, энергетика, транспорт, госуслуги и др. — только при активации контекста.

Если полный текст стандарта законно недоступен автоматически, сохраняем официальную карточку/метаданные и ставим `TEXT_GAP`. Обход ограничений доступа запрещён.

## 2. Первичные источники языков

Для каждого языка скачиваем/индексируем официальную спецификацию, reference и стандартную библиотеку/платформенную документацию:

- Python — Language Reference, Standard Library, PEP index;
- Go — language specification, stdlib/package docs, официальное руководство;
- Java — JLS, JVM Specification, platform/API docs;
- C#/.NET — C# specification, runtime/API docs;
- C/C++ — актуальная информация о стандартах и авторитетные открытые рабочие материалы; поведение компиляторов — из первичной документации конкретного компилятора;
- Rust — Rust Reference, standard library, official language material;
- JavaScript/TypeScript — ECMAScript specification и официальные материалы TypeScript.

Из этих материалов извлекаем не страницы текста, а свойства языка: типизация, модель памяти, runtime, concurrency, стандартная библиотека, ограничения, version boundaries.

## 3. Правила выбора языка

Скачиваем/индексируем SWEBOK, ACM/IEEE-CS/AAAI CS2023, университетские и peer-reviewed материалы, а для производительности — воспроизводимые benchmark evidence.

Строим не рейтинг языков, а правила вида:

`контекст + ограничения -> допустимые языки -> trade-offs -> preferred/avoid -> основание`.

Критерии: регион/отрасль, безопасность памяти, latency/throughput, CPU/IO, concurrency, runtime/deployment, экосистема, сопровождение, компетенции команды, TCO, interoperability, lifecycle horizon.

## 4. Алгоритмы и структуры данных

Скачиваем открытые университетские курсы/конспекты с доказательствами и анализом сложности, ACM/IEEE algorithmics material, peer-reviewed материалы и при необходимости воспроизводимые benchmarks.

MIN-каталог постепенно покрывает:

- поиск и сортировку;
- hashing;
- массивы/списки/стэки/очереди;
- trees/heaps;
- graphs, BFS/DFS, shortest paths;
- union-find;
- greedy;
- dynamic programming;
- string algorithms;
- concurrency-relevant structures.

Каждый алгоритм раскладывается на:

`problem class -> preconditions -> invariant -> correctness basis -> time complexity -> space complexity -> data assumptions -> edge/failure cases -> alternatives -> selection rule`.

## 5. Инженерная компоновка и secure development

Скачиваем/индексируем NIST SSDF, OWASP ASVS/релевантные первичные OWASP-материалы, RFC для используемых протоколов, первичную документацию БД/фреймворков при достижении соответствующего слоя, Google SRE/DORA как эмпирическую эксплуатационную базу.

Извлекаем: secure-development rule, protocol rule, reliability rule, test rule, observability rule, decision card, pattern/anti-pattern.

## 6. Книги, конференции, GitHub, Telegram

Это вспомогательный слой.

- открытые/разрешённые книги и курсы — можно автоматически загружать;
- коммерческие книги — только собственные/разрешённые копии или библиографическая карточка;
- GitHub/конференции/статьи — примеры, case studies, candidate patterns;
- Telegram — discovery/candidate source, а не источник нормативной или технической истины.

## Что Фабрика знаний делает с каждым источником

1. Сохраняет `ORIGINAL`, URI, время получения, media type, SHA-256.
2. Создаёт `DOCUMENT` и `DOCUMENT_VERSION`.
3. Извлекает автора/издателя/орган, версии, даты публикации и действия, статус.
4. Разбирает структуру: часть -> глава -> раздел -> пункт -> таблица -> рисунок -> код -> пример.
5. Создаёт стабильные `CHUNK` с якорями на оригинал.
6. Извлекает `TERM` и `DEFINITION`.
7. Разделяет `FACT`, `CLAIM`, `REQUIREMENT`, `RECOMMENDATION`, `EXAMPLE`.
8. Выделяет условия, исключения, запреты, разрешения и рекомендации.
9. Выделяет сущности: стандарт, язык, алгоритм, структура данных, артефакт, роль, control, metric.
10. Присваивает класс источника и измерения доверия.
11. Создаёт `GAP`, если не хватает точного текста, актуальности, применимости или доказательства.

## Главные узлы PROGRAMMING_KB

- `REGION_PROFILE`
- `LEGAL_NORM`
- `STANDARD`
- `APPLICABILITY_RULE`
- `STANDARD_REQUIREMENT`
- `WORK_PRODUCT_RULE`
- `TERM` / `DEFINITION`
- `LANGUAGE` / `LANGUAGE_VERSION`
- `LANGUAGE_FEATURE` / `LANGUAGE_LIMITATION`
- `LANGUAGE_SELECTION_RULE`
- `ALGORITHM`
- `DATA_STRUCTURE`
- `PRECONDITION`
- `INVARIANT`
- `CORRECTNESS_BASIS`
- `COMPLEXITY_BOUND`
- `ALGORITHM_SELECTION_RULE`
- `DECISION_RULE` / `DECISION_CARD`
- `PATTERN` / `ANTI_PATTERN`
- `SECURITY_CONTROL`
- `TEST_RULE`
- `BENCHMARK_EVIDENCE`
- `EXAMPLE` / `COUNTEREXAMPLE`
- `GAP`

## Главные связи

- `APPLIES_IN_REGION`
- `MANDATORY_IF`
- `VOLUNTARY_UNLESS_ACTIVATED`
- `EFFECTIVE_FROM`
- `AMENDS` / `SUPERSEDES`
- `DEFINED_IN`
- `DERIVED_FROM`
- `SUPPORTED_BY`
- `CONFLICTS_WITH`
- `REQUIRES`
- `IMPLEMENTS`
- `PRODUCES_WORK_PRODUCT`
- `PREFERRED_WHEN` / `AVOID_WHEN`
- `HAS_FEATURE` / `HAS_LIMITATION`
- `HAS_PRECONDITION` / `HAS_INVARIANT` / `HAS_COMPLEXITY`
- `USES_DATA_STRUCTURE`
- `ALTERNATIVE_TO`
- `VERIFIED_BY` / `EVIDENCED_BY`
- `EXAMPLE_OF` / `COUNTEREXAMPLE_TO`
- `TEACHES` / `DEMONSTRATES`

## Как потом появятся задачи

Только после прохождения `PROGRAMMING_KB MIN`:

`TASK -> TEACHES -> KNOWLEDGE_NODE`

`TASK -> REQUIRES -> KNOWLEDGE_NODE`

`TASK -> VERIFIED_BY -> TEST_RULE`

`GOLDEN_CASE -> DEMONSTRATES -> DECISION_RULE`

`GOLDEN_CASE -> SUPPORTED_BY -> SOURCE`

До этого существующие 8 Golden Cases используются только как regression fixtures, существующие 40 derived candidates остаются `HOLD`, новая генерация задач и обучение модели приостановлены.

Машиночитаемый план: `config/programming_kb_acquisition_decomposition_plan.json`.
