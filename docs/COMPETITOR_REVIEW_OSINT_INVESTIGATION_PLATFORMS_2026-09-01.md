# Competitor review — OSINT / investigation / graph / evidence / blockchain platforms

> Date: 2026-09-01
> Purpose: identify capabilities worth adopting into the target OSINT Acquisition Workbench.
> Rule: competitor features are treated as design references, not copied UX or proprietary logic.

## 1. Executive conclusion

No single reviewed platform combines all of the following equally well:

- automated source acquisition;
- investigative graph;
- strict evidence provenance and capture;
- entity resolution;
- case workflow;
- query planning;
- OSINT + corporate + legal + logistics + blockchain;
- Red Team / contradiction management;
- formal decision-ready reporting with finding-to-source traceability.

The strongest target architecture is therefore a synthesis rather than a clone.

Recommended product positioning:

> **Investigation Operating System** = Maltego-style pivots + Aleph-style investigative memory + Hunchly-grade evidence capture + Linkurious/Siren graph case workflow + OpenCTI-style source-linked knowledge + ShadowDragon/Babel Street collection/monitoring + GraphSense/Chainalysis-style crypto tracing + formal report/evidence governance.

---

## 2. Maltego — strongest idea: Transform ecosystem

### Useful ideas
- transforms as reusable pivots from one entity to another;
- Data Hub for integrations/providers;
- internal transform distribution for private enterprise sources;
- collaboration server/shared graphs;
- ability to integrate internal organizational data without exposing it externally.

### What to adopt
Create a **Source/Transform SDK** where each integration declares:

```yaml
transform_id:
input_entity_types:
output_entity_types:
source_id:
required_credentials:
legal_scope:
rate_limit:
parser_version:
evidence_capture_mode:
confidence_policy:
```

Every transform output must include provenance and journal events, which is stricter than the usual graph-pivot model.

### Improvement over Maltego
Do not let a transform simply create an edge. Require:
`source → raw capture → claim → normalized relation → confidence/status`.

---

## 3. OCCRP Aleph — strongest idea: investigative memory + cross-referencing

### Useful ideas
- investigations as first-class workspaces;
- structured and unstructured data in the same environment;
- secure document/leak upload;
- OCR/search over scanned documents;
- network diagrams and timelines;
- lists of people/companies cross-referenced against hundreds of datasets;
- dataset categories and countries;
- alerts when tracked names/entities appear in new or updated datasets.

### What to adopt
1. **Investigation workspace as data container**, not merely a saved graph.
2. **Cross-reference lists**: upload 100 names/companies/wallets and match against all enabled datasets.
3. **Dataset catalog** with country/category/update frequency/access level.
4. **Watchlists / saved pivots** that re-run as source datasets change.
5. OCR/document ingestion should feed the same entity graph as registries and web sources.

### Improvement over Aleph
Add active acquisition orchestration and evidence-chain controls to the investigative memory model.

---

## 4. Hunchly — strongest idea: automatic evidence preservation

### Useful ideas
- automatically capture visited pages;
- preserve URL, timestamp and content hash;
- full-page captures;
- organization/tagging/search;
- transparent audit trail;
- court/client-ready evidence packages.

### What to adopt — P0
Build an **Investigation Browser Recorder**:

```text
OPEN PAGE
  ↓
automatic metadata capture
  ↓
HTML + screenshot/PDF
  ↓
canonical URL + redirects
  ↓
timestamp UTC
  ↓
SHA-256
  ↓
case/source IDs
  ↓
journal event
```

Analyst should never need to remember to take screenshots manually.

### Critical design requirement
The browser recorder should support:
- auto capture ON/OFF per case;
- PII/access classification before sync;
- hash manifest;
- immutable original + derived parsed version.

This feature is one of the most important missing pieces in our current architecture.

---

## 5. Linkurious Enterprise — strongest idea: graph + operational case management

### Useful ideas
- graph-based case investigation;
- case assignment and status;
- comments and @mentions;
- unified case list;
- filters, layouts, grouping and geomode inside a case;
- export;
- automated alerts/queries which create investigation cases;
- No-Code Query Builder.

### What to adopt
Add a **Case Queue** independent of the graph:

```text
NEW → TRIAGE → INVESTIGATING → REVIEW → DECISION → CLOSED → REOPENED
```

