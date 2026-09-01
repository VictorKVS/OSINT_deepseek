# Habr NPA sweep — Stream 1

Date boundary: 2026-09-01 (Europe/Moscow)

Scope: Habr 432466, section «Государственные и муниципальные информационные системы (ГИС и МИС)», positions 22–28. Targets: ПП РФ 21.04.2018 №482; ПП РФ 31.05.2021 №844; ПП РФ 02.09.2021 №1472; ПП РФ 24.07.2021 №1264; ПП РФ 22.12.2021 №2389; ПП РФ 13.05.2022 №860; ПП РФ 07.06.2022 №1040. GitHub copies are non-official discovery candidates only. Currentness and official provenance are tracked independently.

## Normalized GitHub result

| Target | GitHub normative candidate | Classification |
|---|---|---|
| ПП РФ 21.04.2018 №482 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 31.05.2021 №844 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 02.09.2021 №1472 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 24.07.2021 №1264 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 22.12.2021 №2389 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 13.05.2022 №860 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 07.06.2022 №1040 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |

No GitHub result passed the full-body + internal number/date/title identity gate.

## New rejected GitHub hits

| Target | repo | commit | path | size | type | result |
|---|---|---|---|---:|---|---|
| ПП №482/2018 | PaulineP-P/study_project_rag | a80b8d270470bae485852193aa0d68d844149883 | data/raw/evrejskaya-avtonomnaya-oblast-1_ocr.txt | 332261 | TXT / OCR | MENTION_ONLY / REGIONAL_STRATEGY_OCR / REJECTED_AS_NORMATIVE_BODY |
| ПП №1264/2021 | Drunken-Shogun/systems-analyst-knowledge-base | 939f82413f480b69ebd2b9101566e7b9a1464f51 | Системный анализ/Углубленный разбор/Анализ документации.md | 6181 | Markdown | MENTION_ONLY / STUDY_NOTES / REJECTED_AS_NORMATIVE_BODY |

The regional strategy OCR discusses the GIS «Типовое облачное решение…» as a digital-transformation project but is not the body of PP №482. The systems-analysis note contains a one-line normative reference to PP №1264, not its Rules or appendices.

A separate `intuition-team/orb` search hit for №482 was rejected as `SEARCH_FALSE_POSITIVE / NUMERIC_COLLISION`: the number 482 referred to a count of athletes, not to the Government resolution.

## Currentness / lifecycle findings

### ПП РФ №482 от 21.04.2018

Current corroborated edition advanced to 10.05.2026. PP РФ 10.05.2026 №539 directly changes the Regulation approved by №482 and states that №539 enters into force on official publication.

Classification: `CURRENT_EDITION_2026-05-10_CORROBORATED / LATEST_AMENDMENT_PP_539_2026_CONFIRMED`.

Completeness gate: current `FULL_TEXT` means the resolution + complete current Regulation. A pre-№539 body is `STALE_EDITION`.

Direct primary publication pointer for №539 was not resolved in this pass: `PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER`.

### ПП РФ №844 от 31.05.2021

The current legal card still shows edition 01.09.2021. The act has an explicit validity limit: until 1 June 2027, so it is active on 01.09.2026.

Classification: `BUILT_IN_SUNSET_CONFIRMED_2027-06-01 / CURRENTNESS_CORROBORATED_NONPRIMARY`.

Completeness gate: resolution + complete approved Rules. Primary consolidated/current-status proof was not directly resolved in this pass: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### ПП РФ №1472 от 02.09.2021 — Habr title is stale

The current edition is 11.06.2024, effective in the amended wording from 19.06.2024. PP РФ 11.06.2024 №778 changed the act substantially: the current title is in the singular «Об определении информационной системы…» and the description of the authorized federal body was rewritten. Habr still reproduces the original 2021 plural/old-authority title.

Classification: `HABR_TITLE_STALE_ORIGINAL / CURRENT_TITLE_CHANGED_2024 / SAME_ACT_IDENTITY_PRESERVED`.

This is not a different NPA: number, date and act lineage remain №1472/02.09.2021. Primary publication pointer for amendment №778 was not directly resolved in this pass: `PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER`.

### ПП РФ №1264 от 24.07.2021

Current corroborated edition is 04.08.2025 and incorporates PP РФ №1170/2025. The official publication index directly confirms PP №1170: publication number `0001202508050018`, publication date 05.08.2025, PDF 1890 KB / 8 pages.

Classification: `CURRENT_EDITION_2025-08-04_CORROBORATED / LATEST_AMENDMENT_PRIMARY_PUBLICATION_INDEX_CONFIRMED`.

Completeness gate is stricter than a single Rules body: `FULL_TEXT` = resolution + Rules + Appendix №1 (global address directory interaction) + Appendix №2 (notification workflow). The GitHub study note is only a mention.

