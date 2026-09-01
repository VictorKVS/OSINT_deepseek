# Habr NPA sweep — Stream 1 — 2026-09-01 19:56 MSK

## Scope

Habr 432466, section `Транспорт`, positions 1–5:

1. Федеральный закон от 09.02.2007 №16-ФЗ «О транспортной безопасности».
2. Постановление Правительства РФ от 24.07.2019 №955 «Об утверждении требований к автоматизированной информационной системе оформления воздушных перевозок, к базам данных, входящим в ее состав, к информационно-телекоммуникационной сети, обеспечивающей работу указанной автоматизированной информационной системы, к ее оператору, а также мер по защите информации, содержащейся в ней, и порядка ее функционирования».
3. Постановление Правительства РФ от 14.11.2022 №2051 «Об утверждении Правил обращения со сведениями о результатах проведенной оценки уязвимости ...».
4. Приказ Минтранса России от 28.10.2022 №439 «Об установлении порядка формирования и ведения автоматизированной централизованной базы персональных данных, касающихся состояния здоровья членов летного экипажа гражданского воздушного судна и диспетчеров управления воздушным движением...».
5. Постановление Правительства РФ от 01.06.2023 №906 «Об аккредитации юридических лиц для обработки персональных данных отдельных категорий лиц ... в области транспортной безопасности».

Habr source: https://habr.com/ru/articles/432466/

## GitHub body/candidate audit

| Target | repo | commit/ref | path | size | type | Result |
|---|---|---|---|---:|---|---|
| 16-ФЗ/2007 | `acurofobia/new` | `58f83804d6b8155b2ad15f0372819bbbce492cf1` | `project_backend/FAVT_tem_4k.json` | `131677 B` | JSON / educational test dataset | `MENTION_ONLY / EDUCATIONAL_TEST_DATASET / REJECTED_AS_NORMATIVE_BODY`. Blob `c2a5b093b33d24139b5fc6babf4c3a533556980d`. The file contains an exam question and a long list of regulatory acts; №16-ФЗ is only one cited item, not the law body. |
| PP RF №955/2019 | `null` | `null` | `null` | `null` | `null` | `GITHUB_FULL_TEXT_BLOCKER`. A related `edekeulenaar/global-digital-regulations` hit is an Air Code/amending-law context, not PP №955 body, and is rejected as target text. |
| PP RF №2051/2022 | `null` | `null` | `null` | `null` | `null` | `GITHUB_FULL_TEXT_BLOCKER`. Exact/distinctive-title search returned training/reference material, not the normative body. |
| Mintrans №439/2022 | `null` | `null` | `null` | `null` | `null` | `GITHUB_FULL_TEXT_BLOCKER`. Exact number/date/title and distinctive phrase search returned no body candidate. |
| PP RF №906/2023 | `null` | `null` | `null` | `null` | `null` | `GITHUB_FULL_TEXT_BLOCKER`. Exact number/date/title and distinctive phrase search returned no body candidate. |

GitHub copies/candidates are not treated as official sources. Body identity, completeness, edition and official status are separate gates.

## New lifecycle/status findings

### 16-ФЗ/2007

- Current consolidated references show edition `04.08.2026`.
- Federal Law 04.08.2026 №325-ФЗ amended articles 1 and 2 of №16-ФЗ. Official-publication pointer corroborated: `0001202608040071`, publication date 04.08.2026.
- A separate earlier amending act, Federal Law 30.01.2026 №13-ФЗ, entered into force **01.09.2026**. It expands the railway transport-security definition to passenger-train rolling stock carrying passengers, baggage, cargo-baggage and/or postal items.
- Classification: `CURRENT_EDITION=2026-08-04` + `CURRENT_EFFECTIVE_LAYER_ACTIVATED_2026-09-01`.
- Gate: `EDITION_DATE != LATEST_EFFECTIVE_DATE`. A current body must include both the 04.08.2026 editorial layer and provisions whose effective date is 01.09.2026.
- Habr version 28.05.2026 necessarily predates both later changes: `POST_HABR_CURRENT_EDITION_ADVANCE`, not an error existing on the article's own version date.
- Direct primary current consolidated card remains `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`; the official publication pointer for №325-ФЗ is corroborated separately.

### PP RF №955/2019

