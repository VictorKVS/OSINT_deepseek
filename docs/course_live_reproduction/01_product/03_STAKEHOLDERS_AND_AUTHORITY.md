# Lesson 01 / Product — Stakeholders and Decision Authority

Status: `DRAFT_FROM_CURRENT_EVIDENCE / RETROSPECTIVE_RECONSTRUCTION`

## Stakeholder map

| Stakeholder / role | Interest | Authority / responsibility | Evidence status |
|---|---|---|---|
| Project Owner | business/product direction | confirms scope, priorities and product intent | OWNER_CONFIRMATION_REQUIRED |
| Product / Requester | obtains reusable research capability | defines business outcome and product priorities | PARTLY_EVIDENCED |
| Analyst | consumes evidence and creates analysis | owns interpretation, not raw collection | FACT_FROM_EXISTING_REPO |
| OSINT Agent | collects/preserves materials | owns bounded collection workflow | FACT_FROM_EXISTING_REPO |
| Collector | acquires one source class | cannot perform cross-domain analysis | FACT_FROM_EXISTING_REPO |
| Socrates / Reviewer | challenges sufficiency | may PASS or request bounded additional research | FACT_FROM_EXISTING_REPO |
| Security Engineer | security constraints and threat/supply-chain review | does not accept residual business risk | PARTLY_EVIDENCED |
| Operations / DevOps | production operation, monitoring, access and recovery | operational controls and platform constraints | PARTLY_EVIDENCED |
| Legal / Compliance | lawful collection/use constraints | owns legal applicability conclusions | GAP / TO FORMALIZE |
| Data Owner | classification and allowed handling | owns data handling decisions | GAP / TO FORMALIZE |
| Knowledge Gate | future publication control | cannot replace Analyst/Socrates reasoning | FUTURE_DECISION |

## Decision authority rules

```text
Business/product scope            → Project Owner / Product
Interpretation of evidence        → Analyst
Evidence sufficiency challenge    → Socrates / Reviewer
Security constraints              → Security role
Legal applicability               → Legal/Compliance
Data classification/handling      → Data Owner
Residual risk acceptance          → designated Risk Owner / business authority
Architecture decision             → Architecture process + independent review
```

No technical component, LLM or agent may silently replace these authorities.

## Open questions

- Named product owner for the production/commercial track — `OWNER_CONFIRMATION_REQUIRED`.
- Named legal/compliance authority for live-source collection — `UNKNOWN`.
- Named data owner for production evidence stores — `UNKNOWN`.
- Residual-risk acceptance authority for production — `UNKNOWN`.

## Evidence

- `docs/03_architecture/01_BUSINESS_ANALYSIS.md` — current actors and responsibilities;
- `README.md` — current lifecycle and operations role direction;
- `docs/OPERATIONS_GOVERNANCE_MODEL.md` — production separation-of-duty intent.
