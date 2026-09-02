# Habr NPA sweep — Stream 1 — 2026-09-02 09:56 MSK

Scope: Habr 432466, section `Персональные данные. Особые случаи обработки ПДн`, positions 11–15. GitHub copies are evidence/candidates only and are never promoted to official sources. Current status/edition is checked separately.

## Batch summary

| # | Target | GitHub result | Identity / completeness | Current / official gate | Conflict / blocker |
|---|---|---|---|---|---|
| 11 | 173-ФЗ от 10.12.2003 «О валютном регулировании и валютном контроле» | No full body. Representative derived hit: `basvandorst/where-is-satoshi@0b579f41a829ff2d1fd46d0a1d9a811d275ddc9f`, `data/testlist-cpunks/buh_wcore_ru.txt`, blob `bc94c7c2940bb2b4f6b94747c81251f3a55c360d`, size `UNRESOLVED_CONNECTOR_METADATA`, `text/plain` | Seminar announcement. Contains exact law number/title only as a bullet; no law articles/body. `MENTION_ONLY / SEMINAR_ANNOUNCEMENT / REJECTED_AS_NORMATIVE_BODY` | Current consolidated edition: 04.08.2026, based on 283-ФЗ. Official publication of 283-ФЗ: `0001202608040008`, 04.08.2026. Changes entered into force 01.09.2026. | `GITHUB_FULL_TEXT_BLOCKER`; `POST_HABR_CURRENT_EDITION_ADVANCE`; official publication pointer confirmed, direct primary page fetch was unstable/time-out in this run. |
| 12 | 177-ФЗ от 23.12.2003 | No full body. Representative hit: `infoculture/finguide@d87540a90eb23c17e56ab1f3e8364615df0efa52`, `wiki/glossary/org-types/state-corporations.md`, 21,723 B, Markdown, blob `27b2f02a82103a6a1aaac6431c09a423eba24656` | Glossary/table mention only; not law body. It still uses the former title «О страховании вкладов физических лиц в банках Российской Федерации». `MENTION_ONLY / GLOSSARY_RECORD / REJECTED_AS_NORMATIVE_BODY` | Current title: «О страховании вкладов в банках Российской Федерации»; current consolidated edition: 31.07.2025 (changes effective through 14.12.2025). Newly signed 317-ФЗ of 04.08.2026 changes 177-ФЗ but enters into force only after 180 days, i.e. 01.02.2027. Official publication: `0001202608040042`. | `HABR_STALE_TITLE_177FZ`; `GITHUB_DERIVED_STALE_TITLE`; `SIGNED_FUTURE_LAYER_317 / EFFECTIVE_FROM_2027-02-01`; `GITHUB_FULL_TEXT_BLOCKER`. |
| 13 | 79-ФЗ от 27.07.2004 «О государственной гражданской службе Российской Федерации» | No full body. Representative hit: `mperestoronin/ethical_index_HW6_special@a702a55ba73b640cae33e15e164ad848600374f2`, `app_config/npa.py`, 21,590 B, Python, blob `3e98f8bb8f506e211deb73daa3f97d963216379c` | NPA registry/config entry only; no normative articles. `MENTION_ONLY / NPA_REGISTRY_ENTRY / REJECTED_AS_NORMATIVE_BODY` | Current edition: 08.03.2026. 52-ФЗ of 08.03.2026 directly changes part 5 of article 15; official publication `0001202603080008`; entered into force after 90 days, 07.06.2026. | `GITHUB_FULL_TEXT_BLOCKER`; current layer is already effective. |
| 14 | 125-ФЗ от 22.10.2004 «Об архивном деле в Российской Федерации» | No full body. Reliable bibliographic pointer: `SpectralOne/bmstu-diploma@f933ac17e53d8d35636d1ebc94bf138e370bf593`, `nir-7sem/bibliography.bib`, 5,937 B, BibTeX/text, blob `7a5964a4ed0a5397eb90aa5f0b2d9ec6d9012336` | Exact number/date/title plus link to `pravo.gov.ru/proxy/ips/?docbody=&nd=102089077`; bibliography only. `BIBLIOGRAPHIC_POINTER / REJECTED_AS_NORMATIVE_BODY` | Current edition: 13.12.2024. Latest amendment 469-ФЗ of 13.12.2024; official publication `0001202412130022`. | `GITHUB_FULL_TEXT_BLOCKER`; no post-Habr edition advance found. |
| 15 | 402-ФЗ от 06.12.2011 «О бухгалтерском учете» | **Full multi-file old edition found**: `dei-s/law@f21d61aa01bce14505a3fd55b0bfc5fd47197686`, `rf/fl/402/{0,1,2,3,4}.md`, total 137,785 B, Markdown. Blobs: `0.md=1ffa06149751110a40d7ee424f79543805b0c199` (4,457 B); `1.md=46c5465fb02430a24291baa39b2f38867b7dc040` (10,930 B); `2.md=19a9e9dd4190c8ca60b218d086d1ca19d208167e` (58,293 B); `3.md=850e6b03f944bfe3319ec017ba9b7cd88b014d1a` (51,717 B); `4.md=2f1b6fc972328c7edc0119067978bde775c07c5b` (12,388 B). | Exact number/date/title. `0.md` identifies edition based on amendments through 26.07.2019; `1–4.md` contain articles 1–32 including final article 32. `9.md` in the same folder is a Ministry of Finance information note and is explicitly excluded from the law body. `GITHUB_FULL_TEXT_MULTI_FILE_OLD_EDITION / NON_OFFICIAL_COPY` | Current edition: 15.12.2025 after 471-ФЗ; official publication of 471-ФЗ: `0001202512150036`. Separate signed future layer: 263-ФЗ of 23.07.2025 changes article 21 from 01.01.2027; publication pointer `0001202507230068`. | GitHub copy is complete but obsolete (2019 edition), not official. `SIGNED_FUTURE_LAYER_263 / EFFECTIVE_FROM_2027-01-01`. |

## Primary / authoritative status references

- Habr 432466, version 28.05.2026: https://habr.com/ru/articles/432466/
- 283-ФЗ official publication: https://publication.pravo.gov.ru/document/0001202608040008
- 317-ФЗ official publication: https://publication.pravo.gov.ru/document/0001202608040042
- 52-ФЗ official publication: https://publication.pravo.gov.ru/document/0001202603080008
- 469-ФЗ official publication: https://publication.pravo.gov.ru/document/0001202412130022
- 471-ФЗ official publication: https://publication.pravo.gov.ru/document/0001202512150036
- 263-ФЗ publication pointer: `0001202507230068`; effective 01.01.2027.

## Counters for this batch

- `GITHUB_FULL_TEXT_CURRENT +0`
- `GITHUB_FULL_TEXT_MULTI_FILE_OLD_EDITION +1`
- `GITHUB_FULL_TEXT_BLOCKER +4`
- `GITHUB_MENTION_OR_BIBLIOGRAPHIC_REJECTED +4`
- `HABR_STALE_TITLE +1`
- `POST_HABR_CURRENT_EDITION_ADVANCE +1`
- `SIGNED_FUTURE_LAYER +2`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Next boundary

Habr positions 16–18 in this section: 230-ФЗ от 03.07.2016; 168-ФЗ от 08.06.2020; ПП РФ №1723 от 09.10.2021. Positions 19–20 are a Moscow regional law and a Ministry of Finance explanatory letter; treat separately from the federal/core NPA track.
