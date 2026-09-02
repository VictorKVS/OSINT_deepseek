# Habr NPA sweep — Stream 1 — 2026-09-02 10:52 MSK

Scope: `Персональные данные → Особые случаи обработки ПДн`, федеральный/core слой, позиции 16–18 после ранее закрытых 173-ФЗ / 177-ФЗ / 79-ФЗ / 125-ФЗ / 402-ФЗ.

Method gates retained:
- GitHub copy is never treated as an official source automatically.
- `FULL_TEXT` requires internal identity match by number/date/title and a body-completeness check.
- Mentions, compliance code, datasets, migrations, summaries and cross-document references are rejected as normative bodies.
- Currency/current status and official publication are checked independently from GitHub provenance.

## 16. Federal Law 230-FZ dated 03.07.2016

Target: `О защите прав и законных интересов физических лиц при осуществлении деятельности по возврату просроченной задолженности ...`.

### GitHub
No full normative body or reliable full-body candidate confirmed.

Representative inspected derived hit:
- repo: `NikitaSuvorov1/collection_project`
- commit: `5680b474268fff348ef2ae0b2ea7682084313f75`
- path: `backend/collection_app/services/compliance_230fz.py`
- size: `6314 B`
- type: `Python (.py)`
- blob: `45b8992390840faacce641adc3040ea6de2337cd`
- classification: `DERIVED_COMPLIANCE_CODE / MENTION_ONLY / REJECTED_AS_NORMATIVE_BODY`

The file implements checks derived from 230-FZ constraints; it is not the text of the law.

Search hazard: `NUMBER_COLLISION_230`. Search results also contain another Federal Law No. 230-FZ from 2012. Number-only identity is therefore rejected; date/title/internal requisites are mandatory.

### Current / official layer
- Reliable consolidated legal sources show 230-FZ in edition `11.02.2026`.
- Federal Law No. 20-FZ dated `11.02.2026` amends article 17.1 of target 230-FZ.
- Official publication pointer for No. 20-FZ: `0001202602120002`; publication date `12.02.2026`.
- No. 20-FZ entered into force `01.09.2026`; therefore this layer is already effective as of this sweep.

Classification:
- `CURRENT_EDITION_SECONDARY_CONFIRMED_2026-02-11`
- `PRIMARY_AMENDING_ACT_PUBLICATION_CONFIRMED`
- `CURRENT_EFFECTIVE_LAYER_ACTIVATED_2026-09-01`
- `SIGNED_PRE_HABR_EFFECTIVE_POST_HABR`
- `GITHUB_FULL_TEXT_BLOCKER`

## 17. Federal Law 168-FZ dated 08.06.2020

Target: `О едином федеральном информационном регистре, содержащем сведения о населении Российской Федерации`.

### GitHub
No full normative body confirmed.

Representative inspected wrong-target/mention hit:
- repo: `losper8/hack_13_04`
- commit: `db19ad330af9f12531960fbc3e683fe2d08ed31d`
- path: `DolyaAl/raw_dataset/arrangement/dopolnitelnoe-soglashenie-n-8-k-soglasheniiu-ob.txt`
- size: `UNRESOLVED_CONNECTOR_METADATA`
- type: `text/plain`
- blob: `UNRESOLVED_CONNECTOR_METADATA`
- classification: `DIFFERENT_DOCUMENT_BODY / MENTION_ONLY / TARGET_IDENTITY_MISMATCH / REJECTED_AS_TARGET_BODY`

Internal identity check shows the file is `Дополнительное соглашение N 8 к Соглашению о взаимодействии между Министерством внутренних дел РФ и Пенсионным фондом РФ...`; 168-FZ appears only as a referenced legal basis.

### Current / official layer
- Reliable consolidated sources show current edition `28.11.2025`.
- Federal Law No. 442-FZ dated `28.11.2025` directly amends articles 4 and 11 of 168-FZ.
- Official publication portal confirms No. 442-FZ, publication ID `0001202511280105`, publication date `28.11.2025`, PDF `185 KB / 4 pages`.
- Article 3 of No. 442-FZ sets entry into force after 180 days; secondary legal reproduction resolves this to `28.05.2026`.

Classification:
- `CURRENT_EDITION_SECONDARY_CONFIRMED_2025-11-28`
- `PRIMARY_AMENDING_ACT_PUBLICATION_CONFIRMED`
- `CURRENT_EFFECTIVE_LAYER_2026-05-28_CONFIRMED`
- `GITHUB_FULL_TEXT_BLOCKER`

## 18. Government Resolution RF No. 1723 dated 09.10.2021

Target: rules for providing information from the unified federal population register, including the list/timing of information and the list of anonymized personal data.

### GitHub
Exact long-title, number/date and characteristic-phrase searches produced no full-body or reliable body candidate.

Metadata:
- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### Current / official layer
- Original official publication pointer is known: `0001202110140018`, publication date `14.10.2021`, official PDF `460 KB / 15 pages`.
- Direct fetch of that official card failed in this pass (`cache miss`), so pointer discovery and direct primary-body retrieval remain separate gates.
- Reliable consolidated sources show current edition `28.05.2026`.
- Government Resolution No. 612 dated `28.05.2026` directly amends No. 1723.
- Exact primary publication pointer for No. 612 was not resolved in this pass; the amendment is therefore current-status confirmed via reliable legal reproduction, but its primary publication card remains a blocker.

Classification:
- `PRIMARY_ORIGINAL_PUBLICATION_POINTER_CONFIRMED`
- `PRIMARY_ORIGINAL_DIRECT_FETCH_BLOCKER`
- `CURRENT_EDITION_SECONDARY_CONFIRMED_2026-05-28`
- `PRIMARY_AMENDING_ACT_612_PUBLICATION_POINTER_BLOCKER`
- `GITHUB_FULL_TEXT_BLOCKER`

## New counters for this batch

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +3`
- `GITHUB_DERIVED_OR_WRONG_TARGET_REJECTED +2 confirmed inspected representative files`
- `GITHUB_CANDIDATE_TARGET_IDENTITY_MISMATCH +1`
- `NUMBER_COLLISION +1`
- `PRIMARY_AMENDING_ACT_PUBLICATION_CONFIRMED +2` (20-FZ, 442-FZ)
- `PRIMARY_ORIGINAL_PUBLICATION_POINTER_CONFIRMED +1` (PP RF 1723)
- `PRIMARY_ORIGINAL_DIRECT_FETCH_BLOCKER +1`
- `PRIMARY_AMENDING_ACT_PUBLICATION_POINTER_BLOCKER +1` (PP RF 612)
- `CURRENT_EFFECTIVE_LAYER_ACTIVATED_2026-09-01 +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Next boundary

The two immediately following Habr positions are a Moscow regional law and a Minfin explanatory letter. Keep them in a separate regional/explanatory layer rather than silently mixing them into the federal/core-NPA registry. Continue the next federal/core item after that boundary while preserving deduplication against already processed common acts.
