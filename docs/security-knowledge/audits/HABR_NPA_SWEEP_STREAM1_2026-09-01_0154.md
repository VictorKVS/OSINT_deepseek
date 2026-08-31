# Habr NPA sweep — Stream 1

Date boundary: 2026-09-01 (Europe/Moscow)

Scope: Habr 432466, section «Государственные и муниципальные информационные системы (ГИС и МИС)», positions 16–21. Targets: ПП РФ 10.07.2013 №584; ПП РФ 31.07.2014 №747; распоряжение Правительства РФ 29.12.2014 №2769-р; ПП РФ 06.07.2015 №675; ПП РФ 06.07.2015 №676; ПП РФ 14.11.2015 №1235. GitHub copies are non-official discovery candidates only. Currentness and official provenance are tracked independently.

## Normalized GitHub result

| Target | GitHub normative candidate | Classification |
|---|---|---|
| ПП РФ 10.07.2013 №584 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 31.07.2014 №747 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| Распоряжение Правительства РФ 29.12.2014 №2769-р | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 06.07.2015 №675 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 06.07.2015 №676 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 14.11.2015 №1235 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |

No GitHub result passed the full-body + internal number/date/title identity gate.

## New rejected GitHub hits

| Target | repo | commit | path | size | type | result |
|---|---|---|---|---:|---|---|
| ПП №676/2015 | hbktq98brn-stack/dashbord | 1bd1540fa6ca1bd72a18811b57db6873ef2cc651 | src/components/NormativeDocs.jsx | 25820 | JSX | MENTION_ONLY / MOCK_UI_DATA / REJECTED_AS_NORMATIVE_BODY |
| ПП №676/2015 | ale88andr/obs-vault | 7c3b5dfa92bde4382d3148b9b16131080718c281 | InfoSec/Законодотельство ИБ/Основные законодательные акты.md | 17780 | Markdown | MENTION_ONLY / STUDY_NOTES / REJECTED_AS_NORMATIVE_BODY |

The first file is mock React card data; the second is an InfoSec study note. Neither contains the normative body.

## Currentness / lifecycle findings

### ПП РФ №584 от 10.07.2013

Current corroborated edition advanced to 03.04.2026. ПП РФ 03.04.2026 №372 directly changes the Rules approved by №584. Government.ru indexes №372 as a Government act dated 03.04.2026. №372 has staggered effective dates for some of its own provisions; this must not be flattened into one effective-date flag.

Status: `CURRENT_EDITION_2026-04-03_CORROBORATED / LATEST_AMENDMENT_PRIMARY_GOVERNMENT_INDEX_CONFIRMED`.

Completeness gate: `FULL_TEXT` for №584 means the resolution plus the complete current Rules; old copies that still contain superseded registration provisions are `STALE_EDITION`, even if the original 2013 text is complete.

### ПП РФ №747 от 31.07.2014

Current secondary legal card still shows the original 31.07.2014 edition as effective. No repeal or later amendment was confirmed in this pass.

Status remains strict: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER` — absence of a found repeal is not primary proof of currentness.

Completeness gate: resolution + complete approved list of personal/family/household needs.

### Распоряжение Правительства РФ №2769-р от 29.12.2014

Latest corroborated edition remains 18.10.2018. No later amendment/repeal was confirmed in this pass.

Status: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

Completeness gate: распоряжение + full attached Concept of regional informatization.

### ПП РФ №675 от 06.07.2015 — effective body changes on 01.09.2026

ПП РФ 04.07.2026 №845 enters into force on 01.09.2026 and directly amends №675. It adds a third approved Rules block: control over compliance by operators of state/municipal and specified procurement-related information systems with requirements preventing use, during system operation, of databases and technical means located outside the Russian Federation and not part of such systems.

Therefore the old edition 25.09.2018 ceases to be the current effective body from 01.09.2026.

New classification: `CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01 / HABR_ATTACHMENT_SET_STALE_2026-09-01`.

New completeness gate: `FULL_TEXT` for current №675 now requires the resolution + all THREE approved Rules blocks. A copy with only the two historical Rules is `STALE_PARTIAL_CURRENT_BODY`, even if it was complete before 01.09.2026.

Primary-publication pointer for №845 was not resolved directly from publication.pravo.gov.ru in this pass; direct primary publication fetch remains `PRIMARY_PUBLICATION_POINTER_BLOCKER`. Effective date and amendment body are corroborated from current legal sources.

### ПП РФ №676 от 06.07.2015 — effective body changes on 01.09.2026

ПП РФ 01.07.2026 №813 directly amends №676 and enters into force on 01.09.2026. Government.ru indexes №813 with the exact title «О внесении изменений в постановление Правительства Российской Федерации от 6 июля 2015 г. № 676».

Therefore as of 01.09.2026 the applicable body is the edition incorporating №813, not the former 18.03.2025 edition.

Classification: `CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01 / LATEST_AMENDMENT_PRIMARY_GOVERNMENT_INDEX_CONFIRMED`.

Completeness gate: current resolution + complete Requirements after incorporation of №813. A GitHub body frozen before №813 is `STALE_EDITION`.

### ПП РФ №1235 от 14.11.2015 — effective body changes on 01.09.2026

ПП РФ 04.07.2026 №845 also amends the Regulation approved by №1235; the changes enter into force 01.09.2026. Current legal consolidation lists amendments dated 04.07.2026 and marks the affected provisions effective from 01.09.2026.

Classification: `CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01`.

Completeness gate: `FULL_TEXT` must include the resolution + complete current Regulation. For historical/original-body archival capture, №1235 also contains the approved changes to Government acts and the repeal list; these should not be silently dropped when preserving the signed act package.

Direct primary publication pointer for №845 remains unresolved in this pass: `PRIMARY_PUBLICATION_POINTER_BLOCKER`.

## New conflicts / blockers

- `HABR_ATTACHMENT_SET_STALE_2026-09-01 +1`: №675 — Habr's two-Rules description is no longer complete after №845 becomes effective.
- `CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01 +3`: №675, №676, №1235.
- `LATEST_AMENDMENT_PRIMARY_GOVERNMENT_INDEX_CONFIRMED +2`: №584 via №372; №676 via №813.
- `PRIMARY_PUBLICATION_POINTER_BLOCKER +1 target amendment family`: №845 (affects №675 and №1235).
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER +2`: №747, №2769-р.
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`.
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`.

## Batch counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `GITHUB_MENTION_ONLY_REJECTED +2`
- `CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01 +3`
- `HABR_ATTACHMENT_SET_STALE_2026-09-01 +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Gates added / confirmed

- `EFFECTIVE_TODAY_CHANGE != PREVIOUS_DAY_CURRENT_BODY`.
- `FULL_TEXT_COMPLETE_YESTERDAY_CAN_BECOME_STALE_PARTIAL_TODAY` when a new approved attachment/rules block enters into force.
- `GITHUB_IDENTITY_MATCH != CURRENTNESS`.
- `GOVERNMENT_INDEX_CONFIRMATION != DIRECT_OFFICIAL_PUBLICATION_POINTER`.

Next boundary: continue GIS/MIS after №1235, prioritizing Government acts, then Roskomnadzor/general PDn-information acts from the user list.