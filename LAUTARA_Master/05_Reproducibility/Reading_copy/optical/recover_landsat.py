#!/usr/bin/env python3
"""Bounded retry of historical Landsat raster reads. Never write the SAS token."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import csv
import time
import urllib.request

from osgeo import gdal
from run_coverage import FIELDS,get_json,read

P=Path(__file__).resolve().parent/"landsat_history_coverage.csv"


def fetch(row,token):
    for i in range(3):
        try:
            with urllib.request.urlopen(row["asset_url"]+"?"+token,timeout=15) as h:
                content=h.read()
            if len(content)<1000 or content[:2] not in {b'II',b'MM'}:
                raise ValueError("Incomplete or invalid TIFF response")
            tmp=f"/vsimem/{row['id']}.tif"
            gdal.FileFromMemBuffer(tmp,content)
            try:
                a=row.copy()
                a["asset_url"]=tmp
                result=read((a,token,True))
                result["asset_url"]=row["asset_url"]
                return result
            finally:
                gdal.Unlink(tmp)
        except Exception as e:
            if i==2:
                row["error"]=str(e).split("?",1)[0][:140]
                return row
            time.sleep(1)
    return row


def main():
    token=get_json("https://planetarycomputer.microsoft.com/api/sas/v1/token/landsateuwest/landsat-c2")["token"]
    with P.open() as f:
        rows=list(csv.DictReader(f))
    truth={(a["site"],a["id"]):a for a in rows}
    pending=[a for a in rows if a["status"]!="ok"]
    with ThreadPoolExecutor(max_workers=12) as pool:
        jobs=[pool.submit(fetch,a,token) for a in pending]
        for i,job in enumerate(as_completed(jobs),1):
            a=job.result()
            truth[(a["site"],a["id"])]=a
            if i%25==0 or i==len(jobs):
                temp=P.with_suffix(".saving")
                with temp.open("w") as f:
                    w=csv.DictWriter(f,FIELDS)
                    w.writeheader()
                    w.writerows(truth.values())
                temp.replace(P)
                print(i,"/",len(jobs),"done",sum(a["status"]=="ok" for a in truth.values()),flush=True)
if __name__=="__main__":
    main()
