# Habr NPA sweep — Stream 1 — 2026-08-30 20:53 MSK

Scope: Habr 432466, sections `Персональные данные. Сроки хранения` and selected `Персональные данные. Примеры внутренних документов`. This pass covers FKTsB №03-33/пс/2003, Rosarchiv №236/2019, Rosarchiv №142/2021, Rosarchiv/Bank of Russia №1/801-П/2022, Rosarchiv №77/2023, Rospatent №111/2025, RKN recommendations on operator privacy policy, and RKN №201/2022.

## GitHub search gate

Exact identity/title searches and registration-number recall searches were run through GitHub code search. No indexed full-text target body and no reliable target-body candidate were returned.

| Target | GitHub query examples | repo | commit | path | size | type | result |
|---|---|---|---|---|---:|---|---|
| FKTsB 16.07.2003 №03-33/пс | `"03-33/пс" "16.07.2003" "хранения документов акционерных обществ"`; `"03-33/пс" 4994` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Rosarchiv 20.12.2019 №236 | `"Приказ Росархива" "20.12.2019" "N 236" "Перечня типовых управленческих архивных документов"`; `57449 Росархива` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Rosarchiv 28.12.2021 №142 | `"28.12.2021" "N 142" "Перечня типовых архивных документов"`; `67095 Росархива` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Rosarchiv/Bank of Russia 12.07.2022 №1/801-П | `"12.07.2022" "801-П" "Перечня документов" "кредитных организаций"`; `801-П 69304` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Rosarchiv 31.07.2023 №77 | `"Приказ Росархива" "31.07.2023" "N 77" "Правил организации хранения"`; `75119 Росархива` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Rospatent 23.10.2025 №111 | `"Приказ Роспатента" "23.10.2025" "N 111" "сроков хранения"` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| RKN recommendations 2017 | `"27 июля 2017" "Рекомендации Роскомнадзора" "политику оператора"` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| RKN 15.12.2022 №201 | `"Роскомнадзор" "15.12.2022" "N 201" "Об обработке персональных данных"`; `73374 Роскомнадзор` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

No new GitHub duplicate/reference-only artifact was returned in this batch. No target-body identity conflict was possible because no GitHub candidate body reached the identity gate.

## New confirmed findings

### FKTsB RF 16.07.2003 №03-33/пс

Full consolidated body corroborates exact number/date/title and Minjust registration №4994. Current legal-text services still mark the act as `Действует`; current legal commentary in 2025 continues to apply it. A fresh official Bank of Russia / primary-successor current-status record was not resolved, therefore the corpus must not elevate this to primary-current verified.

Important dependency issue: clauses 2.1.3, 2.1.5 and 2.1.20 expressly point to the `Перечень типовых управленческих документов ... утвержденный Федеральной архивной службой России 06.10.2000`. The current Rosarchiv typical-management list is the one approved by Rosarchiv order №236/2019. Therefore the act can be historically/currently operative while one of its cross-referenced archival-list dependencies is legacy/stale. Do not silently rewrite the original body; model the dependency lifecycle separately.

Classification: `CURRENT_STATUS_CORROBORATED_NONPRIMARY`, `PRIMARY_CURRENT_STATUS_BLOCKER`, `LEGACY_STALE_REFERENCE_DEPENDENCY`, `GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- https://normativ.kontur.ru/document/1/59628-postanovlenie-fktsb-rf-ot-16-07-2003-n-03-33-ps
- https://archives.gov.ru/perechni-dokumentov.shtml

### Rosarchiv 20.12.2019 №236

Primary official publication is confirmed directly: registered 06.02.2020 №57449; publication number `0001202002070036`; published 07.02.2020. Rosarchiv's current `Перечни документов` page still lists the document as the governing typical management archival-document list. Current legal/court usage in 2026 also corroborates continued application. No later amending act was found in the fresh amendment search, but absence of a result is not stored as a formal no-amendment guarantee.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`, `CURRENT_PRIMARY_AGENCY_LISTING_CONFIRMED`, `NO_LATER_AMENDMENT_FOUND_IN_FRESH_SEARCH`, `GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- https://publication.pravo.gov.ru/Document/View/0001202002070036
- https://archives.gov.ru/perechni-dokumentov.shtml

### Rosarchiv 28.12.2021 №142

Rosarchiv's official orders registry confirms exact identity and Minjust registration 02.02.2022 №67095. Its current `Перечни документов` page also continues to list №142 as the typical list for scientific/technical and production activity. Publication timing is independently corroborated as official-portal publication on 02.02.2022 and entry into force 13.02.2022, but a stable direct `publication.pravo.gov.ru` publication-number card was not resolved in this pass.

Classification: `PRIMARY_AGENCY_IDENTITY_REGISTRATION_CONFIRMED`, `CURRENT_PRIMARY_AGENCY_LISTING_CONFIRMED`, `OFFICIAL_PUBLICATION_ID_BLOCKER`, `GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- https://archives.gov.ru/documents/rosarhiv-orders.shtml
- https://archives.gov.ru/perechni-dokumentov.shtml

