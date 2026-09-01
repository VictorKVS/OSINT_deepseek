# Habr NPA sweep — Stream 1 — 2026-09-01 14:55 MSK

## Scope

Continued Habr 432466, KII positions 29–34:

1. FSTEK information message 04.05.2018 No. 240/22/2339.
2. FSTEK information message 24.08.2018 No. 240/25/3752.
3. FSTEK information message 17.04.2020 No. 240/84/611.
4. FSTEK information message 28.04.2023 No. 240/82/818.
5. FSTEK information message 27.05.2024 No. 240/82/1376.
6. FSTEK information message 12.08.2024 No. 240/83/2028.

These records are classified as `REGULATOR_GUIDANCE / INFORMATION_MESSAGE`, not registered NPA. A GitHub copy, if found, must not be treated as an official source automatically.

## GitHub search result

Exact searches by number/date/title and distinctive phrases produced no target normative/guidance body for all six records.

| target | repo | commit | path | size | type | result |
|---|---|---|---|---:|---|---|
| 240/22/2339 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| 240/25/3752 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| 240/84/611 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| 240/82/818 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| 240/82/1376 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| 240/83/2028 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

Broad GitHub results for the 2339 title/phrases were unrelated study/data files and were rejected. No new full-body duplicate and no new body-identity conflict were found.

## New confirmed findings

### 240/22/2339 — historical transition guidance, not a current substitute for the 2021 threat methodology

The reproduced body confirms that FSTEK declared the 2007 General Requirements and Recommendations for key systems invalid by director decision dated 03.05.2018. It allowed the 18.05.2007 Base Threat Model and threat-determination methodology to be used for significant KII objects only **until FSTEK approved corresponding methodological documents**.

FSTEK's Methodical Document `Methodology for Information Security Threat Assessment`, approved 05.02.2021, expressly applies to significant KII objects. Therefore the transitional allowance in message 240/22/2339 must not be treated as a perpetual current methodological basis.

Classification:
- `HISTORICAL_TRANSITION_GUIDANCE`
- `TRANSITIONAL_ALLOWANCE_SUBJECT_MATTER_SUPERSEDED_BY_FSTEK_METHOD_2021`
- `FORMAL_WITHDRAWAL_OF_MESSAGE_NOT_CONFIRMED`

Gate: `TRANSITIONAL_ALLOWANCE_UNTIL_NEW_METHOD != PERPETUAL_CURRENT_GUIDANCE`.

Sources:
- Habr source list: https://habr.com/ru/articles/432466/
- reproduced body: https://www.garant.ru/products/ipo/prime/doc/71857568/
- 2021 methodology text: https://digital.gov-dpr.ru/upload/iblock/08e/9hlybfdvbc7vfsorv9moj0t2mp28vfg2/%D0%9D%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%20%D0%9C%D0%95%D0%A2%D0%9E%D0%94%D0%98%D0%9A%D0%90%20%D0%9E%D0%A6%D0%95%D0%9D%D0%9A%D0%98%20%D0%A3%D0%91%D0%98%20%D0%BE%D1%82%205%20%D1%84%D0%B5%D0%B2%D1%80%D0%B0%D0%BB%D1%8F%202021%20%D0%B3.pdf

### 240/25/3752 vs 240/84/611 — confirmed guidance-version conflict in electronic formats

The 2018 message recommends attaching electronic copies in `docx/xlsx`. The 2020 message, reflecting the then-current Rules and Order No. 59/2019, states that lists are submitted electronically as `.ods` and/or `.odt`, while categorization results use `.ods`.

Thus Habr contains two historical guidance snapshots with different electronic-format instructions. They must not be flattened into simultaneous current requirements.

Classification:
- `GUIDANCE_VERSION_CONFLICT_CONFIRMED`
- `LEGACY_SUBMISSION_GUIDANCE_2018`
- `LEGACY_SUBMISSION_GUIDANCE_2020`

Gate: `OLDER_INFORMATION_MESSAGE_FORMAT != CURRENT_REQUIREMENT`.

Sources:
- 2018 body: https://www.garant.ru/products/ipo/prime/doc/71935164/
- 2020 preserved page/body: https://hub.zlonov.ru/laws/%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F-%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A-%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8/%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B5-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A-%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%E2%84%96240-84-611-%D0%BE%D1%82-17.04.2020

