# Programmer Agent — Classic and Public Task Corpus Map v0.1

Status: **MANDATORY TRAINING-SOURCE MAP / NO BULK COPYRIGHT INGESTION**  
Date: **2026-08-15**

## 1. Purpose

This document defines the classical and public problem-solving corpus that should train and qualify the FATHER Programmer before and alongside production-style engineering cases.

The goal is not to maximize the number of solved puzzles. The goal is to build complementary capabilities:

```text
syntax fluency
→ algorithmic correctness
→ mathematical reasoning
→ data-structure choice
→ edge-case discipline
→ implementation speed
→ code quality
→ debugging
→ systems reasoning
→ secure engineering
→ real-repository work
→ production/organization cases
→ agent engineering
```

No single platform is accepted as proof of Senior capability.

## 2. Corpus classes

Each source is classified as one of:

- `REFERENCE_ONLY` — commercial/copyrighted source; store bibliographic metadata, exercise references, competency mapping and project-original variants, but not bulk exercise text unless rights permit;
- `PUBLIC_LINKED` — publicly accessible source used through links/API/manual retrieval under its terms; do not assume redistribution rights;
- `OPEN_REUSABLE` — content may be mirrored/derived only when an explicit licence permits the intended reuse;
- `PROJECT_ORIGINAL` — FATHER-owned original tasks and variants;
- `HIDDEN_EVAL` — private tasks/expected states kept outside public GitHub.

Licence state is a gate. Accessibility is not equivalent to permission to republish.

## 3. Classical Russian-language taskbooks

### SRC-TASK-RU-001 — M. E. Abramyan, `1000 задач по программированию`

Class: `REFERENCE_ONLY` unless a specific edition/source grants broader rights.

Training role:
- scalar types and expressions;
- conditions and loops;
- procedures/functions;
- arrays and strings;
- files;
- recursion;
- pointer/data-structure fundamentals where applicable.

Use:
- primary drill layer for Junior syntax/algorithm fluency;
- solve the same competency on Python and Go where useful;
- generate project-original structurally similar variants rather than copying the whole corpus.

Qualification value: **Junior mandatory / Master warm-up**.

### SRC-TASK-RU-002 — A. Shen, `Программирование: теоремы и задачи`

Class: `REFERENCE_ONLY` for printed material; a specific publisher-provided electronic version may be used according to its stated terms.

Training role:
- correctness arguments;
- construction of algorithms;
- proof-oriented reasoning;
- asymptotic thinking;
- distinguishing a working example from a generally correct method.

Qualification value: **Junior→Master mandatory reasoning lane**.

### SRC-TASK-RU-003 — D. M. Zlatopolsky, `Сборник задач по программированию`

Class: `REFERENCE_ONLY`.

Training role:
- large language-independent drill bank;
- conditions/loops;
- strings;
- functions/procedures;
- one- and two-dimensional arrays;
- files;
- sorting and classic school/university programming topics.

Use:
- broad coverage and repetition;
- paired variants are useful for public-vs-hidden task construction;
- preferred for cross-language reimplementation exercises.

Qualification value: **Junior mandatory breadth layer**.

### SRC-TASK-RU-004 — `Cracking the Coding Interview`, Gayle Laakmann McDowell

Class: `REFERENCE_ONLY`.

Training role:
- decomposition under time pressure;
- data-structure selection;
- coding-interview style edge cases;
- communication of assumptions and complexity.

Qualification value: **Junior/Master timed diagnostic**, not Senior proof.

## 4. Canonical algorithmic and mathematical sources

### SRC-TASK-ALG-001 — Donald E. Knuth, `The Art of Computer Programming`

Class: `REFERENCE_ONLY`.

Use as a long-horizon reasoning corpus, especially:
- Volume 1 — fundamental algorithms and data structures;
- Volume 3 — sorting/searching;
- Volume 4 family — combinatorial algorithms and advanced discrete methods.

Store in TASK_KB:
- bibliographic source/version;
- section/exercise reference;
- concepts/competencies tested;
- project-produced solution evidence;
- project-original variants;
- failure/counterexample records.

Do **not** encode an exercise-difficulty scale from secondary summaries unless verified against the actual lawful source/version.

Qualification value: **Master mandatory selected set / Senior advanced selected set**.

### SRC-TASK-ALG-002 — CLRS, `Introduction to Algorithms`

Class: `REFERENCE_ONLY`.

