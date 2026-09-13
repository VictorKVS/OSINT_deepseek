# Lesson 03 — Review / What Changed in Project Understanding

Status: `DOCUMENTATION_LAYER_COMPLETE / OWNER_REVIEW_REMAINS`

## What Lesson 03 added to the existing OSINT project

Lesson 03 did not introduce a new implementation. It clarified how the existing project should move through evidence-producing delivery stages.

New documentation views:
- discovery questions that block Product/MVP/Production certainty;
- explicit separation of Demo, PoC, MVP and Production;
- contract-model reasoning tied to uncertainty;
- staged risk matrix;
- stage gates and evidence expected at each transition;
- mapping of the existing TDLib/Telegram path into the PoC stage.

## What was already strong in the project

The existing repository already had several controls aligned with the lesson:
- capability/evidence-driven roadmap instead of invented dates;
- explicit PoC work item type;
- current TDLib PoC on the critical path;
- MUST/SHOULD/OPTION separation;
- WIP limits;
- Definition of Ready / Done;
- risk register;
- ADR threshold;
- change-impact analysis;
- clear statement that DEV baseline is not Production readiness.

Therefore the lesson mostly normalizes and extends the existing governance instead of replacing it.

## What remains UNKNOWN

- first externally useful MVP/product path;
- external customer/user segment for MVP;
- production workload and freshness targets;
- production deployment mode;
- legal/compliance authority and production data-processing boundaries;
- production SLO/support model;
- production TCO/budget envelope;
- commercial contract model for an external customer;
- production acceptance/risk authority.

These UNKNOWNs are visible and are not blockers for documenting the existing DEV/PoC project. They become blockers at the relevant MVP/Production gates.

## Gate interpretation

Current project status after Lesson 03:

```text
DEV BASELINE              = EXISTING_VERIFIED
DEMO                       = NOT REQUIRED AS A SEPARATE CLAIM
TECHNICAL POC PATH         = ACTIVE / M5 TDLib EVIDENCE PATH
MVP PRODUCT CHOICE         = UNKNOWN / OWNER DECISION REQUIRED
PRODUCTION READY           = NOT CLAIMED
```

Lesson 03 documentation result:

```text
LESSON_03_DOCUMENTATION = CONDITIONAL_PASS
```

Reason: the staged delivery model is defined and maps to current evidence, but MVP/Production business and operational parameters remain deliberately unresolved.

## Improvement Review

### What should be improved

1. Select one bounded MVP outcome before treating future Telegram work as a product MVP.
2. Define measurable product-value evidence for MVP, not only technical collector metrics.
3. Add production data/legal applicability before real-source scope expands materially.
4. Define production workload/freshness/SLO assumptions before sizing and TCO.
5. Formalize PoC reports with hypothesis → setup → raw evidence → conclusion → decision impact.
6. Add explicit stage-state badges to the live course master index/site later: DEV / PoC / MVP / Production.

### Priority

- legal/data production applicability: `P0` before Production/regulated live scope;
- MVP outcome and measurable value: `P1`;
- production workload/SLO: `P1`;
- standardized PoC report: `P1`;
- course/site visualization: `P2`.

### Owners

Product Owner, Legal/Compliance, Data Owner, Security, PM, QA, Operations and Architect according to artifact authority.

## Lesson 03 artifacts

- `01_DISCOVERY_QUESTIONS.md`
- `02_DELIVERY_STRATEGY_AND_CONTRACT.md`
- `03_POC_MVP_PROD_ROADMAP.md`
- `04_RISK_MATRIX.md`
- `05_STAGE_GATE_CRITERIA.md`
- `06_LESSON_03_REVIEW.md`

## Source basis

- OTUS Lesson 03 course description and homework.
- Existing `docs/PROJECT_ROADMAP_AND_CONTROL.md`.
- Existing `docs/PROJECT_EXECUTION_CONTROL.md`.
- Existing OSINT Agent requirements/architecture/verification evidence.
