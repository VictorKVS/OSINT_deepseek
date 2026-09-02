# Habr NPA sweep — Stream 1 — 2026-09-02 17:53 MSK

## Scope

Continued Habr 432466 / user NPA sweep. This pass covers Bank of Russia acts 3–7 in the Habr section `Национальная платежная система`, kept in a separate `BANK_OF_RUSSIA_REGULATORY_LAYER`:

1. Bank of Russia Instruction No. 2695-U of 14.09.2011, `О требованиях к обеспечению бесперебойности осуществления перевода электронных денежных средств`.
2. Bank of Russia Instruction No. 2831-U of 09.06.2012, `Об отчетности по обеспечению защиты информации при осуществлении переводов денежных средств операторов платежных систем, операторов услуг платежной инфраструктуры, операторов по переводу денежных средств`.
3. Bank of Russia Regulation No. 422-P of 11.06.2014, `О порядке признания Банком России платежной системы национально значимой платежной системой`.
4. Bank of Russia Instruction No. 3342-U of 25.07.2014, `О требованиях к информационным технологиям, используемым операторами услуг платежной инфраструктуры, для целей признания платежной системы национально значимой платежной системой`.
5. Bank of Russia Regulation No. 607-P of 03.10.2017, `О требованиях к порядку обеспечения бесперебойности функционирования платежной системы, показателям бесперебойности функционирования платежной системы и методикам анализа рисков в платежной системе, включая профили рисков`.

GitHub copies are never treated as official merely because they are on GitHub. GitHub-body identity/completeness and primary official/current status are separate gates.

## GitHub findings

### 2695-U

Exact number/title searches did not produce a full normative body or reliable body candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### 2831-U

The previously identified derived NPS list is also an exact bibliographic hit for 2831-U:

- repo: `LAIR-RCC/InfSecurityRussianNLP`
- commit/ref: `0f072394f0ada37f607bc4a3da2f22fdd5201eae`
- path: `seccoll/1255.txt`
- blob: `d0d2f7c4efbb541393d62d62843cc996c3a6f26f`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `text/plain`

Internal identity check: the file contains `2831-У`, date `09.06.2012`, and the full target title. It is explicitly a topical list of NPS documents with `почитать/скачать` pointers, not the normative body.

Classification:

`DOCUMENT_LIST / POINTER_ONLY / BIBLIOGRAPHIC_IDENTITY_PASS / REJECTED_AS_NORMATIVE_BODY`

This extends the already known multi-target relationship of `seccoll/1255.txt`: the same derived file now maps to 161-FZ, Government Resolution No. 584, and 2831-U.

A paired annotation artifact was also confirmed:

- repo: `LAIR-RCC/InfSecurityRussianNLP`
- commit/ref: `0f072394f0ada37f607bc4a3da2f22fdd5201eae`
- path: `seccoll/1255.ann`
- blob: `668ac84cd8a8ae38bade6f564be28ea18f6bb793`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: annotation/text

It contains an `ARTEFACT` span with number + full title for 2831-U but no full normative text and no independent date identity. Classification: `ANNOTATION_LAYER / DERIVED_FROM_SOURCE_RECORD / REJECTED_AS_NORMATIVE_BODY`.

Another GitHub text, `seccoll/12513.txt`, discusses reporting and assessment under 2831-U but contains commentary rather than the act itself. It is not accepted as a body candidate.

No GitHub full normative body was found for 2831-U.

### 422-P

Exact number/title searches did not produce a GitHub normative body or reliable body candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### 3342-U

Exact number/title searches did not produce a GitHub normative body or reliable body candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### 607-P

A GitHub number collision / wrong-target summary was confirmed:

- repo: `nik1138/Frontend-knowledge-vault-ru`
- commit/ref: `611a232ac55e5ea48ee34dde65e9da8907d5554f`
- path: `планы_обучения/middle/week13/day6/Другие_материалы.md`
- blob: `5e6a82d3aa809abb6bfa13b2941d4d1ef3bebe14`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `text/markdown`

Internal text says `Положение Банка России №607-П — О требованиях к системе управления рисками кредитных организаций`. This title/subject does not match the target 607-P on payment-system continuity and payment-system risk analysis. Date and exact target title are absent.

Classification:

`NUMBER_COLLISION_607P / WRONG_TARGET_SUMMARY / TARGET_IDENTITY_MISMATCH / REJECTED_AS_TARGET_BODY`

Exact target-title searches produced no full normative GitHub body.

## Primary official / current-status checks

### 2695-U

Bank of Russia primary publication text confirms:

- date: 14.09.2011
- number: 2695-U
- exact target title
- Ministry of Justice registration No. 21877 dated 23.09.2011.

The primary original is therefore confirmed. This pass did not resolve a later primary act explicitly repealing the instruction, but absence of a found repeal is not treated as proof of current force.

Classification:

- `PRIMARY_ORIGINAL_CONFIRMED`
- `PRIMARY_CURRENT_STATUS_BLOCKER`

Primary source: https://www.cbr.ru/queries/unidbquery/file/48362/58

### 2831-U

A material Habr freshness conflict is confirmed by the Bank of Russia's own official publication of Instruction No. 6060-U of 12.01.2022.

