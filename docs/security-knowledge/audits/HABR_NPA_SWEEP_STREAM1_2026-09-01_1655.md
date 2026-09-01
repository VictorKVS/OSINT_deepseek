# Habr NPA sweep — Stream 1 — 2026-09-01 16:55 MSK

## Scope

Systematic pass over Habr article 432466, KII positions 42–49. Position 49 is an exact duplicate of position 48, therefore this run contains seven unique target documents/materials:

1. Минпромторг России — справочный материал «Перечни типовых объектов КИИ».
2. Информационное сообщение ФСТЭК России от 12.03.2025 № 240/82/672.
3. Методические рекомендации Минздрава России по категорированию объектов КИИ сферы здравоохранения, версия 1.0, утв. 05.04.2021.
4. Методические рекомендации Минтранса России по категорированию объектов КИИ, функционирующих в сфере транспорта, утв. 24.01.2024.
5. Письмо Минэнерго России от 28.02.2024 № 15-203.
6. Методические рекомендации Минобрнауки России по категорированию объектов КИИ, функционирующих в сфере науки, утв. 21.02.2025.
7. Информационное сообщение ФСТЭК России от 22.10.2025 № 240/84/3451.

## GitHub evidence

### 1. Минпромторг — sectoral typical-object lists

Found only a derivative educational/reference mention:

- repo: `pikov-vitaliy/pikov-expert-lectures`
- commit: `3743195404811ac9c3468c948bc4e78c67b56561`
- path: `risk/materials.md`
- size: `184214 B`
- type: `Markdown`
- blob: `d71ef1d775fa4616b1186b0de63d58bec48550cc`
- classification: `MENTION_ONLY / EDUCATIONAL_REFERENCE / REJECTED_AS_NORMATIVE_BODY`

The file is lecture material and explicitly instructs readers to verify normative status using official sources. It is not the body of the Minpromtorg sectoral lists.

### 2. ФСТЭК № 240/82/672

No indexed full text or reliable GitHub candidate found in this pass.

`repo=null / commit=null / path=null / size=null / type=null`

### 3. Минздрав methodology 05.04.2021

Found only a derivative blog article:

- repo: `BuminAI/hospital-ai-lab`
- commit: `492734551264d504e4ce5cf43122e237e377c394`
- path: `src/content/blog-ru/2026-08-31-medicinskie-sistemy-ii-rezhim-kii-187-fz.md`
- size: `9549 B`
- type: `Markdown`
- blob: `980351fcfc8eb8da35d4237544e28b22a1dc93fe`
- classification: `MENTION_ONLY / BLOG_SUMMARY / REJECTED_AS_NORMATIVE_BODY`

The GitHub file correctly identifies the health-sector KII methodology but does not reproduce the full 175-page recommendation body.

### 4. Минтранс methodology 24.01.2024

No indexed full text or reliable GitHub candidate found in this pass.

`repo=null / commit=null / path=null / size=null / type=null`

### 5. Минэнерго letter № 15-203

No indexed full text or reliable GitHub candidate found in this pass.

`repo=null / commit=null / path=null / size=null / type=null`

### 6. Минобрнауки methodology 21.02.2025

No indexed full text or reliable GitHub candidate found in this pass.

`repo=null / commit=null / path=null / size=null / type=null`

### 7. ФСТЭК № 240/84/3451

No indexed full text or reliable GitHub candidate found in this pass.

`repo=null / commit=null / path=null / size=null / type=null`

## New confirmed status / lifecycle findings

### Habr exact duplicate

Positions 48 and 49 contain the same FSTEK information message dated 22.10.2025 № 240/84/3451 with the same title and target link.

Classification: `HABR_EXACT_DUPLICATE`.

This is a source-list duplication only; it is not a duplicate GitHub full body.

### Minzdrav 2021 methodology

The primary Minzdrav-hosted PDF is reachable and internally identifies the document as the 2021 health-sector KII categorization recommendations, version 1.0, 175 pages, approved 05.04.2021. The document is methodological guidance rather than a registered normative legal act.

Classification: `NON_NPA_METHODICAL_GUIDANCE`.

A 2025 draft Government resolution on binding sector-specific KII categorization rules for healthcare was found, but this pass did not resolve a signed and officially published final healthcare resolution as of 2026-09-01.

Blocker: `FINAL_SIGNED_SECTOR_RULES_HEALTHCARE_BLOCKER`.

No formal withdrawal of the 2021 recommendations was confirmed.

### Mintrans 2024 methodology

The document is methodological guidance, not a registered NPA. A 2025 draft Government resolution on binding sector-specific KII categorization rules for transport was found, but this pass did not resolve a signed and officially published final transport resolution as of 2026-09-01.

Classification: `NON_NPA_METHODICAL_GUIDANCE`.

Blocker: `FINAL_SIGNED_SECTOR_RULES_TRANSPORT_BLOCKER`.

No formal withdrawal of the 2024 recommendations was confirmed.

### Minobrnauki 2025 methodology vs PP № 246/2026

The 21.02.2025 science methodology explicitly has a recommendatory character. A later binding Government act now exists: Government Resolution № 246 dated **07.03.2026**, “Об утверждении отраслевых особенностей категорирования объектов критической информационной инфраструктуры Российской Федерации в сфере науки”, officially published 07.03.2026 as `0001202603070013` and effective from 15.03.2026.

Classification: `GUIDANCE_LAYER_PRECEDES_BINDING_SECTOR_RULES_2026`.

Gate: `NON_NPA_GUIDANCE_CANNOT_OVERRIDE_PP246_2026`.

No formal withdrawal of the 2025 methodology was confirmed.

Metadata correction: PP № 246 is dated **07.03.2026**. Any earlier local record containing `06.03.2026` must be corrected.

### Primary-source blockers

- Minpromtorg typical-object lists: `PRIMARY_MINPROMTORG_DIRECT_FETCH_BLOCKER` (official target timed out in this pass).
- FSTEK № 240/82/672: `PRIMARY_REGULATOR_DIRECT_FETCH_BLOCKER`.
- FSTEK № 240/84/3451: `PRIMARY_REGULATOR_DIRECT_FETCH_BLOCKER`.
- Minobrnauki 21.02.2025 methodology: `PRIMARY_MINOBRNAUKI_ORIGINAL_BLOCKER`.

Secondary copies/summaries are not promoted to official-source status.

## Counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_MENTION_ONLY_REJECTED +2`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `HABR_EXACT_DUPLICATE +1`
- `GUIDANCE_LAYER_PRECEDES_BINDING_SECTOR_RULES_2026 +1`
- `PREVIOUS_METADATA_CORRECTION_PP246_DATE +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Next boundary

Continue from Habr KII positions 50–51:

- FSTEK methodological document dated 11.11.2025: «Методика оценки показателя состояния технической защиты информации в информационных системах и обеспечения безопасности значимых объектов критической информационной инфраструктуры Российской Федерации».
- Rosatom order dated 20.03.2026 № 1/9-НПА.

Then proceed to the Habr subsection `Критическая информационная инфраструктура. Связь`.