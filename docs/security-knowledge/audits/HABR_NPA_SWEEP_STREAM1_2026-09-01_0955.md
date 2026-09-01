# Habr NPA sweep — Stream 1 — 2026-09-01 09:55 MSK

## Scope
Continuation after `HABR_NPA_SWEEP_STREAM1_2026-09-01_0854.md`.

Habr 432466 targets reviewed in this pass:

1. Распоряжение Правительства РФ от 10.07.2013 № 1187-р — открытые данные.
2. Методические рекомендации по публикации открытых данных, версия 3.0 (протокол от 29.05.2014 № 4).
3. Указ Президента РФ от 17.03.2008 № 351.
4. Указ Президента РФ от 22.05.2015 № 260.
5. Приказ ФСО России от 07.09.2016 № 443.

The next Habr boundary is `Критическая информационная инфраструктура (КИИ)`, starting with Federal Law 187-FZ and Presidential Decree 166/2022.

## GitHub body search

| Target | repo | commit | path | size | type | classification | identity result |
|---|---|---|---|---:|---|---|---|
| 1187-р/2013 | `DimmKG/ru-phone-base` | `7acf6e1d1de9c1afd0512e1f54af46111b4130d6` | `LICENSE` | 14540 B | text/LICENSE | `MENTION_ONLY / RELATED_OPEN_DATA_LICENSE / REJECTED_AS_NORMATIVE_BODY` | Exact number/date/title appear only as a normative reference inside open-data licence terms; target disposition body absent. Blob `bc08e9543c9f41238456bed44db2a2ffbeb44ecd`. |
| Methodical recommendations v3.0/2014 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | No full text or reliable candidate found by exact title/version/distinctive-phrase search. |
| Decree 351/2008 | `kvdep/Abstracts` | `1452ed80ab3611959b9f40bf8873014322215975` | `ВУЗ/Информационное Право/Дз/ψ ДЗ 3.md` | 28924 B | Markdown | `MENTION_ONLY / STUDY_NOTES / REJECTED_AS_NORMATIVE_BODY` | Exact number/date/title plus a one-line point summary; target body absent. Blob `0f854f9726cea27851ebbfd07a579a7b271b4649`. |
| Decree 260/2015 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | Exact title and attached Procedure phrase searches returned no body/candidate. |
| FSO Order 443/2016 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | Exact title and RSNet/operator distinctive-phrase searches returned no body/candidate. |

### GitHub counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_MENTION_ONLY_REJECTED +2`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Official / current-status verification

### 1. Распоряжение Правительства РФ № 1187-р от 10.07.2013

Identity is stable. The current consolidated secondary text found in this pass is edition 10.11.2022 and includes amendments by dispositions 2757-р/2015 and 500-р/2018 and Government Resolution 2025/2022. No later amendment/repeal was confirmed in this pass.

Strict status: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER` remains because a direct primary current consolidated Government copy was not resolved. Do not promote a GitHub or secondary consolidated copy to official/current automatically.

Completeness gate for a GitHub body: disposition + all three currently approved lists. A file containing only the operative clauses or one/two lists is `PARTIAL_TEXT`.

### 2. Open-data Methodical Recommendations v3.0/2014

Habr still points to version 3.0 approved by protocol 29.05.2014 № 4. A current official Rosstat page now publishes `Методические рекомендации ... версия 4.0`; the current v4 identity is corroborated as approved by protocol of the Presidium of the Government Commission on Digital Development dated 12.12.2024 № 49пр. Rosstat also publishes Ministry of Economic Development Order 247 dated 23.04.2024 (Minjust registration 07.06.2024 № 78494) in the same current open-data methodological layer.

Classification: `HABR_STALE_METHODICAL_VERSION / CURRENT_GUIDANCE_VERSION_4_0_CONFIRMED`.

Important legal-type gate: these methodical recommendations are `NON_NPA_METHODICAL_GUIDANCE`; they must not be treated as a registered normative legal act merely because they appear in the Habr legislation reference. Formal withdrawal/repeal of v3 itself was not confirmed: `FORMAL_WITHDRAWAL_OF_V3_NOT_CONFIRMED`.

### 3. Presidential Decree № 351 dated 17.03.2008

Original identity is confirmed by the official Kremlin document bank. Secondary consolidated copies show current edition date 22.05.2015 and that clauses 2–3 lost force on 22.05.2015 under Decree 260/2015, while the decree itself was not thereby repealed as a whole.

Classification: `PARTIAL_INTERNAL_REPEAL_CONFIRMED_2015`; gate `PARTIAL_CLAUSE_REPEAL != ACT_REPEAL`.

Strict blocker: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER` because the current consolidated primary presidential body was not directly resolved in this pass.

