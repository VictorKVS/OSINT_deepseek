# 2026-08-11 — Tree_F append-only development corpus / Накопительная база развития Tree_F

## EN

**Date:** 2026-08-11  
**Stage / milestone:** Cross-cutting project governance / Stage 07 M5 support  
**Trigger / problem:** Git history and living documents do not by themselves provide one compact append-only corpus of development generations, WHY, file changes, experiments, defects, rollbacks and verification evidence.  
**Decision:** Introduce `Tree_F/` with sequential immutable-under-normal-evolution records `TF-0001`, `TF-0002`, ...; never reuse IDs; supersede by links instead of rewriting history.  
**WHY:** Preserve architecture lineage and engineering learning while keeping approved requirements/architecture/tests as the current source of truth.  
**Commercial / reuse review:** Reusable for onboarding, postmortems, internal engineering assistants, architecture lineage, security lessons, regression reasoning and product retrospectives. No new commercial product is promoted.  
**Files/components affected:** `Tree_F/README.md`, `Tree_F/TF_TEMPLATE.md`, `Tree_F/TF-0001_2026-08-11_APPEND_ONLY_DEVELOPMENT_CORPUS_AND_SYNC_BASELINE.md`, `docs/03_architecture/05_APPEND_ONLY_DEVELOPMENT_CORPUS_DECISION.md`, this journal record.  
**Acceptance test / evidence:** append-only rules present; TF numbering starts at 0001; bilingual template exists; supersede links defined; local `G:\1\PX00` sync workflow documented; security/legal sanitation exception documented; runtime contracts unchanged.  
**Result:** PASS  
**New risks:** documentation duplication, accidental sensitive-data capture, over-documentation of trivial changes. Controls are defined in `Tree_F/README.md`.  
**Registry changes:** none.  
**Next action / next reuse-review gate:** after the next local `git pull`, capture pre/post SHAs and file-status evidence; create the next TF only for a new material engineering event.

---

## RU

**Дата:** 11.08.2026  
**Этап / веха:** Сквозное управление разработкой / поддержка Stage 07 M5  
**Причина / проблема:** Git history и живые документы сами по себе не дают одной компактной накопительной базы поколений разработки, причин WHY, изменений файлов, экспериментов, ошибок, откатов и доказательств.  
**Решение:** Ввести `Tree_F/` с последовательными записями `TF-0001`, `TF-0002`, ...; при обычном развитии записи не перезаписывать, номера не переиспользовать; устаревшие решения связывать через `SUPERSEDED`, а не стирать.  
**ПОЧЕМУ:** Сохранить происхождение архитектуры и накопленный инженерный опыт, при этом актуальным источником истины оставить утверждённые ТЗ, архитектуру и тесты.  
**Коммерческое / повторное использование:** Механизм пригоден для onboarding, postmortem, внутренних инженерных AI-помощников, анализа поколений архитектуры, ИБ-уроков, причин регрессий и продуктовых ретроспектив. Новая коммерческая разработка этой записью не запускается.  
**Затронутые файлы / компоненты:** `Tree_F/README.md`, `Tree_F/TF_TEMPLATE.md`, `Tree_F/TF-0001_2026-08-11_APPEND_ONLY_DEVELOPMENT_CORPUS_AND_SYNC_BASELINE.md`, `docs/03_architecture/05_APPEND_ONLY_DEVELOPMENT_CORPUS_DECISION.md`, эта запись журнала.  
**Приёмочный тест / доказательство:** правила append-only зафиксированы; нумерация начинается с TF-0001; существует двуязычный шаблон; определены связи supersede; описан локальный цикл `G:\1\PX00`; предусмотрено исключение security/legal sanitation; runtime-контракты не менялись.  
**Результат:** PASS  
**Новые риски:** дублирование документации, случайное сохранение чувствительных данных, чрезмерное документирование мелочей. Контроли описаны в `Tree_F/README.md`.  
**Изменения реестров:** нет.  
**Следующее действие / следующий reuse-review gate:** после следующего локального `git pull` зафиксировать SHA до/после и изменения файлов; следующий TF создавать только для нового существенного инженерного события.
