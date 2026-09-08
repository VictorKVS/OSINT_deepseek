# M4 — FATHER Unified Analyst Core

Status: ACTIVE INTEGRATION PLAN
Execution branch: `codex/father-unified-analyst-m4`

## 1. Product goal

Create one local-first analytical system that can:

1. accept a Case and Research Questions;
2. plan collection across several investigative directions;
3. route typed inputs to a governed zoo of tools;
4. preserve raw results and normalize them to observations;
5. promote selected observations to reviewed evidence;
6. build entity/relation candidate graphs;
7. run independent analytical perspectives;
8. maintain primary and alternative hypotheses with support/counter-evidence;
9. challenge them through Socrates and human review;
10. send only reviewed, version-bound objects to Knowledge Factory D14/D15;
11. retrieve compact role-specific knowledge locally to minimize LLM tokens.

## 2. The system we are building

```text
CASE / RQ
   |
   v
COLLECTION PLANNER
   |
   +--> Identity / Registry --------+
   +--> Business / Financial -------+
   +--> Digital Footprint ----------+--> TOOL FACTORY / WORKERS
   +--> Legal / Sanctions ----------+
   +--> Red Team / Source Quality --+
                                      |
                                      v
                              RAW ARTIFACT VAULT
                                      |
                                      v
                                OBSERVATIONS
                                      |
                                      v
                                EVIDENCE LAYER
                                      |
                        +-------------+-------------+
                        |                           |
                        v                           v
                 ENTITY GRAPH               ANALYSIS ZOO
                        |                           |
                        +-------------+-------------+
                                      v
                               REASONING GRAPH
                          HYP <-> ALT-HYP
                     support / counter / gap / test
                                      |
                                      v
                                  SOCRATES
                                      |
                                      v
                                HUMAN REVIEW
                                      |
                                      v
                              PROMOTION REQUEST
                                      |
                                      v
                             KNOWLEDGE FACTORY
                                D14 -> D15
                                      |
                                      v
                               KNOWLEDGE BASE
```

## 3. Donor subsystem map

| Donor | What is already valuable | M4 action |
|---|---|---|
| PR #22 Passive OSINT Workbench | evidence vault, provenance, candidate graph, analysis zoo, gaps, reporting | extract contracts/patterns behind compatibility tests |
| PR #23 Core OSINT MVP | evidence-first vertical, analyzer consensus/dissent, human finding gate | reuse semantics; avoid duplicate storage model |
| PR #31 Screening Factory | five streams, bounded parallelism, adapter/policy registry, honest BLOCKED states | use as Tool Factory scheduling donor |
| PR #26 Bitcoin | evidence-safe BTC flow parsing and provenance contamination guards | wrap as CRYPTO adapter family |
| Telegram existing paths | TDLib/Telethon transport and collection | wrap as TELEGRAM adapters |
| PR #32 D14/D15 repair | fail-closed review/promotion binding | use as mandatory Knowledge bridge target |
| PR #33 Graph Core | Case shell, reasoning ontology, graph-first product model | use as M4 base |
| PR #11 Knowledge Factory | D0-D15 conveyor, exact acquisition, structure/chunks, KB-ready contracts | preserve as downstream knowledge engine |

No subsystem above is declared merged/canonical merely because the PR exists. Codex must prove compatibility before integration.

## 4. Canonical object taxonomy

### Investigation control
- CASE
- RESEARCH_QUESTION
- COLLECTION_PLAN
- TOOL_JOB
- TOOL_RUN

### Acquisition/evidence
- RAW_ARTIFACT
- SOURCE_OBSERVATION
- OBSERVATION
- FINDING
- EVIDENCE
- SOURCE

### Entity analysis
- ENTITY
- RELATION_CANDIDATE
- RELATION
- EVENT

### Reasoning
- CLAIM
- FACT
- HYPOTHESIS
- ALTERNATIVE_HYPOTHESIS
- GAP
- TEST
- TEST_RESULT
- CONFLICT
- ANALYST_OPINION
- REVIEW_DECISION
- CONCLUSION

### Knowledge promotion
- PROMOTION_REQUEST
- D14_REVIEW_RESULT
- D15_MANIFEST
- KNOWLEDGE_OBJECT

## 5. Tool Factory model

The key reusable function is:

`INPUT TYPE -> ELIGIBLE TOOLS -> TOOL RUN -> OUTPUT TYPES -> POSSIBLE EDGE CANDIDATES`

Examples:

| Input | Tools | Normalized output | Candidate edges |
|---|---|---|---|
| DOMAIN | Subfinder, RDAP/DNS, theHarvester, Censys/Shodan | SUBDOMAIN, IP, ASN, CERT, EMAIL, SERVICE | RESOLVES_TO, ANNOUNCED_BY, USES_CERT, MENTIONED_EMAIL |
| EMAIL | Holehe, Maigret where applicable, public-search adapters | ACCOUNT, DOMAIN, PROFILE | REGISTERED_AT?, USES_ACCOUNT? — candidate only |
| USERNAME | Sherlock, Maigret | ACCOUNT, PROFILE_URL, ALIAS | HAS_PROFILE?, ALIAS_OF? |
| PHONE | PhoneInfoga/public registry adapters | COUNTRY, CARRIER, ACCOUNT_LEAD | ASSOCIATED_WITH? |
| MEDIA | ExifTool | TIME, GEO, DEVICE, SOFTWARE | CAPTURED_AT?, CREATED_BY_DEVICE? |
| IP | RDAP, Shodan, Censys | ASN, ORG, SERVICE, CERT | ANNOUNCED_BY, EXPOSES_SERVICE |
| WALLET | Bitcoin adapter | TX, WALLET, LABEL/SERVICE | SENT_TO, RECEIVED_FROM, LABEL_CANDIDATE |
| TELEGRAM ACCOUNT/CHANNEL | Telegram adapters | MESSAGE, URL, ACCOUNT, CHANNEL, TIME | POSTED, FORWARDED_FROM, MENTIONS |

