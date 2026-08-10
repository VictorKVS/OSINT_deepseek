# Development Journal — Senior Council Governance + M5 Review

**Date:** 2026-08-10  
**Stage / milestone:** Stage 07 / M5 Telegram Radar  
**Trigger:** project owner requested a standing senior council so product, architecture, analysis, engineering and security contribute independently at every material stage.

## Decision

Introduce a permanent **FATHER Senior Engineering & Product Council** as a governance gate.

Council roles:
- Senior Product Lead;
- Senior Solution / Security Architect;
- Senior Business / Intelligence Analyst;
- Senior Software Engineer;
- Senior Security / DevSecOps Reviewer.

Each role must produce its own findings, risks, plan/recommendation and may disagree with the others. Council synthesis records agreements, dissent, unresolved questions, MUST/SHOULD/OPTION work and final disposition.

## WHY

The project has already shown that technically plausible decisions can become weaker after donor verification, architecture review or security review. A permanent multi-perspective challenge reduces four recurring failure modes:

1. building a technically interesting feature without enough product value;
2. selecting a convenient technology that creates architectural or operational debt;
3. losing evidence/analytical semantics while optimizing implementation;
4. discovering security/supply-chain problems only after implementation.

The council is intentionally constrained by FATHER principles: no code before contract, Occam, evidence over confidence, uncertainty allowed, history preserved, reusable core/product-specific edges and permanent DevSecOps review.

## First council execution — SCR-M5-001

The first formal council reviewed the current M5 Telegram Radar transport PoC gate.

### Product
M5 remains the correct critical-path capability. Preserve stable IDs/timestamps/forward-reply/source/hash metadata cheaply because it strengthens Competitive Intelligence, Content Propagation, Brand Monitoring and Technology Radar. Do not pull dashboards/media/risk scoring into M5.

### Architecture
Keep TDLib behind the existing transport boundary. Critical invariant: durable Material save occurs before per-source checkpoint advancement. Prefer bounded catch-up + live updates + reconciliation and source isolation.

### Analyst
Collector preserves observations/provenance, not truth/authorship/intent. `earliest observed` must remain distinct from true origin. Edits/deletes should not silently erase history.

### Engineering
Use a deliberately bounded/disposable PoC harness. Prove auth/connect, bounded history, updates, restart/checkpoint, source failure handling, safe shutdown and DEV v1 regression before any product transport expansion.

### Security / DevSecOps
New critical surfaces are Telegram credentials/session material, TDLib binary/dependency provenance, untrusted content, local TDLib state, FloodWait/rate behavior and logging. Real credentials stay outside Git and shared CI.

## Result

**Council disposition: PROCEED → TDLib POC.**

Not approved yet:
- production transport choice;
- M5 freeze;
- media ingestion;
- product-specific analytics;
- shared-CI live credentials.

## Commercial / reuse review

No registry reprioritization required at this gate. Existing ★★★★★ Telegram-dependent product hypotheses are strengthened by preserving low-cost source/provenance metadata, but they do not become implementation backlog yet.

## Files added
- `docs/SENIOR_COUNCIL_GOVERNANCE.md`
- `docs/07_next_requirement/06_M5_SENIOR_COUNCIL_REVIEW.md`
- this journal entry.

## New risks / controls
- risk of council bureaucracy → controlled by allowing `NO MATERIAL CHANGE` and exempting formatting/minor commits;
- risk of false consensus → dissent must be explicitly recorded;
- security BLOCK may only be overridden through named risk acceptance with WHY.

## Next action

Execute the approved TDLib PoC plan. Convene the next council automatically when the PoC is complete or when a material blocker appears before completion.
