# Habr NPA sweep — Stream 1 — 2026-09-02 18:54 MSK

## Scope

Continued Habr 432466 / user NPA sweep. This pass covers Bank of Russia NPS items 8–13:

1. Bank of Russia Regulation No. 742-P of 03.12.2020.
2. Bank of Russia Regulation No. 760-P of 25.06.2021.
3. Bank of Russia Methodological Recommendations No. 18-MR of 01.10.2021.
4. Bank of Russia Regulation No. 802-P of 25.07.2022.
5. Bank of Russia Regulation No. 821-P of 17.08.2023.
6. Bank of Russia Regulation No. 876-P of 03.12.2025.

GitHub copies are never treated as official merely because they are on GitHub. GitHub body identity/completeness and primary official/current status remain separate gates. No. 18-MR is explicitly kept as methodological/recommendatory material rather than silently classified as a normative legal act.

## GitHub findings

### 742-P

Exact number/date/title and broader subject searches did not produce a full normative body or reliable body candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### 760-P

Exact number/date/title and subject searches did not produce a full normative body or reliable body candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### 18-MR

Exact number/date/title searches did not produce a GitHub body or reliable candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER / METHODOLOGICAL_RECOMMENDATION`

### 802-P

A derived GitHub note was confirmed:

- repo: `ale88andr/obs-vault`
- commit/ref: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/Список НПА, в которых требуется использование СКЗИ.md`
- blob: `5eb397625c97c447afedda15f0e44976c40b2006`
- size: `47106` bytes
- type: Markdown/file

Internal identity check: the note contains the exact target number, date and title and links to the Bank of Russia source. It quotes only selected requirements (including paragraph 14.4) in a cross-sector list of acts requiring cryptographic protection. It is not the complete Regulation No. 802-P.

Classification:

`DERIVED_NPA_REQUIREMENTS_NOTE / PARTIAL_CITATION / OFFICIAL_POINTER / BIBLIOGRAPHIC_IDENTITY_PASS / REJECTED_AS_NORMATIVE_BODY`

No full GitHub normative body was found.

### 821-P

A second derived GitHub reference was confirmed:

- repo: `CyberOrda/cyberorda.github.io`
- commit/ref: `28e50740c537aa93691761e8fe0d7532416b737f`
- path: `docs/standards.md`
- blob: `4362378582a25c5f9f9702c55355254ab2b35892`
- size: `19136` bytes
- type: Markdown/file

The row contains `821-P` and the full target title with a secondary legal-system link. The date and normative body are absent. This is a standards/NPA reference table, not the Regulation itself.

Classification:

`NPA_REFERENCE_TABLE / SUMMARY_ONLY / NUMBER_TITLE_IDENTITY_PASS_DATE_ABSENT / REJECTED_AS_NORMATIVE_BODY`

No full GitHub normative body was found.

### 876-P

Exact number/date/title searches did not produce a GitHub body or reliable candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

## Primary official / current-status checks

### 742-P — primary-site metadata conflict resolved

The exact official body in `Вестник Банка России` No. 5 (2245), 03.02.2021 confirms:

- 03.12.2020 No. 742-P;
- exact target title;
- Ministry of Justice registration dated 18.01.2021;
- registration No. `62124`.

Primary source:
https://www.cbr.ru/Queries/XsltBlock/File/105012/-1/2245

However, the Bank of Russia's current financial-platform navigator/acts page displays immediately with the 742-P card the metadata `Регистрация в Минюсте России № 62210 от 25.01.2021. Официально опубликовано 05.02.2021`. That is inconsistent with the exact official body and is treated as a page-rendering/association defect rather than a second identity for 742-P.

Navigator source:
https://www.cbr.ru/admissionfinmarket/navigator/ofp/acts/

Resolution:

- authoritative identity gate: `62124 / 18.01.2021` from the exact official body;
- `CBR_NAVIGATOR_REGISTRATION_METADATA_MISASSOCIATION`;
- `PRIMARY_SITE_INTERNAL_METADATA_CONFLICT_RESOLVED_IN_FAVOR_OF_EXACT_BODY`.

