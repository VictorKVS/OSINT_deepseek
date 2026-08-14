# PROGRAMMING_KB Graph / Volume / Build Model v0.1

Status: **DRAFT DESIGN / ESTIMATION BASELINE**  
Date: **2026-08-14**  
Scope: PROGRAMMER knowledge graph only; no runtime implementation authorized.

## 1. Purpose

Define what the Programmer knowledge base means when we say **nodes and weights**, estimate realistic storage volume, identify the dominant creation cost, and define conditions for MIN / MEDIUM / MAX maturity.

The design extends the existing PROGRAMMING_KB evidence model. It does **not** introduce a synthetic universal truth/confidence score. Numeric weights are allowed only where the underlying quantity is measured or where a separately calibrated model exists.

## 2. Logical graph

```text
SOURCE / SPEC / BOOK / PAPER / DOC
              ↓
            CHUNK
              ↓
            CLAIM
          ↙   ↓   ↘
     CONCEPT PATTERN ANTIPATTERN
        ↓       ↓       ↓
    COMPETENCY  ───→ FAILURE MODE
        ↓                 ↓
      TASK ←──────── REGRESSION TEST
        ↓
     DECISION
     ↙      ↘
ALTERNATIVE  RISK
     ↓
EXPERIMENT / BENCHMARK
     ↓
RESULT / PROJECT EVIDENCE
     ↓
CRITIC REVIEW
     ↓
EXPERIENCE RECORD
```

## 3. Primary node classes

1. `SOURCE` — canonical source identity, provenance, licence/access state, version and freshness.
2. `SOURCE_VERSION` — exact edition/release/version state.
3. `CHUNK` — retrievable bounded source fragment with provenance.
4. `CLAIM` / `KNOWLEDGE_OBJECT` — normalized engineering assertion with scope and limitations.
5. `CONCEPT` — algorithmic/engineering concept.
6. `COMPETENCY` — demonstrable professional capability.
7. `PATTERN` — reusable solution form.
8. `ANTIPATTERN` — recurring harmful solution form.
9. `TECHNOLOGY` — language/runtime/framework/database/tool.
10. `REQUIREMENT` — functional or non-functional requirement.
11. `DECISION` — D0-D3 decision bundle.
12. `ALTERNATIVE` — candidate rejected or selected in a decision.
13. `RISK` / `FAILURE_MODE` — expected or observed failure.
14. `EXPERIMENT` / `BENCHMARK` — reproducible verification activity.
15. `RESULT` / `PROJECT_EVIDENCE` — measured evidence from our environment.
16. `TEST` / `REGRESSION_TEST` — executable verification and failure-prevention object.
17. `TASK` / `EVALUATION_CASE` — training/evaluation task with acceptance criteria.
18. `CRITIC_REVIEW` — independent falsification/review artifact.
19. `EXPERIENCE_RECORD` — normalized success/failure lesson.
20. `AGENT_CAPABILITY_STATE` — evidence-backed state of demonstrated competence.

## 4. Core edge classes

Examples:

- `SOURCE_SUPPORTS_CLAIM`
- `SOURCE_CONTRADICTS_CLAIM`
- `SOURCE_SUPERSEDES_SOURCE`
- `CLAIM_APPLIES_TO_TECHNOLOGY_VERSION`
- `CLAIM_REQUIRES_CONCEPT`
- `COMPETENCY_REQUIRES_CONCEPT`
- `PATTERN_SOLVES_REQUIREMENT`
- `ANTIPATTERN_CAUSES_FAILURE`
- `DECISION_USES_CLAIM`
- `DECISION_REJECTS_ALTERNATIVE`
- `RISK_THREATENS_DECISION`
- `EXPERIMENT_TESTS_CLAIM`
- `RESULT_SUPPORTS_CLAIM`
- `RESULT_REFUTES_CLAIM`
- `FAILURE_CAUSED_BY`
- `REGRESSION_TEST_PREVENTS_FAILURE`
- `TASK_TESTS_COMPETENCY`
- `CRITIC_CHALLENGES_DECISION`
- `EXPERIENCE_UPDATES_KNOWLEDGE`
- `AGENT_DEMONSTRATES_COMPETENCY`

Every material edge carries provenance: `created_from`, `source_ref` or `evidence_ref`, `created_at`, `review_state`, and `supersession` information where applicable.

## 5. What a "weight" means

