# HABR NPA SWEEP — STREAM 1 — 2026-09-01 15:51 MSK

## Scope

Continuation of Habr 432466, KII block, positions 35–41:

35. Methodical recommendations for identification/categorization of KII objects of the fuel-and-energy complex (Minenergo outgoing 31.07.2019 No. ЧА-8630/15; FSTEK outgoing 26.08.2019 No. 240/25/4048).
36. List of typical sectoral KII objects in transport, agreed by FSTEK 05.05.2023 and Mintrans 15.05.2023.
37. Mincomsvyaz Order 17.03.2020 No. 114.
38. Mintsifry Order 18.01.2023 No. 21.
39. Minpromtorg Order 31.05.2023 No. 1981.
40. Government Resolution 14.11.2023 No. 1912.
41. Minenergo Order 26.12.2023 No. 1215.

## GitHub sweep

Exact and distinctive-phrase searches were run for every target (number/date/title, registration number where applicable). In the currently indexed GitHub search no full normative body or reliable candidate was found for positions 35–41.

| Pos | Target | repo | commit | path | size | type | Classification |
|---|---|---|---|---|---:|---|---|
|35|ЧА-8630/15 + 240/25/4048|null|null|null|null|null|GITHUB_FULL_TEXT_BLOCKER|
|36|Transport typical KII list 2023|null|null|null|null|null|GITHUB_FULL_TEXT_BLOCKER|
|37|Mincomsvyaz 114/2020|null|null|null|null|null|GITHUB_FULL_TEXT_BLOCKER|
|38|Mintsifry 21/2023|null|null|null|null|null|GITHUB_FULL_TEXT_BLOCKER|
|39|Minpromtorg 1981/2023|null|null|null|null|null|GITHUB_FULL_TEXT_BLOCKER|
|40|PP RF 1912/2023|null|null|null|null|null|GITHUB_FULL_TEXT_BLOCKER|
|41|Minenergo 1215/2023|null|null|null|null|null|GITHUB_FULL_TEXT_BLOCKER|

No new full-body duplicate and no new body-identity conflict were found in this batch. Absence in indexed search is not treated as proof that no GitHub copy exists.

## Confirmed lifecycle/status findings

### 35 — TЭК methodical recommendations 2019

Minenergo letter 28.02.2024 No. 15-203 confirms that these recommendations are recommendatory and do not contain normative-legal prescriptions. Subjects of KII may use them only insofar as they do not contradict current Russian legislation. The same letter stated that work on updating them was planned in view of KII-law changes.

Classification:
- NON_NPA_METHODICAL_GUIDANCE
- CURRENT_USE_ONLY_INSOFAR_AS_NOT_CONTRADICTING_LAW_CONFIRMED_2024
- PRIMARY_ISSUING_AGENCY_CURRENT_VERSION_BLOCKER

Gate: METHODICAL_RECOMMENDATIONS != REGISTERED_NPA.

### 36 — transport typical KII list 2023

Primary Mintrans PDF is available and identifies the document as the list of typical sectoral KII objects functioning in transport. Mintrans later approved sectoral categorization recommendations on 24.01.2024 (agreed by FSTEK 18.01.2024), and that document includes the transport object list as an appendix.

A newer statutory layer now exists: Government распоряжение 26.02.2026 No. 360-r approved the unified list of typical sectoral KII objects of the Russian Federation; the current consolidated edition is 27.05.2026 and explicitly contains section III “Transport”. Therefore the 2023 agreed sectoral list must not be used as the only current reference list. Formal withdrawal of the 2023 Mintrans material was not confirmed in this pass.

Classification:
- LEGACY_SECTORAL_LIST_LAYER
- CENTRALIZED_GOVERNMENT_LIST_CURRENT_LAYER_360R_2026
- FORMAL_WITHDRAWAL_OF_2023_LIST_NOT_CONFIRMED

Gate: OLD_SECTORAL_REFERENCE_LIST != CURRENT_GOVERNMENT_APPROVED_LIST.

### 37 — Mincomsvyaz Order 114/2020

Identity is corroborated: signed 17.03.2020, registered by Minjust 25.06.2020 No. 58753, officially published on the legal-information portal 25.06.2020, effective 06.07.2020. A complete normative body must include the order plus Appendix 1 (Procedure) and Appendix 2 (Technical Conditions).

No confirmed amendment/repeal was found in this pass, but this negative search is not sufficient to assert current consolidated status.

