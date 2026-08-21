# Knowledge Factory UI — Graph / Table / Document Contract

Status: ACTIVE DESIGN CONTRACT

## Product principle
The same knowledge model must be viewable without data loss in three synchronized forms:

1. GRAPH — relationships and propagation are visually obvious.
2. TABLE — sortable/filterable professional work with explicit fields.
3. DOCUMENT/CLAUSE LIST — exact documents, versions, articles/paragraphs and citations.

No view owns separate truth. All views project the same node/relation/document records.

## Themes
The product supports:
- DAY
- NIGHT
- SYSTEM

Theme changes appearance only; statuses, semantic node types and accessibility meaning remain invariant.

## Node semantics
Use distinct semantic colors for node types, not random decoration:
- document: blue
- clause/article/paragraph: cyan
- term: violet
- definition: purple
- requirement/rule: amber
- entity/actor: teal
- control/measure: green
- conflict/contradiction: red
- source: indigo
- method/calculation: orange
- unknown/unclassified: gray

Color must always be accompanied by node type/icon/text for accessibility.

## Interaction
### Hover node
Show compact popover:
- label;
- node type;
- document count;
- verification/status;
- most important source/document refs.

### Click node
Open right-side inspector:
- node identity/type;
- all connected relations grouped by type;
- documents containing the node;
- exact article/paragraph/clause locators;
- definitions/requirements where applicable;
- provenance;
- review state;
- “open as table” and “open document refs” actions.

### Double click / Open
Open full workspace focused on the node with tabs:
- Overview
- Relations
- Documents
- Clauses
- Timeline/versions
- Evidence
- Audit

### Click edge
Open relation inspector:
- from/to node;
- relation type;
- evidence documents;
- exact article/paragraph/clause numbers;
- rationale;
- method/version;
- author/agent;
- reviewer;
- state: DRAFT / VERIFIED / CONFLICTED / REJECTED.

## Table projection
Every graph node can be represented as a row with:
- node_id
- node_type
- label
- document_count
- document_ids
- clause_locators

Every relation can be represented as a row with:
- relation_id
- from_node_id
- to_node_id
- relation_type
- status
- evidence_documents
- evidence_clauses
- rationale
- method_ref
- reviewer

This lets an investigator switch from a visual graph to a spreadsheet-like evidence view without losing traceability.

## Document card conveyor
Each document card shows D0-D15 processing stages as interactive status buttons:
- GREEN = DONE/VERIFIED
- YELLOW = IN_PROGRESS/NEEDS_REVIEW
- RED = NOT_DONE/BLOCKED
- FAILED = distinct error treatment
- GREY = NOT_APPLICABLE

Clicking a stage opens:
- prerequisites;
- inputs;
- outputs;
- method/algorithm version;
- execution/review history;
- affected nodes;
- next permitted action.

## Investigator-oriented workspace
Recommended layout:

```text
┌ Navigation ┬──────────── Main workspace ────────────┬ Inspector ┐
│ Dashboard  │ Graph / Table / Document / Matrix     │ Node      │
│ Sources    │                                        │ Relation  │
│ Documents  │                                        │ Evidence  │
│ Graph      ├────────────────────────────────────────┤ Clauses   │
│ Reviews    │ Processing / Agent / Audit trace       │ History   │
│ Security   │                                        │           │
└────────────┴────────────────────────────────────────┴───────────┘
```

## M1 implementation boundary
M1 does not need a complete graph UI. It must establish contracts that prevent a later rewrite:
- day/night/system theme enum;
- semantic node type tokens;
- graph/table projections from one model;
- document and clause references on nodes/relations;
- processing-stage status tokens;
- relation inspector evidence fields.

The actual interactive graph renderer belongs to the next UI implementation increment after OfficialSource/DocumentRegistry and D0-D3 acquisition are operational.
