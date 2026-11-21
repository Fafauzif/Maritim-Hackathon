#!/usr/bin/env python3
"""Recover late or incomplete Sentinel reads by limiting per-raster HTTP requests."""
import csv
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from osgeo import gdal
from run_coverage import FIELDS, read

HERE = Path(__file__).resolve().parent
P = HERE/"sentinel_legacy_coverage.csv"
host = {
    0: "https://sentinel-cogs.s3.us-west-2.amazonaws.com/",
    1: "https://s3.us-west-2.amazonaws.com/sentinel-cogs/",
    2: "https://sentinel-cogs.s3.amazonaws.com/",
    3: "https://sentinel-cogs.s3-us-west-2.amazonaws.com/",
    4: "https://sentinel-cogs.s3.dualstack.us-west-2.amazonaws.com/",
}
UNSIGNED_READ = read


def fetch(row,n):
    asset = row["asset_url"]
    if not asset.startswith("https:"):
        return row
    for i in range(3):
        try:
            mirror=host[(n+i)%len(host)] + urllib.parse.urlparse(asset).path.lstrip("/")
            with urllib.request.urlopen(mirror,timeout=13) as f:
                content=f.read()
            if len(content)<1000 or content[:2] not in {b'II',b'MM'}:
                raise ValueError("Incomplete or invalid TIFF response")
            temp=f"/vsimem/{row['id']}.tif"
            gdal.FileFromMemBuffer(temp,content)
            try:
                read_row = row.copy()
                read_row["asset_url"]=temp
                result=UNSIGNED_READ((read_row,None,True))
                result["asset_url"]=asset
                return result
            finally:
                gdal.Unlink(temp)
        except Exception as e:
            if i==2:
                row["error"]=str(e)[:140]
                return row
            time.sleep(i+1)
    return row


def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--workers",type=int,default=16)
    p.add_argument("--start",default="2025-01-01")
    p.add_argument("--include-earlier",action="store_true")
    opts=p.parse_args()
    with P.open() as f:
        entries = list(csv.DictReader(f))
    fixed = {(x["site"], x["id"]): x for x in entries}
    stages = [[x for x in entries if x["status"]!="ok" and x["date"]>=opts.start]]
    if opts.include_earlier:
        stages.append([x for x in entries if x["status"]!="ok" and x["date"]<opts.start])
    for queue in stages:
        print("starting",len(queue),flush=True)
        with ThreadPoolExecutor(max_workers=opts.workers) as pool:
            work = [pool.submit(fetch,x,i) for i,x in enumerate(queue)]
            for i,f in enumerate(as_completed(work),1):
                y=f.result()
                fixed[(y["site"],y["id"])]=y
                if i%25==0 or i==len(queue):
                    tmp=P.with_suffix(".tmp.csv")
                    with tmp.open("w") as out:
                        w=csv.DictWriter(out,FIELDS)
                        w.writeheader()
                        w.writerows(fixed.values())
                    tmp.replace(P)
                    print(i,"/",len(queue),"complete, total successful:",sum(int(x["status"]=="ok") for x in fixed.values()),flush=True)
if __name__=="__main__":
    main()
