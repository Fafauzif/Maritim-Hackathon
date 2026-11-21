"""Verify all reported Amur counts from distributed tables, without a network."""
from collections import Counter
import csv
from datetime import date, datetime
from math import isclose
from pathlib import Path

BASE=Path(__file__).resolve().parent
FLOODS=((date(2023,8,10),date(2023,8,13)),(date(2023,8,24),date(2023,8,27)),
        (date(2023,8,30),date(2023,9,1)))

def io(path):
    with (BASE/path).open(newline='') as stream:
        return list(csv.DictReader(stream))

def acceptable(row, cutoff=90):
    return all(float(row[f'{z}_water_pct'])>=cutoff for z in ('west','east'))

def red_contrast(row):
    return float(row['west_red'])-float(row['east_red'])

def verify():
    sentinel=io('amur_daily_2023.csv')
    landsat=io('amur_landsat_daily_2023.csv')
    assert all(not row['error'] for row in sentinel+landsat)
    assert len(sentinel)==18 and len(landsat)==12
    s2={row['date']:row for row in sentinel if acceptable(row)}
    l8={row['date']:row for row in landsat if acceptable(row)}
    assert len(s2)==2 and len(l8)==4
    dates={date.fromisoformat(row['date']) for row in sentinel+landsat}
    assert len(dates)==28 and len(set(s2)|set(l8))==5 and set(s2)&set(l8)=={'2023-09-06'}
    flood_dates={d for d in dates if any(first<=d<=last for first,last in FLOODS)}
    assert flood_dates=={date(2023,8,12),date(2023,8,13),date(2023,8,27),date(2023,9,1)}
    assert not any(str(d) in s2 or str(d) in l8 for d in flood_dates)
    paired='2023-09-06'
    delta=datetime.fromisoformat(s2[paired]['utc'])-datetime.fromisoformat(l8[paired]['utc'])
    assert round(delta.total_seconds())==1100
    assert isclose(red_contrast(s2[paired]),.0552)
    assert isclose(red_contrast(l8[paired]),.0645975)
    assert isclose(red_contrast(l8['2023-07-12']),.09614)
    assert len([x for x in sentinel if acceptable(x,80)])==2
    assert len([x for x in sentinel if acceptable(x,75)])==3
    assert len([x for x in sentinel if acceptable(x,95)])==2
    catalog=io('amur_catalog_2019_2026.csv')
    assert len(catalog)==156 and len({row['date_utc'] for row in catalog})==156
    assert sum(float(row['tile_cloud_pct'])<=20 for row in catalog)==33
    assert Counter(row['date_utc'][:4] for row in catalog)['2022']==18
    print('Amur results passed source-table checks.')
if __name__=='__main__':
    verify()
