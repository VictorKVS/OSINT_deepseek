# Habr NPA sweep — Stream 1 — 2026-09-01 04:53 MSK

Scope: Habr 432466, section «Государственные и муниципальные информационные системы (ГИС и МИС)», federal items 36–40.

Targets:
- ПП РФ от 24.07.2025 №1092
- ПП РФ от 19.09.2025 №1443
- ПП РФ от 28.11.2025 №1933
- ПП РФ от 07.02.2026 №102
- ПП РФ от 27.02.2026 №200

Method: GitHub exact + distinctive-phrase search; body/mention separation; identity gate by type/authority/number/date/title; official publication and lifecycle checked independently. GitHub is never treated as an official source by itself.

## Results

| Act | GitHub result | repo | commit | path | blob | size | type | classification |
|---|---|---|---|---|---|---:|---|---|
| ПП №1092/2025 | no body/candidate | null | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| ПП №1443/2025 | no body/candidate | null | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| ПП №1933/2025 | no body/candidate | null | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| ПП №102/2026 | binary PDF candidate | biondohod/ru-a11y | 9f0ba249d87ea4268b5ae487f224b2e262c5025b | documents/Постановления 102.pdf | 3fb726187a5374eec874dbba937b60a96819c0fe | 1,272,299 B | PDF | RELIABLE_GITHUB_CANDIDATE / PDF_INTERNAL_IDENTITY_BLOCKER |
| ПП №102/2026 | exact reference/implementation summary | biondohod/ru-a11y | 9f0ba249d87ea4268b5ae487f224b2e262c5025b | packages/eslint-preset/README.md | 9c9a71e5cc77943e89fc40d07c48a21a2b13b63a | 35,582 B | Markdown | MENTION_ONLY / IMPLEMENTATION_SUMMARY / REJECTED_AS_NORMATIVE_BODY |
| ПП №200/2026 | no body/candidate | null | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

### GitHub candidate — ПП №102/2026

Repository tree at commit `9f0ba249d87ea4268b5ae487f224b2e262c5025b` confirms `documents/Постановления 102.pdf`, blob `3fb726187a5374eec874dbba937b60a96819c0fe`, size 1,272,299 bytes. The same commit contains `packages/eslint-preset/README.md` (blob `9c9a71e5cc77943e89fc40d07c48a21a2b13b63a`, 35,582 bytes), which explicitly identifies «Постановление Правительства РФ №102 от 07.02.2026» and links to the official publication pointer `0001202602100010`.

The README is not a normative body: it is an ESLint accessibility implementation summary. The PDF is therefore promoted only to `RELIABLE_GITHUB_CANDIDATE`, not `FULL_TEXT`: the connector exposes binary metadata but does not expose the PDF bytes/text for an internal number/date/title/body check. Required blocker: `PDF_INTERNAL_IDENTITY_BLOCKER`.

## Official-source / lifecycle checks

### ПП РФ №1092 от 24.07.2025
- Identity matches Habr.
- Primary official publication confirmed: https://publication.pravo.gov.ru/document/0001202507240022
- Publication no.: `0001202507240022`; published 24.07.2025.
- No later primary amendment/repeal was confirmed in this pass; do not infer currentness from absence of a hit.
- Status gate: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.
- FULL_TEXT gate: постановление + complete approved Положение.

