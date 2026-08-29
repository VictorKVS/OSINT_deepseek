# Habr NPA sweep — Stream 1 — 2026-08-29 19:53 MSK

Scope: continued systematic pass over Habr 432466 and the user NPA list. GitHub copies are treated as non-official evidence only; official identity/lifecycle is checked separately.

## Delta for this pass

- `GITHUB_FULL_TEXT +0`
- `BINARY_PDF_CANDIDATE +3`
- `SUMMARY_OR_NOTES_REJECT +3`
- `REFERENCE_TABLE_MENTION_REJECT +1`
- `GITHUB_FULL_TEXT_BLOCKER +2` (Roskomnadzor 178/179)
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +2` (Roskomnadzor 178/179)
- `CURRENT_AMENDMENT_MARKER_CONFIRMED +1` (152-FZ via 265-FZ/2026)
- `PDF_DIRECT_BODY_INSPECTION_BLOCKER +3`
- `EXACT_DUPLICATE +0`
- `BODY_IDENTITY_CONFLICT +0`

## 1. Federal Law 27.07.2006 No. 149-FZ

### GitHub artefacts

Companion note:
- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/ФЗ 149.md`
- size: `21340`
- type: `Markdown/file`
- blob: `4e053c8a4596d4d64be5e44af7473dc87f77bd6f`
- classification: `SUMMARY_EXTRACT / SELECTED_ARTICLES / NOT_FULL_TEXT`
- evidence: starts with a link to `[[ФP149.pdf]]`, then selected definitions and thematic fragments rather than the complete numbered law body.

Linked binary candidate:
- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/attachments/ФP149.pdf`
- size: `592565`
- type: `PDF/file`
- blob: `05f47bf9499121eb876c1b4e789522490a658257`
- classification: `BINARY_PDF_CANDIDATE / BODY_IDENTITY_UNVERIFIED / FULLTEXT_UNVERIFIED / NON_OFFICIAL_GITHUB_COPY`
- blocker: direct PDF body could not be retrieved for page/body inspection, so number/date/title inside the PDF and completeness are not promoted from filename/companion-note evidence.

### Official/lifecycle check

Original law identity is corroborated by official publication in Rossiyskaya Gazeta. A key temporal gate is now explicit: Federal Law No. 568-FZ of 29.12.2025 amends 149-FZ but enters into force only on `2026-09-01`. As of this pass (`2026-08-29`), a GitHub copy that prematurely includes those future provisions is not an accurate current-in-force consolidation. Publication and entry into force must therefore be modeled separately.

Sources:
- https://rg.ru/documents/2026/01/12/fz568-dok.html

Status: `GITHUB_PDF_CANDIDATE_FOUND / BODY_UNVERIFIED / FRESHNESS_UNVERIFIED`.

## 2. Federal Law 27.07.2006 No. 152-FZ "On Personal Data"

### GitHub artefacts

Companion note:
- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/ФЗ 152.md`
- size: `42427`
- type: `Markdown/file`
- blob: `4fccc3c95e1af3874a277b3dff4958b9f3ffce85`
- classification: `SUMMARY_EXTRACT / SELECTED_ARTICLES / NOT_FULL_TEXT`
- evidence: the file opens with `[[ФЗ152.pdf]]`, then commentary and selected articles (including Art. 19, 5, 6, 9, 10, 10.1, 11, 16, 18.1), not the complete law body.

Linked binary candidate:
- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/attachments/ФЗ152.pdf`
- size: `266755`
- type: `PDF/file`
- blob: `d12a53e869b5eeeafc985187d9a2331b3749f11a`
- classification: `BINARY_PDF_CANDIDATE / BODY_IDENTITY_UNVERIFIED / FULLTEXT_UNVERIFIED / NON_OFFICIAL_GITHUB_COPY`
- blocker: PDF body could not be retrieved for mandatory page/body inspection.

### Official/lifecycle check

Freshness floor advanced: Federal Law of 26.07.2026 No. 265-FZ directly amends Article 12 of 152-FZ. The amendment was published in 2026 and its Article 1 changes are already in force; a GitHub copy that lacks the effective 26.07.2026 Article 12 wording is stale for current use. Some other provisions of 265-FZ have later effective dates, so per-provision effective dates must be retained.

Status: `GITHUB_PDF_CANDIDATE_FOUND / BODY_UNVERIFIED / CURRENT_AMENDMENT_MARKER_265-FZ_2026`.

## 3. Government Resolution 01.11.2012 No. 1119

### GitHub artefacts

Companion note:
- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/ПП № 1119.md`
- size: `26071`
- type: `Markdown/file`
- blob: `ae49fc93460a72b53ef5b67326a65ac72371809a`
- body identity signal: exact header matches `Постановление Правительства РФ от 1 ноября 2012 г. N 1119` and the target title.
- classification: `LEGAL_NOTES / IMPLEMENTATION_GUIDE / IDENTITY_HEADER_MATCH / NOT_FULL_TEXT`
- evidence: after the identity header and PDF link the file gives section summaries, threat-modeling notes, implementation measures and explanatory material rather than the complete normative body.

