# M5 Telegram Radar — TDLib PoC Test Plan

**Status:** APPROVED FOR POC PREPARATION / NO PRODUCT CODE YET  
**Stage:** 07 — M5 Telegram Radar  
**Candidate:** TDLib  
**Role:** transport implementation candidate behind the existing `TelegramTransport` boundary  
**Frozen baseline:** FATHER OSINT DEV v1 must remain green throughout the PoC.

---

## 1. Purpose

The PoC answers one narrow engineering question:

> Can TDLib serve as a reliable, replaceable Telegram transport for FATHER OSINT Radar without changing the frozen `ResearchTask → TelegramCollector → Material → MaterialStore` contract?

The PoC does **not** approve TDLib for production merely because a connection succeeds.

---

## 2. What must be proven

TDLib must demonstrate all of the following at PoC level:

1. authentication/session bootstrap can be isolated from product logic;
2. public Telegram channel history can be read deterministically;
3. source/channel/message identifiers remain stable enough for provenance;
4. message timestamp, text, author/channel metadata and public locator can be mapped into current `TelegramMessage` / `Material` semantics;
5. restart does not silently lose or duplicate observations outside the defined collection window;
6. one failing/slow source does not crash the whole collection run;
7. rate-limit / retry conditions are surfaced explicitly;
8. credentials/session state are never committed to Git;
9. the adapter can be removed/replaced without changing `TelegramCollector`;
10. the complete frozen DEV v1 suite remains green.

---

## 3. Explicit non-goals

This PoC does not include:

- private chats/groups;
- bypassing access controls;
- mass account creation;
- proxy rotation;
- Tor/dark-web routing;
- sockpuppets;
- media OCR/transcription;
- semantic analysis;
- source trust scoring;
- Knowledge Gate publication;
- automatic channel discovery;
- production scheduler;
- horizontal scaling.

Those require separate requirements.

---

## 4. Architecture boundary

```text
ResearchTask
    ↓
OSINTAgent
    ↓
TelegramCollector
    ↓
TelegramTransport protocol
    ↓
TDLibAdapter   ← PoC only
    ↓
TDLib
    ↓
Telegram
```

The PoC is invalid if TDLib-specific objects leak upward into `TelegramCollector`, `Material`, Analyst or Socrates.

---

## 5. Test-source policy

Use **5–10 public channels** only.

The final list must be verified immediately before execution because channel availability and public status can change.

Selection should cover distinct traffic patterns rather than famous names:

| Slot | Channel profile | Purpose |
|---|---|---|
| CH-01 | low-volume public technology/news channel | baseline history read |
| CH-02 | medium-volume public technology channel | normal pagination |
| CH-03 | high-volume public news channel | burst/history behavior |
| CH-04 | public channel with frequent forwarded posts | forward metadata |
| CH-05 | public channel with replies/comments linked | reply metadata availability |
| CH-06 | multilingual public technology channel | Unicode/text integrity |
| CH-07 | public channel with media-heavy posts | text + media metadata without media download |
| CH-08 | intentionally invalid/unavailable locator | explicit failure behavior |

Optional CH-09/CH-10 may be added for a second language or another high-volume source.

### Source rules

- public access only;
- no personal/private test material;
- no confidential information;
- no channel is considered trustworthy merely because it is in the PoC;
- exact handles/IDs used during execution belong in the run report, not in architecture requirements.

---

## 6. PoC environment

Minimum target environment:

```text
OS:        Linux clean checkout first
Python:    3.12
TDLib:     pinned tested build/version
Secrets:   environment / external local secret file only
Session:   outside repository
Data root: isolated PoC runtime directory
```

A Windows run may follow, but Linux is the first reproducible benchmark environment because the frozen baseline is already proven there.

---

## 7. Secret/session rules

The PoC must fail review if any of these appear in Git history or normal logs:

- Telegram API ID/API hash;
- phone number unless deliberately redacted in a local-only diagnostic;
- authentication code;
- password / 2FA secret;
- TDLib auth database/session files;
- reusable auth token/key material.

Required layout principle:

```text
repository code
      │
      ├── configuration schema only
      │
external secret/session location
      │
      └── runtime injection
```

Session files must have restrictive local permissions where supported.

---

## 8. Functional PoC cases

### POC-TD-01 — Session bootstrap

**Given:** valid locally supplied Telegram API/session parameters.  
**When:** TDLib adapter starts.  
**Then:** it reaches an authenticated ready state without putting secrets in repository files.

**Evidence:** startup log with redacted state transitions.

---

### POC-TD-02 — Public channel resolution

**Given:** a valid public channel locator.  
**When:** adapter resolves it.  
**Then:** a stable Telegram chat/channel identifier is returned and recorded as transport metadata.

---

### POC-TD-03 — Bounded history read

**Given:** a public channel and bounded request (`max_items`, optional time/window cursor).  
**When:** collection runs.  
**Then:** no more than the requested bound is returned and execution terminates predictably.

---

