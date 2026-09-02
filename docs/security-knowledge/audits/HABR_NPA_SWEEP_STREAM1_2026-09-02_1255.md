# Habr NPA Sweep — Stream 1 — 2026-09-02 12:55 MSK

## Scope

Systematic continuation of Habr 432466, section `Персональные данные. Примеры внутренних документов`, positions 1–6. GitHub copies are evaluated independently from official/legal status. A GitHub object is not treated as an official source merely because it reproduces or links a normative document.

Source boundary from Habr (version 28.05.2026):
1. Рекомендации Роскомнадзора от 27.07.2017 по составлению политики оператора.
2. Методические рекомендации 2010 г. для банковской системы.
3. Приказ Банка России от 22.08.2018 № ОД-2189.
4. Приказ Росфинмониторинга от 06.02.2019 № 30.
5. Приказ Минцифры России от 21.12.2020 № 734.
6. Приказ Роскомнадзора от 15.12.2022 № 201.

## New results

### 1. Рекомендации Роскомнадзора от 27.07.2017

**GitHub full body:** not confirmed.

New GitHub pointer object:
- repo: `seclab-ucr/A4`
- commit: `1cb3fec31d9e5e9eb2fb448e28b11ce3641b72cc`
- path: `rendering_stream/html/rkn.gov.ru.html`
- blob: `da1e8ba35db8482b44fa314d4e2162f9afc43f13`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `HTML`
- classification: `OFFICIAL_SITE_ARCHIVE_HOME_PAGE / POINTER_ONLY / REJECTED_AS_RECOMMENDATIONS_BODY`

Identity/completeness check: the HTML is a captured Roskomnadzor homepage (page date 03.12.2020) and contains the menu link `/personal-data/p908/` with the exact recommendations title. It does **not** contain the recommendations normative/guidance body itself.

Additional pointer-only hits include `netology-code/ibb-homeworks@97b2911fbc6569ce22a420d54688e46cca34a36e`, `02_privacy/README.md`, blob `9db51d4c4eaeb6d124e883717e4dccb711119817`, and `DEVSYS-15/HW@25a15765d332d6dc317ab63a6dd088e675b89360`, same path, blob `584245ac80b244a2a1e7b25de40db28cdf4d477d`. Both only link to the Roskomnadzor page. Blob SHA differs, therefore no byte-duplicate is claimed.

Legal/source status: this is `NON_NPA_RKN_GUIDANCE`. The historical official Roskomnadzor URL is identified, but direct fetch of the old RKN page did not complete in this pass. Keep `PRIMARY_RKN_OLD_PAGE_DIRECT_FETCH_BLOCKER`; do not elevate secondary reproductions to primary status.

### 2. «Методические рекомендации по выполнению законодательных требований при обработке персональных данных в организациях банковской системы РФ» (2010)

**GitHub full body:** not confirmed.
- repo/commit/path/size/type: `null`
- classification: `NON_NPA_BANKING_METHODICAL_GUIDANCE / OUTDATED_GUIDANCE`

Habr itself marks the document outdated while retaining it as an example source. No GitHub full body or reliable body candidate was confirmed in exact-title searches. Direct archival issuer copy/current archival status remains `PRIMARY_ISSUER_ARCHIVE_BLOCKER`.

### 3. Приказ Банка России от 22.08.2018 № ОД-2189

**GitHub full body:** not confirmed.
- repo/commit/path/size/type: `null`

**New confirmed Habr actuality conflict:** the official Bank of Russia document dated 15.05.2025 № ОД-950 is titled `Об утверждении Политики обработки персональных данных в Банке России и отмене приказа Банка России от 22.08.2018 № ОД-2189`. Its operative part approves the new policy and explicitly cancels № ОД-2189.

Classification:
- `HABR_STALE_REPEALED_INTERNAL_ACT`
- `OD-2189_STATUS=CANCELLED`
- `CANCELLED_BY=OD-950_2025-05-15`
- `CURRENT_SUCCESSOR=OD-950`

This conflict is primary-source confirmed by `cbr.ru`; it is not inferred from GitHub.

### 4. Приказ Росфинмониторинга от 06.02.2019 № 30