Training role:
- standard algorithms/data structures;
- proofs and invariants;
- asymptotic analysis;
- graph algorithms;
- dynamic programming;
- greedy methods;
- advanced algorithmic foundations.

Qualification value: **Junior→Master core**.

### SRC-TASK-ALG-003 — Skiena, `The Algorithm Design Manual` / related challenge material

Class: `REFERENCE_ONLY` unless a specific public resource says otherwise.

Training role:
- problem classification;
- design-pattern recognition for algorithms;
- mapping unfamiliar tasks to known structures.

Qualification value: **Master**.

### SRC-TASK-ALG-004 — Project Euler

Class: `PUBLIC_LINKED`; reuse terms must be checked before mirroring statements.

Training role:
- mathematical modelling;
- efficient computation;
- number theory/combinatorics;
- performance-aware reasoning.

Qualification value: **Junior→Master optional/diagnostic**.

### SRC-TASK-ALG-005 — Advent of Code

Class: `PUBLIC_LINKED`; do not mirror content without permission.

Training role:
- parsing;
- state machines;
- graph/search problems;
- incremental problem complexity;
- fast engineering under changing requirements.

Qualification value: **Junior/Master seasonal sprint lane**.

## 5. Online coding/problem platforms

### SRC-TASK-PLAT-001 — Exercism

Class: `PUBLIC_LINKED` / licence-specific per repository/content.

Training role:
- idiomatic language practice;
- tests-first exercise structure;
- Python and Go primary lanes;
- later Rust/C/TypeScript/other languages as required.

Qualification value: **Junior language fluency**.

### SRC-TASK-PLAT-002 — LeetCode

Class: `PUBLIC_LINKED`; task statements/solutions are not to be mirrored into public TASK_KB without rights.

Training role:
- common DS&A patterns;
- timed implementation;
- arrays/hash maps/trees/graphs/DP;
- variant generation around known competency targets.

Qualification value: **Junior/Master speed + pattern recognition**, never standalone Senior proof.

### SRC-TASK-PLAT-003 — Codeforces

Class: `PUBLIC_LINKED`; respect platform/problem author rights.

Training role:
- adversarial edge cases;
- algorithm selection under tight constraints;
- optimization;
- fast validation;
- novel combinations.

Qualification value: **Master advanced algorithmic lane / Senior optional stress lane**.

## 6. Systems and operating-system progression

The classical corpus must be followed by systems work so the Programmer cannot pass qualification as a puzzle specialist only.

Required system lanes already tracked by the Programmer roadmap/task plan should include:

- Nand2Tetris — computer stack from logic to OS concepts;
- CS:APP-style labs — machine-level representation, assembly, memory, cache, shell/network concepts;
- xv6/MIT OS labs — system calls, VM, traps, concurrency, filesystems;
- Linux From Scratch — build a bootable Linux environment from source under a controlled lawful source set;
- network implementation labs such as TCP/router exercises;
- DBMS implementation labs such as buffer/index/query/transaction components;
- project-original broken-system recovery cases.

Qualification value: **Master→Senior mandatory systems lane**.

## 7. DevOps, infrastructure and production practice

Reference/product inspiration may include practice-first platforms such as REBRAIN, but their course content is **not** copied into TASK_KB.

FATHER should build project-original scenarios such as:
- deploy a Linux service;
- configure reverse proxy/TLS;
- configure CI/CD;
- diagnose broken DNS/routing;
- repair systemd/service failure;
- configure PostgreSQL and backups;
- restore after a failed change;
- build monitoring/alerting;
- perform migration with rollback;
- create/update Windows/Linux endpoints in an organization template.

These tasks belong primarily to `PROJECT_ORIGINAL` and later the FATHER Engineering Polygon.

Qualification value: **Master/Senior mandatory**.

## 8. Secure-programming and authorized security lane

Candidate public practice sources include deliberately vulnerable applications and CTF/training platforms, but qualification work must run only in authorized isolated environments.

Training families:
- find + fix injection defects;
- authentication/authorization defects;
- SSRF/file/path handling;
- secrets leakage;
- dependency/supply-chain defects;
- unsafe deserialization;
- race/TOCTOU;
- insecure logging;
- protocol/parser robustness;
- reverse-engineering exercises where legally and operationally authorized.

Public platforms may be used for training, but FATHER qualification requires project-owned fix-and-regression cases, not merely capture-the-flag completion.

