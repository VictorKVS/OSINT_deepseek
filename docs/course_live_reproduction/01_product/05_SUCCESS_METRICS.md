# Lesson 01 / Product — Success Metrics

Status: `DRAFT_FROM_CURRENT_EVIDENCE / TARGETS_PARTLY_UNKNOWN`

The project already has executable acceptance criteria and verified DEV behavior. Product/business KPI targets are not yet fully evidenced and therefore remain separate from technical acceptance.

## Product outcome metrics

| ID | Metric | Current state | Target state |
|---|---|---|---|
| PM-01 | share of research tasks that return traceable evidence or an explicit gap/error | measurable from runs | `TO_BE_BASELINED` |
| PM-02 | provenance completeness of returned observations | partially testable | target to be confirmed |
| PM-03 | repeated raw payload reuse without source-observation loss | technically evidenced in DEV | preserve correctness; business saving TBD |
| PM-04 | bounded completion of research cycles | technically evidenced in DEV | no unbounded loops |
| PM-05 | collector failure visibility/isolation | technically evidenced in DEV | all material failures explicit |
| PM-06 | analyst time saved on repeated evidence discovery | not currently measured | `TO_BE_BASELINED` |
| PM-07 | reusable evidence ratio across investigations | not currently measured | `TO_BE_BASELINED` |
| PM-08 | production source coverage by approved source class | future | define per product release |

## Technical acceptance already available

`FACT_FROM_EXISTING_REPO`

The current TZ defines AC-01…AC-13, including non-empty valid package behavior, bounded collection, failure isolation, cumulative evidence preservation, equal-payload/source-observation semantics and file hashing behavior.

These are **verification criteria**, not substitutes for product/business KPIs.

## Measurement principle

No percentage improvement is recorded without telemetry. Until measurement exists, FATHER uses `TO_BE_BASELINED` rather than an invented target.

## Evidence

- `docs/OSINT_AGENT_TZ_V1.md` acceptance criteria;
- `docs/TRACEABILITY_MATRIX.md` technical traceability;
- `docs/06_verification/` verified DEV evidence.
