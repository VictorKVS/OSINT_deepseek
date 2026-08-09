# 2026-08-09 — M2 LLM Gateway Experiment Cleanup

**Stage:** Stage 06 / Milestone M2  
**Trigger / problem:** `services/llm-gateway/` remained in the repository although it was not part of the verified FATHER OSINT DEV product and was not actually an approved LLM provider gateway.  
**Decision:** remove the experimental implementation from the active repository tree; retain its useful architectural lessons in documentation and Git history.  

## WHY

The project is being deliberately reduced to one understandable canonical path. The old subsystem implemented a policy-control experiment with Sphinx heuristics, Enigma rules, Judge decisions and duplicate policy logic. Keeping it beside the current product created a misleading impression that FATHER OSINT required or had approved an LLM gateway.

The useful future concept is separated into two possible requirements:

```text
LLM GATEWAY
= provider/model routing, fallback, cost, quotas, model policy

POLICY GATE
= deterministic versioned rules, decision, reason, audit trail
```

Neither is currently required for the DEV baseline.

## Files/documents affected

Removed from active tree:
- `services/llm-gateway/` implementation and historical outputs;
- now-empty `services/` marker README.

Added/updated:
- `docs/06_verification/13_LLM_GATEWAY_DISPOSITION.md`;
- root `README.md`;
- this journal record.

## Tests/evidence

Before removal:
- code search found no current product dependency on the service;
- the subsystem had already been statically audited and classified as a frozen experimental policy prototype.

Required after removal:
- clean GitHub Actions Stage 06 verification must remain green.

## Result

**PENDING CI at journal creation.**

## New risks/open questions

A future need for LLM routing or policy enforcement must not resurrect this old implementation automatically. Each must return as a separate requirement and pass architecture, test, donor/security and ADR gates.

## Next action

Confirm clean CI after removal. Then complete M2 repository-boundary review and decide whether Stage 06 can move to documentation consistency / DEV v1 baseline preparation.
