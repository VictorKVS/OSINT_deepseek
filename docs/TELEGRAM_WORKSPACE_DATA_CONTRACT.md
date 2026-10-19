# Telegram Workspace — data contract and acceptance checks

Status: implemented browser UI + local JSON import. No live Telegram collector connection.

## Import contract v0.1
UTF-8 JSON object with arrays `channels` and `posts`. Required:
- channel: `id` (unique string), `title` (string). Optional `username`.
- post: `id` (unique string), `channel_id` (must refer to a channel), `published_at` (ISO-8601 timestamp), `text` (string).
- optional post `url` (http/https URL), `skills` (array of candidate skill names).

Example:
```json
{
  "channels": [
    {"id": "research-1", "title": "Учебный источник", "username": "@example"}
  ],
  "posts": [
    {
      "id": "research-1:101",
      "channel_id": "research-1",
      "published_at": "2026-10-18T08:00:00Z",
      "text": "Учебная публикация о поиске первоисточника",
      "url": "https://example.org/post/101",
      "skills": ["Проверка первоисточника"]
    }
  ]
}
```

## Browser behavior
- UI opens without external services; synthetic demonstration records are visibly labeled.
- JSON is read locally, never transmitted by this page.
- Input constraints: maximum 10 MB file, 2000 channels, 20000 posts, 200000 characters per post.
- IDs are unique; post channel references and timestamps are validated.
- Imported text is HTML-escaped; links are restricted to http/https.
- Switching channel updates posts, timeline and skill candidates.
- Wave view is **publication counts by hour** only. It does not infer actual forwarding or causal propagation.
- All imported skill names are **candidates**, not verified agent capabilities.
- Clearing import restores synthetic demonstration data.

## Next integration contract (T2)
Build a read-only adapter from an authorized collector export to this schema; do not modify Telegram sessions or collector configuration. Record acquisition timestamps, channel IDs, native message IDs, original URLs, media references, content hashes and collection run ID. Add an evidence store and source verification before claiming provenance. Confirm network route/VPN policy and explicit channel scope before collection.

## Manual acceptance
1. Open `web/osint-intelligence-center/telegram.html` in a browser.
2. Confirm synthetic-data banner, two example channels and three example posts.
3. Switch channel; confirm filtered posts and counts.
4. Switch to Waves and Skills; confirm counts and candidate-only wording.
5. Import a UTF-8 JSON document matching the example; confirm imported-data banner.
6. Import malformed JSON; confirm validation error and no replacement of previous data.
7. Click Reset; confirm demo data returns.
8. Verify no network collection is initiated by UI.

## Separation
ALINA LAB is permanent. B2B deployment data and credentials must remain segregated. See `docs/ALINA_LAB_B2B_BOUNDARY.md`.
