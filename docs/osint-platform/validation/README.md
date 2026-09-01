# Contract validation

```powershell
cd docs\osint-platform\validation
python -m pip install -r requirements.txt
python validate_contracts.py
```

Скрипт не импортирует и не изменяет `father_osint`. Он проверяет только JSON Schema и полностью синтетические fixtures.
