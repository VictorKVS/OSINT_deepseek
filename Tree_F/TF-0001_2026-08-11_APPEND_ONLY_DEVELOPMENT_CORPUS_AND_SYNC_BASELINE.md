# TF-0001 — Append-Only Development Corpus and Local Sync Baseline

```yaml
id: TF-0001
date: 2026-08-11
status: ACTIVE
supersedes: null
superseded_by: null
stage: Stage 07 / M5 — Telegram Radar
change_class: ARCH
old_sha: null
new_sha: null
related_requirements:
  - docs/PROJECT_EXECUTION_CONTROL.md
  - docs/DEVELOPMENT_JOURNAL.md
related_tests: []
related_adrs:
  - docs/03_architecture/05_APPEND_ONLY_DEVELOPMENT_CORPUS_DECISION.md
related_journal_entries:
  - J-018
```

## EN

### Trigger / problem
The repository already contains strong requirements, architecture, testing and verification documents, but long-term engineering evolution needs an explicit append-only memory that records not only the current truth but also the sequence of decisions that produced it.

The local Windows workflow also needs a repeatable synchronization/evidence pattern around:

```powershell
cd G:\1\PX00
git pull
```

Without a dedicated accumulated corpus, older decisions may become hard to reconstruct from Git history and living documents alone.

### Requirement / ТЗ
Preserve traceable engineering evolution without replacing the existing Development Journal, ADR/decision documents or Git history.

The corpus must answer for each material change:

- what changed;
- why it changed;
- which requirement authorized it;
- what was added/modified/removed/renamed;
- which test/evidence proves it;
- which risks changed;
- whether a prior decision was superseded;
- what the next controlled gate is.

### Analysis / architecture / security / reuse review
Three mechanisms already exist but serve different purposes:

1. Git history records commits and diffs but not always complete engineering WHY.
2. `docs/DEVELOPMENT_JOURNAL.md` records important living project decisions and status.
3. Architecture/requirements/test documents record the currently applicable contract.

`Tree_F` therefore becomes a fourth complementary layer: an append-only engineering corpus of material development events.

It must not become a second source of truth for current architecture. Current truth still lives in approved requirements/architecture/tests and living registries. `Tree_F` preserves how that truth evolved.

Security review identified one necessary exception: secrets, personal data, confidential data or legally prohibited content must be sanitizable even if this requires history rewriting. The sensitive content itself is never retained merely to preserve append-only history.

Reuse value: the same mechanism can later support postmortems, onboarding, training data for internal engineering assistants, architecture lineage analysis, security lessons, regression reasoning and product-development retrospectives.

### Test contract before code
This is a documentation/governance change. Acceptance evidence is structural:

- `Tree_F/README.md` exists and defines append-only rules;
- `Tree_F/TF_TEMPLATE.md` exists and captures bilingual change evidence;
- first numbered record is `TF-0001`;
- numbering is sequential and non-reusable;
- superseded decisions are linked instead of overwritten;
- local sync commands are documented;
- security/legal sanitation exception is explicit;
- Development Journal references the new control;
- no product/runtime contract is changed.

### Decision
Create `Tree_F/` as the append-only development corpus.

Number records sequentially as `TF-0001`, `TF-0002`, ... . Existing records are immutable under normal evolution and IDs are never reused.

Use `status: SUPERSEDED` plus `superseded_by` / `supersedes` links when an older decision is replaced.

All material records are bilingual EN + RU.

### WHY
Git tells us *what bytes changed*. Living requirements tell us *what is currently valid*. The Development Journal tells us *which major project decisions matter now*.

None of those alone guarantees a compact, durable, chronological corpus of engineering generations and evidence.

`Tree_F` fills that gap without replacing any existing control object.

### Local sync / Git evidence
Standard local start:

```powershell
cd G:\1\PX00
git status --short
git rev-parse HEAD
git pull
git rev-parse HEAD
git status --short
```

Then compare explicit old/new SHAs when available:

