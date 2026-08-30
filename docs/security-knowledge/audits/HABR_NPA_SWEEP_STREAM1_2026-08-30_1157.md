# Habr NPA sweep — Stream 1 — 2026-08-30 11:57 MSK

## Scope of this pass

Continued the systematic sweep of Habr 432466 (snapshot/version shown by Habr: 28.05.2026) and the working NPA list. This pass covers four previously unreported items from the Habr block on special cases of personal-data processing:

1. Federal Law No. 39-FZ of 22.04.1996, “On the Securities Market”.
2. Federal Law No. 57-FZ of 27.05.1996, “On State Protection”.
3. Air Code of the Russian Federation of 19.03.1997 No. 60-FZ.
4. Federal Law No. 143-FZ of 15.11.1997, “On Acts of Civil Status”.

GitHub copies are treated only as non-official secondary artifacts. Official/current status is checked independently.

## Pass counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +4`
- `CURRENT_EFFECTIVE_EDITION_CORROBORATED +4`
- `OFFICIAL_RG_AMENDMENT_FULLTEXT_CONFIRMED +3` (39-FZ via 172-FZ; 57-FZ via 177-FZ; Air Code via 141-FZ publication/full text)
- `PRIMARY_OFFICIAL_PUBLICATION_ID_CONFIRMED +2` (172-FZ: `0001202606100022`; 287-FZ: `0001202608040012`)
- `KNOWN_FUTURE_EFFECTIVE_CHANGE +3` (39-FZ: 01.09.2026; 57-FZ: one provision 01.09.2026; 143-FZ: 01.12.2026)
- `ENACTED_BUT_NOT_YET_EFFECTIVE_AIR_CODE_AMENDMENTS +2` (49-FZ/2026 and 141-FZ/2026, both beginning 01.09.2026 in whole or in part)
- new exact full-body duplicates: `0`
- new GitHub body-identity conflicts: `0`

## Findings

### 1. Federal Law No. 39-FZ of 22.04.1996 — “On the Securities Market”

**GitHub search**

Exact/title searches for `22.04.1996 39-ФЗ рынок ценных бумаг` and `39-ФЗ О рынке ценных бумаг` returned no reproducible target file.

- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

No mention/summary artifact is promoted to candidate status.

**Identity/currentness**

The base act is currently represented by legal systems as amended on 10.06.2026. Federal Law No. 172-FZ of 10.06.2026 is an amending act; it entered into force on 01.07.2026. The official publication pointer for 172-FZ is `0001202606100022` (10.06.2026), and Rossiyskaya Gazeta published the full text on 16.06.2026.

A further enacted amendment, Federal Law No. 283-FZ of 04.08.2026, changes provisions of 39-FZ from 01.09.2026 (including, inter alia, provisions shown in the future versions of Arts. 3 and 7). Therefore the corpus must distinguish the text effective on 30.08.2026 from the already enacted future version beginning 01.09.2026.

Status: `CURRENT_EFFECTIVE_EDITION_CORROBORATED_2026-06-10 / KNOWN_FUTURE_EFFECTIVE_CHANGE_2026-09-01 / GITHUB_FULL_TEXT_BLOCKER`.

### 2. Federal Law No. 57-FZ of 27.05.1996 — “On State Protection”

**GitHub search**

Exact search for `27.05.1996 57-ФЗ государственной охране` returned no target file.

- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

**Identity/currentness**

Federal Law No. 177-FZ of 10.06.2026 directly amends Federal Law No. 57-FZ of 27.05.1996 “On State Protection”. Rossiyskaya Gazeta published the full amending law on 16.06.2026. Most amendments are already in force; one specifically delayed rule concerning provision of specialized housing to certain servicemen of state-protection bodies takes effect on 01.09.2026.

Status: `CURRENT_EDITION_CORROBORATED_2026-06-10 / SPLIT_EFFECTIVE_DATE_WITH_FUTURE_PROVISION_2026-09-01 / GITHUB_FULL_TEXT_BLOCKER`.

### 3. Air Code of the Russian Federation of 19.03.1997 No. 60-FZ

**GitHub search**

Exact search for `19.03.1997 60-ФЗ Воздушный кодекс Российской Федерации` returned no target file.

- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

**Identity/currentness**

For the text actually effective on 30.08.2026, current legal systems still show the Air Code in the edition of 28.11.2025, with amendments/effects through 01.03.2026, and explicitly mark that a prepared version contains changes not yet in force.

Two 2026 amending laws have already been enacted but are not yet effective as of this pass:

- Federal Law No. 49-FZ of 08.03.2026 amends Art. 108 and enters into force on 01.09.2026.
- Federal Law No. 141-FZ of 25.05.2026 extensively amends the Air Code and suspends Art. 101.2; Rossiyskaya Gazeta published the full text on 29.05.2026. Its main provisions enter into force on 01.09.2026, while specified provisions enter into force on 01.03.2028.

Thus `red. 25.05.2026` as an enacted/prepared version must not be confused with the text legally effective on 30.08.2026.

Status: `CURRENT_EFFECTIVE_EDITION_2025-11-28_WITH_EFFECTS_THROUGH_2026-03-01 / ENACTED_FUTURE_AMENDMENTS_49-FZ_AND_141-FZ / NEXT_CHANGE_2026-09-01 / GITHUB_FULL_TEXT_BLOCKER`.

### 4. Federal Law No. 143-FZ of 15.11.1997 — “On Acts of Civil Status”

**GitHub search**

Exact search for `15.11.1997 143-ФЗ актах гражданского состояния` returned no target file.

- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`
- classification: `GITHUB_FULL_TEXT_BLOCKER`

**Identity/currentness**

Federal Law No. 287-FZ of 04.08.2026 directly amends 143-FZ. Its text identifies the target law by exact date, number and title. The amendment has been officially published under publication No. `0001202608040012` and does **not** enter into force until 01.12.2026. Current legal systems explicitly label it as not yet in force / a prepared future version.

Accordingly, a source that labels 143-FZ simply `ред. 04.08.2026` without separately recording the effective date is insufficient for the current-effective corpus on 30.08.2026.

Status: `CURRENT_EFFECTIVE_BODY_PRE_287-FZ / ENACTED_FUTURE_EDITION_2026-12-01 / GITHUB_FULL_TEXT_BLOCKER`.

## New corpus rule confirmed by this pass

`EDITION_DATE != EFFECTIVE_TEXT_DATE`.

An amending act may already be signed and officially published, and a legal system may expose a “prepared edition” dated by that amendment, while the amended provisions are not yet legally effective. The corpus therefore keeps at least these states separately:

- `enacted_at`
- `officially_published_at`
- `effective_from`
- `current_effective_body_as_of`
- `prepared_future_body`

This is especially material here for the Air Code (changes from 01.09.2026 and 01.03.2028) and 143-FZ (changes from 01.12.2026).

## Sources checked

- Habr 432466, version shown as 28.05.2026; target rows include 39-FZ, 57-FZ, Air Code No. 60-FZ and 143-FZ.
- GitHub Code Search via connected GitHub search: no target full-body files for all four acts.
- Rossiyskaya Gazeta: full text/publication of Federal Law No. 172-FZ of 10.06.2026 (published 16.06.2026); Federal Law No. 177-FZ of 10.06.2026 (published 16.06.2026); Federal Law No. 141-FZ of 25.05.2026 (published 29.05.2026).
- Official publication pointer corroboration: 172-FZ — `0001202606100022`; 287-FZ — `0001202608040012`.
- Current/future version cross-check: ConsultantPlus/Garant current and prepared-version markers.

No GitHub copy is marked official merely because it may reproduce an official source.