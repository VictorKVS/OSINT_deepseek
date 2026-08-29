# Habr NPA sweep — Stream 1 — 2026-08-29 07:55 MSK

Scope: continuation of the systematic pass over Habr 432466 and the user NPA list. GitHub copies are treated only as non-official evidence; legal status/currentness is verified separately against primary official sources when resolvable.

## New findings

### PP RF 01.11.2012 No. 1119 — secondary reference, not full text

Target: Постановление Правительства РФ от 01.11.2012 № 1119 «Об утверждении требований к защите персональных данных при их обработке в информационных системах персональных данных».

GitHub candidate:
- repo: `SwairIt/doday`
- commit: `c7e9ac691aa3e2cc2f2f30367072e71bd248f69e`
- path: `docs/legal/perechen-ugroz.md`
- size: `5865` bytes
- type: `Markdown/blob`
- blob SHA: `e23b7a82aa51387df82cdb0203621cc02744be16`

Body check: the file is a 2026 threat-model document for `getdoday.ru`. It explicitly states that it was prepared under PP RF `01.11.2012 № 1119`, later uses `п. 13 постановления № 1119`, and derives UZ-4. It does not contain the resolution, its approval clause, the complete approved Requirements, or the closing legal text.

Classification: `SECONDARY_THREAT_MODEL / EXACT_DATE_NUMBER_REFERENCE / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY / REJECT_FOR_PRIMARY_KB`.

Official-status handling: no GitHub status promotion. The primary official lifecycle/current consolidated state was not re-resolved in this pass; keep `PRIMARY_OFFICIAL_LIFECYCLE_BLOCKER` until a primary official lifecycle card is successfully fetched.

### Roskomnadzor order 27.10.2022 No. 178 — unnumbered secondary implementation reference

Target: Приказ Роскомнадзора от 27.10.2022 № 178 «Об утверждении Требований к оценке вреда, который может быть причинен субъектам персональных данных в случае нарушения Федерального закона "О персональных данных"».

GitHub candidate:
- repo: `SwairIt/doday`
- commit: `c7e9ac691aa3e2cc2f2f30367072e71bd248f69e`
- path: `docs/legal/otsenka-vreda.md`
- size: `4350` bytes
- type: `Markdown/blob`
- blob SHA: `53c8e2c084669ab24551c9ee2ab907e3153bb2e5`

Body check: this is an operator-specific harm assessment. It says the assessment is made `в соответствии с приказом Роскомнадзора об определении критериев вреда`, but does not give the order number, date, exact official title, registration data, or normative body. Therefore target identity cannot be proven from this GitHub file alone.

Classification: `UNNUMBERED_SECONDARY_REFERENCE / IMPLEMENTATION_DOCUMENT / TARGET_INFERENCE_ONLY / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY / REJECT_FOR_PRIMARY_KB`.

Primary official source separately confirms the real target identity: order 27.10.2022 № 178, registration 28.11.2022 № 71166, official publication No. `0001202211290004` on 29.11.2022. No GitHub full text confirmed.

### Roskomnadzor order 28.10.2022 No. 179 — GitHub full-text blocker retained

Target: Приказ Роскомнадзора от 28.10.2022 № 179 «Об утверждении Требований к подтверждению уничтожения персональных данных».

Exact GitHub code searches by date/number/title yielded no full-text candidate in this pass. This is only `EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

Primary official source confirms identity: registration 28.11.2022 № 71167; official publication No. `0001202211290008` on 29.11.2022.

Classification: `GITHUB_FULL_TEXT_BLOCKER / PRIMARY_IDENTITY_CONFIRMED / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

### PP RF 06.07.2008 No. 512 — no confirmed GitHub body

Target: Постановление Правительства РФ от 06.07.2008 № 512 «Об утверждении требований к материальным носителям биометрических персональных данных и технологиям хранения таких данных вне информационных систем персональных данных».

GitHub searches by date/number/title and biometric-personal-data wording produced no currently resolvable full-text candidate. A previously surfaced transient search hit in `vivsega/PersonalDataNormRepo` could not be reopened (repository/resource now returned not found), so it is not counted as a confirmed finding.

Classification: `GITHUB_FULL_TEXT_BLOCKER / TRANSIENT_HIT_NOT_REPRODUCIBLE / DO_NOT_COUNT_AS_FINDING`.

The direct primary official lifecycle card was not resolved in this pass; do not infer currentness from non-official legal mirrors.

## New counters for this pass

- `FULL_TEXT`: +0
- `SECONDARY_REFERENCE`: +2
- `GITHUB_FULL_TEXT_BLOCKER`: +2 (RKN 179; PP 512)
- `TRANSIENT_UNREPRODUCIBLE_HIT`: +1 (not counted as candidate)
- `EXACT_DUPLICATE`: +0
- `IDENTITY_CONFLICT`: +0

## Gates added/reinforced

1. `IMPLEMENTATION_DOCUMENT_REFERENCES_ACT != ACT_FULL_TEXT`.
2. `UNNUMBERED_GENERIC_REFERENCE != TARGET_IDENTITY_VERIFIED`.
3. `TRANSIENT_SEARCH_HIT_NOT_REPRODUCIBLE != CONFIRMED_CANDIDATE`.
4. `EXACT_SEARCH_ZERO != PROOF_OF_ABSENCE`.
5. `GITHUB_COPY_OR_REFERENCE != OFFICIAL_SOURCE`.
6. `PRIMARY_INITIAL_PUBLICATION != VERIFIED_CURRENT_LIFECYCLE`.
