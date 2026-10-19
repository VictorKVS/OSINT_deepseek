# FATHER OSINT — External Telegram analytics adapter (TGStat)

Status: official TGStat API connector implemented; **no live API request has been made in this repository update**. Requires an API Stat token with channel-search permission.

## Research basis
- TGStat channels/search: https://api.tgstat.ru/docs/ru/channels/search.html — keyword/category discovery; API Stat tier S or higher.
- TGStat channels/stat: https://api.tgstat.ru/docs/ru/channels/stat.html — subscribers, average reach, ERR, citations, forwards, mentions.
- Telemetr.me API: https://api.telemetr.me/doc — separate provider, future adapter.
- Telemetr.io API: https://api.tlmtr.io/docs/intro/getting-started/ — separate provider, future adapter.
- Telemetr.com: https://telemetr.com/ — separate service; evaluate its API contract before integration.

These are distinct products/providers; do not mix credentials or invent endpoints.

## Run from isolated ALINA checkout
```powershell
Set-Location 'G:\1\OSINT_ALINA_PREVIEW'
$env:TGSTAT_API_TOKEN = Read-Host 'TGStat API token'
python tools/tgstat_channel_discovery.py --query OSINT --query форензика --limit 20
```
For metrics, add `--stats --max-stats 10`. These calls consume API quota; start with small limits. The token is read from an environment variable, never placed in the command line or repository. Clear it after running: `Remove-Item Env:TGSTAT_API_TOKEN`.

## Saved files
- `data/telegram/channel_registry.json`: persistent catalog, merged by public username-derived key. Username is mutable: future Telegram numeric-ID reconciliation is required.
- `out/telegram_channel_catalog/tgstat_snapshots.jsonl`: append-only time-stamped source observations with provider, method and metrics.
- `out/telegram_channel_catalog/tgstat_discovery_report.json`: results and run summary.

The existing local server reads the registry for `GET /api/channels` on each request. Refresh `advisor.html` after import; no restart is required. The advisor can then rank new candidates by topic, but external discovery is not equivalent to identity verification. For trustworthy quality rankings, add a distinct evidence-based methodology and dated source snapshots.

## Constraints
- Official documented API only; no browser scraping, no circumvention.
- Query results are candidates, not confirmed sources. `status=candidate` until independent Telegram verification.
- Metrics are provider observations; never infer truthfulness or bot activity from counts alone.
- TGStat search `participants_count` is mapped to `subscribers`; TGStat stat `avg_post_reach` to `avg_views`. `posts_30d`, `original_posts_30d`, `evidence_links` and `validated_skills` are **not invented**.
- Current registry merge uses username key; identity reconciliation and username-change handling remain future work.
- The connector performs bounded queries and bounded optional stat calls, with pause.
- Partial failures do not overwrite the registry: writes happen after successful collection. The service does not run automatically on a schedule.

## Tests
```powershell
python -m unittest discover -s tests -p "test_tgstat_channel_discovery.py" -v
```

## Next implementation gates
1. Run unit tests in the isolated checkout.
2. Obtain an authorized TGStat API Stat token, confirm search entitlement and quotas.
3. Execute one query with `--limit 5`; inspect catalog and JSONL snapshots.
4. Add source-specific analytics tab in the advisor and historical charts.
5. Implement authorized Telemetr adapter and cross-provider comparisons with provenance.
6. Integrate verified Telegram Collector IDs and explicit research authorization.
