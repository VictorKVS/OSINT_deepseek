# Architecture Review Checklist for Material PR / Change

Status: `CANDIDATE CHECKLIST`

Use this checklist only for material changes. A short review is preferred over ceremonial approval.

## 1. Change intent

- [ ] Requirement/capability/defect/risk driving the change is linked.
- [ ] Scope and exclusions are explicit.
- [ ] Author identifies affected components/contracts/data flows.
- [ ] Simpler existing mechanism was considered.

## 2. Architecture

- [ ] C1/C2/C3 responsibility boundaries remain correct or are updated.
- [ ] New coupling/dependency is intentional.
- [ ] No source-specific detail leaks into source-neutral contracts without justification.
- [ ] Material alternative(s) were considered.
- [ ] ADR is linked if the decision is costly/risky to reverse.

## 3. Data & provenance

- [ ] Source observation identity is preserved.
- [ ] Raw/original evidence is not silently replaced by a derivative.
- [ ] Schema/version changes have compatibility/migration treatment.
- [ ] Data classification/retention/external-processing impact is reviewed when applicable.

## 4. Security & supply chain

- [ ] New trust boundary / network egress / credential / privileged tool is identified.
- [ ] New dependency/provider/donor has lifecycle/license/security review.
- [ ] Sensitive content is not routed to an unapproved external model/service.
- [ ] Failure path does not leak secrets/session data.

## 5. Reliability & operations

- [ ] Timeout/retry/idempotency/restart behavior is explicit where applicable.
- [ ] Failure of one source/dependency is isolated where required.
- [ ] Rollback/disable path is known for baseline-affecting changes.
- [ ] Logs/metrics/audit evidence needed to operate the change is defined.

## 6. Verification

- [ ] Acceptance/regression tests cover observable contract changes.
- [ ] Negative/failure cases are included where material.
- [ ] Security checks required by the changed surface are identified.
- [ ] Documentation/traceability changes are part of Done.

## Review result template

```text
Change / PR:
Materiality: LOW / MEDIUM / HIGH
Architecture result: PASS / PASS_WITH_CONDITIONS / REWORK / ADR_REQUIRED / DEBT_ACCEPTANCE_REQUIRED / BLOCKED
Findings:
- ...
Required evidence:
- ...
Debt created/changed:
- DEBT-* / NONE
ADR impact:
- ADR-* / NONE
Reviewer:
Decision date:
```

## Model Zoo use

Routine changes do not need the full model zoo. Material architecture changes may use Champion + challengers + independent judge as an advisory challenge layer, with dissent retained. Final approval remains human/role-bound.