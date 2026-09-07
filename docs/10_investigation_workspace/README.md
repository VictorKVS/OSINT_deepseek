# FATHER OSINT Investigation Workspace

Status: DESIGN BASELINE v1  
Branch: `agent/investigation-workspace-v1`  
Goal: turn the existing OSINT Control Center into a case-centric investigator workstation.

## 1. What we are building

The product is not a collection of unrelated OSINT scripts. It is one investigation workspace where every action is attached to a case and every finding keeps provenance.

Core chain:

`CASE -> QUESTIONS -> HYPOTHESES -> COLLECTION PLAN -> TOOL RUNS -> RAW FINDINGS -> EVIDENCE -> ENTITIES/RELATIONS -> HYPOTHESIS TESTS -> CONCLUSIONS -> REPORT`

The existing Control Center remains the operational engine for searches, downloads, jobs, streams, trace events and role libraries. Investigation Workspace becomes the analyst layer above it.

## 2. Primary analyst objects

### Case
A bounded investigation with title, purpose, scope, legal/safety constraints, owners, dates and status.

### Question
A concrete question that the investigation must answer. Questions prevent open-ended collection.

### Hypothesis
A falsifiable explanation or working theory. Each hypothesis stores support, counter-evidence, unresolved gaps and confidence rationale. Confidence is never inferred only from the number of matching records.

### Entity
A person, organization, account, address, domain, IP, wallet, transaction, repository, document, location, phone, email, device or other investigation object.

### Relation
A typed link between entities. Every relation must point to the evidence that supports it.

### Finding
Raw output from a tool. A finding is not automatically a fact.

### Evidence
A reviewed finding with provenance, acquisition metadata, source identity, hash where applicable, analyst status and relevance to a question/hypothesis.

### Claim
An explicit statement supported, contradicted or left unresolved by evidence.

### Timeline event
A dated/ordered event with evidence references and certainty status.

### Conclusion
An analyst judgement that cites claims/evidence and records alternative explanations and remaining gaps.

## 3. Investigation modes

1. PERSON / IDENTITY
2. COMPANY / ORGANIZATION
3. DOMAIN / INFRASTRUCTURE
4. TELEGRAM / SOCIAL
5. CRYPTO / BLOCKCHAIN
6. DOCUMENT / REGULATORY
7. MEDIA / NARRATIVE
8. GEO / LOCATION
9. INCIDENT / CAMPAIGN
10. CUSTOM

A case may combine several modes.

## 4. Tool families

Tools are adapters. They do not own the investigation state.

### Connected or already represented in the repository
- Telegram acquisition/search: TDLib / Telethon paths already present in the project.
- Web/control-center search and acquisition orchestration.
- GitHub/code investigation paths.
- Local files and Knowledge Factory.
- Evidence hashing, trace events, download receipts and provenance.
- Bitcoin/TRON investigation artifacts already present in project history.

### Next adapters
- Web search / official sources / archived pages.
- DNS / WHOIS / RDAP / TLS / certificate transparency.
- URL/domain reputation and passive infrastructure observations.
- Email / username / account pivots where legally permitted.
- Image metadata and reverse-image workflow.
- Map/geolocation workspace.
- Bitcoin and TRON explorer adapters normalized to one crypto evidence model.
- Media/Narrative Drift analyzer for text, image, audio and video evidence.

### Optional external-tool adapters later
- Maltego-style graph import/export.
- SpiderFoot-style automated collection profiles.
- Amass/Subfinder-style domain discovery.
- Shodan/Censys-style service intelligence where credentials and policy permit.
- ExifTool and other local metadata utilities.

The UI must expose availability and trust state per adapter: `READY`, `NEEDS_CONFIG`, `OFFLINE`, `BLOCKED_BY_POLICY`, `EXPERIMENTAL`.

## 5. Main screen layout

```text
+--------------------------------------------------------------------------------+
| FATHER | Case: CASE-2026-001 | Scope | Status | Search | Run tools | Export    |
+----------------------+--------------------------------------+------------------+
| CASE NAV             | INVESTIGATION CANVAS                 | INSPECTOR        |
|                      |                                      |                  |
| Overview             |  [Entity]----[Relation]----[Entity] | selected object  |
| Questions            |       \          |                 | attributes       |
| Hypotheses           |      [Evidence]---+                 | evidence refs    |
| Entities             |                                      | source quality   |
| Evidence             |  switch: Graph / Table / Timeline   | analyst notes    |
| Timeline             |                                      | actions          |
| Sources              |                                      |                  |
| Tools                |                                      |                  |
| Tasks                |                                      |                  |
| Report               |                                      |                  |
+----------------------+--------------------------------------+------------------+
| TRACE / CHAIN OF CUSTODY: actor -> action -> source -> finding -> evidence ... |
+--------------------------------------------------------------------------------+
```

