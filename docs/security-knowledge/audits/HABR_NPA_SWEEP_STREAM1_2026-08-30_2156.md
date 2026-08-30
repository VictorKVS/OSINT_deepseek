# Habr NPA sweep — Stream 1 — 2026-08-30 21:56 MSK

Scope: Habr 432466, section on identification/authentication and biometric personal data. Processed: PP RF No. 820 (14.07.2018), No. 1703 (28.12.2018), No. 1657 (30.09.2021), No. 1729 (11.10.2021), No. 1753 (15.10.2021), No. 1798 (20.10.2021).

## Counters

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +6
- NEW_GITHUB_DUPLICATE: +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT: +0
- HABR_REPEALED_ACT_CONFLICT: +2
- HABR_STALE_TITLE_OR_SCOPE_CONFLICT: +3
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +5
- OFFICIAL_INITIAL_PUBLICATION_POINTER_CORROBORATED: +1
- PRIMARY_AMENDMENT_OR_REPEAL_PUBLICATION_CONFIRMED: +5
- CURRENT_EDITION_CORROBORATED: +4

## GitHub search result

Exact/date/title-oriented GitHub code searches produced no indexed target-body hits for all six documents. Therefore for each target:

`repo=null; commit=null; path=null; size=null; type=null; classification=GITHUB_FULL_TEXT_BLOCKER`.

No GitHub copy was treated as official, and no mention/summary artifact was promoted to a full-text candidate.

## Confirmed findings

### PP RF 14.07.2018 No. 820

- GitHub: no full text/candidate; all file metadata fields null.
- Initial official publication pointer: `0001201807240012`, publication date 24.07.2018 (pointer corroborated; direct historical card not stably resolved in this pass).
- Current consolidated edition corroborated as 08.11.2023.
- PP RF 08.11.2023 No. 1872 directly rewrote the title/scope and text of No. 820. Official publication: `0001202311090022`, 09.11.2023.
- Habr snapshot 28.05.2026 still carries the older title/scope. Classification: `HABR_STALE_TITLE_AND_BODY_SCOPE_CONFLICT`.

Primary/latest amendment source: https://publication.pravo.gov.ru/document/0001202311090022

### PP RF 28.12.2018 No. 1703

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication confirmed: `0001201812290031`, 29.12.2018.
- Current edition corroborated as 07.03.2023.
- PP RF 07.03.2023 No. 359 directly amended No. 1703. Official publication: `0001202303100020`, 10.03.2023.
- Current document contains two rule sets (EBS operator and regional-segment operator); a GitHub artifact missing either rule set would be `PARTIAL_TEXT`.
- No Habr title conflict confirmed for this item in this pass.

Primary sources:
- https://publication.pravo.gov.ru/document/0001201812290031
- https://publication.pravo.gov.ru/document/0001202303100020

### PP RF 30.09.2021 No. 1657

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication confirmed: `0001202110020003`, 02.10.2021.
- PP RF 23.03.2024 No. 367 explicitly included No. 1657 in the list of acts declared invalid and entered into force on official publication, 26.03.2024.
- Primary repeal publication confirmed: `0001202403260025`, 26.03.2024.
- Habr snapshot 28.05.2026 still lists No. 1657 as a current reference. Classification: `HABR_REPEALED_ACT_CONFLICT / REPEALED_EFFECTIVE_2024-03-26`.

Primary sources:
- https://publication.pravo.gov.ru/document/0001202110020003
- https://publication.pravo.gov.ru/document/0001202403260025

### PP RF 11.10.2021 No. 1729

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication confirmed: `0001202110130008`, 13.10.2021.
- PP RF 11.04.2023 No. 585 explicitly recognized No. 1729 as invalid. Official publication: `0001202304120011`, 12.04.2023.
- Current legal sources corroborate loss of force from 20.04.2023.
- Habr snapshot 28.05.2026 still lists No. 1729. Classification: `HABR_REPEALED_ACT_CONFLICT / REPEALED_FROM_2023-04-20`.

Primary sources:
- https://publication.pravo.gov.ru/document/0001202110130008
- https://publication.pravo.gov.ru/document/0001202304120011

### PP RF 15.10.2021 No. 1753

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication confirmed: `0001202110180003`, 18.10.2021.
- Current edition corroborated as 23.03.2024.
- PP RF 23.03.2024 No. 367 directly rewrote No. 1753, including replacement of the legacy long-form EBS terminology with `единая биометрическая система`.
- Primary amendment publication: `0001202403260025`, 26.03.2024.
- Habr snapshot 28.05.2026 still uses the old title/terminology. Classification: `HABR_STALE_TITLE_AND_TERMINOLOGY_CONFLICT`.

Primary sources:
- https://publication.pravo.gov.ru/document/0001202110180003
- https://publication.pravo.gov.ru/document/0001202403260025

### PP RF 20.10.2021 No. 1798

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication confirmed: `0001202110210025`, 21.10.2021.
- Current edition corroborated as 08.09.2023.
- PP RF 08.09.2023 No. 1463 directly replaced the former long-form EBS wording with `единая биометрическая система`; changes took effect 17.09.2023.
- Primary amendment publication confirmed: `0001202309090002`, 09.09.2023.
- Habr snapshot 28.05.2026 still carries the legacy wording. Classification: `HABR_STALE_TITLE_AND_TERMINOLOGY_CONFLICT`.

Primary sources:
- https://publication.pravo.gov.ru/document/0001202110210025
- https://publication.pravo.gov.ru/document/0001202309090002

## New regression gates

1. `HABR_LISTING_OF_REPEALED_ACT != CURRENT_REQUIREMENT` — a current-looking item in a secondary checklist must be resolved against the repeal chain.
2. `TITLE_AND_TERMINOLOGY_ARE_TEMPORAL_METADATA` — number/date identity can remain constant while the legal title and scope materially change.
3. `FULL_TEXT_FOR_MULTI_RULE_PP_REQUIRES_ALL_APPROVED_RULE_SETS` — e.g. No. 1703 is not complete if only one of its two approved rule sets is present.
4. `PRIMARY_REPEAL_RELATION_OVERRIDES_SECONDARY_CHECKLIST` — explicit repeal in the published amending/repealing act outranks a later Habr listing.

## Next queue

Continue the same Habr section with PP RF No. 1799 (20.10.2021), No. 1815 (22.10.2021), then the 2022 identification/EBS block (No. 1066, No. 1067, No. 1089), while deduplicating against already processed items.
