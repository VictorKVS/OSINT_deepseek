# TF-0014 — Verified legacy Telethon reader baseline

## RU

### Date
2026-08-12

### Stage / milestone
Восстановление ранее рабочего Telegram-контура и фиксация его как проверенного fallback / donor baseline.

### Trigger / problem
TDLib PoC на Windows доходил до `connectionStateConnecting`, но не мог подключиться к Telegram без системного VPN. После запуска AmneziaVPN системный TCP-доступ к `telegram.org:443` стал успешным. Старый Telethon reader снова подключился и прочитал реальные сообщения каналов.

Дополнительно был найден legacy-дефект: русский текст в `simple_reader.py` был сохранён как mojibake, а regex для русских слов был повреждён. После исправления regex и проверки через regression-test чтение сообщений восстановлено.

### Decision
Сохранить очищенную Telethon-реализацию в `legacy/telegram/simple_reader.py` как append-only verified fallback/reference implementation.

TDLib остаётся целевым PoC-направлением. Legacy Telethon reader не заменяет TDLib архитектурно, а служит:
- доказательством работоспособности Telegram collection path;
- fallback для live-проверок;
- donor/reference при переносе функций в TDLib;
- сравнительным baseline для network/auth/content tests.

### WHY
Live evidence подтвердило:
- AmneziaVPN route: PASS;
- `Test-NetConnection telegram.org -Port 443`: PASS через `AmneziaVPN`;
- сохранённая Telethon session: PASS;
- чтение 4 каналов: PASS;
- лимит до 100 сообщений на канал применяется;
- русский text analysis regression-test: PASS;
- menu contract `0 = Выход`: PASS на уровне unit test.

### Commercial / reuse review
Telethon рассматривается только как external dependency / verified donor-fallback. Перед production/commercial reuse требуется отдельная license/dependency review.

VPN не встраивается в репозиторий. AmneziaVPN используется как внешний системный transport dependency для live PoC.

### Files/components affected
- `legacy/telegram/simple_reader.py`
- `tests/test_legacy_telegram_reader_text_analysis.py`
- `tests/test_legacy_telegram_reader_menu.py`
- `Tree_F/TF-0014_2026-08-12_VERIFIED_LEGACY_TELETHON_READER_BASELINE.md`

### Acceptance test / evidence
1. Russian analyzer test accepts Cyrillic and Latin words.
2. Menu test requires readable Russian labels.
3. Exit command is `0`, not `5`.
4. Exit calls disconnect and terminates without traceback.
5. Live validation remains operator-side after `git pull`.

### Result
PARTIAL — repository baseline recorded; fresh pull + local regression + live Telegram run still required.

### New risks
- Local legacy `config.yaml` may contain secrets and MUST NOT be committed.
- `.session` files MUST NOT be committed.
- VPN dependency changes runtime network assumptions.
- Legacy and TDLib paths can drift unless behavior contracts are kept explicit.

### Registry changes
Added verified legacy Telegram fallback baseline.

### Next action / next reuse-review gate
Pull latest `main`, run focused legacy tests, then perform live run through AmneziaVPN. If PASS, close TF-0014 and define migration contract from legacy Telethon collection semantics to TDLib.

---

## EN

### Date
2026-08-12

### Stage / milestone
Recovery of the previously working Telegram path and preservation as a verified fallback / donor baseline.

### Trigger / problem
The TDLib PoC on Windows reached `connectionStateConnecting` but could not reach Telegram without a system VPN. After enabling AmneziaVPN, system TCP access to `telegram.org:443` succeeded. The legacy Telethon reader connected again and retrieved real channel messages.

A legacy defect was also confirmed: Russian UI text had been stored as mojibake and the Cyrillic word regex was corrupted. The regex was repaired and covered by a regression test.

### Decision
Preserve a cleaned Telethon implementation in `legacy/telegram/simple_reader.py` as an append-only verified fallback/reference implementation.

TDLib remains the target PoC direction. The legacy Telethon reader does not replace TDLib architecturally. It is retained as:
- evidence that the Telegram collection path works;
- a live-test fallback;
- a donor/reference for TDLib feature migration;
- a comparison baseline for network/auth/content tests.

### WHY
Live evidence established:
- AmneziaVPN route: PASS;
- `Test-NetConnection telegram.org -Port 443`: PASS through `AmneziaVPN`;
- persisted Telethon session: PASS;
- four-channel collection: PASS;
- per-channel limit up to 100 is applied;
- Russian text-analysis regression: PASS;
- menu contract `0 = Exit`: PASS at unit-test level.

### Commercial / reuse review
Telethon is retained only as an external dependency / verified donor-fallback. Production/commercial reuse requires a separate license/dependency review.

The VPN is not vendored into the repository. AmneziaVPN remains an external system transport dependency for live PoC work.

### Files/components affected
- `legacy/telegram/simple_reader.py`
- `tests/test_legacy_telegram_reader_text_analysis.py`
- `tests/test_legacy_telegram_reader_menu.py`
- `Tree_F/TF-0014_2026-08-12_VERIFIED_LEGACY_TELETHON_READER_BASELINE.md`

### Acceptance test / evidence
1. Russian analyzer test accepts Cyrillic and Latin words.
2. Menu test requires readable Russian labels.
3. Exit command is `0`, not `5`.
4. Exit disconnects and terminates without traceback.
5. Fresh operator-side validation is required after `git pull`.

### Result
PARTIAL — repository baseline recorded; fresh pull + local regression + live Telegram run remain required.

### New risks
- Local legacy `config.yaml` may contain secrets and MUST NOT be committed.
- `.session` files MUST NOT be committed.
- VPN dependency changes runtime network assumptions.
- Legacy and TDLib paths can drift unless behavior contracts remain explicit.

### Registry changes
Added verified legacy Telegram fallback baseline.

### Next action / next reuse-review gate
Pull latest `main`, run focused legacy tests, then perform a live run through AmneziaVPN. On PASS, close TF-0014 and define the migration contract from legacy Telethon collection semantics to TDLib.
