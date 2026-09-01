# External KB donor identity incident — Russian-Law-MCP / 152-FZ

Status: CONFIRMED DONOR DATA IDENTITY COLLISION / CONTENT QUARANTINED  
Scope: `@ansvar/russian-law-mcp@0.1.0` prebuilt `data/database.db`  
Decision: **REUSE INFRASTRUCTURE/CODE PATTERNS ONLY; DO NOT TRUST PREBUILT CONTENT WITHOUT INDEPENDENT VERIFICATION**

## 1. Evidence from the local benchmark

The prebuilt SQLite database itself is operational and fast:

- SQLite `quick_check = ok`;
- database size: 542,265,344 bytes;
- 12,393 rows in `laws`;
- 79,178 rows in `provisions`;
- 152-FZ hot-path provision retrieval: about 1.27 ms p50 and 1.51 ms p95 in the observed workstation run.

However, the row selected as `152-ФЗ / О персональных данных` is semantically bound to another official document identity.

Observed donor metadata:

- `id = fz-152-2006`;
- `identifier = 152-ФЗ`;
- `title = О персональных данных`;
- `source_url ... nd=102108264`.

The FATHER golden identity for 152-FZ is `pravo.gov.ru nd=102108261`.

`nd=102108264` is the official portal identity used for 149-FZ `Об информации, информационных технологиях и о защите информации`.

The donor provisions reinforce the same collision. Examples from the row labelled 152-FZ include titles characteristic of 149-FZ:

- article 3: `Принципы правового регулирования отношений в сфере информации...`;
- article 4: `Законодательство Российской Федерации об информации...`;
- article 5: `Информация как объект правовых отношений`;
- later rows cover search engines, news aggregators, social networks, access blocking, and similar 149-FZ subject matter.

Therefore this is not explainable only by `base 2006 vs amended 2026` version drift. It is a **cross-document identity collision**.

## 2. Why metadata-only identity PASS was wrong

The initial benchmark checked:

`identifier == 152-ФЗ` + title contains `персональных данных`.

That allowed a false PASS even though the source locator and content belonged to another act.

New invariant:

> Metadata identity is necessary but never sufficient for donor adoption.

For a donor legal record, identity acceptance requires at least:

1. canonical identifier match;
2. title/authority/date compatibility;
3. authoritative source locator identity match when available;
4. semantic fingerprint/golden-structure compatibility for sampled high-value records.

Any mismatch at the authoritative source locator boundary is fail-closed.

## 3. Adoption decision

### Allowed to reuse

- SQLite schema patterns;
- FTS5/search architecture;
- indexing/query patterns;
- packaging/distribution pattern;
- hot-path performance techniques;
- update/check workflow ideas after independent review.

### Quarantined / not allowed as trusted input

- prebuilt law text;
- citations generated from that prebuilt content;
- currentness/status claims;
- cross-references;
- legal stance construction;
- automatic KB bootstrap into canonical FATHER knowledge.

Status code:

`REUSE_INFRASTRUCTURE_CODE_ONLY__QUARANTINE_PREBUILT_CONTENT`

## 4. Production rule added

`RUN_BENCHMARK_152_PREBUILT_DB.cmd` now runs an explicit source-identity gate after the benchmark.

For 152-FZ the gate expects:

`pravo.gov.ru nd=102108261`

If the donor record resolves to another `nd`, the runner returns a blocked state and must not treat the donor content as accepted reference data.

The current observed `nd=102108264` is additionally recognized as a 149-FZ collision signature.

## 5. Architectural consequence

The target data architecture is now:

```text
External corpus / KB
        ↓
DONOR IDENTITY GATE
        ↓
source locator + metadata + semantic fingerprint
        ↓
PASS ----------------------→ candidate bootstrap/reference data
  |
  └─ FAIL → QUARANTINE
              ↓
       code/schema patterns may still be reused
```

A donor can therefore be fast and well engineered while its dataset remains untrusted. Performance and trust are independent dimensions.

## 6. Next scale gate

Before adopting any large external legal corpus or KB as FATHER input:

1. sample high-value golden documents;
2. verify source locator identities;
3. compare canonical structure/article fingerprints;
4. measure collision rate;
5. only then choose `REUSE / WRAP / REFERENCE / REJECT` for the **data**, separately from the code.

No bulk donor import may bypass this gate.
