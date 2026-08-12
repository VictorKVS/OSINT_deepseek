# J-018 — M5 live Telegram path + Engineering Council establishment

**Date:** 2026-08-12  
**Stage:** Stage 07 / M5 Telegram Radar  
**Type:** POC / ARCHITECTURE / GOVERNANCE  
**Result:** PARTIAL PASS — live acquisition path proven; M5 integration not yet complete

## Trigger

The TDLib PoC reached `authorizationStateWaitPhoneNumber` but remained in `connectionStateConnecting` and timed out waiting for the authorization request response. Independent Windows network diagnostics showed that direct TCP connectivity to Telegram endpoints was failing even though DNS resolution and the ordinary default route were present.

A previously working Telethon collector was recovered from the legacy project to distinguish transport-code failure from network-path failure.

## Evidence obtained

### Network path

Before VPN:

```text
Test-NetConnection telegram.org -Port 443 → TcpTestSucceeded: False
curl https://telegram.org                 → timeout
Telethon connect                          → TimeoutError / ConnectionError
TDLib                                     → connectionStateConnecting / timeout
```

After enabling AmneziaVPN:

```text
InterfaceAlias       : AmneziaVPN
SourceAddress        : 100.71.91.158
TcpTestSucceeded     : True
```

This establishes that the primary blocker was the host/network path, not the basic Telegram collector logic.

### Legacy Telethon live acquisition

The recovered authorized Telethon session successfully connected through the working VPN route and read the configured public channels.

With `limit_per_channel: 100`, the observed text-message counts were:

```text
durov        97/100
telegram    100/100
meduzalive   89/100
tjournal     70/100
```

Total text messages processed in the observed run: **356**.

Counts lower than 100 reflect the reader counting text-bearing messages rather than claiming every returned Telegram object contains text; this is not yet an acceptance definition for the final M5 collector.

### Defects discovered and corrected

1. Legacy Cyrillic regex had mojibake and raised:

```text
re.error: bad character range
```

A regression test was added and the Russian/English word extraction regex was corrected.

2. Legacy console UI contained mojibake. A UTF-8-clean legacy reader was preserved as a verified fallback/reference component under:

```text
legacy/telegram/simple_reader.py
```

3. Menu contract was changed to `0 = Выход`, with clean disconnect behavior covered by test.

4. The legacy reader originally referenced old repository-relative config/session paths. It was changed to resolve local runtime `config.yaml` and `reader_session.session` adjacent to the legacy reader by default.

5. Local Telegram credentials/config are excluded from source control. Runtime secrets/session files remain operator-local and must not be committed.

## What is proven

```text
Windows host
   ↓
working VPN route
   ↓
Telegram reachable
   ↓
existing authorized Telethon session
   ↓
public channel acquisition
   ↓
100-object request scale demonstrated
   ↓
text analysis executes without previous Cyrillic regex failure
```

## What is NOT yet proven

This evidence does **not** mean M5 is DONE.

Still unproven or incomplete:
- final approved Telegram transport ADR;
- TDLib operational authorization under the now-working network path;
- whether a second candidate PoC materially changes the decision;
- common `TelegramTransport` contract implemented by approved adapters;
- Telegram message → canonical FATHER `Material` mapping;
- stable message/source IDs and full low-cost metadata contract;
- durable save before checkpoint advance;
- restart/reconciliation acceptance;
- FloodWait/429 behavior;
- per-source failure isolation under live transport;
- M5 security/operations review;
- end-to-end ResearchTask → Telegram → MaterialPackage → Analyst → Socrates live proof.

## Architecture decision direction

Telethon is now treated as a **verified fallback/reference implementation**, not automatically as the production winner.

TDLib remains a candidate primary transport pending live evidence under the corrected network path.

The next architecture step must not be another independent Telegram reader. The target boundary is:

```text
TelegramCollector
      ↓
TelegramTransport protocol
      ├── TDLibTransport
      └── TelethonTransport / verified fallback
      ↓
TelegramMessage DTO
      ↓
MaterialFactory
      ↓
Material + provenance + hash
```

## Senior review conclusion

The project has reached the point where additional transport debugging must justify why it blocks the higher-value integration path.

The next major proof should be:

```text
ResearchTask
  ↓
TelegramCollector
  ↓
real Telegram messages
  ↓
canonical Material records
  ↓
provenance + raw hash
  ↓
MaterialPackage
  ↓
Analyst
  ↓
Socrates
```

This, not merely successful Telegram login, is the M5 capability outcome.

## Engineering Council decision

An internal, extractable `engineering_council/` module is established to provide senior multidisciplinary review for material decisions.

Roles:
- Senior System / Solution Architect;
- Senior Software Engineer / Technical Lead;
- Senior Systems / Business Analyst;
- Senior Product Lead;
- Senior Project / Delivery Lead;
- Principal Engineering Critic / Red-Team Reviewer.

The Principal Critic is structurally independent from delivery ownership and must attack proposals with credible alternatives, falsification conditions and evidence-based blocking objections. Other roles must defend or revise their recommendations point-by-point.

The council is designed for later extraction into a separate repository/service and must not depend on internal `father_osint` Python objects for its generic review protocol.

Council contract: `engineering_council/README.md`.

## Risks changed

- **R3 transport/library fragility:** still OPEN; mitigated by verified fallback/reference evidence.
- **R13 mocks vs live behavior:** materially reduced for Telegram network/acquisition path because live evidence now exists.
- **R14 secrets/session leakage:** still OPEN for production; local git exclusion and adjacent runtime-file discipline reduce immediate repository risk.
- **Process overengineering:** remains controlled; the new council is explicitly gate-triggered and must not review routine edits.

## Commercial / reuse review

No new product path is promoted by this event alone. However, live acquisition evidence increases confidence that M5 can unlock the already registered Telegram-dependent product paths.

The transport boundary remains product-neutral.

## Next action

1. Re-run TDLib live authorization under the now-working network path only if it still changes the transport decision.
2. Principal Critic challenges whether GramJS PoC is still decision-relevant.
3. Define common Telegram transport/message contract.
4. Implement/prove Telegram → FATHER Material mapping.
5. Write M5 live acceptance tests around restart, rate/failure behavior, source isolation, checkpoint-after-save and provenance.
6. Produce transport ADR from measured evidence.

## Gate status

```text
M5 network reachability             PASS
legacy Telethon live fallback       PASS
100-request live acquisition        PASS
UTF-8 / regex regression            PASS
local config/session path contract  PASS (unit); LIVE PARTIAL
TDLib live under corrected network  PENDING
transport ADR                       PENDING
Telegram → Material                 PENDING
M5 end-to-end acceptance            PENDING

OVERALL M5                          ACTIVE / PARTIAL PASS
```
