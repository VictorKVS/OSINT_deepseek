# Lesson 05 — Review / LLD

Status: `CONDITIONAL_PASS`

## Added

- C3 decomposition of Research Orchestration;
- current component responsibilities;
- sequence diagrams for success/failure/reuse/follow-up;
- candidate external OpenAPI adapter explicitly marked NOT IMPLEMENTED;
- component-level security notes and open LLD questions.

## Important AS-IS rule

The canonical current interface is Python/domain-contract based:

`ResearchTask -> OSINTAgent/Collector/MaterialStore -> MaterialPackage`

The OpenAPI document is a future adapter candidate only.

## UNKNOWN / future design

- async job execution semantics;
- API authentication/authorization;
- idempotency and replay protection;
- artifact download/reference mechanism replacing local filesystem paths;
- pagination/streaming for large packages;
- API schema version negotiation;
- production queue/storage topology.

## Improvement Review

| Priority | Improvement | Target |
|---|---|---|
| P1 | define stable versioned domain schema independent of Python classes | Lessons 5/11/12 |
| P1 | decide whether an external API is actually required before implementing one | Product/Integration gate |
| P0 | never expose raw local paths/secrets through a future network API | before any API implementation |
| P1 | add idempotency/auth/task ownership if remote submission becomes in-scope | Lessons 11/14 |
| P2 | generate sequence/C3 diagrams from canonical architecture source later | Lesson 10/site pass |

## Gate

`LLD_READY = CONDITIONAL_PASS`

Current DEV component semantics are explicit. Network-service design remains intentionally candidate/future.
