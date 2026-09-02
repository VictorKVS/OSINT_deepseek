# Habr NPA sweep — Stream 1 — 2026-09-02 21:56 MSK

Source boundary: Habr 432466, current page title `Справочник законодательства РФ в области информационной безопасности (версия 28.05.2026)`, section `Банковская безопасность. Нормативно-правовые акты Банка России`, positions 13–18.

Method: GitHub copies are discovery/evidence objects only and are never promoted to official sources automatically. For each target, GitHub body identity/completeness and legal status are evaluated separately. Primary/current status is checked against Bank of Russia official publication/operational pages where available.

## 13. Bank of Russia Regulation No. 440-P dated 2014-11-06
Target title: `О порядке направления в банк отдельных документов налоговых органов, а также направления банком в налоговый орган отдельных документов банка в электронной форме в случаях, предусмотренных законодательством Российской Федерации о налогах и сборах`.

GitHub discovery:
- repo: `dbarabo/observer`
- commit: `6667896ff0b865a444e327cffba1ac5465479de4`
- path: `src/main/kotlin/ru/barabo/observer/config/barabo/p440/P440Config.kt`
- blob: `e9404b077a6e739562fbdad1e0f7c816782db8c8`
- size: `847 B`
- type: `Kotlin/text`
- identity check: target number `440-П` present; target date/title/Minjust registration and normative body absent.
- classification: `OPERATIONAL_INTEGRATION_CODE / TARGET_NUMBER_ONLY / REJECTED_AS_NORMATIVE_BODY`.
- related same-repo operational files form `DERIVED_IMPLEMENTATION_CLUSTER`, not normative duplicates.

Primary lifecycle:
- Bank of Russia Instruction No. 6952-U dated 2024-11-25 enters into force on `2026-01-01` and explicitly recognizes 440-P as invalid from that date.
- classification: `HABR_STALE_REPEALED_BANK_ACT / REPEALED_BY_6952-U / REPEAL_EFFECTIVE_2026-01-01 / DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`.
- Bank of Russia still exposes a legacy 440-P formats block alongside the 6952-U formats on the current FNS exchange page. This is an operational compatibility/reference layer, not restoration of legal force: `PRIMARY_SITE_LEGACY_OPERATIONAL_REFERENCE`.
Primary locators:
- https://www.cbr.ru/Queries/XsltBlock/File/87500/-1/2546
- https://www.cbr.ru/development/feddc/fns/

## 14. Bank of Russia Instruction No. 3893-U dated 2015-12-11
GitHub discovery:
- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- result: `GITHUB_FULL_TEXT_BLOCKER`.

Primary status:
- original identity/publication confirmed by Bank of Russia; Minjust registration No. 41021.
- current Bank of Russia CKKI pages continue to instruct users to submit requests through a credit institution under 3893-U; current operational reference is confirmed.
- classification: `PRIMARY_CURRENT_OPERATIONAL_REFERENCE_CONFIRMED / FORMAL_CURRENT_STATUS_FLAG_BLOCKER` (operational use is not treated as a standalone formal status flag).
Primary locators:
- https://www.cbr.ru/ckki/zaprosy_v_ckki/request_2/
- https://www.cbr.ru/Publ/Vestnik/ves160220016.pdf

## 15. Bank of Russia Instruction No. 4212-U dated 2016-11-24
GitHub discovery:
- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- result: `GITHUB_FULL_TEXT_BLOCKER`.

Lifecycle:
- Instruction No. 4927-U dated 2018-10-08 entered into force on `2019-01-01` and its clause 3 recognizes 4212-U and its amendments as invalid from that date.
- classification: `HABR_STALE_REPEALED_BANK_ACT / REPEALED_BY_4927-U / REPEAL_EFFECTIVE_2019-01-01 / DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`.
- Habr later lists 4927-U separately (position 21), creating a lifecycle duplication if both are ingested without status normalization.

