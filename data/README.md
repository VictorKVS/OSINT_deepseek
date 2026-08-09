# Data

This directory contains development fixtures and local runtime data references.

## DEV chain

```text
prepared fixture
    ↓
FixtureCollector
    ↓
Material
    ↓
MaterialStore
    ↓
MaterialPackage
```

`data/dev/` is deterministic input for development and acceptance testing. Fixture content is test data, not verified intelligence and not Knowledge Base content.

Production raw evidence/storage design is deferred to the PROD architecture gate.
