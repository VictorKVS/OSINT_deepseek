# Lesson 09 — LLM Hosting Drivers

Status: `CURRENT DECISION INPUT`

## Drivers

| ID | Driver | Current evidence/state | Decision impact |
|---|---|---|---|
| HD-01 | preserve evidence privacy/classification boundary | external AI service receiving sensitive evidence is a registered Critical-impact threat | external provider use must be data-classification gated |
| HD-02 | fast evidence-producing PoC/MVP without premature CAPEX | current project is still PoC/MVP-design stage for semantic/agent capabilities | hosted API reduces infrastructure commitment during learning |
| HD-03 | provider/model replaceability | current model-stage registry defines capabilities/champion/challenger rather than one permanent provider | use provider-neutral Model Gateway/adapter boundary |
| HD-04 | same quality gate across options | model output never replaces source evidence; semantic stages require review | compare candidates on same eval set, evidence/citation requirements and review outcome |
| HD-05 | no invented TCO | production workload, token profile, concurrency and SLO are not yet baselined | no hardware purchase justified by speculative break-even |
| HD-06 | operational simplicity at current stage | self-hosted production introduces GPU/runtime/patching/monitoring capacity work | avoid production infra before evidence justifies it |
| HD-07 | local/self-hosted escape path | privacy, provider policy, regional availability or cost can invalidate hosted API | keep interface and data contracts portable; define migration triggers |
| HD-08 | untrusted evidence must not gain tool/policy authority | agent/security threat model | provider choice cannot weaken untrusted-content and tool policy boundaries |
| HD-09 | model/provider updates must be traceable | security threat register and model registry | log model/provider/version and rerun eval/security checks |
| HD-10 | production legal/data authority remains open | lesson 1–3 UNKNOWN | external processing remains conditional; Production approval blocked until owner/legal/data decisions exist |

## Hard constraints for current decision

1. No sensitive/unclassified evidence to external API by default.
2. Provider/model version must be recorded in evaluation/telemetry.
3. Generated output must retain/resolve source evidence refs where the use case requires grounded claims.
4. Hosted provider must be replaceable through a stable internal capability boundary.
5. Production workload/SLO/TCO must be measured before irreversible infrastructure commitment.
6. A provider change is a material model/supply-chain change and triggers evaluation/security review.

## UNKNOWNs

- monthly production requests/tokens;
- peak concurrency;
- target p95 latency/availability;
- external-processing allowed data classes;
- current provider prices/contracts/regions;
- comparable local model quality on project eval set;
- local GPU utilization achievable in operation;
- operations staffing/cost;
- first production semantic use case.

These UNKNOWNs are decision inputs to collect, not numbers to invent.
