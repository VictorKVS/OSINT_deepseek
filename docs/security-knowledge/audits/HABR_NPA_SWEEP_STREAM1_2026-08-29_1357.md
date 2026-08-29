# Habr NPA sweep — Stream 1 — 2026-08-29 13:57 MSK

Scope: continue systematic pass over Habr article 432466 and the user NPA list for federal laws, Presidential/Government acts, Roskomnadzor and general personal-data/information regulation.

## Delta summary

- `FULL_TEXT`: +0
- `RELIABLE_GITHUB_CANDIDATE`: +0
- `REJECTED_FALSE_POSITIVE`: +1
- `GITHUB_FULL_TEXT_BLOCKER`: +5
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`: +1 (`RKN 128/2022`)
- `PRIMARY_AMENDMENT_CONFIRMED`: +1 (`RKN 1/2023 -> RKN 253/2021`)
- `PRIMARY_PUBLICATION_URL_IDENTIFIED_BUT_DIRECT_FETCH_UNRESOLVED`: +2 (`RKN 18/2021`, `RKN 253/2021`)
- exact duplicates: +0

## Targets processed

### 1. Roskomnadzor Order 16.07.2010 No. 482

Canonical title in Habr: `Об утверждении образца формы уведомления об обработке персональных данных` (with recommendations for completing the notification form).

GitHub result: no reproducible target body or reliable per-act candidate found in the exact/expanded searches performed in this pass.

Artifact fields: `repo/commit/path/size/type/blob_sha = null` — do not invent file metadata when no reproducible artifact exists.

Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Lifecycle: secondary legal sources indicate that points 1 and 2 were later declared invalid by Roskomnadzor Order 19.08.2011 No. 706, but a primary direct lifecycle record for the base order was not resolved in this pass. Do **not** promote the secondary lifecycle statement to `VERIFIED_CURRENT`/`REPEALED` without primary verification.

### 2. Roskomnadzor Order 24.02.2021 No. 18

Title: `Об утверждении требований к содержанию согласия на обработку персональных данных, разрешенных субъектом персональных данных для распространения`.

GitHub exact target search produced no reproducible act body. An expanded content-phrase search produced one reproducible false positive:

- repo: `sergeygutovskiy/papakado.ru`
- commit/ref: `800e338ee3641228f86dbad5d7b32b81e0834691`
- path: `resources/ts/client/vue/layout/contacts/Policy.vue`
- size: `43654` bytes
- type: `file` (Vue source)
- blob SHA: `016acc023d31615a1a58d932785c22206f8c36a5`

Body inspection: this is a website privacy/personal-data policy. It contains generic clauses on personal data permitted for distribution and says that consent-content requirements are established by the authorized body, but it contains no `Роскомнадзор`, no order number/date, and no normative body of Order No. 18.

Classification: `CONTENT_PHRASE_FALSE_POSITIVE / IMPLEMENTATION_POLICY / TARGET_IDENTITY_UNVERIFIED / NOT_FULL_TEXT / REJECT`.

Official-publication pointer identified: `0001202104210039`; direct primary card fetch/search remained unresolved in this pass. Identity/registration is corroborated by official-publication reporting: registered 21.04.2021 No. 63204; effective from 01.09.2021. Current lifecycle must remain a separate unresolved field until primary verification.

### 3. Roskomnadzor Order 21.06.2021 No. 106

Title: `Об утверждении Правил использования информационной системы Федеральной службы по надзору в сфере связи, информационных технологий и массовых коммуникаций, в том числе порядка взаимодействия субъекта персональных данных с оператором`.

GitHub result: exact and title-fragment searches produced no reproducible target body/candidate.

Artifact fields: `repo/commit/path/size/type/blob_sha = null`.

Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Identity is corroborated by official-publication reporting as registered 11.08.2021 No. 64602 and effective from 01.03.2022. A direct primary current-lifecycle card was not resolved in this pass, so do not mark `VERIFIED_CURRENT` from secondary/press references alone.

### 4. Roskomnadzor Order 24.12.2021 No. 253

Title: `Об утверждении формы проверочного листа ... применяемого при осуществлении федерального государственного контроля (надзора) за обработкой персональных данных ...`.

GitHub result: exact target search produced no reproducible act body/candidate.

Artifact fields: `repo/commit/path/size/type/blob_sha = null`.

Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official-publication pointer for the base act identified: `0001202202280005`; direct primary card fetch remained unresolved in this pass. Registration/publication metadata is corroborated as 25.02.2022 No. 67486, official portal publication 28.02.2022.

**Primary lifecycle delta confirmed:** the official publication portal contains Roskomnadzor Order 10.01.2023 No. 1, registration 05.04.2023 No. 72886, publication `0001202304050016` on 05.04.2023. Its title explicitly states that it amends the checklist form approved by Order 24.12.2021 No. 253.

Therefore any future GitHub copy of No. 253 lacking the No. 1/2023 changes must be classified `STALE_CONFIRMED` after body-level comparison.

### 5. Roskomnadzor Order 05.08.2022 No. 128

Title: `Об утверждении перечня иностранных государств, обеспечивающих адекватную защиту прав субъектов персональных данных`.

GitHub result: exact target search produced no reproducible act body/candidate.

Artifact fields: `repo/commit/path/size/type/blob_sha = null`.

Classification: `GITHUB_FULL_TEXT_BLOCKER`.

**Primary initial publication confirmed:** official publication portal card identifies Roskomnadzor Order 05.08.2022 No. 128, registered 20.09.2022 No. 70152, publication number `0001202209200008`, publication date 20.09.2022.

This also resolves a prior noisy metadata trail: the correct primary publication identifier for No. 128 is `0001202209200008`; do not retain alternative unverified IDs.

Current lifecycle remains independently unresolved; initial official publication is not proof that the act is still current today.

## New gates / corpus rules

1. `CONTENT_PHRASE_MATCH != TARGET_IDENTITY`: a privacy policy that paraphrases the same legal requirement is not a candidate for the underlying NPA unless number/date/title or normative body identifies the act.
2. `NO_REPRODUCIBLE_ARTIFACT -> NULL_FILE_METADATA`: never fill repo/commit/path/size/type when a GitHub target cannot be reproduced.
3. `PRIMARY_PUBLICATION_URL_IDENTIFIED + FETCH_FAILURE != PRIMARY_DIRECT_VERIFIED`.
4. `PRIMARY_INITIAL_PUBLICATION != CURRENT_LIFECYCLE`.
5. `PRIMARY_AMENDMENT_FOUND -> FUTURE_BASE_TEXT_MUST_PASS_AMENDMENT_MARKER_CHECK`: for No. 253, Order No. 1/2023 is now a mandatory freshness marker.
6. `REFERENCE_LIST_METADATA_IS_UNTRUSTED_UNTIL_CHECKED`: Habr is a target/reference list, not the authority for registration/lifecycle metadata.

## Open blockers carried forward

- `GITHUB_FULL_TEXT_RKN_482_2010`
- `PRIMARY_LIFECYCLE_RKN_482_2010`
- `GITHUB_FULL_TEXT_RKN_18_2021`
- `PRIMARY_CURRENT_LIFECYCLE_RKN_18_2021`
- `GITHUB_FULL_TEXT_RKN_106_2021`
- `PRIMARY_CURRENT_LIFECYCLE_RKN_106_2021`
- `GITHUB_FULL_TEXT_RKN_253_2021`
- `PRIMARY_BASE_CARD_DIRECT_FETCH_RKN_253_2021`
- `GITHUB_FULL_TEXT_RKN_128_2022`
- `PRIMARY_CURRENT_LIFECYCLE_RKN_128_2022`