Desktop is the primary mode. Graph and table are equal first-class projections of the same objects. Day/night themes remain supported.

## 6. Screens

### A. Case Dashboard
Shows scope, questions, hypotheses, latest evidence, gaps, active jobs, milestones and recent changes.

### B. Graph Workspace
Color-coded entities and evidence nodes, typed edges, clustering, filters, expand/collapse, pinned paths and evidence-backed edge inspection.

### C. Evidence Table
High-density analyst table: evidence ID, source, acquired time, entity, claim, support/contradict status, quality dimensions, hash, analyst state and tags.

### D. Timeline
Events ordered by event time and acquisition time separately. Unknown dates remain unknown; the system must not invent chronology.

### E. Tool Drawer
Tool catalogue grouped by family. Analyst selects a tool, input/pivot, target question, expected output, limits and destination. Every run becomes a traceable job.

### F. Hypothesis Board
For each hypothesis: supporting evidence, counter-evidence, alternatives, missing checks, confidence rationale and next best collection action.

### G. Report Builder
Builds an investigation report from selected reviewed evidence and conclusions. Facts, claims, interpretations and hypotheses are rendered separately.

## 7. Evidence states

`RAW -> TRIAGED -> REVIEWED -> ACCEPTED_EVIDENCE`

Additional terminal/exception states:

`REJECTED`, `DUPLICATE`, `OUT_OF_SCOPE`, `UNVERIFIED_SOURCE`, `CONTRADICTED`, `SUPERSEDED`.

No tool is allowed to promote raw collection directly into a final conclusion.

## 8. Source/evidence quality dimensions

Keep dimensions separate instead of one magic score:

- source identity / authority
- directness: primary vs retelling
- provenance completeness
- integrity/hash availability
- temporal relevance
- independence from other evidence
- consistency with other evidence
- known conflicts / counter-evidence
- analyst review status

## 9. Mandatory traceability

Every investigation action stores:

- case_id
- question_id / hypothesis_id when relevant
- actor / role
- tool_id and tool version/profile
- command/run id
- inputs/pivots
- source locator
- acquisition timestamp
- raw artifact reference
- SHA-256 where applicable
- parser/normalizer version
- finding/evidence IDs created
- analyst decisions
- links to downstream claims/conclusions

## 10. Build sequence

### Phase 0 — Product baseline
- [x] Define case-centric model.
- [x] Define target screens.
- [x] Define tool-adapter principle.
- [ ] Freeze v1 JSON schemas.

### Phase 1 — Case shell
- [ ] Case list / create / open / archive.
- [ ] Case dashboard.
- [ ] Persistent case registry.
- [ ] Question and hypothesis CRUD.

### Phase 2 — Evidence workspace
- [ ] Finding/evidence registry.
- [ ] Entity and relation registry.
- [ ] Graph/Table/Timeline projections.
- [ ] Evidence inspector and provenance panel.

### Phase 3 — Tool router
- [ ] Tool registry with capabilities and health.
- [ ] Run tool against selected case/question/entity.
- [ ] Normalize results into findings.
- [ ] Preserve raw output and receipts.

### Phase 4 — Existing integrations
- [ ] Attach Telegram search/download to case.
- [ ] Attach Local KB / documents.
- [ ] Attach GitHub/code pivots.
- [ ] Attach Bitcoin/TRON flows.

### Phase 5 — Analyst layer
- [ ] Hypothesis support/counter-evidence matrix.
- [ ] Research gaps and next-best-action queue.
- [ ] Main Analyst / critic workflow.
- [ ] Narrative Drift module.

### Phase 6 — Reporting
- [ ] Investigation report builder.
- [ ] Evidence appendix.
- [ ] Machine-readable export.
- [ ] Redaction profiles.

### Phase 7 — Hardening
- [ ] RBAC.
- [ ] policy/legality gates.
- [ ] audit integrity.
- [ ] encrypted sensitive local stores where required.
- [ ] backup/recovery/export tests.

## 11. v1 acceptance gate

The first usable Investigator Workspace is accepted when an analyst can:

1. create a case;
2. add a question and hypothesis;
3. launch at least Telegram + one non-Telegram collection tool from the case;
4. receive normalized findings with provenance;
5. promote selected findings to reviewed evidence;
6. connect two entities with an evidence-backed relation;
7. view the same case as graph, table and timeline;
8. record support and counter-evidence for a hypothesis;
9. generate a report with traceable citations/evidence references;
10. reproduce the action chain from the audit log.

## 12. Current architectural decision

Do not build separate mini-sites for every source. Build one Case Workspace and attach source/tool adapters behind a common Tool Router. Existing Control Center screens become operational subviews inside this workspace.
