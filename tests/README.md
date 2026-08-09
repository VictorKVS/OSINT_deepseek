# Tests

Tests are evidence for the contract, not decorations around code.

## Required chain

```text
ТЗ acceptance criterion
        ↓
architecture responsibility
        ↓
test specification
        ↓
execution
        ↓
PASS/FAIL evidence
        ↓
KEEP / CHANGE / DELETE decision
```

## Existing tests

- `test_father_osint_mvp.py` — OSINT orchestration/storage behavior.
- `test_telegram_collector.py` — Telegram collector contract mapping.
- `test_simple_analyst.py` — DEV Analyst behavior.
- `test_dev_pipeline.py` — bounded OSINT↔Analyst cycle.
- `test_simple_socrates.py` — DEV Socrates behavior.

**Current status:** written but not yet accepted as evidence in the requirements-first process. Run them only after the mapping in `docs/TRACEABILITY_MATRIX.md` is reviewed, then record exact results.
