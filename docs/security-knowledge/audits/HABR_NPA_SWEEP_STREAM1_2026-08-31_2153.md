# Habr NPA sweep — Stream 1 — 2026-08-31 21:53 MSK

## Scope
Continuation of Habr 432466, section `Защита связи`, positions 22–26:

1. Приказ Минцифры России от 01.11.2023 № 936.
2. Приказ Минцифры России от 29.02.2024 № 147.
3. Приказ Роскомнадзора от 02.02.2023 № 13.
4. Приказ Роскомнадзора от 04.09.2023 № 129.
5. Приказ Роскомнадзора от 19.02.2024 № 25.

Method remains unchanged: GitHub body discovery is independent from legal-status verification. A GitHub copy is never treated as official merely because it contains the text. `FULL_TEXT`, reliable candidate, mention/reference, digest/index, numeric search false positive and identity mismatch are separate classes. Identity requires at minimum authority/type + number + date + title/body agreement. Currentness and official status are verified separately against the primary publication chain.

Habr source: https://habr.com/ru/articles/432466/ (version shown by Habr: 28.05.2026).

## GitHub normative-body result

| Target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| Минцифры 936/2023 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Минцифры 147/2024 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Роскомнадзор 13/2023 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Роскомнадзор 129/2023 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Роскомнадзор 25/2024 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

Exact GitHub searches by number/date/title and distinctive title fragments returned no normative body or reliable candidate for any of the five targets. Broader searches by Minjust registration numbers produced only unrelated CSV/news/torrent/tf-idf/translation corpus hits. They are recorded as `SEARCH_FALSE_POSITIVE`, not `MENTION_ONLY`, because legal-context identity was not established. No repo/commit/path/size/type metadata is promoted from such noise. No full-body duplicate and no GitHub body-identity conflict were confirmed in this pass.

## Confirmed official-publication / lifecycle findings

### Минцифры 01.11.2023 № 936 — primary publication index confirmed

Identity is confirmed by the official publication index:

- title: `Об утверждении требований о защите информации при предоставлении вычислительной мощности для размещения информации в информационной системе, постоянно подключенной к информационно-телекоммуникационной сети "Интернет"`;
- Minjust registration: 01.12.2023 № 76222;
- official publication id: `0001202312010021`;
- official publication date: 01.12.2023;
- official index benchmark: PDF 256 KB, 4 pages;
- effective date corroborated as 12.12.2023.

Official URL: https://publication.pravo.gov.ru/document/0001202312010021

