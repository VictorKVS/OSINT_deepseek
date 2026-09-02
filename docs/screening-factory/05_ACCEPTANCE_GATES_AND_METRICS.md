# 05. Приёмочные ворота и производственные метрики

## Contract gates

- [ ] каждый request имеет цель, основание, объект, страну, depth и risk tier;
- [ ] каждый work item имеет code, dependency wave, source families и terminal semantics;
- [ ] ни один check не исчезает бесследно: применяется, блокируется или явно не применим;
- [ ] `NO_HIT_IN_SCOPE` содержит перечень попыток и границы поиска;
- [ ] `FOUND` содержит observation, source ID и evidence ref;
- [ ] `CONFLICT` сохраняет обе версии;
- [ ] отсутствующий provider отображается как `BLOCKED_NO_ADAPTER`;
- [ ] результат инструмента не получает статус FACT автоматически.

## Identity gates

- [ ] российское юрлицо по возможности разрешено по ИНН/ОГРН;
- [ ] зарубежное юрлицо разрешено по стране и регистрационному номеру;
- [ ] физическое лицо имеет достаточный lawful identity anchor либо явный gap;
- [ ] тёзки и одноимённые организации не объединяются автоматически;
- [ ] account candidate и person entity остаются разными объектами до атрибуции.

## Evidence gates

- [ ] сохраняется исходный результат адаптера;
- [ ] capture имеет timestamp, source/job IDs, MIME type и SHA-256;
- [ ] parser/adapter version зафиксированы;
- [ ] каждое существенное наблюдение открывается до evidence;
- [ ] повторный источник не считается независимым, если это копия/репост;
- [ ] изменение журнала обнаруживается hash-chain verification.

## Legal/data gates

- [ ] source access соответствует scope и условиям использования;
- [ ] активное воздействие запрещено;
- [ ] ПДн минимизированы;
- [ ] restricted data не попадают в публичный экспорт;
- [ ] санкционный статус ограничен конкретной юрисдикцией/режимом;
- [ ] судебный результат содержит роль стороны и процессуальный статус;
- [ ] adverse media не выдаётся за установленный факт;
- [ ] human review выполнен для high-impact results.

## Производственные метрики

Считать по каждому pass и накопительно:

```text
requests received / completed / blocked
lead time per profile and depth
checks planned / completed
adapter success / NO_HIT / conflict / error rate
source coverage by domain
identity-collision rate
high-impact human-review queue
rework share
false-positive and false-negative rate on labelled fixtures
observations accepted/rejected by analyst
capture/hash completeness
mean and p95 adapter latency
parallel speedup versus measured one-worker baseline
cost per useful reviewed finding
recheck backlog and overdue rate
```

### Правило статистики

Ускорение, throughput и прогноз окончания публикуются только при достаточной телеметрии. Синтетический demo не является оценкой реальной скорости официальных источников.

## Exit criteria M3

- [x] четыре профиля и пять потоков;
- [x] dependency-aware planner;
- [x] parallel runner;
- [x] adapter policy gate;
- [x] source attempts and evidence refs;
- [x] hash-chain journal;
- [x] report/dashboard/recheck;
- [x] offline regression tests;
- [ ] минимум по одному живому утверждённому adapter pack на каждый профиль;
- [ ] измеренная точность identity resolution;
- [ ] browser evidence recorder;
- [ ] signed Windows↔Kali job transport;
- [ ] restricted evidence store and RBAC;
- [ ] reviewed pilot cases without public PII leakage.
