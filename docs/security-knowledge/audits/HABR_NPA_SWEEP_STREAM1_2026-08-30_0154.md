# Habr NPA sweep — Stream 1 — 2026-08-30 01:54 MSK

Scope: continuation of Habr 432466 / user NPA list. GitHub copies are treated only as non-official corpus candidates. Official/current status is checked separately.

## Delta

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- REJECTED_NON_BODY: +3
- GITHUB_FULL_TEXT_BLOCKER: +6
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +1
- CURRENT_STATUS_CORROBORATED: +6
- PRIMARY_DIRECT_CARD_UNRESOLVED: +5
- DUPLICATE_REFERENCE_HIT: +1

## New checked acts

### PPRF 18.09.2012 No. 940
Target title: Rules for coordinating projects of decisions of associations/unions of operators on additional PD threats with FSB/FSTEC.

GitHub: exact/variant search produced no reproducible act body.
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: GITHUB_FULL_TEXT_BLOCKER

Identity/current status: current consolidated secondary source shows the original 18.09.2012 edition, effective 02.10.2012, status active. Direct primary publication card was not resolved in this run, therefore not PRIMARY_CURRENT_VERIFIED.
Completeness gate: FULL_TEXT requires the resolution plus the full approved Rules.

### PPRF 19.08.2015 No. 857
Target: AIS “Register of violators of rights of personal-data subjects”.

GitHub broad phrase search produced a false positive:
- repo: ninastoessinger/word-o-mat
- commit: 13f0e55fbb1eb1e897e2f14f23aad9928a3fc6d4
- path: word-o-mat.roboFontExt/resources/russian.txt
- size: 356755 B
- type: TXT/file
- blob: 2aec0a58811902e27bd682861f9720a690a85141
- body: Russian frequency wordlist derived from Leipzig corpus, not an act
- classification: CORPUS_WORDLIST / SEARCH_FALSE_POSITIVE / NOT_ACT_BODY / REJECT

No reproducible full act body found: GITHUB_FULL_TEXT_BLOCKER.
Current status corroborated: revision 13.11.2019, effective 26.11.2019, active; amendment marker PPRF 13.11.2019 No. 1443. Direct primary current card unresolved.
Completeness gate: FULL_TEXT must contain the resolution, Rules of creation/formation/maintenance of the register, and criteria for determining the register operator.

### Roskomnadzor Order 22.07.2015 No. 84
GitHub exact/registration-number searches produced no reproducible act body.
- repo/commit/path/size/type: null
- classification: GITHUB_FULL_TEXT_BLOCKER

Identity corroborated: Minjust registration No. 38532. Current legal sources continue to list the act as applicable. Direct primary publication card unresolved.
Completeness gate: FULL_TEXT requires BOTH approved procedures: interaction of register operator with hosting provider + access to register information by telecom operator.

### Roskomnadzor Order 22.07.2015 No. 85
GitHub exact/registration-number searches produced no reproducible act body.
- repo/commit/path/size/type: null
- classification: GITHUB_FULL_TEXT_BLOCKER

Identity corroborated: Minjust registration No. 38544. Current legal sources continue to list the act. Direct primary publication card unresolved.
Completeness gate: FULL_TEXT requires the attached application form, not only the dispositive part of the order.

### Roskomnadzor Order 24.02.2021 No. 18
GitHub phrase search produced a false positive privacy-policy implementation:
- repo: sergeygutovskiy/papakado.ru
- commit: 800e338ee3641228f86dbad5d7b32b81e0834691
- path: resources/ts/client/vue/layout/contacts/Policy.vue
- size: 42987 B
- type: Vue/file
- blob: 7ccacc8694fd062bca71a04f6a6e956f8bf6b774
- body: website operator privacy policy, not Roskomnadzor Order No. 18
- classification: DERIVATIVE_PRIVACY_POLICY / NOT_ACT_BODY / REJECT

The same search also returned the already-known full 152-FZ file in Grantik/odin-vault only because the order is referenced inside the law history/body: DUPLICATE_REFERENCE_HIT / NOT_TARGET_BODY.
No full GitHub act body found: GITHUB_FULL_TEXT_BLOCKER.
Current status corroborated: effective from 01.09.2021 and expressly valid through 01.09.2027; Minjust No. 63204. Direct primary publication card unresolved.
Completeness gate: FULL_TEXT requires the order plus the full approved Requirements.

### Roskomnadzor Order 19.06.2025 No. 140
GitHub search found an implementation artifact, not the act:
- repo: Namelomax/Anon
- commit: 79277627343e5df8ed4ab3893e7dad4dda5d42ac
- path: anonymizer/depersonalization_log.py
- size: 15701 B
- type: Python/file
- blob: e07f7e7cb1f3a98eff0381e78c32e7baaddd4bea
- body: depersonalization log implementation that references Order No. 140 and quotes a short requirement; not normative body
- classification: IMPLEMENTATION_REFERENCE_WITH_SHORT_QUOTE / NOT_FULL_TEXT / REJECT

No reproducible full GitHub act body found: GITHUB_FULL_TEXT_BLOCKER.
Primary official publication index CONFIRMED:
- exact act/date/number/title confirmed
- Minjust registration: No. 83110 on 31.07.2025
- official publication No.: 0001202508010002
- publication date: 01.08.2025
- official PDF: 427 KB / 10 pages
Current status corroborated: effective from 01.09.2025.
Completeness gate: FULL_TEXT requires the order + Appendix 1 (requirements) + Appendix 2 (methods).

## New regression gates

1. SEARCH_PHRASE_HIT != ACT_BODY — a privacy policy, source-code implementation or corpus wordlist can match a characteristic legal phrase.
2. QUOTED_REQUIREMENT != FULL_TEXT — implementation code quoting an NPA clause remains a derivative reference.
3. MULTI_APPENDIX_ORDER_FULLTEXT — an order approving several appendices is FULL_TEXT only when all approved appendices are present.
4. CURRENT_SECONDARY_STATUS != PRIMARY_CURRENT_VERIFIED — current status from legal-reference systems is kept separate until a primary official source/current body is directly resolved.

## Primary/secondary source notes

- Official publication portal confirms Roskomnadzor Order No. 140: https://publication.pravo.gov.ru/ (publication No. 0001202508010002).
- Habr source snapshot: https://habr.com/ru/articles/432466/ (version 28.05.2026).
- Other current-status checks in this run were corroborative only and are not promoted to primary verification.
