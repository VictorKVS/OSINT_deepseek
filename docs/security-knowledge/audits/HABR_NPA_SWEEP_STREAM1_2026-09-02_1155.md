# Habr NPA sweep — Stream 1 — 2026-09-02 11:55 MSK

Scope: Habr 432466, section `Персональные данные. Особые случаи обработки ПДн` items 19–20, then `Персональные данные. Сроки хранения` items 1–7.

Method: GitHub copy/candidate identity is verified independently from legal status/currentness. A GitHub file is never treated as an official source merely because it reproduces an act. `FULL_TEXT` requires the normative body, not a citation, source list, search log, implementation checklist, summary, code comment, or structural metadata.

## Findings

### Habr special case #19 — Закон г. Москвы от 22.12.2004 N 90 «О квотировании рабочих мест»

- Layer: `REGIONAL_NON_CORE` (kept in the Habr sweep but not mixed into the federal/core NPA register).
- GitHub exact-title/number search: no full body or reliable body candidate found.
- GitHub metadata: `repo=null; commit=null; path=null; size=null; type=null`.
- Classification: `GITHUB_FULL_TEXT_BLOCKER`.
- Currentness: secondary legal systems show amendments through Moscow Law N 35 of 15.12.2021; recent 2026 court practice still applies N 90.
- Official-status gate: no direct current official Moscow primary copy was resolved in this pass.
- Blocker: `PRIMARY_MOSCOW_CURRENT_STATUS_BLOCKER`.

### Habr special case #20 — Письмо Минфина России от 25.10.2018 N 03-01-11/76554

- GitHub exact number/title search: no full body or reliable candidate found.
- GitHub metadata: `repo=null; commit=null; path=null; size=null; type=null`.
- Classification: `NON_NPA_EXPLANATORY_LETTER / GITHUB_FULL_TEXT_BLOCKER`.
- Secondary reproductions confirm date, number and the position that an INN is not included in the cited list of personal data.
- Legal-status rule: do not elevate this letter into a generally binding NPA or a universal rule on INN merely from the Habr comment.
- Blocker: direct original on a Ministry of Finance primary resource not resolved: `PRIMARY_MINFIN_ORIGINAL_BLOCKER`.

### Retention #1 — Постановление ФКЦБ РФ от 16.07.2003 N 03-33/пс

Target: «Об утверждении Положения о порядке и сроках хранения документов акционерных обществ».

New GitHub hit pair (byte-identical derived copies):

1. `repo=blondinkaizakon/HSE_Oksana_Petrovskaya`
   - `commit=cbb2ac84cda1974042505a534833b1d196181cbc`
   - `path=VKR/rag-system/documents/corp_law/общее собрание.md`
   - `size=108618 B`
   - `type=Markdown`
   - `blob=bacc770231c7460396a83a3a8ef7f807a9a40971`
2. `repo=blondinkaizakon/HSE_Oksana_Petrovskaya`
   - `commit=cbb2ac84cda1974042505a534833b1d196181cbc`
   - `path=VKR/rag-system/documents/knowledge_base/corp_law/общее собрание.md`
   - `size=108618 B`
   - `type=Markdown`
   - `blob=bacc770231c7460396a83a3a8ef7f807a9a40971`

Internal identity check: the file itself is a practical article «Как подготовить и провести годовое общее собрание ООО» and only cites clauses 3.7 and 2.1.11 of N 03-33/пс. It is not the normative body.

Classification: `DERIVED_LEGAL_GUIDANCE / PARTIAL_CITATION / REJECTED_AS_NORMATIVE_BODY`.

Duplicate: `DERIVED_BYTE_DUPLICATE_CONFIRMED` — two paths, same size and blob. This is **not** a full-body NPA duplicate.

GitHub full body remains: `GITHUB_FULL_TEXT_BLOCKER`.

Current/legal status: current secondary systems identify the original 16.07.2003 edition, registration in Ministry of Justice N 4994 (21.08.2003), and current status as acting. Publication metadata points to Rossiyskaya Gazeta N 168, 26.08.2003. No later amendment was confirmed in this pass. Direct primary original/current body remains a separate gate: `PRIMARY_ORIGINAL_DIRECT_FETCH_BLOCKER`.

### Retention #2 — Приказ Росархива от 20.12.2019 N 236

Target: «Об утверждении Перечня типовых управленческих архивных документов, образующихся в процессе деятельности государственных органов, органов местного самоуправления и организаций, с указанием сроков их хранения».

