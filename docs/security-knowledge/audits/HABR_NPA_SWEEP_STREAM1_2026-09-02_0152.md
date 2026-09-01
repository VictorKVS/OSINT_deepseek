# Habr NPA sweep — Stream 1 — 2026-09-02 01:52 MSK

Scope: Habr 432466, section `Персональные данные (ПДн)`, positions 7–14. GitHub copies are treated only as evidence/candidates; official status is tracked independently.

## Batch summary

Unique targets: 8.

- `GITHUB_FULL_TEXT_CURRENT_BY_CONSOLIDATED_EDITION_MATCH +1` — PP RF No. 512/2008.
- `GITHUB_FULL_TEXT_OLD_EDITION +1` — PP RF No. 687/2008.
- `GITHUB_FULL_TEXT_BLOCKER +6` — Presidential Decrees No. 1709/2012, No. 735/2014, CIS Agreement 18.12.2020, PP RF No. 1046/2021, No. 2526/2022, No. 6/2023.
- `GITHUB_MENTION_OR_PARTIAL_QUOTE_REJECTED +4` — No.735 web-index dataset; PP687 two partial quote/test-fixture files; PP1046 educational notes.
- `GITHUB_PATH_METADATA_DATE_CONFLICT +1` — PP687 candidate filename says `15 December 2008`, body correctly says `15 сентября 2008 г.`.
- `POST_HABR_CURRENT_EDITION_ADVANCE +1` — PP1046 amended 03.07.2026 by PP833, after Habr version 28.05.2026.
- `BUILT_IN_SUNSET_2030-09-01 +1` — PP687 after PP12/2025.
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`.
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`.

## Records

### PDn-07 — Presidential Decree 29.12.2012 No. 1709

GitHub exact-title, number/date and distinctive-body searches: no full body or reliable candidate.

- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- GitHub class: `GITHUB_FULL_TEXT_BLOCKER`

Identity/current layer: consolidated legal text confirms the exact decree and edition `07.12.2016`; Presidential Decree No.656 of 07.12.2016 amended No.1709. Direct primary presidential/original fetch was not resolved in this pass.

Blocker: `PRIMARY_PRESIDENTIAL_ORIGINAL_DIRECT_FETCH_BLOCKER`.

### PDn-08 — Presidential Decree 24.11.2014 No. 735

No GitHub body. One exact-title hit is only a dataset/index record pointing to a Ministry of Foreign Affairs page:

- repo: `giocomai/tadadit`
- commit: `fe512d26e0dfcfa29f6808903a9caeeb5b01f8cf`
- path: `datasets/2024/russian_institutions_2024/mid.ru_ru_2024/website_name-no_text.csv`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `CSV`
- class: `MENTION_ONLY / WEB_INDEX_DATASET / REJECTED_AS_NORMATIVE_BODY`

Distinctive-body search returned no normative body. Secondary current text shows the original decree; no amendment was confirmed in this pass. Direct primary presidential fetch remains unresolved.

Blocker: `PRIMARY_PRESIDENTIAL_ORIGINAL_DIRECT_FETCH_BLOCKER`.

### PDn-09 — CIS Agreement 18.12.2020 on mutual administrative legal assistance in personal-data exchange

No GitHub full text/reliable candidate found.

- repo/commit/path/size/type: `null`
- class: `GITHUB_FULL_TEXT_BLOCKER`

The agreement structure and Articles 1–17 are confirmed by legal text. An official Kazakhstan government source confirms the agreement entered into force generally on `06.08.2023`; this pass did not close the Russia-specific depositary/effective-date chain from a primary Russian/depositary source.

Blockers: `PRIMARY_DEPOSITARY_ORIGINAL_BLOCKER`, `RUSSIA_SPECIFIC_DEPOSITARY_EFFECTIVE_DATE_PRIMARY_BLOCKER`.

### PDn-10 — PP RF 06.07.2008 No. 512

New GitHub full-body find:

- repo: `MobileCommerceLab/privacy_law_corpus`
- commit: `1d791bb64741f86f8cc160485dc005230f720042`
- path: `corpus_documents/plain_text_files/non_english_text_files/Russia (Decree of the Government of 6 July 2008 No. 512 on Approving the Requirements to Biometric Personal Data Tangible Carrier and such Data Storage Outside of Personal Data Information Systems).txt`
- blob: `6c15cbb6726e9815e160e9acb6061b38381ddb4c`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `text/plain`
- class: `GITHUB_FULL_TEXT_CURRENT_BY_CONSOLIDATED_EDITION_MATCH / NON_OFFICIAL_COPY`

