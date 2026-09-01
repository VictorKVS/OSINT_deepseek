# Habr NPA sweep — Stream 1 — 2026-09-02 02:52 MSK

## Scope

Continuation of the systematic pass over Habr article 432466 (current article version marked 28.05.2026) and the user NPA list. This pass covers **PDn positions 15–22**:

15. Постановление Правительства РФ от 16.01.2023 № 24.
16. Постановление Правительства РФ от 24.04.2025 № 538.
17. Постановление Правительства РФ от 22.05.2025 № 702.
18. Постановление Правительства РФ от 28.05.2025 № 740.
19. Постановление Правительства РФ от 26.06.2025 № 961.
20. Постановление Правительства РФ от 26.06.2025 № 966.
21. Постановление Правительства РФ от 04.07.2025 № 1012.
22. Постановление Правительства РФ от 01.08.2025 № 1154.

Source list: https://habr.com/ru/articles/432466/

Rules applied: GitHub copy is never treated as an official source; body identity is checked separately from legal/current status; mention/summary/reference files are rejected as normative bodies; full text must include all approved Rules/Requirements/annexes necessary to reconstruct the act.

## Results

| Habr pos | Target | GitHub body result | GitHub metadata | Body identity | Official/current verification | Classification / blocker |
|---:|---|---|---|---|---|---|
| 15 | ПП РФ 16.01.2023 №24 | No full body or reliable candidate found | `repo=null; commit=null; path=null; size=null; type=null` | No candidate to validate | Base act confirmed; current consolidated layer is not the original 2023 text: ПП РФ 14.10.2024 №1371 amended subpara. `в` of para. 23 (word `неправительственных` removed). Original publication pointer independently found as `0001202301170011`, publication date 17.01.2023, 12 pages, but direct primary portal fetch not resolved in this pass. | `GITHUB_FULL_TEXT_BLOCKER`; `CURRENT_EDITION_ADVANCED_2024-10-14`; `PRIMARY_PUBLICATION_DIRECT_FETCH_BLOCKER` |
| 16 | ПП РФ 24.04.2025 №538 | No full body or reliable candidate found | `repo=null; commit=null; path=null; size=null; type=null` | No candidate to validate | **Primary publication index confirmed**: `0001202504250043`, published 25.04.2025, PDF 1214 KB / 5 pp. Secondary current-text sources confirm entry into force 01.09.2025. No later amendment confirmed in this pass. | `GITHUB_FULL_TEXT_BLOCKER`; `PRIMARY_PUBLICATION_POINTER_CONFIRMED`; `CURRENT_STATUS_PRIMARY_CONSOLIDATED_BLOCKER` |
| 17 | ПП РФ 22.05.2025 №702 | No full body or reliable candidate found | `repo=null; commit=null; path=null; size=null; type=null` | No candidate to validate | **Primary Government source confirmed**: https://government.ru/docs/all/159151/ . Government page reproduces the decree and full Rules; clause 2: enters into force 01.09.2025. Publication pointer candidate `0001202505280017` found separately, but direct publication portal fetch timed out. | `GITHUB_FULL_TEXT_BLOCKER`; `PRIMARY_GOVERNMENT_BODY_CONFIRMED`; `PUBLICATION_PORTAL_DIRECT_FETCH_BLOCKER` |
| 18 | ПП РФ 28.05.2025 №740 | No full body or reliable candidate found | `repo=null; commit=null; path=null; size=null; type=null` | No candidate to validate | Exact number/date/title and complete secondary text confirmed. Clause 4 establishes split commencement: the main act from 01.09.2025, while point 3 entered into force on signature. Direct Government/publication primary page was not resolved in this pass. | `GITHUB_FULL_TEXT_BLOCKER`; `SPLIT_EFFECTIVE_DATE_CONFIRMED_SECONDARY`; `PRIMARY_ORIGINAL_DIRECT_FETCH_BLOCKER` |
| 19 | ПП РФ 26.06.2025 №961 | No full body or reliable candidate found | `repo=null; commit=null; path=null; size=null; type=null` | No candidate to validate | Exact title/body structure confirmed (Rules for formation + Rules for access); effective 01.09.2025. Publication pointer found as `0001202506270025`, publication date 27.06.2025, but direct official portal fetch timed out. | `GITHUB_FULL_TEXT_BLOCKER`; `PUBLICATION_POINTER_FOUND_SECONDARY`; `PRIMARY_PUBLICATION_DIRECT_FETCH_BLOCKER` |
| 20 | ПП РФ 26.06.2025 №966 | No full body or reliable candidate found | `repo=null; commit=null; path=null; size=null; type=null` | No candidate to validate | Current secondary consolidated source marks original edition 26.06.2025, status active, effective 01.09.2025. Publication pointer found as `0001202506260044`, publication date 26.06.2025; direct official portal fetch timed out. | `GITHUB_FULL_TEXT_BLOCKER`; `PUBLICATION_POINTER_FOUND_SECONDARY`; `PRIMARY_PUBLICATION_DIRECT_FETCH_BLOCKER` |
| 21 | ПП РФ 04.07.2025 №1012 | No full body or reliable candidate found | `repo=null; commit=null; path=null; size=null; type=null` | No candidate to validate | Exact decree + approved electronic-storage format + digital-photo requirements confirmed in complete secondary text. Clause 4: decree generally enters into force on official publication, but **point 1 enters into force 01.01.2026**. Direct primary publication/Government page not resolved in this pass. | `GITHUB_FULL_TEXT_BLOCKER`; `SPLIT_EFFECTIVE_DATE_CONFIRMED_SECONDARY`; `PRIMARY_ORIGINAL_DIRECT_FETCH_BLOCKER` |
| 22 | ПП РФ 01.08.2025 №1154 | No normative body. One derived reference found and rejected. | `repo=arterm-sedov/cmw-rag; commit=3b5d4e92d7db6d85d5e70ce8264853724a7f4be0; path=docs/research/executive-research-technology-transfer/tasks/20260324-research-task.md; size=63162 B; type=Markdown; blob=3a4b1259e30eb878e8f2bf0fc3e1d8131b523cda` | File itself identifies as a research task/instruction and only contains №1154 in a source/reference list; it is not the decree, Requirements, Methods or Rules. | **Primary publication index confirmed**: `0001202508050011`, published 05.08.2025, PDF 2619 KB / 12 pp. Secondary current sources confirm effective 01.09.2025 and active status. Direct document-card fetch timed out. | `MENTION_ONLY / RESEARCH_TASK_SOURCE_LIST / REJECTED_AS_NORMATIVE_BODY`; `GITHUB_FULL_TEXT_BLOCKER`; `PRIMARY_PUBLICATION_POINTER_CONFIRMED`; `PRIMARY_DOCUMENT_DIRECT_FETCH_BLOCKER` |

