# Habr NPA sweep — Stream 1

Date boundary: 2026-09-01 (Europe/Moscow)

Scope: Habr 432466, section «Государственные и муниципальные информационные системы (ГИС и МИС)», positions 8 and 10–15. Priority pass: presidential acts and Government of the Russian Federation acts. GitHub copies are treated only as non-official discovery candidates; official status/currentness is checked separately.

## Batch targets and normalized GitHub result

| Target | GitHub normative candidate | Classification |
|---|---|---|
| Указ Президента РФ 09.07.2025 №467 «О государственном информационном ресурсе “Цифровой профиль иностранного гражданина”» | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 18.05.2009 №424 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 24.11.2009 №953 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 08.09.2010 №697 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 08.06.2011 №451 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 28.11.2011 №977 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER |
| ПП РФ 26.06.2012 №644 | repo=null; commit=null; path=null; size=null; type=null | GITHUB_FULL_TEXT_BLOCKER / REPEALED_ACT |

No GitHub result in this batch passed the full-body + internal identity gate.

## New rejected GitHub hits

| Target | repo | commit | path | size | type | result |
|---|---|---|---|---:|---|---|
| Указ №467/2025 | agisota/diffs | caccd7e745a1a4c915dc73c7e7169df74dd58902 | migration_v9_integral/04_машинные_приложения/01_реестр_источников.csv | 11316 | CSV | MENTION_ONLY / SOURCE_REGISTRY / REJECTED_AS_NORMATIVE_BODY |
| ПП №953/2009 | alekseypetrow/alekseypetrow.github.io | d4cd23c2688401af40e251f5ba6f39e85d00113f | README.md | 105333 | Markdown | MENTION_ONLY / README_NOTES / REJECTED_AS_NORMATIVE_BODY |
| ПП №697/2010 | avkazmin/sphinx_munidoc | 5f6300a4c2b16598d4f3c7462d49b43cb121baf1 | doc/reglament9.rst | 134036 | RST | MENTION_ONLY / MUNICIPAL_REGULATION / REJECTED_AS_NORMATIVE_BODY |
| ПП №697/2010 | avkazmin/sphinx_munidoc | 5f6300a4c2b16598d4f3c7462d49b43cb121baf1 | doc/reglament20.rst | 112358 | RST | MENTION_ONLY / MUNICIPAL_REGULATION / same mention group |
| ПП №977/2011 | Drunken-Shogun/systems-analyst-knowledge-base | 939f82413f480b69ebd2b9101566e7b9a1464f51 | Системный анализ/Углубленный разбор/Анализ документации.md | 155509 | Markdown | MENTION_ONLY / KNOWLEDGE_BASE / REJECTED_AS_NORMATIVE_BODY |
| ПП №644/2012 | artyom-zolotarevskiy/ru-gpt-3-training-legal | bd0edd5446d2ce94f15d976d34d339dd6f924f35 | decisions__data/14826.txt | 23247 | TXT | MENTION_ONLY / COURT_DECISION_CORPUS / REJECTED_AS_NORMATIVE_BODY |

For the two avkazmin files this is `MENTION_DUPLICATE_GROUP`, not a duplicate of a normative body.

## Official/currentness findings

### Указ Президента РФ №467 от 09.07.2025

Primary official publication is confirmed: publication number `0001202507090019`, publication date 09.07.2025, official PDF 490 KB / 9 pages.

Primary: https://publication.pravo.gov.ru/document/0001202507090019

`FULL_TEXT` requires the decree and the complete approved list of information. Initial official publication is confirmed; a separate primary consolidated-current-status check remains open.

### ПП РФ №424 от 18.05.2009

Identity is corroborated, but no GitHub normative body was found. A primary consolidated-current-status card was not closed in this pass.

Status: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### ПП РФ №953 от 24.11.2009 — Habr title is stale/incomplete

The current title includes the phrase `подведомственных ему организаций`: «Об обеспечении доступа к информации о деятельности Правительства Российской Федерации, подведомственных ему организаций и федеральных органов исполнительной власти». Habr still gives the older/shorter title.

Latest confirmed amendment in this pass: ПП РФ 07.04.2025 №450; it enters into force from 01.01.2026.

Class: `HABR_TITLE_STALE_OR_INCOMPLETE`, same act identity, not a different act.

Current secondary card: https://www.consultant.ru/document/cons_doc_LAW_94194/

