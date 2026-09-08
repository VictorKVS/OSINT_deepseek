# FATHER Engineering Memory Storage Model v0.1

Status: **DESIGN BASELINE / STORAGE ENGINE NOT YET SELECTED**  
Date: **2026-08-15**

## 1. Purpose

The long-form analytics accumulated by Analyst, Tester, Programmer, Security, Critic and experiments is not merely documentation and must not be collapsed directly into PROGRAMMING_KB.

It is **project engineering memory**: the auditable history of how a concrete project was understood, designed, measured, implemented, tested, compared and improved.

Knowledge bases consume validated/distilled results from this memory; they are not the primary store for every project observation.

Core separation:

```text
PROJECT WORK
  ↓
ENGINEERING MEMORY / PROJECT DOSSIER
  ↓
VERIFIED EXPERIENCE
  ↓
KNOWLEDGE GATE
  ↓
PROGRAMMING_KB / ARCHITECTURE_KB / SECURITY_KB / shared ENGINEERING knowledge
```

## 2. Storage layers

### Layer A — Canonical project record

Source of truth for the structured engineering dossier.

During MVP this should be version-controlled text records with stable IDs, not prose-only Markdown.

Preferred record formats:
- YAML/JSON for canonical machine-readable objects;
- Markdown generated as human-readable views;
- small Mermaid/PlantUML/text diagrams where suitable;
- links/hashes to external artifacts.

Example project folder:

```text
engineering_memory/
  PED-000042/
    manifest.yaml
    analyst/
      ANL-000042.yaml
      requirements/
        REQ-000181.yaml
      diagrams/
        DGM-CONTEXT-000031.mmd
        DGM-FLOW-000044.mmd
    tester/
      TPL-000042.yaml
      tests/
        TST-000501.yaml
        TST-000502.yaml
    programmer/
      decisions/
        PDR-000171.yaml
      candidates/
        CAND-000301.yaml
        CAND-000302.yaml
      metrics/
        MET-PROG-000021.yaml
      measurements/
        MEAS-PROG-000144.yaml
    security/
      reviews/
    critic/
      CRIT-000077.yaml
    experiments/
      EXP-000031.yaml
    verification/
      VER-000088.yaml
    experience/
      EXPREC-000177.yaml
    artifacts.yaml
    rendered/
      teaching.md
      production-card.md
```

The `rendered/` documents are generated views. They are not independent sources of truth.

## 3. Layer B — Evidence/artifact store

Large or sensitive evidence must not be embedded in Git history.

Candidate artifact types:
- raw logs/traces;
- benchmark datasets;
- packet captures;
- screenshots/video;
- VM/container images;
- backups/snapshots;
- large generated reports;
- binaries/installers;
- test corpora;
- hidden evaluation material;
- customer/private source material.

The Project Dossier stores only an artifact record:

```yaml
artifact_id: ART-000882
project_record_id: PED-000042
kind: benchmark_raw
classification: INTERNAL
uri_ref: STORE://...
sha256: "..."
size_bytes: 0
created_at: "..."
producer_ref: EXP-000031
retention_class: WARM_1Y
access_policy_ref: ACL-...
```

Physical storage may later be local NAS/object storage/protected cloud/private S3-compatible storage. The logical ID and hash must survive migration.

## 4. Layer C — Engineering graph/index

The canonical Project Dossier records are transformed into graph/search objects such as:

```text
REQ → DGM → TST → PDR → CAND → MET → MEAS → EXP → VER → EXPREC
```

and linked to:

```text
SOURCE → LOCATOR → CLAIM/PKB → DECISION
```

This layer is for retrieval, traversal and analytics. It is a derived index and must be rebuildable from canonical records + artifact metadata.

Do not treat vector similarity or graph rank as truth.

## 5. Layer D — Distilled experience and KB promotion

Project records do not automatically become universal rules.

Promotion path:

