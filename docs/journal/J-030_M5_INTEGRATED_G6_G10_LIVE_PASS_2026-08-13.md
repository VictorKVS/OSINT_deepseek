# J-030 — M5 integrated G6-G10 live PASS — 2026-08-13

## Context

A real Windows/VPN/Telethon operator run executed the integrated M5 live runner after G6-G10 DEV implementation.

Command used:

```powershell
python .\scripts\run_live_telegram_m5_full.py `
  --max-items 25 `
  --recon-sample 10 `
  --resume `
  --sufficiency GOOD
```

## Live result

Top-level status: `PASS`.

Observed evidence:

- `workflow_state=CLOSED`
- 25 Telegram materials collected
- `observations_preserved=true`
- `new_raw_payload_files=25`
- checkpoint/restart reconciliation remained true
- G6 reconnaissance produced a report and `marginal_value=USEFUL`
- G6 did not recommend stopping
- G7 produced 25 separate evidence-quality assessments
- no aggregate truth probability was calculated
- requested sufficiency was `GOOD`
- achieved sufficiency was conservatively `MINIMUM`
- G9 correctly returned `NOT_APPLICABLE` because no leading hypothesis was supplied
- G10 produced a transparent AcquisitionReport with source attempts, unresolved gaps and lineage refs
- Analyst produced 25 observation claims
- Socrates verdict was `PASS`

## Important gaps surfaced by the live run

G6 reported:

- reconnaissance covered fewer than two observable Telegram sources;
- no external domains were observed in the reconnaissance sample;
- no explicit forward-origin metadata was observed.

G8 therefore retained `MINIMUM` and recommended resolving:

- independence;
- primary evidence;
- counter-evidence;
- critical gaps;
- quality context.

G10 retained the unresolved gap:

`Non-Telegram corroboration is not covered by this Telegram-only live proof`.

## Interpretation

This is the expected conservative behavior. A successful acquisition does not imply GOOD research sufficiency. The integrated pipeline correctly distinguishes transport success, evidence preservation, reconnaissance usefulness, evidence quality, research sufficiency and analytical review.

The run validates the integrated role/protocol path for an exploratory Telegram-only scenario. It does **not** validate hypothesis-driven counter-evidence execution, cross-source corroboration, or GOOD/DESIRABLE sufficiency.

## Next gate

Before G11/M5 DONE:

1. execute a live hypothesis-driven scenario where G9 is REQUIRED and an actual counter-evidence attempt is recorded;
2. review why only one observable Telegram source was present in the bounded sample and whether this is config/order/sample behavior or an expected limitation;
3. complete final Engineering Council/Critic review, secrets/session hygiene review and transport ADR update.
