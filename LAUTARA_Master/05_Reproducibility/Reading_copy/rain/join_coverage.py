#!/usr/bin/env python3
"""Descriptively cross-tabulate rainfall and qualified Sentinel-2 viewing opportunities."""
import argparse
from collections import defaultdict
import csv
from datetime import date
from pathlib import Path

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--tunda',type=Path,required=True)
parser.add_argument('--kodingareng',type=Path,required=True)
parser.add_argument('--rain',type=Path,default=HERE/'rainfall_daily.csv')
parser.add_argument('--output-dir',type=Path,default=HERE)
args=parser.parse_args()
SOURCES={'Tunda':(args.tunda,'date','primary_clear_percent'),
         'Kodingareng':(args.kodingareng,'utc_date','clear_1500_3000')}
periods={'Jun–Sep 2025':('2025-06-01','2025-09-30'),'Nov–Dec 2025':('2025-11-01','2025-12-31')}
rain=[r for r in csv.DictReader(args.rain.open()) if r['imerg_mean']]
records=[]
summary=[]
for site,(path,datekey,coverkey) in SOURCES.items():
    acquired=defaultdict(list)
    for row in csv.DictReader(path.open()):
        acquired[row[datekey]].append(row[coverkey])
    for period,(start,end) in periods.items():
        matches=[r for r in rain if r['site']==site and start<=r['date_utc']<=end]
        for r in matches:
            d=r['date_utc']
            local=[float(x) for x in acquired.get(d,[]) if x]
            coverage=max(local) if local else None
            if d not in acquired:
                state='no acquisition in catalog sample'
            elif not local:
                state='acquisition without outcome'
            else:
                state='qualifying acquisition' if coverage>=90 else 'acquisition below 90%'
            records.append({'site':site,'period':period,'date_utc':d,'imerg_mean_mm':float(r['imerg_mean']),
                            'count_acquisitions':len(acquired.get(d,[])),'best_local_clear_percent':coverage,'state':state})
        pp=[r for r in records if r['site']==site and r['period']==period]
        for threshold in (5,10,20):
            for condition in ('above_or_equal','below'):
                group=[r for r in pp if (r['imerg_mean_mm']>=threshold)==(condition=='above_or_equal')]
                n=sum(r['count_acquisitions']>0 for r in group)
                q=sum(r['state']=='qualifying acquisition' for r in group)
                unread=sum(r['state']=='acquisition without outcome' for r in group)
                summary.append({'site':site,'period':period,'proxy_nominal_wet_threshold_mm':threshold,
                                'rain_group':condition,'utc_calendar_days':len(group),'acquired_days':n,
                                'qualifying_acquisition_days':q,'catalog_acquisition_missing_days':len(group)-n,
                                'acquisition_below_threshold_days':n-unread-q,'unread_acquisition_days':unread})
for fname,items in [('rainfall_optical_days.csv',records),('rainfall_optical_summary.csv',summary)]:
    with (args.output_dir/fname).open('w',newline='') as fh:
        w=csv.DictWriter(fh,list(items[0]))
        w.writeheader()
        w.writerows(items)
print('site,period,group,calendar days,acquired,qualifying,no acquisition,below coverage')
for r in summary:
    if r['proxy_nominal_wet_threshold_mm']==10:
        print(', '.join(str(r[x]) for x in ('site','period','rain_group','utc_calendar_days','acquired_days','qualifying_acquisition_days','catalog_acquisition_missing_days','acquisition_below_threshold_days')))
