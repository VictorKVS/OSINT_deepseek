# Habr NPA sweep — Stream 1 — 2026-09-02 00:52 MSK

## Scope

Continuation of the systematic pass over Habr article 432466 and the user NPA list. This pass covers the first six entries of the `Персональные данные (ПДн)` section:

1. Federal Law 19.12.2005 No. 160-FZ (ratification of Convention 108).
2. Federal Law 27.07.2006 No. 152-FZ `О персональных данных`.
3. Federal Law 03.12.2008 No. 242-FZ `О государственной геномной регистрации в Российской Федерации`.
4. Federal Law 24.04.2020 No. 123-FZ (AI experiment / PDn amendments).
5. Federal Law 19.11.2021 No. 367-FZ (ratification of the agreement on mutual legal assistance in administrative matters in the field of personal-data exchange).
6. Presidential Decree 30.05.2005 No. 609 (personal data of a state civil servant / personal file).

Control rule remains unchanged: **`GITHUB_COPY != OFFICIAL_SOURCE`**. GitHub is used to discover and fingerprint copies. Identity, current edition and official status are checked independently against primary/official publication sources where available.

## New GitHub findings

| Target | repo | commit/ref | path | size | type | body classification | internal identity / edition result |
|---|---|---|---|---:|---|---|---|
| 160-FZ/2005 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | No indexable full body or reliable candidate confirmed in this pass. |
| 152-FZ/2006 | `Lilya-te/barko-docs` | `7fc86075540bfb8e3b9d51a15b1de6d140f900d1` | `152 ФЗ.md` | 236561 B | Markdown | `GITHUB_FULL_TEXT_CURRENT / NON_OFFICIAL_COPY` | Body begins with exact act identity and contains the complete law through Art. 25. Amendment history reaches Federal Law 26.07.2026 No. 265-FZ. |
| 152-FZ/2006 | `ValekusVachpekus/pdn-control` | `545586a8a0650d07e1298a6325027f167a4ff80f` | `backend/resources/fz_152.txt` | 232118 B | text/plain | `GITHUB_FULL_TEXT_OLD_EDITION / NON_OFFICIAL_COPY` | Exact 152-FZ body, but internal edition marker is 24.06.2025; therefore superseded by the 2026-07-26 edition. |
| 242-FZ/2008 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | No indexable full body or reliable candidate confirmed in this pass. |
| 123-FZ/2020 | `MobileCommerceLab/privacy_law_corpus` | `1d791bb64741f86f8cc160485dc005230f720042` | `corpus_documents/plain_text_files/non_english_text_files/Russia (Federal Law of 24 April 2020 No. 123-FZ on the Experiment to Establish Special Regulation in Order to Create the Necessary Conditions for the Development and Implementation of Artificial Intelligence Technologies...).txt` | `UNRESOLVED_CONNECTOR_METADATA` | text/plain | `GITHUB_FULL_TEXT_OLD_EDITION / ORIGINAL_2020_BODY / NON_OFFICIAL_COPY` | Exact number/date/original title; terminal Art. 8 is present. The file is the original 2020 body and does not represent the post-233-FZ current title/content. |
| 367-FZ/2021 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | No indexable full body or reliable candidate confirmed in this pass. |
| Presidential Decree 609/2005 | `buba1477/multik_bot` | `e8e0c46feb0d4a7feadafc934920825bed808f7d` | `embendings/Об утверждении Положения о персональных данных.md` | 36246 B | Markdown | `GITHUB_FULL_TEXT_CURRENT / NON_OFFICIAL_COPY` | Exact decree identity; includes the decree and approved Regulation. Header says `По состоянию на 09.04.2026 г.` and amendment history reaches Presidential Decree 31.12.2025 No. 1009, which independently amends Decree No. 609. |

### 152-FZ duplicate/edition result

Two complete bodies were confirmed, but they are not byte-identical and are not the same edition:

- `Lilya-te/barko-docs` — current edition marker through 26.07.2026 No. 265-FZ.
- `ValekusVachpekus/pdn-control` — older edition marker 24.06.2025.

Classification: **`GITHUB_FULL_TEXT_EDITION_DUPLICATE +1`**, not `BYTE_DUPLICATE` and not `BODY_IDENTITY_CONFLICT`.

## Official/current-status verification

### 152-FZ

Federal Law 26.07.2026 No. 265-FZ changes Article 12 of 152-FZ. The official/publication layer confirms No. 265-FZ as the latest amendment identified in this pass. Its general provisions enter into force from official publication; only Article 2 of No. 265-FZ has a separate 01.09.2027 effective date. Therefore this pass records:

