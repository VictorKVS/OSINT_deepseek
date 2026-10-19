# ALINA Advisor — local service (Stage 2)

Implemented: stdlib-only loopback HTTP service and research advisor UI integration.

## Start
From repository root (in a separate checkout of `feature/osint-intelligence-center-ui`):
```powershell
python tools/telegram_channel_catalog.py --input data/telegram/osint_candidates.csv --registry data/telegram/channel_registry.json --out out/telegram_channel_catalog
python tools/alina_research_server.py --port 8765
```
Open `http://127.0.0.1:8765/advisor.html` — **not** `file://` — to use the API. The server listens only on `127.0.0.1`.

API:
- `GET /api/health` -> status, collector_connected=false, rag_mode=local_lexical
- `GET /api/channels` -> persisted channel registry, falling back to CSV seed
- `POST /api/research` with JSON `{"topic":"OSINT Telegram","goal":"skills","language":"any","threshold":20,"limit":10}` -> source-cited lexical retrieval, queries, explainable channel shortlist. No external calls or collection.

## Retrieval limitations
The initial knowledge file `data/telegram/advisor_knowledge.json` contains three short **manually prepared summaries** referencing local architecture documents. They are not direct quotations from those documents. This is source-referenced lexical search, not semantic embedding RAG. For evidence-grade RAG, ingest exact versioned document passages, offsets, hashes and retrieval metadata.

## Safety and trust
- The service reads local files and serves UI only; no Telegram credentials, session or network collector integration.
- No API route triggers collection.
- Proposed channels are not necessarily verified.
- Scores are heuristics and do not prove source quality.
- Loopback binding prevents ordinary remote access, but there is no authentication: do not expose via proxy/tunnel or deploy on public networks.
- CSV/JSON import should only include data you are authorized to process.
- No client data flows into ALINA.

## Tests
```powershell
python -m unittest discover -s tests -p "test_alina_research_server.py" -v
```

## Next gates
1. Test service on local Windows environment and confirm existing registry is read.
2. Add stable Telegram numeric ID resolver and authorized collector adapter with checkpoints.
3. Integrate versioned document fragments with a vector index, hybrid retrieval, exact citations and injection-resistant tool boundaries.
4. Add durable research job queue, review decisions, explicit authorization and safe collection policy.
5. Add historical ranking snapshots and exports.
