# Knowledge Factory Conveyor — P0 Execution Contract

**Status:** ACTIVE / P0  
**Parent decision:** `docs/journal/J-021_2026-08-22_KNOWLEDGE_FACTORY_CONVEYOR_WIP_OVERRIDE.md`  
**Execution branch:** `agent/knowledge-factory-m1`

## Product result

Build one reusable system that can take a bounded request such as “collect and build a knowledge base for domain X” and return a traceable reviewed KB package without manual reinvention of the processing method for each document.

The system must combine:

1. OSINT/source discovery;
2. source trust and applicability control;
3. exact artifact acquisition and immutable evidence;
4. document/version registry;
5. document compiler;
6. knowledge extraction;
7. typed knowledge graph;
8. conflict/overlap/uncertainty analysis;
9. Analyst/Socrates review;
10. controlled KB-ready publication package;
11. change monitoring, reuse and regression.

## Canonical command

Conceptual input:

```text
KnowledgeTask(
  domain,
  scope,
  material_profiles,
  source_policy,
  target_outputs,
  budgets,
  review_policy
)
```

Conceptual output:

```text
KnowledgeRunResult(
  task_id,
  source_registry_delta,
  artifact_manifest,
  document_registry_delta,
  knowledge_objects,
  relations,
  conflicts_and_gaps,
  review_decisions,
  kb_ready_packages,
  metrics,
  audit_refs
)
```

## Architecture boundaries

```text
TaskContract
   ↓
Source Discovery / Source Policy
   ↓
Acquisition Engine
   ↓
Artifact Store + Document Registry
   ↓
Document Compiler
   ↓
Knowledge Extractor
   ↓
Knowledge Graph / Relation Engine
   ↓
Conflict & Applicability Engine
   ↓
Analyst
   ↓
Socrates / Critic
   ↓
Promotion Request / Knowledge Gate boundary
   ↓
KB-ready package
```

The Knowledge Gate remains the sole promotion authority. A model, collector or extractor may propose but must not silently publish truth.

## Phase P0.1 — Consolidate contracts

- [ ] Reconcile `main` and `agent/knowledge-factory-m1` without losing the frozen DEV v1 baseline.
- [ ] Freeze common IDs and schemas for Source, AcquisitionEvent, Artifact, Document, DocumentVersion and AuditEvent.
- [ ] Freeze legal/book/standard/science/vendor/web material-profile boundaries.
- [ ] Freeze D0-D15 transitions and prerequisites.
- [ ] Freeze RBAC action matrix and privileged promotion boundary.
- [ ] Freeze graph/table/document/clause projection contract.
- [ ] Add traceability rows from requirements to tests and code paths.

**Gate P0.1:** no ambiguous identity, provenance, promotion or stage-transition semantics.

## Phase P0.2 — D0-D3 acquisition vertical

- [ ] Load approved `SourcePolicy` records from a machine-readable registry.
- [ ] Resolve a task only against allowed source policy, unless explicitly in discovery mode.
- [ ] Locate exact source item and record locator/discovery event.
- [ ] Acquire exact bytes with bounded retry/timeout behavior.
- [ ] Validate content/signature/MIME as far as profile and transport allow.
- [ ] Compute SHA-256 from acquired bytes.
- [ ] Record byte length, MIME, filename, acquisition timestamp and source locator.
- [ ] Preserve original bytes in content-addressable/version-safe storage.
- [ ] Create/update Document + DocumentVersion without overwriting prior versions.
- [ ] Record legal lifecycle/status metadata where `LEGAL` applies.
- [ ] Reuse unchanged bytes by hash while preserving independent acquisition/provenance events.
- [ ] Emit append-only audit events.
- [ ] Emit reconciled acquisition metrics.

**Gate P0.2:** BASIC / PROFESSIONAL / STRESS all green.

## Phase P0.3 — Document Compiler D4-D5

- [ ] Detect/declare parser profile and parser version.
- [ ] Preserve raw-to-structure locator mapping.
- [ ] Produce stable structure tree: document → part/chapter/section/article/paragraph/clause/page as profile allows.
- [ ] Create stable semantic/legal chunks without losing exact source locators.
- [ ] Store parser failures explicitly; no silent text loss.
- [ ] Support deterministic re-run with unchanged bytes + unchanged parser version.

**Gate P0.3:** all chunks resolve back to original artifact + structure locator.

## Phase P0.4 — Knowledge extraction D6-D9

- [ ] Extract terms/concepts separately from definitions.
- [ ] Extract definitions with exact locators and defining context.
- [ ] Extract atomic facts/requirements/rules/claims without implicit type casts.
- [ ] Extract actors/entities/controls/methods.
- [ ] Attach extraction method/version and provenance to every object.
- [ ] Reuse existing concept/definition/requirement objects when identity/equivalence is proven.
- [ ] Record uncertainty rather than fabricating absent values.