```powershell
git diff --stat <OLD_SHA>..<NEW_SHA>
git diff --name-status <OLD_SHA>..<NEW_SHA>
```

The first Tree_F governance files are being created directly in GitHub, so this record intentionally does not invent local `OLD_SHA` / `NEW_SHA` values. Local synchronization evidence will be captured on the next workstation pull.

### Files/components changed

#### Added
- `Tree_F/README.md`
- `Tree_F/TF_TEMPLATE.md`
- `Tree_F/TF-0001_2026-08-11_APPEND_ONLY_DEVELOPMENT_CORPUS_AND_SYNC_BASELINE.md`
- `docs/03_architecture/05_APPEND_ONLY_DEVELOPMENT_CORPUS_DECISION.md`

#### Modified
- `docs/DEVELOPMENT_JOURNAL.md`

#### Removed
- none

#### Renamed / moved
- none

### Implementation summary
Governance/documentation only. No runtime or product code is authorized or changed by TF-0001.

### Verification / evidence
Structural repository verification plus next local `git pull` evidence.

No DEV v1 runtime regression test is required solely for these documentation-only changes, but the frozen baseline remains mandatory before any later code integration.

### Result
`PASS`

### New / changed risks
- risk of duplicating current architecture truth across documents;
- risk of recording secrets or personal data in historical records;
- risk of excessive documentation for trivial changes.

Controls:
- Tree_F is history/evidence, not the current contract;
- security/legal sanitation exception;
- formatting-only/minor changes do not require a TF record.

### Registry changes
None.

### Rollback / replacement path
The mechanism may later be superseded by a more structured engineering knowledge system, but TF-0001 itself remains preserved and linked to its successor.

### Next action / next gate
On the next local workstation synchronization:

1. run `cd G:\1\PX00`;
2. capture current SHA/status;
3. run `git pull`;
4. capture new SHA/status;
5. inspect added/modified/removed files;
6. create the next TF record only if the synchronized change represents a material engineering event not already covered by TF-0001.

---

## RU

### Причина / проблема
В репозитории уже хорошо ведутся ТЗ, архитектура, тесты и верификация, но для долгого развития нужна отдельная накопительная память, которая хранит не только текущее правильное состояние, но и последовательность решений, приведших к нему.

Нужно также стандартизировать локальный Windows-цикл вокруг:

```powershell
cd G:\1\PX00
git pull
```

Чтобы рядом всегда можно было восстановить: что пришло, почему это появилось, какие файлы добавлены/изменены/удалены/переименованы и чем изменение доказано.

### Требование / ТЗ
Сохранять прослеживаемую историю инженерного развития, не заменяя существующие Development Journal, ADR/архитектурные документы и Git history.

Для каждого существенного изменения база должна отвечать:

- что изменилось;
- почему;
- какое требование разрешило изменение;
- что добавлено/изменено/удалено/переименовано;
- каким тестом или доказательством подтверждено;
- какие риски изменились;
- заменено ли предыдущее решение;
- какой следующий Gate.

### Аналитика / архитектура / ИБ / повторное использование
У нас уже есть три механизма:

1. Git history хорошо показывает commits/diff, но не всегда полный инженерный WHY.
2. `docs/DEVELOPMENT_JOURNAL.md` хранит важные живые решения и состояние проекта.
3. ТЗ/архитектура/тесты описывают действующий контракт.

`Tree_F` становится четвёртым, дополняющим слоем — неизменяемой при обычной эволюции хронологией существенных инженерных событий.

Она **не должна становиться второй копией актуальной архитектуры**. Истина о текущем состоянии остаётся в утверждённых ТЗ, архитектуре, тестах и реестрах. `Tree_F` хранит историю развития этой истины.

По ИБ необходимо исключение: секреты, ПДн, конфиденциальные данные и юридически запрещённые материалы можно и нужно удалять/sanitize, даже если потребуется переписать историю. Сам чувствительный материал ради «неизменяемости» не сохраняется.

