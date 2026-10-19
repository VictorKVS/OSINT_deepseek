#!/usr/bin/env python3
"""FATHER OSINT Telegram channel registry. Stdlib only; no Telegram network access."""
import argparse
import csv
import datetime as dt
import json
import re
from pathlib import Path

FIELDS = ("channel_id","username","title","url","language","topics","discovered_from","discovered_at_utc","verified_at_utc","status","subscribers","avg_views","posts_30d","original_posts_30d","evidence_links","validated_skills","notes")
SCORE_FIELDS = ("popularity","activity","originality","evidence","skill_yield")
WEIGHTS = {"popularity":0.10,"activity":0.15,"originality":0.20,"evidence":0.25,"skill_yield":0.30}
HANDLE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{4,31}$")

def number(row, key):
    raw = row.get(key, "")
    if raw in ("", None):
        return None
    try:
        v = int(raw)
    except (ValueError, TypeError):
        raise ValueError(f"{key}: expected nonnegative integer")
    if v < 0:
        raise ValueError(f"{key}: expected nonnegative integer")
    return v

def normalize(row):
    out = {key: str(row.get(key,"") or "").strip() for key in FIELDS}
    name = out["username"].lstrip("@")
    if name and not HANDLE.fullmatch(name):
        raise ValueError(f"Invalid username: {name}")
    out["username"] = name
    if name and not out["url"]:
        out["url"] = "https://t.me/" + name
    if out["url"] and not re.fullmatch(r"https://t\.me/[A-Za-z][A-Za-z0-9_]{4,31}/?",out["url"]):
        raise ValueError("Only public t.me channel links accepted")
    if not out["channel_id"]:
        out["channel_id"] = name.lower()
    if not out["channel_id"] or not out["title"]:
        raise ValueError("channel_id and title are required")
    for key in ("subscribers","avg_views","posts_30d","original_posts_30d","evidence_links","validated_skills"):
        v = number(out,key)
        out[key] = "" if v is None else str(v)
    return out

def score(row):
    subs=number(row,"subscribers");views=number(row,"avg_views");posts=number(row,"posts_30d")
    originals=number(row,"original_posts_30d");evidence=number(row,"evidence_links");skills=number(row,"validated_skills")
    # No imputation: unavailable data means no overall score.
    parts = {
      "popularity": min(100,round(100*__import__("math").log1p(subs)/__import__("math").log1p(1000000),2)) if subs is not None else None,
      "activity": min(100,round(posts/30*100,2)) if posts is not None else None,
      "originality": round(originals/posts*100,2) if originals is not None and posts is not None and posts>0 and originals<=posts else None,
      "evidence": min(100,round(evidence/20*100,2)) if evidence is not None else None,
      "skill_yield": min(100,round(skills/10*100,2)) if skills is not None else None,
    }
    parts["engagement_ratio"] = round(views/subs,4) if views is not None and subs else None
    parts["overall"] = round(sum(parts[k]*w for k,w in WEIGHTS.items()),2) if all(parts[k] is not None for k in WEIGHTS) else None
    return parts

def read_rows(path):
    if not path.exists(): return []
    if path.suffix.lower()==".json":
        data=json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data,dict): data=data.get("channels",[])
        if not isinstance(data,list): raise ValueError("Expected JSON array or {channels:[]}")
        return [normalize(r) for r in data]
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return [normalize(r) for r in csv.DictReader(f)]

def save(registry,folder):
    folder.mkdir(parents=True,exist_ok=True)
    rows=sorted(registry.values(),key=lambda r:(r["username"],r["channel_id"]))
    scores={r["channel_id"]:score(r) for r in rows}
    stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    (folder/"channels.json").write_text(json.dumps({"generated_at_utc":stamp,"channels":rows},ensure_ascii=False,indent=2),encoding="utf-8")
    with (folder/"channels.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    ratings=[{"channel_id":r["channel_id"],"title":r["title"],"username":r["username"],"status":r["status"],**scores[r["channel_id"]]} for r in rows]
    ratings.sort(key=lambda r:(r["overall"] is None,-(r["overall"] or 0),r["channel_id"]))
    (folder/"ratings.json").write_text(json.dumps({"generated_at_utc":stamp,"methodology":"weighted observed metrics; null when incomplete","weights":WEIGHTS,"ratings":ratings},ensure_ascii=False,indent=2),encoding="utf-8")
    with (folder/"ratings.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(ratings[0]) if ratings else ["channel_id","title","username","status",*SCORE_FIELDS,"engagement_ratio","overall"]);w.writeheader();w.writerows(ratings)
    verified=sum(r["status"]=="verified" for r in rows)
    ranked=sum(s["overall"] is not None for s in scores.values())
    lines=["# Telegram OSINT — отчёт о каталоге","",f"Сформирован: {stamp}","",f"- Всего записей: {len(rows)}",f"- Проверено: {verified}",f"- Полностью рассчитан рейтинг: {ranked}","", "## Ограничения","", "- Непроверенные кандидаты не являются подтверждёнными каналами.","- Неизвестные показатели сохраняются пустыми, рейтинг не выдумывается.","- Показатели должны сопровождаться датой проверки и происхождением.","- Навыки учитываются только после испытаний на полигоне.","", "## Каналы","", "| Канал | Статус | Рейтинг |", "|---|---|---|"]
    for r in rows:
        s=scores[r["channel_id"]]["overall"]
        lines.append(f'| {r["title"].replace("|","/")} (@{r["username"]}) | {r["status"] or "candidate"} | {s if s is not None else "недостаточно данных"} |')
    (folder/"report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return len(rows),ranked

def main():
    p=argparse.ArgumentParser(description="Local OSINT Telegram channel registry and report generator")
    p.add_argument("--input",type=Path,required=True,help="CSV or JSON channel candidates")
    p.add_argument("--registry",type=Path,default=Path("data/telegram/channel_registry.json"))
    p.add_argument("--out",type=Path,default=Path("out/telegram_channel_catalog"))
    args=p.parse_args()
    registry={r["channel_id"]:r for r in read_rows(args.registry)}
    for row in read_rows(args.input):
        old=registry.get(row["channel_id"],{})
        registry[row["channel_id"]]={key:row[key] or old.get(key,"") for key in FIELDS}
    args.registry.parent.mkdir(parents=True,exist_ok=True)
    args.registry.write_text(json.dumps({"channels":list(registry.values())},ensure_ascii=False,indent=2),encoding="utf-8")
    n,ranked=save(registry,args.out)
    print(f"Saved {n} channels, {ranked} fully rated; outputs: {args.out}")

if __name__=="__main__": main()
