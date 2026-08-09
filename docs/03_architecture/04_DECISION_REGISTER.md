# Stage 03 — Architecture Decision Register

**Status:** ACTIVE

This register records decisions and deferred decisions before implementation. It is intentionally lightweight; items that become major or long-lived decisions can later be promoted to standalone ADR files.

| ID | Decision / question | Status | WHY / evidence | Next action |
|---|---|---|---|---|
| ADR-CAND-001 | OSINT returns MaterialPackage, not final expert conclusion | ACCEPTED CONCEPT | preserves role separation and allows Analyst/Socrates replacement | verify through Stage 4 tests |
| ADR-CAND-002 | DEV uses fixtures/simple sources before production transports | ACCEPTED CONCEPT | proves behavior without secrets/Tor/MTProto complexity | keep production adapters frozen |
| ADR-CAND-003 | Collector is source-facing boundary | ACCEPTED CONCEPT | prevents source mechanics leaking into Analyst contract | verify collector contract |
| ADR-CAND-004 | exact content hash deduplication in DEV | PROVISIONAL | simple noise reduction; not intended as source-independence inference | decide required restart semantics |
| ADR-CAND-005 | bounded follow-up research cycles | ACCEPTED CONCEPT | prevents uncontrolled cost and infinite loops | test cycle limit |
| ADR-CAND-006 | Analyst/Socrates simple implementations remain DEV harness only | PROPOSED | useful to prove handoff but may exceed OSINT package ownership | resolve during architecture review |
| ADR-CAND-007 | `pipeline.py` and `review_pipeline.py` both remain | NOT DECIDED | apparent overlap has not been justified | compare and KEEP/MERGE/DELETE |
| ADR-CAND-008 | Teleproto/Node bridge as Telegram transport | DEFERRED | production transport not needed to prove DEV contract | revisit after Stage 4/5 |
| ADR-CAND-009 | local inspectable persistence instead of production DB | PROVISIONAL | lowest-cost mechanism for DEV acceptance | define persistence requirements first |
| ADR-CAND-010 | legacy `core/`, `services/`, old scripts are not implicit FATHER dependencies | ACCEPTED CONCEPT | prevents accidental architecture inheritance | require explicit requirement/test for inclusion |

## Decision quality rule

Every final architecture decision must record:

```text
Problem
→ Alternatives considered
→ Decision
→ WHY
→ Evidence / constraints
→ Consequences
→ What would cause reconsideration
```

A technology already present in the repository is not evidence that it should remain in the approved architecture.
