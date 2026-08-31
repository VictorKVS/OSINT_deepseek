# Habr NPA sweep — Stream 1 — 2026-08-31 03:56 MSK

## Scope

Continuation of the systematic sweep of Habr article 432466, section **«Идентификация и аутентификация»**, positions 38–43:

1. Приказ Минцифры России от 25.02.2022 № 142
2. Приказ Минцифры России от 09.09.2022 № 658
3. Приказ Минцифры России от 31.03.2023 № 334
4. Приказ Минцифры России от 17.04.2023 № 378
5. Приказ Минцифры России от 20.04.2023 № 387
6. Приказ Минцифры России от 27.04.2023 № 432

Habr snapshot checked: version 28.05.2026, https://habr.com/ru/articles/432466/ . Positions 38–43 still list all six targets.

## GitHub body search

Exact number/date searches and title-fragment searches were run through GitHub code search for all six targets. Additional web-indexed searches restricted to `github.com` returned no target body. No indexed full normative text and no reliable body candidate was found.

| Target | repo | commit | path | size | type | Classification |
|---|---|---|---|---:|---|---|
| №142/2022 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №658/2022 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №334/2023 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №378/2023 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №387/2023 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №432/2023 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

No mention/summary artifact was promoted to `FULL_TEXT`. No new GitHub full-body duplicate and no GitHub target-body identity conflict was found.

## Primary publication identity

The initial publication identity of all six targets was resolved on the official publication portal. These official publication records are **provenance/status evidence**, not GitHub copies.

| Target | Minjust registration | Official publication ID | Publication date |
|---|---:|---|---|
| №142/2022 | 68216 | `0001202204150004` | 2022-04-15 |
| №658/2022 | 71923 | `0001202212300065` | 2022-12-30 |
| №334/2023 | 73370 | `0001202305190013` | 2023-05-19 |
| №378/2023 | 73396 | `0001202305240002` | 2023-05-24 |
| №387/2023 | 73366 | `0001202305190014` | 2023-05-19 |
| №432/2023 | 73566 | `0001202305300015` | 2023-05-30 |

Primary URLs:
- https://publication.pravo.gov.ru/Document/View/0001202204150004
- https://publication.pravo.gov.ru/document/0001202212300065
- https://publication.pravo.gov.ru/document/0001202305190013
- https://publication.pravo.gov.ru/document/0001202305240002
- https://publication.pravo.gov.ru/Document/View/0001202305190014
- https://publication.pravo.gov.ru/document/0001202305300015

## Newly confirmed findings

### 1. №142/2022 — applicability expired under the 572-FZ transition even though formal repeal is not yet resolved

This is the main new conflict of the pass.

The official initial publication confirms exact identity: Order Минцифры 25.02.2022 №142, registered 15.04.2022 №68216, publication ID `0001202204150004`.

The full checklist text shows that it was built on the pre-572-FZ architecture and cites, among other sources, PP №1799/2021 and Order №896/2021. Both were later replaced/repealed in the already verified lifecycle graph.

More importantly, an official Минцифры letter dated 08.06.2023 № П24-11789-ОГ expressly states that №142 was adopted under the former Article 14.1 framework of 149-FZ and, under part 13 article 26 of 572-FZ, such acts could be applied only insofar as they did not conflict with the new framework **and no later than 01.01.2025**. The letter also points to PP №585/2023 as the new control regulation.

Source reproducing the official Минцифры letter:
https://normativ.kontur.ru/document/8/451948-pismo-mintsifry-rf-ot-08-06-2023-n-p24-11789-og

Primary 572-FZ publication:
https://publication.pravo.gov.ru/Document/View/0001202212290024

As of the 28.05.2026 Habr snapshot, №142 is still listed without this applicability cutoff. Therefore the classification is:

