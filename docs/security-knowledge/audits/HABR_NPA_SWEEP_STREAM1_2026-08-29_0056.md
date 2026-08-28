# Habr NPA sweep — Stream 1 — 2026-08-29 00:56 MSK

## Delta

- `FULL_TEXT`: +1
- `FORMAT_SIBLING_CANDIDATE`: +1
- `EXACT_DUPLICATE`: +0
- `LEGAL_IDENTITY_CONFLICT`: +0
- `PRIMARY_CURRENT_LIFECYCLE_BLOCKER`: +1

## PP RF 21.03.2012 No. 211

Target: Постановление Правительства РФ от 21.03.2012 N 211 «Об утверждении перечня мер, направленных на обеспечение выполнения обязанностей, предусмотренных Федеральным законом “О персональных данных” и принятыми в соответствии с ним нормативными правовыми актами, операторами, являющимися государственными или муниципальными органами».

Habr 432466: раздел «Персональные данные. Обеспечение безопасности», позиция 2.

### Confirmed GitHub full text

- repo: `VictorKVS/gpt-agent`
- commit: `ef8b02c1e0e997e028efc1dd2f3d30dc7e1cdce8`
- path: `дОКУМЕНТЫ ЗАГРУЖАЕМЫЕ В АГЕНТ/ПП Р Ф 2103 2012 г  N  211 Об утверждении перечня мер/Постановление Правительства РФ от 21 марта 2012 г. N 211 Об утверждении перечня мер .txt`
- size: `16085` bytes
- type: `TXT/blob`
- blob SHA: `e35cb53ce9a8995306eb99206b0759c8c19b6d79`

Body-level identity checks passed:

- type: Постановление Правительства РФ;
- date: 21 марта 2012 г.;
- number: N 211;
- title: exact target title;
- operative body contains the approval clause;
- signature block: Председатель Правительства Российской Федерации В. Путин;
- approved attachment «Перечень мер…» is present;
- attachment reaches пункт 2, i.e. the normative package is not merely a card, mention, or summary.

The GitHub text is a GARANT export and explicitly contains the amendment chain `20.07.2013`, `06.09.2014`, `15.04.2019`; export footer date `22.11.2024` is not treated as a consolidation/revision date.

Classification: `FULL_TEXT / CONSOLIDATED_GARANT_EXPORT / NON_OFFICIAL_GITHUB_COPY / REVISION_THROUGH_15.04.2019 / CURRENT_STATUS_PRIMARY_RECHECK_PENDING`.

### Format sibling

Same directory contains PDF:

- path: `дОКУМЕНТЫ ЗАГРУЖАЕМЫЕ В АГЕНТ/ПП Р Ф 2103 2012 г  N  211 Об утверждении перечня мер/Постановление Правительства РФ от 21 марта 2012 г N 211 Об утверждении перечня м (1).pdf`
- size: `94885` bytes
- type: `PDF/blob`
- blob SHA: `61214187c156b729ae6bf69b51ce72870ebb3cbf`

Binary body was not independently inspected in this pass, therefore it is `FORMAT_SIBLING_CANDIDATE`, not an exact duplicate and not independently promoted to `FULL_TEXT`.

### Official / lifecycle verification

Primary official publication of the original act is independently confirmed by «Российская газета»: signed 21.03.2012, published 29.03.2012, title and normative body match the GitHub candidate. Primary official publication also confirms amendments of 20.07.2013 No. 607 and 06.09.2014 No. 911.

The GitHub body contains the later amendment of 15.04.2019 No. 454 and third-party current legal indexes likewise show the act in revision of 15.04.2019. However, in this pass a stable primary official lifecycle/card proving that no later amendment/repeal occurred through 2026-08-29 was not resolved. Therefore do not mark the GitHub copy `OFFICIAL` or `VERIFIED_CURRENT` yet.

Blocker: `PRIMARY_OFFICIAL_CURRENT_LIFECYCLE: PP-211/2012`.

## Gate update

`EXPORT_FOOTER_DATE != REVISION_DATE` and `FULL_TEXT + MATCHING_AMENDMENT_CHAIN != VERIFIED_CURRENT` until the latest lifecycle is checked against a primary official source.
