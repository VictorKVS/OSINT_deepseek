# J-020 — M5 live Telegram → EvidenceClaim → Socrates PASS

**Date:** 2026-08-12  
**Stage:** Stage 07 / M5 Telegram Radar  
**Status:** PASS / NEW VERIFIED PEAK

## Goal

Prove the first complete live evidence path from a real Telegram source through the canonical FATHER evidence model and deterministic reasoning boundary.

## Live command

```powershell
python .\scripts\run_live_telegram_material.py --max-items 10 --expect-reuse-min 1
```

## Observed result

The live runner returned `status = PASS` and proved all currently required layers in one execution:

- 10 live Telegram materials acquired through `TelethonTransport`;
- 10 raw payloads reused from prior content-addressed storage;
- zero new raw payload files created;
- 10 new material/provenance observations appended;
- 10 deterministic evidence claims produced;
- no analysis limitations reported;
- `DeterministicSocrates` returned `PASS`;
- zero claims were challenged;
- `reasoning_passed = true`.

Representative observed metrics:

```text
materials                   = 10
payloads_reused             = 10
material_records_before     = 20
material_records_after      = 30
observations_appended       = 10
observations_preserved      = true
raw_payload_files_before    = 10
raw_payload_files_after     = 10
new_raw_payload_files       = 0
analysis_claims             = 10
analysis_limitations        = []
socrates_verdict            = PASS
socrates_challenged_claims  = 0
reasoning_passed            = true
```

## Verified architecture path

```text
LIVE TELEGRAM
      ↓
TelethonTransport
      ↓
TelegramMessage
      ↓
TelegramCollector
      ↓
Material
      ↓
MaterialStore / SHA-256
      ↓
MaterialPackage
      ↓
DeterministicEvidenceAnalyst
      ↓
EvidenceClaim(material_id references)
      ↓
DeterministicSocrates
      ↓
PASS
```

## What this proves

The project now has measured live evidence that a real external Telegram observation can traverse the canonical FATHER acquisition, evidence, provenance, storage and reasoning boundaries without Telegram-specific objects leaking above the transport/collector layer.

The reasoning result is evidence-addressed: every produced claim cites one or more `material_id` values from the supplied package, and Socrates verifies that those references belong to that package.

## What this does NOT prove

This entry does not claim that M5 is complete or that the system has proven truth.

Still unverified / not yet closed:

- durable checkpoint and save-before-checkpoint ordering;
- restart/reconciliation semantics;
- rate-limit / FloodWait handling;
- per-source failure isolation in the live Telegram adapter;
- clean first-time authorization/session lifecycle for production operation;
- production LLM-backed Analyst quality, calibration, hallucination control or cost;
- cross-source corroboration and contradiction handling.

## Senior / Principal Critic note

The deterministic reasoning boundary should be treated as a safety and traceability contract, not as an intelligence-quality benchmark. A `PASS` here means the claims are structurally evidence-addressed and package-consistent; it does not mean the claims are complete, unbiased, corroborated, or factually true.

Therefore the next architectural decision must determine whether LLM intelligence should be introduced now or whether operational ingestion reliability must be completed first.

## Next gate

Engineering Council review:

> Should M5 proceed to an LLM-backed Analyst now, or first close checkpoint/restart/FloodWait/failure-isolation reliability gates?
