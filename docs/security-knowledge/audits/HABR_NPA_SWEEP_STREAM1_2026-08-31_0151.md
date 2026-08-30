# Habr NPA sweep — Stream 1 — 2026-08-31 01:51 MSK

Scope: Habr 432466, `Идентификация и аутентификация`, positions 27–31. Deduplicated positions 27 and 29 (PP RF No. 883/2023 and No. 834/2024) because they were already processed earlier as replacement acts for No. 1089/2022 and No. 2326/2022. New systematic targets: PP RF No. 408 (01.04.2024), PP RF No. 372 (03.04.2026), Order No. 321 (25.06.2018).

## Counters

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +3
- NEW_GITHUB_DUPLICATE: +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT: +0
- DUPLICATE_TARGET_ENTRY: +2 (`883/2023`, `834/2024`)
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +3 (`408/2024`, `372/2026`, `321/2018`)
- HABR_REPEALED_ACT_CONFLICT: +1 (`Order 321/2018`)
- REPLACEMENT_ACT_RELATION_CORROBORATED: +1 (`321/2018` -> `930/2021`)
- EXPLICIT_VALIDITY_WINDOW: +1 (`408/2024`, until 01.09.2027)
- STAGED_EFFECTIVE_DATES: +1 (`372/2026`: publication date / 01.07.2026 / 01.10.2026)
- PRIMARY_DIRECT_CARD_FETCH_BLOCKER: +3 (publication search records resolved; direct portal cards timed out in this pass)

## GitHub search

Connected/global GitHub Code Search and public-web `site:github.com` searches were run with exact number/date/title terms and, where available, exact official publication IDs.

Exact publication-ID searches:

- PP No. 408/2024, publication ID `0001202404050032`: `total_count=0`, `incomplete_results=false`.
- PP No. 372/2026, publication ID `0001202604080050`: `total_count=0`, `incomplete_results=false`.
- Order No. 321/2018, publication ID `0001201807110014`: `total_count=0`, `incomplete_results=false`.

For all three new targets:

`repo=null; commit=null; path=null; size=null; type=null; classification=GITHUB_FULL_TEXT_BLOCKER`.

No GitHub copy is treated as official. Mentions, indexes, summaries, download scripts and unrelated numeric matches remain non-body evidence.

## Confirmed findings

### PP RF 01.04.2024 No. 408

- Habr identity is correct: 01.04.2024 No. 408, on the types of biometric personal data covered by Federal Law No. 572-FZ.
- Primary initial publication is confirmed by the Official Internet Portal of Legal Information: publication No. `0001202404050032`, published 05.04.2024.
- Current legal-system text identifies the act as effective from 01.09.2024 and explicitly valid until 01.09.2027 (item 2).
- No later amendment/repeal was confirmed in this pass.
- GitHub: no target body/candidate.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_STATUS_CORROBORATED_NONPRIMARY / EXPLICIT_VALIDITY_WINDOW_TO_2027-09-01 / GITHUB_FULL_TEXT_BLOCKER`.

Primary source:
- https://publication.pravo.gov.ru/document/0001202404050032

Cross-check:
- https://normativ.kontur.ru/document/1/468671-postanovlenie-pravitelstva-rf-ot-01-04-2024-n-408

### PP RF 03.04.2026 No. 372

- Habr identity is correct and complete at the top level: No. 372 approves (1) Rules for registration of an individual in ESIA, (2) Rules for checking/updating ESIA data using state information systems, (3) amendments to Government acts, and (4) a list of repealed acts/provisions.
- Primary publication is confirmed by the Official Internet Portal of Legal Information: publication No. `0001202604080050`, published 08.04.2026.
- Government.ru independently lists the same number/date/title.
- The act has staged effective dates: the general rule takes effect on official publication; a specified provision of item 15 of the registration Rules takes effect 01.07.2026; specified rules concerning incapable persons/related registration functions take effect 01.10.2026.
- Therefore, as of 31.08.2026, the 01.07.2026 layer is already effective while the 01.10.2026 layer is still `ENACTED_FUTURE_CHANGE`.
- The act also repeals selected provisions/acts tied to the previous ESIA registration mechanism. Do not model this as full repeal of PP No. 584/2013: No. 372 itself amends No. 584 while repealing only specific provisions and separate amendment acts.
- GitHub: no target body/candidate.
- `FULL_TEXT` requires all four components listed above; a file containing only the registration Rules is `PARTIAL_TEXT`.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / STAGED_EFFECTIVE_DATES / PARTIAL_FUTURE_EFFECTIVE_LAYER_2026-10-01 / FULLTEXT_REQUIRES_FOUR_COMPONENTS / GITHUB_FULL_TEXT_BLOCKER`.

