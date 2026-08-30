# Habr NPA sweep — Stream 1 — 2026-08-30 07:55 MSK

Source snapshot: Habr article 432466, version dated 2026-05-28, plus the user-maintained NPA queue.

## Delta for this pass

- targets processed: 6
- GITHUB_FULL_TEXT_CONFIRMED: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +6
- SEARCH_HITS_REJECTED_AS_NON_TARGET: +3 for the 5-FZ search; 2 unique newly inspected paths, of which one is a parsed derivative of an already-known non-target source
- CURRENT_EDITION_CORROBORATED: +6
- LATEST_AMENDMENT_RELATION_CONFIRMED: +6
- OFFICIAL_PUBLICATION_POINTER_CONFIRMED_FOR_LATEST_AMENDMENT: +5 exact publication IDs (Decree 90/2022; PP 1557/2024; PP 42/2026; FZ 442/2025; PP 612/2026)
- OFFICIAL_RG_LATEST_AMENDMENT_FULLTEXT_CONFIRMED: +1 (FZ 83/2019 -> FZ 5/1994)
- TEMPORAL_DEPENDENCY_RESOLVED: +1 (PP 612/2026 becomes effective on 2026-05-28 together with FZ 442/2025)
- exact full-body duplicates: +0
- new target-body identity conflicts: +0

Habr presence for this pass:
- foundations: FZ 5/1994, Presidential Decree 763/1996, PP 1009/1997;
- system-forming: PP 1722/2020;
- special PD processing: FZ 168/2020 and PP 1723/2021.

## Findings

### 1. Federal Law 14.06.1994 No. 5-FZ
Target: `О порядке опубликования и вступления в силу федеральных конституционных законов, федеральных законов, актов палат Федерального Собрания`.

GitHub:
- exact title/date search returned no target body.
- broader search produced three non-target paths. Newly inspected false positive:
  - repo: `Grantik/odin-vault`
  - commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
  - path: `canon/sources/originals-text/FZ-422_2018-11-27.md`
  - blob SHA: `5978c9fda27b4efc93f2ea6645a341bfd7d72588`
  - size: `87762` bytes
  - type: `Markdown/file`
  - body identity: Federal Law 27.11.2018 No. 422-FZ on the professional-income-tax experiment, not FZ 5/1994.
  - classification: `SEARCH_FALSE_POSITIVE / WRONG_PRIMARY_BODY / REJECT`.
- the other hits resolve to `minekonom_prikaz_67_gis_ekonomika.txt` (already-known wrong body) and its parsed derivative `sync/canon/package/samples/parsed/minekonom_prikaz_67_gis_ekonomika.md`, SHA `388b65a0878ebef8f254f468808c3426ef19fd36`, size `189374`, `Markdown/file`; the parsed body explicitly identifies MinEconomy Order 18.02.2022 No. 67 and therefore is not FZ 5/1994.
- target metadata remain `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current legal full-text sources consistently identify the current edition as `01.05.2019`.
- Federal Law 01.05.2019 No. 83-FZ directly amends Article 9.1 of FZ 5/1994; the official Rossiyskaya Gazeta publication reproduces the amending text.
- a direct act-specific current consolidated record on `pravo.gov.ru` was not resolved in this pass.
- status: `CURRENT_EDITION_CORROBORATED_2019-05-01 / LATEST_AMENDMENT_RELATION_OFFICIAL_RG_CONFIRMED / PRIMARY_CURRENT_RECORD_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 2. Presidential Decree 23.05.1996 No. 763
Target: `О порядке опубликования и вступления в силу актов Президента Российской Федерации, Правительства Российской Федерации и нормативных правовых актов федеральных органов исполнительной власти`.