### ПП РФ №1443 от 19.09.2025
- Identity matches Habr.
- Primary official publication confirmed: https://publication.pravo.gov.ru/document/0001202509220001
- Publication no.: `0001202509220001`; published 22.09.2025; official index reports PDF 9,686 KB / 44 pages.
- New completeness conflict in Habr metadata: Habr parenthetical names only the two Rules, while operative clause 1 approves four separate bodies: (1) agreed list of documents, (2) Rules for the mobile app, (3) Rules for the registry, (4) amendments to Government acts.
- Classification: `HABR_ATTACHMENT_SET_INCOMPLETE`.
- FULL_TEXT gate: постановление + Перечень + both Rules (including their appendices) + Changes to Government acts.
- Implementation is staged: I from entry into force; II +90 days; III +120; IV +150; V +180; VI from 01.07.2029. Separate temporary rule for simple e-signature runs until 01.07.2027.
- Gate: `IMPLEMENTATION_STAGE != ACT_SUNSET`.
- No later primary amendment/repeal confirmed in this pass: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### ПП РФ №1933 от 28.11.2025
- Identity matches Habr.
- Primary official publication confirmed: https://publication.pravo.gov.ru/document/0001202512080029
- Publication no.: `0001202512080029`; published 08.12.2025.
- Important completeness/effect gate: a copy containing only the approved Положение is not the complete enacted body. Operative clause 2 separately amends the Положение on the procurement information system (PP №60/2022); clause 2 entered into force 01.07.2026. Clause 4 also sets 01.07.2026 for specified provisions of the approved Положение.
- As of 01.09.2026 those staged provisions are already effective.
- Classification: `STAGED_EFFECTIVE_BODY_CONFIRMED_2026-07-01`; `FULL_TEXT_REQUIRES_OPERATIVE_AMENDMENT_CLAUSE`.
- No later primary amendment/repeal confirmed in this pass: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### ПП РФ №102 от 07.02.2026
- Habr identity matches the exact number/date/title used by current legal texts.
- GitHub README points to primary publication ID `0001202602100010` (`publication.pravo.gov.ru`). Direct fetch of the official card timed out in this pass.
- Secondary current legal text confirms entry into force 01.03.2026, but this is not used as a substitute for a successful primary fetch.
- Status: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_FETCH_BLOCKER / PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### ПП РФ №200 от 27.02.2026
- Habr identity matches current legal texts.
- Secondary full text confirms the act approves the Положение on the state information system for countering ICT-enabled offenses and says the act enters into force on the day of official publication.
- Exact primary `publication.pravo.gov.ru` document pointer was not resolved in this pass despite exact-title searches.
- Do not upgrade publication/current status from secondary repositories.
- Status: `PRIMARY_PUBLICATION_POINTER_BLOCKER / PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.
- FULL_TEXT gate: постановление + complete approved Положение.

## New counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +1`
- `GITHUB_FULL_TEXT_BLOCKER +4` (№102 moved from pure no-hit blocker to candidate-with-inspection-blocker)
- `GITHUB_MENTION_ONLY_REJECTED +1`
- `HABR_ATTACHMENT_SET_INCOMPLETE +1`
- `STAGED_EFFECTIVE_BODY_CONFIRMED_2026-07-01 +1`
- `PDF_INTERNAL_IDENTITY_BLOCKER +1`
- `PRIMARY_DIRECT_FETCH_BLOCKER +1`
- `PRIMARY_PUBLICATION_POINTER_BLOCKER +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Gates added / reinforced

1. `SAME_REPO_HAS_NORMATIVE_PDF + EXACT_README_REFERENCE != PDF_IDENTITY_CONFIRMED`.
2. `HABR_PARENTHESES != COMPLETE_SIGNED_PACKAGE`.
3. `IMPLEMENTATION_STAGE != ACT_SUNSET`.
4. `APPROVED_ATTACHMENT_ONLY != COMPLETE_ENACTED_BODY` when operative clauses independently amend other acts.
5. `OFFICIAL_PUBLICATION_POINTER != SUCCESSFUL_PRIMARY_FETCH`.

## Next boundary

Federal Government acts in this Habr GIS/MIS block are complete through item 40. Next direct pass starts with Mincomsvyaz/Minцифры orders in the same section: item 41 — Приказ Минкомсвязи РФ от 25.08.2009 №104; item 42 — Приказ Минкомсвязи России от 31.05.2013 №127; then continue sequentially, while keeping user priority on federal acts, Roskomnadzor and general PDn/information acts.