- Current consolidated references continue to label the act as edition `30.04.2021`.
- PP RF 30.04.2021 №685 changed the entry-into-force date in item 2 to `30.10.2022`.
- Original publication is corroborated as 02.08.2019 on the official legal-information portal, but the exact publication pointer ID was not resolved in this pass: `PRIMARY_PUBLICATION_POINTER_BLOCKER`.
- No later amendment/repeal was confirmed; direct primary consolidated current-status verification remains `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.
- Completeness gate: постановление + all 14 points of the approved Requirements. A heading, summary or amendment-only text is not `FULL_TEXT`.

### PP RF №2051/2022

- Current edition is `15.09.2023`; PP RF №1509 amended №2051 and the amended layer entered into force `01.09.2024`.
- The current title/body explicitly includes information contained in `программах обеспечения транспортной безопасности эксплуатантов (транспортных средств)` in addition to plans/passports.
- Habr 28.05.2026 still reproduces the older title without that phrase: `HABR_STALE_TITLE / CURRENT_TITLE_EXPANDED_2023`.
- The act entered into force 01.03.2023 and has a built-in sunset: `BUILT_IN_SUNSET_2029-03-01`.
- A current Rostransnadzor-hosted PDF is a saved ConsultantPlus copy, not an official publication-portal original; therefore `AGENCY_HOSTED_SECONDARY_COPY != OFFICIAL_PUBLICATION`.
- Exact official-publication pointer for PP №1509 was not resolved in this pass: `PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER`.

### Mintrans №439/2022

- Base identity remains: order 28.10.2022 №439, Minjust registration 21.12.2022 №71734.
- Current edition advanced to `02.06.2025` via Mintrans order №178.
- The latest amendment is officially published as `0001202507110007`, publication date 11.07.2025, Minjust registration 04.07.2025 №82814.
- Classification: `CURRENT_EDITION_ADVANCED_2025-06-02` and `PRIMARY_LATEST_AMENDMENT_POINTER_CONFIRMED`.
- Any GitHub copy of the original 2022 text without the 2025 amendment must be `OLD_EDITION`.
- Completeness gate: order + full approved procedure, with the 2025 amendment applied.

### PP RF №906/2023

- Current consolidated references now show edition `07.07.2026`, after PP RF №853.
- №853 changes the accreditation rules, including information concerning presence/absence of foreign-investor control and related accreditation procedure requirements.
- This is a `POST_HABR_CURRENT_EDITION_ADVANCE`: Habr version 28.05.2026 predates the July 2026 amendment.
- PP №906 is directly relevant to PD processing in transport security and has built-in validity through `01.09.2029`: `BUILT_IN_SUNSET_2029-09-01`.
- Exact official-publication pointer for №853 was not resolved in this pass: `PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER`.
- Completeness gate: постановление + complete Rules + all appendices, with №853 changes applied.

## New conflicts / duplicates / blockers

- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `GITHUB_MENTION_ONLY_REJECTED +1`
- `HABR_STALE_TITLE_PP2051 +1`
- `POST_HABR_CURRENT_EDITION_ADVANCE +2` (16-ФЗ, PP №906)
- `CURRENT_EFFECTIVE_LAYER_ACTIVATED_2026-09-01 +1` (16-ФЗ via 13-ФЗ/2026)
- `CURRENT_EDITION_ADVANCED_2025 +1` (Mintrans №439)
- `BUILT_IN_SUNSET_2029 +2` (PP №2051, PP №906)
- `PRIMARY_PUBLICATION_POINTER_BLOCKER +1` (PP №955 exact original pointer)
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER +2` (PP №1509/2023; PP №853/2026)

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `GITHUB_DERIVED_OR_MENTION_REJECTED +1`

## Next boundary

Habr section `Государственная система обнаружения, предупреждения и ликвидации последствий компьютерных атак (ГосСОПКА)`, first federal/high-level layer:

1. Указ Президента РФ от 15.01.2013 №31с (выписка).
2. Выписка из Концепции ГосСОПКА, утв. Президентом РФ 12.12.2014 №К 1274.
3. Указ Президента РФ от 22.12.2017 №620.
4. Постановление Правительства РФ от 17.09.2022 №1636.

After that, the FSB orders in the same Habr section must be deduplicated against acts already processed in the KII lifecycle pass, especially №368/2018, №196/2019, №281/2019 and №282/2019, which were previously confirmed as replaced/repealed by the 2025 successor layer.