Повторное использование этой базы возможно для postmortem, обучения новых участников, внутренних инженерных AI-помощников, анализа архитектурных поколений, ИБ-уроков, регрессий и ретроспектив продуктовой разработки.

### Контракт тестов до кода
Это изменение документации и governance, поэтому проверяем структуру:

- существует `Tree_F/README.md` с правилами;
- существует `Tree_F/TF_TEMPLATE.md`;
- первая запись имеет номер `TF-0001`;
- номера последовательны и не переиспользуются;
- устаревшие решения связываются через `SUPERSEDED`, а не переписываются;
- команды локальной синхронизации описаны;
- исключение security/legal sanitation зафиксировано;
- Development Journal связан с новой системой;
- runtime/product contract не меняется.

### Решение
Создать `Tree_F/` как накопительную базу развития.

Нумерация: `TF-0001`, `TF-0002`, ... . Старые записи при обычной эволюции не удаляем, не перезаписываем и номера не используем повторно.

Если решение заменено, используем `status: SUPERSEDED` и связи `superseded_by` / `supersedes`.

Все существенные записи — EN + RU.

### ПОЧЕМУ
Git показывает, **какие байты изменились**. ТЗ и архитектура показывают, **что сейчас считается правильным**. Development Journal показывает **ключевые решения и состояние проекта**.

Но этого недостаточно для компактной накопительной базы архитектурных поколений, причин и доказательств.

`Tree_F` закрывает именно этот пробел и не заменяет существующие документы.

### Локальная синхронизация / Git-доказательства
Стандартное начало работы:

```powershell
cd G:\1\PX00
git status --short
git rev-parse HEAD
git pull
git rev-parse HEAD
git status --short
```

При наличии старого и нового SHA сравниваем:

```powershell
git diff --stat <OLD_SHA>..<NEW_SHA>
git diff --name-status <OLD_SHA>..<NEW_SHA>
```

Первые файлы `Tree_F` сейчас создаются непосредственно в GitHub, поэтому мы не выдумываем локальные `OLD_SHA` / `NEW_SHA`. Их зафиксируем при следующем `git pull` на рабочем компьютере.

### Изменённые файлы / компоненты

#### Добавлено
- `Tree_F/README.md`
- `Tree_F/TF_TEMPLATE.md`
- `Tree_F/TF-0001_2026-08-11_APPEND_ONLY_DEVELOPMENT_CORPUS_AND_SYNC_BASELINE.md`
- `docs/03_architecture/05_APPEND_ONLY_DEVELOPMENT_CORPUS_DECISION.md`

#### Изменено
- `docs/DEVELOPMENT_JOURNAL.md`

#### Удалено
- ничего

#### Переименовано / перемещено
- ничего

### Кратко о реализации
Только governance/documentation. TF-0001 не разрешает и не изменяет runtime/product code.

### Проверка / доказательства
Проверка структуры репозитория и следующая локальная синхронизация через `git pull`.

Для чисто документационных изменений отдельный прогон DEV v1 не обязателен, но перед последующей интеграцией кода замороженный regression baseline остаётся обязательным.

### Результат
`PASS`

### Новые / изменённые риски
- дублирование актуальной архитектуры в исторических документах;
- случайная запись секретов/ПДн;
- чрезмерная документация мелочей.

Контроли:
- Tree_F — история/доказательства, а не действующий контракт;
- security/legal sanitation;
- мелкое форматирование и несущественные изменения отдельного TF не требуют.

### Изменения реестров
Нет.

### Откат / замена
В будущем механизм может быть заменён более структурированной инженерной knowledge system. Тогда TF-0001 не стирается, а получает ссылку на заменившее решение.

### Следующее действие / Gate
При следующей синхронизации рабочего компьютера:

1. `cd G:\1\PX00`;
2. зафиксировать текущий SHA и status;
3. выполнить `git pull`;
4. зафиксировать новый SHA и status;
5. посмотреть added/modified/removed files;
6. создать следующий TF только если пришедшее изменение является новым существенным инженерным событием, ещё не покрытым TF-0001.
