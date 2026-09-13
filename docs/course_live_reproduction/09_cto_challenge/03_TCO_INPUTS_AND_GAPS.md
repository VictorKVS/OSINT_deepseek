# Lesson 09 — TCO Inputs and Evidence Gaps

Status: `MODEL READY / PROJECT NUMBERS TO BE MEASURED`

## Hosted API model

```text
Monthly_API = Requests × ((InputTokens × InputRate) + (OutputTokens × OutputRate)) / rate_unit
            + storage/network/auxiliary services
            + operational support
```

Project inputs required:
- requests/month by capability;
- input/output token distributions;
- model/provider/rate version;
- retry/caching behavior;
- storage/traffic/tool costs;
- support/monitoring cost.

## Cloud GPU self-hosted model

```text
Monthly_Cloud_GPU = GPU_hour_rate × GPU_count × active_hours
                  + storage
                  + network
                  + platform/runtime
                  + operations
```

Inputs:
- model and quantization;
- GPU type/count;
- active/idle hours;
- utilization;
- batching/concurrency;
- storage/network;
- serving/runtime operations effort.

## On-prem model

```text
Monthly_OnPrem = CAPEX / lifetime_months
               + electricity
               + cooling/facility
               + maintenance/spares
               + operations

Electricity = power_kW × hours × electricity_rate × PUE
```

Inputs:
- server/GPU purchase and lifecycle;
- actual power draw;
- utilization;
- facility/PUE assumptions;
- support/maintenance/spares;
- staffing;
- downtime/risk cost where decision-relevant.

## Effective useful GPU-hour

```text
Effective_GPU_Hour = total_monthly_cost / (available_hours × utilization)
```

Low utilization can make owned capacity expensive even when raw hardware amortization appears attractive.

## Break-even

```text
BreakEvenMonths = CAPEX / (monthly_hosted_or_cloud - monthly_onprem_opex)
```

If denominator is <= 0 under comparable quality/SLO, financial break-even does not exist for those assumptions.

## Mandatory quality/SLO normalization

TCO comparison must be run only across alternatives that satisfy the same acceptance envelope:

- project eval/golden set quality;
- groundedness/evidence citation requirements;
- p50/p95 latency;
- throughput/concurrency;
- availability/error rate;
- security/privacy/data-location constraints.

## Current OSINT project gap table

| Input | State |
|---|---|
| production request volume | UNKNOWN |
| input/output token profile | UNKNOWN |
| p95 latency target | UNKNOWN |
| concurrency target | UNKNOWN |
| production availability target | UNKNOWN |
| provider current price/contract | RECHECK_REQUIRED |
| local model candidate | CANDIDATE SET NOT FROZEN |
| same-set quality comparison | NOT MEASURED |
| GPU utilization | NOT MEASURED |
| on-prem CAPEX/current quote | NOT COLLECTED |
| cloud GPU current quote | NOT COLLECTED |
| operations staffing/cost | UNKNOWN |
| allowed data classes for hosted provider | OWNER/LEGAL/DATA DECISION REQUIRED |

## What we can conclude now

We can select an **experiment/reversibility policy** but cannot honestly claim a final three-year cost winner.

The next evidence loop is:

```text
PoC/MVP telemetry
  ↓
requests/tokens/latency/quality/data classes
  ↓
current provider/cloud/hardware quotes
  ↓
comparable TCO scenarios
  ↓
Production hosting ADR revision
```
