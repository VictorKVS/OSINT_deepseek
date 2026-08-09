# Stage 06 — Legacy Cleanup Report

**Date:** 2026-08-09  
**Stage:** 06 — Verification and Repository Rationalization  
**Result:** PASS for legacy `core/` + old local runtime cleanup group

## Trigger

The repository still contained a pre-FATHER local runtime cluster: `core/`, a monolithic `run.py`, Windows/RTX stress tooling, and several Ollama/GPU experiment scripts. These assets had already been audited and classified as legacy, but deletion was intentionally deferred until the current DEV product could be proven independently.

## Precondition evidence

Before cleanup, the current product had already demonstrated on a clean GitHub Actions checkout:

```text
Python 3.12
father_osint import PASS
17 tests PASS
run_dev_osint.py PASS
run_dev_pipeline.py PASS
```

The dependency split also proved that current DEV verification requires only its explicit DEV requirements, not Ollama/GPU monitoring libraries.

## Dependency finding

`run.py` still referenced `core.logger` and `core.agent_tracker`, but it was itself part of the same audited legacy runtime cluster. The canonical FATHER OSINT package, tests and two current DEV runners did not require `core/`.

This meant the safe cleanup unit was the **legacy runtime cluster**, not an isolated `core/` file chosen by aesthetics.

## Removed files

### Legacy core

- `core/agent_tracker.py`
- `core/logger.py`
- `core/__init__.py`
- `core/README.md`

### Legacy root runtime

- `run.py`
- `start.ps1`
- `crash_analyzer.ps1`
- `system_stress_test.ps1`
- `system_test_results.txt`

### Legacy scripts

- `scripts/deepseek_safe.py`
- `scripts/hello_agent.py`
- `scripts/monitor.py`
- `scripts/rtx3060_agent.py`
- `scripts/smart_agent.py`

## Knowledge preserved before deletion

The implementations were removed, but the useful ideas remain captured in the Stage 06 audits:

- explicit agent/tool execution traces;
- health checks;
- runtime supervision;
- crash evidence;
- resource protection;
- logs/metrics as a future independent observability concern.

No hidden model reasoning is adopted as an observability requirement. Future tracing should contain explicit inputs, actions, tool events, outputs, errors, timing and formal decision reasons only.

## Verification after cleanup

GitHub Actions remained green after the cleanup sequence. The final legacy-script removal commit completed the canonical Stage 06 workflow successfully, and subsequent README/navigation cleanup also remained green.

Therefore deletion did not break the approved current DEV path.

## Architecture effect

Before:

```text
current FATHER OSINT
legacy core/runtime
legacy Ollama/GPU scripts
        all visible at repository top level
```

After:

```text
father_osint/              current DEV product
scripts/                   canonical DEV runners only
tests/                     current verification
requirements*.txt          explicit dependency classes
docs/                      retained engineering history
services/                  frozen experiments
telegram_bridge/           deferred experiment
```

## Decision

**PASS — legacy local-runtime cleanup group is complete.**

The old code is not moved into a new `archive/` directory because Git history plus the audit documents already preserve recoverability and design knowledge. Keeping duplicate inactive source in-tree would continue to confuse the current product boundary.

## Next action

Continue M2 with experimental-subproject placement and repository rationalization:

1. verify whether `services/llm-gateway/` should remain in this repository or be clearly isolated as a frozen subproject;
2. verify `telegram_bridge/` and `father_osint/transports/teleproto.py` boundaries;
3. update stale documentation references;
4. run clean CI after every approved structural change;
5. only then consider Stage 06 complete and prepare the DEV v1 baseline.