## 16. Bank of Russia Regulation No. 579-P dated 2017-02-27
GitHub discovery:
- repo: `Sparky324/AI_mail_analyze`
- commit: `6582b89dba65c5a1ea1ac41e4f6227dbf9e0a028`
- path: `data_simple/normativ.txt`
- blob: `e144cb0aca3d1d0acae8b3b6663f8df190a175a8`
- size: `11127 B`
- type: `text/plain`
- content: compact banking regulatory notes/list; mentions `579-П`, but is not the complete target act and does not reproduce the target normative package.
- classification: `SUMMARY_LIST / MENTION_ONLY / REJECTED_AS_NORMATIVE_BODY`.

Primary lifecycle:
- Regulation No. 809-P dated 2022-11-24 entered into force on `2023-01-01`; its clause 3 explicitly recognizes 579-P and its amendment chain as invalid from that date.
- classification: `HABR_STALE_REPEALED_BANK_ACT / REPEALED_BY_809-P / REPEAL_EFFECTIVE_2023-01-01 / DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`.
Primary locator:
- https://www.cbr.ru/Queries/XsltBlock/File/105012/-1/2400-2401

## 17. Bank of Russia Instruction No. 4512-U dated 2017-08-30
GitHub discovery:
- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- result: `GITHUB_FULL_TEXT_BLOCKER`.

Primary status:
- Bank of Russia FNS/data-exchange page, last updated `2026-03-10`, still provides rules/XSD expressly under 4512-U.
- classification: `PRIMARY_CURRENT_OPERATIONAL_REFERENCE_CONFIRMED_2026-03-10 / FORMAL_CURRENT_STATUS_FLAG_BLOCKER`.
Primary locator:
- https://www.cbr.ru/development/feddc/fns/

## 18. Bank of Russia Regulation No. 600-P dated 2017-09-20
GitHub discovery:
- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- result: `GITHUB_FULL_TEXT_BLOCKER`.

New post-Habr lifecycle layer:
- Bank of Russia Instruction No. `7310-U` dated `2026-03-25` was officially published by the Bank of Russia on `2026-08-21`.
- It is not yet effective. It enters into force on `2027-04-01` and from that date explicitly recognizes 600-P and amending Instruction No. 5768-U as invalid.
- therefore 600-P must NOT be retired as of 2026-09-02; instead record a future replacement layer: `SIGNED_PUBLISHED_FUTURE_REPLACEMENT_7310-U / FUTURE_REPEAL_600-P_EFFECTIVE_2027-04-01 / DO_NOT_RETIRE_BEFORE_2027-04-01`.

New primary metadata conflict:
- the Bank of Russia official-publication listing currently displays `Registration in Minjust No. 87861 from 25.03.2026` for 7310-U, while legal-text reproductions and legal-reference systems identify Minjust registration as `No. 87861 dated 14.08.2026`.
- because `25.03.2026` is the issue date of 7310-U and conflicts with independent registration metadata, classify as `PRIMARY_SITE_REGISTRATION_DATE_METADATA_CONFLICT`; do not silently normalize without preserving the conflict.
Primary/verification locators:
- https://www.cbr.ru/analytics/na_vr/
- secondary full-text verification: ConsultantPlus/other legal systems reproduce clause 6 (effective 2027-04-01), clause 7 (future repeal of 600-P), and Minjust registration No. 87861 dated 2026-08-14.

## Delta counters
- `GITHUB_FULL_TEXT_CURRENT +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `DERIVED_IMPLEMENTATION_CLUSTER +1`
- `SUMMARY_OR_MENTION_REJECTED +1`
- `HABR_STALE_REPEALED_BANK_ACT +3` (440-P, 4212-U, 579-P)
- `PRIMARY_REPEAL_CONFIRMED +3`
- `PRIMARY_CURRENT_OPERATIONAL_REFERENCE_CONFIRMED +2` (3893-U, 4512-U)
- `SIGNED_PUBLISHED_FUTURE_REPLACEMENT +1` (7310-U -> 600-P)
- `PRIMARY_SITE_REGISTRATION_DATE_METADATA_CONFLICT +1` (7310-U)
- `PRIMARY_SITE_LEGACY_OPERATIONAL_REFERENCE +1` (440-P formats retained)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_BODY_IDENTITY_CONFLICT +0`

Next boundary: Habr banking-security position 19 onward (`ИН-03-13/40`, then 4926-U, 4927-U, 655-P, 4933-U, 5039-U). Keep letters/information letters as non-NPA guidance unless their legal nature proves otherwise.