# Tree_F — Append-Only Development Corpus / Накопительная база развития

## EN

`Tree_F` is the append-only engineering memory of FATHER / OSINT_deepseek.

It does **not** represent only the latest state. It preserves how the system evolved: requirements, architecture generations, alternatives, implementation decisions, defects, rollbacks, security findings, DevOps changes, tests, evidence and lessons learned.

### Core rule

For normal system evolution, existing `TF-xxxx` records are never deleted, overwritten or renumbered, and identifiers are never reused.

```text
TF-0001
TF-0002
TF-0003
TF-0004
...
```

Every material engineering change creates the next sequential record.

If a decision becomes obsolete, keep the original record and link the replacement:

```text
TF-0017
status: SUPERSEDED
superseded_by: TF-0023
```

The replacement record links back:

```text
TF-0023
supersedes: TF-0017
```

### What requires a TF record

Create a new TF record for a material change to one or more of:

- requirement / ТЗ;
- architecture or component boundary;
- accepted implementation approach;
- test or acceptance contract;
- security or supply-chain control;
- dependency/runtime/deployment model;
- rollback or recovery decision;
- material defect and its remediation;
- DevOps/CI/CD behavior;
- reusable capability or product opportunity;
- verified experiment / PoC result;
- significant file/component addition, removal, rename or retirement.

Formatting-only changes do not need a separate TF record.

### Required development order

```text
Development Journal
      ↓
Requirement / ТЗ
      ↓
Analysis / Architecture / Security / Reuse Review
      ↓
Acceptance + Security Test Design
      ↓
Implementation
      ↓
Regression + Security Verification
      ↓
Evidence Capture
      ↓
Tree_F record + Journal update
```

`Tree_F` does not authorize code by itself. The rule **NO CODE BEFORE CONTRACT** remains mandatory.

### Local sync baseline

The normal Windows working copy is expected at:

```powershell
cd G:\1\PX00
git pull
```

Before and after a material development step, capture enough Git evidence to reconstruct what changed:

```powershell
cd G:\1\PX00
git status --short
git rev-parse HEAD
git pull
git rev-parse HEAD
git status --short
git diff --stat HEAD~1..HEAD
git diff --name-status HEAD~1..HEAD
```

For a wider range, compare explicit SHAs rather than assuming one commit:

```powershell
git diff --stat <OLD_SHA>..<NEW_SHA>
git diff --name-status <OLD_SHA>..<NEW_SHA>
```

Each TF record should state what was **added, modified, removed, renamed**, why it changed, what requirement/decision caused it, what test proves it, what risks changed and what the next gate is.

### Security / legal sanitation exception

One exception exists to the append-only rule: if a secret, personal data, confidential material or legally prohibited content is accidentally recorded, security/legal sanitation is allowed and may require history rewriting.

The sensitive value itself must not be preserved merely for historical completeness. A safe record should remain describing that sanitation occurred, why it occurred and what preventive control changed, without reproducing the sensitive content.

### Language rule

Material Tree_F records are bilingual:

1. **EN** — engineering/repository-facing version;
2. **RU** — equivalent Russian explanation for maintainability and learning.

Code identifiers, commands, paths and test IDs remain unchanged.

---

## RU

`Tree_F` — это **накопительная инженерная память** проекта FATHER / OSINT_deepseek.

Она хранит не только последнее состояние системы, а историю её развития: ТЗ, поколения архитектуры, варианты решений, причины изменений, реализацию, ошибки, откаты, выводы ИБ, DevOps, тесты, доказательства и накопленный опыт.

### Главное правило

При обычном развитии системы существующие записи `TF-xxxx` **не удаляются, не перезаписываются, не перенумеровываются, а номера не используются повторно**.

```text
TF-0001
TF-0002
TF-0003
TF-0004
...
```

Каждое существенное инженерное изменение получает следующий последовательный номер.

Если решение устарело, старую запись не стираем:

```text
TF-0017
status: SUPERSEDED
superseded_by: TF-0023
```

А новая запись ссылается обратно:

```text
TF-0023
supersedes: TF-0017
```

Так сохраняется реальная история того, **почему система стала именно такой**.

### Когда создаём TF-запись

Новая запись нужна при существенном изменении:

- ТЗ / требования;
- архитектуры или границ компонентов;
- принятого способа реализации;
- приёмочного или security-контракта тестов;
- мер ИБ или supply chain;
- зависимостей, runtime или модели развёртывания;
- механизма отката/восстановления;
- существенного дефекта и его исправления;
- DevOps / CI/CD;
- повторно используемой возможности или продуктовой идеи;
- подтверждённого PoC/эксперимента;
- существенного добавления, удаления, переименования или вывода из эксплуатации файлов/компонентов.

Мелкое форматирование отдельной TF-записи не требует.

### Обязательная последовательность разработки

```text
Журнал разработки
      ↓
ТЗ / требование
      ↓
Аналитика / архитектура / ИБ / reuse-review
      ↓
Проектирование приёмочных + security-тестов
      ↓
Реализация
      ↓
Регрессионные + security-проверки
      ↓
Фиксация доказательств
      ↓
Tree_F + обновление журнала
```

`Tree_F` сама по себе не разрешает писать код. Правило **NO CODE BEFORE CONTRACT** сохраняется.

### Локальная синхронизация

Рабочая копия Windows используется по пути:

```powershell
cd G:\1\PX00
git pull
```

До и после существенного этапа фиксируем Git-состояние, чтобы потом можно было восстановить изменения:

```powershell
cd G:\1\PX00
git status --short
git rev-parse HEAD
git pull
git rev-parse HEAD
git status --short
git diff --stat HEAD~1..HEAD
git diff --name-status HEAD~1..HEAD
```

Если пришло несколько коммитов, сравниваем конкретные SHA:

```powershell
git diff --stat <OLD_SHA>..<NEW_SHA>
git diff --name-status <OLD_SHA>..<NEW_SHA>
```

В TF-записи фиксируем: **что добавлено, изменено, удалено, переименовано; почему; какое ТЗ/решение это вызвало; каким тестом доказано; какие риски изменились; что делаем дальше**.

### Исключение по ИБ / юридическим причинам

Если случайно записан секрет, персональные данные, конфиденциальный материал или содержимое, которое юридически нельзя хранить, допускается sanitation, включая при необходимости переписывание Git history.

Сам секрет ради «истории» не сохраняем. Оставляем безопасную запись о факте удаления, причине и введённом защитном контроле — без воспроизведения чувствительных данных.

### Язык

Существенные записи `Tree_F` ведём в двух версиях внутри файла:

1. **EN** — техническая версия для репозитория;
2. **RU** — равнозначное русское объяснение.

Имена кода, команды, пути и ID тестов не переводим.
