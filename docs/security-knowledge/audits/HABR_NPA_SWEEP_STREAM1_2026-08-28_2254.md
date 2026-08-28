# Habr NPA sweep — Stream 1 — 2026-08-28 22:54 MSK

## Delta

- `TRANSLATED_FULL_TEXT +1`
- `STALE_CONSOLIDATION +1`
- `SIZE_METADATA_BLOCKER +1`
- `EXACT_DUPLICATE +0`

## Federal Law No. 152-FZ of 27 July 2006 "On Personal Data"

### GitHub candidate

- repo: `MobileCommerceLab/privacy_law_corpus`
- commit/ref: `1d791bb64741f86f8cc160485dc005230f720042`
- path: `corpus_documents/plain_text_files/english_text_files/english_translated_text_files/Russia (Federal Law of 27 July 2006 No. 152-FZ on Personal Data).txt`
- type: `TXT/blob`
- blob SHA: `135c36cf9de20bb95adf255069cfd662bc1ee5fd`
- size: `UNRESOLVED_METADATA_BLOCKER` — exact byte count was not returned by the connector; no estimate recorded.

### Body identity check

The body independently identifies the target act as `FEDERAL LAW NO. 152-FZ OF JULY 27, 2006 ON PERSONAL DATA`, records adoption by the State Duma on 8 July 2006 and approval by the Federation Council on 14 July 2006, contains the chapter/article structure through Article 25, and ends with the President / Moscow Kremlin / 27 July 2006 / No. 152-FZ signature block. Therefore this is a translated full normative text rather than a mention, card, or summary.

The header explicitly states consolidation through Federal Law No. 519-FZ of 30 December 2020. No later amendments are represented in this copy.

### Official identity and currency check

Primary official identity was checked independently against the President of Russia legal acts bank: Federal Law of 27.07.2006 No. 152-FZ, "On Personal Data". The official consolidated text exposed there contains amendments at least through Federal Law No. 23-FZ of 28.02.2025.

A later amendment exists after that snapshot: Federal Law No. 265-FZ of 26.07.2026 directly amends Article 12 of 152-FZ. Its official-publication identifier is `0001202607260024`; the published law states that Article 1 amendments to 152-FZ enter into force on the day of official publication, while Article 2 has a deferred effective date of 01.09.2027.

Accordingly, the GitHub translation consolidated only through 30.12.2020 is legally stale and cannot be used as the current normative text.

### Classification

`TRANSLATED_FULL_TEXT / ENGLISH_TRANSLATION / NON_OFFICIAL_GITHUB_COPY / CONSOLIDATED_THROUGH_519-FZ_2020 / STALE / NOT_RUSSIAN_CANONICAL_TEXT`

### Open blockers

1. A Russian-language GitHub copy of 152-FZ that is both full-text and sufficiently current has not yet been confirmed in this pass.
2. Exact byte size of the translated blob remains unresolved in connector metadata.
3. GitHub provenance does not confer official status; official identity and lifecycle remain a separate verification layer.

## Regression gate

`TRANSLATED_FULL_TEXT` may be useful for search/RAG alignment but must never satisfy the `RUSSIAN_CANONICAL_CURRENT_TEXT` acceptance gate. A consolidation cut-off must be parsed from the body/header and compared against independently verified later amendments before ingestion into the current-law layer.
