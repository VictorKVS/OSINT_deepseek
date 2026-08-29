# Habr NPA sweep — Stream 1 — 2026-08-29 15:52 MSK

Scope: continuation of the systematic pass over Habr 432466 and the user NPA list. GitHub copies are treated as non-official artifacts; legal identity/lifecycle is checked separately against primary official publication sources.

## Delta

- `FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +4`
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +1`
- `PRIMARY_AMENDMENT_CONFIRMED +1`
- `PRIMARY_DIRECT_CARD_UNRESOLVED +2`
- `EXACT_DUPLICATE +0`
- `BODY_IDENTITY_CONFLICT +0`

## 1. Постановление Правительства РФ от 21.03.2012 № 211

Canonical target: «Об утверждении перечня мер, направленных на обеспечение выполнения обязанностей, предусмотренных Федеральным законом \"О персональных данных\" и принятыми в соответствии с ним нормативными правовыми актами, операторами, являющимися государственными или муниципальными органами».

GitHub exact code search by date/number/title returned `0` results (`incomplete_results=false`). No reproducible blob or binary artifact was confirmed in this pass.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Classification: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE / PRIMARY_DIRECT_CARD_UNRESOLVED`.

Secondary consolidated legal systems expose later revisions, but those are not promoted to `VERIFIED_CURRENT` without a primary lifecycle chain.

## 2. Указ Президента РФ от 22.05.2015 № 260

Canonical target: «О некоторых вопросах информационной безопасности Российской Федерации», together with the approved «Порядок подключения информационных систем и информационно-телекоммуникационных сетей к информационно-телекоммуникационной сети \"Интернет\" и размещения (публикации) в ней информации через российский государственный сегмент информационно-телекоммуникационной сети \"Интернет\"».

GitHub exact code search returned `0` results; no reproducible GitHub body/binary was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Official-publication pointer independently corroborated for the initial act: `0001201505220028`, publication date 22.05.2015. Direct primary-card fetch was not resolved in this pass, therefore this is not promoted to a direct primary lifecycle verification.

A suspected lifecycle pointer to Presidential Decree 22.07.2024 № 613 was checked against the primary official publication index: № 613/2024 is titled «О комиссиях Государственного Совета Российской Федерации по направлениям социально-экономического развития Российской Федерации и их председателях». No verified body-level relation to № 260 was established, so it must not be used as an amendment/repeal marker for № 260 without explicit text evidence.

Classification: `GITHUB_FULL_TEXT_BLOCKER / PRIMARY_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_CARD_UNRESOLVED / SUSPECT_LIFECYCLE_POINTER_REJECTED_PENDING_BODY_EVIDENCE`.

Completeness gate: an artifact containing only the decree body but omitting the approved Order is `PARTIAL_TEXT`, not `FULL_TEXT`.

## 3. Указ Президента РФ от 05.12.2016 № 646

Canonical target: «Об утверждении Доктрины информационной безопасности Российской Федерации».

GitHub exact code search returned `0` results; no reproducible GitHub artifact was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Primary official publication directly confirms the act: publication number `0001201612060002`, publication date 06.12.2016, exact date/number/title match.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_UNRESOLVED`.

Completeness gate: `FULL_TEXT` requires both the presidential decree and the approved Doctrine text.

## 4. Постановление Правительства РФ от 09.10.2021 № 1723

Canonical target: «Об утверждении Правил формирования и ведения единого федерального информационного регистра, содержащего сведения о населении Российской Федерации, в том числе порядка включения в него сведений о населении Российской Федерации и их изменения».

GitHub exact code search returned `0` results; no reproducible GitHub artifact was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Primary official publication confirms a later amendment: Постановление Правительства РФ от 17.06.2025 № 908 «О внесении изменений в постановление Правительства Российской Федерации от 9 октября 2021 г. № 1723», official publication `0001202506200018` on 20.06.2025, PDF 2752 KB / 13 pages. This is a mandatory freshness marker for any future GitHub candidate. An earlier amendment by № 663/2023 is therefore not the latest confirmed amendment marker in this stream.

Classification: `PRIMARY_AMENDMENT_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_AFTER_2025-06-20_UNRESOLVED`.

## New gates

1. `PRIMARY_AMENDMENT_MARKER` must be refreshed when a later official amending act is found; an older known amendment is not sufficient for freshness testing.
2. `SAME_NUMBER + SAME_YEAR` or a secondary lifecycle pointer is not enough to bind an amending act to the target; require explicit body/title evidence.
3. For acts approving a doctrine/order/rules, `FULL_TEXT` requires the approved normative attachment as well as the enacting decree/resolution.
