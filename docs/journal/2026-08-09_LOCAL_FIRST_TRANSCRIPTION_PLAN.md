# 2026-08-09 — Local-first transcription plan fixed

**Stage:** Stage 06 / architecture knowledge capture  
**Result:** PLANNED / NOT IMPLEMENTED

## Trigger

A reusable ingestion/transcription pattern from the AI-secretary work showed that FATHER will eventually need to process heterogeneous audio/video artifacts, but should not depend on a third-party transcription server for core work.

## Decision

1. Local transcription is a required future FATHER capability.
2. External transcription services are optional fallback/acceleration tools.
3. A service registry will be maintained, but listing never implies trust or approval.
4. Sensitive material routes local-first by default; external upload requires a later explicit policy/exception process.
5. No transcription code is added during the current cleanup stage.

## WHY

- external services may be unavailable, blocked, expensive or legally prohibited for a specific artifact;
- provenance/evidence should stay under operator control where required;
- cloud services remain useful for speed, comparison and emergency processing;
- provider availability, pricing and data terms change, therefore the registry must be re-verified over time.

## Artifacts added

- `docs/06_verification/14_LOCAL_FIRST_TRANSCRIPTION_ROADMAP.md`
- `docs/TRANSCRIPTION_SERVICE_REGISTRY.md`

## Future gate

When transcription becomes an approved use case:

```text
ТЗ
→ privacy/threat review
→ artifact/transcription contracts
→ test corpus
→ donor research for local engines
→ benchmark on target hardware
→ ADR
→ implementation
→ offline/network-disabled acceptance test
```

## Invariant

FATHER core transcription must remain usable without sending source files to an external provider.
