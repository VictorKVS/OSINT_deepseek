# Habr NPA sweep — Stream 1 — 2026-08-30 23:52 MSK

Scope: Habr 432466, `Идентификация и аутентификация`, positions 17–21. Processed: PP RF No. 2326 (16.12.2022), No. 2511 (29.12.2022), No. 405 (17.03.2023), No. 451 (24.03.2023), No. 478 (27.03.2023).

## Counters

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +5
- NEW_GITHUB_DUPLICATE: +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT: +0
- HABR_REPEALED_ACT_CONFLICT: +1
- HABR_REPEALED_ACT_AND_REPLACEMENT_SIMULTANEOUSLY: +1
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +5
- PRIMARY_REPLACEMENT_PUBLICATION_CONFIRMED: +1
- PRIMARY_GOVERNMENT_CURRENT_FULLTEXT_CONFIRMED: +1
- CURRENT_EDITION_CORROBORATED: +2
- CURRENT_STATUS_CORROBORATED_NONPRIMARY: +2
- PRIMARY_CURRENT_STATUS_BLOCKER: +2

## GitHub search result

Exact number/date and title-oriented GitHub Code Search returned no indexed target-body file or reliable candidate for all five documents. For each target:

`repo=null; commit=null; path=null; size=null; type=null; classification=GITHUB_FULL_TEXT_BLOCKER`.

The exact/title searches returned `total_count=0; incomplete_results=false`. A broader numeric/date query for No. 2326 produced unrelated files (COVID CSV, giveaway JS and other non-Russian-law artifacts); these are `NOISY_FALSE_POSITIVE / NON_TARGET` and were not promoted to candidates.

No GitHub copy was treated as official. No reference-only artifact, summary, implementation, corpus index or downloader was counted as a full text.

## Confirmed findings

### PP RF 16.12.2022 No. 2326

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication is confirmed on the Official Internet Portal of Legal Information: publication No. `0001202212190055`, published 19.12.2022.
- The act assigned JSC `Center for Biometric Technologies` the operator functions of the former long-form EBS construct.
- PP RF 21.06.2024 No. 834 is the replacement act: the official publication portal confirms No. `0001202406210030`, published 21.06.2024, and the official daily government-act listing carries No. 834 with the current title `Об определении организации, осуществляющей функции оператора единой биометрической системы`.
- ConsultantPlus' current legal review expressly states that PP No. 2326 was recognized as invalid by No. 834. Thus No. 2326 is not a current requirement.
- Habr 28.05.2026 still lists No. 2326 while later in the same section it also lists No. 834. This is a lifecycle contradiction inside the same checklist.
- Classification: `HABR_REPEALED_ACT_CONFLICT / HABR_REPEALED_ACT_AND_REPLACEMENT_SIMULTANEOUSLY / PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_REPLACEMENT_PUBLICATION_CONFIRMED`.
- Blocker: direct extraction of the repeal clause from the primary No. 834 card timed out during this pass; repeal relation is therefore corroborated by the enacted primary replacement plus a current legal-system review, not promoted to `PRIMARY_REPEAL_CLAUSE_DIRECT_FETCH_VERIFIED`.

Sources:
- Habr: https://habr.com/ru/articles/432466/
- Primary initial publication: https://publication.pravo.gov.ru/Document/View/0001202212190055
- Primary replacement publication: https://publication.pravo.gov.ru/document/0001202406210030
- Current legal review of replacement/repeal relation: https://www.consultant.ru/law/review/209045530.html

### PP RF 29.12.2022 No. 2511

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication is confirmed: publication No. `0001202212310024`, published 31.12.2022.
- Current consolidated edition is corroborated as 23.03.2024.
- PP RF 23.03.2024 No. 367 directly amends the Regulation approved by No. 2511: it rewrites point 1, changes point 6 and rewrites point 9. This is a real body change, not only a cross-reference update.
- The Habr title remains consistent with the current act; no stale-title conflict recorded in this pass.
- `FULL_TEXT` requires the resolution plus the complete Regulation on the Coordination Council. A file containing only the short dispositive part is `PARTIAL_TEXT`.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_EDITION_CORROBORATED_2024-03-23 / GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- Primary initial publication: https://publication.pravo.gov.ru/Document/View/0001202212310024
- Amendment body used to confirm the No. 2511 relation: PP RF 23.03.2024 No. 367 (point 14 of the amendments).

