# Knowledge Factory — reuse-first target architecture

Status: TARGET ARCHITECTURE / architecture guardrail  
Scope: source discovery, acquisition, corpus reuse, verification, knowledge compilation, change monitoring, review/promotion  
Primary goals: **efficiency, reliability, traceability, controlled reuse**

## 1. Architecture decision

The system must not treat document downloading/parsing as its product value. Existing official APIs, public corpora, parsers, searchable legal databases and workflow libraries are donor systems.

FATHER/Knowledge Factory becomes a **verification, reconciliation, enrichment and controlled-promotion platform**.

Canonical principle:

`REUSE-FIRST → VERIFY → CANONICALIZE → ENRICH → RELATE → REVIEW → PROMOTE`

The current D0-D15 conveyor remains valid, but a mandatory **R-1 External Reuse Gate** is inserted before D0.

## 2. Non-negotiable architecture principles

1. **One canonical truth model.** External datasets, SQLite databases, RAG indexes and graph projections are donors/read models, never independent sources of truth.
2. **Exact evidence before legal claims.** A legal-currentness or exact-original claim requires trusted-source provenance and exact bytes/hash evidence according to source policy.
3. **External corpus != legal proof.** Bulk corpora may bootstrap coverage, text and metadata, but cannot silently satisfy A0/A1 proof requirements.
4. **Immutable evidence, replaceable derivations.** Originals and acquisition events are append-only; parsed structure, chunks, embeddings and projections are reproducible derived artifacts.
5. **Idempotent by design.** The same source/version/hash may be processed repeatedly without duplicate knowledge or lost provenance.
6. **Incremental processing.** Reprocess only the changed document/version and the dependency cone affected by that change.
7. **Fail closed at trust boundaries.** Transport failure, identity ambiguity, hash mismatch, lineage break, unresolved review or conflict candidate blocks promotion.
8. **Modular monolith first.** Keep one deployable codebase and explicit component boundaries until measured load justifies service extraction.
9. **No bespoke implementation without R-1 decision record.** Every new crawler/downloader/parser/indexer must have a documented REUSE / WRAP / FORK / REFERENCE / REJECT decision.
10. **Observability is part of correctness.** Every run has correlation ID, counters, timings, reuse/rework metrics and stage outcomes.

## 3. R-1 External Reuse Gate

Before implementing a capability, the system/reviewer performs:

- R-1.1: search official APIs/open data;
- R-1.2: search maintained open-source implementations;
- R-1.3: search existing corpora/knowledge bases/indexes;
- R-1.4: license/security/supply-chain review;
- R-1.5: freshness/coverage/provenance assessment;
- R-1.6: benchmark against golden fixtures;
- R-1.7: decision = `REUSE | WRAP | FORK | REFERENCE | REJECT`.

Minimum decision dimensions:

| Dimension | Question |
|---|---|
| Provenance | Can records be traced to the authoritative source? |
| Freshness | How are changes detected and how stale can data become? |
| Coverage | Which document classes/jurisdictions/years are covered? |
| Integrity | Are bytes/hashes/version identities available? |
| Structure | Are articles/points/sections preserved reliably? |
| License | Can code/data legally be used and redistributed? |
| Security | What execution/network/supply-chain risks are introduced? |
| Operability | Is the project maintained, testable and observable? |
| Integration cost | Is wrapping cheaper and safer than replacement? |
| Exit cost | Can the donor be replaced without changing canonical IDs? |

## 4. Target system boundaries

### 4.1 Control plane

Owns policy and orchestration, not source bytes.

Components:

- `KnowledgeTask / Watchlist Registry`
- `Source Catalog`
- `External Asset Registry`
- `Source/Trust Policy Engine`
- `Pipeline Orchestrator`
- `Review/Promotion Policy`
- `Telemetry/Reconciliation`

### 4.2 Evidence plane

Owns exact acquired artifacts and acquisition history.

Components:

- `Discovery Adapter`
- `Acquisition Broker`
- `Identity Resolver`
- `Version Resolver`
- `Content-Addressed Evidence Vault`
- `Acquisition Event Log`

### 4.3 Knowledge plane

Owns canonical derived knowledge objects.

Components:

