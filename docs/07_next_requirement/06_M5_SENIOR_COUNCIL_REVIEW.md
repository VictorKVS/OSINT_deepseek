# M5 Telegram Radar — Senior Council Review 001

**Council review ID:** SCR-M5-001  
**Stage:** Stage 07 / M5 Telegram Radar  
**Trigger:** transport PoC preparation after donor/pattern/security reviews  
**Decision requested:** confirm whether the project is ready to proceed to TDLib PoC and what must be proven before an ADR.

## Senior Product Lead

### Findings
- M5 remains the correct next capability because it converts the frozen fixture-based OSINT worker into a live acquisition capability without requiring M6/M7/M8 first.
- The same low-level Telegram metadata materially strengthens several high-priority product paths: Competitive Intelligence, Content Origin/Propagation, Brand Monitoring, Technology Radar and later Source Quality / Risk Intelligence.
- Product value does **not** require dashboards, AI summaries, identity scoring or media download in the first M5 implementation.

### Product guardrails
- Preserve stable source/message IDs, publication/edit timestamps, source locator, forward/reply metadata and text/content hash where cheap.
- Keep product-specific watchlists, scoring and reports outside the transport/core collector.
- Do not pull M6 media processing into M5 merely because commercial products may need it later.

### Recommendation
**PROCEED** with a bounded TDLib PoC. Do not start product UI/reporting during the transport decision.

---

## Senior Solution / Security Architect

### Findings
- The existing `TelegramTransport` boundary remains architecturally correct and should contain TDLib-specific concepts.
- The most important correctness invariant is not transport speed; it is state safety:

```text
receive / catch-up
      ↓
convert to Material
      ↓
durable save succeeds
      ↓
advance per-source checkpoint
```

- Recommended operational pattern remains: bounded catch-up + live updates + periodic reconciliation.
- A single bad/hanging source must not block other sources.
- Session/credentials introduce a new critical trust boundary and require dedicated storage/logging/disable controls before any reusable live adapter is approved.

### Architecture questions the PoC must answer
- Does TDLib expose stable enough identifiers and ordered updates for our adapter contract?
- How are edit/delete events represented and how much should M5 preserve?
- What local TDLib state is created and how can it be isolated/removed?
- How is crash/restart recovery observed?
- What is the simplest Python integration boundary that avoids leaking TDLib details upward?

### Recommendation
**PROCEED TO POC, NOT TO PRODUCT IMPLEMENTATION.** ADR remains blocked until measured restart/session/failure evidence exists.

---

## Senior Business / Intelligence Analyst

### Findings
- The collector must preserve observations, not infer truth, authorship, intent or identity.
- `earliest observed` is useful later for propagation analysis but must never be silently interpreted as true original author.
- Edits and deletions should be represented as observation/history signals rather than destructive rewrites when feasible within M5 scope.
- Forward/reply metadata has high analytical value because it supports propagation/relationship analysis without requiring semantic inference.

### Acceptance implications
The M5 contract should be able to answer from stored evidence:
- Which public source did this observation come from?
- Which Telegram message/source identifier referred to it?
- When was it observed/published/edited where available?
- Was it a forward/reply where available?
- Can the original observation still be traced after restart/reconciliation?

### Recommendation
**PROCEED**. Require provenance completeness tests before freeze; do not add trust/confidence scores to Telegram sources in M5.

---

## Senior Software Engineer

### Findings
- PoC should be a separate harness/adapter experiment, not a rewrite of `TelegramCollector` or DEV v1.
- Minimum implementation should prove connect/auth, bounded source retrieval, update handling, normalized adapter output, restart behavior, error isolation and safe shutdown.
- No framework/service/database should be added merely to run the PoC unless TDLib itself requires it.
- Raw operational metrics should be recorded instead of artificial scores.

### Proposed PoC work packets
1. Environment/bootstrap and TDLib loading.
2. Credentials/session directory external to repo.
3. Minimal adapter returning transport-neutral message records.
4. Bounded history/catch-up for allow-listed public sources.
5. Live update listener.
6. Restart/checkpoint experiment.
7. Source failure/timeout/error experiment.
8. Logging/secrets review.
9. Regression of frozen DEV v1.
10. Written raw results + defects.

### Recommendation
**PROCEED** with a deliberately disposable PoC harness. No production abstraction expansion until results require it.

---

## Senior Security / DevSecOps Reviewer

### Newly active / high-priority surfaces
- Telegram API credentials and session material.
- TDLib binary/library provenance and update lifecycle.
- untrusted Telegram content crossing into the process;
- FloodWait/rate behavior;
- local TDLib database/cache permissions;
- accidental secret/session logging;
- future containerization/CI execution risks if PoC setup is later automated.

### Blocking security requirements before M5 freeze
- no session/API secret in Git, normal logs or CI artifacts;
- dependency/binary source and version recorded;
- transport can be disabled/replaced without corrupting stored evidence;
- per-source bounded execution and rate/backoff behavior evidenced;
- invalid/untrusted content cannot become executable instructions;
- session/local DB paths have an explicit permissions/storage policy;
- relevant Top-100 and threat-register entries updated from PoC findings.

### Recommendation
**PROCEED TO LOCAL BOUNDED POC**. Real credentials must not enter shared CI. M5 freeze remains blocked on the above controls.

---

# Council synthesis

## Agreements
All five reviewers agree:
- M5 remains the correct critical-path capability.
- TDLib PoC should proceed.
- PoC must not modify the frozen DEV v1 semantic contract unnecessarily.
- the key evidence is restart/state/provenance/security behavior, not feature count.
- media download, dashboards, risk scoring and expert analytics stay out of M5 core.

## Disagreements / unresolved questions
No blocking disagreement. Open evidence questions:
- practical Python integration cost of TDLib;
- exact session/local-state operational behavior;
- quality of edit/delete/update handling;
- whether TDLib evidence is strong enough that GramJS comparative PoC ceases to add decision value.

## MUST before next gate
- execute TDLib PoC against the approved PoC plan;
- preserve secrets outside repository and shared CI;
- collect raw restart/error/session/provenance evidence;
- record dependency/upstream/binary state;
- run existing regression;
- issue a new council review after PoC before ADR.

## SHOULD
- preserve low-cost metadata supporting future propagation/competitive products;
- explicitly test edit/forward/reply mapping where TDLib exposes it;
- document kill/disable/cleanup procedure for the PoC session/state.

## OPTIONS — not current scope
- early Competitive Intelligence reporting MVP;
- propagation visualization;
- media Artifact download;
- multi-account operational layer.

## Final council disposition

**PROCEED → TDLib POC**

**Not approved:** production transport selection, M5 freeze, media ingestion, product-specific analytics.

## Next council trigger

`TDLib PoC completed OR material security/architecture blocker discovered`, whichever occurs first.
