# Habr NPA sweep — stream 1 — 2026-08-29 23:53 MSK

## Delta

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `REJECTED_FALSE_POSITIVE +2`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `PRIMARY_CURRENT_CONSOLIDATED_BODY_CONFIRMED +1`
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED +1`
- `PRIMARY_LATEST_AMENDMENT_RELATION_CONFIRMED +1`
- `QUEUE_TITLE_CONFLICT_RESOLVED +1`
- exact duplicates: `+0`
- new body identity conflicts: `+0`

## New confirmed findings

### Постановление Правительства РФ от 15.09.2008 № 687

**GitHub:** full text not confirmed.

A semantic GitHub hit was inspected and rejected:

- repo: `ivan-niceman/mobistravel`
- commit: `5e0fc7c8ab0e25f54f7e8cf2aeef833562f01d63`
- path: `important.php`
- size: `276188` bytes
- type: `PHP/blob`
- blob: `69fda679274b29131f760ddb268b592b78e0aa2f`
- classification: `SEMANTIC_SEARCH_FALSE_POSITIVE / WRONG_BODY / NOT_FULL_TEXT / REJECT`

The body is a tourist-information page (customs/travel information), not the text of Government Resolution №687.

**Primary official status:** direct Government page provides the consolidated text of Resolution №687 and explicitly marks it as amended by Government Resolution of 18.01.2025 №12. The Government text also states that the act applies until 1 September 2030.

Primary sources:

- https://government.ru/docs/all/65436/
- https://publication.pravo.gov.ru/document/0001202501180009 — Government Resolution of 18.01.2025 №12, official publication №0001202501180009 dated 18.01.2025.

Status:

- `PRIMARY_CURRENT_CONSOLIDATED_BODY_CONFIRMED`
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`
- `GITHUB_FULL_TEXT_BLOCKER`
- `NON_OFFICIAL_GITHUB_COPY` remains mandatory for any future GitHub artifact.

### Указ Президента РФ от 30.05.2005 № 609

**GitHub:** exact-title search produced no reproducible target body; `repo/commit/path/size/type = null`.

**Primary amendment relation:** the Kremlin primary source for Presidential Decree of 31.12.2025 №1009 explicitly changes the Regulation on personal data of a state civil servant approved by Decree №609. Among other changes, points 12–15 are declared void and point 16 is amended.

Primary source:

- https://www.kremlin.ru/acts/bank/52887/print

A current consolidated secondary legal source indicates that these changes took effect on 01.01.2026. The direct primary consolidated body of base Decree №609 was not resolved in this pass, so current consolidated status is not promoted to primary-verified.

Status:

- `PRIMARY_LATEST_AMENDMENT_RELATION_CONFIRMED`
- `LATEST_AMENDMENT_EFFECTIVE_2026-01-01_CORROBORATED`
- `PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED`
- `GITHUB_FULL_TEXT_BLOCKER`

### Федеральный закон от 03.12.2008 № 242-ФЗ «О государственной геномной регистрации в Российской Федерации»

**GitHub:** exact-title search produced a hit in the full-text 152-ФЗ file already found in `Grantik/odin-vault`, but body inspection shows that the occurrence is **Federal Law of 21.07.2014 №242-ФЗ** in the amendment history of 152-ФЗ — a different law with the same number.

False-positive metadata:

- repo: `Grantik/odin-vault`
- commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
- path: `sync/canon/law/fz_152_personalnye_dannye_20060727_kremlin.txt`
- size: `53084` bytes
- type: `TXT/file`
- blob: `0ee9df5244483bf4d6559d5244236b664528c22d`
- classification: `NUMBER_COLLISION_FALSE_POSITIVE / WRONG_242_FZ / NOT_TARGET_BODY / REJECT`

**Freshness:** Federal Law of 08.03.2026 №52-ФЗ amends the target 03.12.2008 №242-ФЗ; the available publication metadata points to official publication №0001202603080008 and the amendments took effect 07.06.2026. Direct primary-card retrieval timed out, therefore this is kept as corroborated rather than primary-direct verified.

Status:

- `LATEST_AMENDMENT_CORROBORATED`
- `PRIMARY_DIRECT_CARD_TIMEOUT`
- `GITHUB_FULL_TEXT_BLOCKER`

Future GitHub copies must include the 2026 amendment state or be marked stale.

### Федеральный закон от 19.11.2021 № 367-ФЗ — queue/title conflict resolved

The previous working queue incorrectly associated №367-ФЗ with ratification of the Protocol amending Convention 108.

The Habr list and legal publication references identify the correct target as:

> Федеральный закон от 19.11.2021 №367-ФЗ «О ратификации Соглашения о взаимной правовой помощи по административным вопросам в сфере обмена персональными данными».

Corrected-title GitHub searches produced no reproducible full text or reliable candidate.

Official-publication metadata is corroborated as publication №`0001202111190005` dated 19.11.2021; direct primary-card retrieval was not completed in this pass.

Status:

- `QUEUE_TITLE_CONFLICT_RESOLVED`
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED`
- `PRIMARY_DIRECT_CARD_UNRESOLVED`
- `GITHUB_FULL_TEXT_BLOCKER`

### Постановление Правительства РФ от 06.07.2008 № 512

**GitHub:** no reproducible full body; `repo/commit/path/size/type = null`.

Secondary consolidated legal sources consistently show the current revision marker as 27.12.2012. Government Resolution of 27.12.2012 №1404 explicitly amends Resolution №512 in connection with the Federal Law «Об электронной подписи», including terminology in points 9 and 10.

The direct primary current consolidated body was not resolved in this pass.

Status:

- `LATEST_AMENDMENT_CORROBORATED`
- `PRIMARY_DIRECT_CURRENT_BODY_UNRESOLVED`
- `GITHUB_FULL_TEXT_BLOCKER`

### Федеральный закон от 19.12.2005 № 160-ФЗ

Correct exact title: «О ратификации Конвенции Совета Европы о защите физических лиц при автоматизированной обработке персональных данных».

GitHub exact-title/body searches produced no reproducible full-text artifact; `repo/commit/path/size/type = null`.

Secondary legal sources provide the full one-page act and publication history, but a direct primary current-lifecycle source was not resolved in this pass. It therefore remains:

- `GITHUB_FULL_TEXT_BLOCKER`
- `PRIMARY_CURRENT_LIFECYCLE_UNRESOLVED`

## Gates added / reinforced

1. `ACT_NUMBER_MATCH ≠ ACT_IDENTITY` — federal-law numbers repeat by year; date + number + title/body must all match. The 242-ФЗ collision is a concrete regression fixture.
2. `SEMANTIC_SEARCH_HIT ≠ NPA_BODY` — unrelated large pages must be body-classified before acceptance.
3. `PRIMARY_AMENDMENT_RELATION_CONFIRMED ≠ PRIMARY_CURRENT_CONSOLIDATED_BODY_CONFIRMED`.
4. Working-queue titles are not canonical: they must be normalized against the source list and official publication metadata before search and ingestion.
