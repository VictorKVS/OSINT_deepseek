# ADR-0003 — Follow-up Research Must Be Bounded and Cumulative

Status: `ACCEPTED_RETROSPECTIVE`

Source decision: `ADR-CAND-005`, current requirements and acceptance criteria.

## Context

Analyst/Reviewer may discover evidence gaps after an initial research cycle. An unconstrained autonomous loop can create cost, rate-limit, storage and availability problems. A non-cumulative loop can also lose earlier evidence and repeatedly recollect satisfied source classes.

## Drivers

- bounded cost/time/resource use;
- auditability;
- cumulative evidence;
- explicit stop reasons;
- prevention of runaway agent loops.

## Options

### A — unbounded research-until-satisfied loop

Flexible but operationally unsafe and difficult to test.

### B — fixed single-pass research

Simple but cannot close meaningful evidence gaps.

### C — bounded cumulative cycles with targeted follow-up

Preserves earlier evidence, narrows later collection to gaps and has hard stop controls.

## Decision

Select **C**.

Each follow-up is another explicit `ResearchTask`. Previous evidence remains available to Analyst/Reviewer. Cycle/item/time/cost controls must stop uncontrolled work; unresolved evidence may end as UNKNOWN rather than infinite research.

## Consequences

Positive:
- controlled autonomy;
- better reuse of already collected evidence;
- explicit gap handling;
- predictable failure/stop behavior.

Trade-offs:
- cumulative evidence/package handling is more complex;
- stop thresholds need product/operational calibration;
- some questions remain unresolved by design.

## Verification

- hard maximum cycle count in DEV scenarios;
- earlier-cycle evidence remains visible in later review;
- follow-up can target missing source types;
- stop reason is explicit when bounds are reached.

## Revisit triggers

Revisit bounds when measured production workload/cost/SLO data justifies calibrated limits; do not remove the boundedness invariant.
