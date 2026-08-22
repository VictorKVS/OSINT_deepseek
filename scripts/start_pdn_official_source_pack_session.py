from __future__ import annotations

import json
import time
import webbrowser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACK = REPO_ROOT / "config" / "pdn_official_source_pack.json"
SESSION = REPO_ROOT / ".runtime" / "pdn_official_source_pack_session.json"


def main() -> int:
    payload = json.loads(PACK.read_text(encoding="utf-8"))
    documents = payload["documents"]
    started_epoch = int(time.time())
    SESSION.parent.mkdir(parents=True, exist_ok=True)
    session = {
        "pack_id": payload["pack_id"],
        "started_epoch": started_epoch,
        "documents": [
            {
                "document_id": item["document_id"],
                "source_url": item["publication_anchor"]["url"],
                "source_id": item["publication_anchor"]["source_id"],
                "trust_tier": item["publication_anchor"]["trust_tier"],
            }
            for item in documents
        ],
    }
    SESSION.write_text(json.dumps(session, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("PDN OFFICIAL SOURCE PACK SESSION STARTED")
    print(f"started_epoch={started_epoch}")
    print("Opening exact A0 publication pages in Российская газета...")
    for item in documents:
        webbrowser.open(item["publication_anchor"]["url"], new=2)
    print()
    print("For each opened page: Ctrl+S -> save as Webpage/HTML into Downloads.")
    print("Do not save from GARANT for this pass.")
    print("After all four pages are saved, run RUN_PDN_OFFICIAL_SOURCE_PACK_INVENTORY.cmd")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
