#!/usr/bin/env python3
"""Combine the designated Sentinel archive with same-acquisition recovery rows."""
import argparse
from pathlib import Path

import pandas as pd
from summarize import CUTOFFS, chart_combined, chart_monthly, chart_reef, row_summary

ROOT=Path(__file__).resolve().parent


def load(p):
    df=pd.read_csv(p)
    df["date"]=pd.to_datetime(df.date,format="%Y-%m-%d")
    df["time"]=pd.to_datetime(df.utc,format="mixed",utc=True)
    return df


def resolve(s2,c1):
    s2=s2.copy()
    s2["archive"]="legacy Sentinel-2 L2A"
    s2["legacy_scene_id"]=s2.id
    s2["legacy_catalog_cloud_pct"]=s2.catalog_cloud_pct
    if c1 is None:
        return s2
    c1=c1[c1.status.eq("ok")].copy()
    match=s2.merge(c1,on=["site","date","platform"],suffixes=("_base","_c1"))
    match=match[(match.time_base-match.time_c1).abs()<=pd.Timedelta(minutes=2)]
    both=match[match.status_base.eq("ok")].copy()
    both["delta_pct"]=both.clear_pct_c1-both.clear_pct_base
    both["decision_differs"]=(both.clear_pct_base>=90)!=(both.clear_pct_c1>=90)
    both[["site","date","id_base","id_c1","clear_pct_base","clear_pct_c1","delta_pct","decision_differs"]].to_csv(ROOT/"paired_archive_qa.csv",index=False)
    q=match[match.status_base.ne("ok")].drop_duplicates(["site","id_base"])
    replace=q.set_index(["site","id_base"])
    fields=[c for c in c1.columns if c+"_c1" in q.columns]
    for idx, row in s2.iterrows():
        key=(row.site,row.id)
        if key in replace.index:
            s2.loc[idx,fields]=[replace.loc[key,f+"_c1"] for f in fields]
            s2.loc[idx,"archive"]="Collection 1 same site/date/platform and ±2 minutes"
    return s2


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--c1",type=Path)
    p.add_argument("--out-dir",type=Path,default=ROOT.parent/"figures")
    args=p.parse_args()
    s=resolve(load(ROOT/"sentinel_legacy_coverage.csv"),load(args.c1) if args.c1 else None)
    l=load(ROOT/"landsat_coverage.csv")
    if (ROOT/"landsat_history_coverage.csv").exists():
        l=pd.concat([load(ROOT/"landsat_history_coverage.csv"),l],ignore_index=True)
    d=pd.concat([s,l],ignore_index=True)
    args.out_dir.mkdir(exist_ok=True)
    s.drop(columns=["time"]).to_csv(ROOT/"sentinel_longitudinal.csv",index=False,date_format="%Y-%m-%d")
    l.drop(columns=["time"]).to_csv(ROOT/"landsat_longitudinal.csv",index=False,date_format="%Y-%m-%d")
    d.drop(columns=["time"]).to_csv(ROOT/"all_optical_scenes.csv",index=False,date_format="%Y-%m-%d")
    o=row_summary(d)
    o.to_csv(ROOT/"multisensor_summary.csv",index=False)
    t=s.assign(year=s.date.dt.year,month=s.date.dt.month,
               query=s.status.ne("missing"),usable=s.status.eq("ok"),qual=s.status.eq("ok") & s.clear_pct.ge(90),
               tile=s.legacy_catalog_cloud_pct.le(20),known_clear=s.status.eq("ok") & s.reef_clear_pct.ge(90),
               rescued=s.status.eq("ok") & s.clear_pct.ge(90) & s.legacy_catalog_cloud_pct.gt(20),
               tileonly=s.status.eq("ok") & s.clear_pct.lt(90) & s.legacy_catalog_cloud_pct.le(20))
    g=t.groupby(["site","year"]).agg(catalog=("query","sum"),read=("usable","sum"),local=("qual","sum"),tile=("tile","sum"),reef=("known_clear","sum"),locally_rescued=("rescued","sum"),tile_only=("tileonly","sum")).reset_index()
    g["pass_min_pct"]=g.local/g.catalog*100
    g["pass_max_pct"]=(g.local+g.catalog-g.read)/g.catalog*100
    g.to_csv(ROOT/"annual_sentinel_summary.csv",index=False)
    h=t.groupby(["site","month"]).agg(catalog=("query","sum"),read=("usable","sum"),local=("qual","sum")).reset_index()
    h["pass_min_pct"]=h.local/h.catalog*100
    h["pass_max_pct"]=(h.local+h.catalog-h.read)/h.catalog*100
    h.to_csv(ROOT/"monthly_sentinel_bounds.csv",index=False)
    chart_monthly(s,args.out_dir)
    chart_combined(d,args.out_dir)
    chart_reef(s,args.out_dir)
    print(g.to_string(index=False))
    print(s.groupby(["site","archive","status"]).size().to_string())


if __name__=="__main__":
    main()