- `APPLICABILITY_CEASED_NO_LATER_THAN_2025-01-01_BY_TRANSITIONAL_LAW`
- `HABR_TRANSITIONAL_EXPIRY_CONFLICT`
- **not** `FORMALLY_REPEALED` unless a final repeal act is found.

A 2026 draft Minцифры order prepared 21.05.2026 explicitly proposes a new checklist under PP №585/2023 and clause 2 would formally repeal №142. Search in this pass did not resolve a later officially published final version of that draft. Therefore:

- `FINAL_REPLACEMENT_PUBLICATION_BLOCKER`
- `DRAFT_REPLACEMENT_FOUND_NOT_NPA`

Draft source:
https://www.garant.ru/products/ipo/prime/doc/56956132/

This distinction is important: **legal applicability can end before formal repeal metadata is cleaned up**.

### 2. №658/2022 — official identity confirmed; current primary status remains unresolved

Official initial publication ID: `0001202212300065`; registration №71923.

The order body is anchored to point 8 of PP №1753/2021 and retains the old long-form terminology for the biometric system. PP №1753 itself was later amended in the new 572-FZ architecture rather than simply disappearing.

No explicit repeal of №658 was found in this pass, but no primary official consolidated current-status record was resolved either. A current legal-system copy still reproduces the original scan/text.

