# OSINT Acquisition Workbench — architecture and operating model

> Status: REQUIREMENT / ARCHITECTURE DRAFT  
> Scope: convenience, effectiveness, visual analysis, evidence acquisition, case production  
> Constraint: DEV v1 frozen baseline remains unchanged. This document defines the target architecture only.

## 1. Goal

Build an analyst workbench that turns OSINT from a sequence of manual searches into a governed production process:

```text
TASK
  ↓
ENTITY RESOLUTION
  ↓
COLLECTION PLAN
  ↓
MULTI-SOURCE ACQUISITION
  ↓
NORMALIZATION + PROVENANCE
  ↓
RELATIONSHIP GRAPH
  ↓
CLAIMS / FACTS / HYPOTHESES
  ↓
RED TEAM
  ↓
FORMAL REPORT
  ↓
DECISION + AUDIT TRAIL
```

The system must be useful even when no pre-collected database contains the answer. Pre-built datasets accelerate discovery, but the core value is orchestration, evidence control, entity resolution and repeatable investigative workflows.

## 2. What is needed besides pre-collected databases

### 2.1 Source registry
A living catalog of sources and collection methods, not just saved data.

Each source record contains:
- jurisdiction;
- source family;
- official / commercial / media / archive / community;
- access method: browser, API, downloadable file, manual query, connector;
- required parameters;
- rate limits;
- legal/access constraints;
- freshness model;
- parser/normalizer;
- reliability defaults;
- known blind spots;
- fallback sources.

Example families:
- company registries;
- sanctions / PEP / enforcement;
- court / bankruptcy / enforcement proceedings;
- procurement / tenders / contracts;
- domain / DNS / certificate / WHOIS/RDAP;
- archive/history;
- social/media/public profiles;
- maps / geospatial / property;
- logistics / customs / shipping / rail / port sources;
- blockchain explorers;
- technical metadata;
- press / investigations;
- official publications.

### 2.2 Query planner
The analyst should not manually remember every place to search.

Input:
```yaml
entity_type: ORGANIZATION
country: BY
seed:
  name: "TECHNOSPETSTRADINGEXPORT LLC"
  registration_id: "193648909"
  address: "Minsk, Naklonnaya 28"
```

Planner generates pivots:
```text
name variants
registration number
address cluster
phones
emails
domains
directors
shareholders
beneficial owners
procurements
court cases
sanctions
historical names
related legal entities
foreign transliterations
logistics and trade references
```

Every generated query becomes a journal event with status `FOUND / NO-HIT / BLOCKED / CONFLICT`.

### 2.3 Entity-resolution engine
The system must continuously answer: "is this the same person/company/address?"

Inputs:
- exact identifiers;
- names and aliases;
- transliteration;
- DOB/incorporation date;
- addresses;
- phones/emails;
- directors/shareholders;
- websites/domains;
- photos;
- temporal overlap;
- business sector;
- source quality.

Output:
```yaml
entity_match:
  candidate_a: PERSON-001
  candidate_b: PERSON-014
  confidence: 0.84
  status: HYPOTHESIS
  supporting_features: [...]
  contradicting_features: [...]
  missing_decisive_evidence: [...]
```

No silent merging.

### 2.4 Acquisition orchestrator
A queue-based collector that can run many independent acquisition jobs and report progress.

Job states:
```text
PLANNED → RUNNING → FOUND / NO-HIT / BLOCKED / ERROR → REVIEWED
```

The orchestrator needs:
- retry policy;
- timeout;
- throttling;
- source-specific rate limit;
- browser/API/manual execution modes;
- per-case authorization scope;
- full run manifest;
- raw output retention;
- parser version;
- checksum.

### 2.5 Browser-assisted collection
Many important sources are not friendly APIs.

Needed capabilities:
- controlled browser session;
- save HTML/PDF/screenshot;
- capture canonical URL;
- timestamp;
- page title/publisher;
- extract links/tables;
- archive page snapshot;
- compare historical versions;
- human confirmation for ambiguous forms / captchas / legal acknowledgements.

### 2.6 Document extraction pipeline
Documents are often more valuable than webpages.

Pipeline:
```text
PDF/DOC/XLS/IMAGE
  ↓
metadata
  ↓
text/table extraction
  ↓
entity detection
  ↓
claims
  ↓
references / signatures / dates
  ↓
source graph
```

Special extraction objects:
- names and positions;
- signatures;
- dates;
- contract numbers;
- amounts;
- bank details;
- addresses;
- phone/email;
- registry IDs;
- cited documents;
- annexes;
- counterparties.

### 2.7 Relationship graph
The graph is the analyst's main working memory.

Node types:
`PERSON, ORGANIZATION, ADDRESS, DOMAIN, PHONE, EMAIL, DOCUMENT, CONTRACT, CASE, ASSET, WALLET, TRANSACTION, EVENT, SOURCE, CLAIM, RISK`

