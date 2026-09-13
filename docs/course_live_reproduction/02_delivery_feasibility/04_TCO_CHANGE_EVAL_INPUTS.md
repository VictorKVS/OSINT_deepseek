# Lesson 02 — TCO, Change Control and Evaluation Inputs

Status: `INPUT MODEL / VALUES MOSTLY UNKNOWN`

## TCO v0 scenario families

Future semantic/LLM operation should compare at least:

- hosted model API;
- cloud GPU self-hosted model;
- on-prem GPU;
- hybrid/provider-neutral routing where justified.

No current cost winner is claimed before workload/quality/SLO/current-price evidence exists.

Required inputs:
- requests/tokens or workload units;
- concurrency and latency envelope;
- model/runtime quality on common eval set;
- compute/storage/network;
- license/provider terms;
- operations/support effort;
- hardware lifecycle/utilization for owned capacity;
- data/privacy constraints that may make a scenario inapplicable.

## Change Request model

A material change should record:

```text
Change request
Current baseline
Desired change
WHY / source
Requirement impact
Architecture impact
Security/data/legal impact
Schedule/estimate impact
Budget/TCO impact
Operational impact
Risk impact
Approval authority
Decision: APPROVE / REJECT / DEFER / NEED_MORE_EVIDENCE
Baseline/ADR/doc updates required
```

Change control is mandatory when scope/requirements materially affect an agreed Fixed Price or frozen baseline.

## Golden/Evaluation set plan

Future RAG/LLM decisions need a versioned evaluation set. Current project requirement:

- dataset/query-set owner named;
- intended capability/coverage stated;
- cases trace to real project scenarios;
- evidence/expected answer/expected source refs captured where applicable;
- privacy/classification reviewed;
- version immutable for a comparison run;
- model/retrieval/provider versions recorded;
- disagreements/reviewer corrections retained.

Size is project-specific; OTUS example counts are not imported as requirements.

## Delivery feasibility decision inputs

`DELIVERY_FEASIBILITY_READY` needs:
- measurable or explicitly unbaselined material NFRs;
- verification intent;
- WBS for known scope;
- named estimation method and assumptions;
- material project risks with owners/treatment;
- cost/budget envelope or explicit UNKNOWN owner;
- change-control mechanism;
- acceptance/evaluation evidence strategy.
