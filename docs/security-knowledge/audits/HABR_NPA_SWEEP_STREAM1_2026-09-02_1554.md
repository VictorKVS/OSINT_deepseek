# Habr NPA Sweep — Stream 1 — 2026-09-02 15:54 MSK

## Scope

Systematic continuation of Habr 432466, section `Персональные данные. Примеры внутренних документов`, positions 21–24. GitHub-copy completeness, target identity, legal currentness and official publication status remain separate gates. A GitHub copy is never treated as an official source merely because it reproduces a legal text.

Target boundary (Habr version 28.05.2026):
21. Минюст России от 27.11.2025 № 312 (Минюст № 84408).
22. Минприроды России от 08.12.2025 № 690 (Минюст № 85063).
23. Росжелдор от 27.01.2026 № 65 (Минюст № 85830).
24. Россельхознадзор от 04.03.2026 № 256 (Минюст № 86255).

## New results

### 21. Минюст России от 27.11.2025 № 312

**GitHub full body / reliable body candidate:** not confirmed.
- repo/commit/path/size/type: `null`
- exact number/date/title search: no target body
- registration-number search `84408`: no target body
- publication-ID search `0001202512030003`: no GitHub body

Primary official publication is confirmed directly by `publication.pravo.gov.ru`:
- URL: `https://publication.pravo.gov.ru/document/0001202512030003`
- number/date/title: exact target match
- registration: Минюст России 02.12.2025 № 84408
- publication ID: `0001202512030003`
- publication date: 03.12.2025
- official portal index exposes PDF 507 KB / 10 pages

Secondary full-text reproductions confirm the order contains the order body plus appendices № 1–3 and explicitly repeals the earlier Минюст России order of 21.03.2013 № 36. Secondary lifecycle sources give entry into force 14.12.2025. No later primary consolidated amendment/repeal state was independently closed in this pass.

Classification:
- `GITHUB_FULL_TEXT_BLOCKER`
- `PRIMARY_ORIGINAL_PUBLICATION_CONFIRMED`
- `SUPERSEDES_MINJUST_36_2013`
- `EFFECTIVE_FROM_2025-12-14_SECONDARY_CONFIRMED`
- `PRIMARY_CURRENT_CONSOLIDATED_STATUS_BLOCKER`

### 22. Минприроды России от 08.12.2025 № 690

**GitHub full body / reliable body candidate:** not confirmed.
- repo/commit/path/size/type: `null`
- exact number/date/title search: no target body
- publication-ID: not resolved directly from the primary portal in this pass

A registration-number search produced one false positive:
- repo: `school-tagger/school`
- commit: `f8255740a3d7866bfc425e80a72a54a801ad9364`
- path: `weirdness_uni_bi_tri_clean/join_clean_join_weirdness_file_160_mystem_vopr_del.txt`
- blob: `3034242cc8afd55d8fc47514174500915844cf0b`
- type: `text/plain`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- content: weighted word/phrase statistics; `85063` and `минприроды рф` occur only as unrelated tokens. It fails number/date/title/body identity and is rejected as `SEARCH_NOISE`.

Official-publication reproduction by `Российская газета` confirms:
- exact number/date/title
- registration: Минюст России 26.01.2026 № 85063
- official internet-portal publication date stated as 27.01.2026
- entry into force: 07.02.2026
- signed PDF reproduces the order and its appendix

The reproduced order explicitly repeals Минприроды России order of 17.07.2023 № 431 (Минюст № 74832). The exact `publication.pravo.gov.ru` document ID and direct primary document card were not resolved, so primary publication and current-consolidation remain separate blockers.

Classification:
- `GITHUB_FULL_TEXT_BLOCKER`
- `SEARCH_NOISE_REJECTED`
- `OFFICIAL_PUBLICATION_MIRROR_IDENTITY_CONFIRMED`
- `SUPERSEDES_MINPRIRODY_431_2023`
- `EFFECTIVE_FROM_2026-02-07_OFFICIAL_PUBLISHER_CONFIRMED`
- `PRIMARY_PUBLICATION_ID_OR_DIRECT_CARD_BLOCKER`
- `PRIMARY_CURRENT_CONSOLIDATED_STATUS_BLOCKER`

### 23. Росжелдор от 27.01.2026 № 65

**GitHub full body / reliable body candidate:** not confirmed.
- repo/commit/path/size/type: `null`
- exact number/date/title search: no target body
- publication-ID search `0001202604010024`: no GitHub body

Registration-number search `85830` returned unrelated corporate CSV data and was rejected before candidate promotion because it contains neither the target date/title nor a normative body.

