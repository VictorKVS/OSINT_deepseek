# J-021 — Knowledge Factory Conveyor: global WIP override

**Date:** 2026-08-22  
**Status:** ACTIVE / P0 / WIP OVERRIDE  
**Decision owner:** Product/System Owner  
**Execution branch:** `agent/knowledge-factory-m1`

## Trigger

The project has accumulated useful OSINT, evidence, analyst, source-policy, document-registry, knowledge-model and specialist-KB work, but delivery is fragmented across parallel tracks. The immediate priority is no longer to expand individual collectors, agents or specialist knowledge domains. The priority is to turn the existing capabilities into one repeatable production conveyor that finds material, preserves evidence, converts it into structured knowledge, checks it and prepares it for controlled publication into knowledge bases.

## Decision

Effective immediately, all non-blocking feature/product/research work is placed in **HOLD**. Existing branches, issues, research notes and prototypes are preserved; they are not deleted and do not lose priority history. New work may enter active WIP only if it directly removes a blocker from the Knowledge Factory conveyor described below.

The single active P0 objective is:

> **Build a reusable Knowledge Factory that receives a bounded knowledge task and reliably produces traceable, reviewable, machine-readable knowledge-base objects from verified source material.**

Frozen DEV v1 semantics remain protected. This override changes active priority and integration order; it does not authorize silent modification of established provenance invariants or automatic truth publication.

## Unified conveyor

```text
KNOWLEDGE TASK / DOMAIN SCOPE
        ↓
SOURCE DISCOVERY
        ↓
SOURCE TRUST / AUTHORITY / APPLICABILITY CHECK
        ↓
EXACT ARTIFACT ACQUISITION
        ↓
ORIGINAL PRESERVATION + MIME + SIZE + SHA-256
        ↓
DOCUMENT / VERSION / LIFECYCLE REGISTRY
        ↓
STRUCTURE PARSING
        ↓
SEMANTIC / LEGAL CHUNKING
        ↓
TERMS + CONCEPTS + DEFINITIONS
        ↓
ATOMIC FACTS / REQUIREMENTS / RULES / CLAIMS
        ↓
ENTITIES + ACTORS + CONTROLS + METHODS
        ↓
INTERNAL RELATIONS
        ↓
CROSS-DOCUMENT RELATIONS
        ↓
VERSION / APPLICABILITY / DEPENDENCY EDGES
        ↓
CONFLICT / OVERLAP / DUPLICATE / UNCERTAINTY CHECK
        ↓
ANALYST REVIEW
        ↓
SOCRATES / CRITIC REVIEW
        ↓
KNOWLEDGE-GATE CANDIDATE
        ↓
KB-READY PACKAGE
        ↓
REUSE + CHANGE MONITORING + REGRESSION
```

## Mandatory object chain

Every accepted source item must be traceable through stable identifiers:

```text
Task
 → Source
 → AcquisitionEvent
 → OriginalArtifact
 → Document
 → DocumentVersion
 → StructureNode
 → Chunk
 → Term / Concept / Definition
 → Fact / Requirement / Rule / Claim
 → Entity / Control / Method
 → Relation
 → ConflictOrGap
 → ReviewDecision
 → KnowledgeObject
```

No stage may erase the identity or provenance of the previous stage.

## Required material profiles

The conveyor is generic, but profile semantics are not mixed:

- `LEGAL` — legal lifecycle, publication/effective dates, amendment/repeal/supersession and exact clause locators are mandatory where applicable.
- `STANDARD` — edition/version, issuer, normative status and clause locators.
- `BOOK` — author, title, edition, publisher, year, ISBN where available, chapter/section/page structure; no legal-status semantics.
- `SCIENCE` — authorship, venue, date, DOI/identifier, methodology/evidence context.
- `VENDOR_DOC` — product/version/vendor applicability and documentation revision.
- `WEB/SIGNAL` — discovery or supporting evidence with explicit lower trust and freshness controls.

## Production stages

The D0-D15 state machine remains the common document conveyor:

| Stage | Meaning | Exit evidence |
|---|---|---|
| D0 | SOURCE_DISCOVERED | source identity recorded |
| D1 | SOURCE_VERIFIED | trust class/basis and scope recorded |
| D2 | ORIGINAL_ACQUIRED | exact bytes preserved |
| D3 | INTEGRITY_METADATA_VERIFIED | MIME/size/SHA-256/version metadata complete |
| D4 | STRUCTURE_PARSED | deterministic structure tree |
| D5 | CHUNKED | stable chunks with source locators |
| D6 | TERMS_EXTRACTED | terms/concepts with occurrence provenance |
| D7 | DEFINITIONS_EXTRACTED | definitions separated from mentions |
| D8 | REQUIREMENTS_EXTRACTED | atomic obligations/rules/claims |
| D9 | ENTITIES_EXTRACTED | actors/entities/controls/methods |
| D10 | INTERNAL_RELATIONS | within-document typed edges |
| D11 | CROSS_DOCUMENT_RELATIONS | typed inter-document edges |
| D12 | CONFLICTS_OVERLAPS | conflicts, overlaps, duplicates and gaps classified |
| D13 | KNOWLEDGE_GRAPH_READY | graph/table/document projections reconcile |
| D14 | EXPERT_REVIEWED | human/critic decision and limitations recorded |
| D15 | KB_READY | immutable evidence links + reviewed knowledge package |

