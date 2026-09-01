# Security departmental evening acquisition — 2026-08-24

## Scope

Run the departmental/sectoral information-security acquisition in five parallel workers after checking the official publication route and A2 working-copy quality. Only content-quality PASS material is allowed into shadow D4-D9. No document is promoted to `CURRENT` without exact official bytes, SHA-256, and amendment/replacement-chain verification.

## Execution evidence

- GitHub Actions run: `32754932404` (`Departmental Security Evening Acquisition`)
- Head branch: `agent/knowledge-factory-m1`
- Head SHA: `5d61ec39655bc227c8d587bffe8c407cd150c3db`
- Job result: `success`
- Workers: `5`
- Evidence artifact: `departmental-security-evening-resume`, artifact id `9530489117`
- Artifact size: `242398` bytes
- Artifact SHA-256: `8f7e84e556211548a0f6129f9c35854d3d11b220fe070543b86ca27f8ae71064`
- Artifact expiry: `2026-08-31T17:10:02Z`

## Source preflight

### publication.pravo.gov.ru

Status: `DEGRADED`.

Three exact document routes were probed and all three timed out. The departmental acquisition circuit breaker therefore marked `publication.pravo.gov.ru` as `DEGRADED_SKIP_FOR_RUN`; no official payload was claimed for this run.

### A2 working-copy sources

- routes tested: `14`
- fetch failures: `0`
- content-quality PASS: `1`
- content-quality BLOCKED: `13`

The single PASS item was `DOC-RU-ROSFMON-149-2025` (Rosfinmonitoring order No. 149 of 2025) from the configured ConsultantPlus working-copy route. It remained `A2_REFERENCE_WORKING_COPY`; it did not become legal truth or `CURRENT`.

## Acquisition result

The GitHub runner started from a fresh checkout, so no uncommitted/local runtime corpus from the operator workstation was visible. The resume filter found `0` existing full-quality local items in that runner and processed all `14` configured queue items.

- downloaded payloads: `14`
- exact official downloads: `0`
- A2 downloads: `14`
- normalized/content-quality PASS: `1`
- content blocked: `13`
- unresolved: `0`
- operationally available: `1`
- CURRENT promotions: `0`
- currentness verified: `false`
- KB promotion allowed: `false`

All fetched A2 payloads received SHA-256 evidence. Thirteen were retained as blocked working copies because the full legal body could not be confirmed. Exact official evidence was not acquired for any queue item in this run.

## Shadow D4-D9

Shadow processing was restricted to acquisition rows with `content_quality_pass == true` and normalized content. Exactly one document entered shadow D4-D9:

- ready D9 shadow candidates: `1`
- requirements extracted: `0`
- entities extracted: `0`
- official pipeline advanced: `false`
- legal truth promoted: `false`
- review required: `true`

## Throughput

- acquisition wall for the five-worker departmental stage: `11.675370021 s`
- downloaded payload throughput: `1.199105465 docs/s`
- operational full-quality throughput: `0.085650390 docs/s`
- shadow D4-D9: `0.004118849 s` for one document, reported as `242.786274 docs/s`; this one-document figure is not a meaningful capacity benchmark
- complete orchestration wall time including source preflight: `64.082430334 s`

No 1-stream speedup is claimed because there was no same-queue/same-runner 1-stream baseline.

## Gate outcome

`CURRENT` gate remains closed for every departmental item. Exact official bytes were not obtained from `publication.pravo.gov.ru`; amendment/replacement-chain verification was not completed. A2 material remains operational/shadow evidence only.

## Local-state caveat

The acquisition was executed in GitHub Actions, not on the operator workstation. Therefore the "already has full quality text" filter only saw files present in the checked-out repository/runtime generated during this run. Before the next local run, the same filter can be executed against the local `G:\1\OSINT_deepseek` corpus to avoid reacquiring locally cached full-quality documents.
