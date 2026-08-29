# Habr NPA sweep — Stream 1 — 2026-08-30 00:57 MSK

Scope: continuation of Habr 432466 and user NPA queue, focused on personal-data/common information acts. GitHub copies are treated only as non-official corpus candidates. Official status/lifecycle is checked separately.

## Delta

- GITHUB_FULL_TEXT_CONFIRMED: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +10
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +3
- OFFICIAL_PUBLICATION_POINTER_CORROBORATED: +3
- LATEST_AMENDMENT_CORROBORATED: +1
- EXACT_DUPLICATE: +0
- NEW_BODY_IDENTITY_CONFLICT: +0

## New findings

### PP RF 29.06.2021 No. 1046 — federal state control over personal-data processing

GitHub exact characteristic-title Code Search: `total_count=0`, `incomplete_results=false`. Recursive path traversal of `Grantik/odin-vault` at `c4028e14dcadc511b566826ce2ee8e1fccbf83d0` found no path containing `1046`. Therefore `repo/commit/path/size/type = null`; status `GITHUB_FULL_TEXT_BLOCKER` (not proof of global absence).

Initial official publication pointer: `0001202106300055` (30.06.2021), corroborated from cross-references; direct primary fetch timed out in this pass.

Important freshness delta: current legal databases identify PP RF 03.07.2026 No. 833 as an amendment to No. 1046, effective 11.07.2026. This amendment post-dates the Habr snapshot of 28.05.2026. Primary publication card for No. 833 was not resolved in this pass, so status is `LATEST_AMENDMENT_CORROBORATED / PRIMARY_LATEST_AMENDMENT_CARD_UNRESOLVED`, not primary-current verified.

### PP RF 29.12.2022 No. 2526 — cases exempted from parts of Article 12 transborder-transfer requirements

GitHub exact Code Search: `0`, `incomplete_results=false`; no `2526` path in the inspected `Grantik/odin-vault` tree. `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

Primary official publication directly confirmed: `publication.pravo.gov.ru/Document/View/0001202212310018`, publication No. `0001202212310018`, 31.12.2022. Secondary full text confirms the act body and effective date 01.03.2023. Current lifecycle remains unresolved from a primary consolidated source.

### PP RF 10.01.2023 No. 6 — prohibition/restriction of transborder personal-data transfer

GitHub exact Code Search: `0`, `incomplete_results=false`; `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

Primary official index directly confirms publication No. `0001202301110015`, 11.01.2023, official PDF 6498 KB / 8 pages. Direct card fetch timed out; current lifecycle not elevated beyond initial publication confirmation.

### Presidential Decree 29.12.2012 No. 1709 — biometric foreign passport

GitHub exact Code Search by number + characteristic title phrase: `0`, `incomplete_results=false`; `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

A consolidated non-primary source shows the exact title/body and an amendment dated 07.12.2016 (Decree No. 656). Primary current card was not resolved, so this remains `CURRENT_AMENDMENT_HISTORY_CORROBORATED / PRIMARY_DIRECT_CURRENT_CARD_UNRESOLVED`.

### Presidential Decree 24.11.2014 No. 735 — biometric data of foreign citizens/stateless persons

GitHub exact Code Search: `0`, `incomplete_results=false`; `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

Secondary full-body sources confirm number/date/title and report official portal publication on 25.11.2014; direct primary card not resolved. Status `OFFICIAL_PUBLICATION_CORROBORATED / PRIMARY_DIRECT_CARD_UNRESOLVED`.

### Roskomnadzor Order 21.06.2021 No. 106

GitHub exact Code Search: `0`, `incomplete_results=false`; `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

Habr identity matches: rules for use of the Roskomnadzor information system and interaction between data subject and operator; Ministry of Justice registration No. 64602. Secondary legal archive confirms the same identity and entry into force 01.03.2022. Primary publication card/current lifecycle not resolved in this pass.

### Roskomnadzor Order 24.12.2021 No. 253

GitHub exact Code Search: `0`, `incomplete_results=false`; `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

Official-publication pointer corroborated as `0001202202280005`; Ministry of Justice registration No. 67486. Direct primary fetch timed out, so do not elevate to direct primary verification.

### Roskomnadzor Order 05.08.2022 No. 128

GitHub exact Code Search: `0`, `incomplete_results=false`; `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

Primary official portal directly confirms exact date/number/title, registration No. 70152, publication No. `0001202209200008` on 20.09.2022. Full secondary text shows the order plus the complete approved list and states entry into force on 01.03.2023. Future GitHub candidate must include the entire approved list to qualify as `FULL_TEXT`.

### Roskomnadzor Order 28.10.2022 No. 180

GitHub exact Code Search: `0`, `incomplete_results=false`; `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

Official-publication pointer corroborated as `0001202212150022`; Ministry of Justice registration No. 71532. Secondary body confirms that the normative package contains three notification forms; a GitHub file without all forms is `PARTIAL_TEXT`. Direct primary fetch timed out.

### Roskomnadzor Order 14.11.2022 No. 187

GitHub exact Code Search: `0`, `incomplete_results=false`; `repo/commit/path/size/type = null`; `GITHUB_FULL_TEXT_BLOCKER`.

Secondary full text confirms exact identity, Ministry of Justice registration No. 71851, official portal publication on 28.12.2022, and the complete approved procedure; entry into force is stated as 01.03.2023. Direct primary publication card/current lifecycle was not resolved, so status remains `OFFICIAL_PUBLICATION_CORROBORATED / PRIMARY_DIRECT_CARD_UNRESOLVED`.

## New gates

1. `HABR_SNAPSHOT_DATE < LATEST_AMENDMENT_DATE` is recorded as `POST_SNAPSHOT_AMENDMENT`, not an Habr error.
2. For acts approving forms/lists/procedures, `FULL_TEXT` requires the complete approved attachment set, not only the signing order.
3. `OFFICIAL_PUBLICATION_POINTER_CORROBORATED != PRIMARY_DIRECT_VERIFIED` when the primary card cannot be fetched.
4. `EXACT_CODE_SEARCH_ZERO + TREE_PATH_ZERO != GLOBAL_GITHUB_ABSENCE`; keep as a blocker and continue binary/tree traversal in later passes.
