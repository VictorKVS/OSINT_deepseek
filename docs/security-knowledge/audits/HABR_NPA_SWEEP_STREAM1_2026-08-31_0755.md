# Habr NPA sweep — Stream 1 — 2026-08-31 07:55 MSK

## Scope
Continuation of systematic review of Habr 432466 (`Государственные регуляторы`), targets:

1. Federal Law 10.07.2002 No. 86-FZ — Central Bank of Russia.
2. Presidential Decree 16.08.2004 No. 1082 — Ministry of Defence.
3. Presidential Decree 23.07.2013 No. 631 — General Staff.
4. Presidential Decree 13.10.2004 No. 1313 — Ministry of Justice.
5. Presidential Decree 11.07.2004 No. 865 — Ministry of Foreign Affairs.
6. Presidential Decree 14.04.2022 No. 203 — Security Council commission on technological sovereignty / CII.
7. Presidential Decree 10.11.2018 No. 648 — Security Council commission on information security, positional composition.

Habr reference: https://habr.com/ru/articles/432466/

## GitHub body search

Exact number/date/title searches were performed for all seven targets. No full normative body and no reliable normative-body candidate was found.

| target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| 86-FZ/2002 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Decree 1082/2004 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Decree 631/2013 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Decree 1313/2004 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Decree 865/2004 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Decree 203/2022 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Decree 648/2018 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

### Rejected lexical hits
Search for Decree 1082 produced two word-sense/translation corpus hits in `mk322/contextual-word-level-translation`, commit `ae0d84cf65555193a4841b8bfc304d6bbf7159c0`:

- `xl-wsd-files/Korean/all_sense_labels_ko_ru.txt`
- `xl-wsd-files/Italian/all_sense_labels_it_ru.txt`

They are lexical datasets, not mentions/notes or normative bodies. Classification: `FALSE_POSITIVE_LEXICAL_CORPUS`; they are not candidates and do not populate target `repo/commit/path/size/type`.

## New confirmed lifecycle/current-edition evidence

### Federal Law No. 86-FZ of 10.07.2002
Habr target identity is correct. Current consolidated legal systems show edition 04.08.2026 with amendments/effects staged across dates.

- Federal Law No. 334-FZ of 04.08.2026 directly amends part 5 of article 74 of 86-FZ and enters into force on official publication. Corroborated official publication pointer: `0001202608040078`, 04.08.2026.
- Federal Law No. 283-FZ of 04.08.2026 directly amends 86-FZ in article 9. Main effective date: 01.09.2026. Subparagraph `a` of point 8 of article 9 enters into force only 01.03.2027. Corroborated official publication pointer: `0001202608040008`, 04.08.2026.

Status at 2026-08-31: `CURRENT_EFFECTIVE_LAYER + ENACTED_FUTURE_CHANGE_2026-09-01 + ENACTED_FUTURE_CHANGE_2027-03-01`. Gate: a consolidated edition date does not mean every provision in that edition is effective now.

Completeness: `FULL_TEXT` means the complete law body for the requested temporal state; a future-consolidated copy must not be silently treated as the current effective body.

### Presidential Decree No. 1082 of 16.08.2004
Current edition corroborated as 27.07.2026. Decree No. 526 of 27.07.2026 directly amends No. 1082; it takes effect 01.08.2026. Corroborated official publication pointer: `0001202607270022`, 27.07.2026.

Completeness: Decree shell + current `Положение о Министерстве обороны Российской Федерации`; shell-only copies are `PARTIAL_TEXT`.

### Presidential Decree No. 631 of 23.07.2013
Current edition corroborated as 26.02.2024. Decree No. 141 of 26.02.2024 amends the Regulation attached to No. 631. Primary publication of No. 141 confirmed directly on publication.pravo.gov.ru: `0001202402260031`, 26.02.2024.

Completeness: Decree + full current `Положение о Генеральном штабе Вооруженных Сил Российской Федерации`.

### Presidential Decree No. 1313 of 13.10.2004 — Habr conflict
Official Ministry of Justice text of Presidential Decree No. 10 of 13.01.2023 states in clause 3 that decrees in the appendix are repealed; item 1 of the appendix explicitly lists Decree No. 1313 of 13.10.2004. Decree No. 10 entered into force on signing and is the current regulatory basis for the Ministry of Justice (later amended in 2023 and 2025).

