# TF-0006 — TDLib runtime DB key mismatch and reset decision

```yaml
id: TF-0006
date: 2026-08-11
status: ACTIVE
supersedes: null
superseded_by: null
stage: Stage 07 / M5 — Telegram Radar / POC-TD-01
change_class: DEFECT
related_requirements: [REQ-M5-001, POC-M5-001]
related_tests: [POC-TD-01]
related_adrs: []
related_journal_entries: []
```

## EN

### Trigger / problem
A live TDLib authorization retry reached `authorizationStateWaitTdlibParameters` and then TDLib returned `Wrong database encryption key` for the existing local runtime database under `G:\1\father-tdlib\runtime`.

The environment variable `FATHER_TDLIB_DB_KEY` was present, but its value did not match the key previously used to encrypt the existing TDLib database.

### Requirement / ТЗ
POC-TD-01 requires controlled local authorization with session/database state kept outside Git and protected by a non-empty database encryption key.

### Analysis / architecture / security / reuse review
The existing runtime contains TDLib database/session artifacts (`db.sqlite`, `db.sqlite-shm`, `db.sqlite-wal`, `td.binlog`). Because the encryption key does not match, the existing encrypted runtime cannot be safely resumed.

Do not delete the old runtime silently. Preserve it as operational evidence by moving it to a timestamped archive path outside the repository. Create a fresh runtime directory and a new random local database key outside Git.

This is an operational reset of PoC state only. It does not change FATHER domain contracts, transport abstractions, product requirements or production architecture.

### Test contract before code
No code change is authorized.

Operational acceptance criteria:
1. old runtime is preserved outside Git under an archive name;
2. new runtime directory is empty before launch;
3. a new non-empty random DB key is supplied only in the local process environment;
4. TDLib no longer returns `Wrong database encryption key` on `setTdlibParameters`;
5. POC-TD-01 continues to the next explicit auth state, explicit TDLib error or bounded timeout;
6. no secret/session files enter Git.

### Decision
Archive the current local runtime and start a fresh PoC runtime with a newly generated local encryption key.

### WHY
The previous DB key is not available or does not match the existing encrypted database. Repeated retries cannot repair an encryption-key mismatch. Preserving the old runtime maintains evidence and rollback context while a clean runtime restores deterministic testing.

### Files/components changed
#### Added
- `Tree_F/TF-0006_2026-08-11_TDLIB_RUNTIME_DB_KEY_MISMATCH_AND_RESET_DECISION.md`

#### Modified
- NONE

#### Removed
- NONE

#### Renamed / moved
- local runtime only, outside Git: `G:\1\father-tdlib\runtime` -> timestamped archive path

### Implementation summary
Documentation/operational decision only. No product or PoC source code change.

### Verification / evidence
Observed live error (secret-safe):
`TDLib returned an error during authorization: ... 'Wrong database encryption key'`

### Result
`PARTIAL`

### New / changed risks
- accidental deletion of useful PoC runtime evidence;
- accidental reuse/loss of local encryption keys across sessions;
- accidental placement of session/runtime artifacts inside Git.

### Registry changes
NONE. POC-TD-01 remains PARTIAL.

### Rollback / replacement path
The archived runtime remains available if the correct old key is later recovered. The new runtime can be discarded independently because it is PoC-only state outside Git.

### Next action / next gate
Archive the old runtime, create a fresh runtime and new external DB key, then retry POC-TD-01 without code changes.

---

## RU

### Причина / проблема
При повторном живом запуске TDLib дошёл до `authorizationStateWaitTdlibParameters`, после чего вернул `Wrong database encryption key` для существующей локальной базы в `G:\1\father-tdlib\runtime`.

Переменная `FATHER_TDLIB_DB_KEY` была задана, но её значение не совпадает с ключом, которым ранее была зашифрована существующая база TDLib.

### Требование / ТЗ
POC-TD-01 требует контролируемой локальной авторизации, при которой session/database state находится вне Git и защищён непустым ключом шифрования базы.

### Аналитика / архитектура / ИБ / повторное использование
В существующем runtime находятся артефакты базы/сессии TDLib (`db.sqlite`, `db.sqlite-shm`, `db.sqlite-wal`, `td.binlog`). При несовпадении ключа корректно продолжить эту зашифрованную базу нельзя.

Старый runtime молча не удаляем. Сохраняем его как operational evidence, переименовав в архивную папку с датой/временем вне репозитория. Затем создаём новый чистый runtime и новый случайный локальный DB key вне Git.

Это только operational reset PoC-состояния. Доменные контракты FATHER, транспортная абстракция, требования и production-архитектура не меняются.

### Контракт тестов до кода
Изменение кода не разрешается и не требуется.

Критерии приёмки:
1. старый runtime сохранён вне Git под архивным именем;
2. новый runtime до запуска пуст;
3. новый непустой случайный DB key существует только в локальном окружении процесса;
4. TDLib больше не выдаёт `Wrong database encryption key` на `setTdlibParameters`;
5. POC-TD-01 переходит к следующему явному auth-state, TDLib error или ограниченному timeout;
6. никакие секреты/session-файлы не попадают в Git.

### Решение
Архивировать текущий локальный runtime и начать новый чистый PoC runtime с новым локальным ключом шифрования.

### ПОЧЕМУ
Предыдущий DB key недоступен или не совпадает с существующей зашифрованной базой. Повторные запуски не исправят несовпадение ключа. Архивирование сохраняет доказательства и возможность вернуться к старой базе при обнаружении правильного ключа, а чистый runtime делает дальнейший тест детерминированным.

### Изменённые файлы / компоненты
#### Добавлено
- `Tree_F/TF-0006_2026-08-11_TDLIB_RUNTIME_DB_KEY_MISMATCH_AND_RESET_DECISION.md`

#### Изменено
- НЕТ

#### Удалено
- НЕТ

#### Переименовано / перемещено
- только локальный runtime вне Git: `G:\1\father-tdlib\runtime` -> архивная папка с timestamp

### Кратко о реализации
Только документация и operational decision. Код продукта и PoC не меняется.

### Проверка / доказательства
Фактическая безопасная ошибка live-run:
`TDLib returned an error during authorization: ... 'Wrong database encryption key'`

### Результат
`PARTIAL`

### Новые / изменённые риски
- случайное удаление полезных PoC-артефактов;
- потеря/путаница локальных ключей между сессиями;
- случайное попадание runtime/session в Git.

### Изменения реестров
НЕТ. POC-TD-01 остаётся PARTIAL.

### Откат / замена
Архивный runtime сохраняется и может быть использован, если правильный старый ключ позже найдётся. Новый PoC runtime можно удалить независимо, так как он находится вне Git.

### Следующее действие / Gate
Архивировать старый runtime, создать новый чистый runtime и новый внешний DB key, затем повторить POC-TD-01 без изменения кода.