### Rosarchiv / Bank of Russia 12.07.2022 №1/801-П

Primary publication is confirmed: registered 19.07.2022 №69304; publication number `0001202207190003`; published 19.07.2022. A new metadata conflict was confirmed between primary sources: the official publication portal renders the header as `Приказ Федерального архивного агентства, Центрального банка Российской Федерации ... № 1/801-П`, while Rosarchiv's current authoritative lists page calls the same instrument `Положением Федерального архивного агентства и Центрального банка Российской Федерации ... № 1/801-П`. Habr also calls it `Положение`.

Do not resolve this by guessing or normalizing one source away. Store the source-specific legal-form labels and keep the canonical identity keyed by issuing bodies + date + №1/801-П + title + Minjust №69304.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`, `CURRENT_PRIMARY_AGENCY_LISTING_CONFIRMED`, `PRIMARY_SOURCE_DOCUMENT_TYPE_CONFLICT`, `GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- https://publication.pravo.gov.ru/document/0001202207190003
- https://archives.gov.ru/perechni-dokumentov.shtml

### Rosarchiv 31.07.2023 №77

Primary publication is confirmed directly: registered 06.09.2023 №75119; publication number `0001202309060005`; published 06.09.2023. Official portal exposes a 107-page normative body. Rosarchiv's own press page confirms registration. Current Rosarchiv materials continue to rely on these Rules.

Completeness gate: a GitHub file containing only the short approving order is `PARTIAL_TEXT`; `FULL_TEXT` requires the full Rules and all appendices/forms across the 107-page body.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`, `CURRENT_USE_CORROBORATED`, `FULL_TEXT_REQUIRES_ALL_APPENDICES`, `GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- https://publication.pravo.gov.ru/document/0001202309060005
- https://archives.gov.ru/press/06-09-2023.shtml

### Rospatent 23.10.2025 №111

A strong official full-text artifact was found outside GitHub: Rosarchiv hosts the complete departmental list PDF. Its title page explicitly says it is approved by Rospatent order 23.10.2025 №111 and agreed by decision of the Central Expert-Verification Commission at Rosarchiv dated 13.10.2025 №12/4111-10. Rosarchiv's current lists page includes the Rospatent list.

No Minjust registration record and no `publication.pravo.gov.ru` official-publication event were resolved in this pass. Therefore official agency hosting and an approval order are not enough to classify it automatically as a generally binding, Minjust-registered NPA. Keep it as a departmental archival list with legal-form/publication status separately unresolved.

