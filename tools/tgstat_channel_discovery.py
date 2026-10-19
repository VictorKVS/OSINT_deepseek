#!/usr/bin/env python3
"""Authorized TGStat API adapter for ALINA. No scraping, no Telegram sessions."""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://api.tgstat.ru"
HANDLE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{4,31}$")
FIELDS = ("channel_id","username","title","url","language","topics","discovered_from","discovered_at_utc","verified_at_utc","status","subscribers","avg_views","posts_30d","original_posts_30d","evidence_links","validated_skills","notes")

def get(path, params, token, opener=urllib.request.urlopen):
    query = urllib.parse.urlencode({**params, "token": token})
    request = urllib.request.Request(BASE + path + "?" + query, headers={"User-Agent":"FATHER-ALINA-OSINT/0.1","Accept":"application/json"})
    try:
        with opener(request, timeout=20) as response:
            data=json.loads(response.read(2_000_000).decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError("TGStat HTTP "+str(exc.code)) from None
    except urllib.error.URLError as exc:
        raise RuntimeError("TGStat connection failed: "+str(exc.reason)) from None
    if not isinstance(data,dict) or data.get("status")!="ok":
        raise RuntimeError("TGStat API returned an error; check access, quota and parameters")
    return data.get("response",{})

def valid_handle(value):
    handle=str(value or "").lstrip("@")
    return handle if HANDLE.fullmatch(handle) else ""

def number(value):
    if isinstance(value,bool):return ""
    try:
        v=int(value)
        return str(v) if v>=0 else ""
    except (TypeError,ValueError):return ""

def row_from_item(item, query, stamp):
    if not isinstance(item,dict) or item.get("peer_type") not in ("channel",None):
        return None
    handle=valid_handle(item.get("username"))
    if not handle:
        return None
    row={k:"" for k in FIELDS}
    row.update(channel_id=handle.lower(),username=handle,title=str(item.get("title") or handle)[:500],
        url="https://t.me/"+handle,topics=query[:200],discovered_from="tgstat:channels/search",
        discovered_at_utc=stamp,status="candidate",subscribers=number(item.get("participants_count")),
        notes="External catalog candidate; not Telegram-identity verified")
    return row

def read_registry(path):
    if not path.exists():return {}
    obj=json.loads(path.read_text(encoding="utf-8-sig"))
    rows=obj.get("channels",[]) if isinstance(obj,dict) else obj
    return {str(r["channel_id"]):{k:str(r.get(k,"") or "") for k in FIELDS} for r in rows if isinstance(r,dict) and r.get("channel_id")}

def save_registry(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(".tmp")
    tmp.write_text(json.dumps({"channels":sorted(rows.values(),key=lambda r:r["channel_id"])},ensure_ascii=False,indent=2),encoding="utf-8")
    tmp.replace(path)

def append_snapshots(path, snapshots):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as f:
        for row in snapshots:
            f.write(json.dumps(row,ensure_ascii=False)+"\n")

def run(args, token):
    stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    registry=read_registry(args.registry)
    snapshots=[]
    results=[]
    for query in args.query:
        query=query.strip()
        if len(query)<3:raise ValueError("Query must be at least 3 characters")
        payload=get("/channels/search",{"q":query,"peer_type":"channel","limit":args.limit,"search_by_description":1,"country":args.country},token)
        items=payload.get("items",[]) if isinstance(payload,dict) else []
        for item in items:
            row=row_from_item(item,query,stamp)
            if not row:continue
            key=row["channel_id"]
            if key in registry:
                existing=registry[key]
                for field in ("title","username","url","subscribers"):
                    if row[field]:existing[field]=row[field]
                if query not in existing["topics"].split(";"):
                    existing["topics"]=";".join(filter(None,[existing["topics"],query]))
                row=existing
            else:
                registry[key]=row
            results.append({"channel_id":key,"title":row["title"],"query":query,"source":"tgstat:channels/search"})
            snapshots.append({"observed_at_utc":stamp,"provider":"tgstat","method":"channels/search",
                "channel_id":key,"query":query,"tgstat_id":item.get("id"),"telegram_id":item.get("tg_id"),
                "subscribers":item.get("participants_count"),"citation_index":item.get("ci_index")})
        if args.pause and len(args.query)>1:time.sleep(args.pause)
    if args.stats:
        for key in list(dict.fromkeys(x["channel_id"] for x in results))[:args.max_stats]:
            row=registry[key]
            payload=get("/channels/stat",{"channelId":"@"+row["username"]},token)
            if not isinstance(payload,dict):continue
            if payload.get("peer_type") not in ("channel",None):continue
            subs=number(payload.get("participants_count"))
            reach=number(payload.get("avg_post_reach"))
            if subs:row["subscribers"]=subs
            if reach:row["avg_views"]=reach
            # Do not mark Telegram identity as verified based only on external analytics.
            snapshots.append({"observed_at_utc":stamp,"provider":"tgstat","method":"channels/stat",
                "channel_id":key,"subscribers":payload.get("participants_count"),
                "avg_post_reach":payload.get("avg_post_reach"),"err_percent":payload.get("err_percent"),
                "err24_percent":payload.get("err24_percent"),"er_percent":payload.get("er_percent"),
                "citation_index":payload.get("ci_index"),"mentions_count":payload.get("mentions_count"),
                "forwards_count":payload.get("forwards_count"),"daily_reach":payload.get("daily_reach")})
            if args.pause:time.sleep(args.pause)
    save_registry(args.registry,registry)
    append_snapshots(args.snapshots,snapshots)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps({"generated_at_utc":stamp,"provider":"tgstat",
        "queries":args.query,"results":results,"snapshots_written":len(snapshots),
        "warning":"External analytics are observations, not proof of source reliability or identity."},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"TGStat: {len(results)} results, {len(registry)} registry records, {len(snapshots)} snapshots")
    print(f"Registry: {args.registry}\nSnapshots: {args.snapshots}\nReport: {args.report}")

def main():
    p=argparse.ArgumentParser(description="Search public Telegram channels through official TGStat API")
    p.add_argument("--query",action="append",required=True,help="Repeat for multiple search topics")
    p.add_argument("--country",default="ru",help="TGStat country code; adjust to your plan")
    p.add_argument("--limit",type=int,default=20)
    p.add_argument("--stats",action="store_true",help="Fetch additional statistics (quota-consuming)")
    p.add_argument("--max-stats",type=int,default=10)
    p.add_argument("--pause",type=float,default=1.0)
    p.add_argument("--registry",type=Path,default=Path("data/telegram/channel_registry.json"))
    p.add_argument("--snapshots",type=Path,default=Path("out/telegram_channel_catalog/tgstat_snapshots.jsonl"))
    p.add_argument("--report",type=Path,default=Path("out/telegram_channel_catalog/tgstat_discovery_report.json"))
    args=p.parse_args()
    if not 1<=args.limit<=100 or not 0<=args.max_stats<=100 or not 0<=args.pause<=60:
        p.error("Invalid limits")
    token=os.getenv("TGSTAT_API_TOKEN","").strip()
    if not token:
        p.error("Set TGSTAT_API_TOKEN in the environment; never commit credentials")
    try:run(args,token)
    except (RuntimeError,ValueError) as exc:
        print("ERROR:",exc,file=sys.stderr);sys.exit(1)

if __name__=="__main__":main()
