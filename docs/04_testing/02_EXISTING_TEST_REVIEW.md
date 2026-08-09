# Stage 04 — Existing Test Review

**Status:** COMPLETE FOR CURRENT TEST INVENTORY

The goal is not to maximize test count. Each test must have a clear contract purpose and an approved requirement owner.

| Test file | Current value | Decision | WHY |
|---|---|---|---|
| `tests/test_father_osint_mvp.py` | covers collection, old hash-dedup behavior, no-collector, max_items | **CHANGE** | first test encodes obsolete AC-02 semantics by expecting two same-payload source observations to become one Material |
| `tests/test_telegram_collector.py` | validates transport-neutral mapping and fallback locator | **KEEP** | directly supports AT-02 and does not require live Telegram |
| `tests/test_simple_analyst.py` | validates generic handoff and missing-source follow-up | **KEEP DEV HARNESS** | supports AC-06/07; not evidence of final Analyst quality |
| `tests/test_dev_pipeline.py` | validates old OSINT↔Analyst loop and cycle bound | **PARTIAL KEEP / MIGRATE** | bound test is valuable for AC-08, but pipeline is a DELETE/FREEZE candidate because `review_pipeline.py` supersedes the larger flow |
| `tests/test_simple_socrates.py` | validates PASS and RESEARCH_MORE for obvious gaps | **KEEP DEV HARNESS** | supports AC-09 only at handoff level; not evidence of epistemic correctness |

## Required changes before first acceptance run

### R1 — Replace obsolete duplicate test
Current test expects:

```text
source A + payload X
source B + payload X
        ↓
2 Material records total after adding payload Y
```

This contradicts the reviewed requirement. Correct oracle:

```text
source A + payload X ─┐
                     ├─ two source observations retained
source B + payload X ─┘

payload X may have one physical raw blob
```

Decision: **CHANGE TEST, then later CHANGE IMPLEMENTATION.** Do not patch implementation before the revised test exists and is reviewed.

### R2 — Add collector exception isolation test
AC-05 is not explicitly proven by the current inventory. Add a fixture/fake collector that raises while another returns valid material.

### R3 — Add review-pipeline bound test
AC-08 should ultimately be tested on the chosen orchestration path. Current bound test targets `DevResearchPipeline`; architecture currently favors `DevReviewPipeline` as the fuller candidate. Design a test for `DevReviewPipeline` before deleting the old pipeline.

### R4 — Add storage restart/provenance test
Reopen the store and submit same payload from a second locator. The second source observation must remain visible while raw payload reuse is allowed.

### R5 — AC-10 remains architecture/environment evidence
Do not invent a fake unit test that claims production independence. Capture the command/environment used for the DEV suite and prove that no live credentials/connectors are required.

## Test quality notes

The existing tests are compact and useful, but they reflect the order in which prototype code was written. Stage 04 changes the direction of authority: acceptance criteria now define tests, and tests then judge code.
