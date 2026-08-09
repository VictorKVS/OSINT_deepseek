# FATHER OSINT — DEV v1 Baseline Freeze

**Date:** 2026-08-10  
**Status:** APPROVED DEV BASELINE  
**Stage 06:** CLOSED

## Purpose

This record freezes the first verified FATHER OSINT development baseline after requirements review, architecture review, acceptance tests, repository cleanup, semantic remediation and clean CI verification.

The freeze exists to prevent silent feature creep. Future work starts from a new approved requirement.

## Frozen business boundary

```text
ResearchTask
    ↓
OSINTAgent
    ↓
Collectors
    ↓
Material + provenance
    ↓
MaterialStore
    ↓
MaterialPackage
    ↓
SimpleAnalyst [DEV]
    ↓
SimpleSocrates [DEV]
    ↓
PASS or bounded RESEARCH_MORE
```

Not part of DEV v1:
- Knowledge Gate / KB publication;
- expert-quality LLM Analyst/Socrates;
- live Telegram transport;
- Tor/dark-web gateway;
- scheduler/distributed queues;
- production secrets infrastructure;
- production observability;
- generic Artifact/media/document ingestion;
- local transcription engine.

## Frozen semantic invariants

1. OSINT collects; it does not decide truth or publish knowledge.
2. Source observation identity is distinct from payload identity.
3. Equal payload may reuse storage but must not erase provenance.
4. Follow-up research uses cumulative evidence from earlier cycles.
5. Research loops are hard bounded.
6. Collector failure is isolated and visible.
7. Missing evidence produces explicit gaps/errors rather than invented material.
8. File-only material is hashed from original bytes.
9. Missing local files fail explicitly.
10. Telegram collector remains independent of a concrete transport implementation.
11. Fixtures prove program behavior, not external-world truth.
12. Uncalibrated configuration weights are not confidence/trust scores.

## Verification evidence

Current clean CI baseline:

```text
Python 3.12               PASS
import father_osint       PASS
21 tests collected        PASS
21 tests passed           PASS
run_dev_osint.py          PASS
run_dev_pipeline.py       PASS
```

The verification workflow is `.github/workflows/dev-verification.yml`.

## Active dependency surface

- Runtime: Python standard library only.
- DEV verification: `pytest` via `requirements-dev.txt`.

Historical prototype dependencies are not active product dependencies.

## Repository state

Active product areas:
- `father_osint/`;
- `tests/`;
- `scripts/`;
- `config/`;
- `data/dev/`;
- `docs/`;
- `.github/workflows/`.

Legacy/experimental implementations removed from the active tree remain recoverable through Git history and documented audits.

## Change-control rule after freeze

A proposed change to DEV v1 must answer all of the following before implementation:

1. What approved requirement requires the change?
2. Is the change a defect correction or a new capability?
3. Which component owns the responsibility?
4. What exact contract changes?
5. Which acceptance test will fail before the change and pass after it?
6. Does the change break any frozen invariant?
7. Does it add a new dependency or external service?
8. What is the rollback path?

If these questions are not answered, the baseline is not modified.

## Next milestone

**M5 — select one next business capability and start a new engineering cycle.**

Current candidates recorded in the roadmap:
- live Telegram Radar transport;
- generic Artifact/Ingestion layer;
- local-first transcription;
- Knowledge Gate foundation.

Selection is based on business value and reuse, not on which technology is most interesting.
