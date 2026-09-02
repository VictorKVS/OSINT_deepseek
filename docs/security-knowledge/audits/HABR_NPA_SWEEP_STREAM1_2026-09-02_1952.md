# Habr NPA sweep — Stream 1 — 2026-09-02 19:52 MSK

## Scope

Continued Habr 432466 / user NPA sweep. This pass covers the next Bank of Russia banking-security block:

1. Bank of Russia Regulation No. 311-P of 07.09.2007.
2. Bank of Russia Letter No. 197-T of 07.12.2007.
3. Bank of Russia Letter No. 36-T of 31.03.2008.
4. Bank of Russia Letter No. 11-T of 30.01.2009.
5. Bank of Russia Letter No. 120-T of 02.10.2009.
6. Bank of Russia Letter No. 128-T of 23.10.2009.

GitHub copies are never treated as official merely because they are on GitHub. GitHub body identity/completeness and primary official/current-status checks remain separate gates. The five `*-T` items are letters/recommendatory materials, not silently classified as normative legal acts.

## GitHub findings

### 311-P

Exact number/date/title and broader subject searches did not produce a full normative body or reliable GitHub body candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

### 197-T

Exact number/date/title and characteristic-text searches did not produce a full letter body or reliable candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER / CBR_LETTER_NON_NPA_GUIDANCE`

### 36-T

Exact number/date/title and characteristic-text searches did not produce a full letter body or reliable candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER / CBR_LETTER_NON_NPA_GUIDANCE`

### 11-T

