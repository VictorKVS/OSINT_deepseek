# Habr NPA sweep — Stream 1 — 2026-08-31 11:53 MSK

## Scope
Continuation of Habr 432466, subsection `Лицензирование деятельности в области информационной безопасности`:

1. Federal Law 04.05.2011 No. 99-FZ `О лицензировании отдельных видов деятельности`.
2. Government Resolution No. 770 — Habr gives 01.06.1996; verified document date is 01.07.1996.
3. Government Resolution 21.11.2011 No. 957.
4. Government Resolution 03.02.2012 No. 79.
5. Government Resolution 03.03.2012 No. 171.
6. Government Resolution 12.04.2012 No. 287.
7. Government Resolution 16.04.2012 No. 313.

Habr reference: https://habr.com/ru/articles/432466/

## GitHub normative-body search

Exact/body searches were run for each target using number, date and distinctive title phrases. No full normative body and no reliable body candidate was found in this pass.

| target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| 99-FZ/2011 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 770/1996 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 957/2011 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 79/2012 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 171/2012 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 287/2012 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 313/2012 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

No mention/summary was promoted to normative body. No new GitHub full-body duplicate and no GitHub body identity conflict was found.

## New confirmed findings, conflicts and blockers

### Federal Law No. 99-FZ of 04.05.2011

A fresh consolidated legal-system view shows edition 04.08.2026, with amendments/additions entering into force through 15.08.2026. Federal Law No. 285-FZ of 04.08.2026 directly amends 99-FZ (including Articles 14 and 20). Official-publication metadata for 285-FZ is corroborated as publication No. `0001202608040010` dated 04.08.2026, but the primary publication page was not directly fetched in this pass.

The consolidated source also indicates that a prepared future edition exists. The specific amending source/effective date behind that future edition was not resolved in this pass, so it is not applied to the current body.