**Gate P0.4:** every knowledge object has typed identity, source evidence and method provenance.

## Phase P0.5 — Relations and comparison D10-D12

- [ ] Build internal relations within each document.
- [ ] Build cross-document typed relations.
- [ ] Build version/amendment/repeal/supersession edges.
- [ ] Build applicability/context edges.
- [ ] Detect duplicate/same-as candidates separately from confirmed equivalence.
- [ ] Detect definition/requirement conflicts and overlaps.
- [ ] Detect evidence dependence/circularity.
- [ ] Preserve both sides of conflicts with provenance.
- [ ] Distinguish `CONFLICT`, `CONTEXT_SPLIT_REQUIRED`, `OVERLAP`, `DUPLICATE_CANDIDATE`, `GAP`, `UNKNOWN`.

**Gate P0.5:** no candidate difference becomes a legal/technical conflict without explicit classification evidence.

## Phase P0.6 — Graph, review and KB package D13-D15

- [ ] Reconcile graph/table/document/clause views from one canonical model.
- [ ] Analyst produces normalized review package.
- [ ] Socrates/Critic challenges source independence, applicability, contradictions, missing evidence and unsupported promotions.
- [ ] Produce `PASS | REWORK | INCONCLUSIVE` decision with reasons.
- [ ] Generate promotion request only; direct uncontrolled KB publication remains impossible.
- [ ] Create KB-ready package containing knowledge objects plus immutable source/audit references.
- [ ] Preserve rejected/reworked history rather than overwriting it.

**Gate P0.6:** one bounded corpus reaches D15 with full traceability.

## Phase P0.7 — Change monitoring and reuse

- [ ] Monitor approved sources by source-specific cadence/method.
- [ ] Detect changed bytes, metadata or lifecycle status.
- [ ] Recompile only affected downstream objects.
- [ ] Propagate invalidation/review flags through dependency graph.
- [ ] Reuse unchanged artifacts, chunks, concepts and reviewed decisions where valid.
- [ ] Record method/parser/model version changes as possible reprocessing triggers.
- [ ] Run regression fixtures on every material pipeline change.

**Gate P0.7:** update one source version and prove bounded impact propagation without full-library rebuild.

## Acceptance corpus

The first corpus must intentionally mix at least two material profiles and contain:

- a current authoritative/official document;
- an amended/versioned document;
- a superseded/repealed or obsolete document where available;
- a book or other non-legal source;
- duplicate content from different observations;
- conflicting or context-dependent definitions/requirements;
- one unavailable/malformed source fixture;
- one changed artifact fixture.

Synthetic fixtures prove behavior only. External-world truth claims require source evidence.

## Five conveyor lanes

Parallel execution is permitted only as lanes feeding the same gates:

| Lane | Responsibility | Main gate |
|---|---|---|
| A | Source policy + acquisition + originals + versions | P0.2 |
| B | Structure + chunks + deterministic compiler | P0.3 |
| C | Concepts + definitions + facts/requirements/entities | P0.4 |
| D | Relations + conflicts + Analyst/Socrates | P0.5–P0.6 |
| E | Storage + RBAC + audit + metrics + regression + projections | all gates |

A lane may not start speculative downstream work that lacks upstream contracts or fixtures.

## Production telemetry

Per run and cumulative:

```text
tasks
source candidates / verified / rejected
acquisition attempts / successes / failures
bytes acquired
artifacts created / reused
unique hashes
versions created / changed
D0..D15 transitions
structures / chunks
concepts / definitions
facts / requirements / claims
entities / controls / methods
relations
conflict candidates / confirmed / context splits / gaps
review PASS / REWORK / INCONCLUSIVE
reused objects
reprocessed objects
stage failures
human review time (when measured)
machine/tool cost (when measurable)
```

Derived speedup, remaining-volume and completion forecasts are allowed only when sufficient comparable telemetry exists.

## Stop conditions

Stop/fail safely when:
- task budget expires;
- source is outside policy and no explicit discovery authorization exists;
- exact bytes required by the gate cannot be obtained;
- integrity/hash cannot be computed;
- stage prerequisite is missing;
- parser/extractor returns untraceable output;
- promotion lacks required review;
- registry/audit counters do not reconcile.

A safe stop is a valid explicit result; fabrication is not.

## Definition of Done for P0

P0 is complete when:

1. D0-D15 works as one pipeline, not a collection of documents/scripts;
2. at least two material profiles pass through the same reusable architecture;
3. exact originals and version history are retained;
4. every KB object resolves to evidence and method provenance;
5. conflicts/gaps/uncertainty remain explicit;
6. Analyst/Socrates review is traceable;
7. uncontrolled promotion is blocked;
8. graph/table/document views reconcile;
9. change propagation and reuse are proven;
10. regression + telemetry are green and reproducible.

Until then, unrelated expansion remains HOLD.
