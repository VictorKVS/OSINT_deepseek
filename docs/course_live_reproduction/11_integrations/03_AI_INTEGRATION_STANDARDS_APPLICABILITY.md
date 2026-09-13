# AI Integration Standards Applicability

Status: `CANDIDATE APPLICABILITY VIEW`

This document separates **interaction protocols/patterns** from **model portability formats** and avoids choosing a standard without a use case.

## Applicability matrix

| Mechanism | Best fit | OSINT project use | Current state |
|---|---|---|---|
| HTTP/REST | external request/response APIs, broad interoperability | candidate Analyst→OSINT or status/result API | CANDIDATE |
| gRPC | typed low-latency service-to-service communication | candidate internal service boundary if service split appears | CANDIDATE |
| Message Broker | durable async work, buffering, fan-out, retry/replay | candidate Production task/result path | CANDIDATE |
| ETL/ELT | batch/history synchronization, dataset preparation | relevant for backfill, source imports and AI data pipeline | CANDIDATE / LESSON 12 |
| MCP | controlled exposure of tools/resources to model/agent runtimes | candidate tool boundary for future agents | FUTURE / SECURITY GATED |
| A2A | agent-to-agent task/coordination between separately deployed agents | candidate only if agents become independent services | FUTURE |
| ONNX | portable model artifact/runtime representation | possible local inference portability concern; not a message transport | CONDITIONAL |

## MCP applicability

MCP becomes relevant if an Analyst/agent needs to access approved tools/resources through a standardized boundary. It does **not** replace:

- server-side authorization;
- data classification/egress policy;
- tool allowlists;
- task scope propagation;
- audit;
- human approval for high-impact actions.

For current OSINT DEV, direct Python contracts remain simpler.

## A2A applicability

A2A becomes relevant if OSINT, Analyst, Reviewer or other agents are independently deployed and need explicit task delegation/status/result exchange. Current in-process DEV harnesses do not need an inter-agent network protocol.

Required properties before A2A adoption:

- stable agent identity;
- explicit task/trace IDs;
- privilege ceiling propagation;
- capability advertisement without implicit authorization;
- bounded retries/timeouts;
- signed/auditable result identity where justified.

## ONNX applicability

ONNX is treated here as a **model portability/deployment format**, not as the integration bus between business systems. It could become useful if local model inference needs runtime portability or vendor-neutral packaging. Its value must be evaluated against actual model/runtime support and quality/performance evidence.

## Selection rule

```text
interaction need
→ reliability/security/data constraints
→ simplest adequate pattern
→ protocol/technology
```

Not:

```text
interesting technology
→ invent a reason to use it
```

## Architecture implication

All future adapters must preserve the stable semantic contracts (`ResearchTask`, evidence/material identity, `MaterialPackage`, review/gate semantics) even if the transport changes.