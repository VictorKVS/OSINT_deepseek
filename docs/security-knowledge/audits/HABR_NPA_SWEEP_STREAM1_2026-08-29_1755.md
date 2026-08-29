# Habr NPA sweep — Stream 1 — 2026-08-29 17:55 MSK

Scope: continuation of the systematic pass over Habr 432466 and the user NPA list. GitHub artifacts are non-official copies/candidates; identity, publication and lifecycle are checked separately against primary official sources.

## Delta

- `FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `REJECTED_FALSE_POSITIVE +1`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +3`
- `PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED +3`
- `PRIMARY_AMENDMENT_MARKER_CONFIRMED +2`
- `CURRENTNESS_FLOOR_MARKER +1`
- `EXACT_DUPLICATE +0`
- `BODY_IDENTITY_CONFLICT +0`

## 1. Указ Президента РФ от 10.10.2019 № 490

Canonical target: «О развитии искусственного интеллекта в Российской Федерации», together with the complete National Strategy for AI Development through 2030 approved by the Decree.

GitHub exact code search by the full title returned `total_count=0`, `incomplete_results=false`. No reproducible GitHub text/blob/PDF/DOCX candidate was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Primary initial publication: official publication portal confirms Decree 10.10.2019 № 490, publication no. `0001201910110003`, publication date 11.10.2019.

Freshness marker: the official Kremlin legal bank confirms Presidential Decree 15.02.2024 № 124, which expressly amends both Decree № 490 and the National Strategy approved by it. Therefore a future GitHub copy that does not contain the № 124/2024 changes is `STALE_CONFIRMED` after body-level comparison.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_AMENDMENT_MARKER_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER`.

Completeness gate: a copy containing only the short Decree without the complete approved Strategy is `PARTIAL_TEXT`, not `FULL_TEXT`.

## 2. Распоряжение Правительства РФ от 22.12.2022 № 4088-р

Canonical target: order approving the «Концепция формирования и развития культуры информационной безопасности граждан Российской Федерации», together with the complete Concept.

GitHub searches by the exact Concept title and by `4088-р + информационной безопасности` returned `total_count=0`, `incomplete_results=false`; no reproducible artifact was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Primary official source: Government of Russia page `government.ru/docs/all/145092/` contains the order body, exact date/number, and the approved Concept; the page exposes the official PDF (7.3 MB).

Classification: `PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_UNRESOLVED`.

Completeness gate: the one-page enacting order without the attached Concept is `PARTIAL_TEXT`.

## 3. Распоряжение Правительства РФ от 28.04.2023 № 1105-р

Canonical target: order approving the «Концепция информационной безопасности детей в Российской Федерации», together with the complete Concept.

GitHub exact search `1105-р + "информационной безопасности детей"` returned `total_count=0`, `incomplete_results=false`; no reproducible GitHub artifact was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Primary initial publication: official publication portal confirms order 28.04.2023 № 1105-р, publication no. `0001202305050026`, publication date 05.05.2023. Government of Russia page `government.ru/docs/all/147360/` contains the complete order and approved Concept and exposes the official PDF (11.2 MB).

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_UNRESOLVED`.

## 4. Распоряжение Правительства РФ от 20.05.2023 № 1315-р

Canonical target: order approving the «Концепция технологического развития на период до 2030 года», together with the complete Concept.

GitHub exact search `1315-р + "технологического развития"` returned `total_count=0`, `incomplete_results=false`; no reproducible GitHub artifact was confirmed.

Artifact fields: `repo=null`, `commit=null`, `path=null`, `size=null`, `type=null`.

Primary initial publication: official publication portal confirms order 20.05.2023 № 1315-р, publication no. `0001202305250050`, publication date 25.05.2023.

Freshness marker: current Government of Russia page `government.ru/docs/all/147621/` explicitly marks both the order and the Concept as being in the edition of Government Order 21.10.2024 № 2963-р. Hence any future GitHub copy lacking the № 2963-р/2024 changes is `STALE_CONFIRMED` after body-level verification.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED / PRIMARY_AMENDMENT_MARKER_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER`.

## 5. Федеральный закон от 27.07.2006 № 149-ФЗ

Canonical target: «Об информации, информационных технологиях и о защите информации» in a current consolidated text.

GitHub exact title search returned 18 indexed hits, but the inspected first hit is not the law:

- repo: `zhsrl/tnvd-web`
- commit/ref: `451fc8e312532dc8333c9da9dc14abca9dbf3671`
- path: `assets/pap.md`
- size: `32403` bytes
- file format: `Markdown`
- Git object type: `blob`
- blob SHA: `790513bc36468cb40a4f93da894384f7bebae4c0`

Body inspection shows the file begins as an operator «Политика в отношении обработки персональных данных», defines the operator's data-processing rules and cites legislation. It is a derivative privacy policy, not the normative body of 149-ФЗ. Classification: `DERIVATIVE_PRIVACY_POLICY / MENTION_ONLY / NOT_FULL_TEXT / REJECT`.

Additional GitHub checks: exact searches for characteristic article text and exact-title `.txt` copies returned zero reproducible full-law candidates. Therefore the target remains `GITHUB_FULL_TEXT_BLOCKER`; the 18 title hits cannot be treated as full-law copies without individual body verification.

Primary identity: the official newspaper «Российская газета» publication confirms Federal Law 27.07.2006 № 149-ФЗ, exact title, and publication on 28.07.2006.

Freshness floor: the official publication portal confirms at least two later amendment acts dated 29.12.2025 that expressly amend 149-ФЗ: № 568-ФЗ (`0001202512290056`) and № 569-ФЗ (`0001202512290057`). These are freshness markers, not proof that a given consolidated copy is current on 29.08.2026. Any future GitHub candidate must at minimum be checked for incorporation/applicability of these amendments and then against any subsequent amendments.

Classification: `PRIMARY_IDENTITY_CONFIRMED / CURRENTNESS_FLOOR_MARKER_568_569_FZ_2025 / GITHUB_FULL_TEXT_BLOCKER`.

## New gates

1. `TITLE_SEARCH_HIT != ACT_BODY`: even an exact act-title hit can be only an operator policy, implementation note, checklist or citation list.
2. `STRATEGY_OR_CONCEPT_ACT_FULL_TEXT`: enacting order/decree plus every approved strategy/concept/attachment is required for `FULL_TEXT`.
3. `PRIMARY_AMENDMENT_MARKER => FRESHNESS_FLOOR`: a known official amendment provides a minimum revision marker for GitHub copies, but does not itself prove the full current lifecycle.
4. `CURRENTNESS_FLOOR != VERIFIED_CURRENT`: for heavily amended laws such as 149-ФЗ, confirming amendments through a date is only a floor; subsequent amendments must still be checked.
5. `SEARCH_INDEX_ZERO != PROOF_OF_ABSENCE`: binary or unindexed repository artifacts still require tree/path traversal where practical.