Linked binary candidate:
- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/attachments/ПП 1119.pdf`
- size: `61801`
- type: `PDF/file`
- blob: `6154f092dfcc863fef9b4ee6e76ca733c75dae7f`
- classification: `BINARY_PDF_CANDIDATE / LINKED_FROM_IDENTITY_MATCHING_NOTE / BODY_IDENTITY_UNVERIFIED / FULLTEXT_UNVERIFIED / NON_OFFICIAL_GITHUB_COPY`
- blocker: direct PDF body inspection unavailable in this pass.

### Official check

Rossiyskaya Gazeta has the official publication of the target resolution with exact date/number/title and the approving clause for the attached Requirements. This corroborates identity independently of the GitHub copy. Direct current consolidated lifecycle remains a separate gate.

Source:
- https://rg.ru/documents/2012/11/07/pers-dannye-dok.html

Status: `OFFICIAL_INITIAL_PUBLICATION_CONFIRMED / GITHUB_BINARY_BODY_UNVERIFIED / CURRENT_LIFECYCLE_UNRESOLVED`.

## 4. Roskomnadzor Order 27.10.2022 No. 178

A new reproducible GitHub hit was checked and rejected as an act copy:
- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/ПДн пакет документов.md`
- size: `83439`
- type: `Markdown/file`
- blob: `9b11cb7110247398964d957a876fcd6abec2b2bd`
- classification: `REFERENCE_TABLE / MENTION_ONLY / NOT_FULL_TEXT / REJECT`
- evidence: Order No. 178 is cited as a legal basis for internal harm-assessment documents; the normative body of Order 178 is not reproduced.

A distinctive body-phrase GitHub code search returned `total_count=0`, `incomplete_results=false`; this is a blocker, not proof of absence.

Primary official publication directly confirms:
- date/no.: `27.10.2022 № 178`
- title: Requirements for assessing harm to personal-data subjects
- Ministry of Justice registration: `28.11.2022 № 71166`
- publication id: `0001202211290004`
- publication date: `29.11.2022`

Primary source:
- https://publication.pravo.gov.ru/Document/View/0001202211290004

Status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER`.

## 5. Roskomnadzor Order 28.10.2022 No. 179

No verified full GitHub body was obtained. Exact-title searches yield references/commentary, but a distinctive normative-body phrase search returned `total_count=0`, `incomplete_results=false`.

Primary official publication directly confirms:
- date/no.: `28.10.2022 № 179`
- title: Requirements for confirming destruction of personal data
- Ministry of Justice registration: `28.11.2022 № 71167`
- publication id: `0001202211290008`
- publication date: `29.11.2022`

Primary source:
- https://publication.pravo.gov.ru/Document/View/0001202211290008

Status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER`.

## New corpus gates

1. `TREE_TRAVERSAL > CODE_SEARCH_FOR_BINARIES`: repository tree traversal can expose PDF/DOCX candidates that ordinary GitHub Code Search misses.
2. `COMPANION_NOTE_IDENTITY != LINKED_BINARY_BODY_IDENTITY`: a note that names an act and links a PDF does not prove that the binary itself contains the correct/full act until the binary body is inspected.
3. `BINARY_WITHOUT_PAGE_INSPECTION != FULL_TEXT`: binary candidates remain candidates when page/body inspection is unavailable.
4. `PUBLISHED != IN_FORCE`: freshness must track publication and effective dates separately; 149-FZ/568-FZ provides a concrete current example because 568-FZ is published but enters into force only 01.09.2026.
5. `IDENTITY_HEADER_MATCH != NORMATIVE_BODY`: an exact number/date/title in a Markdown note may validate the referenced identity but the file can still be only notes or an implementation guide.
6. `NUMBER_ONLY_OFFICIAL_SEARCH_IS_UNSAFE`: reused resolution/order numbers generate unrelated official hits; date + issuer + title must be part of primary-source resolution.
