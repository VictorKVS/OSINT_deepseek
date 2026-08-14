# PROGRAMMER Qualification / Training Plan v0.1

Status: **CAPTURED / FUTURE EXECUTION AFTER KB GATES**  
Date: **2026-08-14**

## 1. Goal

After PROGRAMMING_KB reaches each qualification threshold, the Programmer Agent must prove that it can *use* knowledge rather than merely retrieve it.

Qualification is earned through repeated tasks, executable checks, independent review and retained failure history.

```text
KNOWLEDGE
  → CONTROLLED EXERCISES
  → REALISTIC ENGINEERING CASES
  → HIDDEN EVALUATION
  → PRINCIPAL CRITIC
  → EXPERIENCE / FAILURE MEMORY
  → QUALIFICATION STATE
```

## 2. Qualification levels

### Junior

Purpose: reliable execution under an approved contract.

Training emphasis:
- basic algorithms/data structures;
- language/runtime semantics;
- ordinary CRUD/API/data transformations;
- unit/integration tests;
- debugging bounded defects;
- Git/CI basics;
- secure coding baseline;
- exact adherence to constraints.

Autonomy boundary: no material architecture or dependency choice without approval.

### Master

Purpose: independent solution search with bounded approval gates.

Training emphasis:
- algorithm selection under constraints;
- refactoring/legacy work;
- ORM/SQL trade-offs;
- sync/async/concurrency choices;
- performance bottlenecks;
- API/schema evolution;
- dependency selection/replacement;
- reliability and failure handling;
- alternative generation and D2 evidence bundles.

Autonomy boundary: may propose and prototype material changes; approval required before high-impact adoption.

### Senior

Purpose: result ownership for bounded engineering problems with strong evidence.

Training emphasis:
- unfamiliar/underspecified systems;
- multi-constraint trade-offs;
- production defects and incident reconstruction;
- architecture-sensitive implementation;
- concurrency/distributed failure modes;
- performance/cost/security interactions;
- migration/rollback/compatibility;
- falsification of own preferred solution;
- operational and economic consequences;
- D2/D3 evidence, Critic defence and revisit rules.

Senior qualification is not awarded from knowledge-card count alone.

## 3. Stage A — classical problem corpus

Use established algorithmic/programming exercise families to train precision and constraint reasoning.

Candidate source families include:
- Knuth / *The Art of Computer Programming* exercises where lawful access exists;
- CLRS exercises/problems;
- Skiena / *The Algorithm Design Manual* exercises;
- established university algorithm/data-structure problem sets;
- competitive-programming style tasks and archives where terms permit use;
- project-owned/generated equivalent tasks derived from concepts rather than copied protected text.

What is measured:
- correctness;
- time/memory complexity;
- proof/invariant quality where applicable;
- edge-case coverage;
- implementation robustness;
- solve time;
- unnecessary complexity;
- ability to explain rejected approaches.

Important: commercial books are references, not automatically bulk-ingested training datasets. Store source cards and original project-authored derivative/equivalent exercises unless rights permit fuller use.

## 4. Stage B — everyday engineering corpus

Algorithmic ability is necessary but insufficient. The next corpus must represent ordinary professional work.

Task families:
1. fix a real-looking bug with incomplete symptoms;
2. implement a small feature in an existing codebase;
3. refactor without observable behaviour change;
4. add/repair tests;
5. diagnose an ORM/SQL performance problem;
6. change an API while preserving compatibility;
7. perform a schema/data migration;
8. remove or replace a dependency;
9. add timeout/retry/idempotency correctly;
10. investigate a race/resource leak;
11. repair CI/build/deployment behaviour;
12. add logging/metrics/tracing without breaking semantics;
13. close a security defect;
14. review a pull request and identify latent defects;
15. recover from a deliberately introduced operational failure.

These tasks should include mundane work, not only impressive architecture challenges.

## 5. Stage C — AI-generated realistic case engine

After the human-designed seed corpus is stable, use one or more independent LLMs as **task generators**, not as authoritative judges.

Generator input should be structured:

```yaml
domain: backend | web | data | algorithms | concurrency | reliability | security | devops
qualification_target: junior | master | senior
complexity_band: 1..10
commonness_band: 1..10
novelty_band: 1..10
ambiguity_band: 1..10
risk_band: 1..10
constraints: []
required_artifacts: []
known_failure_modes: []
hidden_acceptance_properties: []
```

