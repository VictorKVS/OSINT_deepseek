# Stage 07 / M5 — Telegram Transport Donor Research

**Verified:** 2026-08-10  
**Scope:** transport candidates for the approved Telegram Radar requirement.  
**Rule:** no candidate is ADOPTED by reputation. The path remains `DISCOVERED → SOURCE_VERIFIED → TECHNICALLY_VERIFIED → BENCHMARKED → APPROVED`.

## Decision summary

### PoC finalists

1. **TDLib** — primary PoC candidate.
2. **GramJS** — secondary PoC candidate / architecture comparison.

### Study / not PoC finalists

- **Telethon** — upstream GitHub archived 2026-02-21 and moved away from GitHub; retain as historical/design study, not a fresh foundation without separately verifying the new upstream.
- **Pyrogram** — upstream archived and explicitly no longer maintained; reject as new foundation.
- **Hydrogram** — Python/Pyrogram-family fork, but latest listed release found is 2024-06-30; insufficient freshness evidence for the M5 shortlist.

## 1. TDLib

**Official source:** `tdlib/td`  
**License:** Boost Software License 1.0.  
**Current evidence:** official Telegram library; repository updated May 2026; version update to 1.8.64 appeared 2026-05-07; commits continued through 2026-05-18.

### Relevant engineering properties

- Telegram-maintained transport/client core.
- Cross-platform C++ implementation.
- Fully asynchronous.
- Handles network implementation, encryption and local storage internally.
- Guarantees ordered updates.
- Local data can be encrypted using a user-provided key.
- JSON interface is specifically intended for languages other than native C++/Java/.NET.
- Official Python example uses the JSON/C interface through `ctypes`.
- A May 2026 commit specifically fixed the Python example log callback lifetime, showing that Python interoperability still receives upstream attention.

### Risks / costs

- Native build/deployment surface is materially heavier than a pure Python package.
- Python integration is a foreign-function/JSON boundary rather than a first-class Python package API.
- TDLib correctness does not remove Telegram account/API policy risks or FloodWait/429 realities.
- We still need our own Radar semantics: source registry, bounded fetch policy, checkpointing, provenance mapping, timeout/isolation and operational metrics.

### Current status

`SOURCE_VERIFIED → POC-1`

**WHY:** strongest upstream longevity signal, official ownership, explicit local encrypted storage, asynchronous update model and neutral JSON integration make it the best reference transport for a long-lived FATHER component.

## 2. GramJS

**Official source:** `gram-js/gramjs`  
**License:** MIT.  
**Current repository evidence:** roughly 1.7k stars / 228 forks in the retrieved official repository view; MTProto client for Node.js/browser; string and store sessions; connection retry option; raw Telegram API invocation; event handlers are supported.

### Relevant engineering properties

- Direct MTProto access.
- Simpler operational PoC than compiling TDLib if Node.js is acceptable.
- `StringSession` and `StoreSession` make session persistence explicit.
- `connectionRetries` is exposed in the client setup.
- Raw API access preserves escape hatches for unsupported high-level helpers.
- MIT is uncomplicated for use as a dependency.

### Caution from fresh verification

The official repository view lists the latest GitHub release as **v2.17.4 (2023-05-14)**. GitHub also showed a large open issue/PR backlog and no visible workflow runs in the retrieved Actions view. Search results did not establish the previously claimed “3.0.0 May 2026” release history. Therefore the older DONOR-KB claim that GramJS had a 2026 release cadence is **not accepted**.

The project may still have commits or npm publishing activity not captured by GitHub Releases, but that must be established during TECHNICAL_VERIFICATION rather than assumed.

### Current status

`SOURCE_VERIFIED → POC-2 / ACTIVITY-RISK`

**WHY:** excellent integration simplicity and proven MTProto design, but upstream freshness is less convincing than TDLib and creates a maintenance-risk question that the PoC/benchmark must answer.

## 3. Telethon

**GitHub source:** `LonamiWebs/Telethon`  
**Finding:** GitHub repository archived by owner on **2026-02-21** and read-only. GitHub README says the project moved to Codeberg.

### Implication

The old conclusion “Telethon is dead” is too strong; the accurate statement is: **the GitHub upstream is retired and the project claims a new upstream elsewhere**. Because the new upstream could not be independently inspected in this research environment, it does not pass SOURCE_VERIFIED for a new FATHER dependency today.

### Current status

`LEGACY/STUDY → REVERIFY NEW UPSTREAM LATER`

## 4. Pyrogram

**Source:** `pyrogram/pyrogram`  
**Finding:** archived 2024-12-23; README explicitly states the project is no longer maintained or supported. Licenses found include LGPL-3.0/GPL-3.0.

### Current status

`REJECT AS NEW FOUNDATION / STUDY ONLY`

## 5. Hydrogram

**Source:** `hydrogram/hydrogram`  
**License:** LGPL-3.0/GPL-3.0 files reported.  
**Model:** Python MTProto framework derived from/inspired by Pyrogram.

The official repository view found a latest listed release of **v0.2.0, 2024-06-30**. That is not sufficient freshness evidence for a 2026 production shortlist without deeper commit/security verification.

### Current status

`WATCH / NOT SHORTLISTED`

## Socrates gate

Before APPROVED, the following must be answered with tests/evidence rather than README claims:

1. Can one account monitor the target number of public channels without pathological FloodWait behavior?
2. What is the correct update strategy: live updates, bounded polling, or hybrid recovery polling?
3. How do we recover after process restart without silently losing messages?
4. How do we prevent one channel/request from blocking a full collection cycle?
5. How are sessions encrypted/stored/rotated and excluded from logs/repository?
6. Can edited/deleted/forward/reply metadata be represented without breaking the existing `Material` provenance contract?
7. What happens under network loss, Telegram DC migration, authorization expiry and 429/FloodWait?
8. What install/build burden does each transport add on Linux and Windows?
9. Does the transport expose enough stable identifiers to checkpoint per source?
10. Can the transport be replaced without changing `TelegramCollector` or Analyst/Socrates contracts?

## PoC contract — next gate

The PoC is intentionally small. Both finalists must implement the same adapter contract and must not enter production code directly.

```text
ResearchTask
   ↓
TelegramTransport adapter
   ↓
fetch public messages from a tiny allow-listed test set
   ↓
TelegramMessage records
   ↓
existing TelegramCollector
   ↓
Material / MaterialStore
```

### Mandatory PoC cases

- authenticate with secrets outside Git;
- read a small public-channel allow-list;
- fetch recent messages with stable channel/message identifiers;
- capture timestamp, author/sender when available, forward/reply metadata when available;
- restart and resume from a checkpoint without treating old messages as new observations;
- explicit FloodWait/429 reporting;
- per-source timeout/isolation;
- session file/string never printed by normal logs;
- all existing 21 DEV v1 tests remain green;
- fake transport tests remain the contract-level acceptance mechanism.

## Current architecture decision

No transport is APPROVED yet.

```text
TDLib  → PoC-1
GramJS → PoC-2
          ↓
identical functional scenario
          ↓
benchmark + ops/security comparison
          ↓
ADR
          ↓
ONE approved default transport
```

A second implementation may remain documented as a fallback option, but FATHER should not carry two production transports without a demonstrated operational need.
