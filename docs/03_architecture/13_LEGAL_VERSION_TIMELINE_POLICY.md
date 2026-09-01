# Legal Version Timeline Policy

Status: P0 Knowledge Factory architectural rule.

## Decision

For Russian legal Knowledge Factory material, GARANT is the preferred **working navigator of the document timeline** because one document page exposes amendment acts, edition chronology, effective-date notes, previous/future edition references and consolidated current text.

GARANT is **not** promoted to official-publication evidence. The roles stay separate:

1. `VERSION_TIMELINE_PROVIDER` — preferred: GARANT (`A2_AUTHORITATIVE`).
2. `CONSOLIDATED_REFERENCE` — independent cross-check: ConsultantPlus (`A2_AUTHORITATIVE`).
3. `PUBLICATION_EVIDENCE` — official publication/state evidence (`A0/A1`).
4. `GOVERNMENT_COPY` — state-hosted downloadable/inspectable copy (`A1`).

Rule: **GARANT navigates; A0/A1 proves.**

## Why

A legal KB must answer not only “what does the document say now?” but also:

- what edition was in force on date X;
- which act changed a clause;
- when the amendment became effective;
- whether a future edition already exists;
- what text was superseded;
- whether two authoritative consolidated systems disagree;
- which official publication proves each temporal change.

A single downloaded current document cannot answer these questions reliably.

## Timeline flow

```text
GARANT page / authorized saved representation
        ↓
metadata-only timeline extraction
        ↓
amending act identity + act date + effective rule/date(s)
        ↓
OFFICIAL_EVIDENCE_PENDING
        ↓
A0/A1 acquisition / publication verification
        ↓
ConsultantPlus consolidated cross-check
        ↓
MATCH | VERSION_DIFFERENCE | SOURCE_CONFLICT
        ↓
expert review
        ↓
confirmed edition/version graph
```

## Copyright and provenance boundary

The timeline extractor records only legal/temporal metadata needed for provenance and edition routing. It does not mirror GARANT commentary or full legal text into Git. Saved source pages remain under ignored local operator-import storage. Public exports contain source URL, identifiers, dates, status and evidence requests only.

## Minimum timeline event

Every amendment candidate contains:

- parent `document_id`;
- amending act type/title;
- amending act number;
- amending act date;
- explicit effective date(s), when present;
- otherwise the effective-date rule as observed;
- timeline source ID and URL;
- `OFFICIAL_EVIDENCE_PENDING` state until A0/A1 confirmation.

No date is invented when the source states only a rule such as “after official publication”.

## Promotion gate

A timeline hint from A2 can create a research/evidence request, but it cannot by itself promote a legal edition to confirmed/KB-ready status.

Before a legal version becomes confirmed, the system must attach sufficient A0/A1 evidence for the amendment/publication/effective-date claim or mark the gap explicitly for expert review.

## Temporal graph targets

Later graph stages should support at least:

- `DOCUMENT_HAS_EDITION`;
- `EDITION_SUPERSEDES_EDITION`;
- `DOCUMENT_AMENDED_BY`;
- `AMENDMENT_EFFECTIVE_FROM`;
- `EDITION_VALID_DURING`;
- `EDITION_PROVEN_BY`;
- `EDITION_CROSSCHECKED_BY`;
- `VERSION_DIFFERENCE`;
- `SOURCE_CONFLICT`.

Stable document identity remains constant while editions/versions and their evidence are append-only.

## MVP acceptance

For the PDn vertical:

1. every source bundle has a preferred GARANT timeline provider;
2. ConsultantPlus remains an independent A2 cross-check;
3. timeline extraction is metadata-only and local-input based;
4. amendment events generate A0/A1 evidence requests;
5. full legal text from GARANT is not mirrored into public Git;
6. no timeline event is treated as officially proven before the evidence gate.