- `Document Compiler` (D4-D5)
- `Knowledge Extractor` (D6-D9)
- `Relation/Conflict Engine` (D10-D12)
- `Knowledge Graph Projection` (D13)
- `Expert Review` (D14)
- `KB Promotion` (D15)

### 4.4 Serving plane

Read-only projections optimized for use by agents and humans.

- exact-document view;
- table view;
- graph view;
- BM25/full-text index;
- vector index;
- RAG retrieval API;
- MCP/API adapters.

Serving indexes are disposable and rebuildable from canonical storage.

## 5. Logical data flow

```text
                 ┌──────────────────────────┐
                 │ R-1 External Reuse Gate  │
                 └────────────┬─────────────┘
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
  Official APIs/OpenData  Existing corpora   Existing KB/search DB
          │                   │                    │
          └──────────────┬────┴──────────────┬─────┘
                         v                   v
                  Source/Asset Registry   Donor Import
                         │                   │
                         └─────────┬─────────┘
                                   v
                            Identity Resolver
                                   │
                                   v
                            Acquisition Broker
                                   │
                         ┌─────────┴─────────┐
                         v                   v
                  Evidence Vault       Acquisition Log
                    (CAS/SHA256)        (append-only)
                         │
                         v
                      D0-D3
                         │
                         v
                Document Compiler D4-D5
                         │
                         v
               Knowledge Extractor D6-D9
                         │
                         v
            Relations/Conflicts D10-D12
                         │
                         v
                   D13 canonical graph
                         │
                         v
                  D14 controlled review
                         │
                         v
                  D15 explicit promotion
                         │
             ┌───────────┼────────────┐
             v           v            v
           Search       Graph        RAG/MCP
```

## 6. Source and donor roles

Trust tier and system role are separate fields.

Suggested roles:

- `PROOF_SOURCE` — authoritative evidence capable of satisfying legal proof gates;
- `BOOTSTRAP_CORPUS` — bulk text/metadata coverage, not proof by itself;
- `NAVIGATION_SOURCE` — helps find/identify sources but cannot prove exact/current state;
- `REFERENCE_KB` — searchable external KB used for differential verification;
- `ALGORITHM_DONOR` — code/patterns reused or wrapped;
- `BENCHMARK_DATASET` — labeled or structured corpus used for regression/evaluation.

This prevents the common error "high coverage = high trust".

## 7. Storage architecture

### 7.1 M1/M2 local implementation

Keep the current repository-compatible implementation, but enforce contracts:

- exact originals: content-addressed filesystem under protected data root;
- metadata/registries: current JSONL while M1 is small;
- generated structures/chunks/knowledge: deterministic files keyed by document/version/parser;
- audit: append-only JSONL;
- reports: derived, disposable.

### 7.2 Production target

Use a small number of boring, proven stores:

- **S3-compatible object storage**: exact originals and large immutable artifacts;
- **PostgreSQL**: canonical source/document/version/knowledge/relation/review/audit metadata;
- **pgvector**: vector read model when needed;
- **PostgreSQL FTS or OpenSearch**: lexical search depending measured scale;
- optional queue: PostgreSQL-backed job queue initially; dedicated broker only when load requires it.

Do **not** introduce Neo4j as a second source of truth. Graph DB may later be a projection if measured query needs justify it.

## 8. Canonical identity model

Stable identity must survive changes in storage, donor and parser.

Canonical hierarchy:

`DocumentIdentity → DocumentVersion → OriginalArtifact → StructureNode → Chunk → KnowledgeObject`

Required identifiers:

- `document_id`: stable logical act/document identity;
- `version_id`: stable version identity tied to exact content/provenance;
- `artifact_sha256`: exact acquired bytes;
- `structure_node_id`: deterministic from document/version/locator/content;
- `chunk_id`: deterministic from node/version/chunk locator/content;
- `knowledge_object_id`: deterministic from type + normalized content + lineage where appropriate.

External IDs (`eoNumber`, donor primary keys, repository IDs) are aliases, not canonical IDs.

## 9. Acquisition architecture

`AcquisitionBroker` owns policy and delegates transport to adapters.

Adapters may include:

- official API adapter;
- official OpenData adapter;
- direct HTTP downloader;
- donor-corpus importer;
- local operator import fallback;
- repository/dataset importer.

