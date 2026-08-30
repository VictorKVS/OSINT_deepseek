# Habr NPA sweep — Stream 1 — 2026-08-30 15:56 MSK

Scope: Habr 432466, section «Персональные данные. Обеспечение безопасности». Audited this pass: PP RF №940/2012, PP RF №211/2012, FSTEK order №21/2013, the Habr cross-reference to FSTEK order №17/2013, FSB order №378/2014, FSB order №77/2023. PP RF №1119/2012 was already audited and is intentionally skipped.

## Delta

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `DUPLICATE_NON_TARGET_REFERENCE_HITS +7`, collapsed to `3` already-known GitHub artifacts:
  - `Grantik/odin-vault @ 310311752a7aba7749a202d6a1a3a19ce2484faa / sync/canon/package/samples/minekonom_prikaz_67_gis_ekonomika.txt`, blob `bad57fdb9d2f27f9d120964eb2c8011ee0cf58f4`, type `TXT/file`, size `METADATA_UNRESOLVED_THIS_PASS`;
  - parsed derivative `sync/canon/package/samples/parsed/minekonom_prikaz_67_gis_ekonomika.md`, blob `388b65a0878ebef8f254f468808c3426ef19fd36`, type `Markdown/file`, size previously measured `189374 bytes`;
  - `sync/canon/package/samples/koncepciya_gis_rt_teo.txt`, known blob `067866c9fe3b098c0432205ca554945298e53bd8`, `345746 bytes`, `TXT/file`.
