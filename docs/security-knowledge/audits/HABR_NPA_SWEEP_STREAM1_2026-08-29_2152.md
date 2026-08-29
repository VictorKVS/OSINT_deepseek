# Habr NPA sweep — Stream 1 — 2026-08-29 21:52 MSK

Scope: continue systematic verification of Habr 432466 and the user NPA list. GitHub artifacts are classified independently from official/legal status. A GitHub copy is never treated as an official source automatically.

## Delta

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- REJECTED_REFERENCE_ONLY: +2
- GITHUB_FULL_TEXT_BLOCKER: +4
- PRIMARY_AMENDMENT_PUBLICATION_CONFIRMED: +1
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +1
- LATEST_AMENDMENT_CORROBORATED_PRIMARY_DIRECT_BLOCKER: +1
- OFFICIAL_PUBLICATION_CORROBORATED_PRIMARY_DIRECT_BLOCKER: +1
- EXACT_DUPLICATE: +0
- BODY_IDENTITY_CONFLICT: +0

## 1. Federal Law of 26.12.2008 No. 294-FZ

Canonical title: «О защите прав юридических лиц и индивидуальных предпринимателей при осуществлении государственного контроля (надзора) и муниципального контроля».

### GitHub

Rejected hit:
- repo: `AxHulk/osp-kavkaz-ing`
- commit: `b902d3e57875c53d2c284e3e257fefc7f8d5e9e9`
- path: `src/pages/Accreditation.tsx`
- size: `174314` bytes
- type: `TSX/blob`
- blob_sha: `019eb2fb8c4e15d46859ff2a43c58517b56bfbd8`
- classification: `REFERENCE_LIST / MENTION_ONLY / NOT_FULL_TEXT / REJECT`

Body check: the file is a React accreditation page. No. 294-FZ appears only in a normative-reference list; the statutory body is absent.

Additional exact-title/body searches did not yield a reproducible full-text artifact. `repo/commit/path/size/type = null` for a usable act-body candidate.

### Official/lifecycle

Primary official amendment publication confirmed:
- Federal Law of 29.12.2025 No. 548-FZ
- title explicitly amends Federal Law No. 294-FZ and arts. 29/65 of Federal Law No. 248-FZ
- official publication No. `0001202512290036`
- publication date: `2025-12-29`
- source: https://publication.pravo.gov.ru/Document/View/0001202512290036

Status: `PRIMARY_LATEST_AMENDMENT_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED`.

Gate: do not mark No. 294-FZ simply as wholly irrelevant/repealed merely because No. 248-FZ became the general control framework. No. 548-FZ/2025 itself proves continuing transitional legal treatment of No. 294-FZ; applicability must be resolved provision-by-provision and by effective date.

## 2. Government Resolution of 10.03.2022 No. 336

Canonical title: «Об особенностях организации и осуществления государственного контроля (надзора), муниципального контроля».

### GitHub

Rejected hit:
- repo: `Grantik/odin-vault`
- commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
- path: `sync/canon/package/samples/minekonom_prikaz_67_gis_ekonomika.txt`
- size: `METADATA_BLOCKER` (connector body endpoint did not expose a byte-size field in this pass)
- type: `TXT/blob`
- blob_sha: `bad57fdb9d2f27f9d120964eb2c8011ee0cf58f4`
- classification: `REFERENCE_ONLY / WRONG_PRIMARY_BODY / NOT_FULL_TEXT / REJECT`

Body identity check: the file begins with Ministry of Economic Development Order of 18.02.2022 No. 67 «О государственной информационной системе "Экономика"». Therefore it cannot be the body of PP No. 336; any No. 336 occurrence is only a cross-reference/context occurrence.

No reproducible full-text GitHub artifact for PP No. 336 was confirmed.

### Official/lifecycle

Initial publication pointer: `0001202203100013`; direct official fetch timed out in this pass, so no upgrade to direct-primary-body verification.

A new 2026 amendment marker is corroborated by multiple current legal sources:
- Government Resolution of 10.08.2026 No. 991
- title: «О внесении изменения в постановление Правительства Российской Федерации от 10 марта 2022 г. № 336»
- adds point 11(24), with a temporary rule through 31.12.2026
- enters into force from official publication.

Direct primary `publication.pravo.gov.ru` card for No. 991 was not resolved by the current search index, therefore status remains `LATEST_AMENDMENT_CORROBORATED / PRIMARY_DIRECT_CARD_BLOCKER`, not `PRIMARY_LATEST_AMENDMENT_CONFIRMED`.

Status: `GITHUB_FULL_TEXT_BLOCKER / LATEST_AMENDMENT_CORROBORATED / PRIMARY_DIRECT_CARD_BLOCKER`.

Gate: any future GitHub copy of No. 336 lacking the No. 991/2026 marker must be treated as stale unless its edition date is explicitly historical.

## 3. Government Resolution of 01.08.2025 No. 1154

Canonical title: «Об утверждении требований к обезличиванию персональных данных, методов обезличивания персональных данных и Правил обезличивания персональных данных».

### GitHub

Exact/variant searches by number, title and characteristic anonymization-method phrasing returned no reproducible full act-body candidate.

- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### Official

Primary official index confirms:
- act date/number/title: exact match
- publication No. `0001202508050011`
- publication date: `2025-08-05`
- official PDF: `2619 KB`, `12 pages`
- source: https://publication.pravo.gov.ru/Document/View/0001202508050011

Status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER / CURRENT_CONSOLIDATED_BODY_UNRESOLVED`.

Completeness gate: `FULL_TEXT` requires all three approved normative components — Requirements + Methods + Rules. A copy containing only one component or only the operative resolution text is `PARTIAL_TEXT`.

## 4. Roskomnadzor Order of 02.02.2023 No. 13

Canonical title: «Об утверждении порядка проведения мониторинга информационно-телекоммуникационных сетей, в том числе сети "Интернет", а также определении видов информации и (или) информационных ресурсов, в отношении которых проводится мониторинг».

### GitHub

Exact-title/number search produced no reproducible full-text candidate.

- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### Official/publication corroboration

Official-publication corroboration via Rossiyskaya Gazeta confirms:
- date/number/title: exact match
- Ministry of Justice registration: `31.03.2023 No. 72824`
- official internet legal-information portal publication: `31.03.2023`
- RG publication: `03.04.2023`
- effective date: `11.04.2023`
- expected official-publication pointer: `0001202303310014`
- source: https://rg.ru/documents/2023/04/03/roskomnadzor-prikaz13-site-dok.html

The direct `publication.pravo.gov.ru` card was not resolved in this pass, so the record is not upgraded to `PRIMARY_DIRECT_VERIFIED`.

Status: `OFFICIAL_PUBLICATION_CORROBORATED / PRIMARY_DIRECT_CARD_BLOCKER / GITHUB_FULL_TEXT_BLOCKER / CURRENT_LIFECYCLE_UNRESOLVED`.

## New corpus gates

1. `REFERENCE_WITH_EXACT_NUMBER_DATE_TITLE != ACT_BODY`.
2. `LATEST_LEGAL_DATABASE_AMENDMENT != PRIMARY_LATEST_AMENDMENT_CONFIRMED` until the direct primary publication card/body is resolved.
3. `TRANSITIONAL_APPLICATION != FULL_REPEAL`: for old framework laws such as 294-FZ, applicability must be stored at provision/effective-date level.
4. For compound acts such as PP No. 1154, `FULL_TEXT` requires the whole approved normative package, not only the signing/operative page.
