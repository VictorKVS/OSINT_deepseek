# Lesson 02 — Review / Delivery Feasibility

Status: `CONDITIONAL_PASS / DOCUMENTATION`

## Added to real OSINT project

- project-specific NFR baseline/gaps;
- WBS v0 mapped to current M5→M8 roadmap;
- estimate-method contract without invented hours;
- project/security-risk crosswalk;
- TCO input model;
- Change Request structure;
- evaluation/golden-set requirements.

## Strong existing controls reused

- capability/evidence roadmap;
- MUST/SHOULD/OPTION priorities;
- PoC/ADR gates;
- project and security risk registers;
- Definition of Ready/Done;
- change-impact analysis;
- traceability and DEV baseline freeze.

## Remaining gaps

- owner-confirmed production NFR targets;
- measured team delivery capacity / numeric estimates;
- production budget envelope;
- production workload/token/concurrency profile;
- current provider/cloud/hardware quotes;
- evaluation-set ownership and first version.

## Improvement Review

| Priority | Improvement | Target |
|---|---|---|
| P1 | baseline production NFRs with Product/Ops/QA | Lessons 3–16 |
| P1 | collect estimate inputs for active M5 work rather than invent date | project planning |
| P1 | connect risk IDs across registers and WBS/ADR | Lessons 2–10 |
| P1 | instantiate Change Request on next material scope change | next material change |
| P1 | create first versioned eval/golden set before RAG/LLM selection | Lessons 6/9/13 |

## Gate

`DELIVERY_FEASIBILITY_READY = CONDITIONAL_PASS FOR CURRENT DOCUMENTATION`.

The project is structurally estimable, but final schedule/cost/Production capacity is not yet evidenced.
