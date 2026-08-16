# FATHER Development Journal & Commit Policy

Status: FOUNDATIONAL PROCESS RULE

## Purpose
The journal exists to reconstruct important engineering reasoning and maturity progress. It is not a transcript of every action, test run, thought, or commit.

## Journal structure
Keep maturity transition reports together with the development journal. Each meaningful gate report uses:
CURRENT -> TESTED -> LIMITATIONS -> NEXT -> WHY -> BEFORE/AFTER -> NEXT TESTS -> EXIT GATE -> DECISION.

## What MUST be journaled
- maturity gate reached or failed;
- architecture/role/protocol decision that constrains future work;
- important live acceptance evidence;
- security finding or remediation that changes risk;
- rejected/retired approach when the reason may prevent repeating the mistake;
- benchmark/A-B/calibration result that changes algorithm choice;
- Golden Pattern adoption or retirement;
- major incident/regression/root-cause lesson.

## What should NOT create a separate journal entry
- routine green unit-test run;
- typo/formatting cleanup;
- repeated live run with no new finding;
- minor refactor with unchanged contract/behavior;
- intermediate exploratory thought already represented by a final decision;
- mechanically generated status noise.

Such evidence may be referenced by the next meaningful gate report or retained in CI/test artifacts instead.

## Commit value test
A repository commit is justified when at least one is true:
1. It changes executable behavior or a stable contract.
2. It adds/fixes a test that protects meaningful behavior.
3. It changes architecture, security, evidence methodology, role protocol, or maturity policy that future developers need.
4. It records a milestone/gate/decision whose loss would make later reasoning difficult to reconstruct.
5. It adds reusable knowledge or a Golden Pattern.

If none is true, prefer not to create a repository commit solely to record conversational/progress noise.

## Commit batching
Batch tightly related documentation/status updates into one coherent commit when practical. Do not create one commit per sentence, test observation, or tiny journal note.

Do not batch unrelated executable changes merely to reduce commit count: commits should remain reviewable and reversible.

## Journal optimization
Older journal entries are historical evidence and should not be deleted merely because they are verbose. Periodically create a compact milestone index/synthesis that points to the durable decisions and gate evidence. Archive/supersede redundant planning notes only after confirming no unique decision/evidence is lost.

## Primary progress record
For each product keep one current maturity status containing:
- current level/pass;
- A/B/C acceptance state;
- proven capabilities;
- blockers;
- deferred items;
- next level;
- why the next level matters;
- BEFORE -> AFTER capability change;
- tests required to advance.

The journal then records only meaningful changes to this state.

## Principle
Git history is an engineering evidence trail, not a diary. Journal density must optimize future reconstruction, auditability and learning—not commit count.
