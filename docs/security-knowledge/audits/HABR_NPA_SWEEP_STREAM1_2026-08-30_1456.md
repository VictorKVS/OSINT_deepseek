# Habr NPA sweep — Stream 1 — 2026-08-30 14:56 MSK

Scope: Habr 432466, block «Персональные данные», Roskomnadzor / departmental acts: items 25, 27, 29, 33, 34, 38, 39, 40. Items 35–36 (orders №178/2022 and №179/2022) were audited in an earlier pass and are intentionally not repeated.

## Delta

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +8`
- `REJECTED_GITHUB_REFERENCE_OR_IMPLEMENTATION +2`
  - duplicate known reference artifact for №187/2022;
  - new implementation/source-code reference for №140/2025.
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +3` — №128/2022, №180/2022, №140/2025.
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED +2` — №18/2021, №253/2021 (direct portal fetch timed out; pointer retained, not promoted to direct-primary verification).
- `CURRENT_EDITION_CORROBORATED +2` — №253/2021 → edition 10.01.2023; №128/2022 → base/current edition corroborated as 05.08.2022 in this pass.
- `EXPLICIT_VALIDITY_WINDOW_CONFIRMED +2` — №18/2021 to 01.09.2027; №106/2021 to 01.03.2028.
- `LEGACY_LIFECYCLE_CONFLICT +1` — №482/2010: normative core marked repealed by №706/2011, while №706 itself was later cancelled by №198/2014; no automatic revival is accepted.
- exact duplicate full normative bodies: `+0`
- GitHub target-body identity conflicts: `+0`

GitHub searches used exact/near-exact date + number + distinctive title terms. For acts with no reproducible target file, `repo/commit/path/size/type = null` is intentional and means no GitHub artifact passed candidate intake.

## Per-act results

### Приказ Роскомнадзора от 16.07.2010 №482

- GitHub: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Consolidated body still identifies the act exactly by date/number/title, but points 1–2 and both normative appendices are marked as having lost force by Roskomnadzor order №706 of 19.08.2011.
- Order №706 itself expressly recognized points 1–2 of №482 as having lost force and replaced the notification recommendations.
- Roskomnadzor order №198 of 30.12.2014 later cancelled orders №706 and №37/2014 following Ministry of Justice legal review; secondary legal commentary links that cancellation to the newer notification regime under the Mincomsvyaz administrative regulation №346/2011.
- Critical lifecycle rule: cancellation of the amending/replacing act is **not** treated as automatic revival of the text previously marked repealed in №482. Current consolidated copies continue to show the form/recommendations as repealed.
- Classification: `LEGACY_ACT / NORMATIVE_CORE_REPEALED_IN_CONSOLIDATED_TEXT / AMENDING_ACT_706_LATER_CANCELLED / NO_AUTOMATIC_REVIVAL / PRIMARY_HISTORICAL_PUBLICATION_RECORD_UNRESOLVED`.
- Habr keeps №482 as a reference; for operational notification forms it must not be treated as the current form source without a separate legal applicability check.

### Приказ Роскомнадзора от 24.02.2021 №18

- GitHub: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Body identity confirmed by exact date/number/title; Ministry of Justice registration №63204.
- Effective from `01.09.2021`; explicit validity horizon: `through 01.09.2027`.
- Official publication pointer corroborated as `0001202104210039`; direct primary portal fetch timed out in this pass, therefore status is `OFFICIAL_PUBLICATION_POINTER_CORROBORATED`, not `PRIMARY_DIRECT_CARD_VERIFIED`.
- Completeness gate: `FULL_TEXT = приказ + полные Требования к содержанию согласия`.

### Приказ Роскомнадзора от 21.06.2021 №106

- GitHub: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Exact title and Ministry of Justice registration №64602 corroborated; full Rules are present in legal-text sources.
- Effective from `01.03.2022`; explicit validity horizon: `through 01.03.2028`.
- Publication on pravo.gov.ru on 11.08.2021 is corroborated, but exact official publication ID/direct primary card was not resolved in this pass.
- Classification: `ACTIVE_BY_EXPLICIT_VALIDITY_WINDOW / PRIMARY_PUBLICATION_ID_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.
- Completeness gate: `FULL_TEXT = приказ + полные Правила использования информационной системы и взаимодействия субъекта с оператором`.

### Приказ Роскомнадзора от 24.12.2021 №253

- GitHub: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Exact identity and Ministry of Justice registration №67486 corroborated.
- Current consolidated edition corroborated as `10.01.2023`.
- Roskomnadzor order №1 of 10.01.2023 (Minjust registration №72886) directly changes the checklist form approved by №253.
- Initial official publication pointer corroborated as `0001202202280005`; direct primary fetch timed out. Latest-amendment primary publication record remains unresolved in this pass.
- Completeness gate: `FULL_TEXT = приказ + вся актуальная форма проверочного листа`; a pre-2023 form is `STALE`.

### Приказ Роскомнадзора от 05.08.2022 №128

- GitHub: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Primary official publication directly confirmed: `0001202209200008`, published `20.09.2022`; Minjust registration №70152.
- Exact title: list of foreign states providing adequate protection of personal-data-subject rights.
- Effective from `01.03.2023`; fresh search did not reveal a later enacted edition. Do not infer immutability from absence of a later hit.
- Completeness gate: `FULL_TEXT = приказ + полный перечень государств`.

