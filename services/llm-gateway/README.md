# LLM Gateway / Cognitive Policy Prototype

**Status:** FROZEN EXPERIMENTAL SUBPROJECT — DO NOT INTEGRATE INTO CURRENT FATHER OSINT DEV PATH.

Despite the historical directory name `llm-gateway`, the current code does **not** implement multi-provider LLM routing. It is an experimental cognitive-policy/control-plane prototype built around:

```text
HTTP request
    ↓
Sphinx
(intent / regex patterns / heuristic risk)
    ↓
Enigma
(YAML policy laws)
    ↓
Judge
    ↓
ALLOW / DENY / QUARANTINE / SIMULATE
```

## Current decision

- Preserve the subsystem as engineering history.
- Do not import it from `father_osint`.
- Do not add FastAPI/PyYAML or HTTP dependencies to the current minimal DEV path because this code exists.
- Do not reuse its risk scores as confidence values.
- Do not treat keyword classification as expert truth.

## Patterns worth studying later

- deterministic enforcement after interpretation;
- externalized/versionable policy rules;
- explicit decision + reason + matched rule;
- separate control-plane boundary.

The current implementations are **not approved implementations** of those future requirements.

## Known architectural issues

- hand-written, uncalibrated risk scoring;
- two overlapping policy engines (`enigma` and `policies`);
- global mutable singletons and in-memory statistics;
- no immutable decision/audit record;
- no effective policy version in decisions;
- path manipulation via `sys.path.insert`;
- `simulation/mode.py` is empty;
- the API request contains `simulate`, but the execution path does not use it;
- the service name claims LLM-gateway capability that is not implemented.

## Future activation path

```text
approved business/use-case requirement
    ↓
architecture boundary
    ↓
input/output contract
    ↓
security / cost / latency constraints
    ↓
acceptance tests
    ↓
donor & technology research
    ↓
PoC / benchmark
    ↓
ADR
    ↓
implementation
```

If FATHER later needs a real multi-LLM gateway, it must be designed against provider routing, capability selection, privacy, retries, quotas, cost, telemetry and fallback requirements rather than promoted from this prototype by default.

Full audit: [`../../docs/06_verification/07_LLM_GATEWAY_AUDIT.md`](../../docs/06_verification/07_LLM_GATEWAY_AUDIT.md)
