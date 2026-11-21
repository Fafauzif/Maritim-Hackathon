"""Verify headline claims from the article against the packaged observations."""
import csv,json
from pathlib import Path
from datetime import date,timedelta
from collections import defaultdict
import math

P=Path(__file__).resolve().parent
def data(f):
    with (P/f).open(encoding='utf-8',newline='') as src:return list(csv.DictReader(src))
def groups(rows,start,end,threshold=90):
    passes=defaultdict(set)
    for x in rows:
        if x['status']=='ok' and start<=x['date']<=end and float(x['clear_pct'])>=threshold:
            passes[x['site']].add(date.fromisoformat(x['date']))
    return passes
def horizons(dates):
    start=date(2025,1,1);end=date(2026,10,31)
    n=(end-start).days+1
    seq=[start+timedelta(days=i) for i in range(n)]
    longest=gap=0
    for d in seq:
        gap=0 if d in dates else gap+1
        longest=max(longest,gap)
    step=sum(any(d+timedelta(days=j) in dates for j in range(8)) for d in seq[:-7])
    return n-7,step,longest

s=data('optical/sentinel_longitudinal.csv')
l=data('optical/landsat_longitudinal.csv')
assert len(s)==1178 and len({(r['site'],r['date']) for r in s})==1178
assert sum(r['status']=='ok' for r in s)==1177 and len(l)==799 and all(r['status']=='ok' for r in l)
S=groups(s,'2025-01-01','2026-10-31')
L=groups(l,'2025-01-01','2026-10-31')
for site,expect in {'Tunda':(62,77,132,131,51.21,57.70),'Kodingareng Lompo':(63,88,162,158,48.19,55.59)}.items():
    n,h,g=horizons(S[site]);n2,h2,g2=horizons(S[site]|L[site])
    assert n==n2==662
    assert (len(S[site]),len(S[site]|L[site]),g,g2,round(100*h/n,2),round(100*h2/n,2))==expect
reef=[r for r in s if r['site']=='Tunda' and r['reef_clear_pct']]
assert len(reef)==587
assert sum(float(x['clear_pct'])>=90>float(x['reef_clear_pct']) for x in reef)==10
assert sum(float(x['reef_clear_pct'])>=90>float(x['clear_pct']) for x in reef)==24
geom=data('root/kodingareng_habitat_scl.csv')
assert len(geom)==109 and all(x['status']=='read' for x in geom)
assert sum(float(x['reef_broad_pct'])>=90>float(x['ring_broad_pct']) for x in geom)==8
rain=data('rain/rainfall_multisensor_days.csv')
assert len(rain)==730
wet=[r for r in rain if r['date_utc'][5:7] in ('11','12') and float(r['region_proxy_imerg_mm'])>=10]
assert (len(wet),sum(int(r['either_acquired']) for r in wet),sum(int(r['either_pass']) for r in wet))==(72,23,1)
clocks=data('review/tunda_event_sensor_clocks.csv')
assert not any('2023-10-27' in (r.get('acquisition') or '') for r in clocks)
assert len({r['acquisition'][:10] for r in clocks if r['query']=='mpc-l89' and r['platform'] in {'landsat-8','landsat-9'}})==4
a=[r for r in data('amur/amur_landsat_daily_2023.csv') if r['date']=='2023-07-12'][0]
assert abs(float(a['west_red'])-float(a['east_red'])-.09614)<.00001
for x in data('root/travel_scenarios.csv'):
    assert math.isclose(float(x['kinematic_distance_km']),3.6*float(x['constant_speed_m_per_s'])*float(x['hours']),abs_tol=.001)
print('Verified optical inventory, mission gains, calendar horizons, receptor disagreement, higher-rain observations, Tunda clocks, Amur contrast and transport scenarios.')