The task generator must produce:
- scenario/context;
- repository/project fixture or minimal reproduction;
- explicit visible requirements;
- hidden acceptance properties held by the judge;
- at least one plausible trap/failure mode for Master/Senior cases;
- expected evidence type, not necessarily a single prescribed solution.

AI-generated cases are admitted to the evaluation corpus only after validation for solvability, non-duplication, realism and absence of leaked answers.

## 6. Difficulty versus everydayness

Do not equate rare with difficult or common with easy.

Maintain two independent axes:

- `complexity`: reasoning/implementation difficulty;
- `commonness`: probability of encountering this task in ordinary engineering work.

Recommended training balance is initially a design hypothesis, to be calibrated from real project/task data rather than treated as truth.

A useful first curriculum shape:
- high-commonness ordinary work must dominate Junior/Master exposure;
- algorithmic/constraint drills remain continuous;
- Senior receives more low-commonness/high-impact failures and novel combinations;
- weakness-driven tasks are generated more often after enough history exists.

## 7. Tournament / rating record

Each run records at minimum:

```yaml
agent_version: "..."
kb_snapshot: "..."
task_id: "..."
qualification_target: "..."
start_time: "..."
end_time: "..."
solution_status: PASS | PARTIAL | FAIL
visible_tests: {}
hidden_tests: {}
critic_result: {}
security_result: {}
performance_result: {}
evidence_quality: {}
rework_count: 0
failure_refs: []
experience_refs: []
cost: {}
```

Do not collapse all of this into one score until the weighting scheme is calibrated. Maintain component scores and raw measurements.

## 8. Promotion concept

Promotion requires sustained evidence, not one good run.

Candidate gates to calibrate later:
- minimum number of independent tasks across distinct domains;
- no unresolved critical recurring failure class;
- target pass rate on hidden tests;
- acceptable regression rate;
- evidence/critic pass threshold for D2/D3 tasks;
- solve-time distribution appropriate to the level;
- successful tasks from both classical and everyday corpora;
- successful unfamiliar/novel cases for Senior.

Exact numeric thresholds remain `UNCALIBRATED` until the first evaluation history exists.

## 9. Storage boundary

### GitHub repository — suitable
Store:
- schemas/ontologies;
- Knowledge Object records and source metadata;
- public/open training tasks;
- generators and harness code;
- task manifests;
- small reproducible fixtures;
- aggregate scorecards;
- ADRs / Critic records where disclosure is acceptable;
- references/pointers to protected objects.

### External/object/secure storage — required as volume grows
Store outside normal Git history:
- full lawful source archives;
- embeddings/vector indexes;
- large repositories/datasets;
- binaries/container images;
- sandbox snapshots;
- long traces/logs;
- high-volume benchmark/tournament artifacts.

### Secure IP Vault — future protected layer
Do not expose publicly:
- hidden tests and hidden acceptance properties;
- unreleased evaluation corpus;
- proprietary failure/tournament corpus;
- calibrated decision/retrieval coefficients;
- customer-specific code/evidence;
- protected solution keys or judge logic that would let the agent memorize the exam.

GitHub is therefore the **versioned control plane / manifest / public engineering memory**, not the final bulk knowledge warehouse.

## 10. Execution order

```text
MIN KB
→ classical + everyday seed exams
→ measure weaknesses
→ repair KB
→ Master-depth KB
→ broader/harder exams
→ AI realistic case generator
→ hidden evaluation corpus
→ Senior-depth KB
→ adversarial/novel cases
→ tournament history
→ calibrated promotion thresholds
→ optional deeper learning research
```

The AI case generator should not be trusted before a human/independent seed corpus establishes what "good", "hard" and "realistic" mean.

## 11. First future gate

When MIN PROGRAMMING_KB is reached, create the first qualification pack:
- 20 classical/algorithmic tasks across several concept families;
- 30 everyday engineering tasks across backend/web/data/testing/reliability/security;
- 10 hidden variants/counterexamples;
- independent Critic review of task quality;
- reproducible execution harness;
- baseline run of at least two agent configurations/versions.

The first goal is not to award Senior status. It is to discover the agent's real weakness map and calibrate the next curriculum.
