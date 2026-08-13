# J-026 — M5 G8 Research Sufficiency DEV PASS — 2026-08-13

## Outcome

G8 Research Sufficiency is accepted at DEV level.

A deterministic policy assessor now produces one of:

- `INSUFFICIENT`;
- `MINIMUM`;
- `GOOD`;
- `DESIRABLE`.

Raw material/post count is explicitly not a sufficiency criterion.

## Protocol correction

The protocol previously used one set of sufficiency levels for both requested targets and achieved outcomes. This conflicted with the architecture standard because an investigation must be able to *achieve* `INSUFFICIENT`, while an Analyst should never *request* `INSUFFICIENT` as a target.

The protocol now separates:

- `REQUESTED_SUFFICIENCY_LEVELS = MINIMUM | GOOD | DESIRABLE`;
- `ACHIEVED_SUFFICIENCY_LEVELS = INSUFFICIENT | MINIMUM | GOOD | DESIRABLE`.

`EvidencePackage.achieved_sufficiency` and `ResearchGap.current_sufficiency` may therefore represent `INSUFFICIENT` without weakening requested-target validation.

## Implementation

Added `father_osint/sufficiency.py` with `DeterministicResearchSufficiencyAssessor`.

The v1 policy considers explicit signals for:

- successful source-class/source-identity coverage;
- source diversity;
- independent evidence;
- primary evidence;
- counter-evidence search;
- critical/blocking gaps;
- evidence-quality context;
- temporal and target coverage for the highest tier.

The assessor returns explicit reasons, critical gaps, recommended next search actions and a `DecisionRecord` with method/knowledge lineage.

## Key behavior

- no evidence or no successful source coverage → `INSUFFICIENT`;
- fatal/blocking critical gaps → `INSUFFICIENT`;
- at least one covered source/evidence item → `MINIMUM`;
- diversity + independence + primary evidence + counter-evidence + no critical gaps + quality context → `GOOD`;
- broader diversity/depth + temporal/target coverage → `DESIRABLE`.

These are policy gates, not calibrated truth probabilities.

## Acceptance tests

Added `tests/test_g8_research_sufficiency.py` covering:

- explicit `INSUFFICIENT` result;
- 100 materials from one weak coverage context do not become `GOOD`;
- `GOOD` requires diversity, independence, primary evidence, counter-evidence and quality context;
- `DESIRABLE` requires broader depth plus temporal/target coverage;
- blocking gaps force `INSUFFICIENT`;
- protocol accepts `INSUFFICIENT` as achieved/current but not as requested target.

## CI evidence

Commit: `ace9915e7be124a5e819ab87b9d7426f134b317a`

GitHub Actions `Stage 06 DEV Verification`: SUCCESS.

- 103 tests collected;
- 103 passed;
- 2 skipped.

## Next gate

G9 — Counter-evidence / alternative search behavior.

The next implementation must make counter-evidence search an explicit SearchPlan branch for material analytical questions, or record a reasoned `NOT_APPLICABLE` decision with lineage. Silent omission must not be allowed.
