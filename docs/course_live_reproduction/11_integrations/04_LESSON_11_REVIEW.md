# Lesson 11 — Review

Status: `DOCUMENTATION_LAYER_COMPLETE / PRODUCTION INTEGRATION PATTERNS REMAIN CANDIDATE`

## What Lesson 11 added

- explicit integration landscape around stable OSINT contracts;
- separation of current DEV direct calls from future external/service adapters;
- broker-based reliable asynchronous candidate with retry/DLQ/idempotency/backpressure rules;
- applicability view for HTTP, gRPC, Message Broker, ETL/ELT, MCP, A2A and ONNX;
- failure ownership and security requirements for every integration boundary.

## What is already evidenced

Current Telegram acquisition already demonstrates a useful integration principle: `TelegramCollector` depends on a transport-neutral `TelegramTransport` protocol, so transport choice can change without changing the collector/Analyst contract.

## What is deliberately not claimed

- no production message broker is implemented;
- no public HTTP/gRPC OSINT service is claimed;
- MCP/A2A are not current runtime dependencies;
- ONNX is not selected as a mandatory model format;
- no service mesh is required by the current project.

## Gate interpretation

```text
CURRENT_DEV_INTEGRATIONS = VERIFIED_ENOUGH_FOR_DEV
PRODUCTION_ASYNC_PATTERN = CANDIDATE
AI_PROTOCOLS = CONDITIONAL_BY_USE_CASE
```

## UNKNOWN / evidence needed later

- real task duration/distribution;
- required concurrency/worker count;
- retry/replay/backlog SLO;
- external consumer requirements;
- broker retention/security/compliance constraints;
- whether independent agent services create real MCP/A2A value.

## Improvement Review

| Priority | Improvement | Target |
|---|---|---|
| P1 | Define production integration NFR: timeout/retry/backlog/replay/idempotency | 11–16 |
| P1 | Add versioned event/message schemas if async path is promoted | 11–18 |
| P1 | Add contract tests for transport adapters and compatibility | 11–18 |
| P1 | Perform broker/API technology ADR only after load/reliability requirements exist | 11–17 |
| P0 | Keep auth/data policy/privilege context across MCP/A2A/tool boundaries | before executable agent integration |

## Result

`LESSON_11_INTEGRATION_ARCHITECTURE = CONDITIONAL_PASS`

The project now has a defendable integration strategy without inventing infrastructure before requirements.