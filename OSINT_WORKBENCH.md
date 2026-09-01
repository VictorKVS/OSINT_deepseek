# FATHER OSINT Workbench — Core MVP v0.1

Рабочий пассивный OSINT-контур, реализующий контракты `docs/osint-platform` отдельно от замороженного `father_osint` DEV v1.

```text
SEED → FIVE-STREAM QUERY PLAN → PASSIVE COLLECTION / INGEST
→ SOURCE + IMMUTABLE CAPTURE → CLAIM → ENTITY / RELATION
→ ENTITY RESOLUTION → ANALYSIS OPINIONS + DISSENT
→ HUMAN-APPROVED FINDING → COVERAGE + RESEARCH GAPS
→ DERIVED GRAPH → FORMAL REPORT → MONITOR SNAPSHOT
```

## Быстрый запуск

```powershell
python scripts/run_osint_workbench_demo.py --root data/osint-workbench-demo --force
python -m pip install -r docs/osint-platform/validation/requirements.txt
python scripts/validate_osint_workbench_demo.py `
  --root data/osint-workbench-demo `
  --case-id CASE-SYNTH-CORE-0001 `
  --schemas docs/osint-platform/schemas
python -m osint_workbench --root data/osint-workbench-demo serve
```

Затем открыть локально:

```text
http://127.0.0.1:8765/
http://127.0.0.1:8765/api/v1/cases
```

## Жёсткие границы

- нет свободной командной строки;
- нет активного сканирования, эксплуатации, подбора паролей, фишинга или перехвата;
- HTTP-коллектор выполняет один публичный `GET`, блокирует локальные/частные сети, credentials в URL и нестандартные порты;
- автоматическая модель, правило, transform или графовый алгоритм не создают `FACT`;
- публичный экспорт проходит проверку доступа, редактирования ПДн, републикации, доказательственной трассировки и человеческого review;
- совпадение имени, адреса, IP, домена, контакта или кошелька не означает общий контроль.

Подробности: `docs/osint-platform/10_CORE_OSINT_MVP_IMPLEMENTATION.md` и `11_CORE_OSINT_MVP_RUNBOOK.md`.
