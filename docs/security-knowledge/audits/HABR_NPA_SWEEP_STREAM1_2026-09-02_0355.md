# Habr NPA sweep — Stream 1 — 2026-09-02 03:55 MSK

Scope: Habr 432466, section «Персональные данные», positions 23–29 and 31. Position 30 (Bank of Russia 499-P) is sector-specific banking material and is deferred in this stream, whose priority is federal / Presidential / Government / Roskomnadzor / common PDn-information layer.

Principle: GitHub copies are discovery/corpus candidates only. Official status and currency are checked separately. A mention, bibliography item, lecture note, court decision, research/academic text, or practical summary is not promoted to FULL_TEXT.

## Results

| Habr pos | Target | GitHub repo | Commit | Path | Size | Type | GitHub classification | Identity / official-status result | Blocker |
|---:|---|---|---|---|---:|---|---|---|---|
| 23 | Plenum VS RF 15.06.2010 N 16 | py-tenz/ru_court_analylics | 4a79fce9a552d97c171a2802795f7e80dcca4e5f | legal_parser/documents/doc_36.txt; legal_parser/documents/doc_52.txt | 26,518 B each | text/plain | MENTION_ONLY / COURT_DECISION / REJECTED_AS_NORMATIVE_BODY | Both paths are the same blob `0cd064df88290f3df349d7406b37ee35e3e7d94b`. The document cites N16 but is not the Plenum body. Official VS body confirms N16/date/title. Official Plenum N21 of 16.09.2010 amended N16 by adding pts 37–38, so an original-only 15.06.2010 copy is not the complete current body. | GITHUB_FULL_TEXT_BLOCKER |
| 24 | Plenum VS RF 23.06.2015 N 25 | iis-research-team/summarization-dataset | f5643191986836fc9bdf7f2e332b8b580cc936fe | dataset/law/law_42/text.txt | 22,171 B | text/plain | MENTION_ONLY / ACADEMIC_LEGAL_ARTICLE / REJECTED_AS_NORMATIVE_BODY | Blob `7738435e01a3d783a552e542ac80465404830a4d`; the file discusses legal doctrine and cites N25, not the Plenum body. Exact number/date/title are confirmed by the official Supreme Court index. No later amendment/repeal was confirmed in this pass. | GITHUB_FULL_TEXT_BLOCKER; CURRENT_STATUS_RECHECK_GATE |
| 25 | Roskomnadzor Order 16.07.2010 N 482 | — | — | — | — | — | NO_RELIABLE_GITHUB_BODY_FOUND | Habr's substantive description is stale: Roskomnadzor Order N706 of 19.08.2011 expressly invalidated pts 1–2 of N482; the notification form and recommendations in annexes lost force. Whole-act formal repeal was not established in this pass. | GITHUB_FULL_TEXT_BLOCKER; PRIMARY_RKN_ORIGINAL_DIRECT_FETCH_BLOCKER |
| 26 | Mincomsvyaz Letter 07.07.2017 N P11-15054-OG | blondinkaizakon/HSE_Oksana_Petrovskaya | cbb2ac84cda1974042505a534833b1d196181cbc | VKR/rag-system/documents/infobez/персональные данные.md; VKR/rag-system/documents/knowledge_base/infobez/персональные данные.md | 281,808 B each | Markdown | MENTION_ONLY / PRACTICAL_LEGAL_GUIDANCE / REJECTED_AS_NORMATIVE_BODY | Both paths are the same blob `1f096344693a8055cb27ea96e4a08b294adfdc7b`. The file is practical guidance and only cites the letter for the phone/e-mail interpretation. The letter is explanatory/non-NPA; primary ministry original was not resolved. | GITHUB_FULL_TEXT_BLOCKER; PRIMARY_MINISTRY_ORIGINAL_BLOCKER |
| 27 | Roskomnadzor Order 24.02.2021 N 18 | IKarasev/Study | 46d89cc6ac468698dcc56c9706f744749ed84b8d | norm_obespechenie/03 Комплаенс.md | 211,863 B | Markdown | KNOWN_DERIVED_FILE_NEW_TARGET_MENTION / EDUCATIONAL_NOTES / REJECTED_AS_NORMATIVE_BODY | Blob `fcb692651c552161d4861ae56436576507a63189`. Exact order identity: Minjust N63204; effective 01.09.2021; the order itself contains a sunset through 01.09.2027. | GITHUB_FULL_TEXT_BLOCKER; PRIMARY_PUBLICATION_DIRECT_FETCH_BLOCKER |
| 28 | Mincifry Order 29.09.2021 N 1015 | — | — | — | — | — | NO_RELIABLE_GITHUB_BODY_FOUND | Exact number/date/title and Minjust registration N66042 are confirmed; publication/effect layer is 29.11.2021 / 10.12.2021 in current legal references. No primary ministry/original card was resolved in this pass. | GITHUB_FULL_TEXT_BLOCKER; PRIMARY_CURRENT_STATUS_BLOCKER |
| 29 | Roskomnadzor Order 21.06.2021 N 106 | — | — | — | — | — | NO_RELIABLE_GITHUB_BODY_FOUND | Exact number/date/title and Minjust N64602 confirmed. The order itself specifies effect from 01.03.2022 through 01.03.2028. | GITHUB_FULL_TEXT_BLOCKER; PRIMARY_PUBLICATION_DIRECT_FETCH_BLOCKER |
| 31 | Roskomnadzor Clarifications 14.12.2012 on employees/applicants/personnel reserve | — | — | — | — | — | NO_RELIABLE_GITHUB_BODY_FOUND | The item is explanatory/methodical material, not a registered NPA. Secondary legal references confirm the title/content; primary RKN original was not resolved. | GITHUB_FULL_TEXT_BLOCKER; PRIMARY_RKN_ORIGINAL_BLOCKER; CURRENT_RELEVANCE_BLOCKER |

