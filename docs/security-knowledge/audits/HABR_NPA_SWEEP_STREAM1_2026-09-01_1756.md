# Habr NPA sweep — Stream 1 — 2026-09-01 17:56 MSK

## Scope

Continuation of Habr 432466 systematic sweep.

Processed unique targets in this pass:

1. KII #50 — FSTEC methodical document dated 11.11.2025, methodology for evaluating the state of technical protection of information and security of significant KII objects.
2. KII #51 — Rosatom Order dated 20.03.2026 No. 1/9-NPA.
3. KII. Communications #2 — Ministry of Digital Development Order dated 28.12.2020 No. 777.
4. KII. Communications #3 — Ministry of Digital Development Order dated 28.12.2020 No. 779.
5. KII. Communications #4 — Association of Documentary Telecommunications methodical recommendations dated 26.06.2019 on categorization of KII in communications.
6. KII. Communications #5 — Ministry of Digital Development list of typical sectoral KII objects in communications, approved 05.02.2024 No. 2226vn.
7. KII. Communications #6 — Ministry of Digital Development methodical instructions on categorization in communications, approved 04.04.2025 No. ASH-7089vn.

KII. Communications #1 (Ministry of Communications Order No. 114/2020) is a cross-section duplicate reference already processed in an earlier pass; it was not recounted as a new target.

## GitHub findings

| Target | repo | commit/ref | path | size | type | result |
|---|---|---|---|---:|---|---|
| FSTEC method 11.11.2025 | `ale88andr/obs-vault` | `7c3b5dfa92bde4382d3148b9b16131080718c281` | `copilot/copilot-conversations/agent__Расчёт_Кзи_(6_мес.),_Пзи_(2_года),_отправка_в@20260825_054922.md` | 29167 B | Markdown | `MENTION_ONLY / AI_SESSION_SUMMARY / REJECTED_AS_NORMATIVE_BODY` |
| FSTEC predecessor method 02.05.2024 | `evsrt/evsrt.github.io` | `88e58f8c443b3b48b53caca10ff4c2427c303b27` | `docs/gov.md` | 984 B | Markdown | `OLD_PREDECESSOR_LINK_ONLY / NOT_TARGET_BODY` |
| Rosatom 1/9-NPA/2026 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| MinDigital No. 777/2020 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| MinDigital No. 779/2020 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ADT recommendations 26.06.2019 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| MinDigital No. 2226vn/2024 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| MinDigital No. ASH-7089vn/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

GitHub blob metadata confirmed:

- `ale88andr/obs-vault` AI conversation blob: `1dab5f40017499aff55fbb1d5c059582275d4184`, size 29167 B.
- `evsrt/evsrt.github.io/docs/gov.md` blob: `4b350c78afc68926cb9235f6fc8d5faba52be859`, size 984 B.

No GitHub copy in this pass is promoted to official status.

## Identity, lifecycle and status findings

### FSTEC methodical document 11.11.2025

Official FSTEC index confirms the document dated 11.11.2025. The official FSTEC page lists attachments, but direct page fetch was unavailable during this pass.

The new methodology expressly states that, due to approval of the new methodology, the FSTEC methodology approved on 02.05.2024 is not applied for this evaluation. Therefore:

- `OLD_METHOD_EXPLICITLY_NOT_APPLIED = 02.05.2024`
- `CURRENT_METHODICAL_LAYER = 11.11.2025`
- `NON_NPA_METHODICAL_DOCUMENT`
- `PRIMARY_REGULATOR_DIRECT_FETCH_BLOCKER`

The GitHub AI-session file correctly mentions the 11.11.2025 replacement but is derivative content, not the methodical document body.

### Rosatom Order 20.03.2026 No. 1/9-NPA

Official publication pointer confirmed: `0001202605210004`; publication/registration date 21.05.2026, Ministry of Justice registration No. 86551.

Identity matches Habr: Rosatom, 20.03.2026, No. 1/9-NPA, procedure and criteria concerning relevance/reliability of KII-subject information.

Completeness gate:

`FULL_TEXT_1_9_NPA_REQUIRES_ORDER_PLUS_FULL_PROCEDURE_PLUS_FULL_CRITERIA`

The official publication card could not be fetched directly in this pass, so:

- `OFFICIAL_PUBLICATION_POINTER_CONFIRMED`
- `PRIMARY_DIRECT_FETCH_BLOCKER`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`

### MinDigital Order 28.12.2020 No. 777

Exact number/date/title confirmed by legal-system copies. The approved material is recommendations for certification of communications equipment used at significant KII objects.

Classification:

- `MINISTRY_RECOMMENDATIONS / NON_NPA_GUIDANCE`
- `PRIMARY_MINCIFRY_ORIGINAL_BLOCKER`
- `CURRENT_STATUS_NOT_PRIMARY_CONFIRMED`

No GitHub full body was found.

### MinDigital Order 28.12.2020 No. 779

The official Ministry of Digital Development index confirms No. 779 dated 28.12.2020 and the exact title on organizational and technical measures for information security of public communications-network resources.

Direct official page fetch was unavailable. Registration/non-registration status in the Ministry of Justice was not resolved in this pass; it is not promoted to a registered NPA automatically.

Classification:

- `PRIMARY_MINCIFRY_INDEX_CONFIRMED`
- `PRIMARY_MINCIFRY_DIRECT_FETCH_BLOCKER`
- `MINJUST_REGISTRATION_OR_NONREGISTRATION_STATUS_BLOCKER`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`

