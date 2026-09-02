# Habr NPA sweep — Stream 1 — 2026-09-02 16:52 MSK

## Scope

Continued the Habr 432466 / user NPA sweep. This pass covers the next federal/core boundary in the section on the national payment system:

1. Federal Law No. 161-FZ of 27.06.2011, `О национальной платежной системе`.
2. Government Resolution No. 584 of 13.06.2012, `Об утверждении Положения о защите информации в платежной системе`.

GitHub copies are treated only as independent copies/candidates. Official/current status is verified separately.

## GitHub search result shared by both targets

A single GitHub file contains exact bibliographic entries for both target acts:

- repo: `LAIR-RCC/InfSecurityRussianNLP`
- commit/ref: `0f072394f0ada37f607bc4a3da2f22fdd5201eae`
- path: `seccoll/1255.txt`
- blob: `d0d2f7c4efbb541393d62d62843cc996c3a6f26f`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `text/plain`

Internal inspection: this is a document list / information-security source list. It contains the exact entries for Federal Law No. 161-FZ dated 27.06.2011 and Government Resolution No. 584 dated 13.06.2012, with their titles and outgoing pointers. It does **not** contain the normative bodies of either act.

Classification for both targets:

`DOCUMENT_LIST / POINTER_ONLY / MENTION_WITH_BIBLIOGRAPHIC_IDENTITY / REJECTED_AS_NORMATIVE_BODY`

Because the same derived file points to both target acts:

`DERIVED_MULTI_TARGET_FILE = 1`

Exact/characteristic GitHub searches did not produce a full normative body for either target.

## Federal Law No. 161-FZ of 27.06.2011

### GitHub body status

- full body: not found
- reliable body candidate: not found
- blocker: `GITHUB_FULL_TEXT_BLOCKER`

### Current / official-status layer

Current consolidated legal systems show the law in edition of `04.08.2026`; the list of amending acts includes Federal Laws No. 210-FZ of 26.06.2026 and No. 283-FZ of 04.08.2026. The current layer is already effective as of 01.09.2026.

Primary-publication pointers resolved for the two recent amending acts:

- 210-FZ: `0001202606260070`, publication date 26.06.2026
- 283-FZ: `0001202608040008`, publication date 04.08.2026

Direct primary portal reading was not stable in this pass, therefore publication-pointer confirmation and successful direct-body retrieval remain separate gates.

Classification:

- `POST_HABR_CURRENT_EDITION_ADVANCE`
- `CURRENT_EFFECTIVE_LAYER_ACTIVATED_2026-09-01`
- `PRIMARY_AMENDING_ACT_PUBLICATION_POINTER_RESOLVED_INDIRECTLY`
- `PRIMARY_DIRECT_PUBLICATION_FETCH_BLOCKER`

Reference sources:

- https://www.consultant.ru/document/cons_doc_LAW_115625/
- https://www.cbr.ru/PSystem/acts/161-fz/
- https://publication.pravo.gov.ru/document/0001202606260070
- https://publication.pravo.gov.ru/document/0001202608040008

## Government Resolution No. 584 of 13.06.2012

### GitHub body status

- full body: not found
- reliable body candidate: not found
- blocker: `GITHUB_FULL_TEXT_BLOCKER`

### Current / official-status layer

The current consolidated edition is `08.12.2022`. Government Resolution No. 2250 of 08.12.2022 directly amended paragraph 1 of the Regulation approved by No. 584. The amended edition took effect on 17.12.2022. No later amendment was confirmed in this pass.

The exact primary publication pointer/direct official card for No. 2250 was not securely resolved in this pass, so current-edition confirmation and primary publication evidence are not collapsed into one status.

Classification:

- `CURRENT_EDITION_SECONDARY_CONFIRMED_2022-12-08`
- `PRIMARY_AMENDING_ACT_PUBLICATION_POINTER_OR_DIRECT_CARD_BLOCKER`

Reference sources:

- https://www.consultant.ru/document/cons_doc_LAW_131173/
- https://www.consultant.ru/document/cons_doc_LAW_433827/

## Delta counters

- `GITHUB_FULL_TEXT_CURRENT +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +2`
- `GITHUB_POINTER_LIST_REJECTED +2 target-hits / 1 distinct file`
- `DERIVED_MULTI_TARGET_FILE +1`
- `POST_HABR_CURRENT_EDITION_ADVANCE +1`
- `CURRENT_EFFECTIVE_LAYER_ACTIVATED_2026-09-01 +1`
- `CURRENT_EDITION_SECONDARY_CONFIRMED +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_BODY_IDENTITY_CONFLICT +0`

## Blockers

1. Exact size of `seccoll/1255.txt` was not returned by the connector metadata; do not estimate it.
2. No GitHub full normative body found for either target.
3. Direct primary publication fetch for the recent 161-FZ amending acts was unstable; pointers are known but direct-body verification remains open.
4. Exact primary publication pointer/direct card for Government Resolution No. 2250 remains unresolved.

## Next boundary

Proceed to Bank of Russia acts cited in the Habr national-payment-system section. Keep them as a separate `BANK_OF_RUSSIA_REGULATORY_LAYER`; do not mix them silently with federal laws / Government resolutions.