Edge types:
`OWNS, CONTROLS, DIRECTS, REPRESENTS, EMPLOYED_BY, RELATED_TO, LOCATED_AT, USES_PHONE, USES_EMAIL, OWNS_DOMAIN, CONTRACTED_WITH, PAID, SUPPLIED, SHIPPED_TO, MENTIONED_IN, SANCTIONED_BY, ALLEGED_BY, CONFIRMED_BY`

Every edge must have:
- source IDs;
- first/last observed date;
- confidence;
- relation status: FACT / SOURCE_CLAIM / INFERENCE / HYPOTHESIS;
- analyst note.

### 2.8 Timeline engine
Dates must be first-class objects.

Differentiate:
- event date;
- effective date;
- publication date;
- collection date;
- validity period.

Timeline use cases:
- ownership changes;
- sanctions;
- director changes;
- address changes;
- shipments;
- court events;
- domain changes;
- wallet flows;
- media mentions.

### 2.9 Geospatial layer
Addresses, facilities, routes and logistics must be visually connected.

Functions:
- address normalization;
- geocoding confidence;
- street/satellite imagery references;
- historical map snapshots;
- route reconstruction;
- port/rail/customs nodes;
- facility comparison;
- proximity relationships.

### 2.10 Blockchain intelligence adapter layer
A wallet is not a person.

Needed objects:
- chain;
- address;
- token;
- transaction;
- counterparty;
- service label;
- cluster hypothesis;
- funding source;
- sweep destination;
- first/last seen;
- velocity;
- amount distribution;
- recurrence;
- exchange/bridge/mixer/merchant tags;
- off-chain references.

Attribution pipeline:
```text
wallet
  ↓
transaction pattern
  ↓
first-hop counterparties
  ↓
repeated counterparties
  ↓
service tags / public references
  ↓
possible controller / economic beneficiary
```

### 2.11 Contradiction register
The system must make contradictions visible instead of hiding them.

Example:
```yaml
claim: "company manufactures fertilizer"
source_a: corporate website
source_b: investigative report
conflict: "independent full-cycle production not demonstrated"
status: OPEN
required_evidence:
  - production site
  - equipment ownership/lease
  - raw-material contracts
  - output records
```

### 2.12 Hypothesis board
Analysts need a place for versions without contaminating facts.

Each hypothesis:
- proposition;
- why it matters;
- supporting evidence;
- contradicting evidence;
- confidence;
- test plan;
- status: OPEN / WEAKENED / CONFIRMED / REJECTED.

### 2.13 Red Team engine
Every material conclusion should be challenged.

Questions:
- Could this be a namesake?
- Could the address be shared?
- Is the source reporting a claim rather than a fact?
- Is temporal order inconsistent?
- Could a platform technically own an account used by a customer?
- Could a commercial intermediary have a legitimate role?
- Are we converting proximity into causality?
- Are we treating nationality/ethnicity as evidence of affiliation? (prohibited inference)

### 2.14 Evidence vault
Raw evidence and analyst outputs must be separated.

Storage classes:
```text
PUBLIC_REFERENCE
PUBLIC_CAPTURE
INTERNAL_WORKING
RESTRICTED_EVIDENCE
PUBLIC_REDACTED_EXPORT
```

Every captured artifact needs:
- source ID;
- original URL;
- acquisition timestamp;
- content hash;
- MIME type;
- collector/job ID;
- access class;
- parser version;
- retention rule.

### 2.15 Search journal
Mandatory append-only case log.

Fields:
```yaml
journal_id:
timestamp_utc:
analyst_or_agent:
case_id:
query_or_action:
source:
result_code:
result_summary:
new_entities:
new_relations:
new_claims:
confidence_change:
next_pivot:
```

GitHub is the versioned journal for the current project; restricted evidence itself must not be blindly published there.

### 2.16 Task dashboard
The analyst must see production state, not just documents.

Dashboard widgets:
- open cases;
- active collectors;
- failed sources;
- unresolved entities;
- contradictions;
- high-impact hypotheses;
- unverified high-risk claims;
- source freshness;
- evidence coverage by finding;
- report readiness;
- Red Team status.

### 2.17 Coverage meter
For every conclusion show evidence coverage.

Example:
```text
Finding: UBO is PERSON-001
Official registry      ✅
Government decision    ✅
Corporate source       ✅
Independent source     ⚠️
Contradicting evidence ❌ none found
Coverage: STRONG
```

This is more useful than a cosmetic "confidence 87%" without explanation.

### 2.18 Report composer
Formal report is generated from structured findings, not copied from analyst notes.

Sections:
- task;
- object resolution;
- established facts;
- related persons/entities;
- activity/business model;
- risk matrix;
- contradictions;
- unresolved questions;
- recommendations;
- annex links;
- source registry.

