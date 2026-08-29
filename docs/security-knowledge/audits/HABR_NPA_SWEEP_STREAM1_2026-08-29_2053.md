# Habr NPA sweep — stream 1 — 2026-08-29 20:53 MSK

Scope: continued systematic pass over Habr 432466 / user NPA list. This pass covers the general legal-publication / mandatory-requirements layer:

1. Federal Law 14.06.1994 No. 5-FZ.
2. Presidential Decree 23.05.1996 No. 763.
3. Government Resolution 13.08.1997 No. 1009.
4. Government Resolution 22.10.2020 No. 1722.

## Result counters

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +4
- Habr identity confirmed: +4
- latest-known amendment marker found/corroborated: +4
- direct primary current-consolidated-text verification: +0
- exact duplicates: +0
- body-level identity conflicts: +0

## Findings

| Act | Habr identity | GitHub result | GitHub artifact metadata | Freshness / official-source result | Classification |
|---|---|---|---|---|---|
| Federal Law 14.06.1994 No. 5-FZ “On the procedure for publication and entry into force…” | Confirmed in Habr 432466, “Основы законодательства” | Exact-title and characteristic body-phrase Code Search: 0 results (`incomplete_results=false`); semantic GitHub search: 0 | `repo=null; commit=null; path=null; size=null; type=null` | Current legal databases converge on revision 01.05.2019. The amending Federal Law 01.05.2019 No. 83-FZ is present in the official publication portal index: publication No. `0001201905010039`, 01.05.2019, PDF 509 KB / 11 pp. Direct current consolidated body for base 5-FZ was not resolved in this pass. | `GITHUB_FULL_TEXT_BLOCKER / PRIMARY_AMENDMENT_PUBLICATION_CONFIRMED / CURRENT_CONSOLIDATED_BODY_UNRESOLVED` |
| Presidential Decree 23.05.1996 No. 763 “On the procedure for publication and entry into force…” | Confirmed in Habr 432466 | Exact-title and characteristic body-phrase Code Search: 0; semantic GitHub search: 0 | `repo=null; commit=null; path=null; size=null; type=null` | Current legal sources identify revision 03.03.2022. Decree 03.03.2022 No. 90 explicitly changes para. 3 of cl. 2 of No. 763. The official pravo.gov.ru homepage itself identifies Decree No. 90 as the basis for official consolidated texts; publication pointer for No. 90 is `0001202203030006`. Direct primary card/body for No. 763 current consolidated text was not resolved. | `GITHUB_FULL_TEXT_BLOCKER / AMENDMENT_RELATION_CORROBORATED / PRIMARY_CURRENT_BODY_UNRESOLVED` |
| Government Resolution 13.08.1997 No. 1009 “On approval of Rules for preparation of normative legal acts…” | Confirmed in Habr 432466 | Exact-title + characteristic body-phrase Code Search: 0; semantic GitHub search: 0 | `repo=null; commit=null; path=null; size=null; type=null` | Current legal sources identify revision 15.11.2024. Government Resolution 15.11.2024 No. 1557 changes cl. 3(3) of the Rules approved by No. 1009. Official-publication pointer corroborated as `0001202411150020` dated 15.11.2024; direct primary card was not resolved in this pass. | `GITHUB_FULL_TEXT_BLOCKER / LATEST_AMENDMENT_CORROBORATED / PRIMARY_DIRECT_CARD_BLOCKER` |
| Government Resolution 22.10.2020 No. 1722 “On placement and updating … lists of normative legal acts containing mandatory requirements” | Confirmed in Habr 432466 | Exact-title + characteristic body-phrase Code Search: 0; semantic GitHub search: 0 | `repo=null; commit=null; path=null; size=null; type=null` | Current legal sources identify revision 26.01.2026. Government Resolution 26.01.2026 No. 42 directly amends the Rules approved by No. 1722: adds use of the Federal State Information System “Register of Mandatory Requirements” and repeals cl. 7(1). Official-publication pointer corroborated as `0001202601270032`, dated 27.01.2026; direct primary card was not resolved. | `GITHUB_FULL_TEXT_BLOCKER / LATEST_AMENDMENT_CORROBORATED / PRIMARY_DIRECT_CARD_BLOCKER` |

## GitHub search evidence

Characteristic body phrase searches all returned `total_count=0`, `incomplete_results=false`:

- 5-FZ: `Федеральные конституционные законы, федеральные законы подлежат официальному опубликованию...`
- Decree 763: `Акты Президента Российской Федерации и акты Правительства Российской Федерации подлежат официальному опубликованию...`
- Resolution 1009: `Государственной регистрации подлежат нормативные правовые акты...`
- Resolution 1722: `перечни нормативных правовых актов (их отдельных положений), содержащих обязательные требования...`

As in earlier passes, zero Code Search results are **not** treated as proof that binary PDF/DOCX copies do not exist on GitHub.

## New corpus gates

1. `CURRENT_DATABASE_REVISION != PRIMARY_CURRENT_VERIFIED`: revision dates from current legal databases are discovery/corroboration signals only; primary current consolidated text must be resolved separately.
2. `OFFICIAL_PUBLICATION_POINTER != PRIMARY_DIRECT_CARD`: a publication number/date recovered from a reliable legal source is stored as a pointer until the primary publication card/body is directly fetched.
3. `GENERAL_LEGAL_FOUNDATION_ACTS` are retained in the Security KB because they determine whether regulator requirements can be treated as binding/current, but their GitHub copies still require the same body-level provenance gates as subject-matter PD/IB acts.
4. For No. 1722, future GitHub candidates must contain the 2026 marker introduced by Resolution No. 42 (FSIS “Register of Mandatory Requirements” in cl. 2 and repeal of cl. 7(1)) or they are stale.
5. For No. 1009, future GitHub candidates must be tested against the 15.11.2024 No. 1557 amendment marker in cl. 3(3).

## Source pointers used in this pass

- Habr 432466, current version 28.05.2026.
- Official publication portal index for Federal Law 01.05.2019 No. 83-FZ: publication `0001201905010039`.
- `pravo.gov.ru` official portal home: consolidated legal texts and Decree 03.03.2022 No. 90.
- Decree No. 90 publication pointer: `0001202203030006`.
- Government Resolution No. 1557 publication pointer: `0001202411150020`.
- Government Resolution No. 42 publication pointer: `0001202601270032`.

No GitHub copy is classified as official merely because it contains legal text or matching requisites.
