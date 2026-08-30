# Habr NPA sweep — Stream 1 — 2026-08-30 16:56 MSK

Scope: continuation of systematic verification of Habr 432466 and the user NPA/source list. This pass focuses on FSB/FSTEC methodical and informational materials used in the PDn security block. GitHub copies are treated only as corpus candidates; official/provenance/legal-status checks are separate.

## Delta

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `DUPLICATE_REFERENCE_ARTIFACT +1`
- `REFERENCE_ONLY_WRONG_BODY +1`
- `DERIVED_DUPLICATE_REFERENCE +1`
- `PRIMARY_FSB_SOURCE_CONFIRMED +3`
- `PRIMARY_FSB_LIFECYCLE_STATEMENT +1`
- `PRIMARY_FSTEC_SOURCE_BLOCKER +2`
- `PARTIAL_CONTEXT_STALE +1`
- new exact duplicates of target full bodies: `0`
- new target-body identity conflicts: `0`

## Results

### FSB methodological materials dated 21.02.2008, No. 149/54-144

GitHub exact code search by `149/54-144`: no target file; `incomplete_results=false`.

- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Primary FSB lifecycle evidence: the FSB information page dated 21.06.2016 states that the 2008 methodical recommendations on cryptographic protection of PDn and the related standard requirements **lost relevance** because Government Resolution No. 781 of 17.11.2007 had been withdrawn from effect. This is agency-confirmed loss of relevance, but it is not automatically evidence of formal repeal of an NPA.

Status: `LOST_RELEVANCE_CONFIRMED_BY_FSB / FORMAL_REPEAL_NOT_ESTABLISHED`.

### FSB Methodical Recommendations dated 31.03.2015, No. 149/7/2/6-432

GitHub exact search returned one already-known non-target artifact:

- repo: `Grantik/odin-vault`
- commit: `310311752a7aba7749a202d6a1a3a19ce2484faa`
- path: `sync/canon/package/samples/koncepciya_gis_rt_teo.txt`
- blob: `067866c9fe3b098c0432205ca554945298e53bd8`
- size: `345746` bytes
- type: `TXT/file`
- body identity: starts as the 2024 Concept of the state information system “Russian Transport”; No. 149/7/2/6-432 is only referenced later.
- classification: `DUPLICATE_REFERENCE_ARTIFACT / REFERENCE_ONLY / WRONG_PRIMARY_BODY / REJECT`

Primary FSB source is available as an official FSB PDF and identifies the document as approved by the leadership of the 8th Center of the FSB of Russia on 31.03.2015 No. 149/7/2/6-432. This confirms provenance and body identity. It does **not** by itself establish that the document is a registered/published NPA.

Status: `PRIMARY_FSB_SOURCE_CONFIRMED / DOCUMENT_TYPE=METHODICAL_RECOMMENDATIONS / NPA_PUBLICATION_STATUS_NOT_ESTABLISHED / GITHUB_FULL_TEXT_BLOCKER`.

### FSB information message dated 21.06.2016

Title: “О нормативно-методических документах, действующих в области обеспечения безопасности персональных данных”.

GitHub exact full-title search: `0`, `incomplete_results=false`.

- repo/commit/path/size/type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

The official FSB web page confirms the exact title/date and its informational nature. It also provides the lifecycle statement for the 2008 cryptographic methodical materials.

Status: `PRIMARY_FSB_WEBPAGE_CONFIRMED / INFORMATIONAL_MATERIAL / NPA_STATUS_NOT_ESTABLISHED`.

### FSB information message dated 15.06.2017

Title: “О неукоснительном соблюдении операторами персональных данных требований формуляров на СКЗИ”.

GitHub exact full-title search: `0`, `incomplete_results=false`.

- repo/commit/path/size/type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

The official FSB page confirms the exact date **15.06.2017** and title. The page explains the mandatory observance of SKZI formular/operational-documentation requirements. It is recorded as an agency informational/explanatory material, not automatically as an NPA.

Status: `PRIMARY_FSB_WEBPAGE_CONFIRMED / INFORMATIONAL_MATERIAL / NPA_STATUS_NOT_ESTABLISHED`.

