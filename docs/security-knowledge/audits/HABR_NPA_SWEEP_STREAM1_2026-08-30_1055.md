# Habr NPA sweep — Stream 1 — 2026-08-30 10:55 MSK

## Scope

Continuation of the systematic pass over Habr 432466 and the user NPA list. This pass covers:

1. Federal Law 19.12.2005 No. 160-FZ — ratification of Convention 108.
2. Federal Law 03.12.2008 No. 242-FZ — state genomic registration.
3. Federal Law 19.11.2021 No. 367-FZ — ratification of the agreement on administrative legal assistance in personal-data exchange.
4. Presidential Decree 30.05.2005 No. 609 — personal data of federal civil servants and maintenance of personal files.

GitHub copies are treated only as non-official copies/candidates. Official publication, legal identity, current edition and lifecycle are verified independently.

## Delta

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +4`
- `REJECTED_NUMBER_COLLISION_REFERENCE +1`
- `NPA_NUMBER_COLLISION_ACROSS_YEARS +2` (`160-ФЗ`, `242-ФЗ`)
- `CURRENT_EDITION_CORROBORATED +2` (`242-ФЗ/2008`, Decree `609/2005`)
- `PRIMARY_LATEST_AMENDMENT_CONFIRMED +2` (Federal Law `52-ФЗ/2026`; Presidential Decree `1009/2025`)
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED +1` (`367-ФЗ/2021`)
- `FULLTEXT_SECONDARY_CONFIRMED +2` (`160-ФЗ/2005`, `367-ФЗ/2021`)

No new exact duplicates of a target full body. No new target-body identity conflict.

## 1. Federal Law 19.12.2005 No. 160-FZ

**Target title:** `О ратификации Конвенции Совета Европы о защите физических лиц при автоматизированной обработке персональных данных`.

### GitHub

Exact title, number/date, and broad searches did not produce a reproducible target body.

- `repo = null`
- `commit = null`
- `path = null`
- `size = null`
- `type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

A broad number-only search is unsafe: `160-ФЗ` is reused in different years for unrelated federal laws (e.g. 1999, 2001, 2005, 2006 and later). This is a confirmed `NPA_NUMBER_COLLISION_ACROSS_YEARS` case.

### Identity / official-status verification

The full legal body is independently reproduced by ConsultantPlus/Garant: State Duma adoption 25.11.2005, Federation Council approval 07.12.2005, signature 19.12.2005 No. 160-FZ. The body is not a one-line ratification: it contains several Russian declarations concerning the scope of Convention 108 and restrictions on data-subject access.

Primary historical official-publication record was not directly resolved in this pass (the act predates the modern official-publication portal coverage used in this sweep). Therefore do not promote to `PRIMARY_INITIAL_PUBLICATION_DIRECT_VERIFIED`.

- `FULLTEXT_SECONDARY_CONFIRMED`
- `PRIMARY_HISTORICAL_PUBLICATION_RECORD_UNRESOLVED`
- `GITHUB_FULL_TEXT_BLOCKER`

Completeness gate: `RATIFICATION_LAW_FULL_TEXT = COMPLETE_LAW_BODY + ALL_DECLARATIONS/RESERVATIONS`; a one-line mention that the Convention was ratified is not the full law. The Convention itself is a separate legal instrument and is not silently substituted for the ratification-law body.

Sources:
- https://www.consultant.ru/document/cons_doc_LAW_57153/
- https://base.garant.ru/12143756/

## 2. Federal Law 03.12.2008 No. 242-FZ

**Target title:** `О государственной геномной регистрации в Российской Федерации`.

### GitHub

No target body was found.

A broad `242-ФЗ` search returned a new rejected artifact:

- `repo = Grantik/odin-vault`
- `commit = c4ece018394cb8d19633b733a8320caf6f3173e5`
- `path = monitoring/feeds/legal-feed.md`
- `type = Markdown/file`
- `size = METADATA_UNRESOLVED`
- `blob = METADATA_UNRESOLVED`

Body inspection shows this is `Legal Feed — odin-vault`, explicitly marked as a non-canonical watchlist. Its `242-ФЗ` entry is a **different 2026 federal law**, not Federal Law 03.12.2008 No. 242-FZ on genomic registration.

Classification: `NUMBER_COLLISION / REFERENCE_ONLY / WRONG_ACT_YEAR / NOT_TARGET_BODY / REJECT`.

A second collision is structurally important: Federal Law No. 242-FZ dated 21.07.2014 is the well-known amendment package affecting 152-FZ/data localization. Thus at least the 2008, 2014 and 2026 acts collide under the bare string `242-ФЗ`.

Target GitHub fields remain `null`; status `GITHUB_FULL_TEXT_BLOCKER`.

### Current edition / official amendment

Current consolidated sources identify Federal Law 03.12.2008 No. 242-FZ in edition **08.03.2026**.

Federal Law 08.03.2026 No. 52-FZ directly amends the genomic-registration regime. The official publication portal confirms:

- act: Federal Law 08.03.2026 No. 52-FZ
- publication number: `0001202603080008`
- publication date: `08.03.2026`

The amendment law provides a 90-day delayed commencement; current legal sources mark the relevant changes as effective from **07.06.2026**. Therefore the 08.03.2026 edition is already effective as of this pass.

- `CURRENT_EDITION_CORROBORATED_2026-03-08`
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`
- `LATEST_AMENDMENT_RELATION_CONFIRMED`
- `EFFECTIVE_FROM_2026-06-07`
- `GITHUB_FULL_TEXT_BLOCKER`

