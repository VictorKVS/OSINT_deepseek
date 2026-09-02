# Habr NPA sweep — Stream 1 — 2026-09-02 20:51 MSK

## Scope

Continued the Habr 432466 / user NPA sweep in article order, banking-security positions 7–12:

1. Bank of Russia Instruction No. 2346-U of 25.11.2009.
2. Bank of Russia Letter No. 141-T of 26.10.2010.
3. Bank of Russia Letter No. 154-T of 22.11.2010.
4. Bank of Russia Regulation No. 390-P of 30.11.2012.
5. Bank of Russia Instruction No. 147-I of 05.12.2013.
6. Bank of Russia Letter No. 49-T of 24.03.2014.

GitHub copies are never treated as official merely because they are on GitHub. GitHub body identity/completeness and primary official/current-status checks remain separate gates. Letters `*-T` remain a non-NPA/recommendatory layer unless a separate legal basis says otherwise.

## GitHub findings

### 2346-U

Exact number/date/title and characteristic-text searches did not produce a full normative body or reliable GitHub body candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### 141-T

Exact number/date/title searches did not produce a full letter body or reliable candidate. Short-number searches produced only unrelated token/section/SKU collisions, all rejected before candidate stage.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER / CBR_LETTER_NON_NPA_GUIDANCE`

### 154-T

Exact number/date/title and characteristic-text searches did not produce a full letter body or reliable candidate. Short-number search results were unrelated numerical/text collisions.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER / CBR_LETTER_NON_NPA_GUIDANCE`

### 390-P — operational implementation cluster, not normative body

A new GitHub implementation artifact was confirmed:

- repo: `dbarabo/observer`
- commit/ref: `6667896ff0b865a444e327cffba1ac5465479de4`
- path: `src/main/kotlin/ru/barabo/observer/config/cbr/ticket/task/Get390pArchive.kt`
- blob: `f596216cd6cfcbfcdd0d9dc32fe5a0be59f3dfc2`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `Kotlin source / text`

The file contains operational names and paths such as `390-П Получить Архив`, `X:/390-П`, `C:/390-П`, and archive header `AFT_FTS`; it processes incoming archives and sends workflow notifications. It does **not** contain the target date `30.11.2012`, target title, registration No. 26780, or the normative body.

Classification:

`OPERATIONAL_INTEGRATION_CODE / NUMBER_REFERENCE_AND_WORKFLOW_ONLY / TARGET_FULL_IDENTITY_NOT_PRESENT / REJECTED_AS_NORMATIVE_BODY`

The same repository contains several additional `390-П` workflow modules (`Ticket390IzvXml.kt`, `SendByPtkPsdCopy.kt`, `Sign390pArchive.kt`, `CreateSaveResponse390p.kt`). These form a `DERIVED_IMPLEMENTATION_CLUSTER`, not normative-body duplicates.

The target remains `GITHUB_FULL_TEXT_BLOCKER`.

### 147-I

Exact number/date/title searches did not produce a full GitHub normative body or reliable candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### 49-T

