# Habr NPA sweep — Stream 1 — 2026-08-29 06:51 MSK

## Delta
- FULL_TEXT: +0
- MENTION_ONLY: +1
- REFERENCE_LIST_STALE_TITLE_CONFLICT: +1
- GITHUB_FULL_TEXT_BLOCKER: +4
- EXACT_DUPLICATE: +0
- BODY_IDENTITY_CONFLICT: +0

## Указ Президента РФ от 06.03.1997 № 188
Target: Указ Президента РФ от 06.03.1997 № 188 «Об утверждении Перечня сведений конфиденциального характера».

GitHub hit:
- repo: `sofakotlyar1999/sofakotlyar1999.githab.io`
- snapshot commit: `70490c55583134da403220c20faf19c24c2f4e00`
- path: `3.md`
- size: `9634` bytes
- type: `Markdown/blob`
- blob: `b5bae235aa841d1286aca61a82fc6cc152084fad`

Body assessment: the file is an educational/reference list. Item 15 reproduces the target date, number and title, but no operative part, approved list, signature block or other normative body is present.

Classification: `MENTION_ONLY / EXACT_REFERENCE_IDENTITY / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY / REJECT_FOR_PRIMARY_KB`.

Primary official lifecycle check: official publication portal confirms Presidential Decree of 13.07.2015 № 357 «О внесении изменений в перечень сведений конфиденциального характера, утвержденный Указом Президента Российской Федерации от 6 марта 1997 г. № 188», publication number `0001201507130003`, publication date 13.07.2015. This proves the target identity and lifecycle at least through that amendment, but the direct primary lifecycle card for the 1997 base decree was not reliably resolved in this pass; do not mark `VERIFIED_CURRENT` from the GitHub mention.

Blocker: standalone GitHub `FULL_TEXT` for Указ №188/1997 remains unconfirmed. Exact GitHub code search by full title returned zero hits; zero search result is not proof of absence.

## 258-ФЗ / 31.07.2020 — stale title conflict in reference list
Habr 432466 (current page labelled version 28.05.2026) still lists item 9 under «Системообразующие документы» as Федеральный закон от 31.07.2020 № 258-ФЗ «Об экспериментальных правовых режимах в сфере цифровых инноваций в Российской Федерации».

Primary official publication portal lists Federal Law of 31.07.2025 № 336-ФЗ as «О внесении изменений в Федеральный закон “Об экспериментальных правовых режимах в сфере цифровых и технологических инноваций в Российской Федерации”», publication number `0001202507310081`, publication date 31.07.2025. Therefore the Habr target title is stale relative to the later official nomenclature by the time of the Habr 28.05.2026 version.

Classification: `REFERENCE_LIST_STALE_TITLE_CONFLICT / TARGET_IDENTITY_REQUIRES_CURRENT_TITLE_NORMALIZATION`.

GitHub searches by the old exact title, new exact title and `258-ФЗ` returned zero full-text hits in this pass. Blocker: `GITHUB_FULL_TEXT_258-FZ_2020` remains open.

## Additional exact-search blockers advanced

### Постановление Правительства РФ от 22.10.2020 № 1722
Exact GitHub code search by date/number/title phrase returned zero hits. `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

### Постановление Правительства РФ от 16.03.2009 № 228 (Роскомнадзор)
Exact GitHub code search by date/number/full title returned zero hits. `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

## Gates
- `REFERENCE_LIST_TITLE != CURRENT_OFFICIAL_TITLE` when a later primary act uses a formally changed title.
- `MENTION_WITH_EXACT_REQUISITES != FULL_TEXT`.
- `OFFICIAL_AMENDMENT_REFERENCE_TO_BASE_ACT != VERIFIED_CURRENT_BASE_TEXT`.
- `EXACT_GITHUB_CODE_SEARCH_ZERO != PROOF_OF_ABSENCE`.
