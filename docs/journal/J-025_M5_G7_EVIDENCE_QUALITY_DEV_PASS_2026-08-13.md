# J-025 — M5 G7 Evidence Quality DEV PASS — 2026-08-13

## Outcome

G7 Evidence Quality Assessment is now accepted at DEV level.

The repository already contained `father_osint/evidence_quality.py`; this run completed the acceptance layer by adding dedicated G7 tests and verifying the full DEV suite in GitHub Actions.

## Contract exercised

Evidence quality remains multidimensional and non-calibrated:

- reliability;
- relevance;
- independence;
- recency;
- directness;
- corroboration;
- provenance quality.

The assessor preserves each dimension independently and refuses to expose an aggregate truth probability.

## Safety / epistemic invariants proved

1. Source/platform labels do not automatically promote reliability.
2. Repeated identical payloads are treated as derivative repetition, not independent corroboration.
3. Missing research context leaves relevance `UNKNOWN` rather than guessed.
4. Source-history evidence is required before reliability can move above `UNKNOWN`.
5. Quality decisions preserve `DecisionRecord` lineage to method and knowledge references.
6. Categorical states are policy labels, not calibrated probabilities of truth.

## Acceptance tests

Added:

`tests/test_g7_evidence_quality.py`

Coverage includes:

- all seven dimensions remain separate;
- aggregate truth probability is forbidden;
- repeated payload independence/corroboration behavior;
- source/platform labels do not confer reliability;
- missing research context keeps relevance unknown;
- DecisionRecord method/knowledge lineage.

## CI evidence

Commit: `5ce83d8b4ff01ef6ea52e632f8249e3a781fe0ba`

GitHub Actions:

- `Stage 06 DEV Verification`: SUCCESS;
- 97 tests collected;
- 97 passed;
- 2 skipped.

## Remaining limitation

G7 is a policy/contract baseline. It does not yet provide calibrated statistical reliability or truth probability. Such calibration would require empirical datasets and a separately approved methodology.

## Next gate

G8 — Research Sufficiency.

The next contract must decide `INSUFFICIENT / MINIMUM / GOOD / DESIRED` from explicit evidence-package conditions such as coverage, source diversity, independence, primary evidence, counter-evidence search and critical gaps. Raw material count alone must never be sufficient.
