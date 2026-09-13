# Lesson 03 — OSINT Agent Risk Matrix for PoC → MVP → Production

Status: `DRAFT_FROM_CURRENT_EVIDENCE`

## Rule

This matrix does not replace the project security threat register. It focuses on delivery/product/AI risks across PoC, MVP and Production. Where an existing project risk already exists, we link conceptually instead of creating a second competing truth.

No numeric probability is invented here. Likelihood/impact remain qualitative until measured evidence exists.

| ID | Stage | Risk | Likelihood | Impact | Early evidence / trigger | Treatment | Owner | State |
|---|---|---|---|---|---|---|---|---|
| L03-R01 | PoC | Transport/library appears viable in a happy-path test but fails on restart/session/rate/error behavior | Medium | High | live PoC shows unstable session/restart or rate behavior | repeatable bounded scenarios; failure injection; compare donor only if decision value remains | Architect + Integration/Transport owner | OPEN |
| L03-R02 | PoC | Test sources/fixtures are too clean and hide real operational constraints | Medium | High | fixture PASS diverges from bounded live-source result | use authorized public test sources; preserve raw metrics/errors; document scope of evidence | QA + Analyst | OPEN |
| L03-R03 | PoC | PoC grows into hidden implementation before decision criteria are met | Medium | High | new features appear without PoC question/evidence link | hard time/scope box; one hypothesis per PoC; GO/PIVOT/STOP gate | PM + Architect | CONTROLLED BY PROCESS |
| L03-R04 | MVP | A technically working collector does not create measurable analyst/user value | Medium | High | usage exists but decisions/tasks are not improved | define one user outcome and baseline; measure task completion/quality rather than collection volume only | Product Owner | OPEN |
| L03-R05 | MVP | Evidence quality/provenance is insufficient for analyst use despite high collection volume | Medium | Critical | human reviewer cannot trace/reproduce material origin | preserve source observations; explicit gaps; review against acceptance/evidence quality criteria | Analyst + QA | PARTLY CONTROLLED |
| L03-R06 | MVP | Legal/privacy scope expands when real users/sources/data are introduced | Medium | Critical | new source/data class appears without applicability review | applicability + data classification + purpose/retention review before MVP expansion | Legal + Data Owner + Security | OPEN |
| L03-R07 | MVP | External AI/provider use leaks or mishandles sensitive project data | Medium | Critical | sensitive payload crosses provider boundary | data-egress policy; provider registry; local/restricted mode; redaction/deny rules | Security + Data Owner | OPEN |
| L03-R08 | Production | Upstream source/API/library changes break collection or silently lose coverage | Medium | High | error/reconciliation/coverage metrics degrade | source isolation, monitoring, reconciliation, version/dependency lifecycle, rollback | Operations + Integration | OPEN |
| L03-R09 | Production | Collection grows unbounded and creates storage/cost/rate-limit problems | Medium | High | backlog/storage/API cost grows beyond assumptions | quotas, bounded backfill, capacity model, archive/retention policy, cost monitoring | Operations + Finance | OPEN |
| L03-R10 | Production | Production acceptance is declared while support/incident/backup/restore ownership is incomplete | Medium | Critical | release checklist has no named owner/evidence | Production readiness gate with named operational owners and recovery evidence | Service Owner + Operations | OPEN |
| L03-R11 | All | Product opportunity or technology fascination diverts the core critical path | Medium | High | parallel MVP/features bypass active milestone gate | WIP limit; MUST/SHOULD/OPTION; opportunity registry separate from core backlog | Product + PM | CONTROLLED |
| L03-R12 | All | Documentation reconstruction creates false certainty about decisions that were never explicitly made | Medium | High | retrospective document contains unsupported owner/metric/decision | FACT / OWNER_CONFIRMATION_REQUIRED / UNKNOWN labels; independent review | KGA + Owners | ACTIVE CONTROL |

## Risk transition rule

A risk may move between stages. Example:

```text
PoC: transport restart uncertainty
        ↓ evidence
MVP: service degradation behavior
        ↓ evidence
Production: SLO + alert + recovery control
```

The risk is not “closed” merely because the project changes stage. Its treatment must evolve with the scope.

## Relationship to existing project risk register

Existing `docs/PROJECT_ROADMAP_AND_CONTROL.md` already identifies technology-first design, Telegram upstream fragility, provenance loss, checkpoint correctness, external-provider privacy/cost, legal scope creep, mock-vs-live evidence, secret leakage and unbounded collection. This Lesson 03 matrix reuses those themes specifically for the staged PoC/MVP/Production delivery view.
