# Lesson 11 — Integration Architecture: Classic Patterns → AI Standards

Status: `DOCUMENTATION LAYER / CURRENT + CANDIDATE INTEGRATIONS SEPARATED`

OTUS Lesson 11 covers protocol/pattern selection (HTTP, gRPC, broker, ETL), resilient asynchronous integration and modern AI integration approaches such as MCP/A2A, with ONNX as a model-portability concern.

For OSINT Agent the lesson preserves the current simple DEV architecture and adds a **conditional Production integration model** only where scale/reliability/decoupling requirements justify it.

## Artifacts

- `01_INTEGRATION_LANDSCAPE.md` — current and future boundaries, owners and contracts.
- `02_RELIABLE_ASYNC_INTEGRATION_CANDIDATE.md` — broker-based candidate for long-running/unreliable integration; not current implementation.
- `03_AI_INTEGRATION_STANDARDS_APPLICABILITY.md` — HTTP/gRPC/Broker/ETL/MCP/A2A/ONNX applicability.
- `04_LESSON_11_REVIEW.md` — result, UNKNOWNs and improvements.

## Core principle

```text
choose integration by interaction semantics
≠
choose technology because it is fashionable
```

Current DEV remains direct/in-process where that is the smallest mechanism proving the contract. A broker is introduced only if durability, independent scaling, replay, backpressure or failure isolation becomes a real requirement.