Classification:
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`
- `CURRENT_STATUS_CORROBORATED_NONPRIMARY`
- `PRIMARY_CURRENT_STATUS_BLOCKER`
- `LEGACY_TERMINOLOGY_DEPENDENCY`

No `REPEALED` flag is assigned.

### 3. №334/2023 — current fixed-term act; new repeal edge to №474/2021

Official initial publication ID: `0001202305190013`, registration №73370.

Current legal-system text reports status `Действует`, effective 01.06.2023 and valid to **01.06.2029**. The operative text directly repeals Minцифры Order №474/2021.

Current corroborating text:
https://normativ.kontur.ru/document/1/449055-prikaz-mintsifry-rf-ot-31-03-2023-n-334

New graph edge:
- `REPEALS_ORDER_474_2021`

Habr's own deleted-document history already lists №474, so this is not a new Habr stale-entry conflict; it is a new lifecycle edge for the corpus.

Classification:
- `CURRENT_STATUS_CORROBORATED_NONPRIMARY`
- `EXPLICIT_VALID_UNTIL_2029-06-01`
- `PRIMARY_CURRENT_STATUS_BLOCKER`

`FULL_TEXT` requires the order plus the complete approved Methodology, not the operative part alone.

### 4. №378/2023 — current-generation methodology; new repeal edge to №816/2021

Official initial publication ID: `0001202305240002`, registration №73396.

The full available text directly states in clause 3 that Minцифры Order №816/2021 is repealed. The act approves **two separate methodologies**; a GitHub candidate containing only the order or one methodology must be `PARTIAL_TEXT`.

Corroborating full text:
https://pravo.ppt.ru/prikaz/mincifry-rossii/n-378-281938

New graph edge:
- `REPEALS_ORDER_816_2021`

Habr's deleted-document history already lists №816, so no stale-entry conflict is added for that predecessor.

Current-status evidence remains nonprimary; no separate primary consolidated status card was resolved in this pass:
- `CURRENT_STATUS_CORROBORATED_NONPRIMARY`
- `PRIMARY_CURRENT_STATUS_BLOCKER`

No explicit 01.06.2029 sunset clause was confirmed in the body inspected for №378; do not infer one merely from adjacent orders.

### 5. №387/2023 — current fixed-term act; direct repeal edge to №896/2021

Official initial publication ID: `0001202305190014`, registration №73366.

The operative text directly repeals Order №896/2021 and states that №387 entered into force 01.06.2023 and operates to **01.06.2029**.

Corroborating full text:
https://sudact.ru/law/prikaz-mintsifry-rossii-ot-20042023-n-387/

New graph edge:
- `REPEALS_ORDER_896_2021`

This also strengthens the №142 staleness finding, because the №142 checklist expressly cites №896 as a source of mandatory requirements.

Classification:
- `CURRENT_STATUS_CORROBORATED_NONPRIMARY`
- `EXPLICIT_VALID_UNTIL_2029-06-01`
- `PRIMARY_CURRENT_STATUS_BLOCKER`

### 6. №432/2023 — current fixed-term act with staged effective date inside the act

Official initial publication ID: `0001202305300015`, registration №73566.

The full text confirms two approved procedures (request/block-delete-destroy procedure and confirmation procedure). It states that the order enters into force after ten days from official publication and operates until **01.06.2029**, while point 6 of Appendix №1 enters into force separately on **01.01.2024**.

Corroborating full text:
https://rulaws.ru/acts/Prikaz-Mintsifry-Rossii-ot-27.04.2023-N-432/

Classification:
- `CURRENT_STATUS_CORROBORATED_NONPRIMARY`
- `EXPLICIT_VALID_UNTIL_2029-06-01`
- `STAGED_EFFECTIVE_DATE_WITHIN_ACT`
- `PRIMARY_CURRENT_STATUS_BLOCKER`

`FULL_TEXT` requires the order + Appendix №1 + Appendix №2.

## Habr conflict/update summary

New confirmed Habr conflict in this range:

- **№142/2022** remains listed in the 28.05.2026 reference even though the 572-FZ transition, as expressly explained by Minцифры in 2023, limited application of the old Article 14.1-based acts to no later than **01.01.2025**. A May 2026 draft exists to replace the checklist and formally repeal №142, but a final published replacement was not resolved in this pass.

No formal repeal of №658 was confirmed. №334/378/387/432 are current-generation 572-FZ-era acts in the sources inspected.

## New/strengthened corpus rules

1. `APPLICABILITY_EXPIRY != FORMAL_REPEAL` — an act can cease to be legally applicable under a statutory transitional clause before an explicit repeal order is found.
2. `DRAFT_REPLACEMENT != CURRENT_NPA` — the 2026 draft checklist is evidence of intended replacement, not a valid replacement act.
3. `ADJACENT_ACT_SUNSET_DATES_MUST_NOT_BE_INFERRED` — №334, №387 and №432 have explicit 01.06.2029 horizons; №378 must not inherit that horizon without text evidence.
4. `CHECKLIST_REFERENCES_REQUIRE_LIFECYCLE_RESOLUTION` — a formally existing checklist can reference predecessor acts already repealed/replaced.
5. Existing rule reconfirmed: `PRIMARY_INITIAL_PUBLICATION != PRIMARY_CURRENT_STATUS`.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +6`
- `HABR_TRANSITIONAL_EXPIRY_CONFLICT +1` (№142)
- `DRAFT_REPLACEMENT_FOUND_NOT_NPA +1`
- `FINAL_REPLACEMENT_PUBLICATION_BLOCKER +1`
- `NEW_REPEAL_EDGE +3` (№334→№474; №378→№816; №387→№896)
- `EXPLICIT_VALIDITY_WINDOW_TO_2029-06-01 +3` (№334, №387, №432)
- `STAGED_EFFECTIVE_DATE_WITHIN_ACT +1` (№432)
- `PRIMARY_CURRENT_STATUS_BLOCKER +6`

## Next queue

Continue after position 43 by deduplicating positions 44+ against already established replacement roles. New work should only be counted where there is new GitHub body evidence, new lifecycle/current-edition evidence, or an unresolved Habr entry. Priority follow-ups from this pass:

- search for a final officially published 2026 replacement of checklist №142 (the 21.05.2026 document is only a draft);
- resolve primary current-status evidence for №658 and whether its legacy terminology/order body was formally updated after the 572-FZ transition;
- then move to the next unresolved Habr/NPA group rather than re-counting №445/446/453/1024 already closed in earlier passes.