```text
project observation
→ repeated/important result
→ Experience Record
→ independent review / counter-evidence
→ candidate Knowledge Object
→ Knowledge Gate
→ VALIDATED/LIMITED KB object
```

Example:

```text
PED-000042
  PDR-000171 selected candidate B
  MET-REL-000014 favored B
  EXP-000031 reproduced result
  TST-000501 prevented regression
      ↓
EXPREC-000177
      ↓
PKB-000384 candidate rule
```

This keeps project-specific anecdotes from contaminating general knowledge.

## 6. Public / private / secret separation

### Safe for public GitHub when intentionally open
- schemas;
- example/synthetic dossiers;
- public source references;
- public task definitions;
- non-sensitive architecture examples;
- generated teaching material intended for publication.

### Private engineering repository or protected store
- proprietary project dossiers;
- customer cases;
- internal decision history;
- proprietary metrics/weights;
- commercial experience;
- detailed failure corpus;
- private source annotations.

### Restricted IP / hidden evaluation vault
- hidden tests;
- answer keys/expected states;
- tournament corpus;
- valuable counterexamples;
- calibrated decision/retrieval coefficients;
- agent weaknesses;
- security-sensitive mappings;
- privileged credentials/secrets (prefer dedicated secret manager, not artifact storage).

## 7. MVP physical implementation

Do not choose a production database merely because it is fashionable.

MVP sequence:

1. Define stable IDs and YAML/JSON schemas.
2. Store 1–5 complete synthetic Project Dossiers in Git.
3. Generate Teaching View and Production Card from the same records.
4. Create at least one full chain:
   `ANL → REQ → DGM → TST → PDR → MET → MEAS → EXP → VER → EXPREC`.
5. Link exact source locators and KB IDs.
6. Put at least one large artifact outside Git and resolve it by `artifact_id + hash + uri_ref`.
7. Build a technology-neutral graph export.
8. Measure record sizes, query patterns and update frequency.
9. Only then select the persistent query/storage engine.

Likely candidates may include relational/JSON storage plus vector retrieval and/or a graph projection, but the engine selection is a D2 decision and must be benchmarked against real Project Dossier queries.

## 8. Required query set before database selection

The storage engine must support, either directly or through derived indexes, queries such as:

1. Show every decision influenced by `MET-REL-000014`.
2. Show the source locator and KB object behind each material reason in `PDR-000171`.
3. Show every project where candidate A failed a particular hard gate.
4. Show all tests derived from `REQ-000181`.
5. Show failures that created regression tests and later KB updates.
6. Compare A/B outcomes for the same pattern across different project contexts.
7. Show which metrics consistently correlate with successful outcomes without treating correlation as causation.
8. Show where the same source/claim was used but later contradicted by E0 project evidence.
9. Rebuild a project's Teaching View from canonical records.
10. Reconstruct the complete decision/evidence chain after storage migration.

## 9. Retention model

Suggested logical retention classes:

- `HOT` — active project records/current evidence;
- `WARM` — completed project evidence still frequently queried;
- `COLD` — immutable historical artifacts;
- `PERMANENT_KB` — promoted knowledge/provenance objects;
- `HIDDEN_EVAL` — private retained evaluation corpus;
- `DELETE_ON_EXPIRY` — temporary/sensitive artifacts with explicit deletion date.

Retention is metadata first; physical storage policy can change without changing stable IDs.

## 10. Governing rule

**Git is the constitutional/versioned record for schemas, small canonical dossiers and open evidence. It is not the final warehouse for all engineering analytics.**

The durable architecture is:

```text
VERSIONED CANONICAL RECORDS
        +
PROTECTED ARTIFACT STORE
        +
REBUILDABLE GRAPH/SEARCH INDEX
        +
DISTILLED KNOWLEDGE BASES
```

This gives FATHER both auditability and long-term learning without mixing raw project history, public knowledge, hidden evaluation data and proprietary IP into one uncontrolled store.
