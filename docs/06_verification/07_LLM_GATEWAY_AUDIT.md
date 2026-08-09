# Stage 06 — LLM Gateway Audit

**Status:** REVIEWED / KEEP AS FROZEN EXPERIMENTAL SUBPROJECT / DO NOT INTEGRATE

## Purpose

Review `services/llm-gateway/` as an independent legacy/experimental subsystem before any attempt to reuse it in the current FATHER OSINT architecture.

The review asks five questions:

1. What problem does this subsystem actually solve?
2. Does that problem belong to the current OSINT DEV contract?
3. Which architectural ideas are reusable?
4. Which implementation choices must not leak into the current design?
5. What gate must be passed before any future activation?

---

## 1. What the subsystem actually is

Despite the directory name `llm-gateway`, the current code is not a provider-routing LLM gateway.

It is closer to a **deterministic cognitive-policy prototype**:

```text
HTTP request
    ↓
Sphinx
(intent + regex patterns + heuristic risk)
    ↓
Enigma
(YAML laws / decision rules)
    ↓
Judge
(combine reports)
    ↓
ALLOW / DENY / QUARANTINE / SIMULATE
```

No current module performs model-provider selection, token/cost accounting, fallback across LLM vendors, prompt routing, retry policy, quota management, or model execution.

**Architectural conclusion:** the folder name is historically misleading. Treat it as an experimental policy/control-plane prototype, not as an approved LLM gateway.

---

## 2. Module review

### `app/api/main.py`

Role: FastAPI wrapper over `Judge`.

Useful ideas:
- explicit service boundary;
- typed request/response models;
- health endpoint;
- stats endpoint;
- policy/law inspection endpoint.

Problems:
- API says `status: active` even though the subsystem is not part of the approved runtime;
- path manipulation with `sys.path.insert` instead of a proper package boundary;
- no authentication, authorization, request id, audit id, timeout, versioned policy id, or persistence;
- `simulate` exists in the request schema but is not used in execution.

Decision: **STUDY / DO NOT ACTIVATE**.

### `app/core/judge.py`

Role: orchestration of Sphinx + Enigma.

Useful idea:

```text
analysis result
    ↓
policy evaluation
    ↓
decision + reason
```

This separation is conceptually valuable for future FATHER gates.

Problems:
- global singleton;
- in-memory statistics;
- no immutable decision record;
- no policy version in the decision;
- no evidence lineage;
- assumes Sphinx risk score is meaningful without calibration.

Decision: **PATTERN CANDIDATE ONLY**.

### `app/sphinx/intent.py`

Role: keyword/regex intent classification and heuristic risk scoring.

Current scoring is hand-written and uncalibrated. Examples include fixed risk values for `harm`, `code`, `manipulation`, regex matches, and prompt length.

This is acceptable as a historical experiment but must not be promoted into an expert decision engine without a requirement, labelled evaluation dataset, benchmark, false-positive/false-negative analysis, and policy approval.

Decision: **ARCHIVE IMPLEMENTATION / PRESERVE LESSON**.

### `app/enigma/engine.py` + `laws.yaml`

Role: deterministic rule evaluation from external YAML.

This is the strongest reusable architectural pattern in the subsystem:

```text
input facts/report
     ↓
versioned policy/rules
     ↓
deterministic evaluator
     ↓
decision + matched rule + reason
```

However, current implementation is incomplete for production governance:
- `risk_threshold` appears in YAML laws but is not itself enforced by `_matches` unless represented in `condition.risk`;
- policy version is absent;
- no effective date / lifecycle state;
- no conflict-resolution strategy beyond priority sorting;
- no signed/approved policy source;
- no decision persistence.

Decision: **ADAPT LATER AS POLICY ENGINE PATTERN, NOT CODE COPY**.

### `app/policies/engine.py`

Role: second, independent hard-coded policy engine.

This duplicates responsibility already present in Enigma and creates two different decision vocabularies and rule sources.

Architectural smell:

```text
Enigma policy engine
        ≠
policies/engine.py
```

Without a documented boundary this creates policy drift.

Decision: **DO NOT MERGE / DUPLICATE CONCEPT TO RESOLVE BEFORE ANY FUTURE USE**.

### `simulation/mode.py`

Currently empty.

Decision: **NO FUNCTIONAL VALUE YET**.

### `judge*.txt`, `laws.txt`, `stats*.txt`

Historical execution outputs / notes rather than source-of-truth architecture.

Decision: **ARCHIVE EVIDENCE; NOT RUNTIME CONTRACT**.

---

## 3. Fit with current FATHER OSINT DEV architecture

Current approved path:

```text
ResearchTask
    ↓
OSINTAgent
    ↓
MaterialPackage
    ↓
SimpleAnalyst   [DEV harness]
    ↓
SimpleSocrates [DEV harness]
    ↓
DevReviewPipeline
```

The current DEV goal is to prove handoffs, provenance, bounded follow-up, and failure behaviour.

A networked semantic/policy service is **not required** to prove those contracts.

Therefore:

- no imports from `father_osint` to `services/llm-gateway`;
- no HTTP dependency in current DEV tests;
- no FastAPI/PyYAML dependency should be added to the minimal OSINT DEV environment solely for this subsystem;
- no Sphinx/Enigma risk score may be used as Socrates confidence.

---

## 4. What we preserve as engineering knowledge

Four ideas are worth carrying forward as requirements candidates:

### A. Deterministic execution after interpretation

A model or analyst may classify/interpret, but enforcement should be performed by deterministic code when possible.

### B. Externalized policy

Rules should be data/configuration with explicit lifecycle rather than scattered `if` statements.

### C. Explainable decision output

A decision should include at least:
- decision;
- reason;
- matched policy/rule;
- policy version;
- input/evidence reference;
- timestamp;
- deciding component.

### D. Control-plane separation

Policy/control logic should not be hidden inside collectors, Analyst, or transport adapters.

These are **requirements candidates**, not approved implementation requirements yet.

---

## 5. What must not be inherited

Do not carry forward:

- arbitrary risk percentages without calibration;
- keyword match = intent truth;
- prompt length = risk without evidence;
- global mutable singletons as audit state;
- duplicated policy engines;
- in-memory stats as audit trail;
- hidden `sys.path` manipulation;
- service naming that claims capabilities not actually implemented;
- activating a service because the code already exists.

---

## 6. Decision

### Current decision

`services/llm-gateway/` → **KEEP / FROZEN EXPERIMENTAL SUBPROJECT**.

Do not delete yet because it preserves useful design experiments. Do not integrate because it has no approved requirement in the current OSINT DEV contract.

### Future activation gate

Before any LLM/policy gateway is allowed into FATHER:

```text
business/use-case requirement
        ↓
architecture boundary
        ↓
input/output contract
        ↓
security + cost + latency constraints
        ↓
policy semantics
        ↓
acceptance tests
        ↓
donor/technology research
        ↓
PoC / benchmark
        ↓
ADR
        ↓
implementation
```

If the future requirement is actual multi-LLM routing, this legacy subsystem should be treated only as historical input; the real gateway must be designed against provider routing, retries, cost, quotas, privacy, telemetry, model capability and fallback requirements.

---

## Exit result

The audit closes with:

- current OSINT remains independent of the experimental service;
- useful policy-control patterns are documented;
- uncalibrated scoring is explicitly rejected as an architectural foundation;
- future gateway development remains gated by requirements-first design.
