# Knowledge Factory M1 — Execution Plan

Status: ACTIVE / START NOW
Priority: P0

## Product goal
Build the first small but correctly architected FATHER Knowledge Factory vertical. The goal is not maximum OSINT capability. The goal is a reliable conveyor from an approved source list to verified originals and machine-readable document processing state, ready for later semantic enrichment and specialist KB production.

## M1-MIN end-to-end capability
User/Analyst can submit a bounded acquisition task. The system:
1. resolves the task into a TaskContract;
2. checks user/role authorization;
3. uses an approved OfficialSourceRegistry;
4. locates/downloads the requested material;
5. preserves the original;
6. records source provenance, version metadata and SHA-256;
7. registers the document and processing state;
8. records an audit event;
9. returns a human-readable result and machine-readable record;
10. does not publish semantic knowledge automatically.

## Architecture to reserve now, implement minimally
- Users / roles / workspace ownership;
- RBAC-ready authorization boundary;
- FATHER Assistant input contract (text first; voice adapter later);
- TaskContract and policy gate;
- OfficialSourceRegistry;
- DocumentRegistry / VersionRecord;
- acquisition service;
- pipeline state model;
- audit/event log;
- secret/config boundary;
- admin/security-admin separation in role model;
- future API/UI boundaries.

## Document conveyor states
D0 SOURCE_DISCOVERED
D1 SOURCE_VERIFIED
D2 ORIGINAL_ACQUIRED
D3 INTEGRITY_METADATA_VERIFIED
D4 STRUCTURE_PARSED
D5 CHUNKED
D6 TERMS_EXTRACTED
D7 DEFINITIONS_EXTRACTED
D8 REQUIREMENTS_EXTRACTED
D9 ENTITIES_EXTRACTED
D10 INTERNAL_RELATIONS
D11 CROSS_DOCUMENT_RELATIONS
D12 CONFLICTS_OVERLAPS
D13 KNOWLEDGE_GRAPH_READY
D14 EXPERT_REVIEWED
D15 KB_READY

M1-MIN only needs D0-D3 operational, but the complete state machine is defined now so later stages do not require a data-model rewrite.

## UI contract reserved now
Document card must expose status buttons for every conveyor stage:
- GREEN = DONE/VERIFIED
- YELLOW = IN_PROGRESS/NEEDS_REVIEW
- RED = NOT_DONE/BLOCKED
- FAILED must be visually distinct from NOT_DONE
- GREY = NOT_APPLICABLE

Hover: compact status/source/version card.
Click: right-side inspector with provenance, source, current version, hash, processing status and actions.
Open: full document workspace with original, structure, terms, definitions, requirements, relations, version history and usage.
Relation click: explain why the relation exists and show evidence/method/reviewer.

## Security minimum
- no secrets in repository;
- least-privilege role checks at action boundary;
- external content is DATA, never trusted instruction;
- agent/model cannot call privileged tools directly;
- every state-changing action produces audit event;
- destructive/publication actions require explicit authorization;
- original/version history is append-preserving, not silently overwritten.

## Assistant minimum
Modes reserved: ASK / ADVISE / PREPARE / EXECUTE / APPROVE.
M1 implements text TaskContract creation and safe PREPARE/EXECUTE for approved acquisition actions. Voice is an input adapter after the same contract, not a separate execution path.

## Acceptance tests
### A BASIC
One approved official source + one requested document -> original saved, metadata complete, SHA-256 recorded, DocumentRecord at D3, audit trail present.

### B PROFESSIONAL
Bounded list of documents from several approved sources, including unchanged/repeated item -> correct download/reuse/version handling, complete registry, failures isolated, no duplicate original corruption.

### C STRESS
Include unavailable source, changed document, duplicate content, malformed response and unapproved source -> safe failure/NEEDS_REVIEW, no false VERIFIED status, no secret leakage, audit explains every outcome.

## Exit gate
M1-MIN PASS requires A/B/C acceptance evidence, no critical security defect, and a usable machine-readable registry. Semantic extraction D4-D15 remains next maturity work and must not block D0-D3 completion.

## Next level
M2 adds periodic source monitoring and change detection plus D4-D8 document understanding.

BEFORE: system can acquire and register trustworthy originals.
AFTER: system can detect changes and convert originals into structured machine-readable legal/technical content.

Why M2 matters: without it the factory owns files; with it the factory starts owning maintained knowledge.