Classification: `CURRENT_EDITION_2026-08-04_CORROBORATED_NONPRIMARY / OFFICIAL_PUBLICATION_POINTER_CORROBORATED_FOR_285_FZ / PREPARED_FUTURE_EDITION_SOURCE_UNRESOLVED / PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

Gate: `PREPARED_FUTURE_EDITION != CURRENT_EFFECTIVE_BODY_UNTIL_SOURCE_AND_EFFECTIVE_DATE_RESOLVED`.

### Government Resolution No. 770

New Habr metadata conflict: Habr gives `01.06.1996`, while the full legal text and archival indexes identify the act as Government Resolution of `01.07.1996 No. 770`. The prior sweep queue also contained a local typo `31.07.1996`; both are corrected to `01.07.1996`.

Resolution 770 originally approved two distinct components: a licensing Regulation and a List of types of information-protection activities. Government Resolution No. 526/2002 repealed point 1 of Resolution 770 only **in the part approving the licensing Regulation**, not the List component. The List remains operationally referenced by Government Resolution No. 214/2000 in its current legal-system presentation.

Later repeal of Resolution 526 by Resolution 287/2012 does not automatically revive the old licensing Regulation approved by Resolution 770.

Classification: `HABR_WRONG_DATE_CONFLICT / QUEUE_METADATA_CORRECTION / PARTIAL_REPEAL_2002 / LIST_COMPONENT_REMAINS_OPERATIONALLY_REFERENCED / CURRENT_PARTIAL_STATUS_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER`.

Gates:
- `PARTIAL_REPEAL_OF_APPROVED_COMPONENT != WHOLE_ACT_REPEALED`.
- `REPEAL_OF_REPLACING_ACT != AUTOMATIC_REVIVAL_OF_OLD_COMPONENT`.
- `MULTI_COMPONENT_ACT_REQUIRES_COMPONENT_LEVEL_LIFECYCLE`.

### Government Resolution No. 957 of 21.11.2011

Current consolidated legal-system presentation: edition 17.08.2024, with the latest relevant amendment (Resolution No. 1106 of 17.08.2024) effective from 01.03.2025. The act remains active, while individual rows/authorities in its licensing-authority list may be marked repealed or excluded.

This creates a composite-act gate: removal/repeal of a row in the approved list is not repeal of Resolution 957 itself.

Completeness for a future GitHub candidate: `resolution shell + entire current list of licensing authorities + current appendix/repeal list where included in the act`. A shell-only copy or selected rows are `PARTIAL_TEXT`.

Classification: `CURRENT_STATUS_CORROBORATED_NONPRIMARY / COMPOSITE_LIST_WITH_REPEALED_OR_EXCLUDED_ROWS / PRIMARY_CURRENT_STATUS_BLOCKER`.

Gate: `REPEALED_OR_EXCLUDED_ROW_IN_COMPOSITE_ACT != WHOLE_ACT_REPEALED`.

### Government Resolution No. 79 of 03.02.2012

Current consolidated legal-system presentation is in the 27.12.2024 amendment state. Government Resolution No. 1931 of 27.12.2024 amended a temporary provision in Resolution 79 by replacing `2024` with `2025`.

As of 31.08.2026 that particular temporary 2025 allowance is historical/expired, but the act itself is not thereby repealed.

A 2026 draft amendment package for Resolution 79 was found (latest reviewed project prepared 06.04.2026) with proposed entry into force 01.03.2027. No final enacted Government Resolution corresponding to that project was confirmed in this pass. The project is therefore not merged into current law.

Classification: `CURRENT_STATUS_CORROBORATED_NONPRIMARY / EXPIRED_TEMPORARY_CLAUSE_WITHIN_CURRENT_ACT / DRAFT_AMENDMENT_FOUND_NOT_NPA / FINALIZATION_STATUS_BLOCKER / PRIMARY_CURRENT_STATUS_BLOCKER`.

Gates:
- `EXPIRED_TEMPORARY_CLAUSE_IN_CURRENT_ACT != ACT_REPEALED`.
- `DRAFT_AMENDMENT != ENACTED_FUTURE_CHANGE`.

### Government Resolution No. 171 of 03.03.2012

Current consolidated legal-system presentation is likewise in the 27.12.2024 amendment state. Resolution No. 1931/2024 changed a temporary 2024 reference to 2025 in Resolution 171. That temporary clause is historical by 31.08.2026; the act itself remains separately evaluated.

A 2026 draft amendment package for Resolution 171 was found (project prepared 10.04.2026), proposing entry into force 01.03.2027. No final enacted act was confirmed in this pass.

Classification: `CURRENT_STATUS_CORROBORATED_NONPRIMARY / EXPIRED_TEMPORARY_CLAUSE_WITHIN_CURRENT_ACT / DRAFT_AMENDMENT_FOUND_NOT_NPA / FINALIZATION_STATUS_BLOCKER / PRIMARY_CURRENT_STATUS_BLOCKER`.

### Government Resolution No. 287 of 12.04.2012

Current consolidated legal-system presentation: edition 03.02.2023. Government Resolution No. 159 of 03.02.2023 amended Resolution 287, including addition/change of licensing provisions and repeal of one internal point.

The appendix to Resolution 287 includes Government Resolution No. 526/2002 among acts declared void, closing the replacement chain that had earlier displaced part of Resolution 770. This does not revive the 1996 licensing Regulation.

Completeness for GitHub: `resolution shell + complete current licensing Regulation + appendix/list of acts declared void`. Omission of the appendix is `PARTIAL_TEXT`.

Classification: `CURRENT_STATUS_CORROBORATED_NONPRIMARY / REPLACEMENT_CHAIN_EDGE_CONFIRMED / PRIMARY_CURRENT_STATUS_BLOCKER`.

### Government Resolution No. 313 of 16.04.2012

Current consolidated legal-system presentation: edition 28.08.2023. Resolution No. 1403 of 28.08.2023 amended the appendix/list of licensed cryptographic works and services; the change excludes certain installation/setup/transfer activity for cryptographic means used in smart electricity-metering arrangements. The latest-amendment relation is corroborated, but direct retrieval of the primary official publication page for Resolution 1403 was not completed in this pass.

Completeness for GitHub: `resolution shell + complete licensing Regulation + full current Appendix/List of performed works and rendered services`. Any copy lacking the appendix is `PARTIAL_TEXT`.

Classification: `CURRENT_STATUS_CORROBORATED_NONPRIMARY / LATEST_AMENDMENT_CORROBORATED_NONPRIMARY / PRIMARY_LATEST_AMENDMENT_DIRECT_FETCH_BLOCKER / PRIMARY_CURRENT_STATUS_BLOCKER`.

## New counts

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_WRONG_DATE_CONFLICT +1` (PP 770)
- `QUEUE_METADATA_CORRECTION +1` (PP 770)
- `PARTIAL_REPEAL_COMPONENT_EDGE +1` (PP 770 licensing Regulation)
- `COMPOSITE_ACT_ROW_LIFECYCLE +1` (PP 957)
- `EXPIRED_TEMPORARY_CLAUSE_WITHIN_CURRENT_ACT +2` (PP 79, PP 171)
- `DRAFT_AMENDMENT_FOUND_NOT_NPA +2` (PP 79, PP 171)
- `FINALIZATION_STATUS_BLOCKER +2`
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED +1` (285-FZ -> 99-FZ)
- `PREPARED_FUTURE_EDITION_SOURCE_UNRESOLVED +1` (99-FZ)
- `PRIMARY_LATEST_AMENDMENT_DIRECT_FETCH_BLOCKER +1` (PP 313)
- `PRIMARY_CURRENT_STATUS_BLOCKER +7`
- `DUPLICATE_TARGET_ENTRY +0`

## New corpus gates

1. `PREPARED_FUTURE_EDITION != CURRENT_EFFECTIVE_BODY_UNTIL_SOURCE_AND_EFFECTIVE_DATE_RESOLVED`.
2. `PARTIAL_REPEAL_OF_APPROVED_COMPONENT != WHOLE_ACT_REPEALED`.
3. `REPEAL_OF_REPLACING_ACT != AUTOMATIC_REVIVAL_OF_OLD_COMPONENT`.
4. `MULTI_COMPONENT_ACT_REQUIRES_COMPONENT_LEVEL_LIFECYCLE`.
5. `REPEALED_OR_EXCLUDED_ROW_IN_COMPOSITE_ACT != WHOLE_ACT_REPEALED`.
6. `EXPIRED_TEMPORARY_CLAUSE_IN_CURRENT_ACT != ACT_REPEALED`.
7. `DRAFT_AMENDMENT != ENACTED_FUTURE_CHANGE`.
8. `FULLTEXT_LICENSING_RESOLUTION = SHELL + CURRENT_REGULATION + ALL_CURRENT_APPENDICES/LISTS`.

## Next queue

Continue through the remaining Habr licensing subsection, beginning with:

1. Government Resolution 16.04.2012 No. 314.
2. FSB Russia Order 10.02.2022 No. 35.
3. FSTEK Russia Orders 12.12.2022 Nos. 206 and 207.
4. FSTEK Russia Orders 12.01.2023 Nos. 3 and 4.
5. FSB Russia Order 18.03.2023 No. 142.

Intervening regulator lists/information messages will be separately classified as NPA vs non-NPA official material rather than promoted automatically.