GitHub hit:
- `repo=sergey-globus/Scala_project`
- `commit=b9321afe034c946043d8e449b6971db55db9b84d`
- `path=data/Сессии/6427`
- `size=UNRESOLVED_CONNECTOR_METADATA`
- `type=text/plain`
- `blob=ce8ea37aff3c0bdc23f92d6d70ab87360182dfc1`

Internal check: this is a user/search session log. The exact target date/number/title occurs only in a `QS` search query followed by internal document IDs and `DOC_OPEN` events. No normative body is present.

Classification: `SEARCH_SESSION_LOG / QUERY_MENTION_ONLY / REJECTED_AS_NORMATIVE_BODY`.

GitHub full body: `GITHUB_FULL_TEXT_BLOCKER`.

Primary publication metadata confirmed through Rossiyskaya Gazeta official publication page: signed 20.12.2019; registered 06.02.2020 N 57449; published on official legal-information portal 07.02.2020; effective 18.02.2020; RG PDF 11.8 MB.

Primary/current distinction: original publication is confirmed, but no separately fetched current consolidated primary body was resolved: `PRIMARY_CURRENT_CONSOLIDATED_STATUS_BLOCKER`.

### Retention #3 — Приказ Росархива от 28.12.2021 N 142

Target: «Об утверждении Перечня типовых архивных документов, образующихся в научно-технической и производственной деятельности организаций, с указанием сроков хранения».

GitHub exact-body search: no target body found.

Derived hit:
- `repo=volk6022/enrollment-assistant`
- `commit=5f89a1d6e9b1d14031dcda2ce294ad4fe0a579ff`
- `path=data/npa/knowledge-base-full/_slices_full/mvd-170__head.txt`
- `size=UNRESOLVED_CONNECTOR_METADATA`
- `type=text/plain`
- `blob=UNRESOLVED_CONNECTOR_METADATA`

Internal check: the file is the head/general provisions of a different normative document (MVD N 170) and cites Rosarchiv N 142/N236 among archival-law sources. It is not the target body.

Classification: `MENTION_IN_DIFFERENT_NPA_BODY / REJECTED_AS_TARGET_BODY`.

GitHub full body: `GITHUB_FULL_TEXT_BLOCKER`.

Primary publication confirmed through Rossiyskaya Gazeta: signed 28.12.2021; registered 02.02.2022 N 67095; published on official legal-information portal 02.02.2022; effective 13.02.2022; RG PDF 15.6 MB.

Current consolidated primary body not separately resolved: `PRIMARY_CURRENT_CONSOLIDATED_STATUS_BLOCKER`.

### Retention #4 — Росархив N 1 / Банк России N 801-П от 12.07.2022

Target: «Об утверждении Перечня документов, образующихся в процессе деятельности кредитных организаций, с указанием сроков их хранения».

- GitHub exact number/title search: no full body or reliable candidate.
- GitHub metadata: `repo=null; commit=null; path=null; size=null; type=null`.
- Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Primary publication metadata confirmed by Rossiyskaya Gazeta: signed 12.07.2022, registered 19.07.2022 N 69304, published on official legal-information portal 19.07.2022, RG publication 20.07.2022, effective 30.07.2022, PDF 3.8 MB.

Metadata nuance/conflict: Habr and legal systems cite the act as `Положение Росархива N 1, Банка России N 801-П`, while the Rossiyskaya Gazeta publication page title renders it as `Приказ Федерального архивного агентства, Центрального банка Российской Федерации от 12.07.2022 № 1/801-П`. Date, combined number, title and Ministry of Justice registration all match, so this is recorded as `OFFICIAL_DISPLAY_TYPE_NOMENCLATURE_VARIANT`, not an identity conflict.

### Retention #5 — Приказ Росархива от 31.07.2023 N 77

Target: «Об утверждении Правил организации хранения, комплектования, учета и использования документов Архивного фонда Российской Федерации и других архивных документов в государственных органах, органах местного самоуправления и организациях».

GitHub derived hit:
- `repo=DmitriiKolesnikov/Econom_Fam_Bot_Tg`
- `commit=448de2f2286b9f3717f7a575c1b0915c1e8d11ea`
- `path=main.py`
- `size=UNRESOLVED_CONNECTOR_METADATA`
- `type=Python source`
- `blob=UNRESOLVED_CONNECTOR_METADATA`

Internal check: N 77 is embedded in a static list/prompt of «нормативные акты» inside application source code. The file is a Telegram-bot program, not a normative text.