Amending act: https://www.consultant.ru/document/cons_doc_LAW_502728/

`FULL_TEXT` is not just the resolution: it includes all approved information lists and the technological/software/linguistic requirements. Primary publication ID for №450 remains unresolved in this pass.

### ПП РФ №697 от 08.09.2010 — current edition advanced in 2026

Current corroborated edition is 23.04.2026. ПП РФ 23.04.2026 №462 directly amends №697; official publication pointer: `0001202604230040`.

Primary amendment publication: https://publication.pravo.gov.ru/document/0001202604230040

Current secondary card: https://www.consultant.ru/document/cons_doc_LAW_104665/

A Government-hosted consolidated copy encountered in the pass was older and only reflected amendments through №1687 of 30.10.2025. Therefore: `OFFICIAL_GOVERNMENT_CONSOLIDATION_STALE_VS_LATER_PUBLICATION`. A host being official does not make every cached consolidated text the newest available legal state.

`FULL_TEXT` requires the resolution plus the complete Regulation on SMEV.

### ПП РФ №451 от 08.06.2011

Latest confirmed amending act in this pass is ПП РФ 01.11.2025 №1735 «О внесении изменений в некоторые акты Правительства Российской Федерации», officially published 03.11.2025 under `0001202511030013`.

Primary amendment publication: https://publication.pravo.gov.ru/document/0001202511030013

No GitHub normative body found. `FULL_TEXT` requires the resolution plus the approved Regulation.

### ПП РФ №977 от 28.11.2011

Currentness is corroborated to edition 23.03.2024 in this pass; no later change was confirmed. This is not promoted to primary-current confirmation solely because no later amendment was found.

Status: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

`FULL_TEXT` requires the resolution plus all Requirements for ESIA.

### ПП РФ №644 от 26.06.2012 — critical Habr lifecycle conflict

The act is no longer current. ПП РФ 01.07.2024 №900 approved the new IT-asset accounting regime and its repeal list includes №644. Under paragraph 6 of №900, points 2–6 of the repeal list entered into force on 01.01.2025; №644 is point 2.

Official Government card for №900: https://government.ru/docs/all/154144/

Current secondary confirmation for №644 marks the document as repealed/cancelled: https://www.consultant.ru/document/cons_doc_LAW_131858/

Class: `HABR_REPEALED_ACT_CONFLICT`. Habr simultaneously lists obsolete №644 and current №900 in the same GIS/MIS section. Do not model №900 as a strict one-to-one rename: it is a new/current IT-asset accounting regime that explicitly repeals №644.

Historical `FULL_TEXT` for №644 requires resolution + full Regulation. Current №900 corpus requires resolution + Regulation + amendments + repeal list.

## Counters for this batch

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `GITHUB_MENTION_ONLY_REJECTED +5` target-level hits
- `MENTION_DUPLICATE_GROUP +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_TITLE_STALE_OR_INCOMPLETE +1`
- `CURRENT_EDITION_ADVANCED_2026 +1`
- `OFFICIAL_GOVERNMENT_CONSOLIDATION_STALE_VS_LATER_PUBLICATION +1`
- `HABR_REPEALED_ACT_CONFLICT +1`

## Gates added/confirmed

- `OFFICIAL_HOST_CAN_BE_STALE != CURRENT_PRIMARY_CONSOLIDATION`
- `CURRENT_TITLE_CAN_CHANGE_WITHOUT_ACT_IDENTITY_CHANGE`
- `HABR_LISTING_REPEALED_ACT_ALONGSIDE_CURRENT_REGIME`
- `OFFICIAL_INITIAL_PUBLICATION != OFFICIAL_CURRENT_CONSOLIDATION`
- `NO_LATER_AMENDMENT_FOUND != PRIMARY_CURRENT_STATUS_CONFIRMED`
- `GITHUB_MENTION_OR_REFERENCE != NORMATIVE_BODY`
- `FULL_TEXT_COMPONENTS_REQUIRED`

## Next boundary

Continue GIS/MIS from Habr position 16: ПП РФ 10.07.2013 №584, ПП РФ 31.07.2014 №747, распоряжение Правительства РФ 29.12.2014 №2769-р, ПП РФ 06.07.2015 №675, ПП РФ 06.07.2015 №676, ПП РФ 14.11.2015 №1235; then continue federal/Presidential/Government/Roskomnadzor/general PDn-information priority.