### 4. Presidential Decree № 260 dated 22.05.2015

Identity and attached Procedure title are consistently reproduced by legal sources; no GitHub body found. A direct current primary presidential card / exact official publication pointer was not resolved in this pass.

Strict blockers: `PRIMARY_PRESIDENT_DIRECT_CURRENT_CARD_BLOCKER` and `PRIMARY_PUBLICATION_POINTER_BLOCKER`.

Completeness gate: `FULL_TEXT` requires the decree plus the entire attached `Порядок подключения ... через российский государственный сегмент ...`. Decree-only text is `PARTIAL_TEXT`.

### 5. FSO Order № 443 dated 07.09.2016

Identity is corroborated: Minjust registration 14.10.2016 № 44039. A complete secondary body includes the order and the attached Regulation on the Russian state segment of the Internet (RSNet). The official publication pointer is corroborated as `0001201610170008`, publication date 17.10.2016; direct fetch of the publication.pravo.gov.ru card timed out during this pass.

Classification: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_FETCH_BLOCKER`.

No later repeal/amendment was confirmed in this pass, but absence of a search hit is not primary proof of current status: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

Completeness gate: `FULL_TEXT` = order + full attached Regulation (sections I–V). The order itself also expressly repealed prior FSO Order 487/2009; this is historical predecessor lifecycle, not a conflict in target identity.

## New conflicts / gates

- `HABR_STALE_METHODICAL_VERSION +1` — v3.0 is no longer the current open-data methodological version; current official Rosstat publication is v4.0.
- `NON_NPA_METHODICAL_GUIDANCE +1` — methodical guidance must be separated from registered NPA.
- `PARTIAL_INTERNAL_REPEAL_CONFIRMED_2015 +1` — Decree 351 clauses 2–3 lost force, not the whole decree.
- `PARTIAL_CLAUSE_REPEAL != ACT_REPEAL`.
- `FULL_TEXT_REQUIRES_ALL_APPROVED_ATTACHMENTS` applies to 1187-р, Decree 260 and FSO Order 443.

## Sources checked

- Habr 432466 current version (28.05.2026): https://habr.com/ru/articles/432466/
- Kremlin document bank, Decree 351: https://www.kremlin.ru/acts/bank/27040
- Rosstat current methodical guidance page: https://rosstat.gov.ru/folder/12794
- Rosstat v4 PDF: https://rosstat.gov.ru/storage/mediabank/metodicheskie_rekomendacii_po_publikacii_otkrytyh_dannyh_versiya_4.0.pdf
- Official publication pointer attempted for FSO 443: https://publication.pravo.gov.ru/Document/View/0001201610170008
- Secondary consolidated control for 1187-р: https://www.consultant.ru/document/cons_doc_LAW_149441/

## Next boundary

Proceed to Habr section `Критическая информационная инфраструктура (КИИ)`, starting with 187-ФЗ/2017, Presidential Decree 166/2022, Presidential policy document 803/2012, Government Resolution 127/2018, and subsequent federal/common KII acts. Apply duplicate-target detection against the user-supplied regulatory library before counting any already-reviewed act as new.
