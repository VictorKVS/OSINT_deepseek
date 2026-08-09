# 2026-08-09 — Reusable Artifact Ingestion lesson

**Stage:** Stage 06 — Verification / architecture knowledge capture  
**Trigger / problem:** Parallel Vibe-coding work exposed a general ingestion problem: audio, video, images and documents arrive with different containers, codecs, MIME declarations, encodings and languages. The same problem will later appear in FATHER OSINT.

**Decision:** preserve the pattern as reusable architecture knowledge, but do not add `ingestion.py`, `media.py`, transcription/document routing or other new modules to the current `father_osint/` DEV core.

**WHY:** the design is valuable, but current OSINT acceptance does not yet require heterogeneous artifact ingestion. Adding the code now would violate `NO CODE BEFORE CONTRACT` and reintroduce premature growth.

**Reusable pattern captured:**

```text
source
  ↓
ingestion
  ↓
type verification
  ↓
original Artifact + SHA-256
  ↓
router
  ├─ audio/video → stream inspection / normalization
  ├─ image → safe normalized derivative
  └─ document → native extraction first, OCR fallback
  ↓
ExtractedContent
  ↓
downstream Analyst / processing
```

**Key invariants retained:**
- original artifact is never destroyed by normalization;
- SHA-256 is calculated before transformation;
- extension alone is not trusted;
- declared MIME and detected signature are compared;
- container and codec are separate concepts;
- original language/text is preserved;
- translation is a derivative with provenance;
- OCR is fallback, not default;
- UI progress must represent actual processing events, not cosmetic animation.

**Files/documents affected:**
- `docs/06_verification/13_REUSABLE_INGESTION_CONCEPT.md`
- this journal entry

**Tests/evidence:** architectural capture only; no new runtime requirement and therefore no new implementation/test contract.

**Result:** DEFERRED / KNOWLEDGE PRESERVED.

**New risks/open questions:**
- supported file classes and size limits are undefined;
- untrusted-file threat model is not yet approved;
- normalization standards are not benchmarked;
- parser/FFmpeg/image-stack technology choices are not approved;
- relation between future `Artifact` and current `Material` still requires formal domain review.

**Next action:** continue Stage 06 cleanup. Reopen this concept only when an approved OSINT requirement demands heterogeneous file/media ingestion.
