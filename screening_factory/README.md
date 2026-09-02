# screening_factory package

Standard-library-only M3 kernel for repeatable, passive screening production.

Main entry points:

```python
ScreeningPlanner
AdapterRegistry
ScreeningFactoryRunner
MarkdownReportBuilder
HtmlDashboardBuilder
HashChainJournal
RecheckScheduler
```

The package ships no live provider credentials and performs no network access by itself. Real collection is introduced only through approved adapters.
