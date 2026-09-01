# Habr NPA sweep — Stream 1 — 2026-09-01 10:55 MSK

Scope: Habr 432466, section **Критическая информационная инфраструктура (КИИ)**, positions 1–7.

Targets:
1. Федеральный закон от 26.07.2017 № 187-ФЗ.
2. Указ Президента РФ от 30.03.2022 № 166.
3. «Основные направления государственной политики в области обеспечения безопасности автоматизированных систем управления производственными и технологическими процессами критически важных объектов инфраструктуры Российской Федерации», утв. Президентом РФ 03.02.2012 № 803.
4. Постановление Правительства РФ от 08.02.2018 № 127.
5. Постановление Правительства РФ от 17.02.2018 № 162.
6. Постановление Правительства РФ от 08.06.2019 № 743.
7. Постановление Правительства РФ от 22.08.2022 № 1478.

## GitHub body/candidate sweep

| Target | repo | commit | path | size | type | classification | identity result |
|---|---|---|---|---:|---|---|---|
| 187-ФЗ | `BEaStia/legal-raggy` | `5d509da1f44bd43866d14b21adb45e446438415e` | `data/raw/laws/187fz_kii.md` | 3269 B | Markdown | `BODY_IDENTITY_CONFLICT / MISLABELED_FILE / REJECTED_AS_NORMATIVE_BODY` | filename/front matter say 187-ФЗ, but body is **Приказ Росимущества от 25.09.2014 №367** |
| 187-ФЗ archive | `BEaStia/legal-raggy` | `5d509da1f44bd43866d14b21adb45e446438415e` | `data/raw/laws/archive/187fz_kii_20.11.2015.md` | 3971 B | Markdown | `MANUAL_EXCERPT / REJECTED_AS_FULL_TEXT` | front matter itself says `manual excerpt for MVP`; filename date 20.11.2015 predates enactment of 187-ФЗ |
| Указ 166 | — | — | — | — | — | `NO_RELIABLE_GITHUB_BODY_FOUND` | exact hits were training notes / link lists only |
| документ 803/2012 | — | — | — | — | — | `NO_RELIABLE_GITHUB_BODY_FOUND` | exact search returned no body candidate |
| ПП 127/2018 | — | — | — | — | — | `NO_RELIABLE_GITHUB_BODY_FOUND` | exact hits were summaries, link lists, or mentions inside regional OCR |
| ПП 162/2018 | — | — | — | — | — | `NO_RELIABLE_GITHUB_BODY_FOUND` | exact hit was a training summary only |
| ПП 743/2019 | — | — | — | — | — | `NO_RELIABLE_GITHUB_BODY_FOUND` | exact search returned no body candidate; number-only search is collision-prone |
| ПП 1478/2022 | — | — | — | — | — | `NO_RELIABLE_GITHUB_BODY_FOUND` | exact hits were notes/thesis references only |

### New GitHub quality finding

`BEaStia/legal-raggy/data/raw/laws/187fz_kii.md` is a confirmed false positive that would pass a filename/front-matter-only intake gate. The body contradicts the metadata: it contains Rosimushchestvo order №367/2014, not 187-ФЗ. Blob SHA: `5f2dbcac072e884ce066311a568726561e3eee82`.

The adjacent archive file is not a normative body either: it is explicitly a manually prepared MVP excerpt. Its filename contains `20.11.2015`, an impossible edition date for a law adopted on 26.07.2017.

New gates:
- `METADATA_IDENTITY != BODY_IDENTITY`
- `FILENAME_DATE < ACT_DATE => REJECT_VERSION_METADATA`
- `MANUAL_EXCERPT != FULL_TEXT`

## Official identity / currency layer

### 187-ФЗ
- Primary original publication confirmed: `0001201707260023`, 26.07.2017, exact number/date/title.
- Current consolidated base-act text found as **ред. от 07.04.2025**.
- The amending Federal Law №58-ФЗ of 07.04.2025 has itself been amended and is currently **ред. от 26.07.2026**; Federal Law №265-ФЗ of 26.07.2026 rewrote part 4 of article 2 of №58-ФЗ concerning temporary regional features of applying clauses 5 and 6 of part 3 of article 9 of 187-ФЗ through 2030.
- Therefore operational currency must store two separate layers: `BASE_ACT_CURRENT_EDITION=2025-04-07` and `AMENDING_ACT_TRANSITIONAL_LAYER_CURRENT_EDITION=2026-07-26`.
- Gate: `AMENDING_ACT_LATER_AMENDED != BASE_ACT_EDITION_CHANGED`.
- Primary publication of №58-ФЗ confirmed: `0001202504070004`, 07.04.2025. Exact primary publication pointer for №265-ФЗ was not resolved in this pass; secondary sources confirm official publication on 26.07.2026.

