# Lesson 09 — Hosted API vs Self-Hosted LLM Trade-off

Status: `QUALITATIVE UNTIL MEASURED TCO/QUALITY DATA EXISTS`

## Options

- **A — Hosted SaaS/API**: provider-hosted proprietary/managed model.
- **B — Cloud GPU self-hosted**: project operates an open model on rented GPU.
- **C — On-prem self-hosted**: project owns/operates GPU infrastructure.
- **D — Hybrid**: internal gateway routes approved workloads across hosted/local options.

## Current-stage trade-off matrix

| Criterion | A Hosted API | B Cloud GPU | C On-prem | D Hybrid |
|---|---|---|---|---|
| Initial delivery speed | strongest | medium | weakest | medium |
| Initial CAPEX | low | low | high | depends |
| Ops burden | low/medium | high | highest | highest coordination burden |
| Data control | weakest unless data is approved/sanitized | stronger | strongest local control | policy-dependent |
| Vendor/provider lock-in | high if API leaks into business logic | model/cloud lock-in | hardware/runtime lock-in | lower if gateway discipline is real |
| Scaling during uncertain PoC | strong | requires capacity mgmt | constrained by owned capacity | strong but complex |
| Predictable unit cost at high stable load | unknown until measured | potentially better | potentially better with high utilization | depends |
| Quality access | often strong frontier models | depends on chosen model/GPU | depends on chosen model/GPU | can choose per task |
| Latency | network/provider dependent | network + own serving | local network + own serving | routing dependent |
| Availability dependency | provider | cloud + serving stack | internal infra/team | multiple dependencies |
| Security/privacy | requires external-processing approval | cloud control still required | highest physical/data control potential | policy/routing complexity |
| Reversibility at current stage | high if interface is abstracted | medium | lower after hardware purchase | medium/high |

## Current interpretation

At the current project stage, exact financial ranking is `UNKNOWN` because workload, token mix, quality equivalence, utilization, staffing and current prices are not established.

However, the **reversibility / learning** dimension is not unknown: a provider-neutral hosted API can gather real workload/quality telemetry without committing to hardware, provided sensitive/unclassified evidence is blocked from external processing.

## Architecture choice vs procurement choice

The current ADR selects a **policy/interface strategy**, not a permanent vendor or procurement contract:

```text
Project semantic capability
        ↓
Model Gateway / policy boundary
        ├─ hosted provider (approved data only)
        └─ local/self-hosted provider (future/approved)
```

## Fair-comparison rule

No local/self-hosted option may be declared cheaper/better unless it meets the same project quality and SLO gate as the hosted option. Likewise hosted API cannot win on quality if privacy/legal constraints make its data path impermissible.

## Revisit triggers

- external processing becomes prohibited for required data;
- hosted cost exceeds measured self-hosted TCO by approved threshold;
- p95/availability misses SLO;
- local model reaches required quality on common eval set;
- stable utilization makes GPU economics credible;
- geopolitical/vendor/retention/terms change;
- production use case requires offline/local operation.
