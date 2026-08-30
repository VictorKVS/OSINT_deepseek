# Habr NPA sweep — Stream 1 — 2026-08-30 06:56 MSK

Source snapshot: Habr article 432466, version dated 2026-05-28, plus the user-maintained NPA queue.

## Delta for this pass

- targets processed: 5
- GITHUB_FULL_TEXT_CONFIRMED: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +5
- DUPLICATE_REFERENCE_ARTIFACT target hits: +3 (Decree 188/1997, Roskomnadzor 178/2022, Roskomnadzor 179/2022), all resolving to the same already-known non-target blob
- unique duplicate-reference artifact: +1
- PRIMARY_INITIAL_PUBLICATION_METADATA_CONFIRMED: +3 (Roskomnadzor 178/2022, 179/2022, 201/2022)
- OFFICIAL_RG_VALIDITY_TERM_CONFIRMED: +2 (Roskomnadzor 178/2022, 179/2022)
- OFFICIAL_AGENCY_CURRENT_COPY_CORROBORATED: +1 (Presidential Decree 188/1997)
- CURRENT_EDITION_CORROBORATED: +2 (Decree 188/1997; Government Resolution 418/2008)
- CURRENT_STATUS_CORROBORATED: +1 (Roskomnadzor 201/2022)
- PRESIDENTIAL_DECREE_NUMBER_COLLISION_SEARCH_RISK: +1 (No. 188 reused by an unrelated Presidential Decree dated 2026-03-25)
- exact full-body duplicates: +0
- new target-body identity conflicts: +0

## Findings

### 1. Presidential Decree 06.03.1997 No. 188
Target: `Об утверждении Перечня сведений конфиденциального характера` + complete approved list.

GitHub:
- exact title search returned `total_count=0`, `incomplete_results=false`.
- a broader number/date search returned the already-known artifact:
  - repo: `Grantik/odin-vault`
  - commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
  - path: `sync/canon/package/samples/koncepciya_gis_rt_teo.txt`
  - blob SHA: `067866c9fe3b098c0432205ca554945298e53bd8`
  - size: `345746` bytes
  - type: `TXT/file`
- body begins `ГОСУДАРСТВЕННАЯ ИНФОРМАЦИОННАЯ СИСТЕМА «РОССИЙСКИЙ ТРАНСПОРТ» / КОНЦЕПЦИЯ ... Москва 2024`; Decree 188 is only a legal reference.
- classification: `DUPLICATE_REFERENCE_ARTIFACT / WRONG_PRIMARY_BODY / REJECT`.
- target full-body metadata remain `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- an official federal-agency publication (Rosgvardia) reproduces Decree 188 and the complete confidential-information list with the edition markers for Presidential Decrees 1111/2005 and 357/2015.
- current legal databases checked in this pass identify the current edition as 2015-07-13.
- original publication is corroborated as Rossiyskaya Gazeta No. 51 dated 1997-03-14 and SZ RF No. 10 dated 1997-03-10, Art. 1127.
- a direct current consolidated copy from the issuing Presidential primary source was not resolved in this pass.
- strict status: `OFFICIAL_AGENCY_CURRENT_COPY_CORROBORATED / CURRENT_EDITION_CORROBORATED_2015-07-13 / PRIMARY_ISSUER_CURRENT_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

Search collision:
- there is a different Presidential Decree No. 188 dated 2026-03-25; therefore `188` alone is not an identity key.
- identity gate remains `act type + date + number + title/body`.

### 2. Government Resolution 02.06.2008 No. 418
Target: `О Министерстве цифрового развития, связи и массовых коммуникаций Российской Федерации` + complete Regulation on the Ministry.

