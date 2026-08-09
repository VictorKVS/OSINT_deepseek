# Техническое задание: FATHER OSINT Agent v1

**Status:** DRAFT FOR REQUIREMENTS REVIEW  
**Implementation status:** existing code is PROTOTYPE / UNVERIFIED until reconciled with this document.

## 1. Purpose

OSINT Agent is a research supplier inside FATHER Knowledge Factory. It receives a research task from Analyst, obtains relevant materials from permitted sources, preserves provenance, removes obvious duplicates and returns a structured `MaterialPackage`.

The OSINT Agent does not decide truth, does not select architecture, does not publish into KB and does not replace Analyst or Socrates.

## 2. Process position

```mermaid
flowchart LR
    A[Analyst] -->|ResearchTask| O[OSINT Agent]
    O -->|MaterialPackage| A2[Analyst]
    A2 --> S[Socrates]
    S -->|research gap| A
    S -->|pass| G[Knowledge Gate - later phase]
```

## 3. Inputs

Minimum `ResearchTask` contract:
- question;
- topics/keywords;
- requested source types;
- optional date range;
- depth: FAST / NORMAL / DEEP / CRITICAL;
- maximum material count or equivalent bounded budget;
- requester identifier;
- optional stop condition.

## 4. Outputs

Minimum `MaterialPackage`:
- task identifier;
- collected materials;
- duplicates skipped;
- collection errors;
- stop reason;
- notes when required.

Minimum material record:
- source type;
- source locator;
- title or fallback identifier;
- collected raw text and/or local raw file reference;
- publication time when known;
- author/publisher when known;
- collection time;
- content hash;
- source-specific metadata.

## 5. Required behavior

1. Accept a bounded research task.
2. Select only collectors compatible with requested source types.
3. Collect permitted material without analytical conclusions.
4. Preserve source locator and original material/reference.
5. Deduplicate obvious identical content.
6. Isolate collector failure so one source does not necessarily destroy the whole package.
7. Stop at a declared limit or after collectors are exhausted.
8. Return explicit errors/gaps instead of silently inventing material.

## 6. DEV scope

DEV v1 uses simple deterministic collectors and prepared fixtures/public inputs. The goal is to prove contracts and handoffs, not battle collection.

Allowed now:
- JSON/text fixtures;
- local append-only storage;
- deterministic Analyst/Socrates stubs;
- bounded 1-3 cycle research loops;
- experimental transport code kept isolated and unapproved.

Deferred to PROD gate:
- live Telegram account/session operation;
- Dark Web/Tor gateway;
- proxy/session rotation;
- long-running scheduler;
- production secret storage;
- distributed queues/databases;
- automatic KB publication.

## 7. Non-functional requirements for DEV

- minimal dependencies;
- deterministic repeatable fixtures;
- no secrets committed to repository;
- code boundary between collector and transport;
- failures visible in result;
- local storage suitable for inspection;
- no unbounded agent loops.

## 8. Acceptance criteria

AC-01: valid ResearchTask with matching fixture collectors returns a non-empty MaterialPackage.  
AC-02: identical raw content is not stored twice as independent material.  
AC-03: absence of eligible collector returns explicit error/stop reason.  
AC-04: max_items bounds collection.  
AC-05: collector exception is recorded without corrupting already collected material.  
AC-06: Analyst can consume MaterialPackage without source-specific knowledge.  
AC-07: Analyst may request follow-up research when expected source coverage is missing.  
AC-08: DEV research loop has a hard maximum cycle count.  
AC-09: Socrates review either passes analysis or returns a bounded research-more request.  
AC-10: no Knowledge Gate/PROD connector is required to prove OSINT v1.

## 9. Definition of Done for this phase

The phase is complete only when this ТЗ is reviewed, architecture is reconciled, tests are mapped to acceptance criteria, current tests are executed, failures are classified, and existing source files receive `KEEP / CHANGE / DELETE / DEFER` status.
