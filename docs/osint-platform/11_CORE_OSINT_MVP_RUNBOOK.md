# 11. Core OSINT MVP v0.1 — runbook

## Требования

Windows 10/11 или Linux, Python 3.12+, запуск из корня репозитория. Runtime использует standard library; для проверки схем нужен `jsonschema`.

## Полная проверка

```powershell
Set-Location "G:\1\OSINT_deepseek"
python -m pip install -r requirements-dev.txt
python -m pip install -r docs\osint-platform\validation\requirements.txt
python -m pytest -q tests\test_osint_workbench_*.py
python scripts\run_osint_workbench_demo.py --root data\osint-workbench-demo --force
python scripts\validate_osint_workbench_demo.py `
  --root data\osint-workbench-demo `
  --case-id CASE-SYNTH-CORE-0001 `
  --schemas docs\osint-platform\schemas
```

Ожидается: `14 passed`, `status: PASS`, `18 schemas`, `50 generated objects`, `journal_valid: true`.

На Windows доступны:

```text
RUN_OSINT_WORKBENCH_VERIFY.cmd
RUN_OSINT_WORKBENCH_API.cmd
```

## Создать дело и пяти-поточный план

```powershell
python -m osint_workbench --root data\osint-workbench init-case `
  --title "Проверка поставщика" `
  --seed-type ORGANIZATION `
  --seed "ООО Пример" `
  --purpose "Проверить идентичность, связи, цифровой след и официальные факторы риска поставщика." `
  --legal-basis "Документированная внутренняя процедура управления рисками контрагентов." `
  --jurisdictions RU `
  --approve-plan `
  --reviewer-id analyst-001
```

Seed сохраняется как неподтверждённый capture; `FACT` не создаётся.

## Зарегистрировать и сохранить источник

```powershell
python -m osint_workbench --root data\osint-workbench add-source CASE-... `
  --url "https://example.org/document" `
  --title "Официальная выписка" `
  --publisher "Наименование органа" `
  --source-type OFFICIAL_DOCUMENT `
  --primary-level PRIMARY `
  --jurisdiction RU --language ru `
  --reliability-grade A_CONFIRMED `
  --legal-basis "Публичный официальный документ в рамках цели дела" `
  --republication-status METADATA_ONLY

python -m osint_workbench --root data\osint-workbench capture-file `
  CASE-... SRC-0001 "G:\evidence\document.pdf"
```

Текст можно передать через `capture-text`. Извлечение:

```powershell
python -m osint_workbench --root data\osint-workbench extract CASE-... SRC-0001 CAP-0001
```

Поддерживаются URL/domain, IPv4, public e-mail, phone, `@handle`, BTC/ETH/TRON strings. Выход — candidate entities и `MENTIONED_IN → DOCUMENT`, не ownership.

## Один пассивный GET

```powershell
python -m osint_workbench --root data\osint-workbench fetch-url `
  CASE-... QPLAN-0001 PVT-0003 "https://example.org/public-page" `
  --title "Публичная страница" --publisher Example `
  --jurisdiction RU --language ru `
  --legal-basis "Пассивное получение публичной страницы в утверждённом scope"
```

План должен быть `APPROVED`. Коллектор не выполняет login, cookies, JS, crawler, CAPTCHA bypass или active scan; raw response сохраняется с SHA-256.

## Разрешение тёзок

```powershell
python -m osint_workbench --root data\osint-workbench resolve `
  CASE-... ENT-0001 ENT-0014 --query-plan-id QPLAN-0001
```

Выход показывает similarity, conflicts, missing decisive evidence и human-review block. Auto-merge отсутствует.

## Утверждение finding человеком

```powershell
python -m osint_workbench --root data\osint-workbench approve-finding CASE-... `
  --classification FACT `
  --statement "Согласно официальной выписке организация зарегистрирована по указанному адресу." `
  --evidence-grade A_CONFIRMED `
  --sources SRC-0002 --claims CLM-0005 --entities ENT-0007,ENT-0008 `
  --reasoning "Первичный документ и capture содержат прямую регистрационную запись." `
  --limitations "Не подтверждает фактическое присутствие,Не подтверждает деятельность" `
  --approved-by-role "Главный аналитик" --red-team-status PASSED
```

Команды «автоматически сделать факт» нет.

## Coverage, graph, zoo, report, monitoring

```powershell
python -m osint_workbench --root data\osint-workbench coverage CASE-... FND-0001
python -m osint_workbench --root data\osint-workbench graph CASE-... --seed-refs ENT-0007 --bounded-hops 2
python -m osint_workbench --root data\osint-workbench analyze CASE-... `
  --task "Проверить provenance и возможный overclaiming" `
  --input-refs FND-0001,REL-0005,CLM-0005
python -m osint_workbench --root data\osint-workbench report CASE-... `
  --public --name main_official_report_redacted.md
python -m osint_workbench --root data\osint-workbench monitor CASE-... --label baseline
python -m osint_workbench --root data\osint-workbench verify-journal CASE-...
```

`NO_HIT` означает только отсутствие результата в проверенном объёме. При нарушении access/redaction/republication/provenance/review gates публичный отчёт блокируется.

## Read-only API

```powershell
python -m osint_workbench --root data\osint-workbench serve --host 127.0.0.1 --port 8765
```

```text
GET /health
GET /api/v1/cases
GET /api/v1/cases/{case_id}/summary
GET /api/v1/cases/{case_id}/objects/{kind}
GET /api/v1/cases/{case_id}/graph/latest
GET /api/v1/cases/{case_id}/reports
GET /api/v1/cases/{case_id}/evidence/{capture_id}/metadata
```

Локальный путь capture скрывается. POST/PUT/PATCH/DELETE возвращают `405 READ_ONLY_API`; bind разрешён только на loopback.