Primary official publication is confirmed on the Roszheldor block of `publication.pravo.gov.ru`:
- target: приказ Росжелдора от 27.01.2026 № 65 `Об организации работы с персональными данными в Федеральном агентстве железнодорожного транспорта и его территориальных органах`
- registration: Минюст России 01.04.2026 № 85830
- publication ID: `0001202604010024`
- publication date: 01.04.2026
- official PDF: 1742 KB / 27 pages

Completeness gate for a future GitHub candidate is the entire official 27-page order package, not a single form or appendix. No later primary consolidated amendment/repeal state was independently closed.

Classification:
- `GITHUB_FULL_TEXT_BLOCKER`
- `SEARCH_NOISE_REJECTED`
- `PRIMARY_ORIGINAL_PUBLICATION_CONFIRMED`
- `PRIMARY_CURRENT_CONSOLIDATED_STATUS_BLOCKER`

### 24. Россельхознадзор от 04.03.2026 № 256

**GitHub full body / reliable body candidate:** not confirmed.
- repo/commit/path/size/type: `null`
- exact number/date/title search: no target body
- publication-ID search `0001202604290008`: no GitHub body

Secondary full-text legal reproductions pass internal identity checks and contain both the order and the approved appendix. They confirm:
- exact number/date/title
- registration: Минюст России 28.04.2026 № 86255
- official publication pointer: `0001202604290008`
- publication date: 29.04.2026
- entry into force: 10.05.2026

Direct opening of `https://publication.pravo.gov.ru/document/0001202604290008` timed out, and exact primary-domain search did not return the card in this pass. Therefore the publication pointer is retained as indirectly resolved rather than promoted to a successfully fetched primary original.

No final later act amending or repealing this exact target was confirmed. Secondary current-text reproductions remain available, but that does not close a primary current-status gate.

Classification:
- `GITHUB_FULL_TEXT_BLOCKER`
- `SECONDARY_FULL_TEXT_IDENTITY_CONFIRMED`
- `OFFICIAL_PUBLICATION_POINTER_INDIRECTLY_RESOLVED`
- `PRIMARY_ORIGINAL_DIRECT_FETCH_BLOCKER`
- `PRIMARY_CURRENT_CONSOLIDATED_STATUS_BLOCKER`

## New duplicates / conflicts / blockers

- `GITHUB_FULL_TEXT_CURRENT = 0`
- `RELIABLE_GITHUB_BODY_CANDIDATE = 0`
- `GITHUB_FULL_TEXT_BLOCKER = 4`
- `SEARCH_NOISE_REJECTED = 2 clusters` (Минприроды № 690; Росжелдор № 65)
- `NEW_GITHUB_FULL_BODY_DUPLICATE = 0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT = 0`
- `SUPERSEDED_PRIOR_AGENCY_PDN_ACT = 2` (Минюст № 36/2013; Минприроды № 431/2023)
- `PRIMARY_ORIGINAL_PUBLICATION_CONFIRMED = 2` (Минюст № 312; Росжелдор № 65)
- `PRIMARY_PUBLICATION_ID_OR_DIRECT_CARD_BLOCKER = 1` (Минприроды № 690)
- `PRIMARY_ORIGINAL_DIRECT_FETCH_BLOCKER = 1` (Россельхознадзор № 256)
- `PRIMARY_CURRENT_CONSOLIDATED_STATUS_BLOCKER = 4`

## Gate discipline

1. An empty GitHub target result is stored as `repo/commit/path/size/type = null`; a word-frequency file or unrelated numeric collision is not promoted to a candidate.
2. Official publication pointer, successful direct fetch of the primary source, and current consolidated legal status remain separate fields.
3. `Российская газета` can confirm an official-publication reproduction and lifecycle date, but it does not replace a successfully fetched `publication.pravo.gov.ru` primary card when that gate is required.
4. Secondary full-text systems may be used to establish internal body identity or find a lifecycle lead, but they do not become official sources.
5. Full-text completeness for multi-appendix agency PDn orders requires the entire order package.

## Next boundary

The Habr section `Персональные данные. Примеры внутренних документов` is closed through position 24. Continue with the next federal/core boundary in `Национальная платежная система`:
- Федеральный закон от 27.06.2011 № 161-ФЗ `О национальной платежной системе`;
- Постановление Правительства РФ от 13.06.2012 № 584.

Keep subsequent Bank of Russia sector acts as a separate banking-regulatory layer unless they are needed to resolve a federal/core dependency.