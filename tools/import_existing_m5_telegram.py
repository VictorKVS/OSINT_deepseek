#!/usr/bin/env python3
"""Read-only adapter: existing FATHER M5 Telegram materials -> ALINA channel registry.

Does not connect to Telegram, load credentials, copy raw messages or alter the source.
"""
import argparse
import datetime as dt
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

FIELDS=("channel_id","username","title","url","language","topics","discovered_from","discovered_at_utc","verified_at_utc","status","subscribers","avg_views","posts_30d","original_posts_30d","evidence_links","validated_skills","notes")
HANDLE=re.compile(r"^[A-Za-z][A-Za-z0-9_]{4,31}$")

def load(path):
    if not path.exists():return {}
    data=json.loads(path.read_text(encoding="utf-8-sig"))
    rows=data.get("channels",[]) if isinstance(data,dict) else data
    return {r["channel_id"]:r for r in rows if isinstance(r,dict) and r.get("channel_id")}

def scan(path):
    grouped=defaultdict(lambda:{"messages":set(),"views":[],"forwards":[],"title":"","username":"","first":"","last":"","material_refs":[]})
    total=0
    with path.open(encoding="utf-8-sig") as stream:
        for line_no,line in enumerate(stream,1):
            if not line.strip():continue
            item=json.loads(line)
            if item.get("source_type")!="telegram":continue
            metadata=item.get("metadata") or {}
            if not isinstance(metadata,dict):continue
            locator=str(item.get("source_locator") or "")
            parts=urlsplit(locator)
            username=parts.path.strip("/").split("/")[0] if parts.scheme=="https" and parts.netloc.lower()=="t.me" else ""
            if not HANDLE.fullmatch(username):continue
            message_id=str(metadata.get("message_id") or "")
            if not message_id:continue
            key=username.lower()
            entry=grouped[key]
            entry["username"]=username
            entry["title"]=str(item.get("title") or username)[:500]
            if message_id in entry["messages"]:continue
            entry["messages"].add(message_id)
            total+=1
            if len(entry["material_refs"])<10 and item.get("material_id"):entry["material_refs"].append(str(item["material_id"]))
            for field in ("views","forwards"):
                value=metadata.get(field)
                if type(value) is int and value>=0:entry[field].append(value)
            date=str(item.get("published_at") or "")
            if date:
                if not entry["first"] or date<entry["first"]:entry["first"]=date
                if not entry["last"] or date>entry["last"]:entry["last"]=date
    return grouped,total

def merge(registry,groups,stamp):
    snapshots=[]
    for key,entry in groups.items():
        row=registry.get(key)
        if row is None:
            row={field:"" for field in FIELDS}
            row.update(channel_id=key,username=entry["username"],title=entry["title"],
                url="https://t.me/"+entry["username"],discovered_from="father:m5_materials",
                discovered_at_utc=stamp,status="candidate",
                notes="Existing M5 evidence observations; channel reliability not independently verified")
            registry[key]=row
        # Do not overwrite prior ratings or independent verification.
        count=len(entry["messages"])
        snapshots.append({"observed_at_utc":stamp,"provider":"father_m5","method":"local_materials_jsonl",
            "channel_id":key,"observed_messages":count,"observed_views_count":len(entry["views"]),
            "observed_views_mean":round(sum(entry["views"])/len(entry["views"]),2) if entry["views"] else None,
            "observed_forwards_count":len(entry["forwards"]),
            "observed_forwards_sum":sum(entry["forwards"]) if entry["forwards"] else None,
            "earliest_published_at":entry["first"] or None,"latest_published_at":entry["last"] or None,
            "sample_material_ids":entry["material_refs"],
            "note":"Sample metrics from stored observations, not channel-wide audience analytics"})
    return snapshots

def run(source,registry_path,snapshot_path):
    if not source.is_file():raise FileNotFoundError(source)
    groups,total=scan(source)
    stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    registry=load(registry_path)
    snapshots=merge(registry,groups,stamp)
    registry_path.parent.mkdir(parents=True,exist_ok=True)
    temp=registry_path.with_suffix(".tmp")
    temp.write_text(json.dumps({"channels":sorted(registry.values(),key=lambda x:x["channel_id"])},ensure_ascii=False,indent=2),encoding="utf-8")
    temp.replace(registry_path)
    snapshot_path.parent.mkdir(parents=True,exist_ok=True)
    with snapshot_path.open("a",encoding="utf-8") as f:
        for snap in snapshots:f.write(json.dumps(snap,ensure_ascii=False)+"\n")
    return {"channels_imported":len(groups),"distinct_messages":total,"registry_size":len(registry),"source":str(source)}

def main():
    p=argparse.ArgumentParser(description="Import existing M5 Telegram evidence summaries into ALINA")
    p.add_argument("--materials",type=Path,required=True,help="Existing M5 materials.jsonl (read-only)")
    p.add_argument("--registry",type=Path,default=Path("data/telegram/channel_registry.json"))
    p.add_argument("--snapshots",type=Path,default=Path("out/telegram_channel_catalog/m5_evidence_snapshots.jsonl"))
    a=p.parse_args()
    print(json.dumps(run(a.materials,a.registry,a.snapshots),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
