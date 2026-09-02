# 02. Модель дела и доказательств

## Объекты

| Объект | Смысл |
|---|---|
| `CASE` | задача, цель, scope, основание, класс доступа |
| `SOURCE` | идентичность и оценка источника |
| `SOURCE_CAPTURE` | сохранённая неизменяемая копия |
| `CLAIM` | утверждение источника |
| `ENTITY` | лицо, организация, адрес, домен, документ, актив, событие |
| `RELATION` | типизированная связь |
| `ANALYSIS_RUN` | воспроизводимый запуск |
| `ANALYSIS_OPINION` | независимое мнение анализатора |
| `CONSENSUS` | согласия и разногласия без удаления меньшинства |
| `FINDING` | reviewed FACT / INFERENCE / HYPOTHESIS / RISK / DECISION |
| `AUDIT_EVENT` | кто, когда, что и почему изменил |
| `EXPORT_MANIFEST` | состав, исключения, хеши и ворота экспорта |

## Жизненный цикл

```text
DISCOVERED → CAPTURED → NORMALIZED → CLAIMED → ANALYZED
→ CHALLENGED → REVIEWED → APPROVED → EXPORTED → SUPERSEDED
```

Переходы фиксируются `AUDIT_EVENT`.

## Разделение смысла

- `SOURCE ≠ CLAIM`: публикация не подтверждает истинность содержания.
- `CLAIM ≠ FACT`: claim — «источник X сообщил Y»; fact — «Y принято установленным по политике проверки».
- `INFERENCE ≠ FACT`: inference хранит reasoning, assumptions, alternatives и limitations.
- `HYPOTHESIS ≠ ALLEGATION`: рабочая версия не должна выглядеть как установленное обвинение.

## Оценки

- `A_CONFIRMED`
- `B_HIGHLY_PROBABLE`
- `C_ANALYTICAL_HYPOTHESIS`
- `D_LEAD`

Помимо класса хранятся authority, directness, independence, corroboration, recency, ambiguity, bias и contradiction severity.

## Инварианты

1. Claim ссылается на source.
2. Материальный finding ссылается на claims/sources.
3. Relation открывает supporting sources.
4. Capture содержит SHA-256 и storage URI.
5. Opinion хранит inputs, limits и analyzer version.
6. FACT требует human approval.
7. Decision ссылается на risk/finding.
8. Export хранит хеш каждого файла.

## Даты

Различаются `event_at`, `effective_at`, `published_at`, `accessed_at_utc`, `captured_at_utc`, `analyzed_at_utc`, `reviewed_at_utc`, `exported_at_utc`. Неизвестная дата остаётся `null`.
