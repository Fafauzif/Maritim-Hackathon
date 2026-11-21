#!/usr/bin/env python3
"""Recalculate numerical headline results from workstream inputs, no manuscript import."""
import argparse
import bisect
from collections import Counter
import csv
from datetime import date, timedelta
from pathlib import Path

def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))

def calc_sensors(data):
    start,end=date(2025,1,1),date(2026,10,31)
    days=[start+timedelta(days=i) for i in range((end-start).days+1)]
    for site in sorted({r['site'] for r in data}):
        baseline=[r for r in data if r['site']==site and r['sensor']=='Sentinel-2']
        print(site,'catalog and readable Sentinel-2 site-dates',len({r['date'] for r in baseline}),len({r['date'] for r in baseline if r['status']=='ok'}))
        selected={}
        for sensor in ('Sentinel-2','Landsat 8/9'):
            selected[sensor]={date.fromisoformat(r['date']) for r in data
                if r['site']==site and r['sensor']==sensor and r['status']=='ok'
                and start<=date.fromisoformat(r['date'])<=end and float(r['clear_pct'])>=90}
        def gap_and_wait(hit):
            arr=sorted(hit)
            padded=[start-timedelta(days=1),*arr,end+timedelta(days=1)]
            longest=max((b-a).days-1 for a,b in zip(padded,padded[1:]))
            waits=[bisect.bisect_left(arr,a) for a in days[:-7]]
            fraction=sum(i<len(arr) and (arr[i]-a).days<=7 for a,i in zip(days,waits))/len(waits)
            return longest,fraction
        s,l=selected.values()
        union=s|l
        gg=gap_and_wait(s),gap_and_wait(union)
        print(site,len(s),len(l),len(union),len(l-s),len(days[:-7]),gg)
        expected={"Tunda":(62,77,15,(132,.5120845921450151),(131,.5770392749244713)),
            "Kodingareng Lompo":(63,88,25,(162,.4818731117824773),(158,.5558912386706949))}
        es,eu,ea,eh,eu2=expected[site]
        assert (len(s),len(union),len(l-s))==(es,eu,ea)
        assert gg[0][0]==eh[0] and gg[1][0]==eu2[0]
        assert abs(gg[0][1]-eh[1])<0.000001 and abs(gg[1][1]-eu2[1])<0.000001
        reef=[r for r in baseline if r['status']=='ok' and r['reef_clear_pct']]
        if reef:
            both = Counter((float(r['clear_pct'])>=90,float(r['reef_clear_pct'])>=90) for r in reef)
            print('reef compared:', site,len(reef),dict(both))

def calc_rain(data):
    for months in (tuple(range(1,13)), (11,12)):
        wet=[r for r in data if int(r['date_utc'][5:7]) in months and float(r['region_proxy_imerg_mm'])>=10]
        classes = Counter("pass" if r['either_pass']=='1' else "failed" if r['either_acquired']=='1' else "no_acq" for r in wet)
        oo=(len(wet),classes['pass'],classes['failed'],classes['no_acq'])
        print("Higher rain optical decomposition",months,oo)
        assert oo==((257,13,68,176) if len(months)==12 else (72,1,22,49))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('base',type=Path,nargs='?',default=Path(__file__).resolve().parent.parent)
    a=parser.parse_args()
    calc_sensors(read(a.base/'optical/all_optical_scenes.csv'))
    calc_rain(read(a.base/'rain/rainfall_multisensor_days.csv'))
    print('Expanded sensor gain, gap, and weather claims reproduced.')
if __name__=="__main__":
    main()
