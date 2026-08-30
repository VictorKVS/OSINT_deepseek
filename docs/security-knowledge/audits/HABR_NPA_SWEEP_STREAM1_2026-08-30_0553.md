# Habr NPA sweep — Stream 1 — 2026-08-30 05:53 MSK

Source snapshot: Habr article 432466, version dated 2026-05-28, plus the user-maintained NPA queue.

## Delta for this pass

- targets processed: 4
- GITHUB_FULL_TEXT_CONFIRMED: +1 (258-FZ)
- BODY_IDENTITY_CONFIRMED: +1 (258-FZ)
- GITHUB_FULL_TEXT_STALE_CONFIRMED: +1 (258-FZ; GitHub amendment list stops at 2025-07-31, while 211-FZ/2026 already amended the law)
- GITHUB_FULL_TEXT_BLOCKER: +3 (1856-r, 3339-r, 247-FZ)
- DUPLICATE_REFERENCE_HIT / WRONG_BODY: +4 target hits across 247-FZ and 258-FZ; 3 unique underlying non-target artifacts
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +2 (247-FZ, 258-FZ)
- PRIMARY_OFFICIAL_BODY_CONFIRMED: +2 (Government 1856-r page; official Government 3339-r document identity/strategy body via static Government publication)
- PRIMARY_AMENDMENT_RELATION_CONFIRMED: +2 (215-FZ -> 247-FZ via Rossiyskaya Gazeta official text; 523-FZ -> 258-FZ via Rossiyskaya Gazeta official text)
- LATEST_EDITION_CORROBORATED_2026-06-26: +2 (247-FZ, 258-FZ)
- HABR_STALE_TITLE_CONFLICT: +1 (258-FZ)
- ORDER_NUMBER_COLLISION_SEARCH_RISK: +1 (1856-r also exists for unrelated 2019 Government order)
- exact full-body duplicates: +0
- new target-body identity conflicts: +0

## Findings

### 1. Federal Law 31.07.2020 No. 258-FZ
Target current title: `Об экспериментальных правовых режимах в сфере цифровых и технологических инноваций в Российской Федерации`.

GitHub — new confirmed full text:
- repo: `Grantik/odin-vault`
- commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
- path: `canon/sources/originals-text/FZ-258_2020-07-31.md`
- blob SHA: `26a160e9647e21ced8a7490196e907e29c6b3bc1`
- size: `162803` bytes
- type: `Markdown/file`
- provenance marker inside file: PDF→text conversion on 2026-05-19; source PDF recorded as 202K and removed after conversion.

Body identity/completeness checks:
- file begins with `РОССИЙСКАЯ ФЕДЕРАЦИЯ / ФЕДЕРАЛЬНЫЙ ЗАКОН` and the exact amended title;
- states State Duma adoption 2020-07-22 and Federation Council approval 2020-07-24;
- code search for the terminal `Статья 20. Вступление в силу настоящего Федерального закона` resolves to the same path;
- code search for final signature marker `В.ПУТИН` plus `258-ФЗ` resolves to the same path;
- code search for `31 июля 2020 года` plus `258-ФЗ` resolves to the same path.
- classification: `GITHUB_FULL_TEXT_CONFIRMED / BODY_IDENTITY_CONFIRMED / NON_OFFICIAL_GITHUB_COPY`.

Currency conflict:
- the file's amendment header ends with Federal Law 31.07.2025 No. 336-FZ.
- Federal Law 26.06.2026 No. 211-FZ directly amends 258-FZ; its Article 1 changes multiple provisions including Art. 2, Art. 3, Art. 6, Art. 7 and Art. 10, and Article 2 makes the amendment effective from official publication.
- legal databases current in August 2026 identify 258-FZ as edition dated 2026-06-26.
- therefore the GitHub artifact is full in structural/body terms but stale in edition terms: `GITHUB_FULL_TEXT_STALE_CONFIRMED`.

Official/source separation:
- primary official publication for the original law: publication number `0001202007310024`, published 2020-07-31.
- Rossiyskaya Gazeta official text of Federal Law 523-FZ dated 2024-12-28, Article 29, explicitly changes the 258-FZ title by replacing `цифровых` with `цифровых и технологических`; 523-FZ entered into force 2025-06-27.
- Rossiyskaya Gazeta / current legal sources confirm the later 211-FZ/2026 amendment relation; direct current consolidated body on the primary publication portal remains unresolved in this pass.

Habr conflict:
- Habr snapshot dated 2026-05-28 still lists the pre-523-FZ title `...в сфере цифровых инноваций...`.
- since the title amendment was already effective from 2025-06-27, classify as `HABR_STALE_TITLE_CONFLICT`.

### 2. Federal Law 31.07.2020 No. 247-FZ
Target: `Об обязательных требованиях в Российской Федерации`.

GitHub:
- exact/title/body searches did not yield a target full body.
- broad search returned only known non-target artifacts:
  1. `AxHulk/osp-kavkaz-ing`, commit `b902d3e57875c53d2c284e3e257fefc7f8d5e9e9`, path `src/pages/Accreditation.tsx`, previously recorded size `174314` bytes, TSX/file, blob `019eb2fb8c4e15d46859ff2a43c58517b56bfbd8`; body is a React accreditation/certification page, not a federal law.
  2. `Grantik/odin-vault`, commit `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`, path `sync/canon/package/samples/koncepciya_gis_rt_teo.txt`, TXT/file, blob `067866c9fe3b098c0432205ca554945298e53bd8`; body is the 2024 Concept for GIS `Российский транспорт`, with 247-FZ only as a legal reference.
