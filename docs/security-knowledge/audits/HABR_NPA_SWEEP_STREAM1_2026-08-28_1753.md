# Habr NPA sweep — Stream 1 — 2026-08-28 17:53 MSK

Delta only. GitHub copies are not treated as official sources automatically.

## New confirmed conflict — 258-ФЗ number collision

### Target identity — official source
- Federal Law: 31.07.2020 No. 258-FZ.
- Title at original publication: «Об экспериментальных правовых режимах в сфере цифровых инноваций в Российской Федерации».
- Official publication: No. 0001202007310024, 31.07.2020.
- Later official lifecycle event: Federal Law 31.07.2025 No. 336-FZ amends 258-FZ; official publication No. 0001202507310081, 31.07.2025. The current title is «Об экспериментальных правовых режимах в сфере цифровых и технологических инноваций в Российской Федерации».

### GitHub false-positive
- repo: `deep-foundation/russian-laws`
- commit: `3507a48f311e617c356adfbfdfb470d94a897f41`
- path: `data/html/102073578.html`
- blob: `51e22ef7d32eae3c4be948a4a546fb20b6fc86f3`
- size: `353295` bytes
- type: `HTML/blob`

Body-level identity check shows that this file is not Federal Law 258-FZ of 31.07.2020. It is a Civil Code Part III corpus item; the `258-ФЗ` occurrence refers to Federal Law of 29.12.2006 No. 258-FZ as an amending law. Therefore number equality alone created a false positive.

Classification: `SEARCH_FALSE_POSITIVE / NUMBER_COLLISION / DIFFERENT_ACT / WRONG_YEAR_2006_VS_2020 / REJECT_FOR_TARGET`.

## Blocker
An exact GitHub search combining the target title/date/number still returned reference hits embedded in 152-FZ/privacy corpora rather than a verified standalone full text of target 258-FZ/2020. `GITHUB_FULL_TEXT` for the target therefore remains unconfirmed.

## Regression gate
`NUMBER_MATCH != LEGAL_IDENTITY`.

Before accepting a candidate require body-level agreement on at least: `act_type + authority + exact_date + number + normalized_title`, then verify the lifecycle/current revision separately from a primary official source.

## Delta
- `FULL_TEXT +0`
- `CONFIRMED_NUMBER_COLLISION +1`
- `EXACT_DUPLICATE +0`
- `GITHUB_FULL_TEXT_BLOCKER: 258-ФЗ/2020 remains open`