Direct retrieval of the official card was unstable/timed out during this pass, therefore `PRIMARY_DIRECT_FETCH_BLOCKER` remains separate from the confirmed official-publication index. No later repealing/amending act was confirmed in targeted searches; this is not promoted to direct proof of current consolidated status.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_INDEX_CONFIRMED = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`
- `HABR_IDENTITY_CONFLICT = false`.

Completeness gate: `order + complete approved Requirements`; operative order only = `PARTIAL_TEXT`.

### Минцифры 29.02.2024 № 147 — primary publication confirmed; six-year lifetime

Official publication index confirms:

- title matches Habr;
- Minjust registration: 01.04.2024 № 77707;
- publication id: `0001202404010010`;
- publication date: 01.04.2024;
- official index benchmark: PDF 272 KB, 5 pages;
- effective date: 01.09.2024.

Official URL: https://publication.pravo.gov.ru/document/0001202404010010

The order expressly operates for six years from entry into force. Working lifecycle is therefore 01.09.2024 through the six-year boundary at 01.09.2030; it is current on 2026-08-31. The current Roskomnadzor mandatory-requirements list also includes this order for telecom supervision, which corroborates operative use but does not replace primary current-status verification.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_INDEX_CONFIRMED = true`
- `BUILT_IN_SUNSET_CONFIRMED = true`
- `CURRENTNESS_CORROBORATED_BY_REGULATOR_REQUIREMENTS_LIST = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Completeness gate: `order + complete approved Requirements`; order without Requirements = `PARTIAL_TEXT`.

### Роскомнадзор 02.02.2023 № 13 — identity and two-appendix completeness model confirmed

Primary publication identity:

- Minjust registration: 31.03.2023 № 72824;
- publication id: `0001202303310014`;
- official publication date: 31.03.2023;
- effective date: 11.04.2023.

Official URL: https://publication.pravo.gov.ru/document/0001202303310014

The act has two integral approved components:

1. Appendix 1 — `Порядок проведения мониторинга информационно-телекоммуникационных сетей, в том числе сети Интернет`;
2. Appendix 2 — `Виды информации и (или) информационных ресурсов, в отношении которых проводится мониторинг`.

Therefore `FULL_TEXT = order + Appendix 1 + Appendix 2`; a copy containing only the monitoring procedure or only the monitored-information list is `PARTIAL_TEXT`.

No later repeal/amendment was confirmed in targeted searches. Direct primary consolidated status remains unclosed.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `TWO_APPENDIX_COMPLETENESS_GATE = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`
- `HABR_IDENTITY_CONFLICT = false`.

### Роскомнадзор 04.09.2023 № 129 — current replacement chain confirmed

Primary publication identity:

- Minjust registration: 07.02.2024 № 77166;
- publication id: `0001202402070025`;
- official publication date: 07.02.2024;
- effective date: 18.02.2024.

Official URL: https://publication.pravo.gov.ru/document/0001202402070025

The order approves the complete interaction procedure for the operator of the prohibited-information register. Clause 2 expressly invalidates/replaces the older Roskomnadzor order 03.08.2017 № 152 and its amendment 05.10.2021 № 209. This establishes a clean replacement edge rather than a simple same-topic coexistence.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `REPLACES_OLD_ORDER_152_2017 = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`
- `HABR_IDENTITY_CONFLICT = false`.

Completeness gate: `order + complete approved interaction procedure`; title/operative clauses only = `PARTIAL_TEXT`.

### Роскомнадзор 19.02.2024 № 25 — two appendices; old № 228/2019 expressly repealed

Primary publication identity:

- Minjust registration: 25.03.2024 № 77628;
- publication id: `0001202403260007`;
- official publication date: 26.03.2024;
- effective date: 06.04.2024.

Official URL: https://publication.pravo.gov.ru/document/0001202403260007

Clause 1 approves two integral appendices:

1. technical conditions for installation of TSPU;
2. requirements to communications networks when TSPU are used.

Clause 2 expressly recognizes Roskomnadzor order 31.07.2019 № 228 (Minjust № 55886) as invalid. Hence `FULL_TEXT = order + Appendix 1 + Appendix 2`; a copy lacking either annex is `PARTIAL_TEXT`.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `TWO_APPENDIX_COMPLETENESS_GATE = true`
- `REPLACES_OLD_ORDER_228_2019 = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`
- `HABR_IDENTITY_CONFLICT = false`.

## New identity collision / amendment-association hazard

Roskomnadzor issued another order numbered № 25 on 27.02.2023 concerning criteria for prohibited-information materials/resources. That is a different legal act from Roskomnadzor № 25 of 19.02.2024 concerning TSPU technical conditions.

A later order № 168 of 08.11.2023 amends the 27.02.2023 № 25; it must not be attached to the 19.02.2024 № 25 lifecycle.

New gate:

`SAME_AUTHORITY + SAME_NUMBER + DIFFERENT_DATE != SAME_ACT`

and specifically:

`RKN_25_2023 + amendment_168_2023 != RKN_25_2024_TSPU`.

This is an identity-association blocker for automated lifecycle extraction, not a conflict in Habr's target identity.

## Gates added or reinforced

1. `NUMBER_DATE_TITLE_IDENTITY != CURRENTNESS != OFFICIAL_STATUS`.
2. `OFFICIAL_PUBLICATION_POINTER != SUCCESSFUL_PRIMARY_FETCH`.
3. `NO_LATER_REPEAL_FOUND != PRIMARY_CONSOLIDATED_CURRENT_STATUS_CONFIRMED`.
4. `ORDER_WITHOUT_ALL_APPROVED_APPENDICES_OR_REQUIREMENTS != FULL_TEXT`.
5. `REGISTRATION_NUMBER_SEARCH_HIT_WITHOUT_LEGAL_CONTEXT = SEARCH_FALSE_POSITIVE`.
6. `SAME_AUTHORITY + SAME_NUMBER + DIFFERENT_DATE != SAME_ACT`.
7. `AMENDMENT_ASSOCIATION_REQUIRES_BASE_ACT_DATE_AND_TITLE_MATCH`.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `GITHUB_SEARCH_FALSE_POSITIVE_GROUP +4`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_IDENTITY_CONFLICT +0`
- `HABR_REPEAL_CONFLICT +0`
- `PRIMARY_INITIAL_PUBLICATION_INDEX_OR_POINTER_CONFIRMED +5`
- `BUILT_IN_SUNSET_CONFIRMED +1`
- `TWO_APPENDIX_COMPLETENESS_GATE +2`
- `REPLACEMENT_EDGE_CONFIRMED +2`
- `SAME_AUTHORITY_SAME_NUMBER_DIFFERENT_DATE_COLLISION +1`
- `PRIMARY_DIRECT_FETCH_BLOCKER +5`

## Next boundary
Continue `Защита связи`, positions 27–31:

1. PP RF 28.08.2025 № 1300;
2. PP RF 29.08.2025 № 1316;
3. PP RF 30.08.2025 № 1333;
4. PP RF 27.10.2025 № 1667;
5. Минцифры 16.12.2025 № 1174.

Positions № 1333/2025 and № 1667/2025 have already appeared earlier in the sweep as replacement acts for old PP №126/2020 and №127/2020. When reached as direct Habr targets they must be handled as `DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED`, with GitHub body search/identity metadata still performed independently rather than skipped.