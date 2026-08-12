# J-019 — M5 live repeat-run reuse + provenance proof

**Date:** 2026-08-12  
**Stage:** Stage 07 / M5 Telegram Radar  
**Type:** LIVE ACCEPTANCE / STORAGE SEMANTICS  
**Result:** PASS

## Purpose

Prove that repeated acquisition of already-seen Telegram payloads reuses the content-addressed raw payload by SHA-256 while preserving a new source-observation/provenance record for the repeated collection event.

This gate distinguishes two concepts that must not be conflated:

```text
content deduplication != observation deduplication
```

The same payload bytes may be reused physically, while each observed source event remains append-only evidence.

## Live evidence

A first live run had already created 10 Telegram materials and 10 raw payload files under the M5 live store.

The repeat acceptance command was executed against the same store with a minimum reuse expectation:

```text
python .\scripts\run_live_telegram_material.py --max-items 10 --expect-reuse-min 1
```

Observed result:

```text
status                    PASS
materials                 10
payloads_reused           10
expect_reuse_min          1
reuse_expectation_met     true
material_records_before   10
material_records_after    20
observations_appended     10
observations_preserved    true
raw_payload_files_before  10
raw_payload_files_after   10
new_raw_payload_files     0
```

The first material in the repeat run retained the same stable Telegram source identity and SHA-256 payload identity as the prior observed message:

```text
source_type     telegram
source_locator  telegram://1006503122/540
chat_id         1006503122
message_id      540
transport       telethon
content_hash    221ce7a3894171878ca67716c6a9b680df95d32e8aa14006cabbea81dcea4b57
```

## What this proves

```text
same Telegram payload
        ↓
existing SHA-256 raw blob detected
        ↓
raw blob reused
        ↓
no duplicate physical raw file
        ↓
new Material observation still appended
        ↓
provenance/history preserved
```

Measured proof:

- 10/10 payloads reused;
- 0 new raw payload files created;
- 10 new Material observation records appended;
- prior observations remained preserved;
- repeat run returned PASS under an explicit minimum-reuse acceptance threshold.

## Architectural significance

This validates the intended DEV storage invariant:

> Raw payload storage is content-addressed and deduplicated, while Material records represent source observations and remain append-only.

The behavior is source-independent and therefore reusable by future Web/GitHub/document collectors, not only Telegram.

## Critic notes

This proof does **not** yet prove full restart/checkpoint semantics because the current live runner re-queries recent messages and appends observations without a collector checkpoint cursor. It proves raw-payload reuse and append-only provenance semantics only.

Still pending for M5 DONE:

- explicit checkpoint model and save-before-checkpoint ordering;
- restart/reconciliation acceptance with interrupted collection;
- rate/FloodWait behavior;
- per-source live failure isolation;
- end-to-end MaterialPackage → Analyst → Socrates live proof;
- final M5 transport/production ADR scope.

## Gate update

```text
M5 network reachability                  PASS
Telethon live acquisition                PASS
TelegramMessage → Material               PASS
Material → SHA-256 raw storage            PASS
repeat raw-payload reuse                 PASS
append-only observation provenance       PASS
checkpoint/restart semantics             PENDING
rate/failure acceptance                  PENDING
MaterialPackage → Analyst → Socrates     PENDING

OVERALL M5                               ACTIVE / STRONG PARTIAL PASS
```

## Next action

Engineering Council EC-002 reviews whether the Telegram ingestion path is mature enough to be accepted as the reference pattern for source adapters, while explicitly keeping checkpoint/restart/rate/failure gates open before M5 DONE.
