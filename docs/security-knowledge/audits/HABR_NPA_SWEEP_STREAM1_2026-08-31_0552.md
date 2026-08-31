# Habr NPA sweep — Stream 1 — 2026-08-31 05:52 MSK

Scope: Habr 432466, section `Системообразующие документы`, positions 5–9 (excluding Civil Code parts): Federal Law №149-ФЗ/2006, Presidential Decree №188/1997, Federal Law №294-ФЗ/2008, Federal Law №247-ФЗ/2020, Federal Law №258-ФЗ/2020.

Habr reference: https://habr.com/ru/articles/432466/ (version shown by the article: 28.05.2026).

## GitHub search summary

No accepted full normative body or reliable body candidate was confirmed for any of the five targets in this pass.

For each target the accepted-body metadata remains:
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Search-result hygiene:
- №149-ФЗ full-title/body-phrase searches produced policy/reference pages and a lexical wordlist hit (`ninastoessinger/word-o-mat`, commit `13f0e55fbb1eb1e897e2f14f23aad9928a3fc6d4`, `word-o-mat.roboFontExt/resources/russian.txt`). Fetching the file confirms it is a Leipzig-derived Russian word-frequency list, not a law body. Classification: `FALSE_POSITIVE_LEXICAL_CORPUS / REJECT_NOT_LEGAL_BODY`.
- №247-ФЗ and №294-ФЗ both hit the same file `AxHulk/osp-kavkaz-ing`, commit `b902d3e57875c53d2c284e3e257fefc7f8d5e9e9`, path `src/pages/Accreditation.tsx`. Body inspection shows only a list of applicable documents containing exact names/numbers of №247-ФЗ and №294-ФЗ. It is not a reproduction of either law. Classification for both: `MENTION_ONLY / SAME_GITHUB_REFERENCE_PAGE / REJECT_AS_FULL_TEXT`.
- №258-ФЗ exact-title search returned no accepted body candidate.
- Presidential Decree №188 exact number/date/title search returned no accepted body candidate.

## 1. Federal Law 27.07.2006 №149-ФЗ — information / information technologies / protection of information

Identity:
- Habr position 5 has correct number, date and current title.
- Current consolidated legal sources show edition dated 26.06.2026.

Current / next-effective state:
- the amendment chain for the current consolidated edition includes Federal Law 26.06.2026 №210-ФЗ; official-publication pointer corroborated as `0001202606260070`, publication date 26.06.2026.
- Federal Law 29.12.2025 №568-ФЗ is primary-confirmed on publication.pravo.gov.ru: publication ID `0001202512290056`, publication date 29.12.2025. It enters into force on **01.09.2026**.
- Federal Law 29.12.2025 №569-ФЗ is primary-confirmed: publication ID `0001202512290057`, publication date 29.12.2025. Point 2 of article 1 (changes to article 14.2 of №149-ФЗ) enters into force on **01.09.2026**; other parts had earlier dates.
- As of 31.08.2026 this means the corpus must keep `CURRENT_EFFECTIVE_BODY_2026-08-31` separate from `ENACTED_FUTURE_BODY_EFFECTIVE_2026-09-01` even though the consolidated edition marker is 26.06.2026.

State:
`CURRENT_EDITION_2026-06-26_CORROBORATED / PRIMARY_FUTURE_AMENDMENTS_568_569_CONFIRMED / NEXT_DAY_EFFECTIVE_CHANGE_2026-09-01 / GITHUB_FULL_TEXT_BLOCKER`.

New gate: `CONSOLIDATED_EDITION_DATE != ALL_PROVISIONS_EFFECTIVE_NOW`.

## 2. Presidential Decree 06.03.1997 №188 — confidential-information list

Identity:
- Habr number/date/title match the target decree.

Lifecycle/currentness:
- the latest amendment identified in this pass is Presidential Decree 13.07.2015 №357.
- primary official publication is confirmed: `0001201507130003`, published 13.07.2015; its official title explicitly states that it amends the confidential-information list approved by Decree №188/1997.
- current legal-reference copies corroborate edition 13.07.2015; no later amendment was established in this pass.
- because the 1997 source predates the modern publication portal and a primary consolidated current card was not resolved, do not label the current status `PRIMARY_CURRENT_STATUS_VERIFIED`.

State:
`PRIMARY_LATEST_AMENDMENT_CONFIRMED_2015-07-13 / CURRENT_EDITION_2015-07-13_CORROBORATED / PRIMARY_CURRENT_STATUS_BLOCKER / GITHUB_FULL_TEXT_BLOCKER`.

## 3. Federal Law 26.12.2008 №294-ФЗ — protection of businesses during state/municipal control

GitHub:
- the only useful indexed hit in this pass is the `AxHulk/osp-kavkaz-ing` accreditation page noted above. It contains an exact bibliographic mention only; no articles/normative body.

Currentness:
- current legal copies show edition 29.12.2025 and provisions effective in 2026.
- Federal Law 29.12.2025 №548-ФЗ directly amends №294-ФЗ. Primary official publication confirmed: `0001202512290036`, 29.12.2025.
- №548-ФЗ extends application of relevant №294-ФЗ provisions for specified control/notification regimes through **31.12.2028**.
- therefore №294-ФЗ must not be globally marked repealed merely because Federal Law №248-ФЗ became the principal modern control framework.

