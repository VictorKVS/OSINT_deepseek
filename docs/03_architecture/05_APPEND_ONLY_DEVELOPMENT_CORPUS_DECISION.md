# ADR-style Decision — Append-Only Development Corpus / Решение по накопительной базе развития

**Date / Дата:** 2026-08-11  
**Status / Статус:** ACCEPTED  
**Related / Связано:** `Tree_F/TF-0001_2026-08-11_APPEND_ONLY_DEVELOPMENT_CORPUS_AND_SYNC_BASELINE.md`

## EN

### Context
The project already uses Git history, a living Development Journal, requirements, architecture documents, test plans and registries. These objects answer different questions but do not provide one compact append-only corpus of architecture generations, causes, experiments, defects, rollbacks and verification evidence.

### Decision
Introduce `Tree_F/` as an append-only development corpus.

Material engineering events receive sequential IDs `TF-0001`, `TF-0002`, ... . IDs are never reused. Existing records are not normally edited to rewrite history. When a prior decision becomes obsolete, it is marked `SUPERSEDED` and linked to the replacing record.

The current source of truth remains approved requirements, architecture, tests and living registries. `Tree_F` is lineage/evidence, not an alternative current architecture.

Material records are bilingual EN + RU.

### Consequences
Positive:
- reconstructable development history;
- explicit WHY next to file/component change evidence;
- easier onboarding and postmortems;
- security and operational lessons remain linked to the change that caused them;
- future engineering assistants can consume a curated historical corpus instead of raw commits alone.

Costs/risks:
- additional documentation work;
- possible duplication if authors copy current contracts into Tree_F;
- sensitive data could accidentally enter history.

Controls:
- only material events require TF records;
- current contracts remain elsewhere;
- security/legal sanitation overrides append-only preservation where necessary.

### Local workflow
Default Windows synchronization starts from:

```powershell
cd G:\1\PX00
git pull
```

For material updates, record pre/post SHAs and inspect file status using `git diff --stat` and `git diff --name-status` over explicit SHAs.

---

## RU

### Контекст
В проекте уже используются Git history, Development Journal, ТЗ, архитектурные документы, планы тестов и реестры. Каждый из этих объектов нужен, но вместе они не дают одной компактной накопительной базы архитектурных поколений, причин решений, экспериментов, ошибок, откатов и доказательств.

### Решение
Ввести `Tree_F/` как append-only базу развития.

Существенные инженерные события получают последовательные номера `TF-0001`, `TF-0002`, ... . Номера не переиспользуются. Историю обычными правками не переписываем. Если решение устарело, ставим `SUPERSEDED` и связываем его с новой записью.

Актуальным источником истины остаются утверждённые ТЗ, архитектура, тесты и живые реестры. `Tree_F` — это история/доказательства, а не параллельная актуальная архитектура.

Существенные записи ведём на EN + RU.

### Последствия
Плюсы:
- можно восстановить развитие системы;
- WHY хранится рядом с доказательством изменения файлов/компонентов;
- легче проводить onboarding и postmortem;
- выводы ИБ и эксплуатации остаются привязаны к конкретному изменению;
- будущие инженерные AI-помощники смогут использовать курированную базу, а не только сырые commits.

Цена/риски:
- дополнительная работа с документацией;
- риск дублирования актуальных контрактов;
- риск случайно записать чувствительные данные.

Контроли:
- TF нужен только для существенных изменений;
- текущие контракты живут в своих документах;
- security/legal sanitation важнее append-only правила, если нужно удалить секреты/ПДн/запрещённые данные.

### Локальный цикл
Базовая Windows-синхронизация:

```powershell
cd G:\1\PX00
git pull
```

Для существенных обновлений фиксируем SHA до/после и смотрим изменения через `git diff --stat` и `git diff --name-status` по конкретным SHA.