GitHub:
- exact current-title search: `total_count=0`, `incomplete_results=false`.
- broader search using date/number/older ministry wording: `total_count=0`, `incomplete_results=false`.
- target metadata: `repo/commit/path/size/type = null`.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current legal sources identify the Resolution as edition dated 2026-04-21, effective in that edition from 2026-04-30.
- Government Resolution 21.04.2026 No. 445 amends No. 418, including addition of subparagraph 5.2.17(1); official-publication metadata for No. 445 had already been separately established in the corpus as publication No. `0001202604220020` dated 2026-04-22.
- direct current consolidated primary body for No. 418 itself was not resolved in this pass.
- strict status: `CURRENT_EDITION_CORROBORATED_2026-04-21 / LATEST_AMENDMENT_PP445_RELATION_CORROBORATED / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: `FULL_TEXT = signing resolution + complete current Regulation on the Ministry`; a copy that omits the Regulation or the 2026-04-21 amendment is not current full text.

### 3. Roskomnadzor Order 27.10.2022 No. 178
Target: `Об утверждении Требований к оценке вреда, который может быть причинен субъектам персональных данных в случае нарушения Федерального закона "О персональных данных"` + complete approved Requirements.

GitHub:
- exact/title search returned exactly one artifact, the same `Grantik/odin-vault` GIS `Российский транспорт` concept listed above.
- metadata: repo `Grantik/odin-vault`, commit `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`, path `sync/canon/package/samples/koncepciya_gis_rt_teo.txt`, blob `067866c9fe3b098c0432205ca554945298e53bd8`, size `345746`, `TXT/file`.
- body mismatch is explicit; the order is only referenced within the concept.
- classification: `DUPLICATE_REFERENCE_ARTIFACT / REFERENCE_ONLY / WRONG_BODY / REJECT`.
- no target full body -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- official publication portal metadata directly confirms the exact act and registration in the Ministry of Justice on 2022-11-28 No. 71166.
- official publication No. `0001202211290004`, publication date 2022-11-29.
- Rossiyskaya Gazeta official text confirms entry into force on 2023-03-01 and a fixed validity period through 2029-03-01.
- direct opening of the primary publication card body timed out in this pass, so no promotion to `PRIMARY_DIRECT_BODY_VERIFIED`.
- status: `PRIMARY_INITIAL_PUBLICATION_METADATA_CONFIRMED / OFFICIAL_RG_FULLTEXT_AND_TERM_CONFIRMED / EFFECTIVE_2023-03-01_TO_2029-03-01 / GITHUB_FULL_TEXT_BLOCKER`.

### 4. Roskomnadzor Order 28.10.2022 No. 179
Target: `Об утверждении Требований к подтверждению уничтожения персональных данных` + complete approved Requirements.

GitHub:
- exact/title search again returned exactly one artifact: the same `Grantik/odin-vault` GIS `Российский транспорт` concept.
- repo/commit/path/blob/size/type are identical to the No. 178 false hit above.
- body is not the Roskomnadzor order.
- classification: `DUPLICATE_REFERENCE_ARTIFACT / REFERENCE_ONLY / WRONG_BODY / REJECT`.
- target status: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- official publication portal metadata directly confirms registration 2022-11-28 No. 71167.
- official publication No. `0001202211290008`, publication date 2022-11-29.
- Rossiyskaya Gazeta official text confirms entry into force on 2023-03-01 and validity through 2029-03-01.
- primary direct body fetch timed out in this pass.
- status: `PRIMARY_INITIAL_PUBLICATION_METADATA_CONFIRMED / OFFICIAL_RG_FULLTEXT_AND_TERM_CONFIRMED / EFFECTIVE_2023-03-01_TO_2029-03-01 / GITHUB_FULL_TEXT_BLOCKER`.

### 5. Roskomnadzor Order 15.12.2022 No. 201
Target: `Об обработке персональных данных в Федеральной службе по надзору в сфере связи, информационных технологий и массовых коммуникаций` + all approved appendices.

GitHub:
- exact title search: `total_count=0`, `incomplete_results=false`.
- broader date/number/Roskomnadzor/personal-data search: `total_count=0`, `incomplete_results=false`.
- target metadata: `repo/commit/path/size/type = null`.
- status: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- official publication portal metadata confirms the exact order, Ministry of Justice registration 2023-05-19 No. 73374, official publication No. `0001202305220004`, published 2023-05-22.
- Rossiyskaya Gazeta confirms entry into force on 2023-06-02.
- the normative package is multi-part: the signing order approves nine appendices/regulations/forms. A GitHub copy of only the signing page or a subset of appendices is `PARTIAL_TEXT`.
- current legal sources continue to reproduce the order as acting; no later amendment or repeal was established in this pass, but a direct primary current consolidated body was not resolved.
- status: `PRIMARY_INITIAL_PUBLICATION_METADATA_CONFIRMED / CURRENT_STATUS_CORROBORATED / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

## New corpus gates

1. `DUPLICATE_REFERENCE_DEDUP_BY_BLOB`: one large technical/concept document may reference many NPAs and repeatedly appear in target searches. De-duplicate by repo + commit + path + blob SHA before counting unique artifacts.
2. `PRIMARY_PUBLICATION_METADATA != PRIMARY_CURRENT_CONSOLIDATED_BODY`: an official publication ID proves the publication event and identity, not current consolidated wording years later.
3. `FIXED_TERM_NPA`: where an act is expressly limited in time, store `effective_from` and `valid_until` as first-class fields; do not infer permanence from a still-accessible text.
4. `PRESIDENTIAL_DECREE_NUMBER_ONLY_MATCH_FORBIDDEN`: decree numbers recur across years; require date + title/body.
5. `INTERNAL_AGENCY_PD_ORDER_FULL_TEXT`: for an order approving multiple regulations/forms, `FULL_TEXT` requires the signing order plus every normative appendix.

## Source pointers used in this pass

Habr:
- https://habr.com/ru/articles/432466/

GitHub duplicate reference artifact:
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/package/samples/koncepciya_gis_rt_teo.txt

Primary/official publication and official-government sources:
- Roskomnadzor Order 178 publication: https://publication.pravo.gov.ru/Document/View/0001202211290004
- Roskomnadzor Order 179 publication: https://publication.pravo.gov.ru/Document/View/0001202211290008
- Roskomnadzor Order 201 publication: https://publication.pravo.gov.ru/Document/View/0001202305220004
- Presidential Decree 188 official-agency reproduction: https://rosguard.gov.ru/ru/page/index/ukaz-prezidenta-rf-ot-6-marta-1997-g-n-188

Current-edition / full-text corroboration used as non-primary-current evidence:
- ConsultantPlus / Garant current pages for Decree 188 and Government Resolution 418.
- Rossiyskaya Gazeta official texts for Roskomnadzor Orders 178, 179 and 201.

Note: no GitHub artifact in this file is treated as an official legal source. Body identity, structural completeness, edition freshness, official publication, effective dates and current consolidated status remain separate evidence dimensions.