Question marks are intentional: many relations are hypotheses/candidates rather than established facts.

## 6. Parallel execution

Five collection streams are scheduling lanes, not five permanent LLM agents.

Workers should be local deterministic processes/containers where possible. LLM use is reserved for tasks that require semantic interpretation.

Suggested execution profiles:
- WINDOWS_NATIVE
- WSL2_KALI
- PYTHON_ISOLATED
- CONTAINER_ISOLATED
- API_REMOTE_READONLY
- MANUAL_EXTERNAL

Parallelism classes:
- CPU_LOCAL
- IO_LOCAL
- NETWORK_PASSIVE
- RATE_LIMITED_API
- GUI_MANUAL

The scheduler must respect per-tool rate limits and case policy rather than equating thread count with usable throughput.

## 7. Local knowledge library / token minimization

Target flow:

`task -> role -> local retrieval -> compact evidence/knowledge packet -> LLM`

The local knowledge layer must support:
- role profile
- topic/domain tags
- source trust/status
- document version
- exact locator/page/chunk
- compact excerpt budget
- deduplicated semantic retrieval
- cache keyed by task/evidence/version
- citation IDs instead of repeated raw text

Initial roles:
- Collector
- Source Analyst
- Entity Analyst
- Main Analyst
- Socrates / Critic
- Knowledge Engineer
- Security/Legal Reviewer

The raw book/document corpus stays local. Only selected chunks should be sent to an external model.

## 8. Milestones and gates

### M4.0 — Contract convergence
Exit:
- one ID namespace policy
- canonical taxonomy frozen
- adapter schema frozen
- observation/evidence schema frozen
- graph edge status model frozen
- AnalysisPacket schema frozen
- ReviewDecision + PromotionRequest frozen

### M4.1 — Tool Factory
Exit:
- registry loader
- tool capability matching
- five-stream bounded scheduler
- health/status states
- synthetic adapters
- deterministic run manifests

### M4.2 — Evidence Layer
Exit:
- raw artifact persistence
- SHA-256/content identity
- observation provenance
- source independence grouping
- observation -> evidence review transition
- no tool -> fact route

### M4.3 — Unified Graph
Exit:
- Entity Graph persisted
- Reasoning Graph persisted
- candidate vs supported relation distinction
- evidence-backed edges
- append-only history
- graph/table/timeline projections reconcile

### M4.4 — Analysis Zoo
Exit:
- at least three independent analyzer families
- deterministic checks run before semantic LLM checks
- consensus/dissent retained
- failure isolation
- bounded local context packets

### M4.5 — Socrates and Human Review
Exit:
- dependency/circularity detection
- counter-evidence review
- alternative explanation requirement
- identification conflict checks
- PASS / REWORK / INCONCLUSIVE
- immutable decision record

### M4.6 — D14/D15 bridge
Exit:
- reviewed object -> version-bound promotion request
- exact evidence/review hashes bound to request
- D14 result integrity verified
- D15 fail-closed
- no bypass to KB

### M4.7 — First real adapters
Order:
1. RDAP/DNS
2. Subfinder
3. theHarvester
4. Sherlock/Maigret
5. ExifTool
6. Telegram
7. Bitcoin
8. Shodan/Censys if credentials are available

### M4.8 — Controlled vertical
Synthetic first; controlled real case second.

Required synthetic acceptance:
- 1 Case
- >=3 competing hypotheses
- 5 scheduling streams
- >=5 tool adapters
- support + counter-evidence
- source-dependency warning
- one rejected relation candidate
- one unresolved GAP
- one discriminating TEST
- Socrates challenge
- Human Review
- one promoted object reaches D15/KB
- complete replay to raw artifact

## 9. What is NOT part of the first integrated milestone

- unrestricted Kali shell
- active scanning outside separately authorized security-assessment cases
- automatic attribution of person/account/wallet ownership
- autonomous FACT creation
- autonomous D14/D15 approval
- hundreds of adapters
- numeric truth/confidence scores without calibration
- sending entire raw case/library to cloud LLMs

## 10. Codex first task queue

1. Inventory existing donor package APIs and schemas.
2. Produce `DONOR_COMPATIBILITY_MATRIX.md` with KEEP / WRAP / MIGRATE / RETIRE / CONFLICT.
3. Add canonical M4 schemas without changing runtime behavior.
4. Add compatibility tests against donor semantics.
5. Implement unified Tool Registry and synthetic Tool Factory.
6. Implement a synthetic end-to-end Case through Observation/Evidence/Graph.
7. Attach Analysis Zoo.
8. Attach Reasoning Graph.
9. Attach Socrates/Human Gate.
10. Attach D14/D15 bridge.
11. Only then connect real tools.

## 11. Completion rule

M4 is not complete because files/classes exist. Completion requires reproducible test/run evidence for the full vertical and provenance replay.
