# Habr NPA sweep — Stream 1 — 2026-08-29 01:10 MSK

Scope: only new confirmed findings, conflicts, duplicates, and blockers from the current pass over Habr 432466 + the user NPA list.

## New confirmed finding

### Federal Law No. 152-FZ of 27.07.2006 — «О персональных данных»

GitHub candidate:
- repository: `MobileCommerceLab/privacy_law_corpus`
- commit: `1d791bb64741f86f8cc160485dc005230f720042`
- path: `corpus_documents/plain_text_files/non_english_text_files/Russia (Federal Law of 27 July 2006 No. 152-FZ on Personal Data).txt`
- size: `77,293 bytes`
- type: `TXT/blob`
- blob SHA: `f610587af16b721aa9544978d9de653d3e192bbf`

Body-level identity check: PASS.
- body contains `ФЕДЕРАЛЬНЫЙ ЗАКОН`;
- body contains `27 июля 2006 года N 152-ФЗ`;
- exact title `О ПЕРСОНАЛЬНЫХ ДАННЫХ` is present;
- structure reaches Article 25;
- terminal signature block is present: President of the Russian Federation, V. Putin, Moscow/Kremlin, 27 July 2006, No. 152-FZ.

Completeness classification: `FULL_TEXT` for this historical consolidated Russian-language copy, not a mention or a summary.

Revision check: the file's amendment chain ends with Federal Law No. 519-FZ of 30.12.2020. Its Article 12 also retains the older Council-of-Europe-Convention wording. Therefore this GitHub copy is not current.

Official-status/currentness check is separate from GitHub:
- the official `ips.pravo.gov.ru` text independently confirms the legal identity of 152-FZ and contains a substantially later amendment chain through 2025;
- Federal Law No. 265-FZ of 26.07.2026 subsequently amends Article 12 of 152-FZ, confirming that the 2020 GitHub consolidation is stale.

Classification:
`FULL_TEXT / RUSSIAN / NON_OFFICIAL_GITHUB_COPY / CONSOLIDATED_THROUGH_519-FZ_2020 / STALE_CONFIRMED / NOT_CURRENT`

## Duplicate / conflict result

- exact duplicate: none; the previously found English translated copy has a different blob SHA, so it is a language sibling, not a byte-identical duplicate.
- body identity conflict: none for this file.

## Blocker update

Closed: `GITHUB_FULL_TEXT_RU_152-FZ` — a self-contained Russian full-text GitHub copy is now confirmed.

Still open: `GITHUB_CURRENT_CONSOLIDATED_RU_152-FZ` — no current Russian GitHub consolidation is confirmed in this pass.

Primary-source lifecycle note: the official IPS copy proves the 2020 GitHub text stale. The separate direct `publication.pravo.gov.ru` card for the 26.07.2026 amendment was not reliably resolved during this pass; do not promote the GitHub file to `CURRENT` or `OFFICIAL` on that basis.