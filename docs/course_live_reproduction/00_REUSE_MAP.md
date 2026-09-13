# Existing OSINT evidence reused by the course project

The live reproduction package is an overlay, not a parallel documentation universe.

## Existing evidence we keep canonical

| Existing artifact | Reused as |
|---|---|
| `README.md` | current project mission, lifecycle and verified DEV status |
| `docs/OSINT_AGENT_TZ_V1.md` | current reviewed technical requirements and acceptance baseline |
| `docs/03_architecture/01_BUSINESS_ANALYSIS.md` | existing business-analysis evidence |
| `docs/03_architecture/02_ARCHITECTURE_VIEWS.md` | existing context/logical/process/data views |
| `docs/03_architecture/03_ARCHITECTURE_REVIEW.md` | architecture-review evidence |
| `docs/03_architecture/04_DECISION_REGISTER.md` | decision history / rationale |
| `docs/04_testing/` | acceptance/security test-design evidence |
| `docs/06_verification/` | verification and baseline-freeze evidence |
| `docs/TRACEABILITY_MATRIX.md` | current requirement→architecture→test→code→evidence links |
| `docs/SECURITY_THREAT_REGISTER.md` | living security/supply-chain threat evidence |
| `docs/SECURITY_TOP100_CONTROL_CATALOG.md` | broad control/coverage aid |
| `docs/OPERATIONS_GOVERNANCE_MODEL.md` | production role separation and operations-control intent |
| `docs/PROJECT_ROADMAP_AND_CONTROL.md` | capability roadmap / project risk / gates |
| `docs/PROJECT_EXECUTION_CONTROL.md` | work-control and change-impact policy |
| `father_osint/` | current DEV implementation baseline |
| `tests/` | executable contract evidence |
| `.github/` | CI evidence and automation surface |

## Missing layers we add for the course

The current repository starts relatively close to a technical specification. For an end-to-end course narrative we add earlier evidence:

```text
Client / Sponsor context
  ↓
Business Need
  ↓
Product Vision / Users / Value / Scope / Metrics
  ↓
Stakeholders / Decision Authority
  ↓
Business Process / Journeys / Rules / Glossary
  ↓
Security / Legal / Data intake
  ↓
System Model
  ↓
Requirements / NFR
  ↓
Delivery Feasibility / Estimate v0 / TCO / Project Risk
```

Then we link those layers into the existing architecture, tests, code and verification rather than replacing them.

## Existing facts vs retrospective reconstruction

Because some implementation already exists, early-course documents are **retrospective engineering reconstruction** based on repository evidence. They must be marked as such.

A reconstructed document may say:

- `FACT_FROM_EXISTING_REPO` — directly supported by current project documents/code/tests;
- `OWNER_CONFIRMATION_REQUIRED` — plausible project intent that requires project-owner confirmation;
- `UNKNOWN` — not evidenced and not guessed;
- `FUTURE_DECISION` — intentionally deferred to a later lesson/gate.

This distinction is mandatory so the course package does not rewrite project history as if all documents had existed before the code.