Exact number/date/title and characteristic-text searches did not produce a full letter body or reliable GitHub candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER / CBR_LETTER_NON_NPA_GUIDANCE`

## Primary official / current-status checks

### 2346-U — edition advanced at least through 5461-U / 2020

Bank of Russia official materials confirm the original identity and Ministry of Justice registration No. 15828. The official Vestnik body of Instruction No. 5461-U of 19.05.2020 directly amends Appendix 1 to No. 2346-U, lists the prior registration chain, and states official publication on 25.06.2020. Therefore an original-2009 GitHub copy without the amendment chain cannot be treated as the current consolidated body.

Confirmed primary amendment layer:

- `5461-U` dated `19.05.2020`
- Ministry of Justice registration `58688` dated `17.06.2020`
- official publication on CBR site `25.06.2020`
- effect: 10 days after official publication

Classification:

- `PRIMARY_ORIGINAL_IDENTITY_CONFIRMED`
- `PRIMARY_AMENDMENT_5461-U_CONFIRMED`
- `CURRENT_EDITION_ADVANCED_AT_LEAST_2020-05-19`
- `PRIMARY_FORMAL_CURRENT_STATUS_OR_LATER_SUPERSESSION_BLOCKER`

No later primary repeal/supersession was resolved in this pass; absence of a search hit is not proof of continuing force.

### 141-T — final official Vestnik body confirmed; separate CBR static PDF carries a draft label

The official Bank of Russia press release of 27.10.2010 confirms issuance of Letter No. 141-T and its exact title/purpose. The official Vestnik No. 59 (1228) of 03.11.2010 contains the dated letter and full Recommendations body, so primary identity/full text is cleanly confirmed.

A separate CBR-hosted static PDF at `/StaticHtml/File/17579/141-t.pdf` is indexed/titled `Проект` while containing the appendix linked to Letter No. 141-T. This is retained as a provenance/display conflict, not as a reason to override the finalized Vestnik publication.

Classification:

- `PRIMARY_FULL_BODY_CONFIRMED_CBR_VESTNIK`
- `CBR_LETTER_NON_NPA_GUIDANCE`
- `PRIMARY_HOSTED_DRAFT_LABEL_CONFLICT`
- `CANONICAL_FINAL_REPRESENTATION = VESTNIK_59_2010`
- `PRIMARY_CURRENT_APPLICABILITY_OR_SUPERSESSION_BLOCKER`

### 154-T — primary full body confirmed; non-NPA guidance layer

Official Vestnik No. 64 (1233) of 24.11.2010 contains the exact date `22.11.2010`, number `154-T`, full title and recommendation text. This is a Bank of Russia letter/recommendation, not silently promoted to a normative legal act.

Classification:

- `PRIMARY_FULL_BODY_CONFIRMED_CBR_VESTNIK`
- `CBR_LETTER_NON_NPA_GUIDANCE`
- `PRIMARY_CURRENT_APPLICABILITY_OR_SUPERSESSION_BLOCKER`

### 390-P — formally repealed from 01.10.2021; legacy terminology survives operationally

The official Vestnik No. 9 (2249) of 17.02.2021 contains Regulation No. 741-P of 30.11.2020. Clause 4.1 states that No. 741-P enters into force on `01.10.2021`; clause 4.2 explicitly recognizes Regulation No. 390-P of 30.11.2012 (Ministry of Justice No. 26780) as invalid from the same date.

Classification:

- `PRIMARY_REPEAL_CONFIRMED`
- `HABR_STALE_REPEALED_BANK_ACT`
- `REPEALED_BY_741-P`
- `REPEAL_EFFECTIVE_2021-10-01`
- `DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`

There is a new lifecycle/provenance conflict worth preserving: the current CBR electronic-format page, last updated 03.12.2025, still exposes an explicit legacy section and XSD links "in accordance with Regulation No. 390-P" while also exposing the replacement No. 741-P formats. The GitHub `dbarabo/observer` code likewise still uses `390-П` operational terminology in a 2026 repository snapshot. Neither operational persistence restores legal force.

Classification of this conflict:

- `PRIMARY_SITE_LEGACY_OPERATIONAL_REFERENCE_CONFLICT`
- `LEGACY_TERMINOLOGY_SURVIVES_AFTER_REPEAL`
- `LEGAL_STATUS_WINS_OVER_OPERATIONAL_LABEL`

Habr itself also lists both No. 390-P (position 10) and its replacement No. 741-P (later position 30) without marking the former repealed, so record `HABR_INTERNAL_LIFECYCLE_DUPLICATION` rather than treating both as simultaneous current requirements.

### 147-I — repealed from 08.05.2020 by transition to 202-I

The official 2014 Vestnik index confirms No. 147-I, date 05.12.2013 and its exact title. A later Bank of Russia primary regulatory-review document states explicitly that Instruction No. 147-I was recognized as invalid in connection with entry into force on `08.05.2020` of Instruction No. 202-I of 15.01.2020, registered by the Ministry of Justice on 22.04.2020 No. 58159. Later Bank of Russia acts also replace references to 147-I with 202-I.

Classification:

- `PRIMARY_REPEAL_CONFIRMED`
- `HABR_STALE_REPEALED_BANK_ACT`
- `REPEALED_BY_202-I`
- `REPEAL_EFFECTIVE_2020-05-08`
- `DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`

### 49-T — primary full body confirmed; non-NPA guidance layer

Official Vestnik No. 34 (1512) of 31.03.2014 contains the exact date `24.03.2014`, number `49-T`, title and letter body stating that the Bank of Russia sends Recommendations on organizing use of malware-protection tools in banking activity.

Classification:

- `PRIMARY_FULL_BODY_CONFIRMED_CBR_VESTNIK`
- `CBR_LETTER_NON_NPA_GUIDANCE`
- `PRIMARY_CURRENT_APPLICABILITY_OR_SUPERSESSION_BLOCKER`

## Delta counters

- `GITHUB_FULL_TEXT_CURRENT +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `DERIVED_IMPLEMENTATION_CLUSTER +1 target / >=5 code files` (390-P)
- `OPERATIONAL_INTEGRATION_CODE_REJECTED +1 principal artifact`
- `PRIMARY_FULL_BODY_CONFIRMED_CBR +3` (141-T, 154-T, 49-T)
- `PRIMARY_AMENDMENT_CONFIRMED +1` (2346-U <- 5461-U)
- `PRIMARY_REPEAL_CONFIRMED +2` (390-P, 147-I)
- `HABR_STALE_REPEALED_BANK_ACT +2`
- `HABR_INTERNAL_LIFECYCLE_DUPLICATION +1` (390-P + 741-P)
- `PRIMARY_HOSTED_DRAFT_LABEL_CONFLICT +1` (141-T static PDF vs final Vestnik)
- `PRIMARY_SITE_LEGACY_OPERATIONAL_REFERENCE_CONFLICT +1` (390-P formats after repeal)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Next boundary

Continue from Habr banking-security position 13:

1. Bank of Russia Regulation No. 440-P of 06.11.2014.
2. Instruction No. 3893-U of 11.12.2015.
3. Instruction No. 4212-U of 24.11.2016.
4. Regulation No. 579-P of 27.02.2017.
5. Instruction No. 4512-U of 30.08.2017.
6. Regulation No. 600-P of 20.09.2017.

Continue to keep normative acts, information letters/recommendations, current/repealed/future layers, and operational legacy references separated in the knowledge model.
