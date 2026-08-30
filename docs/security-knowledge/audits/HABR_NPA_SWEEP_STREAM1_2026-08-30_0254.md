# Habr NPA sweep — Stream 1 — 2026-08-30 02:54 MSK

Source snapshot: Habr article 432466, version dated 2026-05-28, plus the user-maintained NPA queue.

## Delta for this pass

- targets processed: 8
- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- REJECTED_FALSE_POSITIVE: +1
- GITHUB_FULL_TEXT_BLOCKER: +8
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +1
- OFFICIAL_PUBLICATION_POINTER_CORROBORATED: +4
- FULLTEXT_SECONDARY_CORROBORATED: +5
- HABR_LEGACY_CONFLICT: +1
- TEMPORAL_SCOPE_CLARIFICATION: +2
- exact duplicates: +0
- new body-level identity conflicts: +0

## Findings

### 1. Постановление Правительства РФ от 16.01.2023 №24
Target: решение Роскомнадзора о запрещении/ограничении трансграничной передачи персональных данных.

GitHub:
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`
- strict and broad searches found no reproducible target act body; mention-only hits were not accepted.

Official/current:
- publication pointer corroborated: `0001202301170011`, published 2023-01-17.
- exact act identity/title corroborated.
- direct primary card was not obtained in this pass.
- status: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_CARD_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 2. Постановление Правительства РФ от 24.04.2025 №538
Target: перечень случаев формирования составов персональных данных, полученных в результате обезличивания.

Rejected GitHub hit:
- repo: `shchukin/ege-css`
- commit: `ffb20cd04605d12f0002af454031047c4a68a3c6`
- path: `production/storeEgenator/privacy-policy.html`
- blob: `8d2dd432d3104c1f163e53440fbe9439b3dc35f8`
- size: `METADATA_UNRESOLVED` (connector did not return a trustworthy byte size; not invented)
- type: `HTML/file`
- body starts as the EГЭнатор website privacy policy and references general PD legislation; it is not PP №538.
- classification: `DERIVATIVE_PRIVACY_POLICY / SEARCH_FALSE_POSITIVE / NOT_ACT_BODY / REJECT`.

After rejection no reliable GitHub act body remained, so target status is `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary official publication directly identified: `0001202504250043`, published 2025-04-25.
- official index describes PDF ~1214 KB / 5 pages.
- status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: `FULL_TEXT = постановление + полный утвержденный перечень`.

### 3. Постановление Правительства РФ от 22.05.2025 №702
Target: правила подтверждения пользователями государственной информационной системы факта ознакомления / совершения действий по ч.7 ст.13.1 закона о ПДн.

GitHub:
- repo/commit/path/size/type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- publication pointer corroborated: `0001202505280017`, published 2025-05-28.
- direct primary card timed out.
- independent full-text legal source reproduces the act and attached Rules and gives effective date 2025-09-01.
- status: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_CARD_TIMEOUT / FULLTEXT_SECONDARY_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness: signing act + full Rules.

### 4. Постановление Правительства РФ от 28.05.2025 №740
Target: государственная информационная система, предусмотренная ст.13.1 закона о ПДн, and amendments connected with the national data-management infrastructure.

GitHub:
- repo/commit/path/size/type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- full text and identity corroborated by current legal databases.
- primary official publication card was not resolved in this pass.
- temporal nuance: the act contains split effective dates; the relevant item 3 applies from signing (2025-05-28), while the remaining delayed provisions apply from 2025-09-01.
- status: `FULLTEXT_SECONDARY_CORROBORATED / PRIMARY_PUBLICATION_CARD_UNRESOLVED / TEMPORAL_SCOPE_CLARIFICATION / GITHUB_FULL_TEXT_BLOCKER`.
- completeness: act body + complete attached amendments to PP №733.

### 5. Постановление Правительства РФ от 26.06.2025 №961
Target: rules for forming anonymized PD data sets and rules for providing access to them.

