# Habr NPA sweep — stream 1 — 2026-08-29 18:51 MSK

Scope: continuation of Habr 432466 and the user NPA list. GitHub copies are treated only as non-official artifacts; legal identity/status are checked independently against primary official sources where available.

## Delta

- FULL_TEXT: +0
- RELIABLE_GITHUB_ACT_CANDIDATE: +0
- REJECTED_MENTION_ONLY: +2
- GITHUB_FULL_TEXT_BLOCKER: +5
- PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED: +2
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +2
- PRIMARY_AMENDMENT_CONFIRMED: +2
- HABR_STALE_TITLE_CONFLICT: +1
- exact duplicates: +0
- body-level identity conflicts: +0

## 1. Распоряжение Правительства РФ от 11.07.2023 № 1856-р

Canonical title: «Об утверждении Концепции регулирования отрасли квантовых коммуникаций в Российской Федерации до 2030 года».

GitHub:
- exact-title search: 0 results (`incomplete_results=false`)
- variant search `"1856-р" + квантовых коммуникаций`: 0 results
- repo/commit/path/size/type: null (no reproducible artifact)
- classification: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`

Primary official source:
- Government of Russia page: https://government.ru/docs/all/148630/
- identity confirmed: 11.07.2023, № 1856-р
- page contains the dispositive part and the approved Concept body
- official PDF advertised as 3.8 MB
- classification: `PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED / CURRENT_LIFECYCLE_UNRESOLVED`

Full-text gate: the order alone is insufficient; the approved Concept is part of the required normative package.

## 2. Распоряжение Правительства РФ от 24.11.2023 № 3339-р

Canonical title: «Об утверждении Стратегии развития отрасли связи Российской Федерации на период до 2035 года».

GitHub:
- exact strategy-title search: 0 results (`incomplete_results=false`)
- variant search `"3339-р" + "отрасли связи"`: 0 results
- repo/commit/path/size/type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`

Primary official source:
- official Government PDF: https://static.government.ru/media/files/Pc7fHuejbNvqv17b0RJNv0RIqTo20lUV.pdf
- body explicitly states: approved by Government order of 24.11.2023 № 3339-р
- contains the Strategy body
- classification: `PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED / CURRENT_LIFECYCLE_UNRESOLVED`

Full-text gate: a copy must contain the approved Strategy, not only a citation to the order.

## 3. Федеральный закон от 31.07.2020 № 247-ФЗ

Canonical title: «Об обязательных требованиях в Российской Федерации».

GitHub hit inspected:
- repo: `AxHulk/osp-kavkaz-ing`
- commit/ref: `b902d3e57875c53d2c284e3e257fefc7f8d5e9e9`
- path: `src/pages/Accreditation.tsx`
- size: 174314 bytes
- type: `TSX/blob`
- blob SHA: `019eb2fb8c4e15d46859ff2a43c58517b56bfbd8`
- body contains the exact date/number/title only as one item in a list of regulatory documents; there is no statutory body
- classification: `REFERENCE_LIST / MENTION_ONLY / NOT_FULL_TEXT / REJECT`

Primary official source:
- https://publication.pravo.gov.ru/Document/View/0001202007310002
- publication no.: `0001202007310002`
- publication date: 31.07.2020
- identity confirmed

Lifecycle:
- 26.06.2026 № 215-ФЗ is independently corroborated as amending article 1 of 247-ФЗ, but a direct primary publication card for that amendment was not resolved in this pass
- classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / LATEST_AMENDMENT_CORROBORATED / PRIMARY_LATEST_AMENDMENT_DIRECT_CARD_UNRESOLVED`

## 4. Федеральный закон от 31.07.2020 № 258-ФЗ

Habr 432466 (version 28.05.2026) still lists the old title: «Об экспериментальных правовых режимах в сфере цифровых инноваций в Российской Федерации».

GitHub:
- exact old-title search: 0 results (`incomplete_results=false`)
- exact current-title search including «цифровых и технологических инноваций»: 0 results
- repo/commit/path/size/type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Primary official source for initial publication:
- https://publication.pravo.gov.ru/Document/View/0001202007310024
- publication no.: `0001202007310024`
- publication date: 31.07.2020
- original title confirms the old 2020 wording

Primary amendment marker:
- official publication index lists Federal Law 31.07.2025 № 336-ФЗ, publication no. `0001202507310081`, title explicitly refers to 258-ФЗ under the newer wording «...в сфере цифровых и технологических инноваций...»

Current lifecycle corroboration:
- Federal Law 26.06.2026 № 211-ФЗ directly amends 258-ФЗ; current consolidated sources show edition dated 26.06.2026
- direct primary publication card for № 211-ФЗ was not resolved in this pass

Conflict:
- `HABR_STALE_TITLE_CONFLICT`: the Habr version dated 28.05.2026 uses the old title although official 2025 amendment materials already use the newer title.
- canonical title for current corpus: «Об экспериментальных правовых режимах в сфере цифровых и технологических инноваций в Российской Федерации».

## 5. Указ Президента РФ от 06.03.1997 № 188

Canonical title: «Об утверждении Перечня сведений конфиденциального характера».

GitHub candidate inspected:
- repo: `sofakotlyar1999/sofakotlyar1999.githab.io`
- commit: `f0dbcfdb3c2ddeb9223004017354cddf02588528`
- path: `3.md`
- size: 9634 bytes
- type: `Markdown/blob`
- blob SHA: `b5bae235aa841d1286aca61a82fc6cc152084fad`
- body contains exact date/number/title as item 15 in a general list of information-law acts; no decree body and no approved List body
- classification: `REFERENCE_LIST / MENTION_ONLY / NOT_FULL_TEXT / REJECT`

GitHub exact search for the full formal citation returned 0 results, demonstrating again that exact Code Search can miss mention artifacts found by other discovery paths.

Primary/lifecycle:
- official publication portal directly confirms Presidential Decree 13.07.2015 № 357 «О внесении изменений в перечень сведений конфиденциального характера, утвержденный Указом ... от 6 марта 1997 г. № 188», publication no. `0001201507130003`, date 13.07.2015
- current consolidated legal sources show edition of № 188 dated 13.07.2015 with amendment markers № 1111/2005 and № 357/2015
- initial 1997 primary web card was not resolved in this pass
- classification: `PRIMARY_AMENDMENT_CONFIRMED / BASE_IDENTITY_CORROBORATED_BY_PRIMARY_AMENDMENT / PRIMARY_INITIAL_PUBLICATION_WEB_CARD_UNRESOLVED`

## Gates added/reinforced

1. `REFERENCE_LIST_WITH_EXACT_IDENTITY != ACT_BODY`.
2. `EXACT_GITHUB_CODE_SEARCH_ZERO != NO_GITHUB_MENTION_OR_BINARY_ARTIFACT`.
3. For orders approving Concepts/Strategies, `FULL_TEXT` requires the full approved attachment/body.
4. Habr/reference-list titles are aliases for discovery only; canonical current title must be normalized from authoritative lifecycle evidence.
5. Initial official publication and current consolidated lifecycle remain separate verification fields.
