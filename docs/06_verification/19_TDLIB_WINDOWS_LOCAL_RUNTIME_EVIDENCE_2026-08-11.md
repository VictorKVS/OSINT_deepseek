# TDLib Windows Local Runtime Evidence

**Date:** 2026-08-11  
**Scope:** local Windows x64 TDLib build and no-credential smoke test for POC-M5-001  
**Decision:** **PASS — LOCAL NATIVE RUNTIME VERIFIED; LIVE TELEGRAM AUTH STILL SEPARATE**

## 1. Source provenance

TDLib repository was cloned from the official upstream and the working tree was clean at build time.

```text
TDLib commit: 022d60202e446ad1287b9fb68e687c8a0760788b
Working tree: clean
Build configuration: Release / x64
```

## 2. Local toolchain evidenced

```text
Visual Studio Developer PowerShell: 18.9.0-insiders
MSVC compiler used by TDLib CMake configure: 19.51.36252
Windows SDK: 10.0.28000.0
CMake: 4.2.3
```

A separate minimal Windows C++ compile/link/run test was completed successfully before dependency and TDLib build.

## 3. Dependency state

The controlled local vcpkg instance contained:

```text
OpenSSL: 3.6.3
zlib: 1.3.2#2
gperf: 3.3
```

TDLib CMake configure resolved OpenSSL and zlib from `G:\1\father-tdlib\vcpkg\installed\x64-windows` and detected the exact TDLib Git state.

## 4. Build result

Target built:

```text
tdjson
```

Resulting binary:

```text
G:\1\father-tdlib\td\build\Release\tdjson.dll
Size: 27,013,120 bytes
SHA-256: D0BD83317A5BEE2C3758378F564C3C34FAE621166CD545E6B693665E690B8A8E
```

Runtime companion binaries copied by the build:

```text
libssl-3-x64.dll
SHA-256: FBA97683A660268C193CD1DE7D93977571BBB73CB9AB8F2E321052B82D9D3490

libcrypto-3-x64.dll
SHA-256: EF32A82F760FE017CF81A74CBB7DB9DB1A226E15D2259F05982C2F8D5373E505

z.dll
SHA-256: 33F05CC1D8153A6D07F7FC1CB3AF7A9824E9F8D266F2BA5DB51F8F06318C0C4F
```

## 5. No-credential native smoke test

A local Python ctypes smoke test was executed against the built DLL before any Telegram API credentials were supplied.

Observed result:

```text
[OK] tdjson.dll loaded
[OK] TDLib client created
[OK] TDLib client destroyed
TDLIB LOCAL RUNTIME: OK
```

TDLib itself reported:

```text
version = 1.8.66
commit_hash = 022d60202e446ad1287b9fb68e687c8a0760788b
authorizationStateWaitTdlibParameters
```

This is important because the running native library self-reported the same commit hash as the source tree used for the build.

## 6. Security interpretation

### SEC-2026-003

The previously open native-library provenance control now has concrete local evidence:

- exact official source commit recorded;
- local build performed from clean tree;
- exact `tdjson.dll` SHA-256 recorded;
- runtime library successfully loaded;
- runtime self-reported the same TDLib commit hash.

**State:** `CONTROLLED FOR THIS LOCAL POC BINARY`.

This does not approve arbitrary future `tdjson.dll` builds. Any replacement binary requires a new provenance/hash record.

## 7. What this PASS does not prove

This evidence does **not** yet prove:

- Telegram account authorization;
- API ID/hash handling under a real session;
- encrypted TDLib database lifecycle;
- public-channel resolution/history collection;
- restart/checkpoint behavior;
- rate/flood handling;
- multi-source isolation;
- live reliability/stress behavior;
- production readiness.

## 8. Next gate

The next step is `POC-TD-01 — controlled local Telegram authorization` using:

- the exact `tdjson.dll` above;
- the recorded SHA-256 gate;
- a non-empty local DB encryption key outside Git;
- API credentials outside Git;
- the existing FATHER TDLib PoC bootstrap;
- no live credentials in GitHub Actions.

Before the first live credential run, owner-side GitHub secret/push-protection settings that remain unverified should be checked, and Dependabot vulnerability alerts remain a separate repository-owner action.
