# Habr NPA sweep — Stream 1 — 2026-08-29 16:55 MSK

Scope: continuation of the systematic pass over Habr 432466 and the user NPA list. GitHub copies are treated as non-official artifacts; legal identity/lifecycle is checked separately against primary official publication sources.

## Delta

- `FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +4`
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +2`
- `PRIMARY_PUBLICATION_POINTER_CORROBORATED +1`
- `PRIMARY_DIRECT_FETCH_BLOCKER +2`
- `EXACT_DUPLICATE +0`
- `BODY_IDENTITY_CONFLICT +0`

## 1. Указ Президента РФ от 09.05.2017 № 203

Canonical target: «О Стратегии развития информационного общества в Российской Федерации на 2017 — 2030 годы», together with the approved Strategy.

GitHub global code search by characteristic exact title phrase returned `total_count=0`, `incomplete_results=false`. No reproducible GitHub blob, PDF, DOCX, or other artifact was confirmed in this pass.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Primary official publication directly confirms date/number/title: publication number `0001201705100002`, publication date 10.05.2017.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_UNRESOLVED`.

Completeness gate: a GitHub artifact containing only the decree body but omitting the approved Strategy is `PARTIAL_TEXT`, not `FULL_TEXT`.

## 2. Указ Президента РФ от 02.07.2021 № 400

Canonical target: «О Стратегии национальной безопасности Российской Федерации», together with the approved Strategy.

GitHub global code search by exact strategy-title phrase returned `total_count=0`, `incomplete_results=false`; no reproducible GitHub artifact was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Primary official publication directly confirms date/number/title: publication number `0001202107030001`, publication date 03.07.2021.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_UNRESOLVED`.

Completeness gate: `FULL_TEXT` requires both the presidential decree and the complete approved National Security Strategy.

## 3. Указ Президента РФ от 18.06.2024 № 529

Canonical target: «Об утверждении приоритетных направлений научно-технологического развития и перечня важнейших наукоемких технологий».

GitHub global code search by characteristic exact title phrase returned `total_count=0`, `incomplete_results=false`; no reproducible GitHub artifact was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

The official-publication pointer is independently corroborated as `0001202406180018`, publication date 18.06.2024. Direct fetch of the primary `publication.pravo.gov.ru` card timed out in this pass, therefore the status is not promoted to direct primary lifecycle verification.

Classification: `PRIMARY_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_FETCH_BLOCKER / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_UNRESOLVED`.

Completeness gate: the act approves two substantive lists; a GitHub copy lacking either the priority directions or the list of critical knowledge-intensive technologies is `PARTIAL_TEXT`.

## 4. Распоряжение Правительства РФ от 03.06.2019 № 1189-р

Canonical target: «Об утверждении Концепции создания и функционирования национальной системы управления данными и плана мероприятий (“дорожной карты”) по созданию национальной системы управления данными на 2019 — 2021 годы».

GitHub global code search by characteristic exact phrase `национальной системы управления данными` returned `total_count=0`, `incomplete_results=false`; no reproducible GitHub body or binary artifact was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

An official Government page pointer (`government.ru/docs/36940/`) is independently identified, but direct fetch timed out in this pass. Secondary mirrors show the complete package contains the order, the Concept, and the 2019–2021 roadmap; they are not used to assign official/current status.

Classification: `PRIMARY_OFFICIAL_POINTER_IDENTIFIED / PRIMARY_DIRECT_FETCH_BLOCKER / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_UNRESOLVED`.

Completeness gate: `FULL_TEXT` requires the order plus the full Concept and roadmap; an artifact containing only the Concept or only the one-page order is `PARTIAL_TEXT`.

## New gates

1. `SEARCH_INDEX_ZERO` remains a blocker signal only; it is not proof that no binary artifact exists elsewhere in a repository.
2. Strategic acts that approve a strategy/concept/list/package are `FULL_TEXT` only when every approved normative attachment is present.
3. `PRIMARY_POINTER_CORROBORATED` is kept distinct from `PRIMARY_DIRECT_VERIFIED` when the official portal/card cannot be fetched in the current pass.
4. Expired planning horizon in an attachment (for example, a 2019–2021 roadmap) does not by itself prove that the enacting act is repealed; lifecycle status must be established separately.