Case fields:
- owner;
- reviewers;
- SLA/priority;
- comments/mentions;
- unread changes;
- evidence completeness;
- Red Team status;
- report readiness.

Add a **visual query builder** for analysts who do not write Cypher/SQL.

---

## 6. Siren Investigate — strongest idea: relational search before graph exploration

### Useful ideas
- global search across the entire data model;
- dynamic filters mapped across different entity types;
- search results in table form, then send selected records to graph;
- shortest-path queries;
- suspicious graph-pattern queries;
- graph grouping and metrics;
- proactive alerts.

### What to adopt
Do not force graph-first UX.

Provide three equivalent starting modes:
1. **Search/Table** — fastest for known facts.
2. **Graph** — best for relationships.
3. **Case/Dossier** — best for decision production.

Add:
- shortest path;
- common-neighbor search;
- N-hop bounded expansion;
- recurring motif/pattern matching;
- path explanations with source evidence.

---

## 7. OpenCTI — strongest idea: source-linked knowledge model

### Useful ideas
- knowledge graph as entities + typed relationships;
- STIX-based structured model;
- connectors;
- immutable observables distinct from indicators;
- first/last seen dates;
- confidence and attribution/source linkage;
- contextual view of entities within analyses/cases;
- content/deliverables attached to entities.

### What to adopt
Use OpenCTI-style discipline even outside cyber:

```text
ENTITY
RELATIONSHIP
OBSERVATION
CLAIM
SOURCE
REPORT
```

An address/phone/wallet is an observable object; an allegation is not.

Add connector lifecycle metadata:
- connector version;
- import timestamp;
- source freshness;
- ingestion batch;
- update/delete semantics.

### Improvement
Our model must support business/legal/logistics objects beyond STIX without forcing them into cyber semantics.

---

## 8. SpiderFoot — strongest idea: modular automated collection + correlation rules

### Useful ideas
- 200+ modular data-source integrations;
- configurable scan modules;
- built-in correlation engine/rules;
- API/CLI/web UI;
- exports;
- integration with other external tools;
- dark-web/Tor support in its collection model.

### What to adopt
Create **collection profiles** rather than always running every source:

```text
QUICK TRIAGE
COMPANY EDD
PERSON BACKGROUND
DOMAIN / INFRA
SANCTIONS
CRYPTO
LOGISTICS
FULL INVESTIGATION
```

Each profile selects transforms, budgets, timeouts and legal scopes.

Correlation rules should emit **leads**, not facts.

---

## 9. ShadowDragon Horizon — strongest idea: Identity → Investigate → Monitor lifecycle

### Useful ideas
- rapid identity triage;
- enrichment and correlation;
- network building/link analysis;
- recurring pattern detection;
- continuous monitoring of suspects/keywords/topics;
- historical context;
- API-first collection engine.

### What to adopt
Expose three obvious workflow buttons for every entity/case:

```text
IDENTIFY
INVESTIGATE
MONITOR
```

- IDENTIFY = resolve object and identifiers.
- INVESTIGATE = expand relations, evidence and hypotheses.
- MONITOR = scheduled source re-check / change detection.

This is clearer than exposing dozens of tools at once.

---

## 10. Babel Street — strongest idea: human-governed agentic research

### Useful ideas
- AI agents propose research plans;
- human controls the logic/outcome;
- citations and auditability;
- multilingual global sources;
- integrated translation;
- entity/identity resolution;
- centralized research and collaboration;
- secure anonymous browsing / location masking.

### What to adopt
### A. Research Plan mode
An agent should first output:

```yaml
objective:
known_facts:
unknowns:
search_hypotheses:
planned_sources:
expected_cost_time:
stop_conditions:
legal_constraints:
```

Only approved plans run expensive/active collectors.

### B. Secure research browser
Separate analyst identity from target-facing browsing where lawful and authorized:
- isolated profiles;
- no personal cookies/accounts;
- proxy/geolocation policy;
- fingerprint isolation;
- full audit log.

### C. Multilingual entity expansion
Automatic transliteration and local-language query generation should be default, not optional.

---

## 11. GraphSense — strongest idea: open-source crypto intelligence with data sovereignty

### Useful ideas
- self-hostable and open-source;
- Bitcoin + Ethereum + Tron and other chains;
- cross-currency search;
- transaction graph traversal;
- path finding;
- node/edge statistics;
- REST API;
- public/private TagPacks for wallet attribution;
- scalable backend.

