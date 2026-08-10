# M5 Telegram Radar — implementation pattern review

Date: 2026-08-10
Status: DESIGN INPUT — before adapter implementation

## Why

Before implementing TDLibAdapter, inspect how active projects solve the operational problems we actually have: incremental capture, live updates, restart/checkpoint, isolation, cache, session security, media policy and reconciliation. We adopt proven patterns, not whole applications.

## Projects reviewed

### 1. Telegram Archive (GeiserX/Telegram-Archive)

Most useful donor for ingestion lifecycle.

Observed patterns:
- incremental backup instead of full re-fetch;
- scheduled reconciliation plus real-time listener;
- checkpoint persisted after configurable batch intervals, so crash/restart resumes from last committed batch;
- bounded media retry attempts;
- per-chat media policy;
- edits/deletions/new messages handled separately;
- deletion mirroring disabled by default (archive-preserving behavior);
- SQLite for simple deployment, PostgreSQL as scale-up option;
- message-time sender-name snapshot preserves historical observation instead of rewriting history from mutable current profile;
- transient vs terminal peer errors are distinguished; terminal identifiers fail fast instead of consuming retry budget.

FATHER decision: ADAPT these patterns.

### 2. WorldMonitor

Most useful donor for a small low-latency public-channel radar.

Observed patterns:
- curated channel registry;
- sequential 60-second polling cycle;
- per-channel timeout;
- global cycle timeout;
- poll concurrency guard;
- graceful shutdown;
- explicit MTProto session supplied as secret/environment value.

FATHER decision: ADAPT timeout/isolation/guard patterns, but do not copy application code or its product architecture.

### 3. telegram-mcp

Most useful donor for local cache and session hygiene.

Observed patterns:
- transport wrapper separated from MCP/application surface;
- passive SQLite cache;
- live Telegram results merged with cached history for search;
- session/config/cache files created with owner-only permissions;
- explicit request-rate caps by operation class;
- raw JSON retained in cache;
- bulk export bounded per call.

FATHER decision: ADAPT session hygiene, bounded operations and cache-as-supplement semantics. Do not couple Telegram transport to MCP.

### 4. TDLib upstream

Transport foundation candidate.

Observed guarantees/features relevant to our boundary:
- networking/encryption/local data storage handled by TDLib;
- ordered update delivery;
- asynchronous requests;
- encrypted local data with user-provided key;
- JSON interface usable from Python and other languages;
- official upstream.

FATHER decision: POC-1 transport. Keep all TDLib-specific types below TelegramTransport boundary.

## Resulting minimal architecture

```text
ResearchTask
    |
    v
TelegramCollector
    |
    v
TelegramTransport (our stable port)
    |
    +--> TDLibAdapter [PoC-1]
    |
    v
Channel worker / request scope
    |
    +--> bounded history/bootstrap
    +--> update listener
    +--> per-source timeout
    +--> retry classification
    |
    v
TelegramObservation mapper
    |
    v
Material -> MaterialStore

Side state (not domain truth):
- checkpoint per source
- session/auth state
- operational cache if later justified
```

## Key design change after donor review

Do NOT make polling the only ingestion mechanism.

Use a hybrid lifecycle:

```text
START
  -> bounded catch-up from checkpoint
  -> live updates
  -> periodic reconciliation
  -> persist checkpoint only after durable Material save
```

Why: polling-only is simple but can re-fetch unnecessarily and can leave awkward gaps around restarts. Listener-only can miss events during downtime or best-effort update delivery. Catch-up + listener + reconciliation gives a small and robust model.

## Checkpoint rule

Checkpoint is per Telegram source, not global.

Minimum state:

```text
source_id
last_durable_message_id
updated_at
```

A checkpoint MUST advance only after the corresponding observation has been durably saved. Crash before save => safe re-fetch. Crash after save but before checkpoint => duplicate observation may be seen again, but provenance/dedup semantics must make this safe.

## Update semantics

For M5:
- new message: ingest as observation;
- edit: preserve evidence of the observed version; do not silently overwrite historical evidence;
- deletion: do not delete FATHER evidence merely because Telegram later deletes the source message;
- media: metadata first; binary download is deferred to Artifact/Ingestion milestone unless explicitly required by M5 acceptance criteria.

This follows FATHER's evidence-preserving philosophy and avoids turning Telegram Radar into a mirror client.

## Failure isolation

One source must not block the radar.

Required boundaries:
- per-source timeout;
- bounded retry;
- classify terminal vs transient errors;
- FLOOD_WAIT/rate-limit surfaced explicitly;
- global cycle/reconciliation deadline;
- concurrency guard to prevent overlapping reconciliation runs.

No unbounded sleeps inside the domain pipeline.

## Session security

Minimum:
- session/auth data outside repository;
- secrets never written to fixtures/logs;
- restrictive filesystem permissions where supported;
- separate test identity/session from production identity;
- adapter logs must redact credentials/session material.

## What NOT to adopt yet

- Redis: no demonstrated need in M5;
- PostgreSQL: no demonstrated need in M5;
- MCP: application protocol, not ingestion requirement;
- Web viewer/UI: irrelevant;
- complex distributed crawler: premature;
- automatic deletion mirroring: conflicts with evidence preservation;
- media download pipeline: belongs to M6 Artifact unless PoC proves a blocking requirement.

## PoC implications

TDLib PoC must now prove not only `fetch messages`, but the lifecycle:

1. authenticate without secrets in repo;
2. resolve configured public sources;
3. bounded bootstrap/catch-up;
4. map stable Telegram identifiers into Material provenance;
5. save durably;
6. advance per-source checkpoint after save;
7. receive new update or emulate this boundary in harness;
8. restart and resume without losing the gap;
9. isolate a failing/hanging source;
10. preserve DEV v1 regression.

## Socrates gate

Question: Are we building a Telegram client?
Answer: No. Only a source adapter for evidence collection.

Question: Do we need to copy Telegram Archive?
Answer: No. We take its proven lifecycle ideas: incremental catch-up, listener, reconciliation, checkpoint-after-commit and archive-preserving update semantics.

Question: Do we need Redis now?
Answer: No. A local checkpoint store is sufficient for PoC. Introduce infrastructure only after benchmark evidence.

Question: Should Telegram edits overwrite stored evidence?
Answer: No. A later edit is another observed state/version. Historical evidence must remain reconstructable.

## Gate

APPROVED AS DESIGN INPUT.

Next action: revise TDLib PoC harness design to implement the minimal hybrid lifecycle and checkpoint contract. No production integration before PoC evidence.