Do not collapse all evidence into one number.

### 5.1 Evidence dimensions — stored separately

For source/claim relationships keep separate dimensions already defined in the evidence model:

- authority/source class;
- directness;
- freshness;
- exact version match;
- reproducibility;
- independence group;
- context fit;
- known limitations;
- counter-evidence state.

Initially these are categorical/ordinal metadata and are **not** summed into truth probability.

### 5.2 Measured empirical weights

Where the system has real observations, store raw measurements first:

```yaml
success_count: 0
failure_count: 0
independent_case_count: 0
critic_pass_count: 0
regression_count: 0
latency_samples: []
cost_samples: []
resource_samples: []
```

Derived metrics such as pass rate, failure recurrence, latency percentiles or cost distributions are allowed because they can be reconstructed from measurements.

### 5.3 Retrieval weights

Semantic/vector similarity, graph-distance penalties and query relevance may be numeric retrieval weights. They rank candidates for retrieval only; they do not establish truth.

### 5.4 Future calibrated decision weights

A learned/calibrated decision coefficient is permitted only after an evaluation corpus exists and the coefficient is validated against held-out decisions. Until then use `UNCALIBRATED` and preserve the component dimensions.

## 6. Volume model

The following is an engineering planning model, not a provider-size promise.

Assumptions used only for order-of-magnitude planning:

- normalized text chunk: ~4 KB average;
- chunk metadata/provenance: ~1 KB average;
- one embedding vector: model-dependent; planning placeholder ~6 KB/vector;
- other semantic graph node: ~2 KB average metadata/summary;
- graph edge including typed relation + dimensions/provenance: ~0.5 KB average;
- indexes/replication/backups are accounted for separately and can multiply physical storage.

### MIN — professional working MVP

Target already defined by roadmap:
- 12/12 domains;
- >=120 validated/limited Knowledge Objects;
- >=20 reviewable decision scenarios;
- >=10 end-to-end implementations.

Planning graph:
- ~5,000 source chunks;
- ~3,000 concept/competency/pattern/decision/evidence nodes;
- ~25,000 typed edges.

Approximate logical graph payload under the assumptions above: **well below 1 GB**. Plan **1–3 GB** for graph/vector/index overhead rather than optimizing prematurely.

Separate storage envelopes:
- raw/canonical source archive: **5–20 GB**;
- evaluation/code/test artifacts: **2–20 GB**;
- MIN total practical envelope: roughly **10–50 GB** before replicated backups.

### MEDIUM — strong senior-working layer

Roadmap target:
- >=500 Knowledge Objects;
- >=60 decision scenarios;
- >=40 end-to-end implementations.

Planning graph:
- ~30,000 chunks;
- ~15,000 other semantic nodes;
- ~200,000 edges.

Expected graph/vector payload remains small: plan **2–10 GB including working indexes**.

Separate envelopes:
- raw sources: **30–100 GB**;
- evaluation/benchmark/implementation history: **20–100 GB**;
- practical total: **50–250 GB** before full backup replication.

### MAX — principal/research expansion

Roadmap target:
- >=1,500 Knowledge Objects;
- >=150 decision scenarios;
- >=100 end-to-end evaluated implementations.

Planning graph:
- ~200,000 chunks;
- ~70,000 semantic nodes;
- ~1.5 million edges.

Plan **5–20 GB** for graph/vector/index working set depending on embedding model and database/index implementation.

Separate envelopes:
- raw/canonical sources: **100–500 GB**;
- evaluation/tournament/benchmark history: **100 GB–1 TB**;
- total practical envelope: approximately **0.2–1.5 TB** before long-retention build artifacts and replicas.

Multiple terabytes become plausible only when retaining heavy sandbox snapshots, binaries, container images, repositories, traces, datasets and tournament history. This is **training/evidence archive volume**, not the core semantic knowledge graph.

## 7. Shared-core rule

Do not provision storage as `N TB × number of agents`.

Preferred model:

```text
ENGINEERING SHARED KNOWLEDGE CORE
        ├─ PROGRAMMING_KB domain graph
        ├─ ARCHITECTURE_KB domain graph
        ├─ SECURITY_KB domain graph
        └─ shared standards / concepts / evidence

AGENT STATE
        └─ small profile delta: competence history, weaknesses, tournament record, policy/retrieval state
```

Canonical standards, algorithms, generic concepts and shared experience should be deduplicated and referenced by stable IDs.

