# 2026-08-09 — M2 legacy cleanup checkpoint

**Stage:** 06 — Verification and Repository Rationalization  
**Trigger / problem:** audited legacy `core/`, monolithic runtime and workstation/Ollama/GPU scripts remained in the active repository tree and obscured the canonical FATHER OSINT product boundary.  
**Decision:** remove the legacy runtime cluster only after clean-checkout CI proved the current product was independent from it.  
**WHY:** inactive duplicate code creates false dependencies, misleading entrypoints and maintenance cost. Git history plus Stage 06 audit documents preserve recoverability and engineering lessons without retaining obsolete executable code in the active tree.  

**Files removed:**
- `core/agent_tracker.py`
- `core/logger.py`
- `core/__init__.py`
- `core/README.md`
- `run.py`
- `start.ps1`
- `crash_analyzer.ps1`
- `system_stress_test.ps1`
- `system_test_results.txt`
- `scripts/deepseek_safe.py`
- `scripts/hello_agent.py`
- `scripts/monitor.py`
- `scripts/rtx3060_agent.py`
- `scripts/smart_agent.py`

**Knowledge retained:** future observability requirements for explicit traces, tool events, errors, timings, logs/metrics, health checks, crash evidence, runtime supervision and resource protection. Hidden model reasoning is not an observability requirement.

**Tests/evidence:** Stage 06 GitHub Actions remained green after the cleanup sequence; canonical DEV baseline continues to pass clean checkout, imports, tests and both DEV runners.

**Result:** **PASS**  

**New risks/open questions:** frozen experimental subsystems (`services/llm-gateway/`, `telegram_bridge/`, `TeleprotoTransport`) still need final placement decisions before DEV v1 baseline freeze.

**Next action:** audit/isolate experimental subsystems, remove stale documentation references, rerun clean CI, then decide whether Stage 06 can close and DEV v1 can be frozen.
