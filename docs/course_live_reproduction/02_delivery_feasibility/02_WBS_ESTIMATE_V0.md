# Lesson 02 — WBS / Estimate v0

Status: `WORK STRUCTURE READY / NUMERIC ESTIMATE NOT BASELINED`

## WBS v0 — current path

| WBS | Work package | Output/evidence | Estimation state | Key uncertainty |
|---|---|---|---|---|
| W0 | Product/requirements normalization | course/Product/requirements docs | KNOWN WORK ITEM | owner review depth |
| W1 | M5 Telegram requirements/security | approved requirement + security constraints | PARTLY EXISTING | live operational boundary |
| W2 | TDLib technical PoC | raw operational evidence / Tree_F / PoC report | ACTIVE EVIDENCE PATH | network/session/rate behavior |
| W3 | comparative transport evidence if decision value remains | comparable PoC report | CONDITIONAL | whether second donor adds value |
| W4 | Transport ADR | decision + trade-offs + rollback | BLOCKED BY POC EVIDENCE | donor comparison outcome |
| W5 | M5 acceptance test design | executable acceptance/security tests | PLANNED | final transport contract |
| W6 | M5 implementation | bounded Telegram Radar capability | BLOCKED BY ADR/TESTS | operational defects |
| W7 | M5 verification/freeze | regression + security + restart/provenance evidence | BLOCKED BY IMPLEMENTATION | live failure cases |
| W8 | M6 artifact ingestion | document/media evidence pipeline | FUTURE | format/security scope |
| W9 | M7 semantic/local extraction | extraction/transcription/model layer | FUTURE | model/provider/data policy |
| W10 | M8 Knowledge Gate | governed promotion/revision | FUTURE | authority/review model |

## Estimate methods

### Bottom-Up

Use after work packages have observable outputs and responsible roles. Decompose only to a level that materially improves the estimate.

### PERT

For uncertain R&D/PoC work:

`E = (O + 4M + P) / 6`

`sigma = (P - O) / 6`

O/M/P are estimates, not facts. Each requires WHY/evidence.

### Analogous

Allowed only with an identified comparable project/work item and explicit differences.

### Parametric

Coefficient/source/range must be recorded; no unexplained project-wide multipliers.

## Current numeric position

No new project hours/dates are asserted in this documentation pass because measured team capacity and per-work-item estimate evidence are not available here.

Required next estimation inputs:
- owner/role for each active WBS item;
- O/M/P or bottom-up task estimate;
- dependency/parallelism assumptions;
- availability/capacity of contributors;
- risk buffer links;
- external procurement/provider lead times where applicable.

## Confidence rule

A narrow date range without supporting estimate inputs is lower-quality evidence than a wider explicit range with assumptions.
