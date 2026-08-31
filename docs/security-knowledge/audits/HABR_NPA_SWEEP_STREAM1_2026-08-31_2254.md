# Habr NPA sweep — Stream 1 — 2026-08-31 22:54 MSK

## Scope
Continuation of Habr 432466, section `Защита связи`, positions 27–31:

1. Постановление Правительства РФ от 28.08.2025 № 1300.
2. Постановление Правительства РФ от 29.08.2025 № 1316.
3. Постановление Правительства РФ от 30.08.2025 № 1333.
4. Постановление Правительства РФ от 27.10.2025 № 1667.
5. Приказ Минцифры России от 16.12.2025 № 1174.

Method remains unchanged: GitHub body discovery is independent from legal-status verification. A GitHub copy is never treated as official merely because it contains legal text. `FULL_TEXT`, reliable candidate, mention/reference, digest/index, numeric false positive and identity mismatch remain separate classes. Identity requires at minimum authority/type + number + date + title/body agreement; currentness and official status are separate fields verified against the primary publication chain.

Habr source: https://habr.com/ru/articles/432466/ (version shown by Habr: 28.05.2026).

## GitHub normative-body result

| Target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| ПП РФ 1300/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ПП РФ 1316/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ПП РФ 1333/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ПП РФ 1667/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Минцифры 1174/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

Exact GitHub searches by number/date/title and distinctive title fragments returned no normative body and no reliable candidate for any of the five targets. Broader searches produced only unrelated corpus/training/technical-note hits. Example: `OlSiv/my_notes_leaning@50ba53434f9ece207049c130bfad6b3292e761a8/ib_kurets_kiberbez.txt` surfaced for query terms around № 1300, but inspection showed `1300` only as a Hashcat/SHA2-224 mode number in study notes, not as a legal reference; class `SEARCH_FALSE_POSITIVE / REJECTED`. A generic mesh-network article also surfaced for № 1667 terms and was rejected as unrelated. No repo/commit/path/size/type metadata is promoted from such noise. No full-body duplicate and no GitHub body-identity conflict were confirmed in this pass.

## Confirmed official-publication / lifecycle findings

### ПП РФ 28.08.2025 № 1300 — official publication pointer confirmed; six-year lifetime

Habr number/date/title agree with the legal text found in secondary full-text sources.

Confirmed lifecycle:

- entry into force: `01.09.2025`;
- clause 2 expressly states that the постановление operates for six years;
- therefore it is operative on 2026-08-31 and has a six-year boundary at 01.09.2031.

Official publication pointer resolved to:

- publication id: `0001202508290061`;
- official URL: https://publication.pravo.gov.ru/document/0001202508290061 .

Direct retrieval of the official card timed out in this pass, so the primary pointer is recorded separately from direct retrieval:

- `OFFICIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `BUILT_IN_SUNSET_CONFIRMED = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

Completeness gate: `FULL_TEXT = постановление + complete approved Rules`. Operative clauses without the Rules are `PARTIAL_TEXT`.

### ПП РФ 29.08.2025 № 1316 — primary publication confirmed; six-month connection period is not a sunset

Primary publication index confirms:

- exact title;
- publication id `0001202508290089`;
- official publication date `29.08.2025`;
- official URL: https://publication.pravo.gov.ru/document/0001202508290089 .

The act entered into force on `01.09.2025`.

Clause 2 requires an operator to connect to SMEV within six months from entry into force (with a separate six-month mechanism after a motivated notice where technical capability was absent). This is a compliance/transition deadline, **not** an expiry date of the act. Clause 3 contains the entry date but no six-year sunset for the постановление.

New gate:

`COMPLIANCE_TRANSITION_PERIOD != ACT_SUNSET`.

