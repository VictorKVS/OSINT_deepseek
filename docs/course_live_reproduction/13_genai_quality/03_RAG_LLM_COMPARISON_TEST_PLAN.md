# RAG / LLM Comparison Test Plan

Status: `READY FOR EXECUTION DESIGN / RESULTS NOT YET MEASURED`

## 1. Objective

Compare two model routes on the same RAG task without changing the evidence set, retrieval conditions or acceptance rubric between candidates.

The comparison answers:

> Which route gives the strongest evidence-grounded result at acceptable latency, reliability, security and cost?

## 2. Candidate routes

Use generic labels until actual approved candidates are selected:

- `MODEL_A` — candidate A;
- `MODEL_B` — candidate B.

Possible future mapping: hosted model vs local/self-hosted model, or two hosted/local candidates.

No winner is declared before execution.

## 3. Fixed test conditions

Both candidates receive:

- the same dataset version;
- the same question/task;
- the same retrieved evidence context;
- the same source/evidence refs;
- the same output schema;
- the same security/tool policy;
- equivalent generation parameters where comparable;
- the same timeout/retry policy where possible.

If retrieval itself is also under comparison, run a separate experiment so retrieval and generation effects are not conflated.

## 4. Test matrix

| Layer | Metric / evidence | Direction |
|---|---|---|
| Retrieval | expected evidence recall/coverage | higher is better |
| Faithfulness | supported claims / unsupported claims | higher/lower |
| Answer relevance | rubric or automated metric | higher |
| Completeness | required fact/evidence coverage | higher |
| Citation quality | resolvable citation rate | higher |
| Correct UNKNOWN | false certainty on missing evidence | lower |
| Security | prompt-injection/tool-policy violations | zero critical violations |
| Latency | p50 / p95 / p99 | lower subject to quality |
| Reliability | timeout/error rate | lower |
| Cost | cost/query, cost/accepted case | lower subject to quality |
| Stability | repeated-run disagreement/variance | lower where determinism expected |

## 5. Critical gate cases

The following cases are hard gates rather than average-score trade-offs:

- fabricated source/citation;
- unsupported high-impact factual claim;
- untrusted retrieved text changing system/tool policy;
- prohibited external processing/data leak;
- tool execution outside allowlist;
- failure to return `UNKNOWN` when required by the case;
- unresolved evidence ref for a material claim.

A candidate with a critical gate violation cannot win on cost/latency alone.

## 6. Execution rounds

### Round A — calibration

Small reviewed subset to validate metric/rubric behavior.

### Round B — regression dataset

Full versioned regression set.

### Round C — adversarial/security

Prompt injection, retrieval poisoning, citation manipulation, conflicting evidence.

### Round D — load/operational

Representative request sizes/concurrency; capture latency, timeout, throughput and cost.

### Round E — independent review

Blind review of material disagreements and close scores.

## 7. Repetitions

For non-deterministic candidates, run repeated samples per selected case when variance materially affects the decision. Record seed/settings where the provider/runtime exposes them.

Do not average away catastrophic failures: retain per-case failure records.

## 8. Comparison result object

```text
comparison_id
candidate_A_model/version
candidate_B_model/version
dataset_version
retrieval_version
prompt/policy_version
metric/rubric_versions
quality_results
security_results
latency_throughput_results
cost_results
dissent_or_close_cases
winner_by_dimension
recommended_route
conditions
revisit_triggers
reviewer
```

## 9. Decision rule

Preferred route must:

1. pass all hard safety/evidence gates;
2. meet the minimum quality threshold;
3. meet required operational NFRs;
4. then optimize cost/latency/maintainability among acceptable routes.

## 10. Current state

`MODEL_A`, `MODEL_B`, thresholds and measured results remain `TO_BE_BASELINED`.

This is intentional: the Test Plan is complete enough to run once the owner approves candidates, dataset and thresholds.
