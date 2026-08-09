# Reusable Artifact Ingestion Concept

**Status:** FUTURE REQUIREMENT CANDIDATE / NOT IMPLEMENTATION-APPROVED  
**Source of experience:** Vibe-coding AI secretary architecture  
**Purpose:** preserve a reusable ingestion/normalization pattern for future FATHER OSINT development without prematurely adding code.

## Why this matters

The AI-secretary workflow exposes a reusable engineering problem that also exists in OSINT: incoming material may arrive as audio, video, images, documents, URLs or other files, with different codecs, containers, encodings and languages.

The correct architectural response is not one business branch per extension. The reusable pattern is:

```text
Source
  ↓
INGESTION
  ↓
Type verification
  ↓
ARTIFACT
  ↓
ROUTER
  ├─ Audio
  ├─ Video
  ├─ Image
  └─ Document
  ↓
Normalization / extraction
  ↓
EXTRACTED CONTENT
  ↓
Analyst / downstream processing
```

## Cross-project lesson

The Vibe-coding project defines GitHub as source of code/assets, Colab as execution environment and Telegram as the user interface. Its modules are deliberately designed so that ingestion, media normalization, transcription, storage and progress can later move into OSINT without rewriting the user-facing application.

This is useful architectural experience for FATHER, but it does **not** automatically become current OSINT implementation.

## Candidate input object

A future generic input contract may use an object similar to:

```text
Artifact
├─ id
├─ source
├─ original_name
├─ declared_mime
├─ detected_mime
├─ sha256
├─ size
├─ original_path
├─ normalized_path
├─ media_type
├─ language
├─ metadata
└─ created_at
```

Important: this is a design candidate, not yet an approved domain model.

## Required invariants

### 1. Preserve the original

Normalization must never destroy the original artifact. The original is retained for provenance, repeatability and forensic/OSINT evidence.

### 2. Hash before transformation

Calculate SHA-256 for the original bytes before normalization. A normalized derivative receives its own identity and must remain linked to the original.

### 3. Do not trust file extension alone

Use at least:

```text
filename/extension
+ declared MIME
+ detected signature / magic bytes
```

Mismatch becomes an explicit security/processing event rather than silent acceptance.

### 4. Container is not codec

Audio/video routing must inspect actual streams. A `.mp4`, `.mkv`, `.webm` or other container is not sufficient evidence of contained codecs.

### 5. Normalize only for processing

Examples of possible processing standards:

```text
Audio/Video → extracted audio → normalized WAV/PCM
Image       → normalized RGB image
Document    → text + tables + images + metadata
```

The exact internal formats are subject to benchmark and downstream-service requirements.

### 6. Language is metadata, not user-selected truth

Preserve original language and original text. Translation, when used, is a derivative with its own model/version/provenance.

### 7. OCR is fallback, not default

For documents such as PDF, first attempt native text/table extraction. OCR/vision is invoked only when native extraction is unavailable or insufficient.

### 8. Progress reflects real events

If progress is exposed to a UI, it should correspond to real state changes such as:

```text
received
→ original stored
→ type verified
→ normalized
→ text/audio extracted
→ transcription complete
→ analysis complete
→ output stored
```

Percentages, if displayed, are merely presentation of these discrete state transitions unless a measurable continuous metric exists.

## Relation to current FATHER OSINT

Current DEV contract remains deliberately smaller:

```text
ResearchTask
  ↓
Collector
  ↓
Material
  ↓
MaterialPackage
```

The future Artifact/Normalization layer would sit **inside or immediately below source acquisition**, not replace Analyst/Socrates responsibilities.

Possible future relation:

```text
Telegram / URL / Web / File / Email
          ↓
      Artifact Ingestion
          ↓
  normalized/extracted material
          ↓
       OSINT Collector
          ↓
      MaterialPackage
          ↓
        Analyst
```

## Why we do not implement it now

Under `NO CODE BEFORE CONTRACT`, implementation is blocked until a real OSINT requirement needs heterogeneous file ingestion.

Before code, Stage chain must include:

1. use cases and supported input classes;
2. threat model for untrusted files;
3. size/resource limits;
4. MIME/signature policy;
5. normalization requirements per media family;
6. derivative/provenance contract;
7. language/translation policy;
8. acceptance corpus and tests;
9. donor/technology review (FFmpeg, document parsers, image stack, etc.);
10. benchmark and ADR.

## Decision

**PRESERVE AS REUSABLE ARCHITECTURAL KNOWLEDGE. DO NOT ADD MODULES TO `father_osint/` YET.**

This concept should be revisited when a concrete requirement says the OSINT worker must ingest heterogeneous media/documents rather than only fixture/text-like materials.
