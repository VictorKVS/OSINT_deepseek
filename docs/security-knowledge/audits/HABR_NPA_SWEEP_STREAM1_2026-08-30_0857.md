# Habr NPA sweep — Stream 1 — 2026-08-30 08:57 MSK

Source snapshot: Habr article 432466, version dated 2026-05-28, plus the user-maintained NPA queue.

## Delta for this pass

- targets processed: 4
- GITHUB_FULL_TEXT_CONFIRMED: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +4
- duplicate/non-target GitHub search hits: +6 target-hits across 4 unique previously inspected artifacts; no new unique legal-body candidate
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +2 (FZ 548/2025 as latest amendment to FZ 294; PP 1154/2025 itself)
- PRIMARY_GOVERNMENT_CURRENT_RECORD_CONFIRMED: +1 (PP 1119/2012)
- CURRENT_EDITION_CORROBORATED: +2 (FZ 294/2008 -> 29.12.2025 / effective text from 01.03.2026; PP 336/2022 -> 27.08.2026)
- LATEST_AMENDMENT_RELATION_CONFIRMED: +2 (FZ 548/2025 -> FZ 294/2008; PP 1086/2026 -> PP 336/2022)
- POST_HABR_SNAPSHOT_AMENDMENT: +1 target (PP 336; two post-snapshot amendments found, 991/2026 and then 1086/2026)
- WITHIN_PASS_LATEST_AMENDMENT_ADVANCED: +1 (PP 336 freshness floor advanced from 991/10.08.2026 to 1086/27.08.2026)
- exact full-body duplicates: +0
- new target-body identity conflicts: +0

Habr presence confirmed:
- FZ 294/2008 and PP 336/2022 in the system-forming block;
- PP 1154/2025 in the PD block;
- PP 1119/2012 in the PD security block.

## Findings

### 1. Federal Law 26.12.2008 No. 294-FZ
Target: `О защите прав юридических лиц и индивидуальных предпринимателей при осуществлении государственного контроля (надзора) и муниципального контроля`.

GitHub:
- exact title/date/body-identity searches produced no target full body.
- broad search again produced a previously inspected non-target artifact:
  - repo: `AxHulk/osp-kavkaz-ing`
  - commit: `b902d3e57875c53d2c284e3e257fefc7f8d5e9e9`
  - path: `src/pages/Accreditation.tsx`
  - blob SHA: `019eb2fb8c4e15d46859ff2a43c58517b56bfbd8`
  - size: `174314` bytes
  - type: `TypeScript/TSX file` (`git blob`)
  - body identity: React page for a certification body; starts with imports/UI code and page content `Аккредитация`; it is not a federal law.
  - classification: `DUPLICATE_REFERENCE_ARTIFACT / WRONG_PRIMARY_BODY / REJECT`.
