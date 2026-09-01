# Habr NPA sweep — Stream 1 — 2026-09-01 08:54 MSK

Scope: Habr 432466, section `Государственные и муниципальные информационные системы. Обеспечение безопасности`, positions 1–7.

Method: GitHub copies are discovery evidence only. Official/current status is checked separately. A GitHub object is not promoted to an official source merely because its requisites match.

## Batch summary

- Targets reviewed: 7
- `GITHUB_FULL_TEXT`: 0
- `RELIABLE_GITHUB_CANDIDATE`: 0
- `GITHUB_DETAILED_SUMMARY_REJECTED`: 2
- `GITHUB_DERIVED_IMPLEMENTATION_REJECTED`: 1
- `GITHUB_FULL_TEXT_BLOCKER`: 7
- `NEW_GITHUB_FULL_BODY_DUPLICATE`: 0
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT`: 0
- `TRANSITIONAL_METHODICAL_APPLICABILITY_CONFIRMED_2026`: 1
- `GUIDANCE_LEGAL_BASIS_SUPERSEDED_2026-09-01`: 1
- `PRIMARY_DIRECT_FETCH_BLOCKER`: 5+

## Targets

### 1. Постановление Правительства РФ от 26.03.2025 № 372
Title: `О проведении эксперимента по повышению уровня защищенности государственных информационных систем федеральных органов исполнительной власти и подведомственных им учреждений`.

GitHub search: no full body / no reliable candidate.

`repo=null; commit=null; path=null; size=null; type=null`

Identity/status:
- Official publication pointer corroborated: `0001202503270024`, publication date `2025-03-27`, official PDF reported as 10 pages / 2,012,194 bytes.
- Direct `publication.pravo.gov.ru/document/0001202503270024` fetch timed out in this run: `PRIMARY_DIRECT_FETCH_BLOCKER`.
- Experiment period in the enacted text: `2025-04-01 .. 2027-12-31`; therefore the experiment is active on 2026-09-01.
- A draft amendment prepared in August 2026 proposes extending the experiment scope to GovTech infrastructure. No enacted amending act was confirmed in this run. Class: `DRAFT_AMENDMENT_NOT_EFFECTIVE`.

Completeness gate: `FULL_TEXT = постановление + Положение + форма заявки`.

### 2. Совместный приказ ФСБ России № 416 / ФСТЭК России № 489 от 31.08.2010
Title: `Об утверждении Требований о защите информации, содержащейся в информационных системах общего пользования`, MinJust registration № 18704 dated 2010-10-13.

GitHub search: no target body / no reliable candidate.

`repo=null; commit=null; path=null; size=null; type=null`

Identity is stable across current legal databases and a government regional mirror. A direct current-status primary record from FSB/FSTEC was not resolved in this run.

Class: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

Completeness gate: `FULL_TEXT = совместный приказ + все Требования`.

### 3. Приказ ФСТЭК России от 11.04.2025 № 117
Title exactly matched: `Об утверждении Требований о защите информации, содержащейся в государственных информационных системах, иных информационных системах государственных органов, государственных унитарных предприятий, государственных учреждений`.

GitHub find (rejected as normative body):
- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/ФСТЭК 117.md`
- blob: `b2f7462b50c758bf54433255730aaae27687b025`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `Markdown`
- classification: `DETAILED_SUMMARY / STUDY_NOTES / REJECTED_AS_NORMATIVE_BODY`

The file contains exact number/date/title, a structured digest, clause references and links to an official FSTEC page, but it does not reproduce the complete normative body verbatim.

Primary publication:
- MinJust registration № 82619, 2025-06-16.
- `publication.pravo.gov.ru`: publication number `0001202506170011`, publication date 2025-06-17, PDF 2437 KB / 37 pages.
- direct card fetch timed out: `PRIMARY_DIRECT_FETCH_BLOCKER`.
- entered into force 2026-03-01.

Important lifecycle relation: it replaced FSTEC order №17/2013 and its listed amendments.

Completeness gate: `FULL_TEXT = приказ + Требования + приложение по определению класса защищенности`.

### 4. Методический документ ФСТЭК России `Меры защиты информации в государственных информационных системах`, approved 11.02.2014

GitHub find (rejected as source body):
- repo: `Medovi/information-security-measures`
- commit: `de4c3d698754ef75156b68cc167ec5fda9893ff1`
- path: `suppliers_measures.md`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `Markdown`
- classification: `DERIVED_CONTROL_IMPLEMENTATION / CLAUSE_EXCERPTS / REJECTED_AS_NORMATIVE_BODY`

The repository maps FSTEC control measures to OS interfaces and implementation details and quotes/references sections of the 2014 methodical document. It is an engineering derivative, not the full regulator document.

New applicability confirmation:
- FSTEC information message dated 2026-03-12 № 240/22/1492 explicitly states that, until a new methodical document `Состав и содержание мероприятий и мер по защите информации, содержащейся в информационных системах` is approved, implementations under order FSTEC №117 should continue to use the 11.02.2014 methodical document.
- Therefore repeal of base order №17 does **not** automatically make the 2014 methodical document unusable.

