# Habr NPA sweep — Stream 1 — 2026-08-31 09:58 MSK

## Scope
Continuation of the systematic review of Habr 432466, subsection `Техническое регулирование. Сертификация средств защиты информации`, targets:

1. Federal Law 30.12.2004 No. 218-FZ — `О кредитных историях`.
2. Government Resolution 26.06.1995 No. 608 — `О сертификации средств защиты информации`.
3. Government Resolution 01.12.2009 No. 982 — mandatory certification/declaration lists.
4. Government Resolution 21.04.2010 No. 266 — special conformity assessment for protected/state-secret products and processes.
5. FSTEK Order 10.04.2015 No. 33 — accreditation work rules.
6. FSTEK Order 03.04.2018 No. 55 — certification system for information-protection products.
7. FSTEK Order 01.12.2023 No. 240 — certification of secure software-development processes for information-protection products.

Habr reference: https://habr.com/ru/articles/432466/

## GitHub normative-body search

Exact number/date/title searches were performed for all seven targets, plus registration-number searches for FSTEK Orders 33, 55 and 240. No full normative body and no reliable normative-body candidate was found.

| target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| 218-FZ/2004 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 608/1995 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 982/2009 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 266/2010 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEK Order 33/2015 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEK Order 55/2018 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEK Order 240/2023 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

No new GitHub full-body duplicate and no GitHub body identity conflict was found in this batch. Search hits consisting only of summaries or references are not promoted to `FULL_TEXT`.

## New confirmed lifecycle/current-edition evidence

### Federal Law No. 218-FZ of 30.12.2004

The Habr identity is correct, but the target has a multi-layer temporal state.

Accessible consolidated legal text identifies an effective edition dated 04.08.2026. Federal Law No. 334-FZ of 04.08.2026 directly amends Article 4 of 218-FZ and enters into force on official publication; that layer is already effective on 31.08.2026.

Separately, enacted future changes are already prepared:

- Federal Law No. 545-FZ of 29.12.2025 directly amends 218-FZ; its Article 1 enters into force on 01.10.2026.
- Federal Law No. 137-FZ of 07.06.2025 supplies a further prepared target edition effective 26.11.2026.
- The consolidated system also exposes another prepared target edition effective 31.12.2026; its exact source act was not resolved in this pass and is therefore not promoted to a named lifecycle edge yet.

Store separately: `CURRENT_EFFECTIVE_BODY_2026-08-31`, `ENACTED_FUTURE_CHANGE_2026-10-01`, `ENACTED_FUTURE_CHANGE_2026-11-26`, plus an unresolved `PREPARED_FUTURE_EDITION_2026-12-31` pointer.

Status gate: `CURRENT_BODY_CAN_HAVE_MULTIPLE_ENACTED_FUTURE_LAYERS`; a future consolidated copy must not replace the currently effective body.

Primary-publication metadata for the latest/future amending laws was not directly resolved from the publication portal in this pass, so these remain `CURRENT/LIFECYCLE_CORROBORATED_NONPRIMARY` rather than `PRIMARY_DIRECT_FETCH_VERIFIED`.

### Government Resolution No. 608 of 26.06.1995

Accessible consolidated sources identify edition 21.04.2010 and status `Действует`. The 2010 amendment is Government Resolution No. 266. No later repeal was found in this pass.

Completeness: `FULL_TEXT = resolution shell + complete approved Regulation on certification of information-protection products`. Shell-only or an extract of the Regulation is `PARTIAL_TEXT`.

Because the current consolidated status was not resolved on a primary official source in this pass: `CURRENT_STATUS_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER`.

### Government Resolution No. 982 of 01.12.2009 — Habr stale/repealed conflict

Habr 28.05.2026 still lists No. 982 in the current certification section. Government Resolution No. 2425 of 23.12.2021 is officially published under publication No. `0001202112300200` dated 30.12.2021 and its title expressly includes recognition of prior Government acts as invalid.

The repeal appendix to No. 2425 directly lists Government Resolution No. 982 as item 1. No. 2425 entered into force on 01.09.2022. Therefore No. 982 is not a current target NPA after 01.09.2022.

A legacy-certificate transition did not preserve the act itself: certificates issued under No. 982 could remain valid until their own expiry, but no later than 01.09.2025. Thus `LEGACY_CERTIFICATE_TRANSITION != CONTINUED_ACT_VALIDITY`.

Classification: `HABR_REPEALED_ACT_CONFLICT / REPEALED_EFFECTIVE_2022-09-01 / REPLACEMENT_PP_2425_OFFICIALLY_PUBLISHED`.

The replacement act is officially confirmed, while the exact repeal appendix item was resolved from a direct consolidated legal text rather than from a fetched primary PDF in this pass; keep `PRIMARY_REPEAL_CLAUSE_FETCH_BLOCKER` instead of falsely elevating the clause itself to direct-primary verification.

### Government Resolution No. 266 of 21.04.2010

Current consolidated edition is 03.11.2014 after Government Resolution No. 1149/2014. The target remains a live act in accessible consolidated sources; its approved conformity-assessment Regulation remains part of the body.

Important lifecycle distinction: later changes to individual internal provisions or associated accreditation machinery must not be interpreted as repeal of the whole target. `PARTIAL_INTERNAL_REPEAL_OR_REWRITE != WHOLE_ACT_REPEALED`.