Classification: `OFFICIAL_AGENCY_HOSTED_FULLTEXT_CONFIRMED`, `DEPARTMENTAL_ARCHIVAL_LIST`, `MINJUST_REGISTRATION_NOT_FOUND`, `OFFICIAL_PUBLICATION_EVENT_NOT_FOUND`, `GENERAL_BINDING_NPA_STATUS_UNRESOLVED`, `GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- https://archives.gov.ru/sites/default/files/2025_perechen-rospatent.pdf
- https://archives.gov.ru/perechni-dokumentov.shtml

### Roskomnadzor recommendations on operator privacy policy (2017)

No GitHub target body was found. Current public-sector pages still point users to Roskomnadzor's `/personal-data/p908/` URL for `Рекомендации по составлению документа, определяющего политику оператора в отношении обработки персональных данных`, but the direct RKN page could not be fetched in this pass.

A metadata/date conflict remains unresolved: Habr and some current legal reproductions label the recommendations `27.07.2017`, while other legal databases describe the publication/recommendation as `31.07.2017`. Without the retrievable primary RKN page, do not normalize the date. This material is recommendations/guidance, not automatically a Minjust-registered NPA.

Classification: `RECOMMENDATION_MATERIAL`, `DATE_METADATA_CONFLICT_2017-07-27_vs_2017-07-31`, `PRIMARY_RKN_PAGE_FETCH_BLOCKER`, `NPA_STATUS_NOT_ESTABLISHED`, `GITHUB_FULL_TEXT_BLOCKER`.

Source pointer:
- https://rkn.gov.ru/personal-data/p908/

### Roskomnadzor 15.12.2022 №201

Primary official publication is confirmed directly: exact title, registered 19.05.2023 №73374; publication number `0001202305220004`; published 22.05.2023. Fresh search did not surface a later amending/repealing act. Current legal-text services continue to reproduce the order as operative; because no separate current Roskomnadzor status registry was resolved, the `current` label remains corroborated rather than primary-current verified.

Completeness gate is especially important. `FULL_TEXT` must include all nine approved appendices/components (including the PD processing Rules, internal-control Rules, ISPDn list, positions/access lists, responsible-person duties, templates and room-access procedure). A file containing only the order or only Appendix №1 is `PARTIAL_TEXT`.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`, `CURRENT_STATUS_CORROBORATED`, `NO_LATER_AMENDMENT_FOUND_IN_FRESH_SEARCH`, `FULL_TEXT_REQUIRES_ALL_APPROVED_APPENDICES`, `GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- https://publication.pravo.gov.ru/document/0001202305220004

## New corpus gates / conflicts

1. `PRIMARY_SOURCE_DOCUMENT_TYPE_CONFLICT`: for №1/801-П, source-specific type labels disagree (`Приказ` on publication.pravo vs `Положение` on Rosarchiv); do not normalize away primary-source disagreement.
2. `OFFICIAL_AGENCY_HOSTED_FULLTEXT != GENERAL_BINDING_NPA`: Rospatent №111/2025 is officially hosted and approved, but Minjust registration/general-binding NPA status was not established.
3. `RECOMMENDATION_DATE_REQUIRES_PRIMARY_PAGE`: 2017 RKN policy recommendations have a 27.07 vs 31.07 metadata split; retain both claims until primary page resolution.
4. `ACTIVE_OR_CORROBORATED_ACT_CAN_HAVE_STALE_DEPENDENCY`: FKTsB №03-33/пс still points to the 06.10.2000 archival list while Rosarchiv №236/2019 is the current typical-management list. Preserve original text and version the referenced dependency separately.
5. `FULL_TEXT_REQUIRES_ALL_APPROVED_APPENDICES`: approving order alone does not satisfy full-body completeness for Rosarchiv №77 or RKN №201.
6. `PRIMARY_INITIAL_PUBLICATION != PRIMARY_CURRENT_STATUS`: an official publication card proves the publication event and identity, not by itself present-day currency.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +8`
- `NEW_GITHUB_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +4` (Rosarchiv №236, №1/801-П, №77, RKN №201)
- `PRIMARY_AGENCY_IDENTITY/REGISTRATION_CONFIRMED +1` (Rosarchiv №142)
- `OFFICIAL_AGENCY_HOSTED_FULLTEXT_CONFIRMED +1` (Rospatent №111)
- `PRIMARY_SOURCE_DOCUMENT_TYPE_CONFLICT +1`
- `RECOMMENDATION_DATE_METADATA_CONFLICT +1`
- `PRIMARY_RKN_PAGE_FETCH_BLOCKER +1`
- `OFFICIAL_PUBLICATION_ID_BLOCKER +1` (Rosarchiv №142)
- `GENERAL_BINDING_NPA_STATUS_UNRESOLVED +1` (Rospatent №111)
- `LEGACY_STALE_REFERENCE_DEPENDENCY +1` (FKTsB №03-33/пс)

## Next queue

Continue without repeating closed items. Next priority: additional Roskomnadzor/general-PDn internal-document exemplars around the Habr block, separating true registered NPA from departmental/local examples, and then continue remaining federal/general information acts from the user list. Preserve the same GitHub identity/body gate and primary-source lifecycle gate.