# Habr NPA sweep — Stream 1 — 2026-08-31 13:53 MSK

Scope: Habr 432466, section `Лицензирование деятельности в области информационной безопасности`, positions 15–22.

Method:
- GitHub exact/code search by number/date/title/registration identifiers.
- A GitHub copy is never treated as an official source automatically.
- `FULL_TEXT` requires the complete operative body and all required appendices/forms; references, summaries and bibliography-only hits are rejected.
- Official/current status is resolved separately against primary regulator/publication sources; where a primary consolidated current card is unavailable, the blocker is kept.

## Batch counters

- targets: 8
- `GITHUB_FULL_TEXT`: 0
- `RELIABLE_GITHUB_CANDIDATE`: 0
- `GITHUB_FULL_TEXT_BLOCKER`: 8
- `NEW_GITHUB_FULL_BODY_DUPLICATE`: 0
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT`: 0
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`: 5 (orders 3, 4, 142, 163, 164)
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`: 3 (FSB 557/2025; FSTEC 487/2025 affecting both 163 and 164)
- `OFFICIAL_REGULATOR_HOSTING_CONFIRMED`: 3 (226/2022, 240/13/3384, 483/2025)
- `NON_NPA_INFORMATIONAL_MATERIAL`: 1 (240/13/3384)
- `ANNUAL_PROGRAM_LEGACY_ENTRY`: 1 (226/2022, program for 2023)
- `CURRENT_ANNUAL_PROGRAM`: 1 (483/2025, program for 2026)
- `SOURCE_METADATA_CONFLICT_CORRECTED`: 1 (FSB 142 registration number: primary source = 72831)

## Position 15 — FSTEC order 226 of 20.12.2022

Title: Program for prevention of violations of mandatory requirements in FSTEC licensing control for 2023.

GitHub:
- exact search: no usable file
- `repo=null; commit=null; path=null; size=null; type=null`
- status: `GITHUB_FULL_TEXT_BLOCKER`

Official status:
- Official FSTEC page confirms order No. 226 dated 20.12.2022 and the program explicitly scoped to year 2023.
- This is a time-bounded annual prevention program. It is not treated as a current 2026 operative program.
- Habr retains it alongside the later 2026 program; classify as `HABR_LEGACY_ANNUAL_PROGRAM_RETAINED`, not as proof that the 2023 program is currently operative.
- NPA/general-binding status is not inferred merely from regulator hosting: `REGISTRATION_NOT_ESTABLISHED / NPA_STATUS_NOT_ASSUMED`.

Primary/regulator source:
- https://fstec.ru/dokumenty/vse-dokumenty/prikazy/prikaz-fstek-rossii-ot-20-dekabrya-2022-g-n-226

## Position 16 — FSTEC order 3 of 12.01.2023

Identity:
- title matches Habr
- Ministry registration No. 72230
- official publication No. `0001202302030006`, 03.02.2023
- official portal PDF: 2823 KB, 85 pages

GitHub:
- exact title/number search: no usable file
- `repo=null; commit=null; path=null; size=null; type=null`
- status: `GITHUB_FULL_TEXT_BLOCKER`

Lifecycle/completeness:
- Order repeals FSTEC order 134 of 17.07.2017 and amendments to it.
- `FULL_TEXT` must include the order and all approved licensing forms; main order alone is `PARTIAL_TEXT`.
- Current official FSTEC hosting remains available; no later repeal/amendment was confirmed in this sweep, but absence of a later hit is not elevated to a primary consolidated current-status proof.
- status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_OFFICIAL_HOSTING_CONFIRMED / PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

Sources:
- https://publication.pravo.gov.ru/document/0001202302030006
- https://fstec.ru/dokumenty/vse-dokumenty/prikazy/prikaz-fstek-rossii-ot-12-yanvarya-2023-g-n-3

## Position 17 — FSTEC order 4 of 12.01.2023

Identity:
- title matches Habr
- Ministry registration No. 72229
- official publication No. `0001202302030009`, 03.02.2023
- official portal PDF: 1914 KB, 57 pages

GitHub:
- exact title/registration search: no usable file
- `repo=null; commit=null; path=null; size=null; type=null`
- status: `GITHUB_FULL_TEXT_BLOCKER`

Lifecycle/completeness:
- Order repeals FSTEC order 133 of 17.07.2017 and amendments to it.
- `FULL_TEXT` requires the order plus all approved forms; order body alone is `PARTIAL_TEXT`.
- Current official FSTEC hosting remains available; no later repeal/amendment confirmed in this sweep.
- status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_OFFICIAL_HOSTING_CONFIRMED / PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

Sources:
- https://publication.pravo.gov.ru/document/0001202302030009
- https://fstec.ru/dokumenty/vse-dokumenty/prikazy/prikaz-fstek-rossii-ot-12-yanvarya-2023-g-n-4

## Position 18 — FSB order 142 of 25.03.2023

Identity correction:
- official publication No. `0001202303310020`
- Ministry registration No. **72831**
- Habr uses 72831 and is correct on this field.
- A previously surfaced Russian Gazette metadata snippet showed 75831; primary publication and the Ministry/official legal record resolve the conflict in favor of 72831.
- classify `SECONDARY_METADATA_CONFLICT / PRIMARY_WINS`.

GitHub:
- exact number/date/title search: no usable file
- `repo=null; commit=null; path=null; size=null; type=null`
- status: `GITHUB_FULL_TEXT_BLOCKER`

Current lifecycle:
- original order had a time-limited application period.
- FSB order 545 of 16.12.2024 amended point 2 (Ministry registration No. 80660).
- FSB order 557 of 29.12.2025 again amended point 2; official publication No. `0001202512300057`, Ministry registration No. 84878, effective 31.12.2025.
- current application limit is **through 31.12.2028 inclusive**.
- therefore an original 2023 copy without amendments 545/2024 and 557/2025 is `OLD_EDITION`, not current full text.
- `FULL_TEXT` must include the operative order plus all 4 procedure appendices, with the current point-2 validity period.

Sources:
- https://publication.pravo.gov.ru/document/0001202303310020
- https://minjust.consultant.ru/documents/53997
- https://publication.pravo.gov.ru/document/0001202512300057

## Position 19 — FSTEC order 163 of 12.05.2025

Identity:
- Ministry registration No. 82774
- official publication No. `0001202507020008`, 02.07.2025
- official portal PDF: 739 KB, 12 pages

GitHub:
- registration/title search: no usable file
- `repo=null; commit=null; path=null; size=null; type=null`
- status: `GITHUB_FULL_TEXT_BLOCKER`

Current lifecycle:
- original point 2 limited application through 31.12.2025.
- FSTEC order 487 of 29.12.2025 changes the limit from 2025 to **2028**.
- order 487: Ministry registration No. 84884; official publication No. `0001202512300067`, 30.12.2025; official PDF 107 KB, 2 pages; effective 31.12.2025.
- current confirmed status: applicable through **31.12.2028 inclusive**.
- 2026 FSTEC review order No. 194 also references order 163 as the governing licensing-control procedure, corroborating current operational use.
- any GitHub copy of the original 2025 text without order 487 is `OLD_EDITION`.

Sources:
- https://publication.pravo.gov.ru/document/0001202507020008
- https://publication.pravo.gov.ru/document/0001202512300067

## Position 20 — FSTEC order 164 of 12.05.2025

Identity:
- Ministry registration No. 82775
- official publication No. `0001202507020007`, 02.07.2025
- official portal PDF: 743 KB, 11 pages

GitHub:
- registration/title search: no usable file
- `repo=null; commit=null; path=null; size=null; type=null`
- status: `GITHUB_FULL_TEXT_BLOCKER`

Current lifecycle:
- original point 2 limited application through 31.12.2025.
- FSTEC order 487 of 29.12.2025 changed the limit to **31.12.2028 inclusive**.
- same primary amendment publication: `0001202512300067`.
- 2026 FSTEC review order No. 194 references order 164 as operative licensing-control procedure.
- original 2025 body without 487/2025 is `OLD_EDITION`.

Sources:
- https://publication.pravo.gov.ru/document/0001202507020007
- https://publication.pravo.gov.ru/document/0001202512300067

## Position 21 — FSTEC informational message 240/13/3384 of 30.06.2025

Identity:
- official FSTEC page confirms date/number and subject: change of display format for the address of the place of licensed activity in FSTEC public license registers, effective from 01.07.2025.
- official FSTEC tag/index reports file size about 76.57 KB.

GitHub:
- exact number search: no usable file
- `repo=null; commit=null; path=null; size=null; type=null`
- status: `GITHUB_FULL_TEXT_BLOCKER`

Classification:
- `NON_NPA_INFORMATIONAL_MATERIAL`.
- Do not place in the registered-NPA corpus merely because it is officially hosted by FSTEC.
- It belongs in regulator guidance / operational-information layer.

Source:
- https://fstec.ru/dokumenty/vse-dokumenty/informatsionnye-i-analiticheskie-materialy/informatsionnoe-soobshchenie-fstek-rossii-ot-30-iyunya-2025-g-n-240-13-3384

## Position 22 — FSTEC order 483 of 19.12.2025

Identity:
- official FSTEC page confirms order No. 483 dated 19.12.2025 and the Prevention Program for **2026**.

GitHub:
- exact number/date/title search: no usable file
- `repo=null; commit=null; path=null; size=null; type=null`
- status: `GITHUB_FULL_TEXT_BLOCKER`

Current status/classification:
- This is the current annual prevention program for 2026 found on the regulator's official site.
- Do not infer registered-NPA/general-binding status from regulator hosting alone: `OFFICIAL_REGULATOR_ORDER / ANNUAL_PROGRAM / REGISTRATION_NOT_ESTABLISHED / NPA_STATUS_NOT_ASSUMED`.
- It supersedes the 2023 annual program operationally by annual scope; this is not modeled as a formal repeal unless a repeal clause is found.

Source:
- https://fstec.ru/dokumenty/vse-dokumenty/prikazy/prikaz-fstek-rossii-ot-19-dekabrya-2025-g-n-483

## New gates added

1. `ANNUAL_PROGRAM_YEAR_EXPIRED != FORMAL_REPEAL`.
2. `CURRENT_YEAR_PROGRAM != AUTOMATIC_FORMAL_REPEAL_OF_OLD_YEAR_PROGRAM`.
3. `REGULATOR_HOSTING != AUTOMATIC_REGISTERED_NPA_STATUS`.
4. `ORIGINAL_TIME_LIMITED_ORDER + EXTENSION_AMENDMENT => CURRENT_BODY_REQUIRES_EXTENSION`.
5. `SECONDARY_SOURCE_REGISTRATION_NUMBER_CONFLICT => PRIMARY_PUBLICATION_RECORD_WINS`.
6. `OFFICIAL_INFORMATIONAL_MESSAGE != NPA`.
7. `MAIN_ORDER_WITHOUT_REQUIRED_FORMS/PROCEDURE_APPENDICES != FULL_TEXT`.

## Next boundary

Continue after licensing position 22 into `Информационная безопасность и персонал`, while also prioritizing user-scope federal laws, presidential/government acts, Roskomnadzor and common personal-data/information acts. Do not rescan already closed targets unless a new GitHub body, amendment/repeal, official publication or identity conflict appears.
