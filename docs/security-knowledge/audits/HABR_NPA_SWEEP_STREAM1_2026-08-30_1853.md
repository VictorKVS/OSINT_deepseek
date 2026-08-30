# Habr NPA sweep — Stream 1 — 2026-08-30 18:53 MSK

Scope continuation: Habr 432466, section `Персональные данные. Особые случаи обработки ПДн`, items 6–11. Checked acts: 53-ФЗ/1998, Tax Code part I 146-ФЗ/1998, Tax Code part II 117-ФЗ/2000, 115-ФЗ/2001 AML/CFT, 127-ФЗ/2002 bankruptcy, 173-ФЗ/2003 currency regulation.

## Delta summary

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_PIPELINE_CANDIDATE +1` (127-ФЗ downloader/registry only; generated body absent at inspected commit)
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `REFERENCE_OR_CONTROL_ARTIFACT_REJECT +4` (two shared odin-vault control files for 117-ФЗ/173-ФЗ; one FiveText reference-only HTML; themis downloader is not body)
- `CURRENT_EDITION_CORROBORATED +6`
- `ENACTED_FUTURE_CHANGE / EFFECTIVE_DATE_SPLIT +5` (NK I, NK II, 115-ФЗ, 127-ФЗ, 173-ФЗ)
- `PRIMARY_BASE_ACT_URL_BLOCKER +3` (NK I/II and 173-ФЗ not resolved to a directly fetched primary base-act record in this pass)
- exact duplicate full normative bodies: `0`
- target-body identity conflicts: `0`

Habr reference: https://habr.com/ru/articles/432466/ — version 28.05.2026, special PDn items 6–11.

## 1. 53-ФЗ от 28.03.1998 «О воинской обязанности и военной службе»

GitHub exact search by number/date/title: no target body.

`repo=null; commit=null; path=null; size=null; type=null`

Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Freshness: consolidated legal sources show edition `04.08.2026`, with entered-into-force changes through `15.08.2026`. Федеральный закон №308-ФЗ от 04.08.2026 directly changes article 34 and is already effective by the audit date. Base-act Kremlin pointer `kremlin.ru/acts/bank/12128` is known, but direct fetch timed out in this pass; do not elevate to `PRIMARY_DIRECT_FETCH_VERIFIED` here.

Gate: `EDITION_DATE` and `effective-through` remain separate fields.

## 2. НК РФ, часть первая — 146-ФЗ от 31.07.1998

GitHub exact search: no target body.

`repo=null; commit=null; path=null; size=null; type=null`

Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Freshness: consolidated sources show edition `04.08.2026`. At least two 04.08.2026 amendment layers must be separated by effect date: №292-ФЗ changes article 41 and Tax Code part II and is reported as effective from 04.08.2026; №281-ФЗ changes article 102 but enters into force only `01.01.2027`. Current Consultant pages also expose prepared/non-effective deltas. Therefore a single label `ред. 04.08.2026` is insufficient for an as-of-30.08.2026 body.

Primary base-act direct record not resolved in this pass: `PRIMARY_BASE_ACT_URL_BLOCKER`.

## 3. НК РФ, часть вторая — 117-ФЗ от 05.08.2000

No full GitHub body found. Two hits are control records in `Grantik/odin-vault`:

- `repo=Grantik/odin-vault`
- `commit=36366057df301bf3c76d6b56aabf1e14fb299f85`
- `path=sync/canon/law/MANIFEST.md`
- `size=METADATA_UNRESOLVED`
- `type=Markdown/file`

and

- `repo=Grantik/odin-vault`
- `commit=36366057df301bf3c76d6b56aabf1e14fb299f85`
- `path=sync/canon/law/LAW_MAP_verified.md`
- `size=METADATA_UNRESOLVED`
- `type=Markdown/file`

Body check: both are corpus/source-control documents, not the Tax Code. `LAW_MAP_verified.md` explicitly records part II as requiring manual download and says a verified official base URL was not found. Classification: `CONTROL_REFERENCE / NOT_NPA_BODY / REJECT_FOR_FULL_TEXT`.

Freshness: consolidated sources show edition `04.08.2026`. №292-ФЗ changes both Tax Code parts; №293-ФЗ changes articles 166 and 168 but enters into force `01.10.2026`. Consultant additionally flags prepared changes with other future effect dates, so norm-level effectiveness mapping is still required.

Status: `CURRENT_EDITION_CORROBORATED / FUTURE_EFFECTIVE_DELTA_PRESENT / PRIMARY_BASE_ACT_URL_BLOCKER / GITHUB_FULL_TEXT_BLOCKER`.

## 4. 115-ФЗ от 07.08.2001 «О противодействии легализации (отмыванию) доходов…»

GitHub exact search: no target body.

`repo=null; commit=null; path=null; size=null; type=null`

Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Freshness: consolidated systems expose an editorial snapshot dated `04.08.2026`, but №283-ФЗ от 04.08.2026 changes the AML law and enters into force mainly on `01.09.2026`. Therefore on `30.08.2026` the 283-ФЗ delta must be stored as `ENACTED_FUTURE_CHANGE`, not silently merged into the current-effective body. A source current shortly before enactment still showed 115-ФЗ in edition `10.06.2026`, which is consistent with this temporal split.

Base-law Kremlin identity pointer exists (`kremlin.ru/acts/bank/17274`), but direct fetch timed out in this pass. Do not treat a GitHub or consolidated copy as official publication.

## 5. 127-ФЗ от 26.10.2002 «О несостоятельности (банкротстве)»

New GitHub pipeline candidate:

- `repo=zarubinvibe/themis`
- `commit=ef0fb50772ec5384dce97a26a6d470570bd77f7c`
- `path=scripts/update_legal_corpus.py`
- `size=METADATA_UNRESOLVED`
- `type=Python/file`

Body check: script contains exact target identity and registers `doc_ids=[39331]`, intended output `knowledge/kodeksy/fz-127-bankrotstvo.md`. Fetch of that intended output at the same commit returned 404; repository search found only the downloader/citation code, not the generated law body. Classification: `RELIABLE_CORPUS_PIPELINE_CANDIDATE / NOT_NPA_BODY`.

Second hit:

- `repo=KorolevaChiana/FiveText`
- `commit=e3dffa46637f4e115b69bd1eb61642d204ae95e4`
- `path=resources/SindicatE.html`
- `size=METADATA_UNRESOLVED`
- `type=HTML/file`

Body check: investigative HTML cites article 131 and other provisions of 127-ФЗ; it is not the law. Classification: `REFERENCE_ONLY / WRONG_PRIMARY_BODY / REJECT`.

Freshness: consolidated sources show edition `04.08.2026`. №283-ФЗ introduces a `01.09.2026` future delta; №317-ФЗ of the same date also changes the bankruptcy law but becomes effective only after 180 days; №253-ФЗ of 26.07.2026 contains further changes effective in 2027. Thus there are multiple future legal states already enacted.

Status: `RELIABLE_PIPELINE_CANDIDATE_ONLY / GITHUB_FULL_TEXT_BLOCKER / MULTI_FUTURE_EFFECTIVE_STATES`.

## 6. 173-ФЗ от 10.12.2003 «О валютном регулировании и валютном контроле»

No full GitHub body. Search returns the same `Grantik/odin-vault` control records:

- `repo=Grantik/odin-vault`
- `commit=36366057df301bf3c76d6b56aabf1e14fb299f85`
- `path=sync/canon/law/LAW_MAP_verified.md` and `sync/canon/law/MANIFEST.md`
- `size=METADATA_UNRESOLVED`
- `type=Markdown/file`

`LAW_MAP_verified.md` explicitly says `Проверенного официального URL не найдено` for the base act and classifies it as manual-download work. This is useful blocker evidence but not a normative body. Classification: `CONTROL_REFERENCE / NOT_NPA_BODY / REJECT_FOR_FULL_TEXT`.

Freshness: consolidated sources show editorial date `04.08.2026`; article 6 part 2 is marked as amended by №283-ФЗ. №283-ФЗ enters into force principally `01.09.2026`, so on 30.08 the 04.08 editorial snapshot must not be equated with the current-effective text. A still-current page for article 5 shows the prior effective edition `28.12.2024`, supporting the need to keep `CURRENT_EFFECTIVE_TEXT` and `PREPARED_EDITORIAL_TEXT` separately.

Status: `PRIMARY_BASE_ACT_URL_BLOCKER / ENACTED_FUTURE_CHANGE_2026-09-01 / GITHUB_FULL_TEXT_BLOCKER`.

## New regression gates

1. `CONSOLIDATED_EDITION_DATE != CURRENT_EFFECTIVE_BODY_AS_OF` — especially when the consolidator already embeds enacted future amendments.
2. `DOWNLOADER_OR_CORPUS_REGISTRY != FULL_TEXT` — an exact title/doc_id and a planned output path are not a committed law body.
3. `CONTROL_MANIFEST_MISSING_RECORD != RELIABLE_TEXT_CANDIDATE` — useful as blocker provenance only.
4. `MULTIPLE_FUTURE_STATES_REQUIRE_NORM_LEVEL_EFFECTIVE_DATES` — 127-ФЗ already has 01.09.2026, +180-day, 2027 deltas simultaneously.

## Primary/freshness evidence used

- Habr 432466, version 28.05.2026: https://habr.com/ru/articles/432466/
- Consultant current/future consolidated pages for 53-ФЗ, NK I/II, 115-ФЗ, 127-ФЗ, 173-ФЗ.
- Official publication portal was searched separately; direct 2026 cards were not resolved reliably for every latest amendment in this pass, so no candidate was promoted to `PRIMARY_DIRECT_CARD_VERIFIED` without a directly retrieved official record.
- Kremlin base-act pointers were treated only as primary identity pointers where known; timeout/no direct fetch is recorded as a blocker, not silently upgraded.

Next queue: special-PDn items 12–18 (177-ФЗ, 79-ФЗ, 402-ФЗ, 230-ФЗ, 168-ФЗ, ПП РФ №1723/2021; 125-ФЗ already processed earlier), then Roskomnadzor/internal-PDn acts still not swept.