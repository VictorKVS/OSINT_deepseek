#!/usr/bin/env python3
"""ALINA local research service: registry + grounded lexical retrieval. No external network."""
import argparse
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web" / "osint-intelligence-center"
REGISTRY = ROOT / "data" / "telegram" / "channel_registry.json"
SEED = ROOT / "data" / "telegram" / "osint_candidates.csv"
KNOWLEDGE = ROOT / "data" / "telegram" / "advisor_knowledge.json"
TOKENS = re.compile(r"[^\W_]+", re.UNICODE)

def tokenize(value):
    return [x for x in TOKENS.findall(str(value).casefold()) if len(x) >= 3]

def channels():
    if REGISTRY.exists():
        data = json.loads(REGISTRY.read_text(encoding="utf-8-sig"))
        rows = data.get("channels", []) if isinstance(data, dict) else data
    elif SEED.exists():
        import csv
        with SEED.open(encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
    else:
        rows = []
    return [dict(r) for r in rows if isinstance(r, dict)][:10000]

def knowledge():
    if not KNOWLEDGE.exists():
        return []
    raw = json.loads(KNOWLEDGE.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, list):
        raise ValueError("Knowledge must be a list")
    docs = []
    for d in raw[:2000]:
        if not isinstance(d, dict) or not all(isinstance(d.get(k), str) for k in ("id", "title", "text", "source")):
            continue
        docs.append({k: d[k][:30000] for k in ("id", "title", "text", "source")})
    return docs

def retrieve(topic, docs, limit=5):
    q = Counter(tokenize(topic))
    corpus = [Counter(tokenize(d["title"] + " " + d["text"])) for d in docs]
    df = Counter(t for counts in corpus for t in counts)
    found = []
    for d, counts in zip(docs, corpus):
        score = sum(min(q[t], counts[t]) * (1 + math.log((len(docs) + 1) / (df[t] + 1))) for t in q)
        if score > 0:
            found.append({"id": d["id"], "title": d["title"], "source": d["source"],
                          "excerpt": d["text"][:900], "score": round(score, 4)})
    return sorted(found, key=lambda d: (-d["score"], d["id"]))[:limit]

def build(topic, goal="skills", language="any", limit=10, threshold=60):
    topic = str(topic).strip()[:500]
    if not topic:
        raise ValueError("Topic is required")
    docs = retrieve(topic, knowledge())
    rows = channels()
    terms = set(tokenize(topic))
    proposals = []
    for c in rows:
        if language != "any" and c.get("language") != language:
            continue
        channel_id = str(c.get("channel_id") or c.get("id") or "")
        if not channel_id:
            continue
        matched = sorted(terms & set(tokenize(" ".join(str(c.get(k) or "") for k in ("title", "topics", "notes")))))
        relevance = round(60 * len(matched) / max(1, len(terms)))
        verified = 20 if c.get("status") == "verified" else 0
        evidence = 10 if c.get("verified_at_utc") and positive(c.get("evidence_links")) else 0
        metrics = 10 if c.get("verified_at_utc") and numeric(c.get("subscribers")) and numeric(c.get("posts_30d")) else 0
        score = relevance + verified + evidence + metrics
        proposals.append({"channel_id": channel_id, "title": c.get("title", ""),
                          "username": c.get("username", ""), "status": c.get("status", "candidate"),
                          "score": score, "matched_terms": matched,
                          "reasons": {"relevance": relevance, "verified_identity": verified,
                                      "evidence": evidence, "dated_metrics": metrics},
                          "discovered_from": c.get("discovered_from", ""),
                          "verified_at_utc": c.get("verified_at_utc", "")})
    proposals.sort(key=lambda x: (-x["score"], x["channel_id"]))
    proposals = [p for p in proposals if p["score"] >= threshold][:limit]
    base = [topic, topic + " Telegram", topic + " OSINT", topic + " site:t.me"]
    for d in docs:
        base.append(topic + " " + d["title"][:80])
    queries = list(dict.fromkeys(base))[:12]
    return {"schema_version": "0.2", "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "topic": topic, "goal": goal, "language": language, "threshold": threshold,
            "catalog_size": len(rows), "knowledge_size": len(knowledge()),
            "retrieval": {"method": "local lexical overlap with source references", "citations": docs},
            "queries": queries, "suggested_channels": proposals,
            "execution": "not_started", "approval": "required_before_collection",
            "warnings": ["No Telegram collection or live verification performed.",
                         "Retrieval is lexical, not semantic embedding RAG or an LLM.",
                         "Unverified candidates and missing observations are not facts."]}

def numeric(v):
    try:
        return v is not None and str(v).strip() != "" and float(v) >= 0
    except (TypeError, ValueError):
        return False

def positive(v):
    return numeric(v) and float(v) > 0

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def send_json(self, obj, status=200):
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/api/channels":
            try:
                self.send_json({"channels": channels(), "source": "local_registry_or_seed"})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return
        if path == "/api/health":
            self.send_json({"status": "ok", "collector_connected": False, "rag_mode": "local_lexical"})
            return
        if path.startswith("/api/"):
            self.send_json({"error": "not_found"}, 404)
            return
        super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != "/api/research":
            self.send_json({"error": "not_found"}, 404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 10000:
                self.send_json({"error": "invalid_payload_size"}, 400)
                return
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError("Object expected")
            language = str(data.get("language", "any"))
            if language not in ("any", "ru", "en"):
                raise ValueError("Unsupported language")
            threshold = int(data.get("threshold", 60))
            limit = int(data.get("limit", 10))
            if not 0 <= threshold <= 100 or not 1 <= limit <= 100:
                raise ValueError("Invalid threshold or limit")
            self.send_json(build(data.get("topic", ""), str(data.get("goal", "skills"))[:60], language, limit, threshold))
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            self.send_json({"error": str(e)}, 400)
        except Exception as e:
            self.send_json({"error": "internal_error"}, 500)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Port out of range")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"ALINA Research Advisor: http://127.0.0.1:{args.port}/advisor.html", flush=True)
    print("Loopback only. No Telegram collection or LLM calls.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
