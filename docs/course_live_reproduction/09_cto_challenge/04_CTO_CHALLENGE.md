# Lesson 09 — CTO Challenge / Defense Notes

Status: `READY FOR COURSE REVIEW`

## One-paragraph CTO pitch

For the current OSINT/Knowledge Factory PoC/MVP stage, a hosted LLM API behind a replaceable Model Gateway is the least-commitment way to measure whether semantic/RAG/agent capabilities create enough value and quality to justify permanent infrastructure. We explicitly do **not** send sensitive or unclassified evidence to an external provider; that path is policy-blocked until Data/Legal/Security approve it. We also do not claim hosted API is the cheapest Production solution: production workload, quality equivalence, concurrency, GPU utilization and current prices are still unknown. The decision is therefore to buy learning and reversibility now, collect comparable telemetry, and trigger a superseding ADR when privacy, SLO or measured TCO supports self-hosted/cloud-GPU/on-prem operation.

## Challenger questions and responses

### 1. Why not self-host immediately and keep all data private?

Because current workload/model-quality/ops-cost evidence is insufficient to justify hardware/runtime commitment. Privacy is handled by failing closed for sensitive/unclassified evidence. Self-hosting remains a required comparison path when the production use case is known.

### 2. Hosted API creates vendor lock-in. Why accept that?

The decision requires a provider-neutral capability/gateway boundary and prohibits provider-specific structures from becoming domain contracts. Model/provider/version are telemetry and supply-chain items. Lock-in risk remains real and is a revisit trigger.

### 3. How can you choose without TCO numbers?

We are not choosing a permanent Production cost winner. We are choosing the current **experiment strategy**. TCO inputs are explicitly listed as gaps; final Production hosting must be decided with measured requests/tokens/concurrency/quality/SLO/utilization/ops and current quotes.

### 4. What if the hosted model is better than local forever?

Then quality evidence may continue to justify hosted use for approved data. Privacy/legal/offline requirements can still force local operation. Architecture decision remains multidimensional, not quality-only.

### 5. What if local model is cheaper?

Cheaper is relevant only if it passes the same quality and SLO envelope. Once comparable local quality and stable utilization exist, TCO is recalculated and ADR revisited.

### 6. What prevents evidence leakage?

External model use is not a default data path. Data classification/policy gate decides whether evidence may leave the boundary; secrets remain outside prompts; provider/model/version are logged; prohibited data produces blocked/local/unresolved outcome.

### 7. Why not hybrid from day one?

The gateway keeps hybrid optionality, but running two production inference stacks before a use case proves need increases complexity. The architecture keeps the seam; operations complexity is added only when evidence justifies it.

### 8. How will the decision be verified?

Collect common-set quality, evidence/citation correctness, latency, error/availability, requests/tokens/cost, security findings and reviewer rework. Compare future options on the same acceptance envelope.

## ATAM-style sensitivity/trade-off notes

| Driver | Sensitive architectural choice | Trade-off |
|---|---|---|
| privacy/data control | external vs local model path | external speed vs data-control restriction |
| delivery speed | hosted API vs operating inference stack | rapid learning vs provider dependency |
| cost | token/API vs GPU+ops | variable spend vs utilization/CAPEX/ops |
| quality | frontier hosted vs selected local model | quality access vs control/cost |
| latency | network provider vs local serving | provider/network variability vs local capacity tuning |
| maintainability | managed API vs self-managed stack | provider dependency vs internal ops burden |
| evolvability | gateway abstraction | extra interface discipline vs backend replaceability |

## Failure modes that would overturn approval

- external path cannot reliably enforce data classification;
- domain/business logic becomes provider-specific;
- no telemetry exists to support future TCO/review;
- evaluation cannot compare quality across candidates;
- hosted provider terms make required data processing impermissible;
- security review finds unacceptable data/credential leakage.

## Challenge outcome

`ACCEPT WITH CONDITIONS FOR CURRENT PoC/MVP STAGE`

Production hosting remains unapproved until a later evidence-based gate.
