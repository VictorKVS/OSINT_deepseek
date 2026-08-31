# Habr NPA sweep — Stream 1 — 2026-08-31 14:52 MSK

Scope: Habr 432466, section `Информационная безопасность и персонал`, positions 1–7.

Targets:
1. Labor Code of the Russian Federation, Federal Law 197-FZ of 30.12.2001.
2. Federal Law 79-FZ of 27.07.2004 on the state civil service.
3. Government Resolution 399 of 06.05.2016.
4. Ministry of Labour Resolution 37 of 21.08.1998 approving the qualification handbook.
5. Ministry of Education and Science Order 1061 of 12.09.2013.
6. Ministry of Labour Order 462n of 09.07.2021.
7. Ministry of Labour Order 474n of 09.08.2022.

Method:
- GitHub exact/code search by number/date/title and characteristic title phrases.
- A GitHub copy is never treated as an official source automatically.
- `FULL_TEXT` requires the whole operative body and all required appendices/approved rules/professional-standard sections; reference pages, summaries, bibliographies and excerpts are rejected.
- Identity is checked by number/date/title inside a candidate before promotion.
- Currency and official status are resolved separately; when the official publication portal cannot be fetched directly, the blocker remains explicit.

## Batch counters

- targets: 7
- `GITHUB_FULL_TEXT`: 0
- `RELIABLE_GITHUB_CANDIDATE`: 0
- `GITHUB_FULL_TEXT_BLOCKER`: 7
- `NEW_GITHUB_FULL_BODY_DUPLICATE`: 0
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT`: 0
- `MENTION_ONLY_REUSED_SOURCE`: 1 (AxHulk accreditation page hit for 197-FZ; already-known reference-page pattern, rejected)
- `ENACTED_FUTURE_CHANGE_2026-09-01`: at least 4 for Labor Code in this pass (90-FZ, 91-FZ, 108-FZ, 144-FZ)
- `PRIMARY_LATEST_AMENDMENT_POINTER_CORROBORATED`: 2 (52-FZ affecting 79-FZ; 108-FZ affecting Labor Code)
- `PRIMARY_DIRECT_FETCH_BLOCKER`: 2 (publication.pravo.gov.ru timed out for the verified publication pointers checked directly)
- `SCHEDULED_REPLACEMENT_DATE_POSTPONED`: 1 (Order 1061 remains until 01.09.2027 because transition under Order 89 was postponed by Order 201/2026)
- `TIME_LIMITED_CURRENT_PROFSTANDARD`: 2 (462n through 01.03.2028; 474n through 01.03.2029)

## Position 1 — Labor Code, 197-FZ of 30.12.2001

Habr identity:
- Habr lists the Labor Code dated 30.12.2001 No. 197-FZ; identity matches the legal corpus.

GitHub:
- exact title/date/number search: no full body.
- broader number/date search surfaced `AxHulk/osp-kavkaz-ing`, commit `b902d3e57875c53d2c284e3e257fefc7f8d5e9e9`, path `src/pages/Accreditation.tsx`.
- fetched content is a React/TSX accreditation/reference page, not the Labor Code.
- classification: `MENTION_ONLY / REFERENCE_PAGE / REJECTED_AS_NORMATIVE_BODY`.
- normalized candidate row remains `repo=null; commit=null; path=null; size=null; type=null` because the surfaced file is rejected, not a candidate normative body.

Temporal state:
- current consolidated secondary sources show the operative Code separately from enacted changes scheduled for 01.09.2026.
- confirmed in this pass as directly amending the Labor Code and entering into force on 01.09.2026: Federal Laws 90-FZ of 09.04.2026, 91-FZ of 09.04.2026, 108-FZ of 25.04.2026, 144-FZ of 25.05.2026.
- publication pointer for 108-FZ is corroborated as `0001202604250007`; direct fetch of that official publication page timed out in this run.
- therefore store at least `CURRENT_EFFECTIVE_BODY_2026-08-31` separately from `ENACTED_FUTURE_BODY_2026-09-01`.
- do not treat a prepared 01.09.2026 consolidated text as already effective on 31.08.2026.

Sources checked:
- Habr: https://habr.com/ru/articles/432466/
- Federal Law 90-FZ text/status: https://pravo.ppt.ru/fz/90-fz-333373
- Federal Law 91-FZ official prosecutor explanation: https://epp.genproc.gov.ru/ru/proc_44/activity/legal-education/explain/e8501343/
- Federal Law 108-FZ publication pointer: https://publication.pravo.gov.ru/document/0001202604250007
- Federal Law 144-FZ text/status: https://pravo.ppt.ru/fz/144-fz-338255

## Position 2 — Federal Law 79-FZ of 27.07.2004

GitHub:
- exact number/date/title search: no usable file.
- `repo=null; commit=null; path=null; size=null; type=null`.
- status: `GITHUB_FULL_TEXT_BLOCKER`.

Currency/lifecycle:
- current consolidated legal sources show edition dated 08.03.2026.
- the latest identified amending act in this pass is Federal Law 52-FZ of 08.03.2026; its article 3 changes part 5 of article 15 of 79-FZ.
- 52-FZ entered into force 07.06.2026.
- official publication pointer is corroborated as `0001202603080008`; direct official-page fetch timed out in this run.
- status: `CURRENT_STATUS_CORROBORATED_NONPRIMARY / LATEST_AMENDMENT_IDENTITY_CONFIRMED / PRIMARY_DIRECT_FETCH_BLOCKER`.

Sources checked:
- current text: https://www.consultant.ru/document/cons_doc_LAW_48601/
- 52-FZ publication pointer: https://publication.pravo.gov.ru/document/0001202603080008

## Position 3 — Government Resolution 399 of 06.05.2016

GitHub:
- exact number/date/title search: no usable file.
- `repo=null; commit=null; path=null; size=null; type=null`.
- status: `GITHUB_FULL_TEXT_BLOCKER`.

Currency/completeness:
- consolidated legal source shows edition of 11.07.2018, effective from 21.07.2018, amended by Government Resolution 808 of 11.07.2018.
- no later repeal/amendment was confirmed in this pass.
- `FULL_TEXT` requires the Resolution plus the complete approved Rules; the two-point resolution body alone is `PARTIAL_TEXT`.
- primary consolidated current-state card was not resolved in this run: `PRIMARY_CURRENT_STATUS_BLOCKER`.

Source checked:
- https://normativ.kontur.ru/document/1/316975-postanovlenie-pravitelstva-rf-ot-06-05-2016-n-399

## Position 4 — Ministry of Labour Resolution 37 of 21.08.1998

GitHub:
- exact title/date/number search: no usable file.
- `repo=null; commit=null; path=null; size=null; type=null`.
- status: `GITHUB_FULL_TEXT_BLOCKER`.

Currency/completeness:
- current institutional/legal references found in this pass cite edition dated 27.03.2018.
- no later formal repeal was confirmed.
- because this act approves a qualification handbook, `FULL_TEXT` requires the approving resolution plus the complete handbook body relevant to that edition; a single job-description excerpt is not full text.
- current primary status was not resolved: `PRIMARY_CURRENT_STATUS_BLOCKER`.

Corroborating source:
- https://idpo.magtu.ru/index.php/institut/dokumenty/normativnye-dokumenty

## Position 5 — Ministry of Education and Science Order 1061 of 12.09.2013

GitHub:
- exact number/date/title search: no usable file.
- `repo=null; commit=null; path=null; size=null; type=null`.
- status: `GITHUB_FULL_TEXT_BLOCKER`.

New lifecycle finding:
- Order 1061 is not to be marked repealed on 01.09.2026.
- Ministry of Science and Higher Education Order 201 of 27.03.2026, registered by Ministry of Justice 27.04.2026 No. 86219 and effective 09.05.2026, amended the transition orders and moved the entry into force of Order 89 to 01.09.2027.
- current consolidated source consequently states that Order 1061 loses force from 01.09.2027, not 01.09.2026.
- Habr's continued listing of 1061 on 28.05.2026 is therefore not a repeal conflict.
- older secondary pages retaining 2024/2026 transition dates are stale: `SECONDARY_LIFECYCLE_CONFLICT / LATEST_AMENDMENT_WINS`.
- `FULL_TEXT` requires Order 1061 plus all current lists/appendices, including the Information Security specialty block; an isolated `10.00.00` table is `PARTIAL_TEXT`.

Sources checked:
- Order 201 status/text: https://normativ.kontur.ru/document/1/505874-prikaz-minobrnauki-rf-ot-27-03-2026-n-201
- current 1061 transition note: https://www.consultant.ru/document/cons_doc_LAW_153430/3614ddf10908f002a19d44453bea4a184ade5367/

## Position 6 — Ministry of Labour Order 462n of 09.07.2021

GitHub:
- exact and broad title/number search: no usable file.
- `repo=null; commit=null; path=null; size=null; type=null`.
- status: `GITHUB_FULL_TEXT_BLOCKER`.

Current lifecycle/completeness:
- Ministry registration No. 64502 is consistent with Habr.
- the order entered into force 01.03.2022 and is time-limited through 01.03.2028.
- no later repeal/amendment was confirmed in this pass.
- `FULL_TEXT` requires the order plus the entire professional standard and all functional/qualification tables; order body alone is `PARTIAL_TEXT`.
- primary current-status direct card not resolved: `TIME_LIMITED_CURRENT_ACT / PRIMARY_CURRENT_STATUS_BLOCKER`.

Source checked:
- https://www.consultant.ru/document/cons_doc_LAW_392193/

## Position 7 — Ministry of Labour Order 474n of 09.08.2022

GitHub:
- exact number/date/title search: no usable file.
- `repo=null; commit=null; path=null; size=null; type=null`.
- status: `GITHUB_FULL_TEXT_BLOCKER`.

Current lifecycle/completeness:
- Ministry registration No. 70015 is consistent with Habr.
- the order applies from 01.03.2023 and is time-limited through 01.03.2029.
- no later repeal/amendment was confirmed in this pass.
- `FULL_TEXT` requires the order plus the whole professional standard, not only the approving paragraph or selected labour functions.
- primary current-status direct card not resolved: `TIME_LIMITED_CURRENT_ACT / PRIMARY_CURRENT_STATUS_BLOCKER`.

Source checked:
- https://www.consultant.ru/document/cons_doc_LAW_426572/

## New gates added

1. `PREPARED_NEXT_DAY_CONSOLIDATION != CURRENT_EFFECTIVE_BODY`.
2. `MULTIPLE_ENACTED_AMENDMENTS_SAME_EFFECTIVE_DATE => STORE_SEPARATE_FUTURE_LAYER`.
3. `SCHEDULED_REPLACEMENT_DATE_CAN_BE_POSTPONED_BY_LATER_ACT`.
4. `STALE_SECONDARY_REPEAL_DATE != CURRENT_LIFECYCLE_STATUS`.
5. `PROFESSIONAL_STANDARD_ORDER_WITHOUT_FULL_APPROVED_STANDARD != FULL_TEXT`.
6. `QUALIFICATION_HANDBOOK_EXCERPT != FULL_APPROVED_HANDBOOK`.
7. `OFFICIAL_PUBLICATION_POINTER_CORROBORATED + DIRECT_TIMEOUT != PRIMARY_DIRECT_FETCH_VERIFIED`.
8. `REFERENCE_WEBAPP_SOURCE_HIT != NORMATIVE_BODY_CANDIDATE`.

## Next boundary

Continue `Информационная безопасность и персонал`, positions 8–14: Ministry of Labour Orders 525n/2022, 533n/2022, 536n/2022, 609n/2022, 739n/2022, 586n/2023 and Ministry of Digital Development Order 27/2026. In parallel, keep prioritizing user-scope federal laws, presidential/government acts, Roskomnadzor and general PDn/information acts; do not rescan closed targets unless a new GitHub body, amendment/repeal, official publication or identity conflict appears.
