# Traceability Matrix

**Status:** STAGE 06 VERIFIED / SEMANTIC REMEDIATION APPLIED  
**Evidence baseline:** clean GitHub Actions checkout, Python 3.12, current pytest suite and both canonical DEV runners.

| Requirement / AC | Architecture owner | Implementation | Evidence | Status |
|---|---|---|---|---|
| AC-01 collect materials | OSINTAgent + Collector | `father_osint/agent.py`, `collectors/dev.py` | `test_father_osint_mvp.py` | VERIFIED |
| AC-02 preserve observations while reusing equal text payload | MaterialStore + Material | `storage.py`, `models.py` | MVP + architecture + semantic remediation tests | VERIFIED |
| AC-03 explicit no-collector result | OSINTAgent | `agent.py` | `test_father_osint_mvp.py` | VERIFIED |
| AC-04 bounded `max_items` | OSINTAgent | `agent.py` | `test_father_osint_mvp.py` | VERIFIED |
| AC-05 collector failure isolation | OSINTAgent | `agent.py` | `test_architecture_acceptance.py` | VERIFIED |
| AC-06 generic Analyst handoff | MaterialPackage / DEV Analyst | `models.py`, `analysis.py` | `test_simple_analyst.py` | VERIFIED DEV |
| AC-07 follow-up research request | DEV Analyst | `analysis.py` | `test_simple_analyst.py` | VERIFIED DEV |
| AC-08 hard maximum cycles | DEV orchestration | `review_pipeline.py` | pipeline + architecture tests | VERIFIED |
| AC-09 Socrates PASS / RESEARCH_MORE | DEV Socrates | `socrates.py`, `review_pipeline.py` | `test_simple_socrates.py` | VERIFIED DEV |
| AC-10 no PROD dependency required | Architecture | fixture collectors + local store | clean CI + runners | VERIFIED DEV |
| AC-11 cumulative evidence across follow-up cycles | DevReviewPipeline | `review_pipeline.py` | `test_semantic_remediation.py` | VERIFIED |
| AC-12 payload reuse metric has explicit meaning | MaterialPackage + MaterialStore | `models.py`, `storage.py`, `agent.py` | `test_semantic_remediation.py` | VERIFIED |
| AC-13 file-only SHA-256 + missing-file failure | MaterialStore | `storage.py` | `test_semantic_remediation.py` | VERIFIED |

## Current file disposition

| File/group | Decision |
|---|---|
| `father_osint/models.py` | KEEP — current DEV contracts |
| `father_osint/agent.py` | KEEP — collection orchestration |
| `father_osint/collectors/dev.py` | KEEP DEV ONLY |
| `father_osint/collectors/telegram.py` | KEEP TRANSPORT-NEUTRAL CONTRACT; live transport deferred |
| `father_osint/storage.py` | KEEP — append-only DEV provenance store |
| `father_osint/analysis.py` | KEEP DEV SIMULATOR |
| `father_osint/socrates.py` | KEEP DEV SIMULATOR |
| `father_osint/review_pipeline.py` | KEEP — canonical cumulative bounded DEV orchestration |
| `father_osint/transports/` | KEEP AS FUTURE BOUNDARY; no approved implementation |
| removed legacy runtime / `core/` / `vip/` / experimental gateway / Teleproto bridge | REMOVED AFTER AUDIT; history retained in docs/Git |

## Semantic invariants currently enforced

```text
Equal payload != equal observation
Observation provenance is append-only in DEV
Payload reuse never means source observation was skipped
Follow-up research accumulates evidence
File-only source artifacts are hashed from original bytes
Unresolved collection gaps are explicit
Research loops are hard bounded
```

## Rule

A row is VERIFIED only because an executable test or explicit clean-checkout evidence exists. Code existence alone is not verification. Future PROD capabilities require their own requirements, ADRs, threat review and acceptance evidence.
