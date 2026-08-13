# J-027 — M5 G9 Counter-evidence / Alternative Search DEV PASS

Date: 2026-08-13
Status: DEV PASS

## Objective

Close G9 by making deliberate challenge search auditable. A material analytical hypothesis must not reach higher research sufficiency merely because acquisition code sets a boolean flag saying counter-evidence was searched.

## Implemented

### `father_osint/counter_evidence.py`

Added a deterministic G9 contract:

- `CounterEvidenceDirective` — `REQUIRED` or explicit `NOT_APPLICABLE`;
- `CounterEvidenceAttempt` — bounded execution record with `SEARCHED / FAILED / SKIPPED`;
- `CounterEvidenceAssessment` — `SEARCHED / INCOMPLETE / NOT_APPLICABLE`;
- `DeterministicCounterEvidencePlanner`;
- `DeterministicCounterEvidenceAssessor`;
- DecisionRecord lineage for both planning and assessment.

Policy behavior:

- if ANALYST supplies a leading hypothesis, OSINT_EXPERT must create challenge questions, alternative-explanation searches and required methods;
- if no leading hypothesis exists, G9 is not silently skipped: `NOT_APPLICABLE` is recorded with rationale;
- a failed/skipped attempt does not count as searched;
- a completed bounded search may report that no contradiction was found, but must explicitly state that this is not proof that contradictory evidence does not exist.

### `father_osint/sufficiency_g9.py`

Added `LineageBoundResearchSufficiencyAssessor` as a compatibility layer over the accepted G8 policy.

Critical invariant:

`coverage["counter_evidence_searched"]` supplied by collection/reconnaissance code is ignored. The trusted value is derived only from a G9 `CounterEvidenceAssessmentResult` belonging to the same case/request. Its DecisionRecord is added to sufficiency input lineage.

The existing G8 assessor remains unchanged for backward compatibility.

## Acceptance tests

Added `tests/test_g9_counter_evidence.py` covering:

1. hypotheses require deliberate challenge search;
2. absence of a leading hypothesis records explicit NOT_APPLICABLE;
3. failed search remains INCOMPLETE;
4. completed search records SEARCHED without making an absence claim;
5. naked `counter_evidence_searched=true` cannot promote sufficiency;
6. audited G9 lineage can satisfy the counter-evidence component of GOOD sufficiency.

## Verification

GitHub Actions `Stage 06 DEV Verification` on commit `21cd1bbf6ca4d84ef28c106e3d7ed171f32ea903`:

- 109 tests collected;
- 109 passed;
- 2 skipped;
- DEV verification: SUCCESS.

Implementation commits:

- `b4df191` — feat(g9): formalize counter-evidence search protocol
- `a10e424` — feat(g9): bind sufficiency to counter-evidence lineage
- `21cd1bb` — test(g9): cover counter-evidence protocol and sufficiency lineage

## Result

G9 is DEV PASS. Counter-evidence is now a provenance-bearing research action rather than an untrusted boolean. No live Telegram credentials/session were touched.

## Next gate

G10 — Transparent Acquisition Report to ANALYST.
