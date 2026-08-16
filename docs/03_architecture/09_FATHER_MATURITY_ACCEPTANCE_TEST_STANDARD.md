# FATHER Maturity Acceptance Test Standard

Status: FOUNDATIONAL QUALITY STANDARD
Scope: every FATHER product, agent, role, knowledge base, pipeline and maturity level.

## Core rule
A maturity level is not complete because code exists or documentation is written. It is complete only when a real target capability passes explicit acceptance tests.

Every maturity level MUST define:
1. Real operational goal — what complete capability becomes possible.
2. Observable output — what artifact/result proves the capability.
3. Three acceptance-test difficulty levels: BASIC, PROFESSIONAL, STRESS.
4. Quantitative/boolean pass criteria wherever possible.
5. Failure criteria and known limitations.
6. Principal Critic review.
7. Improvement recommendations generated from test evidence.
8. Decision: ADVANCE / HOLD / REDESIGN / RETIRE.

## Test level A — BASIC
Purpose: prove the minimal end-to-end path works.
Characteristics:
- clean/known inputs;
- normal operating conditions;
- smallest representative workload;
- no hidden tricks.
Pass means the system can perform the intended job at all.

## Test level B — PROFESSIONAL
Purpose: prove the capability is usable in realistic professional work.
Characteristics:
- multiple sources/objects;
- incomplete and noisy data;
- duplicates and contradictions;
- ordinary failures;
- restart/recovery where applicable;
- provenance/audit requirements;
- realistic time/volume constraints.
Pass means a professional user can rely on the capability within documented limitations.

## Test level C — STRESS / ADVERSARIAL
Purpose: discover the boundary of competence before advancing maturity.
Characteristics:
- misleading or conflicting evidence;
- source dependency/reposts masquerading as corroboration;
- missing primary evidence;
- partial outages/timeouts;
- malformed inputs;
- attempts to trigger unsupported conclusions;
- security/adversarial cases appropriate to the product;
- workload near the declared operating boundary.
Pass does not require solving the impossible. It requires correct behavior: solve, degrade safely, return UNKNOWN/INSUFFICIENT, request more evidence, or stop without fabricating a result.

## Acceptance matrix
Each maturity gate maintains a table:

| Test ID | Real goal | Difficulty | Input/case | Expected behavior | Metric/threshold | Evidence artifact | Result | Defect/improvement |
|---|---|---|---|---|---|---|---|---|

No vague acceptance wording such as “works well”, “many sources”, “good quality” or “sufficient” is allowed without a defined policy/method and observable criterion.

## Advancement rule
Default advancement requires:
- BASIC: PASS
- PROFESSIONAL: PASS
- STRESS: PASS or PASS_WITH_KNOWN_LIMITATIONS when limitations are explicitly documented, safe, and do not invalidate the next maturity level.
- no unresolved critical security defect;
- no unexplained unsupported judgment in the tested path;
- Principal Critic review completed.

## Test-derived improvement loop
After every gate:
TEST -> OBSERVATION -> DEFECT/GAP -> ROOT CAUSE -> PROPOSED CHANGE -> PRIORITY -> IMPLEMENT/DEFER -> RETEST.

Every proposed improvement is classified:
- BLOCKER: required before advancing;
- NEXT_LEVEL: valuable but belongs to the next maturity level;
- BACKLOG: useful but not currently justified;
- REJECTED: complexity/cost exceeds demonstrated value.

This prevents endless polishing of non-blocking tools.

## Real-goal requirement
Tests should be scenario-based, not only unit tests. Unit/contract tests support the evidence but cannot alone prove maturity.

Example for Telegram OSINT:
A/BASIC: Analyst supplies a topic and configured channels; system returns relevant messages, text, links and provenance.
B/PROFESSIONAL: several channels, duplicates, forwards, external links and restart; system preserves lineage and produces an auditable package.
C/STRESS: contradictory/reposted/missing-origin material and partial failures; system distinguishes dependency where observable, marks UNKNOWN where not provable, does not fabricate independence or certainty, and reports gaps to Analyst.

## Security and intelligence dual gate
For intelligent/agentic systems, advancement requires both:
- capability/intelligence acceptance;
- security/safety acceptance appropriate to the level.
A capability cannot advance solely because it is intelligent if it is unsafe, and cannot advance solely because it is secure if it cannot perform the target task.

## Portfolio metric
FATHER progress reporting should show for every product:
- maturity level;
- current MIN/MED/MAX pass;
- BASIC/PROFESSIONAL/STRESS test status;
- blockers;
- recommended changes;
- next real capability to unlock.
