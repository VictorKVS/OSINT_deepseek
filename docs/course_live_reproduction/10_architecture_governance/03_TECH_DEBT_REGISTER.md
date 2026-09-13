# Technical Debt Register — Current OSINT Project

Status: `ACTIVE CANDIDATE REGISTER / CURRENT COMPROMISES ONLY`

This register intentionally excludes defects already fixed, missing future features and generic risks.

## Register

| ID | Current compromise | Why acceptable now | Consequence if kept indefinitely | Repayment trigger | Simplest repayment path | State |
|---|---|---|---|---|---|---|
| DEBT-001 | DEV evidence persistence is local append-only JSONL + content-addressed files | deterministic, inspectable, minimal dependency baseline | weak multi-process concurrency/querying/transaction/recovery capabilities at scale | first requirement for concurrent workers, durable distributed queueing, production retention/query SLA | select production metadata/payload stores from measured requirements; migrate via versioned export/import | ACCEPTED_DEV |
| DEBT-002 | `SimpleAnalyst` / simple review components remain DEV harnesses in the same repository as OSINT core | proves handoffs and bounded loop without premature LLM complexity | future maintainers may mistake harness behavior for expert-quality analysis | production semantic Analyst/Reviewer requirement becomes approved | move/replace behind explicit Analyst/Reviewer interfaces and retain deterministic harness for tests | ACCEPTED_DEV |
| DEBT-003 | Architecture diagrams and course views are primarily Markdown/Mermaid and manually synchronized with code/docs | low-cost, reviewable documentation during rapid design learning | drift risk grows as components/interfaces change | repeated divergence finding or first Production architecture baseline | introduce architecture-as-code/generated views and conformance checks from canonical model/schema | OPEN |
| DEBT-004 | Cross-repository OTUS mirror duplicates selected project explanations | needed for course submission while project truth stays in OSINT repo | duplicated prose can drift from source of truth | course automation/runtime becomes available or divergence appears | generate lesson mirror from canonical project metadata/review artifacts | OPEN |

## Not debt

The following are **not** classified as technical debt at this stage:

- missing Production Legal/Data policy — this is a governance/readiness gap and can be a blocker;
- missing Production SLO/TCO — this is missing evidence/baseline;
- candidate RAG/agent implementation — future capability, not debt;
- candidate HTTP API — future adapter, not debt;
- security threats — tracked in the security/threat register;
- a contract violation — defect, not debt.

## Debt lifecycle

```text
IDENTIFIED
  ↓
CLASSIFIED AS DEBT (not defect/risk/feature)
  ↓
OWNER + WHY ACCEPTABLE NOW
  ↓
TRIGGER + CONSEQUENCE
  ↓
REVIEW AT CHANGE / MILESTONE FREEZE
  ↓
REPAY / CONTINUE ACCEPTANCE / SUPERSEDE
  ↓
EVIDENCE OF CLOSURE
```

Debt is not automatically scheduled because it exists. It becomes active work when its trigger is met or its carrying cost materially changes.