# Load, Reliability & Security Tests for GenAI/RAG

Status: `TEST DESIGN / MEASUREMENT PENDING`

## 1. Purpose

Semantic quality is insufficient if the route is unsafe, unstable or too slow/costly for the intended operating mode.

This document defines non-functional evaluation for RAG/LLM paths.

## 2. Load model

Until Production workload is measured, the test harness should parameterize rather than invent:

- concurrent users/requests;
- request rate;
- input context size;
- output token budget;
- retrieval K;
- document/chunk corpus size;
- embedding/index size;
- model/provider route;
- timeout/retry policy.

Initial values are `TO_BE_BASELINED` from telemetry and Product/Ops requirements.

## 3. Performance metrics

Capture:

- p50 / p95 / p99 end-to-end latency;
- retrieval latency separately from generation;
- first-token latency where available;
- tokens/sec / requests/sec;
- queue/wait time;
- timeout rate;
- retry rate;
- saturation indicators;
- provider/rate-limit responses;
- local GPU utilization/VRAM when applicable;
- cost/query and cost/accepted answer.

## 4. Reliability scenarios

Test or simulate:

- model/provider timeout;
- retrieval/index unavailable;
- partial source/index failure;
- rate limit / quota exhaustion;
- malformed model output;
- judge/evaluator unavailable;
- retry storm prevention;
- fallback route behavior;
- cancellation and bounded execution;
- stale index/dataset detection.

Expected behavior must prefer explicit degradation/UNKNOWN over silent fabricated success.

## 5. Security / adversarial corpus

Include cases for:

- direct prompt injection;
- indirect prompt injection inside retrieved content;
- malicious instructions in Telegram/web/PDF sources;
- retrieval poisoning;
- fabricated citation/ref IDs;
- attempts to expose secrets/system prompts;
- tool escalation outside allowlist;
- cross-agent privilege escalation;
- data-class policy violation / prohibited external processing;
- malicious oversized input/resource exhaustion.

## 6. Security pass rule

Critical security behavior is not averaged with answer quality.

Examples of hard failure:

```text
retrieved text changes system/tool policy
unapproved data is sent to external provider
tool call exceeds delegated privilege
fabricated execution result is treated as evidence
secret appears in model/output/log
```

## 7. Chaos / dependency behavior

For Production candidates, inject controlled failures where practical:

- one retriever unavailable;
- provider unavailable;
- queue/backlog growth;
- storage/index temporarily unavailable;
- delayed/stale data;
- model route fallback.

Verify that provenance, audit trail and bounded execution survive failure.

## 8. Cost guardrails

Track both technical and economic failure modes:

- runaway loops;
- unexpectedly large contexts;
- high retry amplification;
- expensive judge cascades;
- unnecessary full Model Zoo execution for routine tasks;
- low cache/index reuse;
- cost increase without quality gain.

## 9. Current status

The security threat register already identifies prompt injection, RAG poisoning, excessive agency, runaway loops and provider/data risks. Lesson 13 converts those concerns into candidate evaluation cases.

Measured load/cost/security results remain `TO_BE_MEASURED`.
