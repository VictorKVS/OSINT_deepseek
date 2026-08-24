# FATHER Development Traceability Standard

Status: MANDATORY

## Правило

Во всех разработках FATHER трассировка проектируется одновременно с функционалом. Нельзя сначала сделать модуль, сайт, агента или pipeline, а потом пытаться восстановить, кто что сделал и почему.

Для каждого нового development item обязателен `TRACEABILITY_PLAN.md`.

## Что пользователь должен понимать из трассировки

По любой операции должно быть видно:

1. кто инициировал действие;
2. какая роль/агент/процесс получил задачу;
3. какая команда или событие были отправлены;
4. какие входы использовались;
5. какое состояние было до запуска;
6. кто фактически исполнил команду;
7. какой результат получен;
8. где сохранены файлы, записи, SHA, отчёты и доказательства;
9. какое состояние получилось после выполнения;
10. какая следующая команда или решение стали возможны;
11. где были ошибки, retry, rework, блокировки и ручные подтверждения.

## Обязательная цепочка идентификаторов

`project_id → task_id → command_id → trace_id`

Для дочерних команд добавляется `parent_command_id`, а единая бизнес-операция связывается через `correlation_id`.

Это позволяет пройти путь, например:

`кнопка в OSINT UI → команда поиска → Telegram collector → найденный message_id → скачанный payload → SHA-256 → analyst review → KB promotion request`.

## Два слоя трассировки

### 1. Design trace

До реализации фиксируются:

- роли и зоны ответственности;
- RACI/role matrix;
- схема команд;
- схема состояний;
- входы и выходы этапов;
- ручные gates;
- места хранения evidence;
- ошибки, retry и rework paths.

### 2. Runtime trace

Во время выполнения пишется фактический event log. Минимальная запись содержит:

`trace_id, correlation_id, project_id, task_id, command_id, parent_command_id, actor_role, initiator, executor, trigger, command_name, input_refs, state_before, started_at, finished_at, status, output_refs, state_after, evidence_refs, error_ref, retry_of, rework_reason, human_approval_ref, next_command_ids`.

## Минимальные состояния

`PLANNED → QUEUED → RUNNING → PASS`

Дополнительные обязательные ветки:

`WAITING_HUMAN`, `FAILED`, `RETRY`, `REWORK`, `BLOCKED`, `CANCELLED`.

## Что должно быть видно на сайте

В каждом операторском интерфейсе должен быть раздел **Трассировка / Trace**. Для выбранной задачи он показывает:

- инициатора;
- исполнителя;
- команду;
- parent/child команды;
- входы и выходы;
- переход состояния;
- время выполнения;
- evidence/provenance;
- ошибки/retry/rework;
- следующий шаг.

Предпочтительное представление: одновременно timeline + command graph + таблица событий.

## Acceptance gate

Разработка не считается готовой к витрине, если нет `TRACEABILITY_PLAN.md`.

Разработка не считается operational, если фактические runtime-команды и результаты нельзя связать назад с task/command/trace IDs.

Любой результат без связи с породившей его командой считается **TRACEABILITY_DEFECT**.

## Пример для OSINT

```text
USER
  │ UI_SEARCH_001
  ▼
OSINT CONTROL CENTER
  │ CMD-SEARCH-00042
  ▼
COLLECTOR / TELEGRAM
  │ evidence: chat_id/message_id
  ▼
CANDIDATE
  │ CMD-ACQUIRE-00017
  ▼
LOCAL PAYLOAD + SHA256
  │ CMD-ANALYZE-00009
  ▼
ANALYST
  │ findings / conflicts / confidence
  ▼
HUMAN REVIEW
  │ CMD-PROMOTE-00003
  ▼
KB-READY
```

По любому узлу пользователь должен иметь возможность открыть предыдущую и следующую команду.