Completeness: `FULL_TEXT = resolution shell + complete approved Regulation + current amendment state`. An old copy that preserves superseded internal provisions without amendment markers is `OLD_OR_MIXED_EDITION`.

Primary consolidated-current source not resolved: `CURRENT_EDITION_2014_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER`.

### FSTEK Order No. 33 of 10.04.2015

Current consolidated edition is 27.07.2023, with changes/additions that entered into force on 01.03.2025.

The latest confirmed amending act is FSTEK Order No. 148 of 27.07.2023. The official publication portal records:

- Ministry of Justice registration No. `76062` dated 23.11.2023;
- publication No. `0001202311230019`;
- publication date 23.11.2023;
- title explicitly states that it amends the Rules approved by FSTEK Order No. 33.

This latest amendment is primary-publication verified. Any GitHub candidate lacking the complete Rules or reflecting the pre-01.03.2025 state is not current full text.

### FSTEK Order No. 55 of 03.04.2018

Current consolidated edition is 20.01.2026. The amending chain includes FSTEK Orders No. 121/2021, No. 172/2022, and latest No. 9 of 20.01.2026.

Order No. 9 is registered by the Ministry of Justice on 20.04.2026 under No. `86119`, directly amends the Regulation approved by Order No. 55, and entered into force 02.05.2026. The official-publication link resolves to publication No. `0001202604210031`; direct fetch of the primary page timed out in this pass. Classification: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_FETCH_BLOCKER`, not a missing-publication-metadata blocker.

Completeness: `FULL_TEXT = Order 55 shell + complete current Regulation + all current appendices/forms`. The current Regulation has at least three appendices/forms (application, decision, certificate); omission of any required appendix is `PARTIAL_TEXT`.

### FSTEK Order No. 240 of 01.12.2023

Initial publication and latest amendment are both primary-publication verified.

Initial Order No. 240:

- Ministry of Justice registration No. `77896` dated 16.04.2024;
- publication No. `0001202404170002`;
- publication date 17.04.2024.

Latest amendment — FSTEK Order No. 230 of 30.06.2025:

- Ministry of Justice registration No. `83573` dated 18.09.2025;
- publication No. `0001202509190005`;
- publication date 19.09.2025;
- entered into force 30.09.2025;
- directly amends the Procedure approved by Order No. 240.

Current consolidated edition is therefore 30.06.2025. The updated Procedure references GOST R 56939-2024.

Completeness: `FULL_TEXT = Order shell + complete Procedure + all three current appendices/forms`. A Procedure-only extract or pre-No.230 edition is not current full text.

## New counts

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_REPEALED_ACT_CONFLICT +1` (PP 982)
- `PRIMARY_REPLACEMENT_PUBLICATION_CONFIRMED +1` (PP 2425)
- `PRIMARY_REPEAL_CLAUSE_FETCH_BLOCKER +1` (PP 982 relation)
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED +2` (FSTEK 33 via 148; FSTEK 240 via 230)
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +1` (FSTEK 240)
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED +1` (FSTEK Order 9/2026 -> Order 55)
- `PRIMARY_DIRECT_FETCH_BLOCKER +1` (same Order 9 official page timed out)
- `ENACTED_FUTURE_CHANGE +2` (218-FZ: 01.10.2026, 26.11.2026)
- `PREPARED_FUTURE_EDITION_UNRESOLVED_SOURCE +1` (218-FZ: 31.12.2026)

## New corpus gates

1. `REPEALED_REFERENCE_ENTRY != CURRENT_NPA`.
2. `LEGACY_CERTIFICATE_TRANSITION != CONTINUED_ACT_VALIDITY`.
3. `CURRENT_BODY_CAN_HAVE_MULTIPLE_ENACTED_FUTURE_LAYERS`.
4. `PARTIAL_INTERNAL_REPEAL_OR_REWRITE != WHOLE_ACT_REPEALED`.
5. `OFFICIAL_PUBLICATION_LINK_RESOLVED_BUT_PRIMARY_FETCH_TIMEOUT = OFFICIAL_POINTER_CORROBORATED_NOT_DIRECT_FETCH`.
6. `FSTEK_FULLTEXT = ORDER_SHELL + APPROVED_REGULATION/PROCEDURE + ALL_CURRENT_APPENDICES`.
7. `PRIMARY_PUBLICATION_OF_REPLACEMENT_ACT != PRIMARY_DIRECT_VERIFICATION_OF_EVERY_REPEAL_APPENDIX_ITEM`.

## Next queue

Continue with Habr subsection `Техническое регулирование. Аттестация объектов информатизации`:

1. `Положение по аттестации объектов информатизации по требованиям безопасности информации` (25.11.1994).
2. Gostekhkomissiya Order 05.01.1996 No. 3 — Typical regulation on a certification body.
3. FSTEK Order 29.04.2021 No. 77.
4. FSTEK information message 02.09.2021 No. 240/24/4303.
5. Ministry of Digital Development information message 03.06.2022 — typical technical assignment.
6. FSTEK information message 11.04.2022 No. 240/24/1950.
7. FSTEK Order 27.07.2023 No. 147.