The broker must:

1. resolve source policy;
2. validate requested document identity;
3. fetch/import bytes;
4. record final source locator;
5. calculate SHA-256 and byte length;
6. detect REUSED / NEW_VERSION / FAILED / BLOCKED;
7. persist exact bytes atomically;
8. append acquisition observation;
9. never mutate prior originals.

Browser/manual capture becomes **last-resort fallback**, not the normal path.

## 10. Bulk bootstrap strategy

Efficiency comes from separating **coverage acquisition** from **proof verification**.

### Bootstrap path

1. import an existing corpus/KB in bulk;
2. normalize donor metadata to tentative canonical identities;
3. deduplicate by stable aliases/hash/content fingerprints;
4. mark all imported knowledge as `UNVERIFIED_DONOR` / candidate;
5. use donor structure/text to prebuild indexes and candidate knowledge;
6. verify high-priority/current/legal-significant documents against official proof sources;
7. promote only objects whose policy requirements are satisfied.

This permits hundreds of thousands of documents to become searchable quickly without pretending that all are legally verified.

## 11. Change monitoring and bounded invalidation

Every watched document has a source-check policy.

```text
watchlist
  → discovery snapshot
  → identity match
  → remote metadata/content fingerprint
  → unchanged => NOOP/REUSED
  → changed => acquire exact bytes
  → new DocumentVersion
  → compute dependency cone
  → invalidate only affected D4-D13 artifacts
  → rebuild affected objects
  → create review delta
```

Dependency index records at minimum:

- version → structure nodes;
- node → chunks;
- chunk → knowledge objects;
- knowledge object → relations/conflicts;
- object/relation → graph projections;
- review decision → promoted object set.

Never rebuild the whole corpus for one changed document unless dependency reconciliation fails.

## 12. Reliability model

### 12.1 Idempotency

Every stage receives an idempotency key derived from:

`task_id + document_id + version_id + stage + algorithm_version + input_hashes`.

Repeated execution either reuses the prior valid result or creates a new derived version when inputs/algorithm changed.

### 12.2 Atomicity

- write to temporary path/table row;
- verify hash/count/manifest;
- atomically publish pointer/state;
- only then advance stage.

### 12.3 Retry policy

Retry only transient failures:

- timeout;
- connection reset;
- rate limit;
- temporary 5xx.

Do not retry automatically:

- identity mismatch;
- hash mismatch;
- policy violation;
- unsupported/ambiguous legal status;
- parser invariant failure.

Use bounded exponential backoff + jitter + circuit breaker per source.

### 12.4 Checkpointing

Checkpoint after durable output, never before it. Restart must resume from last verified durable stage without duplicating observations.

### 12.5 Dead-letter / quarantine

Unprocessable artifacts go to quarantine with:

- reason code;
- source/document IDs;
- exact input hash;
- stage/algorithm version;
- retryability flag;
- operator action required.

## 13. Quality and differential verification

Use **golden corpus + donor comparison**, not intuition.

For every parser/extractor version:

- compare FATHER output with approved golden documents;
- compare structure against one or more external structured corpora/KBs;
- measure precision/recall only where labeled truth exists;
- report disagreements as explicit candidates;
- never choose external output merely because it is external.

Initial golden corpus remains the four PDn documents already processed end-to-end.

## 14. Performance architecture

Priority order for optimization:

1. **reuse existing corpus/data** instead of reacquisition;
2. **hash/cache reuse** instead of reparsing unchanged bytes;
3. **incremental invalidation** instead of full rebuilds;
4. **parallelize by independent document/version**;
5. batch DB/index writes;
6. add workers only after queue/latency telemetry proves the need.

Parallelism rule:

- D0-D9: parallel per document/version;
- D10 internal relations: parallel per document;
- D11-D13: parallel by deterministic partition, then reconcile;
- D14-D15: controlled serialized governance boundary.

## 15. Security architecture

- external code is never executed merely because it exists on GitHub;
- donor repositories are pinned to commit/tag and reviewed before reuse;
- dependency/license/SBOM review for adopted components;
- network egress allowlist for source adapters;
- secrets outside repository;
- exact evidence storage separated from public GitHub in production;
- append-only audit with actor, action, object, result and correlation ID;
- no untrusted HTML/script execution during parsing;
- decompression limits and size limits for archives/documents.