Qualification value: **Master/Senior mandatory secure-engineering lane**.

## 9. Real repository and production-like corpus

After classical/task-platform training, the Programmer must work against unfamiliar repositories.

Required case classes:
- real/open issue reproduction;
- failing tests/CI;
- incomplete bug report;
- dependency upgrade regression;
- performance regression;
- data corruption/transaction bug;
- concurrency bug;
- cross-platform bug;
- security finding requiring code change;
- feature request with compatibility constraints;
- legacy refactor with hidden regression tests.

External benchmarks such as SWE-bench may be used as one evidence source, but FATHER must maintain a private held-out corpus to reduce benchmark memorization/contamination risk.

Qualification value: **Master→Senior mandatory**.

## 10. Agent-engineering task corpus

The Programmer is also required to build AI agents.

Task progression:

```text
single bounded child agent
→ tool-using agent
→ retrieval-grounded agent
→ resumable/stateful agent
→ secure permission-bounded agent
→ 3+ candidate instances
→ common benchmark
→ hidden tests
→ Principal Critic
→ winner / NO DOMINATING CANDIDATE
→ release + rollback
```

Qualification value: **MIN capability required; Senior factory capability required**.

## 11. Recommended battle-agent progression

### Stage A — Hand and syntax

Use Abramyan + Zlatopolsky + Exercism.

Exit evidence:
- language basics are automatic;
- tests are written consistently;
- basic tasks are solved without unnecessary architecture.

### Stage B — Correctness and algorithms

Use Shen + CLRS + selected Knuth + Project Euler + LeetCode.

Exit evidence:
- correctness can be explained;
- complexity is reasoned, not guessed;
- multiple algorithms are compared when material.

### Stage C — Adversarial algorithms

Use Codeforces + selected advanced Knuth/Skiena + generated variants.

Exit evidence:
- unfamiliar combinations and hard edge cases do not collapse reasoning discipline.

### Stage D — Systems

Use Nand2Tetris/CS:APP/xv6/LFS/network/DBMS-style labs + FATHER variants.

Exit evidence:
- the agent can operate below framework level and diagnose system failures.

### Stage E — Production engineering

Use FATHER repositories, infrastructure tasks, migrations, incidents, observability, recovery and secure-development cases.

Exit evidence:
- the agent can perform everyday engineering work, not just solve puzzles.

### Stage F — Unknown repositories and hidden qualification

Use public real-world benchmarks plus private FATHER held-out tasks.

Exit evidence:
- capability generalizes to unseen codebases and constraints.

### Stage G — Agent Factory

Use the Agent Engineering competency contract.

Exit evidence:
- multiple candidate agents can be designed, measured, criticized and selected reproducibly.

## 12. Corpus volume planning

Counts are training-control values, not competence proof.

### MIN target envelope

- >=300 carefully selected classical/platform tasks;
- >=20 small implementation projects;
- >=10 bug-fix/repository cases;
- >=10 systems/infrastructure cases;
- >=20 Agent Engineering evaluation cases for the first child-agent bake-off;
- hidden variants for every qualification-critical competency.

### MEDIUM target envelope

- >=1000 task instances/controlled variants;
- >=50 real engineering/repository/infrastructure cases;
- >=40 end-to-end evaluated implementations aligned with the PROGRAMMING_KB roadmap;
- multiple languages/runtimes where justified.

### SENIOR/PRINCIPAL qualification

Do not set a pass condition based on raw task count alone.

Require:
- unseen organization/repository/system cases;
- incomplete or contradictory requirements;
- multiple valid solution paths;
- security/reliability/cost constraints;
- hidden acceptance criteria;
- Principal Critic;
- reproducible evidence;
- measured failure history and regression controls.

## 13. TASK_KB object requirements

Every imported/reference task record should eventually support:

```text
task_id
source_id
source_ref
rights_state
statement_storage_policy
competencies
prerequisites
difficulty
everyday_frequency
ambiguity
security_impact
expected_artifacts
public_tests
hidden_tests_ref
accepted_solution_properties
common_failure_modes
counterexamples
language/runtime applicability
qualification_level
attempt_history
critic_findings
experience_refs
```

For commercial books, `statement_storage_policy` defaults to `REFERENCE_ONLY` until rights are explicitly established.

## 14. Governing principle

The classical books/platforms build the Programmer's **school**. FATHER's own unseen organization, repository, system and agent-factory cases determine whether the Programmer is actually **combat-capable**.
