# Habr NPA sweep — Stream 1 — 2026-08-29 09:56 MSK

Scope: continuation of the systematic pass over Habr 432466 and the user NPA list. GitHub copies are treated as non-official by default. Official identity/lifecycle is checked separately against primary official publication sources.

## Delta only

### 1. Federal Law of 03.12.2008 No. 242-FZ — genomic registration

Target identity from Habr: Federal Law of 03.12.2008 No. 242-FZ «О государственной геномной регистрации в Российской Федерации».

GitHub exact code search by the full title returned `total_count=0` in this pass. No reproducible per-act GitHub blob was found, therefore there is no repo/commit/path/size/type tuple to accept yet.

Status: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

Primary lifecycle delta: the official publication portal confirms Federal Law of 14.02.2024 No. 16-FZ «О внесении изменений в Федеральный закон "О государственной геномной регистрации в Российской Федерации"», publication No. `0001202402140006`, published 14.02.2024. Any GitHub snapshot predating that amendment must therefore be treated as stale even if its identity is otherwise correct.

Gate: `BASE_ACT_IDENTITY_MATCH != CURRENT_CONSOLIDATED_TEXT`.

### 2. Government Decree of 29.06.2021 No. 1046 — federal supervision over personal-data processing

Target is present in the current Habr PDn section as PP RF No. 1046 with the attached Regulation on federal state control (supervision) over personal-data processing.

GitHub exact code search for `1046` together with the characteristic phrase `обработкой персональных данных` returned `total_count=0`. No full text or reliable body candidate was confirmed; repo/commit/path/size/type remain unavailable because no candidate blob passed discovery.

Status: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

Primary-source blocker: this pass did not resolve a direct publication.pravo.gov.ru card for the base act with enough confidence to assert its complete current lifecycle. Third-party legal-system pages and the Habr list are not promoted to primary official evidence.

Status: `PRIMARY_OFFICIAL_DIRECT_CARD_FETCH_BLOCKER`.

### 3. Government Decree of 24.04.2025 No. 538 — anonymized personal-data sets

New Habr target in the PDn section.

GitHub exact code search for `Постановление Правительства РФ от 24.04.2025 N 538` returned `total_count=0`. No reproducible full-text or metadata blob candidate was confirmed, so repo/commit/path/size/type are intentionally not fabricated.

Status: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

Primary identity is confirmed by the official publication portal: Government Decree of 24.04.2025 No. 538, exact title concerning the list of cases for formation of anonymized personal-data sets, publication No. `0001202504250043`, published 25.04.2025.

Status: `PRIMARY_IDENTITY_CONFIRMED / GITHUB_BODY_MISSING`.

### 4. Government Decree of 01.08.2025 No. 1154 — anonymization requirements, methods and rules

New Habr target in the PDn section.

GitHub exact code search for `Постановление Правительства РФ от 01.08.2025 № 1154` returned `total_count=0`. No reproducible GitHub body candidate was confirmed; no repo/commit/path/size/type tuple is assigned.

Status: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

Primary identity is confirmed by the official publication portal: Government Decree of 01.08.2025 No. 1154 «Об утверждении требований к обезличиванию персональных данных, методов обезличивания персональных данных и Правил обезличивания персональных данных», publication No. `0001202508050011`, published 05.08.2025, official PDF listed as 12 pages.

Status: `PRIMARY_IDENTITY_CONFIRMED / GITHUB_BODY_MISSING`.

## Counters for this pass

- `FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +4`
- `PRIMARY_IDENTITY_CONFIRMED +2` (PP 538/2025, PP 1154/2025)
- `PRIMARY_AMENDMENT_CONFIRMED +1` (16-FZ/2024 -> 242-FZ/2008)
- `PRIMARY_OFFICIAL_DIRECT_CARD_FETCH_BLOCKER +1` (PP 1046/2021)
- `EXACT_DUPLICATE +0`
- `BODY_IDENTITY_CONFLICT +0`

## Gates reinforced

1. `EXACT_GITHUB_SEARCH_ZERO != PROOF_OF_ABSENCE`.
2. `NO_REPRODUCIBLE_BLOB => NO repo/commit/path/size/type INVENTION`.
3. `OFFICIAL_AMENDMENT_FOUND => PRE-AMENDMENT_GITHUB_SNAPSHOT IS STALE`.
4. `HABR/CONSULTANT/CODEX POINTER != PRIMARY_OFFICIAL_LIFECYCLE`.
