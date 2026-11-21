#!/usr/bin/env python3
"""Join complete 2025 Sentinel/Landsat optical masks to same-label regional rainfall."""
import argparse
from collections import defaultdict
import csv
from pathlib import Path

BASE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--sentinel',required=True,type=Path)
parser.add_argument('--landsat',required=True,type=Path)
parser.add_argument('--rain',default=BASE/'rainfall_daily.csv',type=Path)
parser.add_argument('--output-dir',default=BASE,type=Path)
args=parser.parse_args()

def read_coverage(path):
    out=defaultdict(list)
    for r in csv.DictReader(path.open()):
        if r['status']=='ok' and r['clear_pct'] and r['date'].startswith('2025-'):
            site='Kodingareng' if r['site']=='Kodingareng Lompo' else r['site']
            out[(site,r['date'])].append(float(r['clear_pct']))
    return out

sent=read_coverage(args.sentinel)
landsat=read_coverage(args.landsat)
daily=[]
for r in csv.DictReader(args.rain.open()):
    d=r['date_utc']; site=r['site']
    if not (d.startswith('2025-') and site in ('Tunda','Kodingareng')):
        continue
    s=sent[(site,d)]; l=landsat[(site,d)]
    o={'site':site,'date_utc':d,'region_proxy_imerg_mm':float(r['imerg_mean'])}
    for name,sensor in (('sentinel',s),('landsat',l),('either',s+l)):
        o[name+'_acquired']=int(bool(sensor))
        o[name+'_pass']=int(max(sensor,default=-1)>=90)
    daily.append(o)
out=[]
for start,end,period in [('2025-01-01','2025-12-31','2025'),('2025-06-01','2025-09-30','Jun–Sep 2025'),('2025-11-01','2025-12-31','Nov–Dec 2025')]:
    for site in ('Tunda','Kodingareng','Both'):
        base=[r for r in daily if (r['site']==site or site=='Both') and start<=r['date_utc']<=end]
        for k in (5,10,20):
            for wet in (True,False):
                rr=[r for r in base if (r['region_proxy_imerg_mm']>=k)==wet]
                o={'site':site,'period':period,'rain_threshold_mm':k,'rain_group':'at or above' if wet else 'below',
                   'site_days':len(rr)}
                for s in ('sentinel','landsat','either'):
                    o[s+'_acquired']=sum(r[s+'_acquired'] for r in rr)
                    o[s+'_pass']=sum(r[s+'_pass'] for r in rr)
                out.append(o)
for name,arr in [('rainfall_multisensor_days.csv',daily),('rainfall_multisensor_summary.csv',out)]:
    with (args.output_dir/name).open('w',newline='') as f:
        w=csv.DictWriter(f,list(arr[0]));w.writeheader();w.writerows(arr)
for r in out:
    if r['rain_threshold_mm']==10: print(r)
