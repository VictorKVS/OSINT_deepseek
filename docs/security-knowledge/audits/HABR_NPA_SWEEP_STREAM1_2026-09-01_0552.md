# Habr NPA Sweep — Stream 1 — 2026-09-01 05:52 MSK

## Scope
Systematic pass over Habr article 432466, section **«Государственные и муниципальные информационные системы (ГИС и МИС)»**, positions **41–47**:

1. Приказ Минкомсвязи РФ от 25.08.2009 №104.
2. Приказ Минкомсвязи России от 31.05.2013 №127.
3. Приказ Минкомсвязи России от 27.06.2013 №149.
4. Приказ Минкомсвязи России от 22.08.2013 №220.
5. Приказ Минкомсвязи России от 03.05.2014 №120.
6. Приказ Минкомсвязи России от 07.12.2015 №514.
7. Приказ Минкомсвязи России от 11.02.2016 №44.

Method: GitHub body/candidate search is independent from official status verification. A GitHub copy is never promoted to an official source solely because it exists in GitHub.

## GitHub body search

| Target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| №104/2009 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №127/2013 | `ispras/dedoc` | `40dde1bc2e46b1b00b7058080c1228615b983424` | `tests/data/txt/pr_17.txt` | UNRESOLVED_CONNECTOR_METADATA | TXT | MENTION_ONLY / OTHER_NPA_FULL_TEXT / REJECTED_AS_NORMATIVE_BODY |
| №149/2013 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №220/2013 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №120/2014 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №514/2015 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №44/2016 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

### Rejected GitHub hit — №127/2013
`ispras/dedoc/tests/data/txt/pr_17.txt` is a full text copy of **ФСТЭК России №17 от 11.02.2013**, not the target Mincomsvyaz order. It only references Mincomsvyaz №127 and registration №30318. Blob SHA: `7a45c2c47855e75f9151af0eecb478a833e4e11d`. Identity gate therefore fails for the target body.

Gate: `REFERENCE_INSIDE_OTHER_NPA != TARGET_BODY`.

## Official/currentness review

### №127/2013 — repealed
Minцифры приказ №888 от 17.10.2024, registered by Minjust 12.11.2024 №80122, expressly recognizes №127/2013 and its amendment №266/2016 as invalid. Clause 2 sets entry into force on **2025-01-01**.

Status:
- `HABR_REPEALED_ACT_CONFLICT`
- `REPEAL_EFFECTIVE_2025-01-01`
- `PRIMARY_REPEAL_PUBLICATION_POINTER_BLOCKER` — exact official publication.pravo.gov.ru document ID was not reliably resolved in this pass.

### №44/2016 — repealed and functionally replaced
Minцифры приказ №15 от 16.01.2024, registered 14.05.2024 №78142, approves new Rules for placement of information in the federal GIS for informatization coordination and expressly repeals №44/2016. It entered into force **2024-05-26**. Official publication number is corroborated as `0001202405150020` (published 15.05.2024).

Status:
- `HABR_REPEALED_ACT_CONFLICT`
- `REPEAL_EFFECTIVE_2024-05-26`
- `FUNCTIONAL_REPLACEMENT_CONFIRMED=ORDER_15_2024`
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED`

### №120/2014 — current body changed on 2026-09-01
Minцифры приказ №79 от 16.02.2026 (Minjust registration 20.04.2026 №86127) amends №120/2014. Clause 2 sets its entry into force on **2026-09-01**; its own term is through **2027-09-01**. Official publication pointer previously resolved/corroborated as `0001202604210025`; direct primary fetch remained unstable.

Status:
- `CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01`
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED`
- `PRIMARY_DIRECT_FETCH_BLOCKER`

Important gate: the sunset stated for amendment №79 must not automatically be attributed to the base order №120 without independent confirmation.

### №220/2013 — non-applicable, formal repeal not yet established
Current legal card marks №220/2013 (ed. 27.03.2014) as **«Документ не применяется»**. The order was tied to the former federal GIS accounting regime under PP RF №644/2012; that government act was previously confirmed repealed effective 2025-01-01 by PP RF №900/2024. This pass did not establish a primary-source act expressly repealing №220 itself.

Status:
- `HABR_NONAPPLICABLE_DOCUMENT_CONFLICT`
- `FORMAL_REPEAL_NOT_CONFIRMED`
- `PRIMARY_NONAPPLICATION_BASIS_BLOCKER`

Gate: `NONAPPLICABLE != FORMALLY_REPEALED`.

### №104/2009, №149/2013, №514/2015
No new repeal/amendment conflict was confirmed in this pass. Absence of a found repeal is not sufficient proof of current official status.

Status for each:
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`

## Full-text completeness gates

- №104/2009: order + complete approved Requirements.
- №127/2013: historical order + complete methodological guidelines; current-use copy must also reflect repeal status.
- №149/2013: order + complete Requirements.
- №220/2013: order + complete methodological recommendations; current-use copy must carry non-applicable status.
- №120/2014: order + complete Requirements + effective amendment layer as of 2026-09-01.
- №514/2015: order + complete Procedure + act form.
- №44/2016: historical order + complete Rules; current-use copy must carry repeal/replacement status.

## Counters — new in this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `GITHUB_MENTION_ONLY_REJECTED +1`
- `HABR_REPEALED_ACT_CONFLICT +2`
- `HABR_NONAPPLICABLE_DOCUMENT_CONFLICT +1`
- `CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01 +1`
- `PRIMARY_REPEAL_PUBLICATION_POINTER_BLOCKER +1`
- `PRIMARY_DIRECT_FETCH_BLOCKER +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## New/confirmed gates

- `FULL_TEXT_BUT_REPEALED != CURRENT_FULL_TEXT`
- `REFERENCE_INSIDE_OTHER_NPA != TARGET_BODY`
- `NONAPPLICABLE != FORMALLY_REPEALED`
- `NO_REPEAL_FOUND != PRIMARY_CURRENT_STATUS_CONFIRMED`
- `AMENDMENT_EFFECTIVE_TODAY => YESTERDAY_FULL_TEXT_CAN_BE_STALE`

## Sources checked

- Habr 432466, version shown 28.05.2026: https://habr.com/ru/articles/432466/
- Official legal publication portal for primary publication/currentness pointers: https://publication.pravo.gov.ru/
- Secondary legal cards used only as corroboration/status leads: ConsultantPlus, Garant.
- GitHub candidate/mention search through repository code search; candidate identity checked inside retrievable text before classification.

## Next boundary
Habr positions **48–55** in the same GIS/MIS block begin with:
- Минцифры №1308 от 06.12.2021;
- Минцифры №1312 от 07.12.2021;
- Постановление ЦИК №86/715-8 от 08.06.2022;
- Минэкономразвития №624 от 15.11.2022;
- совместный Минцифры №611 / ФСО №96 от 12.07.2024;
- Минцифры №677 от 31.07.2024;
- письмо Минцифры №П25-305029 от 17.09.2024;
- Минцифры №1106 от 02.12.2025.

For Stream 1 user priority, federal/Minцифры general acts continue first; non-priority agency/specialized items remain separately classifiable rather than silently merged.