Completeness gate: `FULL_TEXT = постановление + Rules + Appendix containing the complete list of information provided by the operator`. A copy without the appendix is `PARTIAL_TEXT`.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_INDEX_CONFIRMED = true`
- `EFFECTIVE_DATE_CONFIRMED = 2025-09-01`
- `COMPLIANCE_TRANSITION_PERIOD_NOT_SUNSET = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER = true`.

### ПП РФ 30.08.2025 № 1333 — direct-target duplicate; lifecycle and completeness refined

This act was already reviewed earlier in the sweep as the replacement branch reached from obsolete ПП РФ № 126/2020. Direct Habr-target processing is therefore marked `DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED`, but GitHub body search was still performed and returned no body/candidate.

Confirmed lifecycle/content:

- official publication pointer: `0001202508300019`;
- official URL: https://publication.pravo.gov.ru/document/0001202508300019 ;
- entry into force: `01.09.2025`;
- clause 4: approved Rules operate until `01.09.2031`;
- clause 2 simultaneously amends subparagraph `э` of point 5 of the Regulation on the radio-frequency service approved by PP RF 14.05.2014 № 434.

Therefore a strict full-body copy must preserve both the operative amendment to № 434 and the entire approved Rules. A file containing only the Rules is not a faithful `FULL_TEXT` of the постановление.

Classification:

- `DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED = true`
- `OFFICIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `BUILT_IN_SUNSET_CONFIRMED = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`.

### ПП РФ 27.10.2025 № 1667 — direct-target duplicate; replacement chain and sunset confirmed

This act was already reviewed earlier as the replacement for ПП РФ № 127/2020. Direct Habr-target processing is `DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED`; GitHub body search was nevertheless repeated independently and returned no normative body/candidate.

Primary publication index confirms:

- title: `Об утверждении Правил централизованного управления сетью связи общего пользования`;
- publication id: `0001202511060014`;
- publication date: `06.11.2025`;
- official URL: https://publication.pravo.gov.ru/document/0001202511060014 .

The постановление entered into force `01.03.2026` and operates until `01.03.2032`. Clause 2 expressly invalidates the previous № 127/2020 branch, including PP RF № 2343/2021 and the related amendment position under № 1790/2023.

Completeness gate: `FULL_TEXT = постановление including repeal chain + complete approved Rules`.

Classification:

- `DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED = true`
- `PRIMARY_INITIAL_PUBLICATION_INDEX_CONFIRMED = true`
- `BUILT_IN_SUNSET_CONFIRMED = true`
- `REPLACEMENT_EDGE_CONFIRMED = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`.

### Минцифры 16.12.2025 № 1174 — Habr title conflict; official registered title wins

A material title discrepancy is confirmed.

Habr stores the title ending with wording equivalent to:

`...для обеспечения безопасности Российской Федерации по направлению деятельности федеральной службы безопасности`.

The registered/published title is instead:

`Об утверждении Требований к сетям и средствам связи собственников или иных владельцев технологических сетей связи, имеющих уникальный идентификатор совокупности средств связи и иных технических средств в информационно-телекоммуникационной сети "Интернет", для проведения уполномоченными государственными органами, осуществляющими оперативно-разыскную деятельность или обеспечение безопасности Российской Федерации, в случаях, установленных федеральными законами, мероприятий в целях реализации возложенных на них задач`.

Authority, date and number match, so this is **not** promoted to `DIFFERENT_ACT`; it is a `HABR_TITLE_IDENTITY_CONFLICT`. The official registered title wins for the canonical identity card.

Confirmed publication/status metadata:

- Minjust registration: `22.05.2026 № 86587`;
- official publication id: `0001202605230002`;
- official publication date: `23.05.2026`;
- official publication benchmark: `69 pages`;
- official URL: https://publication.pravo.gov.ru/document/0001202605230002 ;
- entry into force corroborated as `03.06.2026`;
- clause 2 expressly invalidates the former Минкомсвязи order 05.11.2019 № 646 (Minjust № 57223).

The full Requirements contain appendices numbered through `Appendix № 7`; no Appendix № 8 was found in the inspected complete secondary text. Therefore:

`FULL_TEXT = order + entire Requirements + Appendices 1–7`.

The 69-page primary-publication benchmark should be used as a strong completeness signal when a future GitHub candidate appears. A short file containing only the operative order or main body without all appendices is `PARTIAL_TEXT`.

A secondary metadata conflict was also confirmed: an archived Garant page still carries the historical label `документ не вступил в силу`, while other current sources establish entry into force on 03.06.2026. The archival label is therefore `STALE_SECONDARY_PRE_EFFECTIVE_LABEL`, not current lifecycle status.

Classification:

- `HABR_TITLE_IDENTITY_CONFLICT = true`
- `NUMBER_DATE_AUTHORITY_MATCH = true`
- `OFFICIAL_REGISTERED_TITLE_WINS = true`
- `PRIMARY_INITIAL_PUBLICATION_POINTER_CONFIRMED = true`
- `MINJUST_REGISTRATION_CONFIRMED = 86587`
- `EFFECTIVE_DATE_CONFIRMED = 2026-06-03`
- `REPLACEMENT_EDGE_CONFIRMED = true`
- `SEVEN_APPENDIX_COMPLETENESS_GATE = true`
- `STALE_SECONDARY_PRE_EFFECTIVE_LABEL_CONFLICT = true`
- `PRIMARY_DIRECT_FETCH_BLOCKER = true`.

## Gates added or reinforced

1. `NUMBER_DATE_AUTHORITY_MATCH + TITLE_MISMATCH => TITLE_IDENTITY_CONFLICT`, not automatic `DIFFERENT_ACT`.
2. `OFFICIAL_REGISTERED_TITLE_WINS_OVER_HABR_OR_SECONDARY_TITLE`.
3. `COMPLIANCE_TRANSITION_PERIOD != ACT_SUNSET`.
4. `RULES_SUNSET_CAN_DIFFER_FROM_PLAIN_EFFECTIVE_DATE_METADATA`.
5. `OPERATIVE_AMENDMENT + APPROVED_RULES = FULL_TEXT`; Rules alone can still be partial where the постановление changes another act.
6. `ARCHIVED_PRE_EFFECTIVE_STATUS_LABEL != CURRENT_STATUS_AFTER_EFFECTIVE_DATE`.
7. `OFFICIAL_PUBLICATION_POINTER != SUCCESSFUL_PRIMARY_FETCH`.
8. `DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED` does not waive direct GitHub body search.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED +2`
- `PRIMARY_INITIAL_PUBLICATION_INDEX_OR_POINTER_CONFIRMED +5`
- `BUILT_IN_SUNSET_CONFIRMED +3`
- `HABR_TITLE_IDENTITY_CONFLICT +1`
- `REPLACEMENT_EDGE_CONFIRMED +2`
- `COMPLIANCE_TRANSITION_PERIOD_NOT_SUNSET +1`
- `SEVEN_APPENDIX_COMPLETENESS_GATE +1`
- `STALE_SECONDARY_PRE_EFFECTIVE_LABEL_CONFLICT +1`
- `PRIMARY_DIRECT_FETCH_BLOCKER +5`

## Next boundary
Habr section `Защита связи` is complete through position 31. Continue into `Государственные и муниципальные информационные системы (ГИС и МИС)`, with user-priority federal acts first:

1. 59-ФЗ от 02.05.2006;
2. 262-ФЗ от 22.12.2008;
3. 8-ФЗ от 09.02.2009;
4. Основы законодательства РФ о нотариате № 4462-1;
5. 20-ФЗ от 10.01.2003 (ГАС "Выборы");
6. 41-ФЗ от 01.04.2025;
7. 156-ФЗ от 24.06.2025.

After those, continue with Presidential/Government and Roskomnadzor positions in the same section, while preserving the user-priority scope for federal laws, Presidential/Government acts, Roskomnadzor and general information/PDn regulation.