Bank of Russia statistical/current materials continue to cite 742-P as the regulatory basis for financial-platform operators, providing current operational-reference evidence. This is not silently collapsed into a formal no-repeal flag.

Classification:

- `PRIMARY_ORIGINAL_BODY_CONFIRMED`
- `PRIMARY_CURRENT_OPERATIONAL_REFERENCE_CONFIRMED`
- `FORMAL_CURRENT_STATUS_FLAG_BLOCKER`

### 760-P — Habr stale: repealed

The primary Bank of Russia text of Instruction No. 6950-U of 22.11.2024, registered by the Ministry of Justice on 24.02.2025 under No. 81359, establishes a new procedure for observation in the national payment system.

Paragraph 13 states that No. 6950-U enters into force after 10 days following official publication; the official footnote states publication on 28.02.2025. Paragraph 14 expressly repeals Regulation No. 760-P from the date No. 6950-U enters into force. Therefore No. 760-P ceased to be current on 11.03.2025.

Primary source:
https://www.cbr.ru/Queries/XsltBlock/File/105253?fileId=-1&scope=ves250305_014(2545).pdf

Classification:

- `PRIMARY_REPEAL_CONFIRMED`
- `HABR_STALE_REPEALED_BANK_ACT`
- `REPEALED_BY_6950-U`
- `REPEAL_EFFECTIVE_2025-03-11`
- `DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`

### 18-MR — primary body confirmed, but not an NPA

The Bank of Russia primary text confirms exact identity:

- 01.10.2021 No. 18-MR;
- `Методические рекомендации по повышению качества оказания услуг по переводу денежных средств операторами электронных денежных средств`;
- expressly issued as `Методические рекомендации` under part 5 of article 31 of Federal Law No. 161-FZ.

Primary source:
https://cbr.ru/Crosscut/LawActs/File/5728

Classification:

- `PRIMARY_ORIGINAL_BODY_CONFIRMED`
- `METHODOLOGICAL_RECOMMENDATION`
- `NON_NPA_GUIDANCE`
- `CURRENT_APPLICABILITY_OR_SUPERSESSION_BLOCKER`

No later primary supersession was resolved in this pass; absence of a hit is not treated as proof that guidance remains current.

### 802-P — signed future amendment, do not merge early

Bank of Russia's legal-acts page confirms the original identity and publication of 802-P: Ministry of Justice No. 71124 dated 25.11.2022, officially published 29.11.2022.

Primary source:
https://cbr.ru/na/?la.Search=802-%D0%9F

A later primary official act is already signed and published: Instruction No. 7271-U of 12.01.2026, Ministry of Justice No. 86871 dated 02.06.2026, amending 802-P. Its own entry-into-force clause states `1 October 2026`; it was officially published by the Bank of Russia on 10.06.2026.

Primary amendment source:
https://www.cbr.ru/Queries/XsltBlock/File/131643/-1/2608

As of 02.09.2026, this amendment is not yet effective.

Classification:

- `PRIMARY_TARGET_IDENTITY_CONFIRMED`
- `PRIMARY_AMENDMENT_7271-U_CONFIRMED`
- `SIGNED_FUTURE_LAYER_7271-U`
- `EFFECTIVE_2026-10-01`
- `DO_NOT_MERGE_BEFORE_EFFECTIVE_DATE`

### 821-P — signed future amendment, do not merge early

Bank of Russia's legal-acts page confirms original identity: Ministry of Justice No. 76286 dated 06.12.2023, officially published 13.12.2023.

Primary source:
https://cbr.ru/na/?la.Search=821-%D0%9F

Instruction No. 7220-U of 28.10.2025 directly amends 821-P. The primary official body confirms Ministry of Justice No. 85263 dated 06.02.2026 and expressly states entry into force on `1 October 2026`; official Bank of Russia publication was 17.02.2026.

Primary amendment source:
https://www.cbr.ru/Queries/XsltBlock/File/105012/-1/2595