Class: `TRANSITIONAL_METHODICAL_APPLICABILITY_CONFIRMED_2026`.
Gate: `BASE_ORDER_REPEALED != METHODICAL_DOC_AUTOMATICALLY_INAPPLICABLE`.

FSTEC direct official attachment/page was not fetchable in this run: `PRIMARY_REGULATOR_DIRECT_FETCH_BLOCKER`.

### 5. Информационное сообщение ФСТЭК России от 06.03.2015 № 240/22/879
Title: `О банке данных угроз безопасности информации`.

GitHub search: no target body / no reliable candidate.

`repo=null; commit=null; path=null; size=null; type=null`

Type gate: `REGULATOR_INFORMATIONAL_DOCUMENT`, not a registered NPA.

Habr points to the FSTEC primary page, but the direct regulator URL failed due robots/cache in this run. Secondary full reproductions confirm the requisites and body. Class: `PRIMARY_REGULATOR_DIRECT_FETCH_BLOCKER`.

### 6. Информационное сообщение ФСТЭК России от 22.06.2017 № 240/22/3031
Title: `О порядке рассмотрения и согласования моделей угроз безопасности информации и технических заданий на создание государственных информационных систем`.

GitHub search: no target body / no reliable candidate.

`repo=null; commit=null; path=null; size=null; type=null`

Type gate: `REGULATOR_INFORMATIONAL_DOCUMENT`, not a registered NPA.

New 2026-09-01 legal-basis conflict:
- the 2017 message expressly explained coordination using then-current point 3 of Government Resolution №676/2015;
- Government Resolution №813 of 01.07.2026, effective **2026-09-01**, rewrites point 3 of Resolution №676 into a recommendation for local self-government bodies and removes the old wording used as the immediate basis in the 2017 explanation;
- therefore the 2017 message must not be treated as a self-sufficient current legal basis for mandatory coordination without re-checking current №676 and current FSTEC requirements.

Class: `GUIDANCE_LEGAL_BASIS_SUPERSEDED_2026-09-01`.
Gate: `REGULATOR_INFORMATIONAL_MESSAGE != IMMUTABLE_CURRENT_LEGAL_BASIS`.

This is **not** classified as formal repeal of the information message: `FORMAL_REPEAL_NOT_CONFIRMED`.

### 7. Приказ ФСБ России от 18.03.2025 № 117
Title exactly matched: `Об утверждении Требований о защите информации, содержащейся в государственных информационных системах, иных информационных системах государственных органов, государственных унитарных предприятий, государственных учреждений, с использованием шифровальных (криптографических) средств`.

GitHub find (rejected as normative body):
- repo: `Javert5555/obsidian_vault`
- commit: `ee8fe087d2c36718e594dbe3f7033043b39aca9a`
- path: `Курс 5/право/Приказ 117.md`
- blob: `6aa291fa8115417c99260edf81b97460540767e4`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `Markdown`
- classification: `DETAILED_SUMMARY / STUDY_NOTES / REJECTED_AS_NORMATIVE_BODY`

The note contains a detailed interpretation and tables, not the complete verbatim order and Requirements.

Primary publication:
- MinJust registration № 81647, 2025-03-26.
- `publication.pravo.gov.ru`: publication number `0001202503260008`, publication date 2025-03-26, PDF 493 KB / 11 pages.
- direct primary card fetch timed out: `PRIMARY_DIRECT_FETCH_BLOCKER`.
- entered into force 2025-04-06.
- it formally repealed FSB order №524/2022 from its effective date.

Completeness gate: `FULL_TEXT = приказ + полностью Требования + приложения/таблицы, если включены в официальное опубликование`.

## New confirmed events only

1. `GITHUB_DETAILED_SUMMARY_REJECTED +2` — FSTEC №117/2025 and FSB №117/2025.
2. `GITHUB_DERIVED_IMPLEMENTATION_REJECTED +1` — 2014 FSTEC measures document.
3. `TRANSITIONAL_METHODICAL_APPLICABILITY_CONFIRMED_2026 +1` — 2014 methodical document remains the instructed interim implementation basis under FSTEC clarification №240/22/1492.
4. `GUIDANCE_LEGAL_BASIS_SUPERSEDED_2026-09-01 +1` — 2017 message №240/22/3031 cites an old point 3 of PP №676 that was rewritten by PP №813 effective today.
5. `FORMAL_REPEAL_NOT_CONFIRMED +1` — do not convert the previous item into a false repeal claim.
6. `NEW_GITHUB_FULL_BODY_DUPLICATE +0`.
7. `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`.

## Next boundary

Continue with Habr section `Государственные и муниципальные информационные системы. Открытые данные`: Government Order №1187-р/2013 and the 2014 open-data methodological recommendations, then continue to the next federal/general blocks. Regional-only Moscow Oblast acts are outside the primary Stream-1 federal/common priority unless needed for duplicate/conflict handling.
