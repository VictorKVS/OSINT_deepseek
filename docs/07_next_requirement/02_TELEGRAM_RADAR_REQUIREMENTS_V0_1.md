# Telegram Radar — Requirements v0.1

**Stage:** 07 / M5  
**Status:** DRAFT FOR REQUIREMENTS REVIEW  
**Date:** 2026-08-10  
**Parent decision:** `01_M5_CAPABILITY_PRIORITY.md`

## 1. Purpose

Telegram Radar is the first live acquisition capability added after DEV v1 freeze.

Its job is narrow:

> Receive a research task that names Telegram as a source type, collect requested material from approved public Telegram sources, preserve provenance, and return it through the existing OSINT contract.

It does not decide whether the material is true.

## 2. Business flow

```text
Analyst / research request
        ↓
ResearchTask
        ↓
OSINTAgent
        ↓
TelegramCollector
        ↓
TelegramTransport [replaceable]
        ↓
Telegram public source
        ↓
Telegram message data
        ↓
Material
        ↓
MaterialStore
        ↓
MaterialPackage
        ↓
Analyst / Socrates
```

## 3. In scope

### R-TG-01 — Public source collection
The system shall collect messages from explicitly requested public Telegram channels/sources that the configured account/transport is permitted to access.

### R-TG-02 — Replaceable transport
Telegram-specific network/protocol implementation shall remain behind the existing transport boundary so the collector contract does not depend on TDLib, GramJS or any named donor.

### R-TG-03 — Provenance
Every collected message shall preserve sufficient source provenance to identify where the observation came from, including source/channel identity, message identity where available, source locator where available, collection timestamp and payload metadata.

### R-TG-04 — Observation preservation
Two sources publishing equal content shall remain separate observations. Equal payload may reuse raw storage according to the frozen DEV v1 storage contract.

### R-TG-05 — Bounded execution
Collection shall respect task limits and shall not retry indefinitely. Rate-limit, timeout and authentication-related behavior must terminate or back off according to an explicit bounded policy.

### R-TG-06 — Explicit failures
Unavailable source, private/inaccessible source, invalid identifier, authentication failure, session failure, timeout and Telegram rate-limit/flood conditions shall be represented explicitly rather than silently disappearing.

### R-TG-07 — Secret separation
API identifiers, phone/account credentials, session keys and tokens shall never be committed to Git and shall never be stored as normal Material metadata.

### R-TG-08 — Deterministic testability
The transport boundary shall support a fake/fixture implementation so the contract can be tested without a live Telegram account or network.

### R-TG-09 — DEV v1 regression
All frozen DEV v1 acceptance tests and canonical runners shall remain green after M5 changes.

### R-TG-10 — Source registry boundary
The list of monitored/requested sources shall be supplied through task/configuration or a future source registry. TelegramCollector shall not hard-code intelligence judgments such as source trust or truth.

## 4. Deferred from M5

The following are explicitly not required for this milestone:

- media transcription;
- OCR/image analysis;
- generic PDF/document parsing;
- private group circumvention;
- account deanonymization;
- sockpuppet automation;
- proxy/Tor rotation as default architecture;
- autonomous channel discovery at internet scale;
- trust/confidence scoring;
- entity graph construction;
- Knowledge Gate or KB publication;
- autonomous scheduling/24x7 operations;
- battle-grade multi-account rotation.

These require separate requirements and gates.

## 5. Data mapping expectations

A Telegram observation should map into existing `Material` without creating Telegram-specific truth objects.

Expected minimum mapping:

```text
Telegram message
    source/channel
    message id
    public URL if available
    text/caption
    author/sender when available and appropriate
    published timestamp
    collection timestamp
    forward/reply metadata when available
        ↓
Material
```

Transport-specific raw structures may be preserved inside metadata only when needed for provenance/debugging and after secret filtering.

## 6. Reliability expectations

The transport/adapter design shall support:

- per-request timeout;
- bounded retries;
- explicit rate-limit/flood response handling;
- reconnect/restart without corrupting stored observations;
- failure isolation so one source does not silently invalidate unrelated collected material;
- idempotent persistence behavior through existing observation/payload semantics.

Exact timeout/retry values are **not approved here**. They must be justified by PoC/benchmark evidence rather than invented percentages or constants.

## 7. Security expectations

Before approval of a live transport implementation, review at minimum:

- session secret storage;
- logging/redaction;
- dependency vulnerabilities;
- upstream maintenance status;
- license compatibility;
- container/process isolation where relevant;
- Telegram account operational risks;
- accidental collection of credentials/private content;
- failure behavior under malformed/untrusted message content.

## 8. Acceptance-test candidates

The formal Stage 07 testing pack shall turn these into executable cases:

- **AC-TG-01:** public message maps to Material with provenance.
- **AC-TG-02:** same payload from two channels remains two observations.
- **AC-TG-03:** `max_items` is respected.
- **AC-TG-04:** one source failure is visible and does not erase successful source output.
- **AC-TG-05:** rate-limit/flood condition is explicit and bounded.
- **AC-TG-06:** unavailable/private source is explicit.
- **AC-TG-07:** fake transport passes without network/credentials.
- **AC-TG-08:** no session/token/credential is emitted into Material/package/log evidence.
- **AC-TG-09:** restart/persistence preserves provenance.
- **AC-TG-10:** all DEV v1 regression remains green.

## 9. Donor gate

No implementation begins until the transport candidates are freshly re-verified.

Required lifecycle:

```text
DISCOVERED
   ↓
SOURCE_VERIFIED
   ↓
TECHNICALLY_VERIFIED
   ↓
BENCHMARKED
   ↓
APPROVED via ADR
```

For each serious candidate verify official upstream, license, recent meaningful activity, issues/PRs, security posture, session handling, rate-limit behavior, language/runtime cost and fit with the Python FATHER stack.

## 10. Requirements review questions

Socrates/architecture review must challenge at least:

1. Are public channels enough for M5 value?
2. Does the existing `Material` contract capture all provenance needed for Telegram text messages?
3. Do we need push updates, polling, or both for the first approved version?
4. What is the smallest account/session model that is operationally safe?
5. Which error states belong in current `collection_errors` and which require a stronger typed error contract?
6. What evidence justifies retry/timeouts/backoff values?
7. How will we benchmark 10, 100 and later more sources without prematurely building distributed infrastructure?

## 11. Exit criterion for requirements stage

This document advances from DRAFT only after:

- requirements review finds no unresolved scope contradiction;
- the current `Material`/collector/error contracts are confirmed or explicitly amended;
- donor research is refreshed against current upstreams;
- candidate PoC plan is approved.

Only then do we create acceptance tests and implementation code.
