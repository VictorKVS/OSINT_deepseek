# Contract validation

```powershell
cd docs\osint-platform\validation
python -m pip install -r requirements.txt
python validate_contracts.py
```

The utility validates:

1. every `*.schema.json` against JSON Schema Draft 2020-12;
2. 29 assigned synthetic fixtures;
3. the canonical query-plan SHA-256;
4. the five-entry append-only journal hash chain;
5. graph node/edge/evidence-path references.

Скрипт не импортирует и не изменяет `father_osint`. Он работает только с contracts и полностью синтетическими fixtures.
