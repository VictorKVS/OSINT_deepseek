# Habr NPA sweep — Stream 1 — 2026-08-30 13:53 MSK

Scope: Habr 432466, block «Персональные данные», items 13–21. Item 22 (ПП РФ №1154 от 01.08.2025) was covered in an earlier pass and is not repeated here.

## Delta

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +9`
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +2` — №2526/2022, №538/2025
- `PRIMARY_GOVERNMENT_FULLTEXT_CONFIRMED +1` — №702/2025
- `CURRENT_EDITION_CORROBORATED +1` — №24/2023 → ред. 14.10.2024
- `LATEST_AMENDMENT_RELATION_CONFIRMED +1` — №1371/2024 → №24/2023
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED +5` — №6/2023, №24/2023 (initial), №740/2025, №961/2025, №966/2025
- `SECONDARY_OFFICIAL_SUMMARY_CONFLICT +1` — №538/2025 effective date
- exact duplicate full normative bodies: `+0`
- GitHub target-body identity conflicts: `+0`

GitHub searches were performed by exact/near-exact number + date + distinctive title terms. No reproducible target files or reliable candidates were returned for all nine acts below. Therefore `repo/commit/path/size/type = null` for each; null is intentional and means no GitHub artifact passed candidate intake.

## Per-act results

### ПП РФ от 29.12.2022 №2526

- GitHub: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Identity/title confirmed by full legal-text mirrors.
- Primary official publication confirmed: `0001202212310018`, published 31.12.2022.
- Operative clause: enters into force 01.03.2023.
- No later modifying act was confirmed in this pass; do not infer immutable/unamended status from that absence.
- Completeness gate: `FULL_TEXT = постановление + весь утвержденный перечень`.

### ПП РФ от 10.01.2023 №6

- GitHub: all artifact fields `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Body identity confirmed by exact date/number/title and complete Rules in legal-text sources.
- Official publication pointer corroborated: `0001202301110015`; direct primary card was not stably fetched in this pass.
- Operative clause: enters into force 01.03.2023.
- Completeness gate: `FULL_TEXT = постановление + полные Правила`.

### ПП РФ от 16.01.2023 №24

- GitHub: all artifact fields `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Current consolidated edition corroborated as `14.10.2024`, effective from `23.10.2024`.
- Change chain confirmed in consolidated text: ПП РФ №1356 от 19.08.2023 and ПП РФ №1371 от 14.10.2024.
- №1371 directly changes subparagraph «в» of point 23 of the Rules approved by №24.
- Initial official publication pointer corroborated: `0001202301170011`; direct latest-amendment primary card remains unresolved in this pass.
- Completeness gate: `FULL_TEXT = постановление + полные Правила`; freshness requires both 2023 and 2024 changes.

### ПП РФ от 24.04.2025 №538

- GitHub: all artifact fields `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Primary official publication directly confirmed: `0001202504250043`, published 25.04.2025, official PDF 1214 KB / 5 pages.
- Normative body states entry into force `01.09.2025`.
- Conflict: a Government of Khakassia legislative-summary page states that №538 enters into force on the day of official publication. This conflicts with the operative clause of the normative text. Classify as `SECONDARY_OFFICIAL_SUMMARY_CONFLICT`; do not let the regional summary override the act body.
- Completeness gate: `FULL_TEXT = постановление + полный перечень случаев`.

### ПП РФ от 22.05.2025 №702

- GitHub: all artifact fields `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Primary Government of Russia page reproduces the decree and the approved Rules and exposes a downloadable PDF (2.3 MB): `PRIMARY_GOVERNMENT_FULLTEXT_CONFIRMED`.
- Identity confirmed by exact date/number/title inside the body.
- Effective date corroborated as `01.09.2025`.
- Completeness gate: `FULL_TEXT = постановление + все Правила проверки`.

### ПП РФ от 28.05.2025 №740

- GitHub: all artifact fields `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Identity and complete body are corroborated by legal-text sources; the act designates EIP NSUD as the GIS under Article 13.1 of 152-FZ and amends the EIP NSUD regulation.
- Official publication pointer extracted from the official-link target: `0001202505300061`, publication date 30.05.2025. The primary card itself timed out, so status is `OFFICIAL_PUBLICATION_POINTER_CORROBORATED`, not direct-card verified.
- Effective-date split: point 3 is effective from 28.05.2025; the rest is effective from 01.09.2025.
- A NormaCS catalog marks the document «отменен», but no primary repeal act was confirmed in this pass; this label is **not accepted** as a lifecycle fact and remains a `STATUS_LABEL_CONFLICT_BLOCKER` pending primary proof.
- Completeness gate: `FULL_TEXT = постановление + все утвержденные изменения к Положению об ЕИП НСУД`.

### ПП РФ от 26.06.2025 №961

- GitHub: all artifact fields `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Official publication pointer extracted from official-link target: `0001202506270025`; direct card timed out.
- Full text and identity corroborated; the act contains **two** approved rule sets: formation of anonymized-data compositions and provision of access to them.
- Effective from `01.09.2025`.
- Completeness gate: `FULL_TEXT = постановление + Rules of formation + Rules of access`.

### ПП РФ от 26.06.2025 №966

- GitHub: all artifact fields `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Official publication pointer extracted from official-link target: `0001202506260044`; direct card timed out.
- Current legal-text sources show base edition `26.06.2025`, effective `01.09.2025` and acting; no later amendment was confirmed in this pass.
- The Rules explicitly cover interaction between Minцифры/operators and between the designated GIS/operator information systems, including information-security requirements.
- Completeness gate: `FULL_TEXT = постановление + полные Правила взаимодействия`.

### ПП РФ от 04.07.2025 №1012

- GitHub: all artifact fields `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Exact body identity corroborated by date/number/title and both approved annex-like normative components.
- Official publication date corroborated as `07.07.2025`; direct official publication ID was not resolved in this pass.
- Split effectiveness is material: decree generally effective on official publication, but point 1 becomes effective only `01.01.2026`.
- Completeness gate: `FULL_TEXT = постановление + формат хранения сведений + требования к цифровой фотографии`.

## New corpus gates

1. `OFFICIAL_SUMMARY != NORMATIVE_OPERATIVE_CLAUSE` — even a government-hosted derivative summary can misstate the effective date; lifecycle is taken from the normative act / primary publication.
2. `SPLIT_EFFECTIVE_DATE_REQUIRES_NORM_LEVEL_STORAGE` — №740 and №1012 show that one `effective_from` field for the whole act is insufficient.
3. `CATALOG_STATUS_LABEL != PRIMARY_REPEAL_PROOF` — a commercial/technical catalog marker such as «отменен» is not accepted without a primary repealing/amending act.
4. `CURRENT_EDITION_REQUIRES_CHANGE_CHAIN` — for №24 the current body must preserve both №1356/2023 and №1371/2024, not only the latest change.

## Sources / pointers captured

- Habr 432466, current snapshot title: version 28.05.2026.
- Official publication №2526: https://publication.pravo.gov.ru/Document/View/0001202212310018
- Official publication №538: https://publication.pravo.gov.ru/document/0001202504250043
- Government full text №702: https://government.ru/docs/all/159151/
- Official pointer №740: https://publication.pravo.gov.ru/document/0001202505300061
- Official pointer №961: https://publication.pravo.gov.ru/document/0001202506270025
- Official pointer №966: https://publication.pravo.gov.ru/document/0001202506260044

Next unprocessed queue after this pass starts with the Roskomnadzor / departmental PDn acts following Habr item 22; №1154/2025 itself was already audited earlier.