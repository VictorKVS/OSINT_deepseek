# Lesson 01 / Product — Business Need

Status: `DRAFT_FROM_CURRENT_EVIDENCE / RETROSPECTIVE_RECONSTRUCTION`

## Problem

`FACT_FROM_EXISTING_REPO`

Repeated technology/security research is expensive and inconsistent when every project or role agent rediscovers the same material from scratch. Existing project documentation states that the system should preserve research materials so later analysts and FATHER roles can reuse evidence with known provenance.

## Opportunity

Create a bounded OSINT research supplier that separates **collection/preservation of evidence** from **analysis/truth decisions**.

## Expected business effect

- reduce repeated source-discovery work;
- preserve provenance and collection history;
- make gaps/errors visible instead of silently losing them;
- support reuse of raw material across later analyses;
- keep research bounded by task/cycle/item limits;
- enable future product assemblies over one verified research core.

## Problem statement

```text
Current state:
project/expert needs evidence
→ ad-hoc search
→ local/unstructured materials
→ provenance may be lost
→ later project repeats search

Target state:
project/expert need
→ ResearchTask
→ OSINT collection
→ provenance-preserving MaterialPackage
→ Analyst / review
→ reusable evidence
```

## Non-goals

The OSINT Agent is not intended to:

- decide final truth;
- autonomously publish knowledge;
- replace analyst judgment;
- perform unauthorized access or collection;
- hide missing evidence;
- create unbounded autonomous research loops.

## Evidence

Canonical project evidence:

- `README.md` — Mission, engineering lifecycle and product direction;
- `docs/03_architecture/01_BUSINESS_ANALYSIS.md` — business objective, boundaries and value stream;
- `docs/OSINT_AGENT_TZ_V1.md` — purpose, process position, inputs/outputs and acceptance criteria.

## Open owner confirmations

`OWNER_CONFIRMATION_REQUIRED`

- target economic effect (hours/cost saved per investigation);
- primary first commercial user segment;
- whether the first production release is internal FATHER-only or also externally packaged;
- explicit business KPI baseline.

These remain open and must not be replaced by invented percentages.
