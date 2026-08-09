# Stage 06 — Legacy Runtime Audit

**Status:** REVIEWED / CLEANUP NOT YET EXECUTED

## Purpose

Review the historical root runtime and pre-FATHER scripts before deleting anything. The rule remains:

```text
historical component
      ↓
recover original purpose
      ↓
identify current dependency
      ↓
extract reusable requirement/pattern
      ↓
classify
      ↓
KEEP / MIGRATE / ARCHIVE / DELETE
```

The audit is about preserving useful engineering knowledge while preventing legacy runtime from silently defining the new FATHER architecture.

---

## 1. `run.py`

### Original purpose

Historical OSINT Studio launcher. It combines:

- system monitoring;
- crash detection;
- Ollama availability/model checks;
- menu/UI;
- subprocess launching of legacy agents;
- GPU/RAM safety thresholds;
- direct dependency on `core.logger` and `core.agent_tracker`.

### Current architectural fit

It is **not** the current FATHER OSINT entrypoint. It predates the requirements-first package and directly couples UI, runtime supervision, hardware monitoring and agent launching.

Current approved DEV entrypoints are:

```text
scripts/run_dev_osint.py
        and
scripts/run_dev_pipeline.py
```

### Useful concepts to preserve

- explicit startup health checks;
- process supervision;
- controlled shutdown;
- crash record creation;
- optional runtime safety policy.

These are future **Operations / Runtime Supervisor** concerns, not responsibilities of `OSINTAgent`.

### Decision

`ARCHIVE / DELETE CANDIDATE`.

Do not migrate its code into `father_osint`. Preserve the operational concepts as future requirements only if/when production runtime is designed.

---

## 2. `start.ps1`

### Original purpose

Machine-specific Windows startup helper. It:

- changes directory to a hard-coded `G:\1\OSINT_deepseek` path;
- activates `.venv`;
- checks Ollama;
- collects WMI CPU/RAM/GPU information;
- appends startup logs;
- prints commands for legacy scripts.

### Risks / portability

It is tied to one workstation layout and old runtime assumptions. It references legacy commands such as `scripts/monitor.py`, `scripts/smart_agent.py` and `scripts/rtx3060_agent.py`.

### Reusable concept

A future environment bootstrap may be useful, but it must be generated from approved deployment requirements and must not contain workstation-specific absolute paths.

### Decision

`ARCHIVE / DELETE CANDIDATE`.

If a bootstrap script is later required, write a new one from deployment requirements rather than adapting this file.

---

## 3. `system_stress_test.ps1`

### Original purpose

Hardware stress/telemetry experiment for the developer workstation, especially RTX 3060 operation. It creates CPU load, samples NVIDIA/Windows metrics and writes a report.

### Current architectural fit

This does not test FATHER business or OSINT behavior. It tests workstation/hardware stability.

### Reusable concept

Performance and resource tests are valid later, but they belong to a separate **non-functional benchmark plan** with defined load profile, acceptance thresholds and reproducible environment.

### Decision

`ARCHIVE / DELETE CANDIDATE` from the product repository after local-history preservation if desired.

Do not call it a FATHER performance benchmark.

---

## 4. `crash_analyzer.ps1`

### Original purpose

Post-crash Windows/NVIDIA event-log collection.

### Current architectural fit

Useful as workstation troubleshooting, not as application-level failure analysis. It is Windows-specific and its broad event-ID selection is not tied to FATHER failure modes.

### Reusable concept

Production operations should have a documented incident evidence collection procedure, but that requirement must be designed independently of this script.

### Decision

`ARCHIVE / DELETE CANDIDATE` from the main product path.

---

## 5. Legacy Python scripts under `scripts/`

### `smart_agent.py`

Historical local Ollama chat agent with resource monitoring and automatic model switching. It uses `scripts.monitor.SystemMonitor` and is unrelated to the current OSINT material-collection contract.

**Decision:** `ARCHIVE / DELETE CANDIDATE`.

### `monitor.py`

Historical hardware monitor used by legacy Ollama agents.

**Decision:** `ARCHIVE / DELETE CANDIDATE`; retain only the concept of operations telemetry for future design.

### `rtx3060_agent.py`

Hardware/model-specific local LLM experiment.

**Decision:** `ARCHIVE / DELETE CANDIDATE`.

### `deepseek_safe.py`

Historical local model safety/resource experiment.

**Decision:** `ARCHIVE / DELETE CANDIDATE`.

### `hello_agent.py`

Early agent/prototype experiment.

**Decision:** `ARCHIVE / DELETE CANDIDATE` unless later audit finds unique knowledge not captured elsewhere.

### Current DEV scripts

- `run_dev_osint.py` — **KEEP**.
- `run_dev_pipeline.py` — **KEEP / canonical DEV runner**.

---

## 6. Relationship to `core/`

The historical runtime explains why `core/logger.py` and `core/agent_tracker.py` existed: they supported `run.py` and the old local-agent environment.

That dependency does **not** justify importing them into the new FATHER package.

```text
legacy run.py
   ├── core.logger
   └── core.agent_tracker

current FATHER DEV
   └── no dependency on core/
```

Therefore `core/` and historical runtime form one legacy cluster that can later be archived/removed together after the final local checkout scan.

---

## 7. Requirements recovered from legacy work

The old implementation contains several valid ideas that should survive as requirements, not copied code:

1. **Operational observability** — record explicit execution events, timings, failures and health state.
2. **Runtime health checks** — verify required external services before production work begins.
3. **Failure evidence** — preserve enough information to diagnose an execution failure.
4. **Resource protection** — production workloads may need configurable resource limits and graceful degradation.
5. **Separation of concerns** — hardware/runtime supervision must remain outside domain analysis and evidence semantics.

These requirements are **DEFERRED** until the production/runtime stage. They are not part of the current DEV OSINT acceptance boundary.

---

## 8. Cleanup gate

Deletion is not yet executed in this audit.

Before deleting the legacy runtime cluster:

- complete a real local checkout;
- run repository-wide text/import search;
- confirm the current DEV scripts and tests do not depend on it;
- preserve any historical files outside the product repository if the user wants an archive;
- rerun canonical tests after removal.

Expected future cleanup cluster:

```text
run.py
start.ps1
system_stress_test.ps1
crash_analyzer.ps1
system_test_results.txt
scripts/smart_agent.py
scripts/monitor.py
scripts/rtx3060_agent.py
scripts/deepseek_safe.py
scripts/hello_agent.py
core/
```

**Current decision:** `ARCHIVE / DELETE CANDIDATES — NO DELETE UNTIL FINAL CLEANUP GATE`.
