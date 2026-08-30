# Habr NPA sweep — stream 1 — 2026-08-30 12:53 MSK

Scope: next unprocessed PDn block from Habr 432466. GitHub copies are treated only as non-official corpus candidates; legal status/freshness is checked separately.

## Delta

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +5
- DUPLICATE_REFERENCE_ARTIFACT: +1
- CURRENT_EDITION_CORROBORATED: +4
- PRIMARY_CURRENT_RECORD_CONFIRMED: +1
- PRIMARY_LATEST_AMENDMENT_CONFIRMED: +1
- PRIMARY_DIRECT_RECORD_UNRESOLVED: 3
- BODY_IDENTITY_CONFLICT: +0
- EXACT_FULLTEXT_DUPLICATE: +0

## Records

### Указ Президента РФ от 29.12.2012 № 1709
Title: «О паспорте гражданина Российской Федерации, удостоверяющем личность гражданина Российской Федерации за пределами территории Российской Федерации, содержащем на электронном носителе информации дополнительные биометрические персональные данные его владельца».

GitHub exact search: no target body.
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: GITHUB_FULL_TEXT_BLOCKER

Identity/currentness: consolidated legal source shows edition 07.12.2016; amendment relation is Указ Президента РФ от 07.12.2016 № 656. Full body identity is internally consistent through final requisites (29.12.2012, № 1709). Direct primary current record was not resolved in this pass, therefore do not promote to PRIMARY_CURRENT_VERIFIED.

### Указ Президента РФ от 24.11.2014 № 735
Title: «О сборе биометрических персональных данных иностранных граждан и лиц без гражданства».

GitHub exact search: no target body.
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: GITHUB_FULL_TEXT_BLOCKER

Identity: consolidated full text confirms the exact date/number/title and operative body beginning with biometric collection from 10.12.2014. No direct primary current record was resolved in this pass. Number-only search is unsafe because № 735 is reused by unrelated Presidential decrees in other years.

### Постановление Правительства РФ от 06.07.2008 № 512
Title: «Об утверждении требований к материальным носителям биометрических персональных данных и технологиям хранения таких данных вне информационных систем персональных данных».

GitHub exact search: no target body.
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: GITHUB_FULL_TEXT_BLOCKER

Currentness: current consolidated sources show edition 27.12.2012. Amendment source: ПП РФ от 27.12.2012 № 1404. FULL_TEXT gate = постановление + complete approved Requirements; resolution-only copy is PARTIAL_TEXT. Direct primary current record unresolved in this pass.

### Постановление Правительства РФ от 15.09.2008 № 687
Title: «Об утверждении Положения об особенностях обработки персональных данных, осуществляемой без использования средств автоматизации».

GitHub search returns one already-known non-target artifact:
- repo: Grantik/odin-vault
- commit: c4ece018394cb8d19633b733a8320caf6f3173e5
- path: sync/canon/package/samples/koncepciya_gis_rt_teo.txt
- blob: 067866c9fe3b098c0432205ca554945298e53bd8
- size: 345746 bytes
- type: TXT/file
- classification: DUPLICATE_REFERENCE_ARTIFACT / REFERENCE_ONLY / WRONG_PRIMARY_BODY / REJECT

Body inspection identifies the file as «Концепция государственной информационной системы “Российский транспорт”», Москва 2024; № 687 is only a normative reference.

Primary Government record confirms the target act and explicitly states current validity through 01.09.2030. Latest edition is 18.01.2025; ПП РФ от 18.01.2025 № 12 directly changes № 687 and official publication record is 0001202501180009 dated 18.01.2025.

### Постановление Правительства РФ от 29.06.2021 № 1046
Title: «О федеральном государственном контроле (надзоре) за обработкой персональных данных».

GitHub exact search: no target body.
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: GITHUB_FULL_TEXT_BLOCKER

Freshness: consolidated sources show amendments 16.12.2021, 27.08.2025 and 03.07.2026. Primary Government full text confirms amendment ПП РФ от 27.08.2025 № 1286. Latest amendment is ПП РФ от 03.07.2026 № 833; official publication pointer 0001202607030035 dated 03.07.2026 is corroborated, with entry into force 11.07.2026. Direct official publication card for № 833 was not fetched successfully in this pass, so status is OFFICIAL_PUBLICATION_POINTER_CORROBORATED, not PRIMARY_DIRECT_CARD_VERIFIED.

FULL_TEXT gate = постановление + complete approved Положение, including current 2026 wording.

## New regression gates

1. NUMBER_ONLY_SEARCH_UNSAFE_FOR_PRESIDENTIAL_DECREES: same decree number recurs across years; identity key must include type + date + number + title/body.
2. VALID_UNTIL is independent from edition date: № 687 is current edition 18.01.2025 but has an explicit legal horizon through 01.09.2030.
3. CURRENT_BODY requires latest effective amendment, not merely latest Government page found: for № 1046 the 2025 Government amendment is not the freshness floor because № 833/2026 is already effective.
4. GitHub hit dedupe remains by repo + commit + path + blob; the GIS RT concept is not a new candidate.

## Source pointers

- Habr 432466, PDn block: https://habr.com/ru/articles/432466/
- Government № 687 current page: https://government.ru/docs/all/65436/
- Official publication № 12/2025: https://publication.pravo.gov.ru/document/0001202501180009
- Government № 1286/2025 amending № 1046: https://government.ru/docs/all/160681/
- Official publication pointer № 833/2026: https://publication.pravo.gov.ru/document/0001202607030035
- GitHub rejected artifact: https://github.com/Grantik/odin-vault/blob/c4ece018394cb8d19633b733a8320caf6f3173e5/sync/canon/package/samples/koncepciya_gis_rt_teo.txt