- target metadata remain `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current legal full-text sources identify edition `29.12.2025`, with the consolidated text reflecting changes effective from `01.03.2026`.
- Federal Law 29.12.2025 No. 548-FZ directly amends FZ 294/2008 and extends the special application period in Article 26.3 through `31.12.2028`.
- official publication of FZ 548/2025 is confirmed directly by `publication.pravo.gov.ru`: publication No. `0001202512290036`, publication date `29.12.2025`, PDF 187 KB / 4 pages.
- the current text still operates in 2026; do not classify the whole FZ 294 as repealed merely because the control system largely migrated to FZ 248/2020.
- status: `CURRENT_EDITION_CORROBORATED_2025-12-29 / EFFECTIVE_TEXT_2026-03-01 / LATEST_AMENDMENT_PRIMARY_PUBLICATION_CONFIRMED / SPECIAL_APPLICATION_EXTENDED_TO_2028-12-31 / GITHUB_FULL_TEXT_BLOCKER`.

### 2. Government Resolution 10.03.2022 No. 336
Target: `Об особенностях организации и осуществления государственного контроля (надзора), муниципального контроля` + all current appendices.

GitHub:
- exact/body searches did not return a target body.
- search hits resolve only to previously rejected `Grantik/odin-vault` technical/legal-reference artifacts:
  - `sync/canon/package/samples/minekonom_prikaz_67_gis_ekonomika.txt` — body is Ministry of Economic Development Order 18.02.2022 No. 67, not PP 336;
  - `sync/canon/package/samples/parsed/minekonom_prikaz_67_gis_ekonomika.md` — parsed derivative of the same wrong source, blob SHA `388b65a0878ebef8f254f468808c3426ef19fd36`, size 189374 bytes, Markdown/file.
- classifications: `DUPLICATE_NON_TARGET_REFERENCE / DERIVATIVE_DUPLICATE / REJECT`.
- target metadata remain `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- an initial freshness check found PP 10.08.2026 No. 991, which directly added point 11(24) to PP 336 and entered into force on official publication.
- a later freshness check in the same pass found a still newer amendment: Government Resolution 27.08.2026 No. 1086, `О внесении изменений в постановление Правительства Российской Федерации от 10 марта 2022 г. № 336`.
- No. 1086 changes point 11(9), point 11(10), and Appendix No. 2; the reproduced publication pointer is `pravo.gov.ru` No. `0001202608270016`, publication date `27.08.2026`; it enters into force on official publication.
- current legal sources now identify PP 336 as edition `27.08.2026`, with certain changes/additions reflected from `01.09.2026`.
- both 991/2026 and 1086/2026 are later than the Habr snapshot date 28.05.2026, therefore absence of these amendments from that snapshot is `POST_HABR_SNAPSHOT_AMENDMENT`, not a source error.
- direct fetch of the primary publication card for 1086/2026 was not resolved in this pass; the exact primary publication ID is corroborated but not direct-card verified.
- status: `CURRENT_EDITION_CORROBORATED_2026-08-27 / LATEST_AMENDMENT_1086-2026 / POST_HABR_SNAPSHOT_AMENDMENT / OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_CARD_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 3. Government Resolution 01.11.2012 No. 1119
Target: `Об утверждении требований к защите персональных данных при их обработке в информационных системах персональных данных` + complete approved Requirements.

GitHub:
- no target full body found.
- broad searches returned only previously inspected `Grantik/odin-vault` artifacts: `minekonom_prikaz_67_gis_ekonomika.txt`, its parsed Markdown derivative, and `koncepciya_gis_rt_teo.txt` (blob `067866c9fe3b098c0432205ca554945298e53bd8`, 345746 bytes, TXT/file). All are other documents that merely cite PP 1119.
- classification for all such hits: `DUPLICATE_REFERENCE_ARTIFACT / REFERENCE_ONLY / WRONG_PRIMARY_BODY / REJECT`.
- target metadata remain `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- the official Government of Russia page directly identifies Resolution No. 1119 and explicitly offers `Постановление от 1 ноября 2012 года №1119 в действующей редакции`.
- the official page describes the four protection levels and the criteria used to determine them.
- secondary full-text sources reproduce the signing resolution and the approved Requirements; independent current public-sector/legal pages continue to mark the resolution as active.
- completeness gate: `FULL_TEXT = signing resolution + complete approved Requirements`; a citation, summary, or only the signing clauses is not enough.
- status: `PRIMARY_GOVERNMENT_CURRENT_RECORD_CONFIRMED / ACTIVE_STATUS_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.

### 4. Government Resolution 01.08.2025 No. 1154
Target: `Об утверждении требований к обезличиванию персональных данных, методов обезличивания персональных данных и Правил обезличивания персональных данных`.

GitHub:
- exact title/date search returned 0 target files.
- broader number/date/topic search also returned 0 target files.
- `repo/commit/path/size/type = null` -> `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary official publication is directly confirmed by `publication.pravo.gov.ru`: publication No. `0001202508050011`, publication date `05.08.2025`, PDF `2619 KB / 12 pages`.
- the act enters into force on `01.09.2025`; current legal sources continue to mark it active.
- secondary full-text sources reproduce the act and show that it approves three distinct normative components: `Требования к обезличиванию`, `Методы обезличивания`, and `Правила обезличивания`.
- completeness gate: `FULL_TEXT = signing resolution + complete Requirements + complete Methods + complete Rules`; omission of any one component is `PARTIAL_TEXT`.
- no later amendment was established in this pass; direct act-specific current consolidated primary body was not separately resolved beyond the official initial publication.
- status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / EFFECTIVE_2025-09-01 / CURRENT_STATUS_CORROBORATED / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

## New / reinforced corpus gates

1. `LATEST_AMENDMENT_MUST_BE_RECHECKED_AT_END_OF_PASS`: PP 336 changed twice after the Habr snapshot; a freshness finding (991/2026) can already be superseded by a still newer act (1086/2026) before the audit finishes.
2. `POST_SNAPSHOT_AMENDMENT != SOURCE_ERROR`: Habr 432466 is explicitly versioned 28.05.2026; later changes belong to the temporal delta, not to an author-error bucket.
3. `CURRENT_LEGAL_OPERATION != PRIMARY_FRAMEWORK_ROLE`: FZ 294/2008 remains legally operative for specified scopes through 31.12.2028 even though FZ 248/2020 is the newer general control framework.
4. `FULL_TEXT_THREE_COMPONENT_GATE`: for PP 1154/2025, a complete corpus artifact must include Requirements + Methods + Rules in addition to the signing resolution.
5. `OFFICIAL_CURRENT_RECORD != GITHUB_BODY`: PP 1119 has an official Government current-record pointer while GitHub still has no verified full body; these evidence dimensions remain independent.
6. `DUPLICATE_SEARCH_HIT_DEDUP_BY_BLOB`: repeated legal references inside known technical documents do not increase the count of independent candidates.

## Source pointers used in this pass

Habr:
- https://habr.com/ru/articles/432466/

GitHub rejected duplicate artifact:
- https://github.com/AxHulk/osp-kavkaz-ing/blob/b902d3e57875c53d2c284e3e257fefc7f8d5e9e9/src/pages/Accreditation.tsx

Primary / official sources:
- FZ 548/2025: https://publication.pravo.gov.ru/Document/View/0001202512290036
- PP 1119/2012 official Government record: https://government.ru/docs/6339/
- PP 1154/2025 official publication: https://publication.pravo.gov.ru/document/0001202508050011
- PP 1086/2026 official publication pointer (direct card not resolved in this pass): https://publication.pravo.gov.ru/document/0001202608270016

No GitHub artifact in this audit is treated as an official legal source. Body identity, structural completeness, edition freshness, official publication, effective date and official current-text status remain independent evidence dimensions.