### Указ Президента №166/2022
- Primary original publication confirmed: `0001202203300001`, 30.03.2022.
- Current consolidated edition: **07.04.2025**.
- Latest amendment primary publication closed: Указ Президента №214 от 07.04.2025, publication `0001202504070002`, 07.04.2025, 1 page.
- No reliable GitHub body found.

### Документ №803/2012
- Habr identity matches the presidentially approved policy document title/date/number.
- Reliable GitHub body not found.
- Direct primary Security Council original/current source could not be resolved in this pass.
- Blockers: `PRIMARY_SECURITY_COUNCIL_ORIGINAL_DIRECT_FETCH_BLOCKER`, `PRIMARY_CURRENT_STATUS_BLOCKER`.

### ПП №127/2018
- Primary original publication confirmed for the 08.02.2018 act.
- Current consolidated edition advanced to **07.11.2025** after ПП РФ №1762.
- Official publication pointer for №1762 is corroborated as `0001202511080017`; direct fetch of the official portal timed out.
- Any GitHub copy predating 07.11.2025 is `OLD_EDITION` even if text-complete for its historical date.
- `FULL_TEXT_CURRENT` completeness requires: постановление + Правила категорирования + complete перечень показателей критериев значимости and their values.
- Blocker: `PRIMARY_LATEST_AMENDMENT_DIRECT_FETCH_BLOCKER`.

### ПП №162/2018
- Exact current legal text remains discoverable without an edition marker; no later amendment/repeal confirmed in this pass.
- Reliable GitHub body not found.
- Exact primary publication pointer/current primary consolidated status not resolved.
- Blockers: `PRIMARY_PUBLICATION_POINTER_BLOCKER`, `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### ПП №743/2019
- Exact act remains present in current legal indexes; no later amendment/repeal confirmed in this pass.
- Reliable GitHub body not found.
- Search by `743` alone produces heavy cross-year numeric collisions.
- New gate: `NUMBER_ONLY_SEARCH_UNSAFE`.
- Blockers: `PRIMARY_PUBLICATION_POINTER_BLOCKER`, `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### ПП №1478/2022
- Original publication identity corroborated: publication `0001202208260051`, publication date 26.08.2022, 20 pages.
- Current consolidated edition: **17.10.2023**, after ПП РФ №1716.
- No reliable GitHub body found.
- `FULL_TEXT_CURRENT` requires all three approved normative blocks, not only the operative decree text: (1) software requirements, (2) rules for coordinating purchases of foreign software/services, (3) rules for transition to predominant use of Russian software.
- Gate: `FULL_TEXT_PP1478_REQUIRES_ALL_THREE_APPROVED_BLOCKS`.
- Latest-amendment primary publication pointer for №1716 remains unresolved in this pass.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `GITHUB_BODY_IDENTITY_CONFLICT +1`
- `GITHUB_MANUAL_EXCERPT_REJECTED +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `CURRENT_EDITION_ADVANCED_PP127_2025 +1`
- `AMENDING_ACT_TRANSITIONAL_LAYER_ADVANCED_2026 +1`
- `PRIMARY_LATEST_AMENDMENT_POINTER_CLOSED_DECREE166 +1`

## Source anchors

- Habr 432466 KII section: https://habr.com/ru/articles/432466/
- 187-ФЗ primary publication: https://publication.pravo.gov.ru/Document/View/0001201707260023
- Указ 166 primary publication: https://publication.pravo.gov.ru/Document/View/0001202203300001
- Указ 214 primary publication ID: `0001202504070002`
- ФЗ 58 primary publication ID: `0001202504070004`
- PP 127 current reference: https://www.consultant.ru/document/cons_doc_LAW_290595/
- PP 1478 current reference: https://www.consultant.ru/document/cons_doc_LAW_425279/

## Next boundary

Continue Habr KII positions 8–14: ПП РФ №4/2026, №92/2026, распоряжение №360-р/2026, ПП №246/2026, №303/2026, №356/2026, №402/2026; then FSB/FSTEC KII orders.