## 16. Observability and SLOs

Every run emits:

- documents discovered / matched / acquired / reused / changed;
- bytes downloaded vs bytes reused;
- stage throughput;
- stage latency p50/p95;
- retry count and source error rate;
- rework ratio;
- cache/reuse ratio;
- parser/extractor version;
- quality-gate pass/fail counts;
- unresolved review count;
- dependency-cone size on change;
- corpus freshness age.

Initial SLO targets are not invented. They must be established after baseline telemetry. Until then report actual observed values only.

## 17. Component ownership and replaceability

| Component | Own | Replaceable donor? |
|---|---|---|
| Source adapters | transport/discovery mechanics | yes |
| External corpus importers | donor schema mapping | yes |
| Evidence vault | exact bytes/integrity | no, canonical boundary |
| Identity/version resolver | canonical IDs/version semantics | no |
| Document compiler | D4-D5 canonical structure contract | implementation replaceable, contract stable |
| Knowledge extractor | D6-D9 candidate contract | implementation replaceable, contract stable |
| Relation/conflict engine | D10-D12 | implementation replaceable, contract stable |
| Review/promotion | D14-D15 governance | no |
| Search/vector/graph indexes | read models | fully disposable/rebuildable |

## 18. Migration from current implementation

Do not rewrite the working D0-D13 code.

### Phase A — architecture guardrails

- add R-1 External Asset Registry;
- document donor roles and adoption decisions;
- keep current four-document corpus as golden regression fixture.

### Phase B — replace transport, not the conveyor

- add official API/OpenData adapter behind existing acquisition contract;
- retain operator import only as fallback;
- prove exact byte/hash/version equivalence on the four golden documents.

### Phase C — bulk corpus bootstrap

- add one donor-corpus importer;
- import a bounded sample first;
- reconcile identities against official source API;
- benchmark D4-D9 output against current golden results.

### Phase D — incremental watcher

- watchlist + scheduled discovery snapshots;
- automatic REUSED/NEW_VERSION decision;
- bounded downstream invalidation;
- delta review packet.

### Phase E — production persistence

- move canonical metadata/audit to PostgreSQL;
- move originals to protected object storage;
- rebuild serving projections from canonical data.

## 19. Stop conditions against overengineering

Do not introduce:

- microservices before measured independent scaling need;
- Kubernetes before a deployment/availability requirement demands it;
- Kafka before an event-volume/durability requirement justifies it;
- Neo4j before PostgreSQL/read-model graph queries become a measured bottleneck;
- a custom crawler when official API/OpenData or a safe reusable adapter exists;
- a custom parser without benchmark evidence that existing parsers fail required quality.

## 20. Immediate architectural backlog

P0-A1. Create `external_assets` registry and donor assessment schema.  
P0-A2. Register official API/OpenData, bulk corpus, searchable legal KB and downloader/parser donors.  
P0-A3. Implement one official-source adapter behind `AcquisitionService`; do not alter D4-D15 contracts.  
P0-A4. Differentially verify the four existing PDn documents across official source + donor corpus/KB.  
P0-A5. Import a bounded external corpus sample and measure identity/structure agreement.  
P0-A6. Implement watchlist snapshot/change detector with REUSED/NEW_VERSION semantics.  
P0-A7. Add dependency-indexed bounded invalidation and delta D14 review.  
P0-A8. Only after telemetry decide whether PostgreSQL/worker extraction is needed immediately.

## 21. Architecture success criteria

The architecture is successful when:

1. adding a new source is an adapter/configuration task, not a pipeline rewrite;
2. adding a donor corpus does not weaken trust/provenance rules;
3. an unchanged document causes near-zero downstream work;
4. a changed document reprocesses only its dependency cone;
5. every promoted knowledge object resolves back to exact evidence/version;
6. external indexes/databases can be deleted and rebuilt without loss of canonical knowledge;
7. donor replacement does not change stable document/knowledge IDs;
8. human review effort is proportional to meaningful deltas, not corpus size;
9. no stage can silently promote ambiguous or unverified knowledge;
10. throughput improvements are demonstrated by telemetry, not assumed from concurrency.
