# Habr NPA sweep — Stream 1 — 2026-09-01 18:55 MSK

## Scope

Habr 432466, section `Топливно-энергетический комплекс (ТЭК)`, positions 1–5:

1. Федеральный закон от 21.07.2011 № 256-ФЗ «О безопасности объектов топливно-энергетического комплекса».
2. Постановление Правительства РФ от 02.03.2017 № 244 «О совершенствовании требований к обеспечению надежности и безопасности электроэнергетических систем и объектов электроэнергетики и внесении изменений в некоторые акты Правительства Российской Федерации».
3. Приказ Минэнерго России от 06.11.2018 № 1015 «Об утверждении требований в отношении базовых (обязательных) функций и информационной безопасности объектов электроэнергетики при создании и последующей эксплуатации на территории Российской Федерации систем удаленного мониторинга и диагностики энергетического оборудования».
4. Письмо Минэнерго России от 29.06.2021 № НШ-7491/07 «О базовой модели угроз безопасности информации в интеллектуальных системах учета электрической энергии (мощности)».
5. Приказ Минэнерго России от 31.10.2025 № 1429 «Об утверждении Порядка раскрытия (предоставления) цифровых информационных моделей электроэнергетических систем и цифровых информационных моделей объектов электроэнергетики или их фрагментов и о внесении изменений в приказ Минэнерго России от 17 февраля 2023 г. № 82», Минюст № 84397 от 01.12.2025.

Habr source: https://habr.com/ru/articles/432466/

## GitHub body/candidate audit

| Target | repo | commit/ref | path | size | type | Result |
|---|---|---|---|---:|---|---|
| 256-ФЗ/2011 | `edekeulenaar/global-digital-regulations` | `633e8261d64910a2dc8913a1cfd8faa7fe78314c` | `data/policies/2251.md` | `UNRESOLVED_CONNECTOR_METADATA` | Markdown/text | `AMENDING_ACT_MENTION / REJECTED_AS_TARGET_BODY`. Blob `003ef89a0f41150f074392328819a7c29b78bab6`. Internal body identity is Federal Law 06.07.2016 №374-ФЗ, not №256-ФЗ. |
| PP RF №244/2017 | `null` | `null` | `null` | `null` | `null` | `GITHUB_FULL_TEXT_BLOCKER` |
| Minenergo №1015/2018 | `leaalex/extended_problem` | `266e9409441b7d55ebc57cd7054941d122f7b20e` | `Кибербезопасность в энергетике/Таблички/3.2.html` | `9128 B` | HTML/Open edX problem | `MENTION_ONLY / EDUCATIONAL_MATCHING_EXERCISE / REJECTED_AS_NORMATIVE_BODY`. Blob `43ee1d0fc47b7674b6235806d15579f5e3875d57`. Exact number/date/title are present only as an answer option. |
| Letter №НШ-7491/07/2021 | `null` | `null` | `null` | `null` | `null` | `GITHUB_FULL_TEXT_BLOCKER` |
| Minenergo №1429/2025 | `null` | `null` | `null` | `null` | `null` | `GITHUB_FULL_TEXT_BLOCKER` |

GitHub copies are treated only as copies/candidates. They are not promoted to official sources without a separate primary-source check.

## New lifecycle/status findings

### 256-ФЗ

- Current consolidated references found in this pass show edition `25.05.2026`.
- Latest confirmed amending act: Federal Law 25.05.2026 №151-ФЗ «О внесении изменений в Федеральный закон “О безопасности объектов топливно-энергетического комплекса” и отдельные законодательные акты Российской Федерации».
- Official-publication pointer corroborated: `0001202605250034`, publication date 25.05.2026, 16 pages.
- Direct primary publication card was not reliably resolved in this pass: `PRIMARY_DIRECT_FETCH_BLOCKER`.
- A current Rosgvardia regional control-reference page still labels №256-ФЗ as edition `28.06.2022`, while current consolidated sources show `25.05.2026`: `PRIMARY_AGENCY_REFERENCE_LIST_STALE_VERSION`.
- Gate: a GitHub body earlier than 25.05.2026 cannot be `FULL_TEXT_CURRENT` even if complete for its historical edition.

### PP RF №244/2017

- Current consolidated references found in this pass label the act as edition `27.12.2024`.
- The 27.12.2024 change layer is tied to PP RF №1937. Its later 14.02.2026 amendment does not by itself imply a newer edition date for №244; the change to №244 remains the 27.12.2024 layer.
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER` remains because a directly readable primary consolidated card was not resolved.
- Completeness gate: a GitHub copy must include the full постановление and all amendment provisions, not only the heading/summary.

### Minenergo №1015/2018

- Identity corroborated: Minjust registration `15.02.2019 №53815`.
- Official publication pointer corroborated from the Habr official link / saved publication reference: `0001201902180013`, publication date 18.02.2019.
- Direct primary portal access remains unstable: `PRIMARY_DIRECT_FETCH_BLOCKER`.
- No newer amendment/repeal was confirmed in this pass; absence of a finding is not promoted to proof of current status: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.
- Completeness gate: order + entire approved Requirements appendix.

### Letter №НШ-7491/07/2021 / base threat model

- Habr still points to the 29.06.2021 letter/model layer.
- The old Minenergo Habr-linked URL currently returns 404: `PRIMARY_2021_MINENERGO_LINK_BROKEN`.
- Minenergo currently hosts an official PDF for the updated base threat model attached to letter `11.12.2024 №СЦ-21040/07`; the PDF contains a 294-page threat-model appendix and explicitly states that changes were made to the base model developed under PP RF №890/2020.
- Classification: `HABR_STALE_GUIDANCE_VERSION / BASE_THREAT_MODEL_UPDATED_2024`.
- This is ministry guidance/information material, not a registered NPA.
- Formal withdrawal of the 2021 letter was not confirmed: `FORMAL_WITHDRAWAL_OF_2021_LETTER_NOT_CONFIRMED`.

Primary current model: https://minenergo.gov.ru/upload/iblock/36f/Bazovaya-model-ugroz-_s-izmeneniyami-ot-11.12.2024_.pdf

### Minenergo №1429/2025

- Identity/registration corroborated: order 31.10.2025 №1429, Minjust 01.12.2025 №84397.
- Registered-text copies state entry into force `01.03.2026` and built-in validity through `01.03.2032`.
- `BUILT_IN_SUNSET_2032-03-01` recorded.
- Exact official publication pointer was not resolved in this pass: `PRIMARY_PUBLICATION_POINTER_BLOCKER`.
- Direct primary consolidated current-status card was not resolved: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.
- Completeness gate: full approved disclosure procedure + all amendment provisions to Minenergo order №82/2023.

## New conflicts / duplicates / blockers

- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `GITHUB_DERIVED_OR_MENTION_REJECTED +2`
- `PRIMARY_AGENCY_REFERENCE_LIST_STALE_VERSION +1`
- `HABR_STALE_GUIDANCE_VERSION +1`
- `PRIMARY_2021_MINENERGO_LINK_BROKEN +1`
- `BUILT_IN_SUNSET_2032-03-01 +1`

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `CURRENT_EDITION_ADVANCED_256FZ_2026-05-25 +1`

## Next boundary

Habr section `Транспорт`, beginning with:

1. Federal Law 09.02.2007 №16-ФЗ «О транспортной безопасности».
2. PP RF 24.07.2019 №955.
3. PP RF 14.11.2022 №2051.
4. Mintrans order 28.10.2022 №439.
5. PP RF 01.06.2023 №906.

The next pass should preserve the same gates: GitHub body identity separately from primary-source official/current status, and full-text completeness separately from mentions/summaries.