### What to adopt — high priority
Use GraphSense concepts as the baseline for the crypto subsystem:

- address/cluster abstraction;
- path finder;
- TagPack registry;
- private analyst tags separate from public labels;
- provenance on every tag;
- cross-chain adapters;
- self-host option for sensitive cases.

A `TAG` must have:
```yaml
label:
entity_id:
chain:
address_or_cluster:
source:
confidence:
first_seen:
last_verified:
public_private:
analyst:
```

---

## 12. Chainalysis Reactor — strongest idea: automated interpretation of complex money movement

### Useful ideas
- unified cross-chain tracing;
- real-world counterparty attribution;
- automated interpretation of swaps/bridges/mixers/contracts;
- on-chain + off-chain context on the same graph;
- customizable annotations/layouts for court/briefing;
- escalation from risk alerts to investigations;
- collaboration ecosystem.

### What to adopt conceptually
Raw blockchain transactions are too low-level.

Introduce an **Economic Event Layer**:

```text
TX-001 + TX-002 + contract calls
       ↓ interpretation
BRIDGE BTC→ETH
SWAP USDT→USDC
DEPOSIT TO EXCHANGE
WITHDRAWAL FROM EXCHANGE
SWEEP
PEEL CHAIN
CONSOLIDATION
OTC-LIKE SETTLEMENT PATTERN
```

Each interpreted event must show:
- underlying transactions;
- interpretation rule/model;
- confidence;
- alternative explanations.

This will dramatically improve readability for non-crypto investigators.

---

## 13. Feature harvest — what should be added to our architecture

### P0 — before expanding source count
1. Hunchly-style automatic browser evidence capture.
2. Maltego-style transform SDK + internal transform registry.
3. Aleph-style investigation workspace + bulk cross-reference lists.
4. Linkurious-style case lifecycle, assignment, comments and review.
5. Siren-style Search/Table/Graph interchangeable views.
6. Saved watchlists and recurring alerts.
7. Source/dataset catalog with update frequency and access class.

### P1 — major differentiators
8. Identity → Investigate → Monitor modes.
9. Agent-generated research plan with human approval.
10. Secure isolated research browser profiles.
11. Multilingual/local-language query generator.
12. Pattern library / graph motif detection.
13. Economic Event Layer for blockchain.
14. Public/private TagPack model for crypto attribution.
15. Shortest-path/common-neighbor/why-path tools.

### P2 — scale and collaboration
16. Dataset-to-dataset bulk cross-reference jobs.
17. Investigation alerts generated from scheduled graph queries.
18. Collaborative review/mentions.
19. Connector/source health and freshness dashboards.
20. Integration SDK for external specialist products.

---

## 14. Proposed UX after competitor review

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ CASE | IDENTIFY | INVESTIGATE | MONITOR | REPORT | evidence readiness       │
├─────────────────┬──────────────────────────────────┬─────────────────────────┤
│ GLOBAL SEARCH   │                                  │ ENTITY DOSSIER          │
│ results/table   │          GRAPH / MAP             │ facts / claims          │
│ filters         │          / TIMELINE              │ sources / contradictions│
│ source packs    │                                  │ hypotheses / risk       │
├─────────────────┴──────────────────────────────────┴─────────────────────────┤
│ PIVOTS | TRANSFORMS | JOBS | JOURNAL | CAPTURE | ALERTS | REVIEW            │
└──────────────────────────────────────────────────────────────────────────────┘
```

Every entity offers:
- identify more;
- run transforms;
- find paths;
- compare/merge;
- add to watchlist;
- open source evidence;
- explain relation;
- Red Team challenge.

---

## 15. Differentiator we should protect

Competitors are individually stronger than us today in specific domains. The product should not attempt to beat each at their specialty by copying every feature.

Our defensible combination should be:

### `Evidence-first agentic investigation`

1. AI plans the search.
2. Collectors acquire evidence.
3. Browser automatically preserves it.
4. Entity engine resolves people/organizations/accounts.
5. Graph connects evidence-backed relationships.
6. Hypothesis board separates versions from facts.
7. Red Team attacks conclusions.
8. Every finding is traceable to immutable source captures.
9. Report composer converts approved findings into formal decision products.
10. GitHub/search journal preserves the entire investigative process.

This is the part that should remain central even if specialized products are integrated later rather than rebuilt.
