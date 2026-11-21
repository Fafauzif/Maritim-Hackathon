"""Inventory 2019–26 July–September Sentinel-2 opportunities in T52TGP."""
import json
from statistics import median
from urllib.parse import urlencode
from amur_analysis import BASE, BBOX, YEARS, TILE, catalog, json_cached, save_rows

def alternate_2022():
    args={'collections':'sentinel-2-l2a','bbox':BBOX,
          'datetime':'2022-07-01T00:00:00Z/2022-09-30T23:59:59Z','limit':100}
    path=BASE/'amur_legacy_2022.json'
    vals=json_cached(path,'https://earth-search.aws.element84.com/v1/search?'+urlencode(args))
    rows={f['properties']['datetime'][:10]:f for f in vals['features'] if '52TGP' in f['id']}
    return rows

rows=[]; byyear=[]
for y in YEARS:
    features=catalog(y)
    source='Earth Search C1'
    if not len(features) and y==2022:
        features=alternate_2022()
        source='Earth Search legacy L2A, C1 empty'
    yr=[]
    for when,item in sorted(features.items()):
        value=item['properties']['eo:cloud_cover']
        yr.append(value)
        rows.append({'date_utc':when,'scene_id':item['id'],
                     'source':source,'tile_cloud_pct':value,
                     'scl_href':item['assets']['scl']['href']})
    byyear.append({'year':y,'dates':len(yr),'tile_cloud_leq_20_pct':sum(x<=20 for x in yr),
                   'tile_cloud_median_pct':round(median(yr),2) if yr else None,'source':source})
save_rows(BASE/'amur_catalog_2019_2026.csv',rows)
save_rows(BASE/'amur_catalog_summary.csv',byyear)
for y in byyear:
    print(y)
