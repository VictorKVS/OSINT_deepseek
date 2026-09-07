# FATHER OSINT — Hypothesis Graph Core

Status: DESIGN BASELINE v0.1

## Product decision

The first usable contour is **not a tool dashboard**. It is a manual, evidence-aware graph of investigative reasoning.

Tools are phase 2. Before any new Telegram/Web/Crypto/Geo integration, the analyst must be able to create, connect, challenge and revise hypotheses by hand.

## Why this is the core

Existing link-analysis products are strong at entities, links, transforms, path finding and large graph navigation. FATHER keeps those capabilities as a later entity graph, but adds a first-class reasoning layer so the graph can represent not only `who is connected to whom`, but also `what we think`, `why we think it`, `what contradicts it`, `what alternative explains the same observations`, and `what test would discriminate between versions`.

## Three graph layers

### Layer A — Reasoning graph (build first)

Node types:
- `RQ` — research question
- `HYP` — primary hypothesis
- `ALT_HYP` — competing/alternative hypothesis
- `FACT` — reviewed fact
- `CLAIM` — attributable source/actor statement
- `EVIDENCE` — reviewed evidence object
- `SRC` — source/observation identity
- `TEST` — planned discriminating check
- `RESULT` — result of a test
- `GAP` — missing information
- `CONFLICT` — explicit contradiction/dependency problem
- `DECISION` — analyst decision/review state

Core edges:
- `ADDRESSES` — hypothesis/question relation
- `SUPPORTS`
- `CONTRADICTS`
- `COMPETES_WITH`
- `DEPENDS_ON`
- `DERIVED_FROM`
- `OBSERVED_IN`
- `TESTED_BY`
- `PRODUCES`
- `REQUIRES`
- `RESOLVES`
- `WEAKENS`
- `REJECTS`
- `SUPERSEDES`

### Layer B — Entity graph (build second)

Node types include PERSON, ORGANIZATION, ACCOUNT, DOMAIN, IP, WALLET, TRANSACTION, DOCUMENT, LOCATION, EVENT and other case objects.

Entity relations such as OWNS, CONTROLS, USES_DOMAIN, TRANSFERRED_TO, MENTIONED_IN or LOCATED_AT are never automatically treated as facts. Each relation has a state and evidence bindings.

### Layer C — Fusion graph

Reasoning and entity graphs are joined through claims/evidence:

`SRC -> EVIDENCE -> FACT/CLAIM -> HYPOTHESIS`

and

`EVIDENCE -> ENTITY/RELATION`

This makes it possible to highlight the exact path from raw observation to a hypothesis or conclusion.

## Hypothesis object

Every hypothesis must store:
- stable ID
- statement
- lifecycle state
- scope
- competing hypothesis IDs
- supporting evidence IDs
- counter-evidence IDs
- missing discriminating evidence IDs
- next test IDs
- confidence rationale (ordinal/text only unless a calibrated model exists)
- analyst notes
- provenance/change history

Lifecycle:

`DRAFT -> OPEN -> SUPPORTED | WEAKENED | CONFLICTED -> REJECTED | CLOSED`

`SUPPORTED` does not mean proven. A hypothesis remains a hypothesis until a separate reviewed fact/conclusion process changes the object type.

## First screen

The initial screen must prioritize hypotheses rather than tools.

```text
+--------------------------------------------------------------------------------+
| CASE | Research question | graph mode | filters | version                      |
+----------------------+--------------------------------------+------------------+
| QUESTIONS / VERSIONS | REASONING GRAPH                      | INSPECTOR        |
|                      |                                      |                  |
| RQ-1                 |      [HYP-1] <----> [ALT-HYP-1]     | selected node    |
| HYP-1                |       /   \              /          | statement        |
| ALT-HYP-1            |   SUPPORT  COUNTER       GAP         | status           |
| Gaps                 |      |        |           |          | evidence for     |
| Tests                |   [EV-1]   [EV-2]      [TEST-1]     | evidence against |
| Conflicts            |      |        |                        | next tests       |
|                      |    [SRC]    [SRC]                      | history          |
+----------------------+--------------------------------------+------------------+
| CHANGE / REVIEW TRACE: who changed which node/edge and why                    |
+--------------------------------------------------------------------------------+
```

Tool drawer is hidden/disabled in Graph Core v0.1. Synthetic/manual evidence is enough for acceptance.

## Analyst actions in v0.1

- create question
- create primary hypothesis
- create alternative hypothesis
- link hypotheses as competitors
- add manual FACT / CLAIM / EVIDENCE / GAP / TEST nodes
- connect support/counter/dependency relationships
- change a hypothesis state with a reason
- compare two hypotheses side by side
- highlight unsupported hypotheses
- highlight evidence used by several hypotheses
- identify circular/source-dependent support
- show path `source -> evidence -> fact/claim -> hypothesis`
- preserve rejected/superseded hypotheses in history

## Guardrails

1. `FACT != CLAIM != INFERENCE != HYPOTHESIS != OPINION != RECOMMENDATION`.
2. A missing result is a GAP, not negative evidence.
3. Collector/tool failure later will be a GAP/FAILURE, not hypothesis rejection.
4. Multiple mirrors of one source do not count as independent evidence.
5. Numeric confidence is forbidden unless a named calibrated model and validation evidence are attached.
6. No hypothesis may silently become a fact.
7. Rejected hypotheses remain visible with rejection basis.
8. Every edge that changes analytical meaning is auditable.

## Build order

### G0 — Ontology freeze
- freeze node/edge vocabulary and lifecycle rules
- define validation of allowed edge pairs
- define IDs and append-only change record

### G1 — Manual graph store
- JSON/file repository for nodes, edges and revisions
- atomic mutation per graph command
- deterministic validation

### G2 — Reasoning canvas
- render nodes/edges from real store
- node inspector
- create/edit/link actions
- filters by object type/state

### G3 — Hypothesis comparison
- support/counter matrix
- competing hypotheses
- gaps/tests
- path-to-hypothesis
- circular/dependent evidence warnings

### G4 — Synthetic pilot
- one synthetic case with 2–4 competing hypotheses
- at least one conflict
- at least one rejected version retained
- at least one unresolved GAP and discriminating TEST

### G5 — Graph Core acceptance
Only after G0–G4 pass do we unlock Tool Router work.

## Explicitly deferred

Until Graph Core acceptance, do not expand:
- Telegram integrations
- Bitcoin/TRON adapters
- Web/DNS/RDAP/CT tools
- Geo/map tooling
- media/Narrative Drift collection adapters
- Kali inventory/adapters
- automation of hypothesis generation

Existing integrations remain available for regression compatibility but are not the active product-development priority.
