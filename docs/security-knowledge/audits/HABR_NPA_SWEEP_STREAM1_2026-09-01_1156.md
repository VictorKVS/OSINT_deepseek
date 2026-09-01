# Habr NPA sweep — Stream 1 — 2026-09-01 11:56 MSK

Scope: Habr 432466, section «Критическая информационная инфраструктура (КИИ)», positions 8–14.

Targets:
1. Постановление Правительства РФ от 16.01.2026 № 4 — отраслевые особенности категорирования КИИ в области атомной энергии.
2. Постановление Правительства РФ от 06.02.2026 № 92 — банковская сфера и иные сферы финансового рынка.
3. Распоряжение Правительства РФ от 26.02.2026 № 360-р — перечень типовых отраслевых объектов КИИ РФ.
4. Постановление Правительства РФ от 07.03.2026 № 246 — сфера науки.
5. Постановление Правительства РФ от 23.03.2026 № 303 — государственная регистрация прав на недвижимое имущество и сделок с ним.
6. Постановление Правительства РФ от 31.03.2026 № 356 — ракетно-космическая промышленность.
7. Постановление Правительства РФ от 13.04.2026 № 402 — сфера связи.

## GitHub body search

For all seven targets, exact searches by number/date/title plus distinctive-title searches returned no full normative body and no reliable candidate on the indexed default branches.

Result for every target in this pass:

- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: GITHUB_FULL_TEXT_BLOCKER

Counters:

- GITHUB_FULL_TEXT +0
- RELIABLE_GITHUB_CANDIDATE +0
- GITHUB_FULL_TEXT_BLOCKER +7
- NEW_GITHUB_FULL_BODY_DUPLICATE +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT +0

Important: absence from GitHub search is not treated as evidence that no copy exists outside indexed/default branches.

## Primary official publication identity

Official publication pointers resolved:

- PP №4/2026 — publication.pravo.gov.ru/document/0001202601160013; publication date 2026-01-16.
- PP №92/2026 — publication no. 0001202602070010; publication date 2026-02-07; official index reports PDF 4172 KB / 17 pages.
- RP №360-р/2026 — publication.pravo.gov.ru/document/0001202602260020; publication date 2026-02-26.
- PP №246/2026 — publication no. 0001202603070013; publication date 2026-03-07; PDF 2450 KB / 10 pages.
- PP №303/2026 — publication no. 0001202603240036; publication date 2026-03-24; PDF 1320 KB / 6 pages.
- PP №356/2026 — publication no. 0001202604010039; publication date 2026-04-01; PDF 1646 KB / 8 pages.
- PP №402/2026 — publication.pravo.gov.ru/document/0001202604130022; publication date 2026-04-13.

Direct fetch of several publication.pravo.gov.ru cards timed out during the pass. Keep OFFICIAL_PUBLICATION_POINTER_CONFIRMED separate from PRIMARY_DIRECT_FETCH_OK.

## New confirmed lifecycle/status findings

### RP №360-р/2026 — current body advanced after initial publication

Current consolidated legal sources show edition 2026-05-27 after RP Government №1237-р of 27.05.2026. The amendment changes the approved list, including rewording position 98 and excluding position 99.

Classification:
- CURRENT_EDITION_ADVANCED_2026-05-27
- ORIGINAL_2026-02-26_BODY_IS_OLD_EDITION
- FULL_TEXT_CURRENT_REQUIRES_CONSOLIDATED_LIST_AFTER_1237-R

The official FSTEC resource currently exposes №360-р with the amendment marker «в ред. распоряжения Правительства РФ от 27.05.2026 №1237-р», which corroborates current use by the regulator. Exact primary publication pointer for №1237-р was not resolved in this pass.

Blocker:
- PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER (№1237-р)

### PP №402/2026 — effective layer activated today

The act text states that PP №402 enters into force on 2026-09-01 and remains in force until 2032-09-01. Therefore as of this pass it changes from FUTURE_EFFECTIVE to CURRENT_EFFECTIVE.

Classification:
- CURRENT_EFFECTIVE_ACTIVATED_2026-09-01
- BUILT_IN_SUNSET_2032-09-01

Gate:
- PUBLISHED_ACT != CURRENT_EFFECTIVE_BEFORE_EFFECTIVE_DATE
- EFFECTIVE_DATE_ACTIVATION_MUST_BE_REEVALUATED_ON_DATE_BOUNDARY

No GitHub copy found; any future candidate must contain both the постановление and the complete approved отраслевые особенности.

## Remaining targets in this batch

PP №4/2026, №92/2026, №246/2026, №303/2026 and №356/2026: identity is confirmed against official publication indexes; no new amendment/repeal conflict was confirmed during this pass. Do not infer current status merely from failure to find an amending act.

Status gate retained for all five:
- PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER where no directly fetched official consolidated current card is available.

Completeness gate for every sectoral PP:
- FULL_TEXT = operative постановление + complete approved «Отраслевые особенности» annex.
- Operative part alone, overview, commentary, implementation article, or excerpt = PARTIAL/MENTION_ONLY, not FULL_TEXT.

## Habr status

Habr 432466 contains positions 8–14 with the same identities. New Habr-relevant lifecycle note: RP №360-р is now a later-edition target (27.05.2026), and PP №402 becomes effective exactly on 01.09.2026.

No new Habr duplicate or title/body identity conflict confirmed in this batch.

## Sources checked

- Habr 432466: https://habr.com/ru/articles/432466/
- Official publication portal: https://publication.pravo.gov.ru/
- FSTEC official resource for RP №360-р: https://fstec.ru/en/dokumenty/vse-dokumenty/rasporyazheniya/rasporyazhenie-pravitelstva-rossijskoj-federatsii-ot-26-fevralya-2026-g-n-360-r
- Secondary consolidation used only to detect current-edition/lifecycle candidates, never as automatic official status: ConsultantPlus / ZakonRF / Garant.

## Delta counters

- CURRENT_EDITION_ADVANCED_2026 +1 (RP №360-р)
- CURRENT_EFFECTIVE_ACTIVATED_2026-09-01 +1 (PP №402)
- BUILT_IN_SUNSET_CONFIRMED +1 (PP №402)
- PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER +1 (RP №1237-р/2026)
- GITHUB_FULL_TEXT +0
- RELIABLE_GITHUB_CANDIDATE +0
- NEW_GITHUB_FULL_BODY_DUPLICATE +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT +0

Next boundary: KII positions 15+ beginning with FSB Russia order №539/2025, followed by FSTEC/FSB KII acts.