`DONE` is not equivalent to `VERIFIED`. A stage can be complete but still require review.

## Workstream allocation under the override

All available execution capacity is redirected to the same critical path. Parallel work is allowed only where outputs join the same conveyor:

1. **Acquisition & Source Trust** — official-source registry, source policy, exact artifact acquisition, retries, integrity metadata, versions.
2. **Document Compiler** — structure, chunks, locators, stable IDs and profile-specific parsing.
3. **Knowledge Extraction & Graph** — concepts, definitions, atomic requirements/facts/claims, entities and typed relations.
4. **Conflict / Analyst / Socrates** — cross-document comparison, applicability, contradictions, uncertainty, review decisions and promotion boundaries.
5. **Platform / QA / Telemetry** — storage, RBAC, audit, regression, BASIC→PROFESSIONAL→STRESS fixtures, throughput/rework counters, UI projections and reconciliation.

These are not five independent products. They are five lanes of one factory and must converge on shared contracts.

## Explicit HOLD

Until the conveyor reaches its acceptance gate, the following are HOLD unless needed to remove a direct P0 blocker:

- further Telegram transport competition beyond proven acquisition needs;
- unrelated OSINT tool expansion;
- autonomous Investigation Engine / R2+ hypothesis automation;
- new specialist agents as standalone products;
- Programmer Agent feature expansion outside reuse of the common Knowledge Factory;
- UI polish that does not prove graph/table/document traceability;
- deep/RL training experiments;
- production-scale infrastructure migration;
- speculative commercial features.

HOLD means preserve and reconcile later; it does not mean reject or delete.

## M1 first executable target

First prove D0-D3 end-to-end on a bounded mixed corpus:

```text
approved task
 → verified source
 → locate exact item
 → acquire bytes
 → preserve original
 → compute SHA-256
 → record MIME + byte length
 → record document/version/lifecycle
 → audit every state change
 → deterministic machine-readable result
```

No source receives `ORIGINAL_ACQUIRED`, `IMMUTABLE` or equivalent status without real bytes and a computed hash.

## Acceptance ladder

### BASIC
One legally significant document and one book complete D0-D3 with profile-correct metadata, preserved originals, SHA-256, registry and audit reconciliation.

### PROFESSIONAL
A bounded multi-source corpus handles unchanged items, new versions, duplicates, several document types, source failures and repeated runs without corrupting provenance or creating duplicate knowledge identities.

### STRESS / RED TEAM
Unavailable source, malformed response, changed bytes, misleading mirror, conflicting documents, invalid lifecycle transition, duplicate payload from independent observations, parser failure and forced budget stop all produce explicit safe states. No false VERIFIED status, no silent provenance loss and no autonomous KB promotion are permitted.

## Next maturity after D0-D3

Once acquisition is frozen green, advance the same corpus through D4-D15 rather than starting a new research track. Each stage gets:

```text
contract
 → fixtures
 → implementation
 → deterministic tests
 → regression
 → telemetry
 → review
 → freeze
```

## Knowledge reuse rule

The factory must never require rereading an original when an already verified reusable object answers the new task. Before extraction or research it checks existing stable IDs, hashes, versions, concepts, relations and prior review decisions.

Reprocessing is triggered only by one of:
- new/changed bytes;
- new document version or lifecycle state;
- changed parser/method version;
- newly discovered applicability context;
- unresolved conflict/gap;
- failed regression or explicit expert re-review.

## Metrics

Every run records at minimum:
- tasks opened/completed/blocked;
- sources discovered/verified/rejected;
- acquisition attempts/successes/failures;
- bytes acquired and artifacts reused;
- unique hashes and version changes;
- documents advanced by D-stage;
- chunks/concepts/definitions/requirements/entities/relations created and reused;
- conflict candidates/confirmed conflicts/context splits/gaps;
- review PASS/REWORK/INCONCLUSIVE;
- processing time and human review time where measurable;
- rework ratio and reuse ratio;
- failures by stage/reason.

Speedup claims versus a one-stream baseline are published only when both baselines have sufficient measured telemetry. No invented percentages or completion forecasts.

## Completion gate for the override

The WIP override remains active until all of the following are true:

1. one canonical end-to-end conveyor contract exists;
2. D0-D3 pass BASIC, PROFESSIONAL and STRESS acceptance;
3. exact originals, versions and audit survive repeated runs;
4. one bounded corpus reaches D15 through the same stable object chain;
5. graph/table/document projections reconcile to the same records;
6. contradictions and uncertainty cannot silently become facts;
7. direct autonomous promotion to KB is blocked;
8. run telemetry reconciles with registries;
9. clean regression protects the frozen DEV v1 baseline;
10. a second domain/material profile reuses the conveyor without a bespoke rewrite.

Only after this gate may the System Owner reopen held product tracks.

## Result

**Decision:** PASS — WIP override accepted.  
**Current P0:** Knowledge Factory Conveyor.  
**Next action:** consolidate M1 branch, prove source-policy + D0-D3 acquisition, then drive the same corpus through D4-D15 with evidence and regression.