Every paragraph should be traceable to `finding_id` and `source_id`.

## 3. Five analytical streams inside the platform

### Stream A — Entity / registry
Who is the object? Who owns/controls/manages it?

### Stream B — Transactions / business / logistics
How does money/product/service actually move?

### Stream C — Digital footprint / infrastructure
Domains, emails, phones, social/public web, archives, technical infrastructure.

### Stream D — Legal / sanctions / adverse information
Courts, enforcement, bankruptcy, sanctions, PEP, regulator notices, credible investigations.

### Stream E — Red Team / source quality
Disprove, detect duplicates, source bias, conflicts, overclaiming.

A case can run these streams in parallel, but the platform must preserve one shared graph and one journal.

## 4. Analyst UX

### 4.1 Three synchronized panes
```text
LEFT: entities / filters / saved views
CENTER: graph / map / timeline
RIGHT: dossier / evidence / claims / risks
BOTTOM: journal / jobs / tools / source queue
```

### 4.2 One-click pivots
From any node:
- Search related companies
- Search sanctions
- Search court cases
- Search procurement
- Search addresses
- Search phones/emails
- Search web archives
- Search domains
- Search blockchain
- Search media
- Compare identities
- Open Red Team challenge

### 4.3 “Why do I see this?”
Every node/edge/finding has a button showing:
```text
SOURCE → EXTRACTED CLAIM → NORMALIZED FACT → RELATION → FINDING → RISK → RECOMMENDATION
```

## 5. Productivity features

- reusable case templates;
- saved query recipes;
- country-specific source packs;
- automatic transliteration variants;
- deduplication;
- entity aliases;
- scheduled re-checks;
- change detection;
- source health monitoring;
- bulk URL capture;
- one-click evidence bundle;
- report diff between versions;
- finding-level comments/review;
- analyst handoff without loss of context;
- keyboard-first navigation;
- quick tags and bookmarks;
- "promote to fact" only after evidence gate.

## 6. Data architecture

Recommended split:

```text
PostgreSQL
  - canonical entities
  - cases
  - claims/findings
  - source metadata
  - journal
  - permissions

Graph database / graph layer
  - relationships
  - paths
  - temporal edges

Search index
  - full text
  - fuzzy name matching
  - documents

Object store
  - captures
  - PDFs
  - screenshots
  - raw tool outputs

Vector index
  - semantic document retrieval
  - not authoritative identity resolution
```

## 7. Agents

Agents should be specialized and constrained:

- Collector Agent — collects and preserves source material.
- Entity Resolver — proposes merges/splits.
- Business Analyst — reconstructs business model.
- Financial/Transaction Analyst — analyzes flows.
- Legal/Sanctions Analyst — evaluates legal context.
- Media/OSINT Analyst — expands public footprint.
- Red Team Analyst — attacks conclusions.
- Report Analyst — composes formal output from approved findings.

Agents may propose; material conclusions require evidence gates.

## 8. Decision gates

### Gate 1 — Object resolved
No deep investigation until entity identity is sufficiently stable.

### Gate 2 — Minimum source coverage
At least one primary or two independent strong sources for high-impact findings.

### Gate 3 — Contradictions reviewed
No unresolved material contradiction hidden from report.

### Gate 4 — Red Team complete
Every high-impact finding challenged.

### Gate 5 — Formal report ready
All findings trace to source IDs and annexes.

## 9. MVP sequence

### MVP-1 — Case + source + journal + graph
- case card;
- source registry;
- append-only journal;
- entity graph;
- manual finding creation;
- source-to-finding traceability.

### MVP-2 — Assisted acquisition
- query planner;
- browser capture;
- registry adapters;
- document extraction;
- entity-resolution suggestions.

### MVP-3 — Analyst workstation
- graph + dossier drawer;
- map;
- timeline;
- contradiction board;
- Red Team workflow;
- formal report composer.

### MVP-4 — Advanced acquisition
- blockchain adapters;
- logistics/trade adapters;
- monitoring/change detection;
- scheduled re-checks;
- multi-agent orchestration.

## 10. Success metrics

Measure:
- time from task to first resolved entity;
- sources checked per hour;
- percentage of automated captures;
- deduplication rate;
- unresolved entity count;
- high-impact findings with primary evidence;
- contradiction closure rate;
- analyst rework rate;
- report production time;
- percentage of report statements with direct traceability;
- source failure rate;
- false entity merge rate.

Do not use "number of pages collected" as a primary productivity metric.

## 11. Core principle

The system is not a search engine with a prettier interface.

Its value is:

```text
DISCOVER → VERIFY → LINK → CHALLENGE → EXPLAIN → PROVE → REPORT
```

Pre-collected databases answer known questions quickly. The workbench must make it efficient to discover unknown relationships, preserve evidence, explain why a conclusion was made, and safely turn exploratory OSINT into a formal decision product.