### PP RF 17.03.2023 No. 405

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication is directly confirmed: publication No. `0001202303200017`, published 20.03.2023.
- The primary Government portal reproduces the current normative body and marks it as amended by PP RF 23.03.2024 No. 367.
- Current operative rule: No. 405 entered into force 01.06.2023 and acts until 01.01.2027, except the fifth paragraph of point 6 of the Rules, which acted only until 01.01.2025.
- This creates a norm-level partial-expiry case inside an otherwise still-current act.
- `FULL_TEXT` requires the resolution + Rules + approved consent form. Missing the form is `PARTIAL_TEXT`.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_GOVERNMENT_CURRENT_FULLTEXT_CONFIRMED / CURRENT_EDITION_2024-03-23 / PARTIAL_NORM_VALIDITY_WINDOW_PRESENT`.

Primary sources:
- Publication: https://publication.pravo.gov.ru/Document/View/0001202303200017
- Current Government text: https://government.ru/docs/all/146559/

### PP RF 24.03.2023 No. 451

- GitHub: no full text/candidate; all file metadata fields null.
- Primary publication identity is confirmed by the Official Internet Portal of Legal Information: publication No. `0001202303290035`, published 29.03.2023.
- Current consolidated legal record still shows the original edition 24.03.2023, effective from 01.06.2023, status `Действует`; no later amendment was found in this pass.
- Because a current primary Government-hosted consolidated card was not resolved, the current-state label remains `CURRENT_STATUS_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER` rather than `PRIMARY_CURRENT_STATUS_VERIFIED`.
- `FULL_TEXT` requires the resolution + the full approved Rules; a reference or summary of the request workflow is not enough.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_STATUS_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER / GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- Primary publication: https://publication.pravo.gov.ru/Document/View/0001202303290035
- Consolidated status cross-check: https://normativ.kontur.ru/document/1/445458-postanovlenie-pravitelstva-rf-ot-24-03-2023-n-451

### PP RF 27.03.2023 No. 478

- GitHub: no full text/candidate; all file metadata fields null.
- Primary publication identity is confirmed by the Official Internet Portal of Legal Information: publication No. `0001202303290038`, published 29.03.2023.
- Current consolidated legal record still shows the original edition 27.03.2023, effective from 01.06.2023, status `Действует`; no later amendment was found in this pass.
- A current primary Government-hosted consolidated card was not resolved, so the current-state record remains `CURRENT_STATUS_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER`.
- `FULL_TEXT` requires the resolution, the Rules, the refusal form, the withdrawal-of-refusal form and the MFC written-confirmation form. A document containing only the Rules is `PARTIAL_TEXT`.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_STATUS_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER / GITHUB_FULL_TEXT_BLOCKER`.

Sources:
- Primary publication: https://publication.pravo.gov.ru/Document/View/0001202303290038
- Consolidated status/body cross-check: https://normativ.kontur.ru/document/1/445572-postanovlenie-pravitelstva-rf-ot-27-03-2023-n-478

## New regression gates

1. `HABR_REPEALED_ACT_AND_REPLACEMENT_SIMULTANEOUSLY` — a checklist may retain both a dead act and its replacement; No. 2326 / No. 834 is the new fixture.
2. `PRIMARY_PUBLICATION_IDENTITY != CURRENT_STATUS` — initial official publication proves identity/origin, not continued force; lifecycle must be resolved separately.
3. `PARTIAL_NORM_EXPIRY_WITHIN_ACTIVE_ACT` — No. 405 is a fixture where the act remains in force while one internal norm has already expired.
4. `APPROVED_FORM_IS_PART_OF_FULLTEXT` — No. 405 and No. 478 are incomplete without their approved forms.
5. `NO_AMENDMENT_FOUND != PRIMARY_CURRENT_STATUS_VERIFIED` — absence of detected amendments in a consolidated system is not promoted above its provenance level.

## Next queue

Continue the same Habr section from item 22: PP RF No. 552 (06.04.2023), No. 585 (11.04.2023), No. 670 (28.04.2023), No. 810 (22.05.2023), No. 815 (23.05.2023). Deduplicate No. 810 if it has already been processed as the replacement for No. 1799; if so, record only genuinely new GitHub/full-text/current-status evidence rather than repeating the lifecycle conclusion.
