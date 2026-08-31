# Habr NPA sweep — Stream 1 — 2026-08-31 20:56 MSK

## Scope
Continuation of Habr 432466, section `Защита связи`, positions 15–21:

1. Постановление Правительства РФ от 23.05.2024 № 639.
2. Приказ Мининформсвязи России от 09.01.2008 № 1.
3. Приказ Минкомсвязи России от 27.06.2011 № 160.
4. Приказ Минкомсвязи России от 28.03.2019 № 108.
5. Приказ Минцифры России от 02.03.2022 № 156.
6. Приказ Минцифры России от 12.09.2022 № 659.
7. Совместный приказ Минцифры России № 321 / ФСБ России № 147 от 29.03.2023.

Method remains unchanged: GitHub body discovery is independent from legal-status verification. A GitHub copy is never treated as official merely because it contains the text. `FULL_TEXT`, reliable candidate, mention/reference, digest/index and identity mismatch are separate classes. Identity requires at minimum authority/type + number + date + title/body agreement. Currentness and official status are verified separately against the primary publication chain.

Habr source: https://habr.com/ru/articles/432466/ (version shown by Habr: 28.05.2026).

## GitHub normative-body result

| Target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| PP RF 639/2024 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Mининформсвязи 1/2008 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Минкомсвязи 160/2011 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Минкомсвязи 108/2019 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Минцифры 156/2022 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Минцифры 659/2022 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Минцифры 321 / ФСБ 147 / 2023 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

Exact GitHub searches by number/date/title and distinctive title fragments returned no normative body or reliable candidate for any of the seven targets. No result passed the number/date/title/body gate; therefore no repo/commit/path/size/type metadata is fabricated. No full-body duplicate and no GitHub body-identity conflict were confirmed in this pass.

## Confirmed lifecycle findings / conflicts / blockers

### PP RF 23.05.2024 № 639 — official publication identity confirmed; direct fetch blocked

Habr correctly identifies PP RF 23.05.2024 № 639, approving the `Положение о схеме пропуска трафика через технические средства противодействия угрозам ...`.

Primary publication identity is confirmed by the official publication index:

- official publication date: 24.05.2024;
- publication id: `0001202405240067`;
- official URL: https://publication.pravo.gov.ru/document/0001202405240067.

Direct retrieval of the official publication card timed out in this pass. Roskomnadzor's official acts page also lists PP 639/2024 as an applicable Government act. No later repealing or amending act was confirmed in this pass, but absence of a found repeal is not promoted to direct proof of current consolidated status.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_INDEX_CONFIRMED = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`
- `HABR_IDENTITY_CONFLICT = false`.

Completeness gate: `postanovlenie + complete approved Pоложение`; the operative resolution alone is `PARTIAL_TEXT`.

### Mининформсвязи 09.01.2008 № 1 — current lifetime was extended/limited by a 2024 amendment

A material lifecycle update is confirmed. Минцифры order 26.08.2024 № 726 amended the 2008 order by adding clause 4:

`Установить, что настоящий приказ действует до 1 сентября 2031 года.`

Order № 726:

- date: 26.08.2024;
- Minjust registration: 06.12.2024 № 80489;
- official publication pointer: `0001202412090008`;
- enters into force: 01.09.2025.

The official publication page currently times out on direct retrieval, but the amendment identity, registration and exact amendment text are independently corroborated. On 2026-08-31 the base order № 1 is therefore not a historical-only act: it remains operative with a sunset at 01.09.2031.

Classification:

- `LATEST_AMENDMENT_IDENTITY_CONFIRMED = true`
- `SUNSET_ADDED_BY_LATER_AMENDMENT = 2031-09-01`
- `PRIMARY_LATEST_AMENDMENT_DIRECT_FETCH_BLOCKER = true`
- `GITHUB_OLD_EDITION_RISK = true`.

Any GitHub copy reproducing the pre-01.09.2025 edition without clause 4 is `OLD_EDITION`, even if the original 2008 body is otherwise complete.

Completeness gate: `order + complete Requirements + integral appendix on categorization of communication nodes`; missing the appendix is `PARTIAL_TEXT`.

### Минкомсвязи 27.06.2011 № 160 — current consolidated edition corroborated; secondary metadata conflict

The document is consistently identified as the Rules for switching equipment in mobile radiotelephone networks, Part VI, for territorially distributed UMTS/GSM 900/1800 architecture.

A current legal source shows edition `13.06.2018`; the amendment chain includes at least order № 30 of 01.02.2012 and order № 275 of 13.06.2018. Some older secondary pages still expose edition `24.10.2017`, creating a stale secondary-edition conflict. The more complete current source resolves the working edition to 13.06.2018.

No later repealing/amending act was confirmed in this pass. Direct primary consolidated status was not closed.

Classification:

