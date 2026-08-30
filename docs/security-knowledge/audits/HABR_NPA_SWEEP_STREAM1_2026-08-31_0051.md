# Habr NPA sweep — Stream 1 — 2026-08-31 00:51 MSK

Scope: Habr 432466, `Идентификация и аутентификация`, positions 22–26. Processed: PP RF No. 552 (06.04.2023), No. 585 (11.04.2023), No. 670 (28.04.2023), No. 810 (22.05.2023), No. 815 (25.05.2023).

## Counters

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +5
- NEW_GITHUB_DUPLICATE: +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT: +0
- DUPLICATE_TARGET_ENTRY_ALREADY_SEEN_IN_OTHER_LIFECYCLE_ROLE: +2 (`585`, `810`)
- PRIMARY_INITIAL_PUBLICATION_NEWLY_CONFIRMED: +3 (`552`, `670`, `815`)
- PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED: +1 (`585` via PP No. 920/2025)
- CURRENT_EDITION_CORROBORATED: +1 (`585`, ed. 18.06.2025)
- EXPLICIT_VALIDITY_WINDOW_CORROBORATED: +3 (`670`, `810`, `815`)
- PRIMARY_GOVERNMENT_CURRENT_TEXT_FOUND: +1 (`810`)
- PRIMARY_CURRENT_STATUS_BLOCKER: +4 (`552`, `585`, `670`, `815` — no directly resolved primary consolidated current card in this pass)
- QUEUE_METADATA_CORRECTION: +1 (`815`: 25.05.2023, not 23.05.2023)
- CONSOLIDATOR_EDITION_SNAPSHOT_TRAP: +1 (`585`)
- NEW_HABR_REPEALED_OR_STALE_TITLE_CONFLICT: +0

## GitHub search result

GitHub Code Search / connected GitHub search plus public-web GitHub-index queries were run for all five targets using number/date/title terms. No indexed target-body file or reliable candidate was returned.

For every target:

`repo=null; commit=null; path=null; size=null; type=null; classification=GITHUB_FULL_TEXT_BLOCKER`.

No GitHub copy was treated as official. No reference-only artifact, summary, implementation, corpus index, downloader, or unrelated numeric hit was promoted to `FULL_TEXT`.

## Confirmed findings

### PP RF 06.04.2023 No. 552

- Habr identity is correct: 06.04.2023 No. 552, rules for considering creation of a regional EBS segment, its operation and exclusion.
- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication is confirmed by the Official Internet Portal of Legal Information: publication No. `0001202304070043`, publication date 07.04.2023.
- Direct opening of the publication card timed out during this pass, so the identity is grounded in the primary portal search record rather than promoted to a successful direct-card fetch.
- No later amendment/repeal was confirmed in the targeted pass, but a directly resolved primary current consolidated card was not obtained. Therefore do not infer `PRIMARY_CURRENT_STATUS_VERIFIED` from absence of amendments.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / PRIMARY_CURRENT_STATUS_BLOCKER`.

Primary source:
- https://publication.pravo.gov.ru/document/0001202304070043

### PP RF 11.04.2023 No. 585

- This act was already encountered earlier as the replacement of PP RF No. 1729; do not count that lifecycle conclusion again.
- GitHub: no full text/candidate; all file metadata fields null.
- New evidence: the act has a later amendment. PP RF 18.06.2025 No. 920 directly amends PP RF 11.04.2023 No. 585.
- The amendment is confirmed by the primary Official Internet Portal of Legal Information: publication No. `0001202506190020`, published 19.06.2025, 4 pages, PDF about 743 KB.
- Current consolidated legal text is corroborated as edition 18.06.2025. The 2025 amendment added/changed, among other things, Section VII with the key performance indicator for federal state control; the legal-system text attributes this section to PP No. 920/2025.
- Important snapshot trap: an old consolidated snapshot of the original 11.04.2023 edition can be marked `Не действует`; this must not be interpreted as repeal of the act itself. The current amended act is represented separately as edition 18.06.2025.
- Classification: `DUPLICATE_TARGET_ENTRY / PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED / CURRENT_EDITION_CORROBORATED_2025-06-18 / CONSOLIDATOR_EDITION_SNAPSHOT_TRAP / GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- Primary amendment publication: https://publication.pravo.gov.ru/document/0001202506190020
- Current consolidated cross-check: https://www.consultant.ru/document/cons_doc_LAW_444421/