## 8. Creation-time model

The bottleneck is **validation**, not downloading documents.

Assumptions for the accelerated estimate:
- 1 human/Principal reviewer available for material gates;
- 4–8 parallel research/drafting agent workers;
- automated source acquisition, deduplication and schema checks;
- official/licensed sources are accessible;
- reproducible sandbox exists for code/tests/benchmarks;
- the team does not simultaneously expand every language/framework.

### Phase A — graph/evidence contract

Deliver ontology, node/edge schemas, provenance, stable IDs, supersession and initial weight policy.

Estimated calendar effort: **2–4 focused days**.

### Phase B — canonical source map and ingestion pipeline

Build source registry, version/freshness controls, legal/licence fields, chunking and provenance verification.

Estimated effort: **3–7 focused days** for the first professional source layer.

### Phase C — MIN Knowledge Objects

Build and independently review >=120 objects across all 12 domains.

Expected drafting throughput can be high, but validation is the gate. Planning throughput after the pipeline stabilizes:
- candidate drafts: ~20–60/day across parallel workers;
- reviewed/promoted objects: ~10–20/day depending on complexity;
- experimental D2/D3 claims reduce throughput further.

Estimated effort: **2–4 weeks** including gap repair.

### Phase D — first evaluation corpus and D2 traces

Create >=20 decision scenarios and execute >=10 end-to-end with code/tests/evidence, with Principal Critic review.

Estimated effort: **1–2 additional weeks** if sandbox/tooling is ready.

### MIN working Programmer KB

Accelerated planning range: **3–6 weeks cumulative** after active build starts under the assumptions above.

If done mostly sequentially/manual with one research agent and irregular human review: plan approximately **2–4 months**.

### MEDIUM

Cumulative planning range: **2–4 months** with sustained parallel acquisition/validation and regular evaluation runs.

### MAX

Cumulative planning range: **6–12 months** for broad principal/research coverage, followed by continuous maintenance. MAX is not a terminal state because runtimes, frameworks, standards and project evidence continue to change.

These are planning ranges, not delivery promises. Actual velocity must be replaced by observed throughput after the first 30–50 validated objects and first 5 end-to-end cases.

## 9. Minimum creation conditions

PROGRAMMING_KB may be called a knowledge system rather than a document collection only if all of the following exist:

1. stable IDs for sources, claims, concepts, competencies, decisions and evidence;
2. explicit provenance down to source/version/chunk;
3. legal/licence/access state for acquired source material;
4. version and freshness/supersession control;
5. no unsupported synthetic truth/confidence score;
6. independent Critic for D3 and selected D2 samples;
7. executable sandbox for context-dependent claims;
8. tests/benchmarks stored as evidence, not only conclusions;
9. failure/counterexample memory retained;
10. hidden/independently controlled evaluation tasks before qualification claims;
11. backups and restore testing before the graph becomes irreplaceable IP;
12. protected/private storage for proprietary experience, hidden tests, decision coefficients and customer-specific evidence;
13. shared-core deduplication rather than isolated full copies per agent;
14. measurable throughput and cost instrumentation once ingestion begins.

## 10. Legal/source-content condition

Do not bulk-ingest copyrighted commercial books merely because they are useful references. Store bibliographic/source cards and independently produced Knowledge Objects; ingest full text only when the project has lawful access/right to do so. Public standards/specifications and project-owned/licensed material follow their applicable terms.

## 11. First implementation gate

Before choosing Neo4j/Qdrant/PostgreSQL/pgvector/another graph-vector stack, validate the data model in technology-neutral serialized fixtures.

First gate:

- >=30 representative nodes covering at least 10 node classes;
- >=100 typed edges covering support, contradiction, prerequisite, decision, experiment and failure relations;
- one full D2 trace from requirement to result;
- one supersession/freshness case;
- one failure → regression → knowledge-update case;
- one retrieval query proving provenance-preserving traversal.

Only after this fixture passes should storage-engine selection become a D2 architecture decision.

## 12. Immediate next pass

1. build ontology/schema fixtures;
2. map the existing 15 source cards and 7 Knowledge Objects into graph nodes;
3. add competency nodes for the 12 current domains;
4. create first explicit typed relations;
5. run Principal Critic against the model;
6. measure real serialized size and ingestion/retrieval timings;
7. replace this planning model with observed figures.
