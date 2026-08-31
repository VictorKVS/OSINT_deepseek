# Habr NPA sweep — Stream 1 — 2026-08-31 16:09 MSK

Scope: Habr 432466, section `Информационная безопасность и персонал`, positions 8–14.

Targets:
1. Ministry of Labour Order 525n of 14.09.2022.
2. Ministry of Labour Order 533n of 14.09.2022.
3. Ministry of Labour Order 536n of 14.09.2022.
4. Ministry of Labour Order 609n of 03.10.2022.
5. Ministry of Labour Order 739n of 28.11.2022.
6. Ministry of Labour Order 586n of 13.07.2023.
7. Ministry of Digital Development Order 27 of 22.01.2026.

Method:
- GitHub code search by exact number/date/title and characteristic title phrases.
- GitHub copy is never treated as an official source automatically.
- `FULL_TEXT` requires the operative order plus the entire approved professional standard / all approved lists and appendices.
- Reference pages, study notes, bibliographies, summaries and isolated labour-function tables are rejected.
- Identity is checked by number/date/title in the surfaced file before promotion.
- Currency / official status are resolved separately from official regulator and official-publication sources.

## Batch counters

- targets: 7
- `GITHUB_FULL_TEXT`: 0
- `RELIABLE_GITHUB_CANDIDATE`: 0
- `GITHUB_FULL_TEXT_BLOCKER`: 7
- `NEW_GITHUB_FULL_BODY_DUPLICATE`: 0
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT`: 0
- `NEW_GITHUB_MENTION_ONLY_SOURCE`: 1
- `MENTION_ONLY_TARGET_HITS_IN_NEW_SOURCE`: 3 (525n, 536n, 739n)
- `TIME_LIMITED_CURRENT_PROFSTANDARD`: 6
- `PRIMARY_REGULATOR_FULL_STANDARD_PACKAGE_CONFIRMED`: 6
- `PRIMARY_OFFICIAL_PUBLICATION_CONFIRMED`: 2 (739n, MinDigital 27)
- `HABR_IDENTITY_CONFLICT`: 0
- `HABR_REPEAL_CONFLICT`: 0

## New GitHub finding — study notes mentioning 525n / 536n / 739n

Repository/candidate metadata:
- repo: `IKarasev/Study`
- commit: `46d89cc6ac468698dcc56c9706f744749ed84b8d`
- path: `info_sec_org_measures/02_Методологические_подходы_к_защите_информации.md`
- blob SHA: `525e9cdde660b16c0f1de3ed820ca747388b9f16`
- size: `29141` bytes
- type: `file / Markdown`

Content check:
- the file is a study/lecture note on organisational information-security measures;
- it contains bibliographic links and short explanatory discussion of professional standards 525n, 536n and 739n;
- it does not reproduce the approved professional-standard bodies/tables;
- classification: `MENTION_ONLY / STUDY_NOTES / REJECTED_AS_NORMATIVE_BODY` for all three target hits;
- this is one source mentioning three acts, not three normative-body candidates and not a duplicate full-text corpus.

Source:
- https://github.com/IKarasev/Study/blob/46d89cc6ac468698dcc56c9706f744749ed84b8d/info_sec_org_measures/02_Методологические_подходы_к_защите_информации.md

## Position 8 — Ministry of Labour Order 525n of 14.09.2022

Identity:
- Habr number/date/title and Ministry of Justice registration No. 70543 match the official Ministry of Labour page.

GitHub:
- surfaced only the `IKarasev/Study` study-note file above.
- classification: `MENTION_ONLY`; no normative-body candidate.
- normalized normative candidate remains `repo=null; commit=null; path=null; size=null; type=null`.

Primary regulator lifecycle/completeness:
- Ministry of Labour states entry into force: 01.03.2023.
- fixed validity: through 01.03.2029.
- Order 525n repealed the previous standard approved by Order 522n/2016.
- official Ministry page exposes the approved professional-standard attachment as DOCX about 120.46 KB, separately from the small order document.
- therefore a copy containing only the approving order is `PARTIAL_TEXT`; `FULL_TEXT` requires the complete approved professional-standard attachment.

Source:
- https://mintrud.gov.ru/docs/mintrud/orders/2446

## Position 9 — Ministry of Labour Order 533n of 14.09.2022

Identity:
- Habr number/date/title and registration No. 70515 match Ministry of Labour.

GitHub:
- no usable hit.
- `repo=null; commit=null; path=null; size=null; type=null`.

Primary regulator lifecycle/completeness:
- effective from 01.03.2023; valid through 01.03.2029.
- repealed the previous standard under Order 598n/2016.
- Ministry of Labour exposes the approved professional-standard attachment as DOCX about 134.81 KB.
- order body without this attachment is `PARTIAL_TEXT`.

Source:
- https://mintrud.gov.ru/docs/mintrud/orders/2445

## Position 10 — Ministry of Labour Order 536n of 14.09.2022

Identity:
- Habr number/date/title and registration No. 70596 match Ministry of Labour.

GitHub:
- same `IKarasev/Study` study-note hit as for 525n.
- classification: `MENTION_ONLY`; no normative-body candidate.
- normalized normative candidate remains `repo=null; commit=null; path=null; size=null; type=null`.

Primary regulator lifecycle/completeness:
- effective from 01.03.2023; valid through 01.03.2029.
- repealed the previous standard under Order 608n/2016.
- Ministry of Labour exposes the approved professional-standard attachment as DOCX about 127.68 KB.
- order body alone is `PARTIAL_TEXT`.

Sources:
- https://mintrud.gov.ru/docs/mintrud/orders/2471
- corroborating official-publication record metadata is also reproduced by Rossiyskaya Gazeta.

## Position 11 — Ministry of Labour Order 609n of 03.10.2022

Identity:
- Habr number/date/title and registration No. 70769 match Ministry of Labour.

GitHub:
- no usable hit.
- `repo=null; commit=null; path=null; size=null; type=null`.

Primary regulator lifecycle/completeness:
- effective from 01.03.2023; valid through 01.03.2029.
- explicitly repealed the prior technical-writer standard under Order 612n/2014 and the related amendment item in Order 727n/2016.
- Ministry page exposes the professional-standard attachment as DOCX about 236.33 KB.
- `FULL_TEXT` requires the entire standard, not only the order body or an educational-program citation.

Source:
- https://mintrud.gov.ru/docs/mintrud/orders/2477

## Position 12 — Ministry of Labour Order 739n of 28.11.2022

Identity/publication:
- Habr number/date/title and registration No. 71784 match both Ministry of Labour and the official publication portal.
- official publication number: `0001202212230020`.
- publication date: 23.12.2022.

GitHub:
- same `IKarasev/Study` study-note file contains a bibliographic mention/link.
- classification: `MENTION_ONLY`; no normative-body candidate.
- normalized normative candidate remains `repo=null; commit=null; path=null; size=null; type=null`.

Primary lifecycle/completeness:
- effective from 01.09.2023; valid through 01.09.2029.
- Ministry page exposes the approved professional-standard attachment as DOCX about 167.61 KB.
- approving order without all professional-standard tables/functions is `PARTIAL_TEXT`.

Sources:
- https://publication.pravo.gov.ru/Document/View/0001202212230020
- https://mintrud.gov.ru/docs/mintrud/orders/2550

## Position 13 — Ministry of Labour Order 586n of 13.07.2023

Identity:
- Habr number/date/title and registration No. 74817 match Ministry of Labour.

GitHub:
- no usable hit.
- `repo=null; commit=null; path=null; size=null; type=null`.

Primary regulator lifecycle/completeness:
- effective from 01.09.2024; valid through 01.09.2030.
- explicitly repealed the former standard under Order 896n/2014 and the related amendment item in Order 727n/2016.
- Ministry page exposes a much larger approved professional-standard attachment, DOCX about 786.85 KB.
- this size/package structure is a useful completeness benchmark: a small file containing only the order or a few labour functions is not `FULL_TEXT`.

Source:
- https://mintrud.gov.ru/docs/mintrud/orders/2723

## Position 14 — Ministry of Digital Development Order 27 of 22.01.2026

Identity/publication:
- official publication portal confirms exact title/date/number.
- Ministry of Justice registration: No. 85666 on 20.03.2026.
- official publication number: `0001202603200024`.
- official publication date: 20.03.2026.
- official PDF: about 1036 KB, 18 pages.

GitHub:
- no usable hit.
- `repo=null; commit=null; path=null; size=null; type=null`.

Completeness/current status:
- the order approves three distinct lists: professions of secondary vocational education, specialties of secondary vocational education, and higher-education specialties/directions.
- secondary legal publication states entry into force from 01.04.2026; no later repeal/amendment was confirmed in this pass.
- `FULL_TEXT` therefore requires the order plus all three appendices/lists; a file containing only the IT-security rows (`10.00.00`) or only one educational level is `PARTIAL_TEXT`.
- Habr identity is correct; no stale-title or repeal conflict found.

Sources:
- https://publication.pravo.gov.ru/documents/block/foiv290
- https://pravo.ppt.ru/prikaz/mincifry-rossii/n-27-325779

## New gates added

1. `ONE_GITHUB_STUDY_NOTE_MENTIONING_MULTIPLE_ACTS != MULTIPLE_NORMATIVE_BODY_CANDIDATES`.
2. `OFFICIAL_ORDER_BODY + SEPARATE_APPROVED_PROFSTANDARD_ATTACHMENT => BOTH_REQUIRED_FOR_FULL_TEXT`.
3. `PROFSTANDARD_EXPLICIT_SUNSET_DATE => STORE_VALID_TO_AND_DO_NOT_INFER_INDEFINITE_FORCE`.
4. `SMALL_ORDER_FILE_WITHOUT_LARGE_APPROVED_STANDARD_ATTACHMENT != FULL_TEXT`.
5. `ORDER_APPROVING_THREE_LISTS_REQUIRES_ALL_THREE_APPENDICES_FOR_FULL_TEXT`.
6. `OFFICIAL_REGULATOR_HOSTING != GITHUB_OFFICIALITY`; GitHub copies remain derivative even when byte-identical.

## Next boundary

Continue after `Информационная безопасность и персонал`: Habr section `Судебные тяжбы, компьютерная криминалистика`, positions 1–6 (144-FZ, Criminal Procedure Code 174-FZ, Arbitration Procedure Code 95-FZ, Civil Procedure Code 138-FZ, Administrative Procedure Code 21-FZ, FSB STO.FSB.KK 1-2018), while continuing to prioritize the user-scope federal laws, presidential/government acts, Roskomnadzor and general PDn/information acts. Do not rescan closed targets unless a new GitHub body, amendment/repeal, official publication or identity conflict appears.
