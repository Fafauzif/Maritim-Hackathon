#!/usr/bin/env python3
"""Compare the version clocks of three archives for a single Sentinel-2 acquisition."""
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request,urlopen

root=Path(__file__).resolve().parent
labels=["copernicus-s2","element84-s2","element84-s2-legacy"]
rows=[]
def get_head(kv):
    key,url=kv
    try:
        with urlopen(Request(url, method="HEAD"), timeout=10) as reply:
            return {"asset":key,"asset_url":url,"http_status":reply.status,
                    "asset_last_modified":reply.headers.get("Last-Modified")}
    except Exception as e:
        return {"asset":key,"asset_url":url,"http_status":str(e)}

for label in labels:
    if label=="element84-s2-legacy":
        path=root/"tunda_26_oct_legacy_item.json"
        f=[json.loads(path.read_text())]
    else:
        f = json.loads((root/f"tunda_event_{label}.json").read_text())["features"]
    a = next(v for v in f if "20231026" in v["id"])
    p=a["properties"]
    row = {"catalog":label,"item_id":a["id"],"acquisition_property":p["datetime"],
           "processing_time":p.get("s2:generation_time") or p.get("processing:datetime"),
           "baseline":p.get("s2:processing_baseline") or p.get("processing:version"),
           "catalog_created":p.get("created"),"catalog_published":p.get("published")}
    urls=[(k,a["assets"][k]["href"]) for k in ("visual","red","scl","granule_metadata") if k in a["assets"] and a["assets"][k]["href"].startswith("https://")]
    if label=="element84-s2-legacy":
        urls.append(("upstream_granule_metadata","https://sentinel-s2-l2a.s3.eu-central-1.amazonaws.com/tiles/48/M/XU/2023/10/26/0/metadata.xml"))
    if urls:
        with ThreadPoolExecutor(max_workers=5) as pool:
            rows.extend(row|res for res in pool.map(get_head,urls))
    else:
        rows.append(row)
with (root/"tunda_product_lineage.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[-1].keys()))
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["catalog"],r.get("asset"),r["processing_time"],r["catalog_created"],r.get("asset_last_modified"),r["catalog_published"])