### ADT methodical recommendations 26.06.2019

Existence/date/title are corroborated, but the issuer is a non-state association. No reliable GitHub body and no directly fetched issuer original were resolved.

Classification:

- `PRIVATE_SECTOR_METHODICAL_RECOMMENDATIONS / NON_NPA`
- `LEGACY_PRIVATE_GUIDANCE`
- `ISSUER_ORIGINAL_2019_DIRECT_FETCH_BLOCKER`
- `FORMAL_WITHDRAWAL_NOT_CONFIRMED`

The document must not be stored in the same legal-status class as Ministry/Government acts.

### MinDigital typical-sector list No. 2226vn dated 05.02.2024

The official Ministry of Digital Development index confirms the list of typical sectoral KII objects in communications.

Current legal framework has advanced: Government Order No. 360-r dated 26.02.2026, current confirmed edition 27.05.2026, contains a centralized list with a dedicated communications section. Therefore:

- `LEGACY_SECTORAL_LIST_LAYER`
- `SUPERSEDED_IN_SUBJECT_MATTER_BY_GOVERNMENT_LIST_360_R_2026`
- `FORMAL_WITHDRAWAL_NOT_CONFIRMED`
- `PRIMARY_MINCIFRY_DIRECT_FETCH_BLOCKER`

A future GitHub copy of 2226vn must not be treated as the current authoritative list merely because it is complete.

### MinDigital methodical instructions No. ASH-7089vn dated 04.04.2025

The official Ministry of Digital Development index confirms No. ASH-7089vn and the categorization methodology for communications-sector KII. Secondary full copies show a multi-annex structure, including treatment of typical sectoral objects and calculation guidance.

As of 01.09.2026, Government Resolution No. 402 dated 13.04.2026 is effective and establishes binding sectoral categorization features through 01.09.2032, while Government Order No. 360-r supplies the current centralized list. Therefore:

- `NON_NPA_METHODICAL_GUIDANCE`
- `PRE_BINDING_GUIDANCE_LAYER`
- `USE_ONLY_IF_CONSISTENT_WITH_PP402_AND_360R`
- `GUIDANCE_LEGAL_FRAMEWORK_ADVANCED_2026_09_01`
- `FORMAL_WITHDRAWAL_NOT_CONFIRMED`
- `PRIMARY_MINCIFRY_DIRECT_FETCH_BLOCKER`

No automatic repeal is asserted: the relation is legal-framework advancement/subordination unless a formal withdrawal act is found.

## New Habr structural conflict

Ministry of Communications Order No. 114/2020 appears again as KII. Communications #1 although it was already present/processed in the broader KII sweep. Record as:

`HABR_CROSS_SECTION_DUPLICATE_REFERENCE +1`

In addition, Habr places legacy/private/sector guidance (2019, 2024, 2025) beside newer binding 2026 Government rules without a lifecycle edge. Record as:

`HABR_CROSS_SECTION_LIFECYCLE_LAYERING_CONFLICT +1`

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `GITHUB_MENTION_ONLY_REJECTED +1`
- `GITHUB_OLD_PREDECESSOR_LINK_ONLY +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `OLD_METHOD_EXPLICITLY_NOT_APPLIED +1`
- `HABR_CROSS_SECTION_DUPLICATE_REFERENCE +1`
- `HABR_CROSS_SECTION_LIFECYCLE_LAYERING_CONFLICT +1`
- `LEGACY_SECTORAL_LIST_LAYER +1`
- `GUIDANCE_LEGAL_FRAMEWORK_ADVANCED_2026_09_01 +1`

## Blockers

1. Direct FSTEC page/attachments for method 11.11.2025 did not resolve in the direct fetch path, although the official index is present.
2. Direct official publication card for Rosatom 1/9-NPA timed out; publication pointer is confirmed separately.
3. Direct Ministry of Digital Development pages for several communications-sector materials were unavailable during the pass despite indexed official pages.
4. No GitHub full body/reliable full-text candidate was found for any of the seven unique targets.
5. Formal withdrawal acts were not found for the 2019 association recommendations, 2226vn/2024, or ASH-7089vn/2025; therefore no repeal edge is created.

## Next boundary

Continue after `Критическая информационная инфраструктура. Связь` into the Habr section `Топливно-энергетический комплекс (ТЭК)`, prioritizing federal laws, Government acts and regulator documents, while preserving the same separation between NPA, regulator guidance, sector/private recommendations, and GitHub copies.