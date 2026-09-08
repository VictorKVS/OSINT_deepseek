# FATHER Golden Solutions / Experience-First Reuse Policy v0.1

Status: **DESIGN BASELINE / CROSS-AGENT REUSE REQUIREMENT**  
Date: **2026-08-15**

## 1. Purpose

FATHER must not repeat full research for every project when a sufficiently similar problem has already been solved, tested, criticized and observed in prior work.

The default order is:

```text
NEW TASK
  ↓
CLASSIFY CONTEXT + CONSTRAINTS
  ↓
SEARCH VERIFIED EXPERIENCE / GOLDEN SOLUTIONS
  ↓
SIMILARITY + APPLICABILITY CHECK
  ↓
REUSE / ADAPT / CHALLENGE / RESEARCH
  ↓
LOCAL VERIFICATION
  ↓
RESULT + EXPERIENCE UPDATE
```

Research is a cost. Reuse of validated experience is preferred when the previous evidence remains applicable.

## 2. Golden Solution concept

A Golden Solution is not a universal truth and not merely a code snippet.

It is a versioned, evidence-backed reusable solution package for a bounded class of problems.

Stable ID example: `GOLD-PROG-000123`.

Minimum structure:

```yaml
golden_id: GOLD-XXXX
role: PROGRAMMER | ANALYST | ARCHITECT | TESTER | SECURITY | DEVSECOPS | OTHER
problem_class: "..."
context_signature: {}
requirement_pattern_refs: []
solution_pattern_ref: null
champion_candidate_ref: null
knowledge_refs: []
source_locator_refs: []
metric_refs: []
hard_gate_refs: []
test_refs: []
validation_refs: []
experience_refs: []
known_failure_refs: []
applies_when: []
does_not_apply_when: []
required_local_checks: []
version_constraints: []
review_after: null
status: CANDIDATE | PROVISIONAL | GOLDEN | LIMITED | DEPRECATED | SUPERSEDED
supersedes: null
superseded_by: null
```

A Golden Solution may include architecture, decision bundle, implementation template, test strategy, security controls, rollback method and operational checks.

## 3. Promotion to GOLDEN

A candidate should not become GOLDEN after one lucky success.

Initial promotion gate:

- at least 3 materially comparable successful uses OR a separately justified stronger evidence path;
- no unresolved critical safety/security/correctness failure;
- explicit context/applicability boundaries;
- exact source/KB provenance for material claims;
- required metrics and hard gates known;
- regression tests exist for important historical failures;
- at least one independent Critic/reviewer pass for D2/D3-class reuse;
- freshness/version state is current.

Where only one or two strong cases exist, use `PROVISIONAL` or `LIMITED` rather than pretending the pattern is universally established.

## 4. Similarity before reuse

FATHER must compare the new task with the Golden Solution's context signature.

Candidate similarity dimensions include:

- business/problem objective;
- functional requirements;
- NFRs;
- security/compliance class;
- data type and sensitivity;
- scale/load;
- latency/availability/recovery requirements;
- language/runtime/framework/database versions;
- infrastructure/deployment model;
- team/operational constraints;
- cost envelope;
- reversibility/blast radius;
- external integrations;
- known threat/failure profile.

No single similarity score is treated as truth until calibrated. Component differences remain visible.

## 5. Four reuse outcomes

After applicability review, the agent must choose one of four explicit routes.

### R1 — DIRECT_REUSE

Use the Golden Solution with only local configuration changes.

Conditions:
- context matches within approved applicability bounds;
- no material version/freshness conflict;
- hard gates remain valid;
- local acceptance/regression checks pass.

Full research is not repeated.

### R2 — ADAPT_REUSE

Reuse the Golden Solution but alter bounded parts.

Conditions:
- core problem class matches;
- differences are known and traceable;
- only affected assumptions/metrics/tests are reopened;
- unchanged validated parts are not needlessly re-researched.

### R3 — CHALLENGE_GOLDEN

Run Champion/Challenger evaluation when a credible alternative may materially improve the Golden Solution.

Triggers include:
- new technology or source evidence;
- repeated operational weakness;
- changed cost/performance/security requirements;
- challenger with plausible measurable advantage;
- scheduled anti-stagnation sampling.

The incumbent Golden Solution is the Champion until a challenger wins under the governed comparison standard.

### R4 — NEW_RESEARCH

