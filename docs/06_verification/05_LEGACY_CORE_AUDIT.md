# Stage 06 — Legacy Core Audit

**Scope:** `core/agent_tracker.py`, `core/logger.py`

**Status:** REVIEWED / NO MIGRATION TO FATHER YET / PRESERVE KNOWLEDGE, NOT IMPLEMENTATION

## Why this audit exists

The current FATHER DEV path must not inherit legacy modules merely because useful ideas are present in old code. We first identify the original business/engineering purpose, then decide whether the capability is required by an approved requirement.

Decision chain:

```text
legacy implementation
      ↓
identify capability
      ↓
identify current requirement
      ↓
separate useful concept from old mechanism
      ↓
KEEP / ADAPT LATER / ARCHIVE / DELETE
```

## 1. `core/agent_tracker.py`

### Original purpose

The module was built to make agent execution visible. It models a trace containing:

- agent name and user query;
- start/end time and duration;
- actions/tool calls;
- observations/results and errors;
- final response;
- historical trace storage and simple aggregate statistics.

It also contains a separate `AgentThought` structure and `add_thought()` path intended to persist intermediate agent reasoning.

### Useful capability that should survive

FATHER will eventually need **execution traceability**, but the useful object is not private model reasoning. The durable requirement is operational evidence:

```text
Agent Run
   ├── run_id
   ├── agent / role
   ├── task_id
   ├── started_at / ended_at
   ├── input reference
   ├── tool/action events
   ├── output reference
   ├── status / error
   └── timing / counters
```

This can later support:

- debugging;
- auditability;
- performance measurement;
- replay/reproduction;
- linking a decision to the run that produced it.

### What must NOT be carried forward

Do not design FATHER around storing hidden chain-of-thought or private model reasoning. `AgentThought.thought` and the "show what the agent thinks" concept are not part of the approved observability contract.

Future observability should store explicit, inspectable events and declared rationale/WHY where required by a business decision, not private reasoning traces.

### Technical issues in the legacy implementation

- global singleton created at import time;
- direct console/UI concerns mixed with persistence;
- JSON history limited by an arbitrary last-1000 policy;
- broad exception handling in history load;
- export behavior assumes dict/dataclass shapes inconsistently;
- runtime dependency on `colorama` solely for presentation;
- tracing decorator is tightly coupled to one calling convention;
- no formal schema/version for stored trace records;
- no retention/security/privacy policy.

### Decision

**Implementation:** `ARCHIVE / DELETE CANDIDATE after full legacy cleanup gate`.

**Concept:** `ADAPT LATER as Agent Execution Trace / Observability requirement`.

No code is migrated into `father_osint` during current DEV stage.

---

## 2. `core/logger.py`

### Original purpose

This module combines generic query counters with host resource monitoring:

- CPU utilization/frequency;
- RAM utilization;
- disk utilization;
- optional GPU metrics;
- basic warning thresholds;
- background periodic sampling.

### Business relevance to current OSINT DEV scope

None of these metrics are required to prove the current OSINT contract:

```text
ResearchTask → MaterialPackage → Analyst → Socrates
```

Resource telemetry may become useful much later for production capacity planning, performance benchmarks, health checks, or model/GPU workloads, but it is not an OSINT-domain responsibility.

### Technical issues in the legacy implementation

- imports `psutil` and optional `GPUtil`, forcing unrelated operational dependencies;
- hard-coded resource thresholds;
- disk check assumes `/`, which is not portable to the Windows-first development environment;
- background infinite daemon loop is created as an application concern rather than infrastructure concern;
- logger name is misleading because most of the file is resource telemetry, not structured application logging;
- query counters are in-memory only and disconnected from the current FATHER domain model.

### Decision

**Implementation:** `ARCHIVE / DELETE CANDIDATE after full legacy cleanup gate`.

**Concepts:**

- structured application logging → future infrastructure requirement;
- host metrics → future production observability/benchmark requirement;
- GPU monitoring → only if a later approved component actually requires local GPU execution.

Do not import this module into `father_osint` and do not keep its packages in the minimal DEV dependency set solely for this legacy code.

---

## Architectural conclusion

The legacy `core/` contains **valuable lessons, not reusable foundations**.

Target separation for a future production design should be:

```text
DOMAIN
OSINT / Analyst / Socrates
        │
        │ emits explicit events
        ▼
OBSERVABILITY INTERFACE
        │
        ├── execution traces
        ├── structured logs
        ├── errors
        └── performance metrics
                │
                ▼
       infrastructure adapters
```

Observability must remain outside domain decisions. Failure of telemetry must not change an OSINT result.

## Current gate decision

| File | Current code | Capability | Decision now |
|---|---|---|---|
| `core/agent_tracker.py` | legacy | execution traceability | ARCHIVE; adapt concept later |
| `core/logger.py` | legacy | resource telemetry/logging | ARCHIVE; adapt concept later |
| `core/__init__.py` | legacy package marker | none | remove with `core/` only after cleanup gate |

### Deletion is NOT executed in this audit

Before deleting `core/`, complete:

1. full-tree caller/import verification;
2. classify root legacy scripts that may still use these modules;
3. preserve any still-useful requirements in documentation;
4. run current DEV regression after legacy removal.

This preserves the FATHER rule: **we may delete obsolete code only after preserving the reason, requirement, and evidence that justified the decision.**
