# FATHER Library Order Conveyor

## Purpose

A `LIBRARY_ORDER` is the operator-facing unit for requesting, acquiring, organizing and processing the base library for one FATHER role.

Example:

`PROGRAMMER + MIN -> acquire role library -> coverage -> compiler -> knowledge extraction -> relations -> analyst/critic -> human review -> PROGRAMMING_KB`

The order is traceable from the UI action to every downloaded artifact and downstream knowledge candidate.

## Operator inputs

- `role_id`
- target `knowledge_base_id` (resolved from the role registry)
- maturity target: `MIN`, `MEDIUM`, or `MAX`
- source channels: `OFFICIAL_WEB`, `GITHUB`, `TELEGRAM`, `LOCAL_LIBRARY`
- execution mode: `AUTO_BOUNDED` or `REVIEW_EACH_STAGE`
- optional topic subset; default is every topic registered for the role

## Stage model

1. `ORDER_CREATED`
2. `STAGE_1_ACQUISITION`
   - build bounded searches for every role topic;
   - acquire only allowed/authorized payloads;
   - route payloads to `data/team_role_telegram/<role>/<target-id>/` for Telegram and equivalent source-specific stores;
   - preserve provenance and SHA-256;
   - commercial books from unverified mirrors remain discovery records and are not automatically downloaded.
3. `STAGE_1_COVERAGE`
   - measure topic coverage;
   - expose authoritative/practice/validation gaps separately;
   - raw material counts do not prove maturity.
4. `STAGE_2_DOCUMENT_COMPILER`
   - select adapter by material profile and file type;
   - preserve exact original identity;
   - generate structured text/chunks.
5. `STAGE_3_KNOWLEDGE_EXTRACTION`
   - definitions, requirements/claims, entities, concepts;
   - every candidate keeps evidence lineage.
6. `STAGE_4_RELATIONS_AND_CONFLICTS`
   - internal/cross-source relations;
   - conflicts and applicability/version edges remain candidates until reviewed.
7. `STAGE_5_ANALYST_AND_CRITIC`
   - main analyst compares materials;
   - Socrates/Critic challenges unsupported or conflicting claims.
8. `STAGE_6_REVIEW`
   - explicit human review gate.
9. `KB_READY`
   - only reviewed packages can be promoted; no autonomous KB promotion.

## Automation boundary

The order may run automatically through every deterministic and policy-approved stage. A missing collector, missing adapter, rights uncertainty, insufficient evidence, or a semantic conflict must stop or degrade the order with an explicit GAP/BLOCKED state rather than being guessed away.

## Current implementation status

- Role registry: implemented.
- Telegram role acquisition with up to five search/download streams: implemented.
- Per-topic Telegram coverage assessment: implemented.
- Live byte-level download progress: implemented.
- Trace/task/command IDs: implemented in OSINT Control Center.
- `LIBRARY_ORDER` control object and Stage-1 orchestrator: introduced by this feature.
- Official Web/GitHub/Local collectors are routed as source channels in the order contract; each channel must report its actual implementation state and cannot be silently treated as complete.
- Full cross-profile Stage 2+ orchestration is adapter-driven; unsupported material types remain explicit handoff gaps.

## Acceptance rules

A role library order is not `KB_READY` merely because files were downloaded. At minimum:

- source policy is satisfied;
- required maturity dimensions are covered or explicitly GAPped;
- every material has provenance;
- acquired bytes have SHA-256;
- compiler and semantic stages preserve lineage;
- review is complete;
- no unresolved blocking rights/source/semantic gap exists.

## Production metrics

For each order record only observed values:

- topics total / covered / gap;
- source channels attempted / successful / blocked;
- search hits / candidates / downloaded / reused / failed;
- bytes downloaded;
- elapsed time and throughput;
- rework/retry counts;
- current stage and blocked reason;
- speedup vs one stream only when a same-queue one-stream baseline exists;
- ETA only when remaining volume and throughput telemetry are sufficient.
