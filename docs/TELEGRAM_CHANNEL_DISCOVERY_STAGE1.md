# Telegram OSINT Channel Discovery — Stage 1

Status: first functional local registry/CSV-JSON reporting tool; **not** an exhaustive discovery crawler or live TGStat/Telemetr integration.

## Goal
Find, deduplicate, verify, rank and continuously monitor public Telegram channels relevant to OSINT. The permanent ALINA LAB registry is separate from B2B client datasets. Data must be saved between runs.

## Discovery sources and adapters
1. Seed lists of public channels with provenance.
2. Authorized Telegram API search / linked public channels / public forward attribution (future).
3. TGStat catalog and rankings: https://tgstat.ru/channel and https://tgstat.ru/ratings/channels (future licensed API/authorized imports).
4. Telemetr channel search and category filters: https://telemetr.me/ (future authorized import).
5. Telemetr.com rankings/API: https://telemetr.com/ (review API docs and usage terms before implementing).
6. Public curated lists, websites and repository references (future).

Do not scrape protected content, bypass access controls, or treat directory coverage as complete.

## Registry
File: `data/telegram/channel_registry.json`. Incoming seed: `data/telegram/osint_candidates.csv`.
Each record has channel_id, username, title, public URL, language, topics, discovered_from, discovery/verification timestamps, status, observed metrics, evidence and validated skill counts.
Use stable Telegram numeric IDs when available; usernames can change. Deduplicate by verified numeric ID when a Telegram adapter is built. Current CLI uses provided channel_id and is not a definitive identity resolver.

## Rating philosophy
Three separate dimensions:
- Popularity: subscribers and views; never equate with truth.
- Research quality: activity, original material, references and provenance.
- Skill utility: methods successfully validated by ALINA on a permitted test fixture.

Initial transparent weighted composite: 10% popularity, 15% activity, 20% originality, 25% evidence, 30% verified skill yield. This is a **prototype heuristic**, not a validated scientific metric. A composite score is **null** until all needed observations exist. Unknown values are not zeros.
`engagement_ratio` is an approximation (views/subscribers), not an audience authenticity verdict. Observations must have a measurement window and provenance before comparisons are trusted.

## Run (Python 3, standard library)
```powershell
python tools/telegram_channel_catalog.py --input data/telegram/osint_candidates.csv --registry data/telegram/channel_registry.json --out out/telegram_channel_catalog
```
Outputs:
- `data/telegram/channel_registry.json` persistent registry
- `out/telegram_channel_catalog/channels.json`
- `out/telegram_channel_catalog/channels.csv` (Excel UTF-8 BOM)
- `out/telegram_channel_catalog/ratings.json`
- `out/telegram_channel_catalog/ratings.csv`
- `out/telegram_channel_catalog/report.md`

The seed entries are **candidates**; no live channel verification or metrics have been performed. To expand, add CSV rows or import an authorized CSV/JSON catalog.

## Acceptance and next gates
T1: CLI imports seed, writes all files, preserves unknown metrics, repeat run idempotent.
T2: Telegram adapter verifies candidate identities and metadata in authorized session, with checkpoints, explicit network route policy and bounded requests.
T3: TGStat/Telemetr adapters with permitted API use and source snapshots.
T4: automated candidate expansion through citations, links and forwards; duplicates reviewed.
T5: professional rating using per-source evidence and time-windowed observations.
T6: connect registry to ALINA Telegram Workspace; add report UI, snapshots and change tracking.
T7: ALINA Skill Factory scores only experimentally validated skills.

Do not put session files, API credentials or client datasets into Git.