As of 02.09.2026 the amendment remains a future signed layer.

Classification:

- `PRIMARY_TARGET_IDENTITY_CONFIRMED`
- `PRIMARY_AMENDMENT_7220-U_CONFIRMED`
- `SIGNED_FUTURE_LAYER_7220-U`
- `EFFECTIVE_2026-10-01`
- `DO_NOT_MERGE_BEFORE_EFFECTIVE_DATE`

### 876-P — current edition advanced after Habr; mixed effective-date layers

The primary Bank of Russia official publication confirms:

- 03.12.2025 No. 876-P;
- exact title `О платежной системе Банка России`;
- Ministry of Justice registration No. 86527 dated 20.05.2026;
- publication in `Вестник Банка России` No. 17 (2606), 04.06.2026.

Primary original source:
https://www.cbr.ru/Queries/XsltBlock/File/185926/-1/2606

Bank of Russia's official-publication register confirms Instruction No. 7374-U of 23.06.2026 amending 876-P, Ministry of Justice No. 87572 dated 23.07.2026, officially published 30.07.2026.

Primary publication source:
https://cbr.ru/analytics/na_vr/

The exact entry-into-force clause reproduced in current full-text legal systems states that the main amendment enters into force after 10 days following official publication, while paragraphs 2–7 of subparagraph 1.3 enter into force on 01.10.2026. With official publication on 30.07.2026, the main amendment layer became effective on 10.08.2026; the specified sublayer remains future as of this pass.

Secondary text used only for the entry-into-force clause (not as the official source):
https://www.consultant.ru/document/cons_doc_LAW_540688/

The original 876-P itself also contains delayed effective dates for some provisions, including 01.10.2026 and 22.11.2027. These must remain separately versioned rather than flattened into a single `effective=true` document.

Classification:

- `PRIMARY_ORIGINAL_BODY_CONFIRMED`
- `PRIMARY_AMENDING_ACT_PUBLICATION_CONFIRMED`
- `CURRENT_EDITION_ADVANCED_876P_2026-06-23`
- `MAIN_AMENDMENT_EFFECTIVE_2026-08-10`
- `PARTIAL_SIGNED_FUTURE_SUBLAYER_EFFECTIVE_2026-10-01`
- `ORIGINAL_DOCUMENT_DELAYED_EFFECTIVE_SUBLAYERS_PRESENT`

## Delta counters

- `GITHUB_FULL_TEXT_CURRENT +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `GITHUB_DERIVED_OR_SUMMARY_REJECTED +2 target-hits`
- `PRIMARY_SITE_INTERNAL_METADATA_CONFLICT +1` (742-P navigator registration metadata)
- `PRIMARY_REPEAL_CONFIRMED +1` (6950-U -> 760-P)
- `HABR_STALE_REPEALED_BANK_ACT +1`
- `PRIMARY_AMENDMENT_CONFIRMED +3` (7271-U -> 802-P; 7220-U -> 821-P; 7374-U -> 876-P)
- `SIGNED_FUTURE_LAYER +2` (802-P, 821-P)
- `CURRENT_EDITION_ADVANCED +1` (876-P)
- `PARTIAL_FUTURE_SUBLAYER +1` (7374-U / 876-P)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Blockers

1. No full GitHub normative body was found for any of the six targets; the only GitHub hits accepted for tracking are derived references for 802-P and 821-P.
2. Formal current-status/no-repeal flag for 742-P remains separate from current operational references.
3. Current applicability/supersession of methodological recommendation 18-MR was not formally resolved; it remains guidance, not a normative act.
4. For 876-P, effective state is multi-layered: main 7374-U changes are already effective, while designated amendment clauses and designated clauses of the original 876-P have future dates. A single flat `current=true` representation would be legally lossy.

## Next boundary

Habr section `Банковская безопасность. Нормативно-правовые акты Банка России`:

`311-P -> 197-T -> 36-T -> 11-T -> 120-T -> 128-T`.

Letters/informational documents (`*-T`) must be classified by their actual legal nature rather than silently loaded as normative acts.