- `HABR_STALE_REFERENCE_CONFLICT +1` — Habr 28.05.2026 still points readers to FSTEK №17 for state/municipal IS protection, although №17 lost force on 01.03.2026 and was replaced by FSTEK №117/2025.
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +2` — FSTEK №117/2025 and FSB №77/2023.
- `CURRENT_EDITION_CORROBORATED +4` — PP №940/2012, PP №211/2012, FSTEK №21/2013, FSB №378/2014.
- `LATEST_AMENDMENT_RELATION_CONFIRMED +1` — PP №211 ← PP №454/2019.
- `ENACTED_FUTURE_CHANGE +1` — FSTEK №137/2026 amends №117 and is scheduled to enter into force 01.09.2026; registration in Minjust №87797 is corroborated. Direct primary publication card/ID was not resolved in this pass, so it is not promoted to direct-primary verification.
- `DRAFT_REPLACEMENT_BLOCKER +1` — the proposed replacement of FSTEK №21 is still evidenced as a draft (project ID `01/02/07-26/00169583`); no final signed/registered/officially published replacement was found by the final check in this pass.
- exact duplicate full normative bodies: `+0`.
- target-body identity conflicts: `+0`.

## Per-act results

### Постановление Правительства РФ от 18.09.2012 №940

- GitHub exact date+number+title search: `0` target files, `incomplete_results=false`.
- Target artifact fields: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Consolidated full body confirms exact date, number and title; base edition `18.09.2012`, effective `02.10.2012`, current status corroborated as active.
- No later amendment was found in the end-of-pass freshness check; this is absence-of-hit evidence only, not proof of immutability.
- Historical primary publication record/card was not directly resolved in this pass. Official publication in `Собрание законодательства РФ, №39, 24.09.2012, ст.5279` is corroborated by current legal sources.
- Completeness gate: `FULL_TEXT = постановление + все утвержденные Правила согласования`.

### Постановление Правительства РФ от 21.03.2012 №211

- Exact GitHub body search: `0`, `incomplete_results=false`; target fields all `null` → `GITHUB_FULL_TEXT_BLOCKER`.
- A broad GitHub search surfaced the known `koncepciya_gis_rt_teo.txt`; it is only a technical concept that cites legal acts, not PP №211 → `DUPLICATE_REFERENCE_ARTIFACT / REJECT`.
- Current consolidated edition corroborated as `15.04.2019`.
- The latest amendment relationship found is PP RF `15.04.2019 №454`, which directly rewrites subparagraph `a` of point 1 of the list approved by №211.
- Direct primary publication card for №454 was not resolved in this pass; relation and current edition are therefore kept as corroborated, not primary-direct.
- Completeness gate: `FULL_TEXT = постановление + весь актуальный перечень мер`.

### Приказ ФСТЭК России от 18.02.2013 №21

- Exact GitHub code search returned `2` files, both already-known artifacts in `Grantik/odin-vault` at commit `310311752a7aba7749a202d6a1a3a19ce2484faa`:
  - `sync/canon/package/samples/minekonom_prikaz_67_gis_ekonomika.txt`, blob `bad57f...`, TXT/file;
  - `sync/canon/package/samples/parsed/minekonom_prikaz_67_gis_ekonomika.md`, blob `388b65...`, Markdown/file.
- Body inspection identifies the source document as **Минэкономразвития России, приказ от 18.02.2022 №67, ГИС «Экономика»**. №21 appears only in a legal-basis list and later in a sentence describing requirements for the security subsystem. It is not a copy of №21.
- Classification for both hits: `DUPLICATE_NON_TARGET_REFERENCE / REFERENCE_ONLY / WRONG_PRIMARY_BODY / REJECT`.
- Target body remains `GITHUB_FULL_TEXT_BLOCKER`.
- Current consolidated order №21 is corroborated in edition `14.05.2020`, effective from `01.01.2021`; current August-2026 sources still describe it as the applicable PDn/ISPDn order.
- Critical fresh check: FSTEK published a **draft** replacement on 24.07.2026, project `01/02/07-26/00169583`. The draft proposed 01.09.2026 as its effective date and repeal of №21, but a fresh search up to 30.08.2026 found no final signed/registered/officially published replacement act.
- Therefore status as of this pass: `ACTIVE_CURRENT_ORDER / DRAFT_REPLACEMENT_EXISTS / NO_ENACTED_REPEAL_FOUND`.
- Gate: a date written in a draft is not an `effective_from` for the legal corpus.

### Приказ ФСТЭК России от 11.02.2013 №17 — Habr cross-reference

- Exact GitHub search again returned the same two `minekonom_prikaz_67_gis_ekonomika` artifacts; both merely cite №17 and are rejected as target body.
- Habr 432466 (version 28.05.2026) still says that state/municipal IS protection follows №17. This is stale.
- FSTEK order `11.04.2025 №117` was officially published on `17.06.2025`, Minjust registration `№82619`, publication number `0001202506170011`; it entered into force `01.03.2026` and replaced №17.
- Thus №17 classification: `LOST_FORCE_2026-03-01 / REPLACED_BY_FSTEK_117 / HABR_STALE_REFERENCE_CONFLICT`.
- Additional future-effective change: FSTEK order `08.05.2026 №137`, Minjust `10.08.2026 №87797`, amends №117 and is corroborated as entering into force `01.09.2026` (with an exception for a separately dated provision). Primary publication pointer is not promoted to direct-primary in this pass because the direct publication card was not resolved.
- For current corpus on `30.08.2026`: use №117 in its presently effective text; keep №137 in `ENACTED_FUTURE_CHANGE` until 01.09.2026.

### Приказ ФСБ России от 10.07.2014 №378

- Exact GitHub date+number+distinctive-title search: `0`, `incomplete_results=false`.
- Target fields: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Broad search had surfaced the same `koncepciya_gis_rt_teo.txt`; body identity rejects it as a technical concept/reference artifact.
- Full legal body independently confirms exact title and Minjust registration `№33620` of 18.08.2014; current status is corroborated as active, base/current edition `10.07.2014` in the sources checked.
- Direct primary historical publication card was not resolved; retain `PRIMARY_PUBLICATION_RECORD_UNRESOLVED` rather than treating the consolidated copy as official publication.
- Completeness gate: `FULL_TEXT = приказ + весь Состав и содержание мер по всем уровням защищенности`.

### Приказ ФСБ России от 13.02.2023 №77

- Exact GitHub date+number+title search: `0`, `incomplete_results=false`.
- Target fields: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Broad search again surfaced the known `koncepciya_gis_rt_teo.txt`; it is reference-only and rejected.
- Primary official publication is directly confirmed: Minjust registration `№72404`, official publication number `0001202302200021`, published `20.02.2023`.
- The act entered into force `01.03.2023`; no later amendment was found in this pass.
- Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_BASE_EDITION_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.
- Completeness gate: `FULL_TEXT = приказ + полный Порядок взаимодействия операторов с ГосСОПКА/ФСБ`.

## New corpus gates

1. `DRAFT_REPLACEMENT != ENACTED_REPEAL` — FSTEK №21 remains the current normative act until a final replacing act is signed/registered/officially published and reaches its effective date.
2. `HABR_REFERENCE_DATE_MUST_BE_CHECKED_AGAINST_EFFECTIVE_LIFECYCLE` — the 28.05.2026 Habr snapshot still points to №17 although №117 already replaced it on 01.03.2026.
3. `CURRENT_EFFECTIVE_TEXT != ENACTED_FUTURE_CHANGE` — on 30.08.2026 FSTEK №117 is current; №137 is already enacted/registered but its main changes are future-effective from 01.09.2026.
4. `REFERENCE_LIST_MATCH != BODY_IDENTITY` — exact title phrases inside a technical concept can make GitHub Code Search look highly precise; the document header/body must still identify the target NPA itself.
5. GitHub deduplication stays `repo + commit + path + blob SHA`; derived TXT/Markdown representations of one technical source are separate files but not separate normative bodies.

## Official/current pointers captured

- FSTEK №117/2025 primary publication: `https://publication.pravo.gov.ru/document/0001202506170011`.
- FSB №77/2023 primary publication: `https://publication.pravo.gov.ru/Document/View/0001202302200021`.
- FSTEK №137/2026: Minjust registration `№87797` and entry into force `01.09.2026` corroborated; direct primary publication card remains unresolved in this pass.
- FSTEK replacement-project for №21: regulation.gov.ru project ID `01/02/07-26/00169583`; project status only.

## Next queue

Continue with the remaining Habr PDn-security methodological/information materials: FSB methodological recommendations `31.03.2015 №149/7/2/6-432`, FSB information messages `21.06.2016` and `15.06.2017`, FSTEK information message `15.07.2013 №240/22/2637`, and the FSTEK basic threat model excerpt approved `15.02.2008`. For each, distinguish NPA vs methodological/information document before assigning legal force, then perform the same GitHub body/provenance and official-source checks.
