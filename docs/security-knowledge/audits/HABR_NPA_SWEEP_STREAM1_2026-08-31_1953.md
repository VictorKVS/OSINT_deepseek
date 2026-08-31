# Habr NPA sweep — Stream 1 — 2026-08-31 19:53 MSK

## Scope
Continuation of Habr 432466, section `Защита связи`, positions 9–14:

1. Постановление Правительства РФ от 12.02.2020 № 126.
2. Постановление Правительства РФ от 12.02.2020 № 127.
3. Постановление Правительства РФ от 03.11.2022 № 1979.
4. Распоряжение Правительства РФ от 15.11.2022 № 3461-р.
5. Постановление Правительства РФ от 08.06.2023 № 944.
6. Постановление Правительства РФ от 15.01.2024 № 4.

Method: GitHub body search is separate from legal-status verification. A GitHub copy is never promoted to official status. Full-body, mention/reference and digest/index artifacts are classified separately. Identity requires at minimum type/authority + number + date + title/body consistency. Currentness and official status are verified separately against the primary publication chain; unresolved primary current/consolidated status is retained as an explicit blocker.

Habr source: https://habr.com/ru/articles/432466/ (version shown by Habr: 28.05.2026).

## GitHub normative-body result

| Target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| PP 126/2020 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 127/2020 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 1979/2022 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| RF Gov Order 3461-r/2022 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 944/2023 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| PP 4/2024 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

Exact GitHub searches by number/date/title and distinctive title fragments did not produce a normative body or a reliable candidate for these six targets. Broad phrase searches produced only unrelated corpora, study/reference pages and other noise; none passed number/date/title/body identity, so no false-positive file was promoted.

Replacement acts PP 1333/2025 and PP 1667/2025 were also searched on GitHub during lifecycle verification; no reliable full-body candidate was confirmed.

## Confirmed lifecycle findings / conflicts

### PP 126/2020 — Habr stale expired-act conflict

Habr version 28.05.2026 still lists PP RF 12.02.2020 № 126 as the operative target. The latest consolidated body contains a sunset clause: `Настоящее постановление действует до 1 сентября 2025 г.`. The 28.02.2024 amendment PP № 224 is officially published under publication number `0001202402290015` and is part of the final 2020-act edition.

A replacement act now exists:

- PP RF 30.08.2025 № 1333 — same regulatory subject, approving new Rules for installation, operation and modernization of TSPU in an operator network;
- effective from 01.09.2025;
- reported official publication pointer: `0001202508300019`;
- direct retrieval of that publication card timed out in this pass, so it remains `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_FETCH_BLOCKER`, not a fabricated direct-primary fetch.

Classification:

- `HABR_EXPIRED_ACT_CONFLICT = true`
- `PP_126_SUNSET_EFFECTIVE = 2025-09-01`
- `CURRENT_REPLACEMENT = PP_1333_2025`
- gate: `SUNSET_EXPIRY != FORMAL_REPEAL`, but both are incompatible with treating PP 126 as current on 2026-08-31.

Primary/publication evidence:

- PP 224/2024 publication pointer: https://publication.pravo.gov.ru/document/0001202402290015
- PP 1333/2025 publication pointer: https://publication.pravo.gov.ru/document/0001202508300019

Full-text gate for PP 126 or PP 1333: `postanovlenie + complete approved Rules`; a file containing only the operative clauses is `PARTIAL_TEXT`.

### PP 127/2020 — Habr expressly repealed-act conflict

Habr version 28.05.2026 still lists PP RF 12.02.2020 № 127. PP RF 27.10.2025 № 1667 approved new Rules of centralized management of the public communications network and expressly recognizes PP 127/2020 and its amendment chain as no longer in force.

The replacement is directly confirmed on the official publication portal:

- PP RF 27.10.2025 № 1667;
- official publication number `0001202511060014`;
- publication date 06.11.2025;
- effective from 01.03.2026;
- valid until 01.03.2032;
- clause 2 explicitly lists PP 127/2020 among acts recognized as invalid.

Classification:

- `HABR_REPEALED_ACT_CONFLICT = true`
- `PP_127_REPEALED_EFFECTIVE_2026-03-01`
- `PRIMARY_REPLACEMENT_PUBLICATION_CONFIRMED = true`
- `CURRENT_REPLACEMENT = PP_1667_2025`.

Primary source: https://publication.pravo.gov.ru/document/0001202511060014