Primary sources:
- https://publication.pravo.gov.ru/document/0001202604080050
- https://government.ru/docs/all/

Cross-check full text:
- https://legalacts.ru/doc/postanovlenie-pravitelstva-rf-ot-03042026-n-372-o-porjadke/

### Order of Mincomsvyaz/Ministry of Digital Development 25.06.2018 No. 321

- Habr still lists Order No. 321 in the 28.05.2026 version.
- Primary initial publication is confirmed: publication No. `0001201807110014`; the act is identified as Order No. 321 of 25.06.2018 and was registered by the Ministry of Justice on 04.07.2018 as No. 51532.
- The act is no longer current. Order of the Ministry of Digital Development No. 930 of 10.09.2021 expressly states in item 2 that Order No. 321/2018 and its amending Order No. 369/2019 are invalidated; No. 930 entered into force on 01.03.2022 and is stated to operate until 01.03.2028.
- Primary publication identity of No. 930 is confirmed separately: publication No. `0001202110280037`, 28.10.2021, registration No. 65621.
- Direct opening of the official publication cards timed out in this pass, so the repeal clause itself is corroborated from complete legal-system copies rather than promoted to `PRIMARY_REPEAL_CLAUSE_DIRECT_FETCH_VERIFIED`.
- Habr simultaneously lists No. 321 and its replacement No. 930 (position 37), creating a clear `HABR_REPEALED_ACT_AND_REPLACEMENT_SIMULTANEOUSLY` fixture.
- GitHub: no target body/candidate.
- Classification: `HABR_REPEALED_ACT_CONFLICT / REPEALED_EFFECTIVE_2022-03-01 / REPLACED_BY_ORDER_930_2021 / PRIMARY_REPLACEMENT_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER`.

Primary sources:
- No. 321: https://publication.pravo.gov.ru/document/0001201807110014
- No. 930: https://publication.pravo.gov.ru/document/0001202110280037

Cross-check repeal clause/full text:
- https://rulaws.ru/acts/Prikaz-Mintsifry-Rossii-ot-10.09.2021-N-930/

## New regression gates

1. `STAGED_EFFECTIVE_DATES_REQUIRE_PROVISION_LEVEL_STATE` — PP No. 372 has provisions effective on publication, 01.07.2026 and 01.10.2026; one document-level boolean is insufficient.
2. `PARTIAL_REPEAL_OR_AMENDMENT != WHOLE_ACT_REPEALED` — PP No. 372 changes PP No. 584/2013 and repeals selected provisions/earlier amendment acts, not the entire No. 584.
3. `HABR_REPEALED_ACT_AND_REPLACEMENT_CAN_COEXIST` — Order No. 321 remains listed together with replacement Order No. 930.
4. `EXPLICIT_VALID_UNTIL_NEEDS_LIFECYCLE_WATCH` — PP No. 408 is currently bounded by 01.09.2027; this date belongs in corpus temporal metadata.
5. `PUBLICATION_ID_SEARCH_ZERO_RESULTS_IS_A_GITHUB_BLOCKER_SIGNAL, NOT_PROOF_OF_ABSENCE` — exact ID searches returned 0 indexed files; keep `repo/commit/path/size/type=null` until a body candidate is actually found.

## Next queue

Continue Habr `Идентификация и аутентификация` after position 31: Order No. 323 (25.06.2018), Order No. 187 (29.03.2021), Order No. 494 (25.05.2021), Order No. 685 (07.07.2021), then No. 902/2021 and No. 930/2021, deduplicating No. 930 as the already confirmed replacement of No. 321 unless new GitHub/full-text or current-primary evidence is found.
