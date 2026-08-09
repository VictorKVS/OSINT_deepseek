# Legacy Core

`core/` belongs to the original OSINT_deepseek prototype and predates the current FATHER requirements-first package.

Current files:
- `agent_tracker.py` — legacy agent tracking/monitoring logic.
- `logger.py` — legacy logging support.

Status: **LEGACY / PRESERVE / REVIEW LATER**.

Do not import these modules into the new `father_osint` path merely to reuse code. First identify an approved requirement, compare behavior, write/locate an acceptance test, then decide `KEEP / ADAPT / RETIRE`.