Classification:
- OFFICIAL_PUBLICATION_CORROBORATED
- PRIMARY_PUBLICATION_POINTER_BLOCKER
- PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER

### 38 — Mintsifry Order 21/2023

The order approves methodical recommendations for transition to Russian software, including on significant KII objects. It is treated as a methodical/non-NPA layer, not as a registered normative legal act. No newer replacement and no primary current Mintsifry original were resolved in this pass.

Classification:
- NON_NPA_METHODICAL_GUIDANCE
- PRIMARY_MINISTRY_ORIGINAL_CURRENT_VERSION_BLOCKER

### 39 — Minpromtorg Order 1981/2023

Primary official publication confirmed: publication No. 0001202308220008, published 22.08.2023, registered by Minjust 21.08.2023 No. 74904. Identity by number/date/title is exact.

No later amendment/repeal was confirmed in this pass; primary consolidated-current status remains unresolved.

Classification:
- PRIMARY_PUBLICATION_POINTER_CONFIRMED
- PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER

### 40 — Government Resolution 1912/2023

Primary original publication confirmed: No. 0001202311160056, published 16.11.2023. The official Government portal currently presents Resolution 1912 in the edition of 26.12.2024 (Resolution 1915/2024).

A Minpromtorg draft dated 15.12.2025 proposed further amendments with planned entry into force on 01.09.2026. As of 01.09.2026 the searchable source is still explicitly a PROJECT, and no signed/final 2026 amendment with official publication was confirmed. The project must therefore not be merged into the current normative body merely because its planned effective date has arrived.

Classification:
- CURRENT_CONFIRMED_EDITION_2024-12-26
- DRAFT_PLANNED_EFFECTIVE_DATE_2026-09-01_NOT_ACTUAL_EFFECTIVE_CHANGE
- FINAL_SIGNED_2026_AMENDMENT_PUBLICATION_BLOCKER

Gate: DRAFT_PLANNED_EFFECTIVE_DATE != ACTUAL_EFFECTIVE_DATE.

### 41 — Minenergo Order 1215/2023

Identity/status corroborated by the official-publication record reproduced by Rossiyskaya Gazeta: signed 26.12.2023, registered 16.05.2024 No. 78165, published on the official legal-information portal 16.05.2024, effective from 01.09.2024 and expressly valid until 01.09.2030.

Classification:
- CURRENT_EFFECTIVE
- BUILT_IN_SUNSET_2030-09-01
- PRIMARY_PUBLICATION_POINTER_BLOCKER
- PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER

Full-text completeness requires the order and the complete approved Additional Requirements.

## Counters for this pass

- GITHUB_FULL_TEXT +0
- RELIABLE_GITHUB_CANDIDATE +0
- GITHUB_FULL_TEXT_BLOCKER +7
- NEW_GITHUB_FULL_BODY_DUPLICATE +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT +0
- NON_NPA_METHODICAL_GUIDANCE +2
- CENTRALIZED_GOVERNMENT_LIST_CURRENT_LAYER +1
- LEGACY_SECTORAL_LIST_FORMAL_WITHDRAWAL_NOT_CONFIRMED +1
- DRAFT_PLANNED_EFFECTIVE_DATE_PASSED_AS_DRAFT +1
- BUILT_IN_SUNSET_2030-09-01 +1

## Sources checked

- Habr 432466, current version 28.05.2026.
- Mintrans primary files: https://mintrans.gov.ru/file/493128 and https://mintrans.gov.ru/file/503442
- Government Resolution 1912 current page: https://government.ru/docs/all/150563/
- Official publication, Minpromtorg 1981/2023: https://publication.pravo.gov.ru/document/0001202308220008
- Official publication, Government Resolution 1912/2023: https://publication.pravo.gov.ru/document/0001202311160056
- Rossiyskaya Gazeta official-publication records for Mincomsvyaz 114/2020 and Minenergo 1215/2023.
- Minenergo letter 28.02.2024 No. 15-203 (content checked through current legal-system mirrors; issuing-agency primary current page remains unresolved).
- Current 360-r consolidation cross-check: edition 27.05.2026.

## Next boundary

KII positions 42–48: Minpromtorg reference material/list of typical KII objects; FSTEK information message 240/82/672 (12.03.2025); healthcare KII categorization recommendations; transport recommendations 24.01.2024; Minenergo letter 15-203; science recommendations 21.02.2025; FSTEK information message 240/84/3451 (22.10.2025). Keep NPA, methodical guidance, regulator information messages, and reference indexes in separate layers.