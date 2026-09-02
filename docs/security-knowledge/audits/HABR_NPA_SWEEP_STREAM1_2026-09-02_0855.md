# Habr NPA sweep — Stream 1 — 2026-09-02 08:55 MSK

Scope: Habr 432466, section `Персональные данные. Особые случаи обработки ПДн`, positions 6–10.

Rules used in this pass:
- GitHub copy is never treated as an official source merely because it is on GitHub.
- Full body requires identity confirmation inside content (number/date/title) plus substantive normative body, not only headings, mentions, summaries or implementation guidance.
- Current legal status / effective layer is tracked separately from GitHub-copy classification.
- Official publication pointer and successful direct read of the primary official body are separate gates.

## 1. Federal Law 53-FZ of 1998-03-28 — `О воинской обязанности и военной службе`

GitHub hit:
- repo: `Code-Labb/groza`
- commit: `f98d85377439d593f7f1f414e05165612c100bc7`
- path: `learning/ustav/chapter_one.html`
- size: `14698 B`
- type: `HTML/blob`
- blob: `61477c16c19b2ff0ded7552f61c585177297fca1`
- identity check: the page cites `Федеральный закон от 28.03.1998 N 53-ФЗ ... О воинской обязанности и военной службе`, but does not contain the law body.
- classification: `MENTION_ONLY / EDUCATIONAL_PAGE / REJECTED_AS_NORMATIVE_BODY`
- GitHub full text: `BLOCKER`

Fresh legal-status layer:
- signed/amending layer dated 2026-08-04 affects 53-FZ; current consolidated secondary sources show edition date `2026-08-04` and changes entering into force by `2026-08-31`.
- official publication pointer identified for 334-FZ: `0001202608040078`.
- classification: `POST_HABR_CURRENT_EDITION_ADVANCE / CURRENT_EDITION_ADVANCED_53FZ_2026-08-04`.
- direct primary body fetch: `BLOCKER` (pointer identified != direct body read).

## 2. Tax Code RF, Part One — 146-FZ of 1998-07-31

GitHub hit A:
- repo: `infoculture/finguide`
- commit: `d87540a90eb23c17e56ab1f3e8364615df0efa52`
- path: `wiki/legal/tax-code.md`
- size/blob: `UNRESOLVED_CONNECTOR_METADATA`
- type: `Markdown`
- content: practical summary beginning with an explanation that the Tax Code consists of two parts; not a normative body.
- classification: `SUMMARY_ONLY / PRACTICAL_GUIDE / REJECTED_AS_NORMATIVE_BODY`

GitHub hit B:
- repo: `IvanchikIvanov/ZkonRf`
- commit: `2ed96981f48397751ce05f735315b3b82302802c`
- path: `data/codexes/ru/zpp_nk_rf_part1.txt`
- size: `34473 B`
- type: `text/plain`
- blob: `06cdb7b9968848afaef0cbd6b8d5b44d3503cd01`
- content: article/section headings and RAG labels; substantive article bodies absent.
- classification: `STRUCTURAL_INDEX / ARTICLE_TITLES_AND_HEADERS_ONLY / RAG_SOURCE_EXTRACT / REJECTED_AS_NORMATIVE_BODY`
- GitHub full text: `BLOCKER`

Fresh legal-status layer:
- 292-FZ of 2026-08-04 changes Tax Code Parts One and Two; official publication pointer identified: `0001202608040036`.
- classification: `POST_HABR_CURRENT_EDITION_ADVANCE / CURRENT_EDITION_ADVANCED_NK1_2026-08-04`.
- separate future signed layer: 281-FZ of 2026-08-04, official pointer `0001202608040006`, relevant NK Part One change effective `2027-01-01`.
- classification: `SIGNED_FUTURE_LAYER_NK1_281FZ_EFFECTIVE_2027-01-01` (must not be merged into current effective edition before that date).

## 3. Tax Code RF, Part Two — 117-FZ of 2000-08-05

GitHub hit A:
- same physical `infoculture/finguide@d87540a90eb23c17e56ab1f3e8364615df0efa52/wiki/legal/tax-code.md` as above.
- classification for this target: `KNOWN_DERIVED_FILE_MULTI_TARGET_MENTION / SUMMARY_ONLY / REJECTED_AS_NORMATIVE_BODY`.

GitHub hit B:
- repo: `IvanchikIvanov/ZkonRf`
- commit: `2ed96981f48397751ce05f735315b3b82302802c`
- path: `data/codexes/ru/zpp_nk_rf_part2.txt`
- size: `43226 B`
- type: `text/plain`
- blob: `e70819146c918661707d7cfc805b96b553c23d11`
- content: article/section headings and RAG labels only; substantive normative body absent.
- classification: `STRUCTURAL_INDEX / ARTICLE_TITLES_AND_HEADERS_ONLY / RAG_SOURCE_EXTRACT / REJECTED_AS_NORMATIVE_BODY`
- GitHub full text: `BLOCKER`

