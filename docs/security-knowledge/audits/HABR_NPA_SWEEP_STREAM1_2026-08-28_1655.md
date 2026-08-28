# Habr NPA sweep — Stream 1 — 2026-08-28 16:55 MSK

## Delta

- New confirmed standalone FULL_TEXT: **1**.
- New exact-duplicate sets: **0**.
- New identity conflicts: **0**.
- New search false-positive checked: **1** (an apparent second hit for Decree No. 609 is actually MChS Order No. 626/2019, not a duplicate of the target act).

## 1. Presidential Decree of 30.05.2005 No. 609 — personal data of state civil servants

Target: `Указ Президента РФ от 30.05.2005 N 609 «Об утверждении Положения о персональных данных государственного гражданского служащего Российской Федерации и ведении его личного дела»` from the PD section of Habr 432466.

### GitHub source

- repo: `buba1477/multik_bot`
- commit/ref: `e8e0c46feb0d4a7feadafc934920825bed808f7d`
- path: `embendings/Об утверждении Положения о персональных данных.md`
- size: `36246` bytes
- type: `Markdown/blob`
- blob SHA: `4c8b1c63d5cb93a4b22dafa04ebf2a63317b1706`

### Body identity / completeness check

The body independently states:

- `Указ Президента Российской Федерации от 30.05.2005 г. № 609`;
- the exact title of the act;
- Moscow/Kremlin, 30 May 2005, No. 609 and President V. Putin;
- operative clauses 1–5 of the parent decree;
- the approved `ПОЛОЖЕНИЕ о персональных данных государственного гражданского служащего Российской Федерации и ведении его личного дела`;
- substantive clauses of the Regulation through clause 23, including amendments and repeal markers.

The file is therefore a consolidated normative body, not a card, TOC, mention, summary or detached appendix.

The header says `По состоянию на 09.04.2026 г.` and lists amendments through Presidential Decree of 31.12.2025 No. 1009. The body actually incorporates that amendment: clauses 12–15 are marked repealed by No. 1009 and the changes to clauses 16 and 19 are present.

### Official/currentness check

Official government sources independently confirm the base identity of Decree No. 609. More importantly, the official Kremlin text of Presidential Decree of 31.12.2025 No. 1009 directly identifies Decree No. 609 and amends its approved Regulation, including repeal of clauses 12–15 and amendments to clauses 16 and 19.

Official publication of Decree No. 1009: `0001202601010001`, publication date `01.01.2026`.

A current legal-reference check during this sweep exposes Decree No. 609 as amended through `31.12.2025 No. 1009`; no later amendment was established in this pass. This supports the GitHub revision as a **current candidate**, but the GitHub copy itself remains non-official.

**Classification**: `FULL_TEXT / CONSOLIDATED / NON_OFFICIAL_GITHUB_COPY / REVISION_THROUGH_31.12.2025_NO_1009 / CURRENT_CANDIDATE`.

## 2. False-positive / non-duplicate check

The second GitHub search hit returned as a possible match was:

- repo: `ispras/dedoc`
- commit/ref: `40dde1bc2e46b1b00b7058080c1228615b983424`
- path: `tests/data/txt/17 (1).txt`
- size: `281145` bytes
- type: `TXT/blob`
- blob SHA: `ede513eaf3b55f3bc3755617ae269071ceedb191`

Its body is **MChS Russia Order of 31.10.2019 No. 626**, `Об обработке и обеспечении защиты персональных данных в МЧС России`, with its own appendices. It is not Decree No. 609 and is not a duplicate of the new target find. It is classified for this target search as `SEARCH_FALSE_POSITIVE / DIFFERENT_ACT / CROSS_REFERENCE_CONTEXT`.

## Regression gate added

`SEARCH_TITLE_HIT != TARGET_IDENTITY`: even a highly ranked exact-title search hit must pass body-level `act type + authority + date + number + title` identity before duplicate analysis. A cross-reference to a target act inside another normative document is not a target copy.
