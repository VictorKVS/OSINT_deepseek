# Habr NPA sweep — Stream 1 — 2026-08-31 17:56 MSK

Scope continued from prior boundary: Habr 432466 / user NPA list. Targets in this pass: 98-FZ (commercial secret), Law 395-1 (banks), 224-FZ (insider information), 176-FZ (postal communication), 126-FZ (communications).

## Rules applied

- GitHub copy is never treated as an official source automatically.
- FULL_TEXT requires normative body, not TOC/index/mention/summary.
- Identity is checked independently by number/date/title inside the candidate.
- Currentness/lifecycle is checked independently from official or regulator sources; prepared future editions are separated from currently effective text.

## GitHub candidate register

| Target | repo | commit | path | size | type | blob | classification | identity/currentness note |
|---|---|---|---|---:|---|---|---|---|
| 98-FZ 29.07.2004 | null | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER | Search produced only non-normative mentions/corpus material. |
| Law 395-1 02.12.1990 | IvanchikIvanov/ZkonRf | 2ed96981f48397751ce05f735315b3b82302802c | data/codexes/ru/zpp_395_1_banks.txt | 27525 | TXT | 31b0fe57c9f9875763a17b9315e1977fb6d53250 | RELIABLE_IDENTITY_AND_STRUCTURE_CANDIDATE / TOC_OR_INDEX_DATASET / NOT_FULL_TEXT / NONOFFICIAL_GITHUB_COPY | Internal identity matches 02.12.1990 N 395-1 and title. Amendment list in this file ends at 09.04.2026 N 86-FZ, so it is not a current 2026 lifecycle snapshot. |
| 224-FZ 27.07.2010 | null | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER | One apparent hit was actually another legal body (KoAP) and one was a news corpus mention. |
| 176-FZ 17.07.1999 | null | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER | No reliable normative body located. |
| 126-FZ 07.07.2003 | edekeulenaar/global-digital-regulations | 633e8261d64910a2dc8913a1cfd8faa7fe78314c | data/policies/2240.md | UNRESOLVED_CONNECTOR_METADATA | Markdown | 4729ca67baa9ca2e1bcc25631e3f2589db63ad7d | RELIABLE_IDENTITY_AND_STRUCTURE_CANDIDATE / TOC_OR_INDEX_DATASET / NOT_FULL_TEXT / NONOFFICIAL_GITHUB_COPY | Header/identity matches 07.07.2003 N 126-FZ. Body is mainly amendment list + chapter/article index, not full article text. Amendment list reaches 20.02.2026 N 33-FZ; later enacted future changes are absent. Size remains a connector metadata blocker. |

### Rejected GitHub hits

1. `len0va/ntplgt@f339f7307f625c4b85c349213154e63b66ca69b7:susp/01194.txt` — mentions/discusses 98-FZ in a corpus-like text; `MENTION_ONLY / REJECTED_AS_NORMATIVE_BODY`.
2. `edekeulenaar/global-digital-regulations@633e8261d64910a2dc8913a1cfd8faa7fe78314c:data/policies/2245.md` — apparent 224-FZ hit, but fetched body is KoAP RF; `BODY_IDENTITY_MISMATCH / REJECTED`.
3. `krikyn/Strong-Paraphrase-Generation-2020@3d5b6f4fd0d4b4f96ed6bdd91b7000d3d80fc901:download/v1/6183.txt` — news/paraphrase corpus mentioning insider-law subject; `MENTION_ONLY / REJECTED_AS_NORMATIVE_BODY`.

## Official/currentness verification

### 98-FZ — commercial secret

- Consolidated legal sources show edition 08.08.2024.
- 251-FZ of 08.08.2024 is the latest confirmed amending act in this pass; corroborated official publication number: `0001202408080046`.
- Direct primary consolidated current-card was not resolved in this pass, therefore status remains `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### Law 395-1 — banks and banking activity

- Current legal systems already display a prepared edition dated 04.08.2026 because 283-FZ of 04.08.2026 directly amends Law 395-1.
- 283-FZ is enacted but takes effect on 01.09.2026; corroborated official publication pointer: `0001202608040008`.
- Therefore on 31.08.2026 the 283-FZ changes must remain a separate `ENACTED_FUTURE_CHANGE_2026-09-01` layer and must not overwrite the current-effective body.
- Additional future staged provisions also exist (for example a change to Art. 26 effective 01.09.2026 from 425-FZ/2025), so a flat `latest_text` field is unsafe.

### 224-FZ — insider information / market manipulation

- Consolidated legal sources show edition 08.08.2024.
- Bank of Russia enforcement on 20.08.2026 directly applies Part 2 Article 6 of 224-FZ, confirming operational use by the primary regulator in 2026.
- This is `CURRENT_OPERATIONAL_USE_CORROBORATED_BY_PRIMARY_REGULATOR`, not a substitute for a primary consolidated current text; `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER` remains.

### 176-FZ — postal communication

- Legal systems show a prepared edition dated 26.07.2026 after 271-FZ.
- 271-FZ directly amends 176-FZ but its principal effective date is 01.03.2027; therefore `PREPARED_EDITION_2026-07-26 != CURRENT_EFFECTIVE_BODY_2026-08-31`.
- GitHub search produced no reliable normative candidate.

### 126-FZ — communications

- Current legal systems show base edition 20.02.2026 with enacted changes entering into force from 01.09.2026.
- Additional enacted changes from 210-FZ/26.06.2026 and 271-FZ/26.07.2026 include later staged effective dates (notably 01.03.2027 for relevant communications provisions).
- The GitHub file `data/policies/2240.md` is structurally useful for identity/indexing but is not normative full text and does not represent the complete lifecycle queue.

## New conflicts / blockers / gates

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_STRUCTURE_CANDIDATE +2`
- `GITHUB_MENTION_ONLY_REJECTED +2`
- `GITHUB_BODY_IDENTITY_MISMATCH_REJECTED +1`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `GITHUB_STRUCTURE_CANDIDATE_STALE_OR_LIFECYCLE_INCOMPLETE +2`
- `GITHUB_INTERNAL_EDITION_METADATA_OR_SCOPE_CONFLICT +1` (126-FZ candidate is labeled as latest while it is only an indexed snapshot and lacks later enacted lifecycle edges)
- `ENACTED_FUTURE_CHANGE_LAYER +2` (395-1 / 126-FZ)
- `PREPARED_FUTURE_EDITION_NOT_CURRENT_BODY +2` (395-1 / 176-FZ)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_CONFIRMED_HABR_IDENTITY_CONFLICT +0`

New gates:

1. `NUMBER_DATE_TITLE_MATCH != FULL_TEXT`.
2. `TOC_OR_INDEX_DATASET != NORMATIVE_BODY`.
3. `PREPARED_CONSOLIDATED_EDITION != CURRENT_EFFECTIVE_BODY`.
4. `ENACTED_FUTURE_AMENDMENT != EFFECTIVE_TODAY`.
5. `PRIMARY_REGULATOR_ENFORCEMENT_CONFIRMS_OPERATIONAL_USE != PRIMARY_CONSOLIDATED_TEXT`.
6. `GITHUB_COPY_CURRENTNESS_AND_OFFICIAL_STATUS_MUST_BE_VERIFIED_SEPARATELY`.

## Next boundary

Continue Habr section `Защита связи`: Government Resolutions 538/27.08.2005, 532/25.06.2009, 1194/14.11.2014, then continue federal/Presidential/Government/Roskomnadzor/general PDn-information priorities from the user list.