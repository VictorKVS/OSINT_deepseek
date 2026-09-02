# Architecture Baseline + Workbench M1 contract validation report

**Executed:** 2026-09-02  
**Scope:** `docs/osint-platform/schemas/*.json`, assigned `fixtures/CASE-SYNTH-0001/*.json`, query-plan hash, journal hash chain and graph references  
**Validator:** `jsonschema` Draft 2020-12 with format checking plus deterministic semantic integrity checks  
**Result:** PASS

## Results

- 21 schemas passed Draft 2020-12 meta-schema validation.
- 29 synthetic JSON fixtures passed their assigned schemas.
- Query-plan canonical SHA-256 check passed.
- Five append-only journal entries have contiguous sequence, valid `previous_entry_hash` linkage and valid canonical entry hashes.
- Graph nodes, edges and evidence-path object references passed integrity checks.
- Python validation utility passed bytecode compilation.
- No network acquisition was performed.
- No real person or organization was introduced into the public fixture.
- No `father_osint`, `poc`, `legacy`, collector, transport or existing DEV v1 test file was imported or modified.

## Important limitation

This is contract and fixture validation, not:

- a full repository regression run;
- a performance benchmark;
- proof of external-source availability;
- legal approval of a real investigation;
- production readiness.

Project time targets in `09_ACQUISITION_WORKBENCH_M1.md` are design SLOs, not measured production telemetry.

## Reproduce

```powershell
cd docs\osint-platform\validation
python -m pip install -r requirements.txt
python validate_contracts.py
```

Expected final line:

```text
PASS: 21 schemas meta-validated, 29 fixtures schema-validated, 4 semantic integrity checks passed.
```
