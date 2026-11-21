#!/usr/bin/env python3
"""Check retrospective quality flags around public incident anchor dates."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
EVENTS=[
 ("Tunda","T3","2023-10-27","2023-10-27","KKP patrol stop; public release October 29"),
 ("Tunda","T5","2023-11-18","2023-11-22","Coalition fishers' passage accounts; observed near Pulau Pari"),
 ("Kodingareng Lompo","K3","2020-02-13","2020-02-13","Coalition account of reported operation onset"),
 ("Kodingareng Lompo","K4","2020-09-12","2020-09-12","Police numeric date for vessel/confrontation account"),
 ("Kodingareng Lompo","K1","2020-02-01","2020-10-31","Contractor month-precision envelope; not a daily work log"),
]


def main():
    d=pd.read_csv(ROOT/"all_optical_scenes.csv",parse_dates=["date"],low_memory=False)
    out=[]
    details=[]
    for site,code,first,last,label in EVENTS:
        first,last=pd.Timestamp(first),pd.Timestamp(last)
        for sensor in ["Sentinel-2","Landsat 8/9"]:
            x=d[(d.site==site)&(d.sensor==sensor)].sort_values("date")
            nearby=x[x.date.between(first-pd.Timedelta(days=14),last+pd.Timedelta(days=14))].copy()
            nearby.insert(0,"event_id",code)
            details.append(nearby[["event_id","site","sensor","date","utc","id","status","clear_pct","reef_clear_pct","asset_url"]])
            dur=x[x.date.between(first,last)]
            passes=x[(x.status=="ok")&x.clear_pct.ge(90)]
            p=passes[passes.date.lt(first)]
            n=passes[passes.date.gt(last)]
            out.append(dict(event_id=code,site=site,sensor=sensor,first=first,last=last,context=label,
                            window_catalog_dates=dur.date.nunique(),window_read_dates=dur[dur.status.eq("ok")].date.nunique(),
                            window_pass_dates=dur[(dur.status.eq("ok"))&dur.clear_pct.ge(90)].date.nunique(),
                            preceding_pass_date=p.date.max(),following_pass_date=n.date.min(),
                            preceding_pass_days=(first-p.date.max()).days,following_pass_days=(n.date.min()-last).days))
    pd.DataFrame(out).to_csv(ROOT/"optical_event_window_summary.csv",index=False,date_format="%Y-%m-%d")
    pd.concat(details,ignore_index=True).to_csv(ROOT/"optical_event_nearby_inventory.csv",index=False,date_format="%Y-%m-%d")
    print(pd.DataFrame(out).to_string(index=False))


if __name__=="__main__":
    main()