Run deeper research only when:
- no sufficiently similar Golden Solution exists;
- applicability is materially uncertain;
- the existing Golden Solution is stale/superseded;
- prior evidence is contradictory;
- the new context violates an assumption or hard boundary;
- D3 impact requires renewed independent evidence.

## 6. Reuse Decision Record

Every material reuse decision gets a stable record.

```yaml
reuse_decision_id: REUSE-XXXX
project_record_id: PED-XXXX
agent_role: PROGRAMMER
new_problem_signature_ref: CTX-XXXX
candidate_golden_refs: []
selected_golden_ref: null
similarity_dimensions: []
material_differences: []
route: DIRECT_REUSE | ADAPT_REUSE | CHALLENGE_GOLDEN | NEW_RESEARCH
reopened_assumptions: []
reused_evidence_refs: []
new_evidence_required: []
local_test_refs: []
result: PASS | FAIL | LIMITED | INCONCLUSIVE
experience_ref: null
```

This lets FATHER prove why it reused experience instead of re-running research.

## 7. Golden Catalogue

FATHER should maintain catalogues by role and problem class.

Example logical catalogue:

```text
GOLDEN_CATALOGUE
  ├─ ANALYST
  │   ├─ requirement decomposition patterns
  │   └─ process/data-flow patterns
  ├─ ARCHITECT
  │   ├─ service boundary patterns
  │   ├─ deployment patterns
  │   └─ resilience patterns
  ├─ TESTER
  │   ├─ test strategy patterns
  │   └─ regression/failure packs
  ├─ PROGRAMMER
  │   ├─ API patterns
  │   ├─ transaction patterns
  │   ├─ retry/idempotency patterns
  │   ├─ concurrency patterns
  │   ├─ agent-engineering patterns
  │   └─ implementation templates
  ├─ SECURITY
  │   ├─ control patterns
  │   └─ verification patterns
  └─ DEVSECOPS
      ├─ CI/CD patterns
      ├─ rollback patterns
      └─ observability patterns
```

The catalogue is an index over governed records; it must not duplicate the underlying evidence.

## 8. Experience frequency and confidence without fake certainty

Track empirical reuse history as raw counts and distributions:

```yaml
reuse_count: 0
successful_reuse_count: 0
failed_reuse_count: 0
adaptation_count: 0
challenge_count: 0
champion_loss_count: 0
context_family_count: 0
critic_pass_count: 0
regression_count: 0
```

Derived pass rates may be shown, but they are not universal truth probabilities.

A pattern that succeeded 50 times in one narrow context is not automatically better evidence than 5 independent successes across materially different applicable contexts.

## 9. Anti-stagnation rule

Golden Solutions reduce repeated research, but they must not freeze the system.

Controls:

- freshness/review date;
- version/supersession checks;
- periodic challenger sampling for high-value/high-frequency patterns;
- automatic challenge trigger after recurring failures;
- new canonical source/version may reopen affected claims;
- local E0 evidence may contradict the Golden Solution;
- Principal Critic may force a challenge when assumptions drift.

## 10. Learning effect

The target learning loop becomes:

```text
PROJECT 1..N
→ PDR/CMP/EXP/VER/EXPREC
→ recurring successful pattern
→ GOLD candidate
→ independent validation
→ GOLDEN SOLUTION
→ future similar project reuses it
→ local verification
→ reuse success/failure history
→ challenger when justified
→ improved Golden Solution
```

Thus FATHER gets faster with experience without becoming dogmatic.

## 11. Relationship to Knowledge Bases

`Knowledge Object` answers primarily: **what principle/claim is supported and when?**

`Golden Solution` answers primarily: **how did we repeatedly solve this bounded class of engineering problem successfully?**

`Project Engineering Memory` answers: **what happened in this concrete project?**

These layers must remain distinct but linked:

```text
PKB/SKB/AKB KNOWLEDGE
        ↓ supports
GOLDEN SOLUTION
        ↓ reused by
PROJECT DOSSIER
        ↓ produces
EXPERIENCE
        ↓ updates/challenges
GOLDEN SOLUTION + KB
```

## 12. Governing rule

**Experience-first, research-on-delta.**

For a similar task, FATHER should reuse the best validated prior solution and reopen only the parts made uncertain by the new context.

Do not repeat a full research cycle merely to create fresh-looking documentation.