In paragraph 9, No. 6060-U explicitly states that from `01.03.2023` Bank of Russia Instruction No. 2831-U of 09.06.2012 is recognized as invalid, together with its amending instructions No. 3024-U and No. 4753-U.

Therefore Habr 432466 (version 28.05.2026) still listing 2831-U in the NPS section is stale for current applicability.

Classification:

- `HABR_STALE_REPEALED_BANK_ACT`
- `REPEALED_BY_6060-U`
- `REPEAL_EFFECTIVE_2023-03-01`
- `DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`

Primary source: https://www.cbr.ru/Queries/XsltBlock/File/105012/-1/2351

### 422-P

Bank of Russia has a dedicated primary application page for 422-P with exact number/date/title and explanatory material on its application. The Bank of Russia 2014 official-act index also confirms the act; Bank of Russia press material confirms the 2017 amendment No. 4436-U.

The primary Bank of Russia page remains available, but a dedicated formal `current/invalid` status flag was not exposed by that page in this pass. Therefore operational use evidence and formal no-repeal status remain separate.

Classification:

- `PRIMARY_CBR_APPLICATION_PAGE_CONFIRMED`
- `PRIMARY_AMENDMENT_4436-U_CONFIRMED`
- `FORMAL_CURRENT_STATUS_FLAG_BLOCKER`

Primary sources:

- https://www.cbr.ru/psystem/acts/422-p/
- https://www.cbr.ru/about_br/publ/vestnik-akts/?year=2014

### 3342-U

Bank of Russia primary official publication confirms date, number, exact title, Ministry of Justice registration No. 34269, and publication in `Вестник Банка России` No. 95 (1573) of 14.10.2014.

A Bank of Russia document published in 2026 still expressly cites 3342-U with the same title and registration data when describing requirements to cryptographic/information technologies in payment infrastructure. This is strong current operational-reference evidence, but it is not collapsed into a formal legal-status flag.

Classification:

- `PRIMARY_ORIGINAL_CONFIRMED`
- `PRIMARY_CURRENT_REFERENCE_CONFIRMED_2026`
- `FORMAL_CURRENT_STATUS_FLAG_BLOCKER`

Primary sources:

- https://www.cbr.ru/Queries/XsltBlock/File/105012/-1/1573
- https://www.cbr.ru/Queries/UniDbQuery/File/90134/607

### 607-P

Primary Bank of Russia sources confirm the original act and the later amendment:

- Regulation No. 607-P was officially published by the Bank of Russia on 29.12.2017; Ministry of Justice registration No. 49386.
- Instruction No. 6352-U of 09.01.2023 directly amends 607-P; Ministry of Justice registration No. 73250.
- The official text of No. 6352-U states that the amendments enter into force on `01.10.2023`.

Current consolidated secondary legal systems identify the edition as `09.01.2023`, effective from `01.10.2023`. Recent Bank of Russia materials continue to cite 607-P as amended by 6352-U.

Classification:

- `CURRENT_EDITION_ADVANCED_607P_2023-01-09`
- `PRIMARY_AMENDMENT_6352-U_CONFIRMED`
- `AMENDMENT_EFFECTIVE_2023-10-01`
- `PRIMARY_CURRENT_REFERENCE_CONFIRMED`

Primary sources:

- https://www.cbr.ru/press/pr/?file=15012018_112502vbr2018-01-15t11_17_07.htm
- https://cbr.ru/Queries/XsltBlock/File/105012/-1/2432

## Delta counters

- `GITHUB_FULL_TEXT_CURRENT +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `GITHUB_POINTER_LIST_REJECTED +1 target-hit`
- `GITHUB_ANNOTATION_LAYER_REJECTED +1`
- `GITHUB_COMMENTARY_REJECTED +1`
- `DERIVED_MULTI_TARGET_FILE_TARGET_EXPANSION +1`
- `NUMBER_COLLISION_TARGET_IDENTITY_MISMATCH +1`
- `HABR_STALE_REPEALED_BANK_ACT +1`
- `PRIMARY_ORIGINAL_CONFIRMED +4` (2695-U, 2831-U via repealing primary context/original references, 3342-U, 607-P; 422-P separately has a dedicated CBR application page)
- `PRIMARY_CURRENT_REFERENCE_CONFIRMED +2` (3342-U, 607-P)
- `PRIMARY_AMENDMENT_CONFIRMED +2` (4436-U -> 422-P; 6352-U -> 607-P)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_BODY_IDENTITY_CONFLICT +0`

## Blockers

1. No GitHub full normative body found for any of the five targets.
2. Exact byte sizes of the derived GitHub text/annotation files were not exposed by the connector metadata; they are not estimated.
3. Formal primary current-status/repeal flags remain unresolved for 2695-U and are not inferred from absence of a repeal hit.
4. For 422-P and 3342-U, primary Bank of Russia operational/current-reference evidence is present, but a dedicated formal current-status flag was not exposed; keep those gates separate.

## Next boundary

Continue Habr NPS items 8–13:

`742-P -> 760-P -> 18-MR -> 802-P -> 821-P -> 876-P`.

Keep 18-MR classified as methodological/recommendatory material, not silently as a normative legal act.