New source-quality conflict: one secondary legal page labels PP №1170, signed 04.08.2025, as having entered into force on 01.08.2025. That date precedes the act date and is rejected as `SECONDARY_EFFECTIVE_DATE_IMPOSSIBLE_CONFLICT`; it must not be propagated into lifecycle data.

### ПП РФ №2389 от 22.12.2021 — experiment has ended

The resolution itself sets the experiment period from 27.12.2021 through 31.03.2025. Therefore on 01.09.2026 the experiment is no longer current operational regulation even though Habr still lists the act in the main GIS/MIS sequence.

Classification: `HABR_EXPIRED_EXPERIMENT_CONFLICT / EXPERIMENT_ENDED_2025-03-31`.

Gate: `EXPERIMENT_END != FORMAL_REPEAL`. This pass did not directly resolve a primary act that formally repeals №2389, so `PRIMARY_FORMAL_STATUS_AFTER_EXPERIMENT_BLOCKER` remains.

### ПП РФ №860 от 13.05.2022 — old experiment ended; successor exists

PP РФ 18.03.2024 №323 changed the end date in №860 from 30.03.2024 to 31.12.2024. Thus the experiment under №860 ended on 31.12.2024.

A successor experiment is established by PP РФ 26.03.2025 №372 for the period 01.04.2025–31.12.2027 and is therefore active on 01.09.2026.

Classification: `HABR_EXPIRED_EXPERIMENT_CONFLICT / EXPERIMENT_ENDED_2024-12-31 / SUCCESSOR_EXPERIMENT_ACTIVE_PP_372_2025`.

Again, `EXPERIMENT_END != FORMAL_REPEAL`; primary formal-status proof for the old №860 and direct primary publication pointer for successor №372 were not resolved in this pass.

### ПП РФ №1040 от 07.06.2022 — Habr title is stale

Current corroborated edition is 01.11.2025 after PP РФ №1716/2025. The current canonical title says «О федеральной государственной географической информационной системе “Единая цифровая платформа ‘Национальная система пространственных данных’”». Habr still shows the older wording without «географической».

Classification: `HABR_TITLE_STALE_ORIGINAL / CURRENT_TITLE_CHANGED / CURRENT_EDITION_2025-11-01_CORROBORATED`.

Completeness gate: resolution + complete current Regulation, including its current appendix/service structure. Direct primary publication pointer for №1716 was not resolved in this pass: `PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER`.

## New conflicts / blockers

- `HABR_TITLE_STALE_ORIGINAL +2`: №1472/2021, №1040/2022.
- `HABR_EXPIRED_EXPERIMENT_CONFLICT +2`: №2389/2021, №860/2022.
- `SUCCESSOR_EXPERIMENT_ACTIVE +1`: №372/2025 succeeds the ended №860 experiment.
- `BUILT_IN_SUNSET_CONFIRMED +1`: №844 valid through 01.06.2027.
- `SECONDARY_EFFECTIVE_DATE_IMPOSSIBLE_CONFLICT +1`: secondary metadata for №1170/2025 predates the act date.
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER +3`: №539/2026→№482, №778/2024→№1472, №1716/2025→№1040.
- `PRIMARY_FORMAL_STATUS_AFTER_EXPERIMENT_BLOCKER +2`: №2389, №860.
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`.
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`.

## Batch counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `GITHUB_MENTION_ONLY_REJECTED +2`
- `SEARCH_FALSE_POSITIVE_NUMERIC_COLLISION +1`
- `HABR_TITLE_STALE_ORIGINAL +2`
- `HABR_EXPIRED_EXPERIMENT_CONFLICT +2`
- `SUCCESSOR_EXPERIMENT_ACTIVE +1`
- `BUILT_IN_SUNSET_CONFIRMED +1`
- `SECONDARY_EFFECTIVE_DATE_IMPOSSIBLE_CONFLICT +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Gates added / confirmed

- `EXPERIMENT_END != FORMAL_REPEAL`.
- `HABR_ORIGINAL_TITLE != CURRENT_CANONICAL_TITLE` after later amendments.
- `SECONDARY_EFFECTIVE_DATE < ACT_DATE => REJECT_METADATA`.
- `GITHUB_MENTION_OF_EXACT_NUMBER_DATE_TITLE != NORMATIVE_BODY`.
- `CURRENTNESS_VERIFIED_SEPARATELY_FROM_GITHUB_IDENTITY`.

Next boundary: GIS/MIS positions 29 onward — PP РФ №1498/2022, №1152/2022, №335/2024, №929/2024, №900/2024, распоряжение №4154-р/2024, PP РФ №981/2025. №900/2024 is already known from an earlier replacement-edge review but still requires direct GitHub-body search when reached.