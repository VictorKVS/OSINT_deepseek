# FATHER OSINT Screening Factory M3

**Статус:** working deterministic kernel / passive-only / source adapters staged  
**Назначение:** постоянный фабричный контур проверки физических и юридических лиц в России и зарубежных юрисдикциях.

## Четыре производственных профиля

| Profile ID | Объект | Юрисдикция | Полный каталог проверок |
|---|---|---|---:|
| `RU_LEGAL_ENTITY` | юридическое лицо | Россия | 21 |
| `FOREIGN_LEGAL_ENTITY` | юридическое лицо | зарубежье | 20 |
| `RU_PERSON` | физическое лицо | Россия | 15 |
| `FOREIGN_PERSON` | физическое лицо | зарубежье | 15 |

Фактическое количество work items зависит от глубины `BASIC / STANDARD / ENHANCED / DEEP`.

## Производственная цепочка

```text
REQUEST + PURPOSE + LEGAL BASIS
        ↓
SUBJECT IDENTITY ANCHORS
        ↓
PROFILE SELECTION
        ↓
DEPENDENCY-AWARE PLAN
        ↓
FIVE PARALLEL STREAMS
        ↓
APPROVED SOURCE ADAPTERS
        ↓
SOURCE ATTEMPTS + EVIDENCE REFS
        ↓
FOUND / NO_HIT_IN_SCOPE / CONFLICT / BLOCKED / ERROR
        ↓
RED TEAM + HUMAN FACT GATE
        ↓
REPORT + DASHBOARD + RECHECK SCHEDULE
        ↓
APPEND-ONLY HASH-CHAIN JOURNAL
```

## Реализовано

- четыре конфигурационных профиля;
- 44 типизированных checks с depth, dependencies, criticality, freshness и source families;
- планировщик, который не скрывает недостающие идентификаторы;
- dependency waves и параллельный runner;
- реестр адаптеров с policy gate;
- `BLOCKED_NO_ADAPTER` вместо ложной галочки;
- раздельные `FOUND`, `NO_HIT_IN_SCOPE`, `CONFLICT`, `BLOCKED_*`, `ERROR`;
- сохранение независимых observations и source attempts;
- hash-chain journal;
- операционный recheck scheduler;
- русский Markdown-отчёт;
- автономный HTML-фасад с галочками Adapter / Evidence / Review;
- полностью офлайн синтетический demo;
- regression suite без сетевых запросов.

## Жёсткие ограничения

- фабрика не выполняет активное сканирование и не принимает произвольные shell-команды;
- совпадение имени, адреса, домена, телефона или username не создаёт доказанную связь;
- `FOUND` не равно `FACT`;
- `NO_HIT_IN_SCOPE` не доказывает отсутствие события или связи;
- санкционный/PEP/судебный матч требует точной идентификации и человеческой проверки;
- негативная публикация остаётся `SOURCE_CLAIM`, пока не подтверждена;
- сроки повторной проверки являются внутренней политикой, а не нормативным сроком;
- персональные данные собираются только в объёме, необходимом для заявленной цели.

## Запуск

```powershell
python -m screening_factory.cli catalog
python -m screening_factory.cli demo --output runtime/screening-factory-demo
python -m screening_factory.cli verify-journal runtime/screening-factory-demo/journal.jsonl
```

Создание плана:

```powershell
python -m screening_factory.cli plan `
  --kind LEGAL_ENTITY `
  --scope RUSSIA `
  --country RU `
  --name "ООО Пример" `
  --identifier inn=7700000000 `
  --identifier ogrn=1027700000000 `
  --region Москва `
  --purpose "Проверка контрагента перед договором" `
  --legal-basis "Внутренняя проверка по открытым данным" `
  --depth STANDARD `
  --risk MEDIUM `
  --output runtime/cases/CASE-001/plan.json
```

## Следующий инкремент

`M3A Provider Packs`: реальные управляемые адаптеры официальных источников с версией, правовым режимом, capture/hash, rate limits, smoke tests и test fixtures. До их подключения проверки честно остаются `BLOCKED_NO_ADAPTER`.