GitHub:
- repo/commit/path/size/type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- publication pointer corroborated: `0001202506270025`, published 2025-06-27.
- direct primary card timed out.
- current secondary full text reproduces the act and both approved rule sets; effective date corroborated as 2025-09-01.
- status: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_CARD_TIMEOUT / FULLTEXT_SECONDARY_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: both approved rule sets are mandatory; one missing attachment = `PARTIAL_TEXT`.

### 6. Постановление Правительства РФ от 26.06.2025 №966
Target: interaction rules between the authorized federal body, PD operators and operators of information systems in the anonymized-data workflow.

GitHub:
- repo/commit/path/size/type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- publication pointer corroborated: `0001202506260044`, published 2025-06-26.
- direct primary card timed out.
- current secondary legal source gives full text/status and effective date 2025-09-01.
- status: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_CARD_TIMEOUT / CURRENT_STATUS_SECONDARY_CORROBORATED / FULLTEXT_SECONDARY_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness: act + full approved Rules.

### 7. Постановление Правительства РФ от 04.07.2025 №1012
Target: storage format for questionnaires used in state/municipal services and requirements for digital photographs.

GitHub:
- repo/commit/path/size/type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current legal full text corroborates exact identity and both attachments.
- primary official publication card was not resolved in this pass.
- temporal nuance from the act body: general provisions take effect upon official publication, while point 1 is expressly deferred to 2026-01-01.
- status: `FULLTEXT_SECONDARY_CORROBORATED / PRIMARY_PUBLICATION_CARD_UNRESOLVED / TEMPORAL_SCOPE_CLARIFICATION / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: both `Формат хранения...` and `Требования к цифровой фотографии` are required for `FULL_TEXT`.

### 8. Приказ Роскомнадзора от 16.07.2010 №482
Target: legacy notification form/recommendations in the PDn block.

GitHub:
- repo/commit/path/size/type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Lifecycle conflict:
- current consolidated sources show that substantive points 1–2 and their appendices were repealed by Roskomnadzor Order №706 of 19.08.2011.
- later regulation replaced the notification forms; the current notification-form framework includes Roskomnadzor Order №180 of 28.10.2022.
- this pass does **not** claim that every residual provision of Order №482 was formally repealed; only the substantive form/recommendation layer is proven superseded/repealed.
- status: `HABR_LEGACY_ACT / SUBSTANTIVE_PROVISIONS_REPEALED / CURRENT_FORM_SUPERSEDED / CURRENT_RESIDUAL_STATUS_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

## New corpus gates

1. `FULL_TEXT_FOR_ATTACHMENT_ACT = SIGNING_ACT + ALL_APPROVED_ATTACHMENTS`.
2. `SUBSTANTIVE_PROVISIONS_REPEALED != WHOLE_ACT_REPEALED` — lifecycle is stored at provision/attachment level when necessary.
3. `SPLIT_EFFECTIVE_DATES` must be stored per clause/attachment, not only at document level.
4. If a connector does not expose trustworthy file size, record `METADATA_UNRESOLVED`; never infer or fabricate bytes.
5. A GitHub privacy policy or implementation artifact quoting an NPA remains `NOT_ACT_BODY` even when the number/title appears exactly.

## Source pointers used in this pass

Primary/official publication portal:
- https://publication.pravo.gov.ru/document/0001202504250043
- publication pointer `0001202301170011` for PP №24
- publication pointer `0001202505280017` for PP №702
- publication pointer `0001202506270025` for PP №961
- publication pointer `0001202506260044` for PP №966

GitHub rejected artifact:
- https://github.com/shchukin/ege-css/blob/ffb20cd04605d12f0002af454031047c4a68a3c6/production/storeEgenator/privacy-policy.html

Note: GitHub copies are never promoted to official legal sources. Officiality, current status and effective dates are maintained as separate evidence dimensions.
