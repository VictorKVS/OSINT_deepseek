# Baseline contract validation report

**Executed:** 2026-09-01  
**Scope:** `docs/osint-platform/schemas/*.json` and `fixtures/CASE-SYNTH-0001/*.json`  
**Validator:** `jsonschema` Draft 2020-12 with format checking  
**Result:** PASS

- 13 schemas passed meta-schema validation.
- 16 synthetic JSON fixtures passed their assigned schemas.
- No network acquisition was performed.
- No `father_osint`, `poc`, `legacy` or existing test file was imported or modified.
- This is contract validation, not a DEV v1 regression run.

Reproduce:

```powershell
cd docs\osint-platform\validation
python -m pip install -r requirements.txt
python validate_contracts.py
```