### Приказ Роскомнадзора от 28.10.2022 №180

- GitHub: `repo=null; commit=null; path=null; size=null; type=null` → `GITHUB_FULL_TEXT_BLOCKER`.
- Primary official publication directly confirmed: `0001202212150022`, published `15.12.2022`; Minjust registration №71532.
- Exact body identity confirmed by date/number/title.
- The order approves three separate notification forms: intention to process; change of information in the notification; termination of processing.
- Fresh search did not reveal a later enacted edition; base edition remains the freshness floor for this pass.
- Completeness gate: `FULL_TEXT = приказ + all 3 approved forms`; one form alone is `PARTIAL_TEXT`.

### Приказ Роскомнадзора от 14.11.2022 №187

- GitHub search returned one artifact, but it is a **known duplicate false candidate**:
  - `repo=Grantik/odin-vault`
  - `commit=f2340b233394bed47ade7ed0de97381223f93230`
  - `path=sync/canon/package/samples/koncepciya_gis_rt_teo.txt`
  - `blob=067866c9fe3b098c0432205ca554945298e53bd8`
  - `size=345746 bytes` (same immutable blob previously measured)
  - `type=TXT/file`
- Body inspection starts with `ГОСУДАРСТВЕННАЯ ИНФОРМАЦИОННАЯ СИСТЕМА «РОССИЙСКИЙ ТРАНСПОРТ» / КОНЦЕПЦИЯ ... Москва 2024`; the target order is only a reference inside a technical document.
- Classification: `DUPLICATE_REFERENCE_ARTIFACT / WRONG_PRIMARY_BODY / REFERENCE_ONLY / REJECT`.
- Target normative body remains `GITHUB_FULL_TEXT_BLOCKER`.
- Exact order identity and Minjust registration №71851 corroborated; effective from `01.03.2023`. Direct official publication card/ID remains unresolved in this pass.
- Completeness gate: `FULL_TEXT = приказ + весь Порядок и условия взаимодействия по реестру учета инцидентов`.

### Приказ Роскомнадзора от 19.06.2025 №140

- GitHub returned a **new non-target implementation artifact**:
  - `repo=Namelomax/Anon`
  - `commit=79277627343e5df8ed4ab3893e7dad4dda5d42ac`
  - `path=anonymizer/depersonalization_log.py`
  - `blob=e07f7e7cb1f3a98eff0381e78c32e7baaddd4bea`
  - `size=METADATA_UNRESOLVED`
  - `type=Python/file`
- Body inspection shows Python source code for an anonymization-operation log. Its module docstring says it is implemented pursuant to point 1.7 of requirements approved by order №140 and quotes a fragment; later comments refer to a method from appendix 2. This is evidence of practical use, **not** a normative copy.
- Classification: `REFERENCE_IMPLEMENTATION / QUOTED_FRAGMENT / NON_TARGET_BODY / REJECT`.
- Therefore target order remains `GITHUB_FULL_TEXT_BLOCKER`.
- Primary official publication directly confirmed by the official publication block: exact title, Minjust registration №83110, publication ID `0001202508010002`, published `01.08.2025`, official PDF `427 KB / 10 pages`.
- Effective from `01.09.2025`; current mandatory-requirements sources continue to reference it.
- Completeness gate: `FULL_TEXT = приказ + Приложение 1 (Требования) + Приложение 2 (Методы)`.

## New corpus gates

1. `IMPLEMENTATION_REFERENCE != FULL_NPA_BODY` — source code that implements a requirement and quotes selected clauses is evidence of application, not a full normative artifact.
2. `CANCELLED_AMENDING_ACT != AUTOMATIC_REVIVAL_OF_REPEALED_TEXT` — №482/№706/№198 demonstrates why lifecycle must preserve the whole change chain; do not reconstruct revival by intuition.
3. `FULL_TEXT_FOR_FORM_ORDER = ORDER + ALL_APPROVED_FORMS/APPENDICES` — №180 and №253 cannot pass completeness on a single form or order header.
4. `EXPLICIT_VALID_UNTIL` is stored separately from edition/effective dates — №18 and №106 have finite validity horizons that require future re-check before expiry.
5. GitHub artifact identity continues to use `repo + commit + path + blob SHA`; repeated references to the same blob are counted once.

## Primary/official pointers captured

- №18/2021: `https://publication.pravo.gov.ru/Document/View/0001202104210039` — pointer corroborated; direct fetch timed out.
- №253/2021: `https://publication.pravo.gov.ru/Document/View/0001202202280005` — pointer corroborated; direct fetch timed out.
- №128/2022: `https://publication.pravo.gov.ru/Document/View/0001202209200008` — direct primary page confirmed.
- №180/2022: `https://publication.pravo.gov.ru/Document/View/0001202212150022` — direct primary page confirmed.
- №140/2025: `https://publication.pravo.gov.ru/document/0001202508010002` — direct primary publication block confirmed.

## Next queue

Continue after the Roskomnadzor PDn list into the Habr PDn security/technical-protection block while skipping acts already audited (notably PP №1119): government PDn-security acts, FSTEK/FSB requirements, and other general PDn/information acts. Preserve the same separation of GitHub-body identity, official publication, current effective version, future effective changes, and lifecycle status.