State:
`CURRENT_EDITION_2025-12-29_CORROBORATED / PRIMARY_LATEST_AMENDMENT_548_2025_CONFIRMED / LIMITED_CONTINUED_APPLICABILITY_TO_2028-12-31 / GITHUB_FULL_TEXT_BLOCKER`.

New gate: `FRAMEWORK_SUPERSEDED_IN_CORE_SCOPE != WHOLE_ACT_REPEALED`.

## 4. Federal Law 31.07.2020 №247-ФЗ — mandatory requirements

GitHub:
- same `AxHulk/osp-kavkaz-ing` file as №294-ФЗ; bibliographic mention only, not body. This is a cross-target duplicate mention page and is not counted as a full-text duplicate.

Identity / publication:
- Habr number/date/title are correct.
- primary initial publication confirmed: `0001202007310002`, 31.07.2020.

Currentness:
- current consolidated legal sources show edition **26.06.2026**.
- the modifying list identifies Federal Law 26.06.2026 №215-ФЗ as the latest amendment; its official-publication pointer is `0001202606260075`, 26.06.2026.
- a separate interaction with №149-ФЗ matters from 01.09.2026: amended №569-ФЗ provides that certain mandatory-requirement acts under parts 5 and 7 of article 14.2 of №149-ФЗ are exempt from part 1 of article 3 of №247-ФЗ. This is a cross-act applicability exception, not repeal of №247-ФЗ.

State:
`PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_EDITION_2026-06-26_CORROBORATED / LATEST_AMENDMENT_215_2026_PUBLICATION_POINTER_CORROBORATED / CROSS_ACT_EXCEPTION_WITH_149FZ / GITHUB_FULL_TEXT_BLOCKER`.

New gate: `CROSS_ACT_EXCEPTION != AMENDMENT_OR_REPEAL_OF_TARGET_BODY`.

## 5. Federal Law 31.07.2020 №258-ФЗ — experimental legal regimes

New Habr conflict:
- Habr still lists the original title: `Об экспериментальных правовых режимах в сфере цифровых инноваций в Российской Федерации`.
- current law title is `Об экспериментальных правовых режимах в сфере цифровых и технологических инноваций в Российской Федерации`.

Primary / lifecycle evidence:
- initial official publication confirms the original title and identity: `0001202007310024`, 31.07.2020.
- Federal Law 28.12.2024 №523-ФЗ, article 29, changed the title by replacing `цифровых` with `цифровых и технологических`; the change took effect 27.06.2025. Primary official publication for №523-ФЗ: `0001202412280025`, 28.12.2024.
- current consolidated legal sources show edition **26.06.2026** and include Federal Law 26.06.2026 №211-ФЗ as the latest amendment.
- publication pointer for №211-ФЗ is corroborated as `0001202606260071`, publication date 26.06.2026; direct official portal search result for that specific card was not resolved in this pass, so classify the pointer as corroborated rather than `PRIMARY_DIRECT_FETCH_VERIFIED`.

State:
`HABR_STALE_TITLE_CONFLICT / PRIMARY_ORIGINAL_TITLE_CONFIRMED / PRIMARY_TITLE_CHANGE_523_2024_CONFIRMED / CURRENT_EDITION_2026-06-26_CORROBORATED / LATEST_AMENDMENT_211_2026_PUBLICATION_POINTER_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.

New gate: `HABR_ORIGINAL_TITLE_CAN_BE_LEGALLY_OBSOLETE_WHILE_NUMBER_AND_DATE_REMAIN_CORRECT`.

## Delta counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `MENTION_ONLY_REJECTED +2 target mappings` (№247, №294, same file)
- `FALSE_POSITIVE_LEXICAL_CORPUS +1` (№149 search)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_STALE_TITLE_CONFLICT +1` (№258)
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +2` (№247, №258)
- `PRIMARY_LATEST_OR_TITLE_AMENDMENT_CONFIRMED +3` (№188 <- №357; №294 <- №548; №258 <- №523)
- `NEXT_DAY_EFFECTIVE_CHANGE +1 target` (№149, 01.09.2026)
- `LIMITED_CONTINUED_APPLICABILITY_TO_2028 +1` (№294)
- `CROSS_ACT_APPLICABILITY_EXCEPTION +1` (№149/№247 interaction)
- `PRIMARY_CURRENT_STATUS_BLOCKER +5`

## New acceptance / regression gates

1. `CONSOLIDATED_EDITION_DATE != ALL_PROVISIONS_EFFECTIVE_NOW`.
2. `FRAMEWORK_SUPERSEDED_IN_CORE_SCOPE != WHOLE_ACT_REPEALED`.
3. `CROSS_ACT_EXCEPTION != AMENDMENT_OR_REPEAL_OF_TARGET_BODY`.
4. `HABR_ORIGINAL_TITLE_CAN_BE_LEGALLY_OBSOLETE_WHILE_NUMBER_AND_DATE_REMAIN_CORRECT`.
5. `SAME_GITHUB_REFERENCE_PAGE_MENTIONING_MULTIPLE_LAWS != FULL_TEXT_DUPLICATE`.
6. `SEARCH_PHRASE_HIT_IN_LEXICAL_CORPUS != LEGAL_DOCUMENT_CANDIDATE`.

## Next unchecked system-forming queue

- Government Resolution 22.10.2020 №1722.
- Government Resolution 10.03.2022 №336.

These should be processed next with the same body-completeness and primary-current-status separation rules.
