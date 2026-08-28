# Habr NPA sweep — Stream 1 — 2026-08-28 14:52 MSK

## Delta

- New confirmed standalone FULL_TEXT: **1**.
- New reliable GitHub secondary candidate: **1**.
- New exact-duplicate sets: **0**.
- New identity conflicts: **0**.
- Currentness conflict: **1** (GitHub copy of 184-FZ is a 2023-era consolidated text; official later amendments exist in 2025 and 2026).

## 1. Federal Law of 27.12.2002 No. 184-FZ — On Technical Regulation

**GitHub source**

- repo: `VictorKVS/gpt-agent`
- commit/ref: `ef8b02c1e0e997e028efc1dd2f3d30dc7e1cdce8`
- path: `дОКУМЕНТЫ ЗАГРУЖАЕМЫЕ В АГЕНТ/Техническое регулирование/Федеральный закон от 27.12.2002 N 184-ФЗ «О техническом регулировании»/Федеральный закон от 27 декабря 2002 г N 184 ФЗ О техническом ре.txt`
- size: `841334` bytes
- type: `TXT/blob`
- blob SHA: `7b7dfa55d2d67f49b171e1f2aa641c94f59bfaf8`

**Body identity check**

The body independently identifies `Федеральный закон от 27 декабря 2002 г. N 184-ФЗ "О техническом регулировании"`, states adoption by the State Duma on 15.12.2002 and approval by the Federation Council on 18.12.2002, and contains substantive article bodies beginning with Chapter 1 / Article 1. Search over the same blob also resolves the closing presidential signature. Therefore this is a substantive consolidated normative text, not a TOC, card, mention, or summary.

The header lists amendments through **25.12.2023**. The export itself is marked by GARANT with date `26.11.2024` and includes future-effective notes originating from the 25.12.2023 amendments; this does not make it a 2025/2026 consolidated version.

**Official/currentness check**

Primary official publication independently proves later amendment events:

- Federal Law of 23.07.2025 No. 262-FZ, `О внесении изменения в Федеральный закон "О техническом регулировании"`, official publication No. `0001202507230066`, 23.07.2025: https://publication.pravo.gov.ru/document/0001202507230066
- Federal Law of 02.05.2026 No. 126-FZ, `О внесении изменений в отдельные законодательные акты Российской Федерации и признании утратившим силу пункта 15 статьи 46 Федерального закона "О техническом регулировании"`, official publication No. `0001202605020011`, 02.05.2026: https://publication.pravo.gov.ru/document/0001202605020011

Current legal-reference sources in the sweep expose 184-FZ as amended through **02.05.2026**. Therefore the GitHub copy is not current.

**Classification**: `FULL_TEXT / CONSOLIDATED_GARANT_EXPORT / NON_OFFICIAL_GITHUB_COPY / REVISION_THROUGH_25.12.2023 / STALE_BEFORE_262-FZ_2025_AND_126-FZ_2026`.

## 2. Roskomnadzor Order of 19.06.2025 No. 140 — de-identification requirements and methods

**GitHub candidate**

- repo: `Namelomax/Anon`
- commit/ref: `79277627343e5df8ed4ab3893e7dad4dda5d42ac`
- path: `anonymizer/ЮРИДИЧЕСКИЕ_ДОКУМЕНТЫ/07_Соответствие_приказу_РКН_140.md`
- size: `24031` bytes
- type: `Markdown/blob`
- blob SHA: `723b5960e5f460c2b17499825868d706f01094b8`

**Body classification**

The file correctly identifies Order No. 140 of 19.06.2025 and builds a detailed compliance matrix against its requirements and Appendix No. 2. It quotes selected clauses and maps them to a software implementation. It is nevertheless an audit/compliance guide, not the normative body of the order: the document is organized as an implementation audit with findings, statuses and remediation guidance rather than the complete official act and appendices.

**Official identity check**

Primary official publication confirms the exact act: Roskomnadzor Order of 19.06.2025 No. 140, registered by the Ministry of Justice on **31.07.2025 No. 83110**, official publication No. **0001202508010002** on **01.08.2025**: https://publication.pravo.gov.ru/document/0001202508010002 . The order entered into force on 01.09.2025 (also confirmed by the Ministry of Justice regional explanatory publication).

**Classification**: `SECONDARY_COMPLIANCE_GUIDE / DETAILED_DERIVATIVE / SELECTIVE_QUOTES / NOT_FULL_TEXT / REJECT_FOR_PRIMARY_KB`.

**Open blocker**: standalone GitHub full text of Roskomnadzor Order No. 140 remains unconfirmed.

## Regression gates added

1. `DETAILED_COMPLIANCE_CROSSWALK != NORMATIVE_FULL_TEXT` — a legally detailed implementation audit with verbatim clauses must remain in the secondary layer unless the complete normative structure is present.
2. `EXPORT_DATE != CONSOLIDATED_REVISION_DATE` — a GARANT/Consultant export timestamp does not prove that amendments adopted after the last listed revision are incorporated.
3. Currentness requires a separate official amendment-chain check; a body-valid GitHub copy can still be legally stale.
