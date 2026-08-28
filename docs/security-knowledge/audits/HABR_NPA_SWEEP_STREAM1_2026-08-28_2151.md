# Habr NPA sweep — Stream 1 — 2026-08-28 21:51 +03

## Delta

- `TRANSLATED_FULL_TEXT +1`
- `EXACT_DUPLICATE_SET +1` (2 paths, same Git blob)
- `NUMBER_COLLISION +1`
- `SEARCH_FALSE_POSITIVE +1`
- `RUSSIAN_CANONICAL_FULL_TEXT +0`

## 1. Federal Law No. 242-FZ of 21 July 2014 — PD localization amendments

Repository: `MobileCommerceLab/privacy_law_corpus`
Commit: `1d791bb64741f86f8cc160485dc005230f720042`
Type: `TXT/blob`
Blob SHA: `71158b1a70ee9cd1621a8a03a23612e3f4ac6bb5`
Size: `METADATA_BLOCKER` — exact byte size was not exposed by the GitHub connector in this pass; not estimated.

Exact duplicate paths:

1. `corpus_documents/plain_text_files/non_english_text_files/Russia (Federal Law No. 242-FZ of 21 July 2014 on amending Some Legislative Acts of the Russian Federation in as Much as it concerns Updating the Procedure for Personal Data Processing in Information-Telecommunication Networks).txt`
2. `corpus_documents/plain_text_files/english_text_files/english_translated_text_files/Russia (Federal Law No. 242-FZ of 21 July 2014 on amending Some Legislative Acts of the Russian Federation in as Much as it concerns Updating the Procedure for Personal Data Processing in Information-Telecommunication Networks).txt`

Body verification: the file contains the full English translation of the federal law: type of act, date `21 July 2014`, number `242-FZ`, title, adoption by the State Duma on 4 July 2014, approval by the Federation Council on 9 July 2014, Articles 1–4, and the closing signature block `President of the Russian Federation V. PUTIN / Moscow, The Kremlin / July 21, 2014 / No. 242-FZ`. The corpus file also includes the surrounding scrape/navigation material from the Roskomnadzor Personal Data Portal.

Classification: `TRANSLATED_FULL_TEXT / ENGLISH_TRANSLATION / NON_OFFICIAL_GITHUB_COPY / SOURCE_ATTRIBUTED_TO_RKN_PORTAL / NOT_RUSSIAN_CANONICAL_TEXT`.

Primary official identity check: official publication portal confirms Federal Law dated 21.07.2014 No. 242-FZ, title «О внесении изменений в отдельные законодательные акты Российской Федерации в части уточнения порядка обработки персональных данных в информационно-телекоммуникационных сетях», official publication No. `0001201407220042`, publication date 22.07.2014. This verifies the legal identity, not the official status of the GitHub copy.

## 2. Hard number collision: 242-FZ

Two different federal laws share the number `242-ФЗ`:

- `03.12.2008 № 242-ФЗ` — «О государственной геномной регистрации в Российской Федерации»;
- `21.07.2014 № 242-ФЗ` — amendments concerning personal-data processing/localization in information-telecommunication networks.

Gate: `ACT_NUMBER_WITHOUT_DATE_AND_TITLE = HARD_AMBIGUITY`.

The 2014 translated full text above does **not** close the blocker for the 2008 genomic-registration law.

### Rejected candidates for 242-FZ / 03.12.2008

- Repo `Chepenkoroman/duma_analysis`, commit `3875b7e726b2ad4af6f859fba85922360b84bfbe`, path `data/txt_output/508.txt`, type `TXT`: State Duma plenary transcript / parliamentary material, not the enacted law body. Classification: `PARLIAMENTARY_TRANSCRIPT / MENTION_CONTEXT / NOT_FULL_TEXT`.
- Repo `z0tedd/Auto-lawyer`, commit `bf09910fd953209dbb3fae50fe1d10c5792c9129`, path `KnowledgeBase/СВО/Контрактники/Поиск военнослужащего/Сдача ДНК/Сдача ДНК.txt`, type `TXT`: practical DNA-submission guide citing 242-FZ/2008 as a legal basis. Classification: `SECONDARY_PROCEDURE_GUIDE / MENTION_ONLY / NOT_FULL_TEXT`.

Blocker remains: `GITHUB_FULL_TEXT: 242-ФЗ / 03.12.2008`.

## 3. 247-FZ / 31.07.2020 — false positive

Repo: `Gevork23/dissertacia_project`
Commit: `8b48b17c22f269b55b2903b408459e863d8fe61f`
Path: `regression/ruslawod_pairs/pair_0018/new.txt`
Type: `TXT/blob`
Blob SHA: `9d95f6cbcecedb56280302349a6fc31c97ce133f`

Body verification shows **Government Resolution of the Russian Federation dated 08.05.2025 No. 612**, amending Government acts and referring to the Federal Law «Об обязательных требованиях в Российской Федерации». It is not the target Federal Law No. 247-FZ itself. Classification: `SEARCH_FALSE_POSITIVE / DIFFERENT_ACT_PP612_2025 / TITLE_CROSS_REFERENCE_TO_TARGET / REJECT_FOR_TARGET`.

Primary official identity check for the target: official publication portal confirms Federal Law dated 31.07.2020 No. 247-FZ «Об обязательных требованиях в Российской Федерации», publication No. `0001202007310002`, publication date 31.07.2020.

Blocker remains: `GITHUB_FULL_TEXT: 247-ФЗ / 31.07.2020`.

## 4. Roskomnadzor 180 / 187

No new standalone GitHub full text confirmed in this pass. Search hits remain secondary/reference material only. Official identity of Order No. 180 is separately confirmed by the official publication portal: 28.10.2022 No. 180, registered 15.12.2022 No. 71532, official publication No. `0001202212150022` dated 15.12.2022. Do not promote secondary GitHub references to normative full text.

## Regression / ingestion gates

- `ACT_NUMBER_WITHOUT_DATE_AND_TITLE = HARD_AMBIGUITY`
- `TRANSLATED_FULL_TEXT != RUSSIAN_CANONICAL_TEXT`
- `SAME_BLOB_SHA = EXACT_DUPLICATE` before semantic ingestion
- `CROSS_REFERENCE_TO_TARGET != TARGET_DOCUMENT`
- `GITHUB_COPY != OFFICIAL_SOURCE`
