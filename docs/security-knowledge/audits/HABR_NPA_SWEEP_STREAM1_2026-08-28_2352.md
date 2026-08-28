# Habr NPA sweep — Stream 1 — 2026-08-28 23:52 MSK

Scope: continuing systematic pass over Habr 432466 and the user NPA list. GitHub artifacts are treated as non-official unless separately proven; legal identity and lifecycle/currentness are verified independently.

## New confirmed findings

### 1. Federal Law 26.07.2017 No. 187-FZ — FULL_TEXT, original version
- repo: `MobileCommerceLab/privacy_law_corpus`
- commit/ref: `1d791bb64741f86f8cc160485dc005230f720042`
- path: `corpus_documents/plain_text_files/non_english_text_files/Russia (Federal Law of 26 July 2017 No. 187-FZ on Security of Critical Information Infrastructure of the Russian Federation).txt`
- blob: `4a8cd17bcd5fe4bd65b05afb40a999a2fdef821e`
- type: `TXT/blob`
- size: `UNRESOLVED` — GitHub connector returned content/blob SHA but not exact byte length; do not estimate.
- body identity: PASS — `ФЕДЕРАЛЬНЫЙ ЗАКОН`, exact title, State Duma 12.07.2017, Federation Council 19.07.2017, Articles 1–15, terminal presidential signature, `Москва, Кремль`, `26 июля 2017 года`, `№ 187-ФЗ`.
- completeness: PASS — terminal Article 15 and signature are present; this is not a summary/cross-reference.
- version: original 2017 text; no consolidation markers observed.
- official identity: official publication portal confirms Federal Law 26.07.2017 No. 187-FZ, publication No. `0001201707260023`, publication date 26.07.2017.
- currentness: STALE — official `pravo.gov.ru` confirms direct amendment by Federal Law 07.04.2025 No. 58-FZ, official publication No. `0001202504070004`.
- classification: `FULL_TEXT / ORIGINAL_VERSION / NON_OFFICIAL_GITHUB_COPY / STALE_AT_LEAST_BEFORE_58-FZ_2025`.
- blocker closed: `GITHUB_FULL_TEXT: 187-ФЗ/2017`.
- blocker remains: current consolidated GitHub copy not confirmed; exact byte size unresolved.

### 2. Federal Law 27.07.2006 No. 149-FZ — correct-header but truncated polluted scrape
- repo: `MobileCommerceLab/privacy_law_corpus`
- commit/ref: `1d791bb64741f86f8cc160485dc005230f720042`
- path: `corpus_documents/plain_text_files/non_english_text_files/Russia (Federal Law of 27 July 2006 No. 149-FZ on Information, Information Technologies and Protection of Information).txt`
- blob: `3e25be77abb21df87f8708ca443578be5d979398`
- type: `TXT/blob`
- size: `UNRESOLVED` — connector did not expose exact byte length; do not estimate.
- body identity: target header is correct (`149-ФЗ`, 27.07.2006, exact title; Duma 08.07.2006; Federation Council 14.07.2006).
- scrape quality: FAIL — website navigation/UI/sidebar text is interleaved with the normative body.
- completeness: FAIL — file terminates during Article 2, definition item 20; Articles 3+ and final presidential signature are absent.
- apparent consolidation header: contains amendment chain through at least 09.03.2021 No. 43-FZ, but this does not cure truncation.
- currentness: STALE — official source confirms later direct amendment to 149-FZ by Federal Law 29.12.2025 No. 568-FZ, official publication No. `0001202512290056`.
- classification: `TRUNCATED_SCRAPE / BODY_UI_INTERLEAVING / CORRECT_TARGET_HEADER / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY / STALE / REJECT_FOR_PRIMARY_KB`.
- blocker remains: reliable standalone full current GitHub text of 149-FZ not yet confirmed.

## Duplicates / conflicts
- exact duplicates: `0` new.
- legal-identity conflicts: `0` new.
- quality conflict: `+1` — correct target header and amendment metadata coexist with a truncated/polluted body (149-FZ candidate).

## New acceptance gates
1. `CORRECT_HEADER + AMENDMENT_CHAIN != FULL_TEXT` — completeness requires terminal-structure verification (expected last article / signature) rather than trusting title/header metadata.
2. `CORPUS_TRUST != FILE_TRUST` — each artifact must pass body-level validation even inside a repository that also contains confirmed full texts.
3. `UI_SIDEBAR_INTERLEAVING => SCRAPE_QUALITY_FAIL` for the canonical primary-NPA layer unless a clean normative body is separately reconstructed and verified.
4. `FULL_TEXT != CURRENT` — original historical text may close the GitHub-full-text discovery blocker but cannot enter the current-law layer without lifecycle verification.
