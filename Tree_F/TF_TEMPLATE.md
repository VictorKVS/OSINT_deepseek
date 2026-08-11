# TF-XXXX — <TITLE>

```yaml
id: TF-XXXX
date: YYYY-MM-DD
status: ACTIVE
supersedes: null
superseded_by: null
stage: <stage / milestone>
change_class: <REQ | ARCH | TEST | CODE | SEC | DEVOPS | DEFECT | ROLLBACK | POC | OPP | OTHER>
old_sha: <optional>
new_sha: <optional>
related_requirements: []
related_tests: []
related_adrs: []
related_journal_entries: []
```

## EN

### Trigger / problem
<What changed or what problem required work?>

### Requirement / ТЗ
<Which approved requirement authorizes this change?>

### Analysis / architecture / security / reuse review
<What was analyzed before implementation? Alternatives, boundaries, threats, reuse/commercial implications.>

### Test contract before code
<Which acceptance/security test must pass before the implementation can be considered correct?>

### Decision
<What was decided?>

### WHY
<Why this decision and not a simpler/alternative one?>

### Local sync / Git evidence

```powershell
cd G:\1\PX00
git status --short
git rev-parse HEAD
git pull
git rev-parse HEAD
```

```text
OLD_SHA: <...>
NEW_SHA: <...>
```

Compare:

```powershell
git diff --stat <OLD_SHA>..<NEW_SHA>
git diff --name-status <OLD_SHA>..<NEW_SHA>
```

### Files/components changed

#### Added
- <path>

#### Modified
- <path>

#### Removed
- <path>

#### Renamed / moved
- <old> -> <new>

### Implementation summary
<What code/config/docs actually changed?>

### Verification / evidence
<Commands, test IDs, CI evidence, benchmark evidence, runtime evidence.>

### Result
`PASS | PARTIAL | REWORK | DEFERRED | ROLLED_BACK`

### New / changed risks
- <risk>

### Registry changes
<Product/security/threat/dependency registry changes, or NONE.>

### Rollback / replacement path
<How can this change be disabled, reverted, superseded or replaced?>

### Next action / next gate
<Next controlled development step.>

---

## RU

### Причина / проблема
<Что изменилось или какая проблема потребовала работы?>

### Требование / ТЗ
<Какое утверждённое требование разрешает это изменение?>

### Аналитика / архитектура / ИБ / повторное использование
<Что было проанализировано до реализации? Альтернативы, границы, угрозы, reuse/commercial implications.>

### Контракт тестов до кода
<Какой приёмочный/security-тест должен пройти, чтобы реализация считалась корректной?>

### Решение
<Что решили?>

### ПОЧЕМУ
<Почему выбрано именно это решение, а не более простое или альтернативное?>

### Локальная синхронизация / Git-доказательства

```powershell
cd G:\1\PX00
git status --short
git rev-parse HEAD
git pull
git rev-parse HEAD
```

```text
OLD_SHA: <...>
NEW_SHA: <...>
```

Сравнение:

```powershell
git diff --stat <OLD_SHA>..<NEW_SHA>
git diff --name-status <OLD_SHA>..<NEW_SHA>
```

### Изменённые файлы / компоненты

#### Добавлено
- <path>

#### Изменено
- <path>

#### Удалено
- <path>

#### Переименовано / перемещено
- <old> -> <new>

### Кратко о реализации
<Что фактически изменилось в коде/config/docs?>

### Проверка / доказательства
<Команды, ID тестов, CI, benchmark, runtime evidence.>

### Результат
`PASS | PARTIAL | REWORK | DEFERRED | ROLLED_BACK`

### Новые / изменённые риски
- <risk>

### Изменения реестров
<Изменения Product/Security/Threat/Dependency Registry или NONE.>

### Откат / замена
<Как изменение можно отключить, откатить, заменить или supersede?>

### Следующее действие / Gate
<Следующий контролируемый этап разработки.>