- classifications: `DUPLICATE_REFERENCE_HIT / WRONG_PRIMARY_BODY / REJECT`.
- target status: `GITHUB_FULL_TEXT_BLOCKER`; repo/commit/path/size/type for a target body remain `null`.

Official/current:
- primary official publication directly confirms No. 247-FZ and publication number `0001202007310002`, published 2020-07-31.
- Federal Law 26.06.2026 No. 215-FZ, Article 4, directly amends Art. 1(2)(4) of 247-FZ by adding the legislation on foreign agents to the excluded regulatory scope.
- Article 6(1) of 215-FZ makes Article 4 effective from the day of official publication; current legal databases identify 247-FZ as edition dated 2026-06-26 and already reproduce the added `законодательства Российской Федерации об иностранных агентах` wording.
- status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_AMENDMENT_RELATION_CONFIRMED / CURRENT_EDITION_CORROBORATED_2026-06-26 / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 3. Government Order 11.07.2023 No. 1856-r
Target: `Об утверждении Концепции регулирования отрасли квантовых коммуникаций в Российской Федерации до 2030 года` + complete approved Concept.

GitHub:
- exact number + characteristic title search returned no reproducible target file.
- repo/commit/path/size/type: `null`.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary Government page reproduces the order and approved Concept and confirms exact number/date/title.
- current legal sources checked in this pass mark the document as acting; a primary consolidated edition marker was not resolved, so currentness remains `CURRENT_STATUS_CORROBORATED`, not `PRIMARY_CURRENT_CONSOLIDATED_VERIFIED`.
- completeness gate: `FULL_TEXT = signing order + complete approved Concept`.

Search collision:
- the number `1856-r` is also used by an unrelated Government Order dated 2019-08-21 concerning agricultural products; therefore number-only matching is unsafe.
- classification: `ORDER_NUMBER_COLLISION_SEARCH_RISK`; identity key remains `type + date + number + title/body`.

### 4. Government Order 24.11.2023 No. 3339-r
Target: `Об утверждении Стратегии развития отрасли связи Российской Федерации на период до 2035 года` + complete Strategy and appendices.

GitHub:
- exact number/title searches returned no reproducible target body.
- repo/commit/path/size/type: `null`.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- official Government static publication identifies the approved Strategy with the header `УТВЕРЖДЕНА распоряжением Правительства Российской Федерации от 24 ноября 2023 г. № 3339-р` and begins the Strategy body under the exact title.
- direct PDF page inspection could not be completed in this pass because the Government PDF endpoint timed out; therefore this pass does not promote the artifact to a page-by-page verified official full-text package.
- official publication pointer is corroborated as `0001202312040015` dated 2023-12-04 by current legal sources.
- current amendment/consolidation status remains unresolved at the primary-source level.
- completeness gate for any future GitHub candidate: `signing order + complete Strategy + all approved appendices`; a Strategy-only excerpt is `PARTIAL_TEXT`.

## New corpus gates

1. `FULL_TEXT_CONFIRMED != CURRENT_TEXT`: body completeness and edition freshness are orthogonal. A structurally complete GitHub copy can be legally stale and must retain both statuses.
2. `TITLE_FRESHNESS` is an independent versioned field. Habr's 258-FZ title is stale even though the act identity is otherwise unambiguous.
3. `AMENDMENT_HEADER_CUTOFF` is a strong stale signal when a GitHub consolidated copy carries an explicit amendment list that stops before a primary/officially corroborated later amendment.
4. `NUMBER_ONLY_MATCH` remains forbidden for Government orders because order numbers can recur across years; require date + title/body identity.
5. For strategic/conceptual acts, `FULL_TEXT` requires the signing order plus the complete approved strategy/concept and every normative appendix.

## Source pointers used in this pass

Habr:
- https://habr.com/ru/articles/432466/

GitHub:
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/canon/sources/originals-text/FZ-258_2020-07-31.md
- https://github.com/AxHulk/osp-kavkaz-ing/blob/b902d3e57875c53d2c284e3e257fefc7f8d5e9e9/src/pages/Accreditation.tsx
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/package/samples/koncepciya_gis_rt_teo.txt

Primary/official or official-publication sources:
- 247-FZ initial publication: https://publication.pravo.gov.ru/Document/View/0001202007310002
- 258-FZ initial publication: https://publication.pravo.gov.ru/Document/View/0001202007310024
- Federal Law 523-FZ official text (Rossiyskaya Gazeta): https://rg.ru/documents/2025/01/09/fz523-tekhnologicheskaya-politika-doc.html
- Federal Law 215-FZ official text (Rossiyskaya Gazeta): https://rg.ru/documents/2026/07/01/fz-215-doc.html
- Government Order 1856-r: https://government.ru/docs/all/148630/
- Government official static document for Order 3339-r: https://static.government.ru/media/files/Pc7fHuejbNvqv17b0RJNv0RIqTo20lUV.pdf

Current-edition corroboration used only as secondary evidence:
- 247-FZ current edition: ConsultantPlus / Legalacts, edition 2026-06-26.
- 258-FZ amendment 211-FZ: Garant and other current legal databases; official publication metadata corroborates publication No. `0001202606260071`.

Note: no GitHub artifact in this file is treated as an official legal source. Body identity, structural completeness, edition freshness, official publication, effective date and current consolidated status remain separate evidence dimensions.