### Submission form advanced in 2025

FSTEK Order No. 247 dated 11.07.2025 amended the form approved by Order No. 236. It was registered by the Ministry of Justice under No. 83246, officially published 21.08.2025 as publication No. `0001202508210016`, and entered into force 01.09.2025. The later FSTEK information message No. 240/84/3451 dated 22.10.2025 clarifies filling/updating the amended form.

Therefore old 2018/2020 guidance cannot be used as the authoritative source for the **current form fields**. Message 240/82/1376 of 27.05.2024 also represents a pre-2025 form-version layer: its procedural point about updating data may remain relevant, but its references must be applied against the amended current form.

Classification:
- `CURRENT_FORM_ADVANCED_2025-09-01`
- `OLD_GUIDANCE_FORM_REFERENCE_LAYER`
- `240/82/1376 = PARTIALLY_STALE_REFERENCE_LAYER / FORM_VERSION_ADVANCED_2025`

Official publication index:
- https://publication.pravo.gov.ru/documents/block/foiv041
- publication No. `0001202508210016`, 21.08.2025, 162 KB / 5 pages.

Later guidance:
- https://hub.zlonov.ru/laws/reviews/2025-10-USSC-review

### 240/82/818 — scope is communications-sector routing

The preserved body shows that the message is not a general all-sector routing rule. It addresses KII subjects operating in the **communications sector**: central FSTEK apparatus reviews specified federal/subordinate bodies and communications organizations operating in two or more RF subjects; other communications KII subjects are routed to the territorial FSTEK administration for the relevant federal district.

Classification:
- `SECTOR_SPECIFIC_GUIDANCE / COMMUNICATIONS`
- `CONTENT_SCOPE_NARROWER_THAN_GENERIC_TITLE`

A later general routing information message No. 240/82/672 dated 12.03.2025 exists and states that the reviewing FSTEK structure depends on the category of KII subject. No explicit primary-source withdrawal/supersession clause for 240/82/818 was confirmed in this run, so no repeal/supersession edge is asserted yet.

Source:
- https://hub.zlonov.ru/laws/%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F-%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A-%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8/%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B5-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A-%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%E2%84%96240-82-818-%D0%BE%D1%82-28.04.2023
- later-routing notice: https://ib-bank.ru/bisjournal/reader/136

### 240/83/2028 — scope is chemical-industry routing

The preserved body confirms that this message applies to KII subjects in the **chemical industry**. Central FSTEK reviews specified federal/subordinate organizations and organizations owning 15 or more KII objects; other chemical-industry subjects are routed to the territorial FSTEK administration.

Classification:
- `SECTOR_SPECIFIC_GUIDANCE / CHEMICAL_INDUSTRY`
- `CONTENT_SCOPE_NARROWER_THAN_GENERIC_TITLE`

No explicit primary-source withdrawal/supersession clause was confirmed in this run.

Source:
- https://hub.zlonov.ru/laws/%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F-%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A-%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8/%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE%D0%B5-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A-%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%E2%84%96240-83-2028-%D0%BE%D1%82-12.08.2024

## Primary-source blockers

Habr points these six records to FSTEK resources, but direct FSTEK pages/PDFs were unavailable or timed out in this run. Consequently:

- `PRIMARY_REGULATOR_DIRECT_FETCH_BLOCKER +6`
- preserved copies are corroboration, not primary official status evidence;
- because these are information messages rather than registered NPA, absence of a `publication.pravo.gov.ru` registration is not treated as a defect.

No formal withdrawal was asserted for messages 240/25/3752, 240/84/611, 240/82/818, 240/82/1376, or 240/83/2028 without an explicit regulator act/message.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `GUIDANCE_VERSION_CONFLICT_CONFIRMED +1`
- `HISTORICAL_TRANSITION_GUIDANCE +1`
- `CURRENT_FORM_ADVANCED_2025-09-01 +1`
- `SECTOR_SPECIFIC_GUIDANCE_SCOPE_CONFIRMED +2`
- `PRIMARY_REGULATOR_DIRECT_FETCH_BLOCKER +6`

## Next boundary

Continue KII positions 35+ from Habr: sectoral methodical recommendations / typical KII object lists, then Mincomsvyaz and Mincifra orders in the KII block. Keep `NPA`, `methodical document`, `sectoral guidance`, `typical-object list`, and `information message` as separate document classes.