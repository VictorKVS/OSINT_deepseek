# FATHER OSINT — Local-First Transcription Roadmap

**Status:** PLANNED / MUST BE IMPLEMENTED WHEN THE TRANSCRIPTION USE CASE IS APPROVED  
**Date fixed:** 2026-08-09  
**Current code status:** NOT IMPLEMENTED  
**Engineering rule:** local capability is the strategic default; external services are optional fallbacks and must never become an implicit dependency.

## Decision

FATHER must eventually be able to process common audio/video files and obtain a transcript **locally, on infrastructure controlled by the operator**, without sending source material to a third-party server.

This is not a request to implement the stack during the current Stage 06 cleanup. It is a roadmap obligation. Implementation starts only after a dedicated requirement, threat/privacy review, architecture decision, test corpus and benchmark are approved.

## Why

The system is expected to work with OSINT material, business records, meetings and potentially sensitive evidence. Therefore the architecture must not assume that an operator is always allowed or willing to upload source files to an external transcription provider.

The desired operational model is:

```text
Artifact / audio / video
        ↓
validate real type + hash original
        ↓
local media normalization
        ↓
LOCAL TRANSCRIPTION
        ↓
local transcript + provenance
        ↓
Analyst
```

External transcription remains a separate optional path:

```text
Artifact
   ↓
classification / sensitivity gate
   ↓
explicit operator decision
   ↓
approved external provider
   ↓
transcript
   ↓
record provider + request time + policy + provenance
```

## Local-first requirements to design later

1. Preserve the original file before normalization.
2. Calculate SHA-256 on the original bytes before transformation.
3. Detect actual media type; do not trust only the filename extension.
4. Inspect audio/video streams before conversion.
5. Extract audio from video without needlessly transcoding the video stream.
6. Normalize to a transcription-friendly internal representation only when required.
7. Support language detection or explicit language selection without destroying the original language.
8. Store transcript separately from the original artifact.
9. Record which local model/version/settings produced the transcript.
10. Make local transcription replaceable behind a provider/engine contract.
11. Benchmark speed, memory/VRAM, word error rate and multilingual quality on target hardware before APPROVED status.
12. A transcription failure must not destroy the original evidence artifact.

## Provider abstraction

Future code should depend on a contract such as:

```text
TranscriptionEngine
    transcribe(artifact, options)
        ↓
TranscriptionResult
```

Possible implementations later:

```text
LocalWhisperEngine
LocalAlternativeEngine
ExternalAssemblyAIEngine
ExternalOtherEngine
```

Names above are examples, not approved implementations.

## Privacy classes for routing

A later requirements stage should define at least:

- `PUBLIC` — already public material; external processing may be allowed by policy.
- `INTERNAL` — non-public but ordinary business material; external use requires explicit policy/contract decision.
- `CONFIDENTIAL` — external upload denied by default.
- `RESTRICTED/EVIDENCE` — local-only unless a separately approved legal/security procedure permits otherwise.

The exact labels and rules are not approved yet; they are design candidates.

## External-provider rule

The project must maintain a current service registry for emergency/convenience transcription. Registry presence means only **DISCOVERED**, not TRUSTED or APPROVED.

Before uploading any non-public file, the operator must consider:

- whether third-party processing is legally and contractually allowed;
- personal/confidential data;
- storage and retention terms;
- deletion controls;
- training/model-improvement terms;
- processing region/jurisdiction;
- account/security controls;
- whether the file itself contains secrets or evidence that must stay local.

## Acceptance concept for the future

The capability is not complete until a test corpus proves at least:

```text
multiple codecs / containers
multiple languages
long recordings
poor/noisy recordings
multiple speakers
video with audio
unsupported/corrupt files
local-only execution with network disabled
reproducible provenance
```

## Architectural invariant

> FATHER must be able to continue core transcription work when external transcription services are unavailable, blocked, too expensive, or prohibited by data policy.

External services are acceleration/fallback options — not the foundation.