Full-text gate for current regulation: PP 1667 body + all approved Rules. An old PP 127 text, even if complete, is `FULL_TEXT_BUT_REPEALED`, never `CURRENT_FULL_TEXT`.

### PP 1979/2022 — currentness corroborated; built-in sunset

Identity and completeness are corroborated for PP RF 03.11.2022 № 1979. It entered into force on 01.01.2023 and, by its own clause 2, operates for six years; legal sources therefore mark its validity as limited to 01.01.2029.

No later amending or repealing act was confirmed in this pass. Because a direct primary current/consolidated card was not closed, status remains:

- `CURRENTNESS_CORROBORATED_NONPRIMARY`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`
- `BUILT_IN_SUNSET = 2029-01-01`.

Completeness is important: the act includes `postanovlenie + Rules + Appendix: format of data sent to/from the compliance system`. A GitHub file missing the Appendix is `PARTIAL_TEXT`.

### RF Gov Order 3461-r/2022 — official publication pointer confirmed, direct fetch blocked

Identity is confirmed as RF Government Order 15.11.2022 № 3461-р approving the list of publicly available information included in the registry of communication lines crossing the State Border of the Russian Federation and the communication facilities to which those lines are connected.

Habr links to the official publication card. The resolved official pointer is:

- `0001202211150029`
- https://publication.pravo.gov.ru/Document/View/0001202211150029

Direct retrieval timed out in this pass, therefore:

- `OFFICIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true` (no later repeal/amendment was established, but absence of a found repeal is not treated as direct proof of currentness).

Full-text gate: `order + complete approved list`; an order page without the list is `PARTIAL_TEXT`.

### PP 944/2023 — primary Government hosting confirmed

PP RF 08.06.2023 № 944 is directly corroborated by the official Government resource (`government.ru/docs/all/147974/`) with matching number/date/title concerning anti-terrorist protection of MinTsifry, Roskomnadzor and related/subordinate facilities.

No later repeal or amendment was confirmed in this pass. Operational use is also corroborated by later enforcement/court materials, but operational citation is not substituted for a primary consolidated status card.

Status:

- `PRIMARY_INITIAL_GOVERNMENT_HOSTING_CONFIRMED = true`
- `CURRENT_OPERATIONAL_USE_CORROBORATED = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Primary Government source: https://government.ru/docs/all/147974/

Full-text gate: `postanovlenie + complete approved Requirements + any integral appendices/forms`; a fragment of the requirements is not `FULL_TEXT`.

### PP 4/2024 — current status corroborated, primary publication card unresolved

PP RF 15.01.2024 № 4 is consistently identified as the Rules for installation, operation and modernization of TSPU at traffic exchange points. Consolidated legal sources mark:

- edition: 15.01.2024;
- effective date: 24.01.2024;
- status: current.

No later amendment/repeal was confirmed in this pass. A primary publication-card identifier was not reliably resolved, therefore:

- `CURRENTNESS_CORROBORATED_NONPRIMARY = true`
- `PRIMARY_INITIAL_PUBLICATION_ID_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Full-text gate: `postanovlenie + complete approved Rules`.

## Identity / retrieval gates added

1. `SUNSET_EXPIRY != FORMAL_REPEAL`, but an expired act is not current.
2. `FULL_TEXT_BUT_REPEALED != CURRENT_FULL_TEXT`.
3. `OFFICIAL_PUBLICATION_POINTER != SUCCESSFUL_PRIMARY_FETCH`.
4. `NO_REPEAL_FOUND != PRIMARY_CURRENT_STATUS_CONFIRMED`.
5. `NUMBER_DATE_TITLE_IDENTITY != CURRENTNESS != OFFICIAL_STATUS`.
6. `POSTANOVLENIE_WITHOUT_APPROVED_RULES_OR_APPENDIX != FULL_TEXT`.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_EXPIRED_ACT_CONFLICT +1` (PP 126/2020)
- `HABR_REPEALED_ACT_CONFLICT +1` (PP 127/2020)
- `PRIMARY_REPLACEMENT_PUBLICATION_CONFIRMED +1` (PP 1667/2025)
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED_WITH_DIRECT_FETCH_BLOCKER +2` (PP 1333/2025, Order 3461-r/2022)
- `BUILT_IN_SUNSET_CONFIRMED +1` (PP 1979/2022)

## Next boundary
Continue `Защита связи` with PP RF 23.05.2024 № 639 and then positions 16 onward, prioritizing Roskomnadzor and general federal/Government regulation of information and personal data.