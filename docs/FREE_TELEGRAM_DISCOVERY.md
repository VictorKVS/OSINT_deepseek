# Бесплатный Telegram Discovery для FATHER OSINT

Реализован альтернативный поиск **публичных Telegram-каналов** через официальный Telegram API (Telethon). Это не TGStat, не платный API и не расширенная аналитика собственного канала.

## Что реально реализовано
- Тематический поиск `contacts.SearchRequest` по нескольким ключевым словам
- Отбор только публичных broadcast-каналов с username
- Сохранение кандидатов в `data/telegram/channel_registry.json`
- Снимки источника, даты, запроса и Telegram numeric ID в `out/telegram_channel_catalog/telegram_discovery_snapshots.jsonl`
- Совместимость с существующим `GET /api/channels` и советником Алины
- Ограничения запросов, без автоматического обхода приватных сообществ

**Не реализовано:** полная история публикаций, оценка просмотров, TGStat-аналитика, бот-детект, граф репостов, эмбеддинги/RAG. Telegram SearchRequest не гарантирует полноту выдачи и не предоставляет те же метрики, что TGStat.

## Подключение
Получите собственные `api_id` и `api_hash` на https://my.telegram.org/ (API development tools). Не отправляйте их в чат и не коммитьте в GitHub. Telethon: https://docs.telethon.dev/

```powershell
Set-Location 'G:\1\OSINT_ALINA_PREVIEW'
python -m pip install telethon
$env:TELEGRAM_API_ID = Read-Host 'Telegram API ID'
$env:TELEGRAM_API_HASH = Read-Host 'Telegram API hash'
python tools/free_telegram_discovery.py --query OSINT --query форензика --limit 10 --allow-new-session
Remove-Item Env:TELEGRAM_API_ID
Remove-Item Env:TELEGRAM_API_HASH
```

First run may ask for the Telegram login code and 2FA in the local terminal. Subsequent runs can omit `--allow-new-session`. Session is stored under `secrets/` relative to the working directory. **Keep this directory out of version control and backups shared with others**. Prefer a separate restricted directory and pass `--session` explicitly. Never share `.session` files.

The Telegram API may be inaccessible from the user's network; this adapter does not configure a proxy or claim VPN anonymity.

## Test
```powershell
python -m unittest discover -s tests -p "test_free_telegram_discovery.py" -v
```

## Next
Add authorized post-history collection and dated engagement metrics; validate discovered entities using Telegram IDs, keep immutable evidence references and a separate quality score. Do not equate popularity with source credibility.