### PP RF 28.04.2023 No. 670

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication is confirmed: publication No. `0001202305030014`, published 03.05.2023.
- Consolidated body confirms entry into force 01.06.2023 and an explicit validity limit until 01.06.2029.
- `FULL_TEXT` requires not only the short resolution but all three approved components: (1) requirements for state bodies/Bank of Russia, (2) requirements for organizations participating in authentication, and (3) the Rules for accreditation. Missing any approved component is `PARTIAL_TEXT`.
- A directly resolved primary current consolidated card was not obtained; current-state/validity is therefore corroborated by a current legal system while primary origin is verified separately.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / EXPLICIT_VALIDITY_WINDOW_TO_2029-06-01 / FULLTEXT_REQUIRES_THREE_APPROVED_COMPONENTS / PRIMARY_CURRENT_STATUS_BLOCKER / GITHUB_FULL_TEXT_BLOCKER`.

Primary source:
- https://publication.pravo.gov.ru/Document/View/0001202305030014

### PP RF 22.05.2023 No. 810

- This is a duplicate target already seen as the replacement act for PP RF No. 1799. Do not count the repeal/replacement relation again.
- GitHub: no full text/candidate; all file metadata fields null.
- Primary publication No. `0001202305220032` (22.05.2023) was already recorded in the earlier lifecycle pass.
- New systematic target check resolves a current Government-hosted page for No. 810. Current legal systems corroborate that the act entered into force 01.06.2023 and is limited to 01.06.2029.
- `FULL_TEXT` requires the resolution plus the complete approved accreditation Rules; a reference to accreditation criteria is not sufficient.
- Classification: `DUPLICATE_TARGET_ENTRY / PRIMARY_GOVERNMENT_CURRENT_TEXT_FOUND / EXPLICIT_VALIDITY_WINDOW_TO_2029-06-01 / GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- Primary publication: https://publication.pravo.gov.ru/document/0001202305220032
- Current Government page: https://government.ru/docs/all/147701/

### PP RF 25.05.2023 No. 815

- Queue metadata correction: the correct date is **25.05.2023**, not 23.05.2023. Habr and the primary publication record agree on 25 May.
- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication is confirmed: publication No. `0001202305260020`, published 26.05.2023.
- Current legal text corroborates entry into force 01.06.2023 and validity until 01.06.2029.
- `FULL_TEXT` requires the resolution plus both approved lists: (1) cases where authentication using the organizational system is not permitted, and (2) cases where consent signed with a simple electronic signature may be used. A file containing only one list is `PARTIAL_TEXT`.
- A directly resolved primary consolidated current card was not obtained, so current-status/expiry remains corroborated rather than promoted to `PRIMARY_CURRENT_STATUS_VERIFIED`.
- Classification: `QUEUE_METADATA_CORRECTION / PRIMARY_INITIAL_PUBLICATION_CONFIRMED / EXPLICIT_VALIDITY_WINDOW_TO_2029-06-01 / FULLTEXT_REQUIRES_BOTH_APPROVED_LISTS / PRIMARY_CURRENT_STATUS_BLOCKER / GITHUB_FULL_TEXT_BLOCKER`.

Primary source:
- https://publication.pravo.gov.ru/document/0001202305260020

## New regression gates

1. `OLD_CONSOLIDATED_EDITION_MARKED_NOT_ACTIVE != ACT_REPEALED` — PP No. 585 is a fixture: an obsolete 2023 edition snapshot may be marked non-current while the act continues in the 18.06.2025 edition.
2. `LATEST_AMENDMENT_EVENT_AND_CURRENT_CONSOLIDATED_BODY_HAVE_SEPARATE_PROVENANCE` — primary publication of No. 920/2025 proves the amendment event; a legal-system consolidated text corroborates the resulting current edition.
3. `FULLTEXT_REQUIRES_ALL_APPROVED_COMPONENTS` — No. 670 and No. 815 are incomplete if an approved requirement/list is missing.
4. `QUEUE_DATE_MUST_BE_REVALIDATED_AGAINST_PRIMARY_IDENTITY` — corrected No. 815 from 23.05.2023 to 25.05.2023 before corpus ingest.
5. `NO_LATER_AMENDMENT_FOUND != PRIMARY_CURRENT_STATUS_VERIFIED` remains enforced for No. 552 and similar acts.

## Next queue

Continue Habr `Идентификация и аутентификация` after item 26. PP RF No. 883 (31.05.2023) and No. 834 (21.06.2024) were already processed earlier as replacement acts for No. 1089 and No. 2326 respectively and should be deduplicated unless new GitHub/full-text or primary-current evidence appears. New unprocessed targets are PP RF No. 408 (01.04.2024), PP RF No. 372 (03.04.2026), then Order of the Ministry of Digital Development/Mincomsvyaz No. 321 (25.06.2018), continuing in article order.