### FSTEC information message dated 15.07.2013 No. 240/22/2637

Title in Habr: “По вопросам защиты информации и обеспечения безопасности персональных данных ... в связи с изданием приказа ФСТЭК России ... No. 17 ... и ... No. 21 ...”.

GitHub exact search by `240/22/2637`: `0`, `incomplete_results=false`.

- repo/commit/path/size/type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

No direct current FSTEC primary page/body was resolved in this pass. Habr links to a CNTD mirror, which is not treated as the primary official source.

Lifecycle/context note: Order FSTEC No. 117 dated 11.04.2025 was officially published on 17.06.2025 (publication No. `0001202506170011`, MinJust No. 82619) and from 01.03.2026 replaced the regulatory role of former Order No. 17. Therefore references in the 2013 information message that depend on No. 17 are contextually stale as of 30.08.2026. This is **not** proof that the entire 2013 information message was formally repealed.

Status: `PRIMARY_FSTEC_SOURCE_BLOCKER / DEPENDENCY_REPLACED / PARTIAL_CONTEXT_STALE`.

### FSTEC Basic threat model for PDn, approved 15.02.2008

Title: “Базовая модель угроз безопасности персональных данных при их обработке в информационных системах персональных данных” (Habr identifies a “Выписка”).

GitHub exact full-title search produced two hits, both non-target references in the same source family:

1. `Grantik/odin-vault`, commit `310311752a7aba7749a202d6a1a3a19ce2484faa`, path `sync/canon/package/samples/minekonom_prikaz_67_gis_ekonomika.txt`, blob `bad57fdb9d2f27f9d120964eb2c8011ee0cf58f4`, size `METADATA_UNRESOLVED`, type `TXT/file`. Body starts as Ministry of Economic Development Order dated 18.02.2022 No. 67 concerning the GIS “Economics”; the Basic Model is only cited. `REFERENCE_ONLY / WRONG_PRIMARY_BODY / REJECT`.
2. Same repo/commit source family, path `sync/canon/package/samples/parsed/minekonom_prikaz_67_gis_ekonomika.md`, blob `388b65a0878ebef8f254f468808c3426ef19fd36`, size `189374` bytes, type `Markdown/file`. Parsed derivative of the same non-target body. `DERIVED_DUPLICATE_REFERENCE / WRONG_PRIMARY_BODY / REJECT`.

No direct current FSTEC primary page/body was resolved. A regional government PDn package currently labels the 2008 Basic Model as “действует, не применяется”; because this is secondary government guidance rather than the issuing authority, it is kept only as a status hint and does not close the primary-source gate.

Status: `GITHUB_FULL_TEXT_BLOCKER / PRIMARY_FSTEC_SOURCE_BLOCKER / SECONDARY_GOVERNMENT_STATUS_HINT=ACTIVE_NOT_APPLIED`.

## Corpus gates added/reaffirmed

1. `OFFICIAL_AGENCY_WEBPAGE != OFFICIAL_PUBLICATION_AS_NPA`
2. `LOST_RELEVANCE_CONFIRMED_BY_AGENCY != FORMAL_REPEAL`
3. `DEPENDENCY_REPLACED => INTERPRETIVE_MESSAGE_CAN_BECOME_PARTIALLY_STALE_WITHOUT_FORMAL_REPEAL`
4. `METHODICAL_OR_INFORMATIONAL_DOCUMENT != NPA_UNLESS_LEGAL_FORM/REGISTRATION/PUBLICATION_GATE_IS_PROVEN`
5. GitHub candidate deduplication key remains `repo + commit + path + blob`.

## Remaining blockers from this pass

- Original primary 2008 FSB body for No. 149/54-144 was not recovered on GitHub; only later official FSB lifecycle evidence is confirmed.
- Direct primary FSTEC body/current-status page for No. 240/22/2637 was not resolved.
- Direct primary FSTEC body/current-status page for the Basic Model dated 15.02.2008 was not resolved.
- For the FSB 2015 methodical recommendations and the 2016/2017 informational materials, provenance is confirmed by FSB, but legal classification as formally published/registered NPA is not established and must not be inferred.