Classification: `MENTION_ONLY_IN_SOURCE_CODE / REJECTED_AS_NORMATIVE_BODY`.

GitHub full body: `GITHUB_FULL_TEXT_BLOCKER`.

Primary publication confirmed by Rossiyskaya Gazeta: signed 31.07.2023; registered 06.09.2023 N 75119; published on official legal-information portal 06.09.2023; RG publication 07.09.2023; effective 17.09.2023; PDF 6.0 MB.

No amending act was confirmed in this pass; current consolidated primary body remains a separate gate: `PRIMARY_CURRENT_CONSOLIDATED_STATUS_BLOCKER`.

### Retention #6 — Приказ Роспатента от 23.10.2025 N 111

Target: «Об утверждении Перечня документов, образующихся в деятельности Федеральной службы по интеллектуальной собственности и ее подведомственных организаций, с указанием сроков хранения».

- GitHub exact title/number search: no full body or reliable candidate.
- GitHub metadata: `repo=null; commit=null; path=null; size=null; type=null`.
- Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Secondary full reproductions consistently confirm date, number, title and complete list structure. Unlike Rosarchiv N236/N142/N77, the Habr entry does not state Ministry of Justice registration, and current secondary listings likewise do not expose a registration number in the citation header.

Status rule: do not infer `REGISTERED_NPA` or official publication merely because the full text exists in Consultant/RuLaws. Direct Rospatent primary original and legal-status basis were not resolved in this pass: `PRIMARY_ROSPATENT_ORIGINAL_AND_STATUS_BLOCKER`.

### Retention #7 — Приказ Росавиации от 06.11.2025 N 848-П

Target: «Об утверждении Перечня документов, образующихся в процессе деятельности Федерального агентства воздушного транспорта, его территориальных органов и подведомственных организаций, с указанием сроков их хранения».

- GitHub exact title/number search: no full body or reliable candidate.
- GitHub metadata: `repo=null; commit=null; path=null; size=null; type=null`.
- Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Secondary reproductions confirm date, number, title and full list structure. Habr does not state Ministry of Justice registration for this order, and no registration/publication pointer was resolved in this pass.

Status rule: keep `AGENCY_ORDER` distinct from `REGISTERED_NPA` until a primary official status source is found. Blocker: `PRIMARY_ROSAVIATSIA_ORIGINAL_AND_STATUS_BLOCKER`.

## New counters for this pass

- `GITHUB_FULL_TEXT_CURRENT +0`
- `GITHUB_FULL_TEXT_OLD_EDITION +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +9` (two special-case targets + seven retention targets)
- `DERIVED_OR_MENTION_REJECTED +5 target-hits` (03-33/пс x2 paths, N236 session log, N142 mention in another NPA, N77 source-code mention)
- `DERIVED_BYTE_DUPLICATE_CONFIRMED +1 pair`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `OFFICIAL_DISPLAY_TYPE_NOMENCLATURE_VARIANT +1` (N1/801-P)
- `REGIONAL_NON_CORE +1`
- `NON_NPA_EXPLANATORY_LETTER +1`
- `PRIMARY_ORIGINAL/CURRENT_STATUS_BLOCKERS`: unresolved as noted per record; no official status was inferred from GitHub or secondary copies.

## Primary-source URLs used for publication verification

- Habr source list: https://habr.com/ru/articles/432466/
- Rosarchiv N236 (Rossiyskaya Gazeta): https://rg.ru/documents/2020/02/10/rosarhiv-prikaz236-site-dok.html
- Rosarchiv N142 (Rossiyskaya Gazeta): https://rg.ru/documents/2022/02/03/rosarhiv-prikaz142-site-dok.html
- Rosarchiv/Bank of Russia N1/801-P (Rossiyskaya Gazeta): https://rg.ru/documents/2022/07/20/prikaz1-801-site-dok.html
- Rosarchiv N77 (Rossiyskaya Gazeta): https://rg.ru/documents/2023/09/07/rosarhiv-prikaz77-site-dok.html

## Next boundary

The Habr retention subsection is now exhausted through item 7. `Персональные данные. Международные требования` is marked as a separate non-Russian-regulation layer. For the requested Russian PDn/information scope, the next systematic boundary is `Персональные данные. Примеры внутренних документов`, starting with the Roskomnadzor recommendations of 27.07.2017 and then the federal/agency acts in that subsection, with Roskomnadzor N201/2022 treated as a priority target.