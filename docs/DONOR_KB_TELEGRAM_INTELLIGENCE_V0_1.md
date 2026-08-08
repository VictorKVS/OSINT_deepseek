# DONOR-KB / Telegram Intelligence v0.1

Status: DRAFT
Verified baseline date: 2026-08-08
Owner: FATHER Intelligence / OSINT

## Purpose

This document is the first structured donor-knowledge object for the FATHER Intelligence Agent. It replaces informal recommendation tables with a gated verification lifecycle.

No candidate may be marked ADOPT or APPROVED based only on README claims, stars, popularity, prior analysis, or LLM summaries.

## Decision lifecycle

DISCOVERED
→ SOURCE_VERIFIED
→ TECHNICALLY_VERIFIED
→ BENCHMARKED
→ APPROVED

Additional states:
WATCH / REJECT / SUPERSEDED / STALE / RETIRED.

## Required evidence before APPROVED

For each donor or component verify:
- canonical upstream repository;
- license and compatibility with project use;
- archive/read-only status;
- last meaningful commit and release activity;
- issue/PR health;
- dependency freshness;
- security posture and credential/session handling;
- architecture and integration boundaries;
- operational characteristics;
- reproducible minimal PoC;
- benchmark against the actual FATHER objective profile;
- documented WHY and alternatives rejected.

## Socrates gate

Before promotion to APPROVED the reviewer SHALL challenge:
- Is the upstream actually maintained?
- Are claimed performance/security properties measured or merely asserted?
- Are stars/forks being mistaken for maturity?
- Does the project solve our problem or merely a nearby one?
- Is the license clear?
- What hidden external services, paid APIs, lock-in or accounts are required?
- What happens if upstream disappears?
- Can we isolate the donor behind an adapter?
- What evidence would falsify the recommendation?

## Current Telegram Radar research frame

Primary mission:
Telegram Radar → Signal → Source Expansion → Analyst → Socrates → Knowledge Candidate → KB.

Telegram is treated as an early-signal layer, not an authority layer.

### Candidate mechanisms to research

1. MTProto ingestion and history retrieval.
2. Channel/source discovery.
3. Cursor/checkpoint management.
4. Polling/streaming, per-source timeout and hard timeout.
5. Session/credential protection.
6. Rate limiting, retry and flood-wait handling.
7. Raw observation storage with provenance.
8. Forward/reply/thread propagation graph.
9. Deduplication and repost clustering.
10. Link/media/entity extraction.
11. Source reliability and early-signal scoring.
12. Cross-source corroboration.
13. Search/index/cache strategy.
14. Health metrics and observability.
15. Adapter contract with FATHER OSINT CORE.

## Known candidate notes

### Telethon
State: SOURCE_VERIFIED / REASSESS
Reason: previously treated as a default Python MTProto client, but upstream archive/read-only status means it must not be automatically promoted to ADOPT. Existing code may still be useful as a compatibility donor, but maintenance risk must be included in the decision.

### WorldMonitor
State: DISCOVERED
Interesting patterns: low-latency Telegram intelligence feed, multi-channel polling, per-channel timeout, global hard timeout, operational feed design.
Action: inspect canonical repository/code and extract ingestion/runtime patterns rather than assume wholesale adoption.

### telegram-mcp
State: DISCOVERED
Interesting patterns: MTProto access, local cache/search, media/history support, rate-limit/session handling.
Action: inspect storage boundary, session protection, API/runtime assumptions.

### Shadowbroker
State: DISCOVERED
Interesting patterns: Telegram as one intelligence layer among many, cross-layer search, source attribution, delta/version ideas, entity correlation.
Action: study architecture and data model as donor patterns.

### OpenOSINT
State: DISCOVERED
Interesting pattern: LLM selects tools while deterministic code performs actual collection/action; useful for provenance and anti-hallucination separation.
Action: inspect tool contract, evidence model and execution boundary.

### Maltego Telegram ecosystem
State: DISCOVERED
Interesting patterns: source discovery, relationships, forwards, similar-channel and propagation analysis.
Action: study relationship-analysis concepts. De-anonymization is not the primary FATHER mission.

## First Donor Research Cycle acceptance criteria

The Telegram Radar donor cycle is complete only when:
- 10–20 canonical candidates have been identified;
- each has a structured donor card;
- source/license/activity/security evidence is captured;
- 3–5 finalists remain;
- at least one minimal PoC is run for finalists where feasible;
- common benchmark scenarios are defined;
- Analyst comparison is complete;
- Socrates challenge is complete;
- one architecture decision records ADOPT/ADAPT/STUDY/WATCH/REJECT with WHY.

## Donor card schema

DONOR-ID
Name
Capability
Canonical source
Version/commit inspected
License
Lifecycle state
Last meaningful activity
Architecture
Dependencies
Security concerns
Operational model
Performance evidence
Integration cost
Failure modes
Bus factor / maintenance risk
FATHER relevance
Alternative candidates
Decision
WHY
Evidence links
PoC result
Benchmark result
Reviewed date
Next review date
Superseded by

## Principle

A donor is not a dependency until proven useful. A dependency is not architecture until its trade-offs are recorded. An architecture decision is not durable knowledge until actual outcomes feed back into the donor card.
