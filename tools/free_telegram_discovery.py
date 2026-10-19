#!/usr/bin/env python3
"""Free, opt-in public Telegram channel discovery via Telegram's official user API.

Requires an authorized Telethon user session. No paid analytics service, no bots
added as admins, and no private/invite-only channel collection.
"""
import argparse
import asyncio
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

HANDLE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{4,31}$")
FIELDS = ("channel_id","username","title","url","language","topics","discovered_from","discovered_at_utc","verified_at_utc","status","subscribers","avg_views","posts_30d","original_posts_30d","evidence_links","validated_skills","notes")

def registry_read(path):
    if not path.exists(): return {}
    obj=json.loads(path.read_text(encoding="utf-8-sig"))
    records=obj.get("channels",[]) if isinstance(obj,dict) else obj
    return {str(x["channel_id"]):x for x in records if isinstance(x,dict) and x.get("channel_id")}

def persist(path,records):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(".tmp")
    temp.write_text(json.dumps({"channels":sorted(records.values(),key=lambda x:x["channel_id"])},ensure_ascii=False,indent=2),encoding="utf-8")
    temp.replace(path)

def candidate(entity,topic,now):
    username=getattr(entity,"username",None)
    if not username or not HANDLE.fullmatch(username):return None
    if not getattr(entity,"broadcast",False):return None
    row={k:"" for k in FIELDS}
    row.update(channel_id=username.lower(),username=username,
        title=str(getattr(entity,"title",username))[:500],url="https://t.me/"+username,
        topics=topic[:200],discovered_from="telegram:contacts.SearchRequest",
        discovered_at_utc=now,status="candidate",
        notes="Public Telegram search result; content and reliability not verified")
    return row

async def discover(args):
    try:
        from telethon import TelegramClient, functions
    except ImportError:
        raise RuntimeError("Install optional dependency: python -m pip install telethon")
    api_id=os.getenv("TELEGRAM_API_ID","").strip()
    api_hash=os.getenv("TELEGRAM_API_HASH","").strip()
    if not api_id.isdigit() or not api_hash:
        raise RuntimeError("Set TELEGRAM_API_ID and TELEGRAM_API_HASH in environment")
    session=Path(args.session).expanduser().resolve()
    if not session.exists() and not args.allow_new_session:
        raise RuntimeError("Session not found. Use --allow-new-session to authorize an account interactively.")
    session.parent.mkdir(parents=True,exist_ok=True)
    records=registry_read(args.registry)
    snapshots=[]
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    async with TelegramClient(str(session),int(api_id),api_hash) as client:
        if not await client.is_user_authorized():
            if not args.allow_new_session:
                raise RuntimeError("Session not authorized; rerun with --allow-new-session")
            await client.start()
        for query in args.query:
            if len(query.strip())<3:raise RuntimeError("Query must contain at least 3 characters")
            response=await client(functions.contacts.SearchRequest(q=query,limit=args.limit))
            for entity in getattr(response,"chats",[]):
                row=candidate(entity,query,now)
                if not row:continue
                key=row["channel_id"]
                old=records.get(key)
                if old:
                    old.update({k:row[k] for k in ("username","title","url")})
                    topics=old.get("topics","").split(";")
                    if query not in topics:old["topics"]=";".join(filter(None,[old.get("topics",""),query]))
                    row=old
                else:records[key]=row
                # ID is evidence for future identity reconciliation, not an identity-verification claim.
                snapshots.append({"observed_at_utc":now,"provider":"telegram","method":"contacts.SearchRequest",
                    "channel_id":key,"telegram_id":getattr(entity,"id",None),"query":query,
                    "subscribers":None,"avg_views":None})
            if args.pause:await asyncio.sleep(args.pause)
    persist(args.registry,records)
    args.snapshots.parent.mkdir(parents=True,exist_ok=True)
    with args.snapshots.open("a",encoding="utf-8") as stream:
        for record in snapshots:stream.write(json.dumps(record,ensure_ascii=False)+"\n")
    print(f"Telegram search: {len(snapshots)} observations; {len(records)} channels in registry")
    print(f"Registry: {args.registry}\nSnapshots: {args.snapshots}")

def main():
    parser=argparse.ArgumentParser(description="Free Telegram public-channel discovery for ALINA")
    parser.add_argument("--query",action="append",required=True,help="Repeat to search multiple topics")
    parser.add_argument("--limit",type=int,default=20)
    parser.add_argument("--pause",type=float,default=1.0)
    parser.add_argument("--session",default="secrets/alina_telegram")
    parser.add_argument("--allow-new-session",action="store_true")
    parser.add_argument("--registry",type=Path,default=Path("data/telegram/channel_registry.json"))
    parser.add_argument("--snapshots",type=Path,default=Path("out/telegram_channel_catalog/telegram_discovery_snapshots.jsonl"))
    args=parser.parse_args()
    if not 1<=args.limit<=100 or not 0<=args.pause<=60:parser.error("Invalid limit or pause")
    try:asyncio.run(discover(args))
    except (RuntimeError,ValueError) as error:
        print("ERROR:",error,file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":main()