Status: `REPEALED_EFFECTIVE_2023-01-13 / PRIMARY_REPEAL_CLAUSE_DIRECT_VERIFIED / HABR_REPEALED_ACT_CONFLICT`. Habr 28.05.2026 still lists No. 1313 in the regulator block.

Official Minjust source: https://minjust.gov.ru/ru/documents/7178/

### Presidential Decree No. 865 of 11.07.2004
Current edition corroborated as 03.04.2026. Decree No. 226 of 03.04.2026 directly amends No. 865 and enters into force on signing. Corroborated official publication pointer: `0001202604030006`, 03.04.2026.

Completeness: Decree + current `Положение о Министерстве иностранных дел Российской Федерации`.

### Presidential Decree No. 203 of 14.04.2022
Current edition corroborated as 30.03.2026. Primary official publication confirms Decree No. 207 of 30.03.2026 directly amends the positional composition approved by No. 203: `0001202603300006`, 30.03.2026.

No. 203 approves both the Regulation and the positional composition. Completeness therefore requires `decree + Regulation + current positional composition`; a copy containing only the Regulation is `PARTIAL_TEXT`.

Primary source: https://publication.pravo.gov.ru/ (publication No. 0001202603300006).

### Presidential Decree No. 648 of 10.11.2018
Current edition corroborated as 16.02.2026. Primary official publication confirms Decree No. 88 of 16.02.2026 amends the composition approved by No. 648: `0001202602160011`, 16.02.2026.

No. 88 also repeals earlier amending Decree No. 298 of 24.04.2023. This does **not** repeal or roll back target No. 648; the new amendment supersedes the historical amending act after its changes were absorbed into the target lifecycle.

Status event: `AMENDING_ACT_REPEALED_AFTER_SUPERSESSION != TARGET_REPEALED`.

Completeness: the current positional composition is the substantive body; a shell without the composition is `PARTIAL_TEXT`.

## New counts

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `FALSE_POSITIVE_LEXICAL_CORPUS +2`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_REPEALED_ACT_CONFLICT +1` (Decree 1313/2004)
- `PRIMARY_REPEAL_CLAUSE_DIRECT_VERIFIED +1`
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED +3` (631 via 141; 203 via 207; 648 via 88)
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED +4` (86-FZ via 283/334; 1082 via 526; 865 via 226)
- `ENACTED_FUTURE_CHANGE +2` for 86-FZ (01.09.2026; 01.03.2027)
- `AMENDING_ACT_REPEALED_AFTER_SUPERSESSION +1` (648 lifecycle)

## New corpus gates

1. `CONSOLIDATED_EDITION_DATE != EVERY_PROVISION_EFFECTIVE_NOW`.
2. `FUTURE_CONSOLIDATED_BODY != CURRENT_EFFECTIVE_BODY`.
3. `FULLTEXT_FOR_ORGAN_REGULATION = ACT_SHELL + CURRENT_ATTACHED_REGULATION`.
4. `FULLTEXT_FOR_COMMISSION_ACT = ACT_SHELL + REGULATION_IF_ANY + CURRENT_POSITIONAL_COMPOSITION`.
5. `REPEAL_OF_PRIOR_AMENDING_ACT_AFTER_NEW_AMENDMENT != REPEAL_OR_ROLLBACK_OF_TARGET`.
6. `HABR_LISTING_OF_REPEALED_REGULATOR_ACT != CURRENT_LEGAL_BASIS`.

## Next queue
Habr `Техническое регулирование`:

1. 184-FZ of 27.12.2002 — technical regulation.
2. 102-FZ of 26.06.2008 — uniformity of measurements.
3. 162-FZ of 29.06.2015 — standardization.
4. Government Resolution No. 1567 of 30.12.2016.
5. Ministry of Digital Development Order No. 486 of 22.09.2020.

Already closed targets are to be re-counted only if a new GitHub body, new primary lifecycle evidence, amendment/repeal, or current-edition change appears.