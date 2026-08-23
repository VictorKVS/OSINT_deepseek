from __future__ import annotations

import json
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.benchmark_152_prebuilt_mcp_db import DB_PATH
from scripts.benchmark_152_reuse import TARGET_NUMBER, TARGET_TITLE_MARKER

REPORT = REPO_ROOT / "reports" / "pdn_live" / "GATE_152_PREBUILT_DB_SOURCE_IDENTITY.json"
EXPECTED_PRAVO_ND = "102108261"  # 152-FZ official pravo.gov.ru document identity
KNOWN_149_PRAVO_ND = "102108264"
ND_RE = re.compile(r"(?:[?&])nd=(\d+)")


def _extract_nd(url: object) -> str | None:
    match = ND_RE.search(str(url or ""))
    return match.group(1) if match else None


def main() -> int:
    if not DB_PATH.is_file():
        print(f"PREBUILT_DB_MISSING: {DB_PATH}")
        return 2

    conn = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        law = conn.execute(
            "SELECT id, title, identifier, source_url, status, last_updated, provision_count "
            "FROM laws WHERE identifier = ? OR title LIKE ? ORDER BY provision_count DESC LIMIT 1",
            (TARGET_NUMBER, f"%{TARGET_TITLE_MARKER}%"),
        ).fetchone()
        if law is None:
            print("152_FZ_NOT_FOUND_IN_PREBUILT_DB")
            return 2

        article_rows = conn.execute(
            "SELECT article, title FROM provisions WHERE law_id = ? AND article IN ('2','3','4') ORDER BY id",
            (law["id"],),
        ).fetchall()
        article_titles = {str(row["article"]): str(row["title"] or "") for row in article_rows}

        observed_nd = _extract_nd(law["source_url"])
        metadata_identity_pass = (
            TARGET_NUMBER.casefold() in str(law["identifier"] or "").casefold()
            and TARGET_TITLE_MARKER in str(law["title"] or "").casefold()
        )
        source_identity_match = observed_nd == EXPECTED_PRAVO_ND

        article3 = article_titles.get("3", "").casefold()
        article4 = article_titles.get("4", "").casefold()
        foreign_149_signature = (
            "принципы" in article3
            and "правового регулирования" in article3
            and "информац" in article3
            and "законодательство" in article4
            and "информац" in article4
        )
        identity_collision = bool(
            metadata_identity_pass
            and not source_identity_match
            and observed_nd is not None
        )
        likely_misbound_to = (
            "149-ФЗ / nd=102108264"
            if observed_nd == KNOWN_149_PRAVO_ND or foreign_149_signature
            else None
        )

        content_reuse_allowed = not identity_collision
        gate_status = "PASS" if content_reuse_allowed else "BLOCKED_IDENTITY_COLLISION"
        adoption_decision = (
            "REFERENCE_KB_CONTENT_CANDIDATE"
            if content_reuse_allowed
            else "REUSE_INFRASTRUCTURE_CODE_ONLY__QUARANTINE_PREBUILT_CONTENT"
        )

        result = {
            "record_type": "PREBUILT_REFERENCE_DB_SOURCE_IDENTITY_GATE",
            "target_identifier": TARGET_NUMBER,
            "database_path": DB_PATH.relative_to(REPO_ROOT).as_posix(),
            "law": dict(law),
            "source_identity": {
                "expected_pravo_nd": EXPECTED_PRAVO_ND,
                "observed_pravo_nd": observed_nd,
                "source_identity_match": source_identity_match,
                "metadata_identity_pass": metadata_identity_pass,
                "identity_collision": identity_collision,
                "likely_misbound_to": likely_misbound_to,
            },
            "content_signatures": {
                "article_titles": article_titles,
                "foreign_149_signature": foreign_149_signature,
            },
            "decision": {
                "gate_status": gate_status,
                "content_reuse_allowed": content_reuse_allowed,
                "adoption_decision": adoption_decision,
                "legal_truth_promoted": False,
            },
        }

        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()
        print(f"EXPECTED_PRAVO_ND={EXPECTED_PRAVO_ND}")
        print(f"OBSERVED_PRAVO_ND={observed_nd or ''}")
        print(f"SOURCE_IDENTITY_MATCH={str(source_identity_match).lower()}")
        print(f"IDENTITY_COLLISION={str(identity_collision).lower()}")
        print(f"LIKELY_MISBOUND_TO={likely_misbound_to or ''}")
        print(f"CONTENT_REUSE_ALLOWED={str(content_reuse_allowed).lower()}")
        print(f"ADOPTION_DECISION={adoption_decision}")
        return 0 if content_reuse_allowed else 3
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