### POC-TD-04 — Stable message identity

Collect the same bounded window twice.

Expected:
- same Telegram message IDs for unchanged posts;
- same source identity;
- same content bytes produce same content hash once mapped to `Material`;
- observations remain separately traceable according to current provenance semantics.

---

### POC-TD-05 — Restart/checkpoint behavior

Run A collects an initial window.  
Restart process.  
Run B continues from a defined checkpoint/window.

Expected:
- no unexplained gap;
- no infinite replay;
- any repeated observations are explicit and explainable;
- checkpoint state belongs to the transport/runtime layer, not Analyst/Socrates.

---

### POC-TD-06 — Invalid channel isolation

Include CH-08 invalid/unavailable locator alongside valid channels.

Expected:
- failure is explicit;
- valid channels still return results;
- one source error does not abort the whole `OSINTAgent` run.

---

### POC-TD-07 — Slow/timeout isolation

Force or simulate one transport call to exceed a per-source timeout.

Expected:
- bounded timeout;
- explicit source error;
- remaining sources continue;
- no deadlock.

---

### POC-TD-08 — Rate-limit / retry visibility

If a real Telegram rate-limit condition occurs, record it. If it cannot be safely reproduced, simulate the adapter-level TDLib error/result contract.

Expected:
- retry/wait condition is not hidden;
- adapter exposes structured failure/wait information;
- bounded retry policy exists outside business logic;
- no uncontrolled busy loop.

---

### POC-TD-09 — Unicode and long text integrity

Use multilingual/long-post samples.

Expected:
- UTF-8 text preserved;
- no silent truncation below Telegram-provided content;
- hash is calculated from the exact bytes stored by FATHER.

---

### POC-TD-10 — DEV v1 regression

After adding the isolated PoC adapter/test harness:

```text
python -m pytest -q
python scripts/run_dev_osint.py
python scripts/run_dev_pipeline.py
```

Expected: frozen baseline remains green.

---

## 9. Measurements

Do not invent a composite score. Record raw measurements first.

For each run capture:

- TDLib version/build;
- adapter commit SHA;
- OS/Python version;
- number of channels;
- messages requested/returned per channel;
- wall-clock time per channel;
- total run time;
- timeout/error count;
- retry/rate-limit events;
- process RSS before/peak/after where practical;
- session/bootstrap time;
- restart behavior;
- duplicate/replayed observation count (as observations, not "duplicate truth");
- payload reuse count in FATHER storage;
- any data-loss discrepancy.

No “95% reliability” or similar percentage is allowed unless a defined repeated-run denominator exists.

---

## 10. PASS / FAIL gate

### Mandatory PASS conditions

TDLib advances to comparative benchmark only if:

1. public channel acquisition works on all valid PoC source classes used in the run;
2. stable source/message identity is available;
3. current `TelegramCollector` contract does not change for TDLib-specific reasons;
4. restart behavior is explainable and bounded;
5. invalid/slow source behavior is isolated;
6. secrets/session state remain outside Git and ordinary logs;
7. current DEV v1 regression remains green;
8. there is no observed silent data loss in the bounded test window.

### Immediate FAIL conditions

- secrets committed or logged;
- TDLib-specific model leaks into upper domain contracts;
- uncontrolled infinite retry/wait;
- one channel can indefinitely block all others;
- message/source identity cannot be preserved;
- reproducible silent data loss;
- frozen baseline regression breaks and cannot be isolated cleanly.

### CONDITIONAL / REVIEW conditions

These do not automatically fail the candidate but must enter the ADR:

- cumbersome native build process;
- large runtime footprint;
- difficult Python integration;
- session database operational complexity;
- weak diagnostics;
- platform-specific deployment burden.

---

## 11. Comparison contract with GramJS

GramJS must later run the **same logical PoC cases** wherever technically applicable.

The decision must compare like with like:

```text
same source set
same requested windows
same max_items
same timeout policy
same Material mapping
same restart scenario
same error scenarios
same evidence report structure
```

We will not choose TDLib because it is official, nor GramJS because it is simpler. The ADR will choose the candidate whose observed behavior best satisfies M5 requirements with acceptable operational cost.

---

## 12. Required PoC artifacts

Before ADR, produce:

1. `TDLIB_POC_RUN_REPORT_<date>.md`;
2. exact TDLib build/version provenance;
3. redacted environment/config instructions;
4. test harness / adapter code isolated under the transport boundary;
5. raw benchmark measurements;
6. defects/limitations list;
7. Socrates review: what is still unproven;
8. equivalent GramJS PoC report;
9. comparative ADR.

---

## 13. Implementation gate

**This document authorizes PoC preparation, not production integration.**

Next sequence:

```text
PoC test plan approved
       ↓
minimal TDLib adapter design
       ↓
PoC harness + tests
       ↓
TDLib execution report
       ↓
GramJS same-contract PoC
       ↓
comparison + security review
       ↓
ADR
       ↓
only then product transport implementation
```