Sources:
- https://www.consultant.ru/document/cons_doc_LAW_82263/
- https://publication.pravo.gov.ru/document/0001202603080008
- https://www.garant.ru/products/ipo/prime/doc/413713292/

## 3. Federal Law 19.11.2021 No. 367-FZ

**Target title:** `О ратификации Соглашения о взаимной правовой помощи по административным вопросам в сфере обмена персональными данными`.

### GitHub

Exact and broad searches returned no reproducible target body.

- `repo = null`
- `commit = null`
- `path = null`
- `size = null`
- `type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### Identity / publication

Independent full-text sources confirm the exact title, adoption/approval chain and body: the law ratifies the agreement signed 18.12.2020.

The official-publication pointer is corroborated as:

- publication number `0001202111190005`
- publication date `19.11.2021`

The law entered into force 30.11.2021 according to the publication/legal reference record.

Direct official-portal body retrieval was not stable in this pass, so classification remains `OFFICIAL_PUBLICATION_POINTER_CORROBORATED`, not `PRIMARY_DIRECT_BODY_VERIFIED`.

- `FULLTEXT_SECONDARY_CONFIRMED`
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED`
- `PRIMARY_DIRECT_BODY_UNRESOLVED`
- `GITHUB_FULL_TEXT_BLOCKER`

Source:
- https://base.garant.ru/403083340/
- official pointer: https://publication.pravo.gov.ru/document/0001202111190005

## 4. Presidential Decree 30.05.2005 No. 609

**Target title:** `Об утверждении Положения о персональных данных государственного гражданского служащего Российской Федерации и ведении его личного дела`.

### GitHub

Exact title/number/date searches returned no reproducible target body.

- `repo = null`
- `commit = null`
- `path = null`
- `size = null`
- `type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Completeness gate: a future copy is `FULL_TEXT` only if it contains the signing decree **and the complete approved Regulation**.

### Current edition / primary amendment

Current consolidated legal sources identify Decree No. 609 in edition **31.12.2025**.

The Kremlin publishes the complete text of Presidential Decree 31.12.2025 No. 1009. Its amendment list directly names the Regulation approved by Decree 30.05.2005 No. 609 and changes it, including repeal of paragraphs 12–15 and amendment of paragraph 16.

Therefore:

- `CURRENT_EDITION_CORROBORATED_2025-12-31`
- `PRIMARY_LATEST_AMENDMENT_FULLTEXT_CONFIRMED`
- `LATEST_AMENDMENT_RELATION_PRIMARY_CONFIRMED`
- `GITHUB_FULL_TEXT_BLOCKER`

Sources:
- https://www.kremlin.ru/acts/bank/52887/print
- https://www.consultant.ru/document/cons_doc_LAW_53747/90a1cfd28b8c8fc4a5858519d3f08a06453f7f29/

## New regression gates

1. `NPA_NUMBER_ALONE_NOT_IDENTITY` — a number such as `160-ФЗ` or `242-ФЗ` is not a stable identifier across years.
2. `BROAD_NUMBER_SEARCH_HIT != SAME_ACT` — a GitHub hit must pass `act_type + date + number + title/body` identity before becoming a candidate.
3. `RATIFICATION_LAW_FULL_TEXT != TREATY_REFERENCE` — a ratification law must preserve the entire law body, including declarations/reservations; the underlying treaty remains a separate instrument.
4. `FULL_TEXT_FOR_DECREE_WITH_APPROVED_REGULATION = DECREE + COMPLETE_REGULATION`.
5. GitHub provenance never implies official publication or official-copy status.