GitHub:
- exact and broad searches did not produce a reproducible target body.
- `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current full-text sources identify edition `03.03.2022` (not 2017).
- Presidential Decree 03.03.2022 No. 90 directly changes paragraph 3 of point 2 of Decree 763/1996.
- official-publication pointer for Decree 90/2022: `0001202203030006`, publication date 2022-03-03.
- the 2022 amendment is substantively important: it updates the rule on which electronic texts of Presidential and Government acts are official.
- direct act-specific current consolidated record for Decree 763 itself was not resolved in this pass.
- status: `CURRENT_EDITION_CORROBORATED_2022-03-03 / LATEST_AMENDMENT_RELATION_CONFIRMED / LATEST_AMENDMENT_OFFICIAL_PUBLICATION_POINTER_CONFIRMED / PRIMARY_CURRENT_RECORD_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 3. Government Resolution 13.08.1997 No. 1009
Target: `Об утверждении Правил подготовки нормативных правовых актов федеральных органов исполнительной власти и их государственной регистрации` + complete approved Rules.

GitHub:
- exact and broad searches returned no target body.
- `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current full-text sources identify edition `15.11.2024`, effective from `23.11.2024`.
- Government Resolution 15.11.2024 No. 1557 directly changes point 3(3) of the Rules approved by No. 1009.
- official publication of No. 1557: `pravo.gov.ru`, 2024-11-15, publication No. `0001202411150020`.
- direct act-specific current consolidated record for No. 1009 was not resolved in this pass.
- completeness gate: `FULL_TEXT = signing resolution + complete approved Rules`; a signing page alone is `PARTIAL_TEXT`.
- status: `CURRENT_EDITION_CORROBORATED_2024-11-15 / LATEST_AMENDMENT_OFFICIAL_PUBLICATION_POINTER_CONFIRMED / PRIMARY_CURRENT_RECORD_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 4. Government Resolution 22.10.2020 No. 1722
Target: rules on publication/updating of official-site lists of NPAs containing mandatory requirements.

GitHub:
- exact and broad searches returned no target body.
- `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current full-text sources identify edition `26.01.2026`, effective from `04.02.2026`.
- Government Resolution 26.01.2026 No. 42 directly changes No. 1722, including the new Federal GIS `Реестр обязательных требований` rule and repeal of point 7(1).
- official publication of No. 42: `pravo.gov.ru`, 2026-01-27, publication No. `0001202601270032`.
- official regulator pages in 2026 continue to use No. 1722 for current mandatory-requirements lists, corroborating active status.
- direct act-specific current consolidated primary record for No. 1722 was not resolved in this pass.
- status: `CURRENT_EDITION_CORROBORATED_2026-01-26 / ACTIVE_STATUS_OFFICIAL_AGENCY_CORROBORATED / LATEST_AMENDMENT_OFFICIAL_PUBLICATION_POINTER_CONFIRMED / PRIMARY_CURRENT_RECORD_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 5. Federal Law 08.06.2020 No. 168-FZ
Target: `О едином федеральном информационном регистре, содержащем сведения о населении Российской Федерации`.

GitHub:
- exact and broad searches returned no target body.
- `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current full-text sources identify edition `28.11.2025`.
- Federal Law 28.11.2025 No. 442-FZ directly amends Articles 4 and 11 of FZ 168/2020.
- official publication: `pravo.gov.ru`, 2025-11-28, publication No. `0001202511280105`.
- FZ 442/2025 entered into force on `2026-05-28` after 180 days; therefore its changes are already effective for this corpus date.
- Article 13 of FZ 168 establishes a transition period only through `2025-12-31`; expiry of that transition period is not expiry of the whole law.
- direct act-specific current consolidated primary record for FZ 168 was not resolved in this pass.
- status: `CURRENT_EDITION_CORROBORATED_2025-11-28 / LATEST_AMENDMENT_EFFECTIVE_2026-05-28 / LATEST_AMENDMENT_OFFICIAL_PUBLICATION_POINTER_CONFIRMED / TRANSITION_PERIOD_ENDED_NOT_ACT_EXPIRED / PRIMARY_CURRENT_RECORD_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 6. Government Resolution 09.10.2021 No. 1723
Target: full Rules for providing information from the federal population register + complete list of anonymized personal data.

