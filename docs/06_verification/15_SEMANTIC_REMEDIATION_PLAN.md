# Stage 06 — Semantic Remediation Plan

**Status:** APPROVED REMEDIATION PLAN  
**Trigger:** findings from `14_FULL_PROJECT_AUDIT_2026-08-09.md`  
**Rule:** contract/test evidence before implementation.

## Problems to correct

### S-01 — Follow-up cycles do not accumulate evidence

Current `DevReviewPipeline` passes only the current cycle's `MaterialPackage` to Analyst and Socrates. A two-source task can therefore oscillate when cycle 1 finds source A and cycle 2 finds source B.

**Required contract:** a research run is cumulative. Every cycle keeps its own package for audit, while Analyst/Socrates review a cumulative package containing all material observations and collection errors acquired so far in that run.

Observations remain separate; cumulative assembly is not semantic entity merging.

### S-02 — `duplicates_skipped` has no valid DEV meaning

Observation-level deduplication is intentionally undefined in DEV v1. Therefore a field named `duplicates_skipped` is misleading.

**Required contract:** replace it with `payloads_reused`, meaning: a collected observation was preserved, while its raw payload bytes already existed in content-addressed storage and were reused.

This metric MUST NOT imply that the observation itself was dropped.

### S-03 — file-only Material has no payload hash

A Material may contain `raw_text` or `local_path`. The store currently hashes text only.

**Required contract:** when Material has a readable local file and no raw text, compute SHA-256 over the original file bytes. The original file remains the source artifact; DEV v1 does not silently copy/normalize it.

If the referenced local file does not exist, persistence must fail explicitly rather than record unverifiable provenance.

## Acceptance tests to add before implementation

### AC-11 cumulative follow-up evidence

```text
Task requires telegram + github
Cycle 1 collector returns telegram only
Cycle 2 collector returns github only
Expected:
- two cycles maximum for the fixture scenario;
- cumulative review sees telegram + github;
- final Socrates status PASS;
- both source observations remain traceable.
```

### AC-12 payload reuse metric

```text
Two distinct source observations contain equal raw_text
Expected:
- both observations saved;
- one raw SHA-256 blob;
- package.payloads_reused == 1;
```

### AC-13 file-only hashing

```text
Material(raw_text=None, local_path=<existing file>)
Expected:
- content_hash = SHA-256(file bytes);
- observation saved.

Material(local_path=<missing file>)
Expected:
- explicit failure/error, not silent persistence.
```

## Minimal implementation target

Only after the tests exist:

1. `models.py` — rename package metric to `payloads_reused`.
2. `storage.py` — return whether raw payload storage was reused; hash file-only payloads.
3. `agent.py` — preserve every observation and increment `payloads_reused` when appropriate.
4. `review_pipeline.py` — build cumulative package for Analyst/Socrates while retaining per-cycle package history.
5. runners/docs — align terminology.

No database, semantic deduplication, entity resolution or production transport is introduced by this remediation.