Fresh legal-status layer:
- 292-FZ of 2026-08-04 affects Part Two as well; current edition layer advanced after Habr 28.05.2026.
- classification: `POST_HABR_CURRENT_EDITION_ADVANCE / CURRENT_EDITION_ADVANCED_NK2_2026-08-04`.
- future signed layer: 293-FZ of 2026-08-04, official pointer `0001202608040029`, relevant changes effective `2026-10-01`.
- classification: `SIGNED_FUTURE_LAYER_NK2_293FZ_EFFECTIVE_2026-10-01`.

## 4. Federal Law 115-FZ of 2001-08-07 — AML/CFT

GitHub hit:
- repo: `voyn88/ai-command-center`
- commit: `f799f78bc25aee263367930fd6a17affce726f67`
- path: `docs/aml/COMPLIANCE_CHECKLIST.md`
- size/blob: `UNRESOLVED_CONNECTOR_METADATA`
- type: `Markdown`
- content: AML compliance checklist referencing 115-FZ as a legal basis; not the law body.
- classification: `DERIVED_COMPLIANCE_CHECKLIST / MENTION_ONLY / REJECTED_AS_NORMATIVE_BODY`
- GitHub full text: `BLOCKER`

Fresh legal-status layer:
- 283-FZ of 2026-08-04 changes 115-FZ; official publication pointer identified: `0001202608040008`; relevant layer effective `2026-09-01`.
- classification: `POST_HABR_CURRENT_EDITION_ADVANCE / CURRENT_EDITION_ADVANCED_115FZ_2026-08-04 / CURRENT_EFFECTIVE_LAYER_283FZ_2026-09-01`.
- one secondary consolidated source still labels the base law as edited `2026-06-10` while incorporating later changes: `SECONDARY_CONSOLIDATION_LAG_115FZ`; do not treat that metadata label as primary-status truth.

## 5. Federal Law 127-FZ of 2002-10-26 — `О несостоятельности (банкротстве)`

GitHub hit:
- repo: `IvanchikIvanov/ZkonRf`
- commit: `2ed96981f48397751ce05f735315b3b82302802c`
- path: `data/codexes/ru/zpp_127_fz_bankruptcy.txt`
- size: `44103 B`
- type: `text/plain`
- blob: `be2b5dcbf2fa3d9577acbe7210f22a796884edf7`
- identity: target law is identified in headers/change list, but distinctive substantive body text is absent; file is an article-title/section index for RAG.
- classification: `STRUCTURAL_INDEX / ARTICLE_TITLES_AND_HEADERS_ONLY / RAG_SOURCE_EXTRACT / REJECTED_AS_NORMATIVE_BODY`
- GitHub full text: `BLOCKER`

Fresh legal-status layer:
- consolidated systems label the document `ред. от 04.08.2026`, but the verified 2026-08-04 amendment identified in this pass is 317-FZ and it has not yet entered into force.
- 317-FZ of 2026-08-04 expressly amends 127-FZ; official publication pointer identified: `0001202608040042`; effective `2027-02-01`.
- classification: `POST_HABR_SIGNED_FUTURE_EDITION_LAYER / SIGNED_FUTURE_LAYER_127FZ_317FZ_EFFECTIVE_2027-02-01`.
- correction gate: do **not** attribute the 127-FZ 2026-08-04 layer to 283-FZ; 283-FZ was verified here as amending 115-FZ, while 317-FZ is the verified 2026-08-04 amendment to 127-FZ.

## Cross-target / duplicate findings

- `infoculture/finguide/wiki/legal/tax-code.md` is one physical derived file hitting both Tax Code Part One and Part Two: `DERIVED_MULTI_TARGET_FILE +1`; it is not a normative-body duplicate.
- `IvanchikIvanov/ZkonRf` files for NK Part One, NK Part Two and 127-FZ are distinct blobs; no byte duplicate among them.
- `NEW_GITHUB_FULL_BODY_DUPLICATE = 0`.
- `NEW_BODY_IDENTITY_CONFLICT = 0`.

## Batch counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `STRUCTURAL_INDEX_REJECTED +3`
- `DERIVED_OR_MENTION_REJECTED +4 target-hits / 3 distinct files`
- `DERIVED_MULTI_TARGET_FILE +1`
- `POST_HABR_CURRENT_EDITION_ADVANCE +4`
- `POST_HABR_SIGNED_FUTURE_EDITION_LAYER +1`
- `SIGNED_FUTURE_LAYER +3`
- `SECONDARY_CONSOLIDATION_LAG +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_BODY_IDENTITY_CONFLICT +0`

## Next boundary

Continue `Персональные данные. Особые случаи обработки ПДн` from position 11:
- 173-FZ of 2003-12-10 `О валютном регулировании и валютном контроле`
- 177-FZ of 2003-12-23 `О страховании вкладов физических лиц в банках Российской Федерации`
- 79-FZ of 2004-07-27 `О государственной гражданской службе Российской Федерации`
- 125-FZ of 2004-10-22 `Об архивном деле в Российской Федерации`
- 402-FZ of 2011-12-06 `О бухгалтерском учете`

Primary-source note: identified `publication.pravo.gov.ru` document IDs are stored as publication pointers. A pointer is not upgraded to `PRIMARY_BODY_DIRECT_FETCH_CONFIRMED` unless the official body itself was successfully fetched/read.