GitHub:
- exact and broad searches returned no target body.
- `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current full-text sources identify edition `28.05.2026`.
- Government Resolution 28.05.2026 No. 612 directly changes No. 1723.
- official publication of No. 612: `pravo.gov.ru`, 2026-05-28, publication No. `0001202605280022`.
- No. 612 expressly enters into force on the date when Federal Law amending Article 13 of the Credit Histories Law and Articles 4 and 11 of FZ 168 enters into force. That federal law is No. 442-FZ of 28.11.2025, whose effective date is `2026-05-28`. Therefore the temporal dependency is resolved: the 612/2026 amendments to 1723 are already effective.
- completeness gate: `FULL_TEXT = signing resolution + complete Rules + all appendices + complete anonymized-PD list`; omission of the list is `PARTIAL_TEXT`.
- direct act-specific current consolidated primary record for No. 1723 was not resolved in this pass.
- status: `CURRENT_EDITION_CORROBORATED_2026-05-28 / LATEST_AMENDMENT_EFFECTIVE_2026-05-28 / TEMPORAL_DEPENDENCY_RESOLVED / LATEST_AMENDMENT_OFFICIAL_PUBLICATION_POINTER_CONFIRMED / PRIMARY_CURRENT_RECORD_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

## New corpus gates

1. `OFFICIAL_PUBLICATION_POINTER != ACT_SPECIFIC_CURRENT_RECORD`: a publication ID for the latest amendment proves the publication event and amendment relation; it is not by itself the consolidated current body of the base act.
2. `PRAVO_INTEGRATED_BANK_OFFICIAL_STATUS`: the official portal states that federal laws, Presidential acts and Government acts placed in its integrated full-text bank have official status, while placement there is distinct from the event of official publication. Store `official_text_status` separately from `official_publication_event`.
3. `TRANSITION_PERIOD_END != ACT_EXPIRY`: FZ 168/2020 is the concrete regression fixture; its transition period ended 2025-12-31, while the law continues and was amended with effect from 2026-05-28.
4. `DEPENDENT_EFFECTIVE_DATE`: for amendments such as PP 612/2026, resolve the referenced triggering federal law and its actual effective date before marking the amendment current.
5. `GITHUB_SEARCH_FALSE_POSITIVE_BODY_GATE`: a code-search match on number/date terms is not a candidate until the body independently matches act type + date + number + title.
6. `DERIVATIVE_PATH_DEDUP`: parsed/normalized derivatives of a known wrong source are counted separately as files but not as independent legal-source candidates.

## Source pointers used in this pass

Habr:
- https://habr.com/ru/articles/432466/

GitHub rejected artifacts:
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/canon/sources/originals-text/FZ-422_2018-11-27.md
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/package/samples/parsed/minekonom_prikaz_67_gis_ekonomika.md

Official-publication pointers / official sources:
- Decree 90/2022: https://publication.pravo.gov.ru/Document/View/0001202203030006
- PP 1557/2024: https://publication.pravo.gov.ru/Document/View/0001202411150020
- PP 42/2026: https://publication.pravo.gov.ru/Document/View/0001202601270032
- FZ 442/2025: https://publication.pravo.gov.ru/Document/View/0001202511280105
- PP 612/2026: https://publication.pravo.gov.ru/Document/View/0001202605280022
- Official portal status description: https://www.pravo.gov.ru/
- FZ 83/2019 official Rossiyskaya Gazeta text: https://rg.ru/documents/2019/05/08/fz83-dok.html
- FZ 442/2025 official Rossiyskaya Gazeta text: https://rg.ru/documents/2025/12/08/fz442-dok.html

No GitHub artifact in this audit is treated as an official legal source. Body identity, structural completeness, edition freshness, official publication, effective date and official current-text status remain independent evidence dimensions.
