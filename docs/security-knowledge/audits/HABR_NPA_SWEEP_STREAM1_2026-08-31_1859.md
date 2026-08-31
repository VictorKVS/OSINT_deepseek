# Habr NPA sweep — Stream 1 — 2026-08-31 18:59 MSK

## Scope
Continuation of Habr 432466, section `Защита связи`, positions 3–8:

1. Постановление Правительства РФ от 27.08.2005 № 538.
2. Постановление Правительства РФ от 25.06.2009 № 532.
3. Постановление Правительства РФ от 14.11.2014 № 1194.
4. Постановление Правительства РФ от 12.04.2018 № 445.
5. Постановление Правительства РФ от 12.10.2019 № 1316.
6. Постановление Правительства РФ от 29.10.2019 № 1385.

Method: GitHub body search is separate from legal-status verification. A GitHub copy is never promoted to official status. Full-body, mention/reference and digest/index artifacts are classified separately. Currentness is checked independently against the official publication chain; where a primary current/consolidated card was not closed, a blocker remains explicit.

## GitHub normative-body result

| Target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| PP 538/2005 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 532/2009 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 1194/2014 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 445/2018 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 1316/2019 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 1385/2019 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

No GitHub file in this pass was promoted to `FULL_TEXT` or `RELIABLE_GITHUB_CANDIDATE`.

## Rejected GitHub hits

### PP 538/2005

- repo: `liberatetheweb/anonymous-handbook`
- commit: `0c1ef298a45f066ca0a55b03873793190fa6c690`
- path: `bibliography.bib`
- blob: `e6f388ee2e70f67d40cb4adc34c20a97630ba266`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `BibTeX`
- identity evidence: bibliographic entry names `Постановление Правительства РФ от 27.08.2005 N 538` and its title.
- classification: `MENTION_ONLY / BIBLIOGRAPHY_REFERENCE / REJECTED_AS_NORMATIVE_BODY`.

This is a citation to the act, not its normative body.

### PP 532/2009

One legal-training corpus produced four related files that cite PP 532 but do not reproduce its complete body:

- repo: `artyom-zolotarevskiy/ru-gpt-3-training-legal`
- commit: `bd0edd5446d2ce94f15d976d34d339dd6f924f35`
- paths: `commercial/11137.txt`, `commercial/13668.txt`, `court_civil/13134.txt`, `criminal/10535.txt`
- size: `UNRESOLVED_CONNECTOR_METADATA` for rejected mention hits
- type: `TXT`
- classification: `MENTION_ONLY / LEGAL_CORPUS / REJECTED_AS_NORMATIVE_BODY`.

The group is recorded as `MENTION_DUPLICATE_GROUP`, not a normative-body duplicate.

## Confirmed lifecycle findings / conflicts

### PP 532/2009 — Habr stale/repealed-act conflict

Habr version 28.05.2026 still lists PP RF 25.06.2009 № 532 as a target in `Защита связи`. PP RF 04.02.2022 № 113 approved a replacement mandatory-certification list, expressly included PP 532 in the acts recognized as no longer in force, and entered into force on 01.09.2022. Therefore:

- `HABR_REPEALED_ACT_CONFLICT = true`
- lifecycle: `PP_532_REPEALED_EFFECTIVE_2022-09-01`
- replacement: `PP_113_2022`
- gate: `OLD_LIST_REFERENCE != CURRENT_CERTIFICATION_LIST`.

Primary official publication-card retrieval for PP 113 was not closed in this pass, so the repeal/effective-date evidence is retained with `PRIMARY_REPLACEMENT_PUBLICATION_DIRECT_FETCH_BLOCKER` rather than falsely promoted to direct-primary.

### PP 1194/2014 — latest amendment after Habr base identity

PP RF 27.09.2025 № 1483 directly amended point 62 of the Rules approved by PP 1194. Secondary legal sources consistently show the consolidated base act as `ред. от 27.09.2025`; the amending act was published 01.10.2025 and is reported effective from 07.10.2025.

- `LATEST_AMENDMENT = PP_1483_2025`
- `CURRENT_CONSOLIDATED_EDITION_CORROBORATED = 2025-09-27`
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_DIRECT_FETCH_BLOCKER` remains because the primary publication card was not resolved directly in this run.

Full-text gate for any later GitHub candidate: `PP body + both approved Rules + amendments/current wording`; a file containing only one Rules block is `PARTIAL_TEXT`.

### PP 538/2005 — current edition corroborated, primary-current blocker remains

Consolidated sources show `ред. от 17.04.2021`; PP RF 17.04.2021 № 613 created that edition, effective from 30.04.2021. No later amendment/repeal was confirmed in this pass.

- `CURRENT_EDITION_CORROBORATED_NONPRIMARY = 2021-04-17`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Full-text gate: `postanovlenie + complete Rules`, not a bibliography entry or a quotation of individual paragraphs.

### PP 445/2018

Consolidated sources show the Rules in `ред. от 28.03.2022`; PP RF 28.03.2022 № 498 directly amended PP 445. No later amendment/repeal was confirmed in this pass.

- `CURRENT_EDITION_CORROBORATED_NONPRIMARY = 2022-03-28`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Full-text gate: `postanovlenie + complete current Rules`.

### PP 1316/2019

Consolidated sources show `ред. от 27.10.2023`; PP RF 27.10.2023 № 1790 amended the exercise Regulation. No later amendment to this 2019 act was confirmed in this pass.

A separate PP RF `№ 1316` dated 29.08.2025 exists and concerns providing telecom-operator information through SMEV. It is a distinct act and must never be merged with PP 12.10.2019 № 1316.

- gate: `SAME_NUMBER_DIFFERENT_DATE != SAME_ACT`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true` for the 2019 act.

### PP 1385/2019

Identity verified as PP RF 29.10.2019 № 1385 approving Rules for interaction of owners/other holders of technological communications networks with authorized state bodies conducting operational-search activity or ensuring security of the Russian Federation. No later amendment or formal repeal was confirmed in this pass.

- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.
- gate: `NUMBER_MATCH_ONLY` is unsafe because a different PP № 1385 dated 16.10.2024 also exists.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `GITHUB_MENTION_ONLY_REJECTED +5`
- `MENTION_DUPLICATE_GROUP +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_REPEALED_ACT_CONFLICT +1`
- `SAME_NUMBER_DIFFERENT_DATE_COLLISION +2` (1316 and 1385 number collisions identified as a retrieval/identity gate)

## New gates

1. `MENTION_DUPLICATE_GROUP != FULL_BODY_DUPLICATE`.
2. `REPEALED_TARGET_IN_HABR != CURRENT_ACT`.
3. `PRIMARY_AMENDING_ACT_PUBLICATION != PRIMARY_CONSOLIDATED_CURRENT_TEXT`.
4. `SAME_NUMBER_DIFFERENT_DATE != SAME_ACT`.
5. `NUMBER_DATE_TITLE_IDENTITY != CURRENTNESS != OFFICIAL_STATUS`.

## Next boundary
Continue `Защита связи` from PP RF 12.02.2020 № 126 onward, while retaining priority for federal laws, presidential/government acts, Roskomnadzor, and general PDn/information regulation.