# Lesson 08 — Architecture Decision Records

Status: `ADR DISCIPLINE ADDED / EXISTING DECISIONS PRESERVED`

## Purpose

Introduce an immutable, reviewable ADR timeline for material architecture choices while preserving the existing `docs/03_architecture/04_DECISION_REGISTER.md` as the historical decision register.

## Rule

```text
Problem / Context
  ↓
Drivers + Constraints + Evidence
  ↓
Options / Alternatives
  ↓
Decision
  ↓
Consequences / Trade-offs
  ↓
Compliance / Verification
  ↓
Revisit triggers
```

A changed accepted decision is not silently rewritten. A new ADR supersedes the old one, preserving WHY and history.

## ADR threshold

Create standalone ADR when a decision:
- is costly/risky to reverse;
- affects multiple components/product paths;
- changes a trust boundary or external dependency;
- chooses a long-lived technology/provider/runtime strategy;
- would otherwise be repeatedly debated;
- materially changes security, data, cost or operations.

Trivial code details remain in code/review, not ADR.

## ADR states

- `PROPOSED`;
- `ACCEPTED`;
- `REJECTED`;
- `SUPERSEDED`;
- `DEFERRED`;
- `ACCEPTED_RETROSPECTIVE` — used only when this course creates a formal ADR for a decision already clearly accepted in the existing project record.

## Initial ADR index

| ADR | Decision | Status | Source decision |
|---|---|---|---|
| ADR-0001 | OSINT worker returns evidence package, not final expert truth | ACCEPTED_RETROSPECTIVE | ADR-CAND-001 + project mission |
| ADR-0002 | source observation identity is separate from reusable raw payload storage | ACCEPTED_RETROSPECTIVE | ADR-CAND-011 / semantic remediation |
| ADR-0003 | bounded follow-up research is required | ACCEPTED_RETROSPECTIVE | ADR-CAND-005 + acceptance criteria |
| ADR-0004 | LLM hosting policy | FUTURE / Lesson 09 | not decided here |

## Architecture-as-code direction

ADR, C4 source, schemas and decision evidence should live in Git and be reviewable/diffable. Rendered diagrams/PDFs are views; source text/YAML/DSL remains the maintainable record.

## Lesson result

`ADR_DISCIPLINE_READY = PASS FOR DOCUMENTATION`

The project already has decisions; this lesson adds a durable standalone ADR mechanism without claiming that all historic decisions have already been migrated.