- `CURRENT_EDITION_152FZ = 2026-07-26`;
- `GITHUB_CURRENT_COPY_MATCHES_LATEST_AMENDMENT_IDENTITY = true` for the Lilya-te copy;
- **no assumption that the GitHub file is official**;
- `PRIMARY_PORTAL_DIRECT_FETCH_BLOCKER` remains for a directly fetched official consolidated 152-FZ body.

### 242-FZ

Federal Law 08.03.2026 No. 52-FZ directly amends 242-FZ. Official publication number: `0001202603080008`, publication date 08.03.2026. No. 52-FZ enters into force after 90 days; the confirmed effective date is **07.06.2026**. Thus, as of this sweep:

- `CURRENT_EDITION_ADVANCED_242FZ_2026-03-08`;
- `CURRENT_EFFECTIVE_LAYER_52FZ = 2026-06-07`;
- any GitHub copy lacking the No. 52-FZ changes must be marked `OLD_EDITION`.

### 123-FZ

Federal Law 08.08.2024 No. 233-FZ (`0001202408080031`) amended both 152-FZ and 123-FZ. In particular it expanded the **title** of 123-FZ by adding the regional anonymized-data composition/access layer. Relevant provisions took effect 01.09.2025. Habr version 28.05.2026 still displays the original 2020 title.

Classification:

- `HABR_STALE_TITLE_123FZ +1`;
- `CURRENT_EDITION_123FZ = 2024-08-08`;
- `CURRENT_EXPANDED_TITLE_EFFECTIVE_LAYER = 2025-09-01`;
- the MobileCommerceLab body is a valid full historical body, but **not current**.

### Presidential Decree No. 609

Presidential Decree 31.12.2025 No. 1009 explicitly amends the Regulation approved by Decree 30.05.2005 No. 609, including repeal/rewording of provisions. The GitHub copy above carries the amendment history through No. 1009 and therefore is classified as current for the checked edition, while remaining a non-official copy.

Classification: `CURRENT_EDITION_ADVANCED_609_2025-12-31 +1`.

### 160-FZ and 367-FZ

No GitHub full body/reliable candidate was confirmed. Identity is known from the Habr target and secondary legal indexes, but direct primary-original retrieval was not completed in this pass. Conservative blockers retained:

- 160-FZ: `PRIMARY_RUSSIAN_ORIGINAL_DIRECT_FETCH_BLOCKER`.
- 367-FZ: `PRIMARY_PUBLICATION_POINTER_BLOCKER`.

No inference of repeal/current treaty operation is made from absence of contrary material.

## New counters

- `GITHUB_FULL_TEXT_CURRENT +2` — 152-FZ (2026 edition), Decree 609 (through No. 1009).
- `GITHUB_FULL_TEXT_OLD_EDITION +2` — 152-FZ (2025 edition), 123-FZ (original 2020 body).
- `GITHUB_FULL_TEXT_EDITION_DUPLICATE +1` — two complete 152-FZ editions.
- `GITHUB_FULL_TEXT_BLOCKER +3` — 160-FZ, 242-FZ, 367-FZ.
- `HABR_STALE_TITLE +1` — 123-FZ.
- `CURRENT_EDITION_ADVANCED_152_2026-07-26 +1`.
- `CURRENT_EDITION_ADVANCED_242_2026-03-08 +1`.
- `CURRENT_EDITION_ADVANCED_609_2025-12-31 +1`.
- `NEW_GITHUB_BYTE_DUPLICATE +0`.
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`.

## Blockers carried forward

1. Direct official consolidated 152-FZ body is not yet pinned as a primary fetched artifact in this pass; latest amending act is separately verified.
2. No GitHub full body for 160-FZ, 242-FZ, 367-FZ.
3. Exact GitHub byte size for the MobileCommerceLab 123-FZ corpus object was not exposed by the connector metadata in this pass; blob/body identity is known, so size remains explicitly unresolved instead of being guessed.
4. Direct primary Russian original/publication pointer for 160-FZ and exact primary pointer for 367-FZ remain unresolved.

## Next boundary

Continue the PDn section from Habr positions 7+:

- Presidential Decree 29.12.2012 No. 1709;
- Presidential Decree 24.11.2014 No. 735;
- CIS Agreement 18.12.2020;
- then Government Resolution 06.07.2008 No. 512 and the subsequent Government/Roskomnadzor PDn layer.

All cross-section repeats must be deduplicated against prior sweep records rather than counted again.