**GitHub full body:** not confirmed.
- repo/commit/path/size/type: `null`

Exact-number/date/title GitHub search produced no reliable candidate. Secondary full-text legal reproduction confirms target identity and Ministry of Justice registration `№ 55845` dated 06.09.2019, but a direct primary publication card/issuer original was not resolved in this pass.

Classification:
- `GITHUB_FULL_TEXT_BLOCKER`
- `PRIMARY_DIRECT_PUBLICATION_OR_ISSUER_COPY_BLOCKER`

### 5. Приказ Минцифры России от 21.12.2020 № 734

**GitHub full body:** not confirmed.

New GitHub derived object:
- repo: `rinarinarinab/consulting.github.io`
- commit: `44f2fb8d73f17398ce046986bbb744a9f44a2960`
- path: `regulations.html`
- blob: `1a53dc447b1e7182b65045bb55c85478a7098eab`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `HTML`
- classification: `SUMMARY_ONLY / NPA_NAVIGATOR / REJECTED_AS_NORMATIVE_BODY`

Identity check: the internal dialog exactly identifies `Приказ Минцифры ... от 21.12.2020 №734`, reproduces the full target title and a short subject summary. It also contains the historical official publication pointer `http://publication.pravo.gov.ru/Document/View/0001202106010042`. The file is nevertheless only a navigator/summary and not the order body.

Secondary legal reproduction confirms Ministry of Justice registration `№ 63735` dated 01.06.2021. The official publication portal itself is reachable, but a direct document-card fetch for pointer `0001202106010042` was not resolved in this pass. Keep publication pointer and direct primary fetch as separate gates:
- `PUBLICATION_POINTER_FOUND_IN_DERIVED_SOURCE=0001202106010042`
- `PRIMARY_DOCUMENT_CARD_DIRECT_FETCH_BLOCKER`

### 6. Приказ Роскомнадзора от 15.12.2022 № 201

**GitHub full body:** not confirmed.
- repo/commit/path/size/type: `null`

Secondary full-text legal reproductions confirm target identity and contain the order plus attached rules. Habr records Ministry of Justice registration `№ 73374` dated 19.05.2023. No reliable GitHub normative-body candidate was found; searches on exact title/date and registration number produced no target body.

Future GitHub `FULL_TEXT` completeness gate must include the main order and all attached blocks, not merely the first rules: processing rules; internal-control rules; ISPDn list; position list; responsible-person job regulation/duties; physical-room access procedure.

Classification:
- `GITHUB_FULL_TEXT_BLOCKER`
- `PRIMARY_DIRECT_PUBLICATION_OR_RKN_ORIGINAL_BLOCKER`

## Duplicates / conflicts / blockers

- `NEW_GITHUB_FULL_BODY_DUPLICATE = 0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT = 0`
- `NEW_DERIVED_BYTE_DUPLICATE_CONFIRMED = 0`
- `HABR_STALE_REPEALED_INTERNAL_ACT = 1` (`ОД-2189` → cancelled by `ОД-950`, 15.05.2025)
- `GITHUB_POINTER_OR_SUMMARY_REJECTED = 2 distinct principal objects` (`seclab-ucr/A4` RKN homepage archive; `rinarinarinab/consulting.github.io` NPA navigator)
- `GITHUB_FULL_TEXT_CURRENT = 0`
- `RELIABLE_GITHUB_BODY_CANDIDATE = 0`
- `GITHUB_FULL_TEXT_BLOCKER = 6`

## Gate discipline

1. GitHub copy/body status is independent from official publication/current legal status.
2. A link to `publication.pravo.gov.ru` inside GitHub is only a pointer until the official document is fetched/verified separately.
3. For internal departmental documents, an official issuer copy can establish replacement/cancellation even if the Habr entry remains unchanged.
4. Derived policies, training assignments, NPA navigators and archived homepages are not upgraded to `FULL_TEXT`.

## Next boundary

Continue from Habr position 7 in `Персональные данные. Примеры внутренних документов`: Минтранс №141/2023 onward. Keep sector-specific examples separated from the common/core PDn registry, but retain them as implementation examples and trace their supersession/current status independently.
