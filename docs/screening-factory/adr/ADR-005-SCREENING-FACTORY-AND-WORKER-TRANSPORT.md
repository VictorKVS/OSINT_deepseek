# ADR-005: Screening Factory and governed worker transport

**Status:** PROPOSED  
**Date:** 2026-09-03

## Context

Repeatable checks for persons and legal entities require parallel tools and country-specific sources, but direct tool-to-tool calls, arbitrary shell transport and silent merge would make the result unsafe and non-auditable.

## Decision

1. Use four stable screening profiles: RU/foreign × person/legal entity.
2. Run dependency-aware work items through five shared streams.
3. Tools remain independent and are invoked only by registered adapters.
4. Windows sends typed, integrity-protected job envelopes to Kali workers.
5. Raw evidence is transferred separately from commands.
6. A single merge service writes the common model.
7. Email is audit/approval/fallback, not the primary execution queue.
8. `FOUND` produces observations, not FACT.
9. High-impact matches require human review.
10. Active/intrusive tools are outside this factory.

## Consequences

Positive: reproducible runs, parallelism, clear gaps, provider isolation, country packs, traceability and controlled re-screening.

Cost: more schemas, adapter maintenance, source-version monitoring, evidence storage and mandatory analyst review for ambiguous/high-impact cases.
