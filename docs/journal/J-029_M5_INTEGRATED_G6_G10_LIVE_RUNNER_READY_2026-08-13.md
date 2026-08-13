# J-029 — M5 Integrated G6–G10 Live Runner READY — 2026-08-13

## Result

An integrated local live proof runner is now available:

`python scripts/run_live_telegram_m5_full.py`

It executes the accepted role/protocol path and then runs the G6–G10 layers in one bounded Telegram acquisition flow.

## Integrated flow

```text
ResearchRequest
→ SearchPlan
→ Analyst ACCEPT
→ Telegram collection
→ durable save/checkpoint
→ G6 reconnaissance/refinement
→ G7 evidence quality
→ G9 counter-evidence directive/assessment
→ EvidencePackage
→ G8 research sufficiency
→ G10 AcquisitionReport
→ Analyst handoff
→ deterministic Analyst
→ Socrates
```

## Conservative behavior

- requested and achieved sufficiency are reported separately;
- Telegram-only evidence is not automatically promoted to GOOD;
- independence is counted only when the quality layer explicitly marks HIGH;
- primary evidence is counted only from explicit source_class metadata;
- no aggregate truth probability is created;
- a supplied leading hypothesis makes G9 REQUIRED, but without an actually completed challenge-search attempt its status remains INCOMPLETE;
- no hypothesis produces explicit NOT_APPLICABLE rather than silently skipping G9;
- source failures and collection bounds flow into G10;
- restart/reconciliation controls remain available.

## Verification

GitHub Actions Stage 06 DEV Verification for commit `4bdb33840ca3ed2e5170e9798665e6f8f1f33d6d` completed SUCCESS.

```text
117 tests collected
117 passed
2 skipped
```

## Live proof still required

The live runner is intentionally not executed in GitHub/autonomous infrastructure because the authorized Telegram credentials/session remain local to the operator machine.

Recommended first live invocation:

```powershell
python .\scripts\run_live_telegram_m5_full.py `
  --max-items 25 `
  --recon-sample 10 `
  --resume `
  --sufficiency GOOD
```

Do not add `--hypothesis` on the first integrated proof. That first proof validates the descriptive/exploratory path where counter-evidence is formally NOT_APPLICABLE. A later controlled hypothesis scenario should separately prove the REQUIRED challenge-search branch rather than faking a completed counter-evidence search.