## New findings / conflicts / duplicates

- `CURRENT_EDITION_ADVANCED_N16_2010-09-16 +1`: official Plenum N21 amended N16 by adding pts 37–38. Full-current completeness therefore requires the N21 amendments.
- `HABR_STALE_SUBSTANTIVE_DESCRIPTION_N482 +1`: Habr still presents N482 as the notification-form + recommendations source, while points 1–2 and the corresponding annexed form/recommendations were invalidated by N706/2011.
- `GITHUB_DERIVED_BYTE_DUPLICATE +2`: (a) `doc_36.txt` and `doc_52.txt` in `py-tenz/ru_court_analylics` are identical blob `0cd064...`; (b) the two PDn guidance paths in `blondinkaizakon/HSE_Oksana_Petrovskaya` are identical blob `1f0963...`. These are duplicate derived/mention bodies, not duplicate normative bodies.
- `BUILT_IN_SUNSET_2027-09-01 +1`: Roskomnadzor N18.
- `BUILT_IN_SUNSET_2028-03-01 +1`: Roskomnadzor N106.
- `NON_NPA_EXPLANATORY_LAYER +2`: Mincomsvyaz letter P11-15054-OG and Roskomnadzor clarification 14.12.2012 are guidance/explanation, not binding registered NPAs.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +8`
- `GITHUB_MENTION_OR_DERIVED_REJECTED +4` (target-level)
- `GITHUB_DERIVED_BYTE_DUPLICATE +2`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_STALE_SUBSTANTIVE_DESCRIPTION +1`
- `CURRENT_EDITION_ADVANCED +1`
- `BUILT_IN_SUNSET +2`

## Next boundary

Continue Habr PDn positions 32–40, prioritizing current control/Roskomnadzor layer: Mincifry N1187/2021; Roskomnadzor N253/2021, N128/2022, N178/2022, N179/2022, letter 08-78032/2022, N180/2022, N187/2022, N140/2025. For each, keep the same GitHub identity/completeness gate and separate primary official status check.
