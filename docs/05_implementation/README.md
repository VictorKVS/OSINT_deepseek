# Stage 05 — Implementation Planning

**Status:** ACTIVE / STORAGE FIX ONLY

Stage 05 converts approved requirements, architecture decisions and failed acceptance tests into the smallest justified code change.

No code change is allowed in this stage until the plan is reviewed.

## Input chain

```text
OSINT_AGENT_TZ_V1
        ↓
Stage 03 Architecture Review
        ↓
Stage 04 Acceptance Tests
        ↓
TEST_REPORT_001
        ↓
Stage 05 Implementation Plan
        ↓
Implementation Review Gate
        ↓
only then: code change
```

## Current scope

Only DEF-001 / DEF-002 are authorized for planning:

- preserve separate source observations when payload text is identical;
- reuse raw blob storage when payload hash matches;
- preserve the same behavior across process restart.

Everything else remains frozen.

## Documents

- [01_STORAGE_SEMANTICS_PLAN.md](01_STORAGE_SEMANTICS_PLAN.md) — smallest compliant fix and alternatives.
- [02_IMPLEMENTATION_REVIEW.md](02_IMPLEMENTATION_REVIEW.md) — gate before editing production code.
