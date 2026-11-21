"""Reproduce Landsat 8/9 same-window, same-footprint QA and reflectance checks."""
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import json
from urllib.parse import urlencode
from urllib.request import urlopen
import numpy as np
from amur_analysis import BASE, ZONES, BBOX, json_cached, raster_zone, save_rows

API = 'https://planetarycomputer.microsoft.com/api'
query = urlencode({'collections':'landsat-c2-l2','bbox':BBOX,
                   'datetime':'2023-07-01T00:00:00Z/2023-09-30T23:59:59Z','limit':100})
catalog = json_cached(BASE/'stac_landsat_2023.json',API+'/stac/v1/search?'+query)
features=sorted([f for f in catalog['features'] if f['id'].startswith(('LC08','LC09'))],
               key=lambda item: item['properties']['datetime'])
with urlopen(API+'/sas/v1/token/landsateuwest/landsat-c2',timeout=25) as response:
    token=json.load(response)['token']

def calculate(item):
    f=dict(item)
    f['assets']={k:dict(a,href=a['href']+'?'+token) for k,a in item['assets'].items()
                  if k in ('qa_pixel','red','green')}
    p=item['properties']
    rec=dict(date=p['datetime'][:10],utc=p['datetime'],item=item['id'],scene_cloud_pct=p['eo:cloud_cover'],
             qa_href=item['assets']['qa_pixel']['href'])
    for n in ZONES:
        rec.update({f'{n}_water_pct':None,f'{n}_red':None,f'{n}_green':None})
    rec['error']=''
    try:
        for z, box in ZONES.items():
            qa,ext,_,_ = raster_zone(f,'qa_pixel',box)
            # Bits 0–5 = fill/dilated cloud/cirrus/cloud/shadow/snow.
            # Water label is bit 7. Require all adverse flags absent.
            good=(qa & 63 == 0) & (qa & 128 != 0)
            rec[f'{z}_water_pct']=100*float(np.mean(good))
            if rec[f'{z}_water_pct']<75:
                continue
            for b in ('red','green'):
                vals, check, scale, off=raster_zone(f,b,ext)
                assert np.max(abs(np.array(check)-np.array(ext)))<1e-8
                rec[f'{z}_{b}']=float(np.median(vals[good & (vals!=0)]*scale+off))
    except Exception as e:
        # Signed URL is session-specific and must not appear in any public file.
        rec['error']=type(e).__name__+': '+str(e).split('?')[0]
    return rec

with ThreadPoolExecutor(max_workers=5) as pool:
    rows=list(pool.map(calculate,features))
save_rows(BASE/'amur_landsat_daily_2023.csv',rows)
for r in rows:
    print(r['date'],r['item'],r['west_water_pct'],r['east_water_pct'],r['west_red'],r['east_red'],r['error'],flush=True)
