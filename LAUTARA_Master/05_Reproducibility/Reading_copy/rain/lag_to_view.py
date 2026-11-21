#!/usr/bin/env python3
"""Count qualifying follow-up opportunities by simple fixed horizons."""
import csv
from datetime import date,timedelta
from pathlib import Path

HERE=Path(__file__).resolve().parent
raw=list(csv.DictReader((HERE/'rainfall_multisensor_days.csv').open()))
lookup={(r['site'],date.fromisoformat(r['date_utc'])):r for r in raw}
last=date(2025,12,31)
results=[]
for site in ('Tunda','Kodingareng','Both'):
    for period,start in [('Full year',date(2025,1,1)),('Nov–Dec',date(2025,11,1))]:
        for mm in (5,10,20):
            for h in (0,1,3,7):
                for mode in ('sentinel','either'):
                    origin=[]
                    matched=0
                    for (s,d),r in lookup.items():
                        if site not in ('Both',s) or not start<=d<=last-timedelta(days=h) or float(r['region_proxy_imerg_mm'])<mm:
                            continue
                        origin.append((s,d))
                        if any(int(lookup[s,d+timedelta(days=i)][mode+'_pass']) for i in range(h+1)):
                            matched+=1
                    results.append({'site':site,'period':period,'rain_threshold_mm':mm,'horizon_days_including_day_zero':h,'mission_set':mode,'eligible_site_days':len(origin),'site_days_with_view':matched})
with (HERE/'rainfall_followup_horizons.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,list(results[0]));w.writeheader();w.writerows(results)
for r in results:
    if r['site']=='Both' and r['rain_threshold_mm']==10:
        print(r)
