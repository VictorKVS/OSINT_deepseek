# J-022 — M5 live restart / reconciliation PASS

**Date:** 2026-08-12  
**Stage:** Stage 07 / M5 Telegram Radar  
**Gate:** G4 Reliability  
**Result:** PASS

## Trigger

M5 reliability contracts for save-before-checkpoint, restart persistence, bounded FloodWait and per-channel failure isolation already passed deterministic tests. The remaining blocking evidence was a real Windows/VPN Telegram restart/reconciliation proof using the live Telethon reference adapter and the canonical Material/MaterialStore path.

## Live evidence

Environment: Windows, repository `G:\1\OSINT_deepseek_poc`, approved local Telegram session, AmneziaVPN network path.

Regression baseline before live proof:

```text
pytest: 75 passed in 3.76s
```

### Run A — first checkpoint-enabled live run

Command:

```powershell
python .\scripts\run_live_telegram_material.py --max-items 10 --resume
```

Observed:

```text
status                         PASS
materials                      10
payloads_reused                10
observations_appended          10
observations_preserved         true
new_raw_payload_files          0
analysis_claims                10
socrates_verdict               PASS
checkpoint_enabled             true
resume_requested               true
resumed_sources                0
checkpoint_commits             10
restart_reconciliation_passed  true
```

This run created/advanced the live checkpoint after durable Material persistence.

### Run B — process restart / reuse / resume proof

Command:

```powershell
python .\scripts\run_live_telegram_material.py --max-items 10 --resume --expect-reuse-min 1
```

Observed:

```text
status                         PASS
materials                      10
payloads_reused                10
reuse_expectation_met          true
material_records_before        40
material_records_after         50
observations_appended          10
observations_preserved         true
raw_payload_files_before       10
raw_payload_files_after        10
new_raw_payload_files          0
analysis_claims                10
socrates_verdict               PASS
checkpoint_enabled             true
resume_requested               true
resumed_sources                1
checkpoint_commits             10
restart_reconciliation_passed  true
```

A subsequent third run reproduced the same restart properties with `resumed_sources=1`, `payloads_reused=10`, `new_raw_payload_files=0`, `observations_appended=10` and Socrates `PASS`.

## What this proves

```text
Telegram LIVE observation
        ↓
canonical Material
        ↓
durable save
        ↓
checkpoint commit
        ↓
process ends
        ↓
new process starts
        ↓
existing checkpoint detected
        ↓
previous raw payload reused by SHA-256
        ↓
new observation/provenance appended
        ↓
MaterialPackage → Analyst → Socrates
        ↓
PASS
```

The live evidence demonstrates that raw-payload deduplication and observation/provenance preservation coexist across a process restart. The checkpoint file survives restart and the runner detects an existing source checkpoint on the next run.

## Scope / non-claims

This proof does **not** claim exactly-once distributed delivery, crash recovery at every possible machine-instruction boundary, multi-host consensus, or production-grade transactional storage. M5 requires a bounded local reference reliability pattern, not speculative distributed infrastructure.

The current live runner still re-observes the bounded recent Telegram sample on the next run; this is intentional for the M5 reconciliation proof. Future incremental source cursors may use transport-native history boundaries when a concrete requirement justifies them.

## G4 disposition

G4 Reliability is now **PASS** for M5:

- save-before-checkpoint — PASS by contract tests;
- checkpoint survives restart — PASS by tests + live evidence;
- bounded FloodWait/retry — PASS by transport contract tests;
- per-channel failure isolation — PASS by transport contract tests;
- live checkpoint/restart/reconciliation — PASS;
- provenance/evidence preserved across restart — PASS.

## Next gate

Proceed to **G5 — OSINT Expert SearchPlan**:

```text
Analyst states WHAT must be established
        ↓
OSINT Expert decomposes observable indicators
        ↓
OSINT owns Telegram source/search tactics
        ↓
explicit scope / limits / exclusions / counter-evidence intent
        ↓
SearchPlan
```

Do not expand into generic Kali/ToolRegistry implementation during G5. Those concepts are recorded in EC-003 and remain deferred until the Telegram proving ground has closed M5.