Internal identity check: body says `от 6 июля 2008 г. N 512`, exact Russian title, and contains the decree plus attached Requirements. Edition marker inside body: `от 27.12.2012 г. N 1404`. Consolidated legal text also reports edition 27.12.2012. GitHub copy is not an official publication.

Blocker: `PRIMARY_GOVERNMENT_ORIGINAL_DIRECT_FETCH_BLOCKER` (current-edition match is not itself a primary-source status proof).

### PDn-11 — PP RF 15.09.2008 No. 687

New GitHub full-body historical/original find:

- repo: `MobileCommerceLab/privacy_law_corpus`
- commit: `1d791bb64741f86f8cc160485dc005230f720042`
- path: `corpus_documents/plain_text_files/non_english_text_files/Russia (Decree of the Government of 15 December 2008 No. 687 on Approving the Provision Regarding Properties of Personal Data Processing without Software).txt`
- blob: `d75270aeb0e5291a9f77e53783c1541510b7139c`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `text/plain`
- class: `GITHUB_FULL_TEXT_OLD_EDITION / NON_OFFICIAL_COPY`

Internal identity check: body correctly says `от 15 сентября 2008 г. N 687` and exact title, followed by the attached Regulation. The filename says `15 December 2008`: `PATH_DATE_CONFLICT`, while body identity is correct.

Current official status: Government of Russia current text is explicitly `в редакции ... от 18.01.2025 №12`; point 3 now says the regulation operates until `01.09.2030`. Official publication portal confirms PP No.12/2025, publication No. `0001202501180009`, published 18.01.2025. Therefore the GitHub body is not current even though it is a full target body.

Rejected side hits: `asmi046/dentalica@3c7de1d4c4f1e0993ad755216ba936e5c757e7f1 public/old_data/policy.html` and `ispras/dedoc@40dde1bc2e46b1b00b7058080c1228615b983424 tests/data/htmls/53.html` only quote/reference fragments; neither is a normative body.

### PDn-12 — PP RF 29.06.2021 No. 1046

No GitHub body. One educational-notes hit:

- repo: `IKarasev/Study`
- commit: `46d89cc6ac468698dcc56c9706f744749ed84b8d`
- path: `norm_obespechenie/03 Комплаенс.md`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `Markdown`
- class: `MENTION_ONLY / EDUCATIONAL_NOTES / REJECTED_AS_NORMATIVE_BODY`

Current layer advanced after the Habr snapshot: PP RF No.833 of `03.07.2026` directly amends point 57 of the Regulation under No.1046; publication No. `0001202607030035`; effective `11.07.2026`. Therefore any GitHub copy of the prior edition must be marked `OLD_EDITION`.

Class: `CURRENT_EDITION_ADVANCED_1046_2026-07-03 / POST_HABR_CURRENT_EDITION_ADVANCE`.

Primary direct publication-page fetch for No.833 was not resolved in this pass; publication pointer was independently resolved from indexed legal sources.

Blocker: `PRIMARY_LATEST_AMENDMENT_DIRECT_FETCH_BLOCKER`.

### PDn-13 — PP RF 29.12.2022 No. 2526

No GitHub full body/reliable candidate.

- repo/commit/path/size/type: `null`
- class: `GITHUB_FULL_TEXT_BLOCKER`

Full legal text and publication date 31.12.2022 are confirmed from consolidated legal sources; no later amendment was found in this pass. Exact official publication identifier/direct primary card was not resolved.

Blocker: `PRIMARY_PUBLICATION_POINTER_BLOCKER`.

### PDn-14 — PP RF 10.01.2023 No. 6

No GitHub full body/reliable candidate.

- repo/commit/path/size/type: `null`
- class: `GITHUB_FULL_TEXT_BLOCKER`

Exact identity and effective date `01.03.2023` are confirmed by legal text; no later amendment was found in this pass. Exact official publication identifier/direct primary card was not resolved.

Blocker: `PRIMARY_PUBLICATION_POINTER_BLOCKER`.

## Next boundary

Continue PDn positions 15+: PP RF No.24/2023, No.538/2025, No.702/2025, No.740/2025, No.961/2025, No.966/2025, then the remaining government and Roskomnadzor layer. Preserve cross-section deduplication and primary-source status gates.
