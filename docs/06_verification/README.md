# Stage 06 — Verification and Repository Rationalization

**Status:** ✅ COMPLETE  
**Outcome:** **DEV v1 BASELINE FROZEN**

Stage 06 verified that the repository, contracts, tests, runtime dependencies and documentation describe the same small DEV product before any new functional growth.

No new production capability was the goal of this stage.

## Completed chain

```text
Approved ТЗ
  ↓
Architecture Review
  ↓
Acceptance Test Design
  ↓
Focused defect/fix evidence
  ↓
Static repository audit
  ↓
Clean-checkout verification
  ↓
Dependency + legacy cleanup
  ↓
Full project audit
  ↓
Semantic remediation
  ↓
Documentation consistency
  ↓
Final clean CI
  ↓
DEV v1 BASELINE FREEZE
```

## Final verified baseline

```text
Python 3.12
father_osint import       PASS
21 tests collected        PASS
21 tests executed         PASS
run_dev_osint.py          PASS
run_dev_pipeline.py       PASS
```

The current DEV core is stdlib-only; verification uses `pytest` from `requirements-dev.txt`.

## Material results

Stage 06 established and verified these semantics:

- independent source observations survive equal payload content;
- identical raw payloads may reuse SHA-256-addressed storage without collapsing provenance;
- follow-up research cycles review cumulative evidence;
- file-only Material is hashed from original file bytes;
- missing local files fail explicitly;
- collector failures are isolated and visible;
- the review loop is hard bounded;
- Telegram collection remains transport-neutral;
- no live transport, Knowledge Gate or production infrastructure is required to prove DEV v1.

## Repository rationalization

The active tree no longer contains the old duplicate pipeline, legacy `core/`, workstation/Ollama/GPU/PowerShell runtime, VIP prototype, experimental policy/"llm-gateway" implementation or Teleproto/Node bridge. Their useful lessons remain in Git history and audit records.

## Evidence pack

1. `01_STATIC_REPOSITORY_AUDIT.md` — initial file/group disposition.
2. `02_FULL_RUN_PLAN.md` — clean execution plan.
3. `03_TEST_REPORT_003.md` — earlier focused verification evidence.
4. `04_DEPENDENCY_AUDIT.md` — pipeline/dependency analysis.
5. `05_LEGACY_CORE_AUDIT.md` — legacy core lessons.
6. `06_LEGACY_RUNTIME_AUDIT.md` — historical runtime analysis.
7. `07_LLM_GATEWAY_AUDIT.md` — experimental policy subsystem analysis.
8. `08_CONFIG_DATA_AUDIT.md` — configuration/data boundaries.
9. `09_COMPONENT_TRACEABILITY_MAP.md` — current component ownership and verification map.
10. `10_DEPENDENCY_SPLIT.md` — current runtime vs DEV dependency decision.
11. `11_LEGACY_CLEANUP_REPORT.md` — evidence-based cleanup record.
12. `12_TELEGRAM_EXPERIMENT_AUDIT.md` — Teleproto/Node experiment disposition.
13. `13_LLM_GATEWAY_DISPOSITION.md` — experimental gateway removal decision.
14. `14_FULL_PROJECT_AUDIT_2026-08-09.md` — full-project audit findings.
15. `15_SEMANTIC_REMEDIATION_PLAN.md` — cumulative evidence, payload reuse and file hashing remediation contract.

## Freeze rule

DEV v1 freeze means:

- current behavior is the reference baseline;
- future changes must identify which approved requirement they satisfy;
- no feature is added merely because a library or prototype exists;
- every new capability re-enters the lifecycle at requirements/business analysis, not at code.

Freeze does **not** mean production readiness. Live Telegram, Tor/dark-web access, local transcription, generic Artifact ingestion, Knowledge Gate, expert Analyst/Socrates and production observability remain future separately approved requirements.

## Next gate

**M5 — choose the next approved business requirement.**

See `../DEVELOPMENT_JOURNAL.md` for the current roadmap and `16_DEV_V1_BASELINE_FREEZE.md` for the formal closure record.
