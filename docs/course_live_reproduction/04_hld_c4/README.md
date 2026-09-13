# Lesson 04 — HLD / C4 Pack for FATHER OSINT Agent

Status: `DOCUMENTATION_NORMALIZATION / CURRENT + FUTURE BOUNDARIES`

## Purpose

Normalize the existing OSINT Agent architecture into a C4-oriented high-level design without inventing infrastructure that is not part of the current DEV baseline.

Lesson 04 requires C1 System Context and C2 Containers. This pack additionally records architecture drivers, trust/responsibility boundaries, evidence flow and open decisions so the diagrams are traceable rather than decorative.

## Source basis

Canonical current evidence:

- `README.md`;
- `docs/OSINT_AGENT_TZ_V1.md`;
- `docs/03_architecture/01_BUSINESS_ANALYSIS.md`;
- `docs/03_architecture/02_ARCHITECTURE_VIEWS.md`;
- `docs/03_architecture/04_DECISION_REGISTER.md`;
- `father_osint/agent.py`;
- `father_osint/models.py`.

## HLD rule

```text
business / research need
  ↓
roles and boundaries
  ↓
logical containers / responsibilities
  ↓
interfaces / information flow
  ↓
quality + security drivers
  ↓
architecture questions
```

No DB engine, queue, LLM provider, Kubernetes platform or external SaaS is approved merely because it is a common implementation choice.

## Current C4 levels

| C4 level | Current project interpretation | Status |
|---|---|---|
| C1 Context | Requester/Analyst → OSINT Worker → Analyst/Socrates → future Knowledge Gate | CURRENT / VERIFIED BY DOCS |
| C2 Containers | Acquisition, orchestration, evidence persistence, analysis/review boundaries | CURRENT LOGICAL / DEPLOYMENT-NEUTRAL |
| C3 Components | `OSINTAgent`, collectors, models, store, analyst/reviewer harness | Lesson 05 |
| Code | Python implementation | existing baseline; not modified by course docs |

## Architectural invariants carried forward

1. OSINT collects and preserves evidence; it does not decide final truth.
2. `ResearchTask` is the bounded order into research.
3. `MaterialPackage` is the evidence delivery unit.
4. Provenance/observation identity must survive storage optimization.
5. Collector failures remain visible and isolated.
6. Research loops are bounded.
7. DEV and Production are distinct scopes.
8. Technology choice follows evidence/ADR, not repository accident.

## HLD gate

`HLD_READY` may be `PASS` only when:

- C1 has all material actors/external systems;
- C2 gives one clear responsibility to each logical container;
- interfaces are named and directional;
- data/trust boundaries are visible;
- current vs future scope is marked;
- significant unknowns are listed;
- no technology candidate is silently promoted to architecture fact.

Current result: `CONDITIONAL_PASS` — C1/C2 are coherent for DEV, while Production deployment, LLM hosting, data governance and operational SLO remain open for later lessons.