- `CURRENT_EDITION_CORROBORATED_NONPRIMARY = 2018-06-13`
- `SECONDARY_EDITION_METADATA_CONFLICT = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Completeness gate: `order + complete Rules + all integral appendices`; the current structure includes appendices № 1–11 and an appendix № 10.1. A file without the annex set is `PARTIAL_TEXT`.

### Минкомсвязи 28.03.2019 № 108 — Minjust publication metadata confirmed; stale pre-effective label detected

Minjust publication metadata confirms:

- order date/number: 28.03.2019 № 108;
- title: forms of request/response for confirmation of correspondence of personal data of actual telecom users to subscriber-contract data;
- Minjust registration: 07.06.2019 № 54878;
- official publication: 10.06.2019;
- Minjust publication PDF: approximately 247 KB, 7 pages.

The order approves two integral forms: request (Appendix 1) and response (Appendix 2). A historical secondary page still carries a pre-effective `не вступил в силу` label, while later/current sources show entry into force on 21.06.2019. This is a page-snapshot conflict, not an act-status conflict.

Classification:

- `PRIMARY_MINJUST_PUBLICATION_METADATA_CONFIRMED = true`
- `PRE_EFFECTIVE_ARCHIVE_LABEL_CONFLICT = true`
- gate: `PRE_EFFECTIVE_ARCHIVE_LABEL != CURRENT_STATUS`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Completeness gate: `order + Appendix 1 + Appendix 2 + all integral fields/tables`; one form only is `PARTIAL_TEXT`.

### Минцифры 02.03.2022 № 156 — built-in six-year lifetime confirmed

Identity and registration are confirmed:

- Minjust registration: 01.06.2022 № 68676;
- official publication pointer: `0001202206010016`;
- enters into force: 01.09.2022;
- the order expressly operates for six years.

Working lifecycle range is therefore 01.09.2022 through the six-year boundary in 2028 (secondary consolidated sources express this as 01.09.2022–31.08.2028). The act is current on 2026-08-31.

Direct primary-card retrieval was not closed in this pass, therefore the publication pointer is retained separately from successful primary fetch.

Classification:

- `OFFICIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `BUILT_IN_SUNSET_CONFIRMED = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Completeness gate: `order + complete approved Порядок`; order-only = `PARTIAL_TEXT`.

### Минцифры 12.09.2022 № 659 — six-year lifetime confirmed

Identity and registration are confirmed:

- Minjust registration: 29.11.2022 № 71191;
- enters into force: 01.01.2023;
- the order expressly operates for six years from entry into force.

Thus it is current on 2026-08-31 and reaches its six-year lifecycle boundary at the beginning of 2029. A reliable primary official-publication identifier was not resolved in this pass.

Classification:

- `BUILT_IN_SUNSET_CONFIRMED = true`
- `PRIMARY_INITIAL_PUBLICATION_ID_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Completeness gate: `order + complete approved Requirements`; bare order = `PARTIAL_TEXT`.

### Joint Минцифры № 321 / ФСБ № 147 of 29.03.2023 — current status corroborated; snippet-adjacency trap recorded

Identity is strongly confirmed:

- joint numbers: 321 / 147;
- date: 29.03.2023;
- Minjust registration: 25.05.2023 № 73467;
- official publication date: 25.05.2023;
- publication pointer: `0001202305250029`;
- effective date: 05.06.2023;
- current legal source marks the document `Действует`.

Direct retrieval of the official publication page timed out in this pass. No later repeal/amendment was confirmed.

A search result adjacent to this document contained a six-year sunset phrase belonging to a different preceding Government act. It is not attributable to joint order 321/147. New retrieval gate:

`SEARCH_SNIPPET_NEIGHBOR_TEXT != TARGET_LIFECYCLE`.

Classification:

- `OFFICIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `CURRENTNESS_CORROBORATED_NONPRIMARY = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`
- `SEARCH_SNIPPET_ADJACENCY_TRAP = true`.

Completeness gate: `joint order + complete approved Typical Requirements`; title/operative clause only = `PARTIAL_TEXT`.

## Gates added or reinforced

1. `NUMBER_DATE_TITLE_IDENTITY != CURRENTNESS != OFFICIAL_STATUS`.
2. `OFFICIAL_PUBLICATION_POINTER != SUCCESSFUL_PRIMARY_FETCH`.
3. `OLD_COMPLETE_EDITION_AFTER_AMENDMENT != CURRENT_FULL_TEXT`.
4. `PRE_EFFECTIVE_ARCHIVE_LABEL != CURRENT_STATUS`.
5. `SEARCH_SNIPPET_NEIGHBOR_TEXT != TARGET_LIFECYCLE`.
6. `ORDER_WITHOUT_APPROVED_RULES_FORMS_OR_APPENDICES != FULL_TEXT`.
7. `NO_LATER_REPEAL_FOUND != PRIMARY_CONSOLIDATED_CURRENT_STATUS_CONFIRMED`.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_IDENTITY_CONFLICT +0`
- `HABR_REPEAL_CONFLICT +0`
- `SUNSET_ADDED_BY_LATER_AMENDMENT +1` (Mининформсвязи № 1 / 2008 via Минцифры № 726 / 2024)
- `BUILT_IN_SUNSET_CONFIRMED +2` (№ 156/2022, № 659/2022)
- `PRIMARY_INITIAL_PUBLICATION_INDEX_OR_POINTER_CONFIRMED +3` (PP 639/2024, № 156/2022, joint № 321/147)
- `SECONDARY_EDITION_METADATA_CONFLICT +1` (№ 160/2011)
- `PRE_EFFECTIVE_ARCHIVE_LABEL_CONFLICT +1` (№ 108/2019)
- `SEARCH_SNIPPET_ADJACENCY_TRAP +1` (joint № 321/147)

## Next boundary
Continue `Защита связи` with positions 22–26: Минцифры 01.11.2023 № 936, Минцифры 29.02.2024 № 147, Роскомнадзор 02.02.2023 № 13, Роскомнадзор 04.09.2023 № 129, Роскомнадзор 19.02.2024 № 25. Roskomnadzor and general personal-data/information acts remain priority targets.