Exact number/date/title and characteristic-text searches did not produce a full letter body or reliable candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER / CBR_LETTER_NON_NPA_GUIDANCE`

### 120-T

No GitHub copy passed the target identity gate. One thematically related educational file was confirmed and rejected as target body:

- repo: `katpavlova/financial_advisor`
- commit/ref: `60befa5f51afe7144208455933854fd530d3a880`
- path: `docs/cat3_educational/bank_cards.txt`
- blob: `e0d681f3fd71dbf50d4cec2453e209c60aab2185`
- size: `6818` bytes
- type: `text/plain`

The file is titled `БАНКОВСКИЕ КАРТЫ: ВИДЫ, ОТЛИЧИЯ И ПРАВИЛА ИСПОЛЬЗОВАНИЯ`, claims `Fincult.info — Финансовая культура, Банк России` as its source, and contains generic card-safety guidance. It does **not** contain target number `120-Т`, target date `02.10.2009`, or the target letter title. It is therefore not a copy or excerpt whose identity can be established as 120-T.

Classification:

`DERIVED_EDUCATIONAL_SUMMARY / THEMATIC_OVERLAP_ONLY / TARGET_IDENTITY_GATE_FAIL / REJECTED_AS_120-T_BODY`

The target remains `GITHUB_FULL_TEXT_BLOCKER`.

### 128-T

Exact number/date/title and characteristic-text searches did not produce a full GitHub body or reliable candidate.

- `repo/commit/path/size/type = null`
- classification: `GITHUB_FULL_TEXT_BLOCKER / CBR_LETTER_NON_NPA_GUIDANCE`

## Primary official / current-status checks

### 311-P — Habr stale: repealed from 01.01.2026

Bank of Russia's official 2007 Vestnik index confirms the original identity and publication of Regulation No. 311-P of 07.09.2007.

Primary original index:
https://www.cbr.ru/about_br/publ/vestnik-akts/?year=2007

Bank of Russia Instruction No. 7187-U of 29.09.2025 introduced the replacement electronic-reporting procedure. The official Bank of Russia publication states that No. 7187-U enters into force on `01.01.2026` and from that date Regulation No. 311-P and its amending acts are repealed.

Primary replacement publication:
https://cbr.ru/Queries/XsltBlock/File/170786/-1/2589

Classification:

- `PRIMARY_REPEAL_CONFIRMED`
- `HABR_STALE_REPEALED_BANK_ACT`
- `REPEALED_BY_7187-U`
- `REPEAL_EFFECTIVE_2026-01-01`
- `DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`

### 197-T — primary publication identity confirmed; letter/non-NPA layer

Bank of Russia's official 2007 Vestnik index confirms:

- No. `197-T`;
- date `07.12.2007`;
- title `О рисках при дистанционном банковском обслуживании`;
- publication in `Вестник Банка России` No. 68 (1012), 12.12.2007.

Primary source:
https://www.cbr.ru/about_br/publ/vestnik-akts/?year=2007

No later primary cancellation/supersession act was resolved in this pass. Absence of a search hit is not treated as proof of continuing applicability.

Classification:

- `PRIMARY_PUBLICATION_IDENTITY_CONFIRMED`
- `CBR_LETTER_NON_NPA_GUIDANCE`
- `PRIMARY_CURRENT_APPLICABILITY_OR_SUPERSESSION_BLOCKER`

### 36-T — primary publication identity confirmed; letter/recommendatory layer

Bank of Russia's official 2008 publication index confirms the letter dated 31.03.2008 and its title concerning recommendations for management of risks arising from Internet-banking operations. The Bank of Russia also published a contemporary notice identifying the same recommendations.

Primary index:
https://www.cbr.ru/about_br/publ/vestnik-akts/?year=2008

No later primary cancellation/supersession act was resolved in this pass.

Classification:

- `PRIMARY_PUBLICATION_IDENTITY_CONFIRMED`
- `CBR_LETTER_NON_NPA_GUIDANCE`
- `RECOMMENDATORY_MATERIAL`
- `PRIMARY_CURRENT_APPLICABILITY_OR_SUPERSESSION_BLOCKER`

### 11-T — secondary body confirmed, primary CBR original unresolved

No primary Bank of Russia body or publication card for the exact 30.01.2009 No. 11-T was resolved in this pass. The official 2009 Vestnik index does not expose this item in the retrieved publication list.

A secondary full-text legal reproduction passes the internal identity gate: it contains `ЦЕНТРАЛЬНЫЙ БАНК РОССИЙСКОЙ ФЕДЕРАЦИИ`, `ПИСЬМО`, date `30 января 2009 г.`, No. `11-Т`, and the exact title, followed by the recommendation body.

Secondary identity source only:
https://www.consultant.ru/document/cons_doc_LAW_100931/

Classification:

- `SECONDARY_FULL_TEXT_IDENTITY_CONFIRMED`
- `CBR_LETTER_NON_NPA_GUIDANCE`
- `PRIMARY_CBR_ORIGINAL_OR_PUBLICATION_BLOCKER`
- `DO_NOT_PROMOTE_SECONDARY_COPY_TO_OFFICIAL`

### 120-T — primary full body confirmed; GitHub thematic summary rejected

Bank of Russia hosts the exact letter and attachment as a primary PDF. The document itself contains:

- date `02.10.2009`;
- No. `120-Т`;
- title `О памятке “О мерах безопасного использования банковских карт”`;
- the attached full `ПАМЯТКА “О МЕРАХ БЕЗОПАСНОГО ИСПОЛЬЗОВАНИЯ БАНКОВСКИХ КАРТ”`.

Primary body:
https://www.cbr.ru/StaticHtml/File/17579/120-t.pdf

The current Bank of Russia site still exposes a card-holder safety page that explicitly points to the 120-T memo as an additional set of measures; that page was last updated 17.09.2021, so it is useful operational-reference evidence but not a 2026 formal no-cancellation certificate.

Operational reference:
https://www.cbr.ru/PSystem/field_offices/rekomendacii-derzhatelyam-platezhnykh-kart/

Classification:

- `PRIMARY_FULL_BODY_CONFIRMED_CBR`
- `CBR_LETTER_NON_NPA_GUIDANCE`
- `PRIMARY_OPERATIONAL_REFERENCE_CONFIRMED`
- `FORMAL_CURRENT_APPLICABILITY_OR_SUPERSESSION_BLOCKER`

### 128-T — Habr stale: cancellation is confirmed, not merely proposed

Bank of Russia's official 2009 Vestnik index confirms the original letter No. 128-T of 23.10.2009 and its title.

Primary original index:
https://www.cbr.ru/about_br/publ/vestnik-akts/?year=2009

A 2022 regulatory-review document had proposed cancelling 128-T, but that proposal is no longer the strongest lifecycle evidence. A later exact primary Bank of Russia document resolves the status conclusively: Information Letter No. `ИН-03-23/104` of `27.12.2021`, titled in part `...об отмене письма Банка России от 23.10.2009 № 128-Т`, states that **from the day the information letter is posted, Letter No. 128-T is cancelled**. The Bank of Russia acts page exposes the exact number/date of this cancelling information letter.

Primary cancelling body:
https://www.cbr.ru/Crosscut/LawActs/File/5773

Primary metadata/index:
https://www.cbr.ru/finm_infrastructure/oper/acts/

Classification:

- `PRIMARY_CANCELLATION_CONFIRMED`
- `HABR_STALE_CANCELLED_BANK_LETTER`
- `CANCELLED_BY_IN-03-23/104_2021-12-27`
- `DO_NOT_LOAD_AS_CURRENT_REQUIREMENT`

## Delta counters

- `GITHUB_FULL_TEXT_CURRENT +0`
- `RELIABLE_GITHUB_BODY_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `DERIVED_THEMATIC_SUMMARY_REJECTED +1`
- `CBR_LETTER_NON_NPA_GUIDANCE +5`
- `PRIMARY_FULL_BODY_CONFIRMED_CBR +1` (120-T)
- `PRIMARY_REPEAL_CONFIRMED +1` (311-P)
- `PRIMARY_CANCELLATION_CONFIRMED +1` (128-T)
- `HABR_STALE_REPEALED_OR_CANCELLED_BANK_ITEM +2` (311-P, 128-T)
- `PRIMARY_CBR_ORIGINAL_OR_PUBLICATION_BLOCKER +1` (11-T)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_BODY_IDENTITY_CONFLICT +0`

## Next boundary

Continue from Habr banking-security position 7: Bank of Russia Instruction No. 2346-U of 25.11.2009, followed by the next items in article order. Normative Bank of Russia instructions/regulations and non-NPA letters/recommendations must remain separated in the knowledge model.
