# Habr NPA sweep — Stream 1 — 2026-08-29 22:56 MSK

## Delta

- `GITHUB_FULL_TEXT +2`
- `BODY_IDENTITY_CONFIRMED +2`
- `REJECTED_REFERENCE_ONLY +1`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `TEMPORAL_CONFLICT_RESOLVED +1`
- `PRIMARY_CURRENT_CONSOLIDATED_BODY_DIRECT_FETCH_BLOCKER +2`
- `EXACT_DUPLICATE +0`
- `BODY_IDENTITY_CONFLICT +0`

## New confirmed GitHub full texts

### Federal Law 27.07.2006 No. 152-FZ — On Personal Data

GitHub artifact:

- repo: `Grantik/odin-vault`
- commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
- path: `sync/canon/law/fz_152_personalnye_dannye_20060727_kremlin.txt`
- size: `53084` bytes
- type: `TXT/file`
- blob: `0ee9df5244483bf4d6559d5244236b664528c22d`
- URL: https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/law/fz_152_personalnye_dannye_20060727_kremlin.txt

Body identity was checked inside the file. The header contains `ФЕДЕРАЛЬНЫЙ ЗАКОН / О ПЕРСОНАЛЬНЫХ ДАННЫХ`, adoption by the State Duma on 08.07.2006 and approval by the Federation Council on 14.07.2006. The tail contains Article 25 and the signature block `Президент Российской Федерации В.Путин / Москва, Кремль / 27 июля 2006 года / № 152-ФЗ`. The file contains the statute body, not a reference list or notes. The amendment header includes `26.07.2026 № 265-ФЗ`.

Classification: `GITHUB_FULL_TEXT_CONFIRMED / BODY_IDENTITY_CONFIRMED / NON_OFFICIAL_GITHUB_COPY`.

Official-source separation:

- The official Kremlin document bank confirms the base act identity and title: https://www.kremlin.ru/acts/bank/24154/print
- The Kremlin consolidated print currently indexed by search only lists amendments through 28.02.2025 No. 23-FZ, so it is not sufficient to prove the current 29.08.2026 consolidated body.
- Federal Law 26.07.2026 No. 265-FZ directly amends Article 12 of 152-FZ. The Russian Gazette text states that the law generally enters into force on the day of official publication, while Article 2 alone enters into force on 01.09.2027. Therefore the Article 12 amendments are already operative by 29.08.2026. Direct `publication.pravo.gov.ru` card for No. 265-FZ was not resolved in this pass.

Status gate: `PRIMARY_IDENTITY_CONFIRMED / CURRENT_AMENDMENT_CORROBORATED / PRIMARY_CURRENT_CONSOLIDATED_BODY_DIRECT_FETCH_BLOCKER`.

### Federal Law 27.07.2006 No. 149-FZ — On Information, Information Technologies and Protection of Information

GitHub artifact:

- repo: `Grantik/odin-vault`
- commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
- path: `sync/canon/law/fz_149_informacia_20060727_kremlin.txt`
- size: `216712` bytes
- type: `TXT/file`
- blob: `4e5b966d04918ecbe2a93ce6e30c2319a979b2c9`
- URL: https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/law/fz_149_informacia_20060727_kremlin.txt

Body identity was checked inside the file. The header contains `ФЕДЕРАЛЬНЫЙ ЗАКОН / ОБ ИНФОРМАЦИИ, ИНФОРМАЦИОННЫХ ТЕХНОЛОГИЯХ И О ЗАЩИТЕ ИНФОРМАЦИИ`, adoption on 08.07.2006 and approval on 14.07.2006. The tail contains the presidential signature block `Москва, Кремль / 27 июля 2006 года / N 149-ФЗ`. The amendment list includes 29.12.2025 No. 569-FZ and 2026 acts through 26.06.2026 No. 210-FZ.

Classification: `GITHUB_FULL_TEXT_CONFIRMED / BODY_IDENTITY_CONFIRMED / NON_OFFICIAL_GITHUB_COPY`.

Official-source separation:

- The official Kremlin document bank confirms No. 149-FZ identity and title: https://special.kremlin.ru/acts/bank/24157/page/2
- Official publication portal directly confirms 29.12.2025 No. 568-FZ, publication No. `0001202512290056`, and 29.12.2025 No. 569-FZ, publication No. `0001202512290057`.
- No. 568-FZ is published but enters into force only on 01.09.2026. On 29.08.2026, omission of No. 568-FZ from a text intended to represent the operative edition does not by itself prove staleness.
- A direct current consolidated primary body for No. 149-FZ was not resolved in this pass.

Status gate: `PRIMARY_IDENTITY_CONFIRMED / CURRENT_IN_FORCE_FLOOR_CORROBORATED_THROUGH_210-FZ_26.06.2026 / FUTURE_EFFECTIVE_568-FZ_TRACKED_SEPARATELY / PRIMARY_CURRENT_CONSOLIDATED_BODY_DIRECT_FETCH_BLOCKER`.

## New rejected candidate

### 123-FZ — Moscow AI experiment amendments

GitHub search for `123-ФЗ` together with the Moscow AI-experiment title language returned only the 152-FZ file above. Inside that file, 123-FZ occurs in the amendment history of 152-FZ; it is not the body of the target 123-FZ.

Classification: `REFERENCE_IN_AMENDMENT_LIST / NOT_TARGET_BODY / REJECT`.

## New GitHub full-text blockers

No reproducible target body was confirmed for the following acts in this pass:

- 160-FZ — ratification of the Council of Europe Convention on protection of individuals with regard to automated processing of personal data;
- 242-FZ — On State Genomic Registration in the Russian Federation;
- 367-FZ — mutual legal assistance / personal-data related act from the user/Habr sweep set;
- Presidential Decree 30.05.2005 No. 609 — personal data of a state civil servant and maintenance of the personal file;
- Government Resolution 06.07.2008 No. 512 — requirements for material carriers of biometric personal data and storage technologies outside personal-data information systems;
- Government Resolution 15.09.2008 No. 687 — specifics of personal-data processing without automation tools.

For these blocker rows: `repo/commit/path/size/type = null`. Search-zero is not treated as proof that no GitHub artifact exists; tree/path and binary traversal remain required.

## New corpus gates

1. `FULL_BODY_IDENTITY_CONFIRMED != OFFICIAL_COPY` — a complete GitHub text remains a non-official copy until official-source status is tracked separately.
2. `REFERENCE_IN_CONSOLIDATED_ACT != TARGET_BODY` — an act number in an amendment history is only a reference, not the referenced act body.
3. `AMENDMENT_LIST_MEMBER != AMENDMENT_IN_FORCE` — amendment lists and legal effect dates are stored separately.
4. `PUBLISHED_FUTURE_EFFECTIVE_AMENDMENT_OMISSION != STALE` — a copy of the currently operative edition is not automatically stale merely because it omits an already published amendment that has not yet entered into force.

## Next search priority

Continue tree/path traversal and binary discovery for 160-FZ, 242-FZ, 367-FZ, Decree No. 609, Government Resolutions No. 512 and No. 687; for 149-FZ and 152-FZ, separately close the `PRIMARY_CURRENT_CONSOLIDATED_BODY` gate rather than treating the GitHub copy as official.