## GitHub search disposition

Exact number/date/title and distinctive-body searches were run for all eight targets. No GitHub object in this batch qualifies as `FULL_TEXT` or `RELIABLE_GITHUB_CANDIDATE`.

The only reportable GitHub hit is the №1154 reference in `arterm-sedov/cmw-rag`. Metadata was independently resolved through the GitHub Contents API: **63162 bytes**, Markdown file, blob `3a4b1259e30eb878e8f2bf0fc3e1d8131b523cda`. Fetching the file shows the document begins as `# Задача: Ревалидация и расширение отчётов для руководства`, so it is definitively a research-work instruction, not an NPA body.

## New lifecycle / conflict findings

1. **PP №24 current layer advanced**: a GitHub copy of only the original 2023 body, if found later, must not be tagged current without the amendment by PP №1371 of 14.10.2024.
2. **Coordinated Article 13.1 layer**: PP №538, №702, №740, №961, №966 and №1154 are all part of the 2025 anonymised-personal-data / Article 13.1 implementation layer and are operational from **01.09.2025** (№740 has an earlier effective point 3). This should be represented as a linked regime, not six unrelated flat records.
3. **PP №1012 has split commencement**: metadata must not flatten it to a single effective date; the decree generally operates from official publication, while point 1 starts on **01.01.2026**.
4. No Habr duplicate, GitHub full-body byte duplicate, or body identity conflict was confirmed in this batch.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +8`
- `GITHUB_MENTION_ONLY_REJECTED +1`
- `PRIMARY_PUBLICATION_POINTER_CONFIRMED +2` (№538, №1154 directly from official publication index)
- `PRIMARY_GOVERNMENT_BODY_CONFIRMED +1` (№702)
- `CURRENT_EDITION_ADVANCED +1` (№24 -> amendment №1371/2024)
- `SPLIT_EFFECTIVE_DATE +2` (№740, №1012)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_EXACT_DUPLICATE +0`

## Primary-source blockers retained

Direct `publication.pravo.gov.ru/document/...` fetches repeatedly timed out for known pointers in this pass. A pointer discovered in a secondary index is therefore stored as `FOUND_SECONDARY` and is **not** promoted to `PRIMARY_DIRECT_FETCH_CONFIRMED`. Official-index results for №538 and №1154 are stored separately as primary publication evidence. The Government page for №702 is stored as a primary issuing-government body source.

## Next boundary

PDn positions 23–24 are Supreme Court Plenum materials; after them the Habr PDn section enters the **Roskomnadzor** layer starting with order №482/2010 and related acts. For Stream 1 priority, subsequent processing should deduplicate any already-covered general PDn acts and then continue Roskomnadzor / general information-law materials.