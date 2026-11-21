"""Download bounded daily GLORYS12V1 surface currents directly from the public
Copernicus Marine Zarr archive and write long-form CSV. Python 3.12, numpy and
numcodecs. Archive key and coordinate indices are explicit in each row."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import csv
import hashlib
import json
import math
import time
from pathlib import Path
import urllib.request as url
import numpy as np
import numcodecs

BASE='https://s3.waw3-1.cloudferro.com/mdl-arco-geo-025/arco/GLOBAL_MULTIYEAR_PHY_001_030/cmems_mod_glo_phy_my_0.083deg_P1D-m_202311/geoChunked.zarr'
ROOT=Path(__file__).resolve().parent
CACHE=ROOT/'glorys_cache'
SITES=[('Tunda',-5.81151,106.27811,'2023-10-12','2023-11-11'),('Kodingareng',-5.14905,119.26473,'2020-02-01','2020-10-31')]

def fetch(key):
    CACHE.mkdir(exist_ok=True)
    f=CACHE/(key.replace('/','_'))
    if f.exists():
        return f.read_bytes()
    last=None
    for attempt in range(4):
        try:
            with url.urlopen(BASE+'/'+key,timeout=20) as stream:
                payload=stream.read()
            f.write_bytes(payload)
            return payload
        except OSError as error:
            last=error
            if getattr(error,"code",None)==429:
                time.sleep(2**attempt)
    raise last

def unpack(key,var):
    schema=META[f'{var}/.zarray']
    compression=numcodecs.get_codec(schema['compressor'])
    raw=compression.decode(fetch(key))
    return np.frombuffer(raw,dtype=schema['dtype'])

def format_time(date):
    return str(date.astype('datetime64[D]'))

def spatial_range(arr,center):
    i=int(np.argmin(abs(arr-center)))
    return list(range(i-1,i+2))

def dist_km(lat,lon,lat0,lon0):
    return 111.20*math.hypot(lat-lat0,(lon-lon0)*math.cos(math.radians(lat0)))

def decode_tuple(t,c):
    var,chunk=t
    k=f'{var}/'+'.'.join(map(str,chunk))
    return k,unpack(k,var).reshape(c)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',action='store_true',help='fetch all days in full calendar years 2019–2025')
    args=parser.parse_args()
    sites=[(site,lat,lon,'2019-01-01','2025-12-31') for site,lat,lon,_,_ in SITES] if args.baseline else SITES
    suffix='_baseline' if args.baseline else ''
    META=json.loads(fetch('.zmetadata'))['metadata']
    vdef={v:META[f'{v}/.zarray'] for v in ['uo','vo']}
    attrs={v:META[f'{v}/.zattrs'] for v in ['uo','vo']}
    defs={v:np.array(vdef[v]['chunks']) for v in vdef}
    with ThreadPoolExecutor(max_workers=3) as pool:
        keys=['latitude/0','longitude/0','elevation/0','time/0','time/1']
        coord=list(pool.map(lambda k:unpack(k,k.split('/')[0]),keys))
        latitude,longitude,depth=coord[:3]
        cal=np.append(coord[3],coord[4])[:META['time/.zarray']['shape'][0]]
        dates=(np.datetime64('1950-01-01T00')+cal.astype('timedelta64[h]')).astype('datetime64[D]')
        surface=int(np.argmin(abs(depth)))
        nd=int(np.argmin(abs(abs(depth)-10)))
        selected={}
        wanted=set()
        for label,lat0,lon0,begin,end in sites:
            tids=np.flatnonzero((dates>=np.datetime64(begin))&(dates<=np.datetime64(end)))
            inds=[(t,d,y,x) for t in tids for d in [surface,nd] for y in spatial_range(latitude,lat0) for x in spatial_range(longitude,lon0)]
            selected[label]=(lat0,lon0,inds)
            for v in vdef:
                chunks=np.unique(np.array(inds)//defs[v],axis=0)
                wanted.update((v,tuple(z)) for z in chunks)
        data=dict(pool.map(lambda t:decode_tuple(t,defs[t[0]]),sorted(wanted)))
    def val(v,idx):
        coords=idx//defs[v]
        rr=tuple(idx%defs[v])
        key=f'{v}/'+'.'.join(map(str,coords))
        raw=data[key][rr]
        if raw == vdef[v]['fill_value']:
            return None
        return float(raw)*attrs[v]['scale_factor']+attrs[v].get('add_offset',0)
    rows=[]
    for label,(lat0,lon0,inds) in selected.items():
        for idx in inds:
            t,d,y,x=idx
            u=val('uo',np.array(idx))
            v=val('vo',np.array(idx))
            usable=u is not None and v is not None
            vals=(math.hypot(u,v),math.degrees(math.atan2(u,v))%360) if usable else ('','')
            rows.append([label,format_time(dates[t]),float(abs(depth[d])),float(latitude[y]),float(longitude[x]),dist_km(latitude[y],longitude[x],lat0,lon0),u,v,*vals,t,d,y,x])
    with (ROOT/f'glorys_daily{suffix}.csv').open('w') as f:
        w=csv.writer(f)
        w.writerow(['site','utc_day','depth_m','lat','lon','distance_km_from_island','east_m_s','north_m_s','speed_m_s','towards_deg','time_index','depth_index','lat_index','lon_index'])
        w.writerows(rows)
    lead={k: {'url':BASE+'/'+k,'sha256':hashlib.sha256(fetch(k)).hexdigest()} for k in ['.zmetadata',*keys,*data]}
    (ROOT/f'glorys_manifest{suffix}.json').write_text(json.dumps(lead,indent=2))
    print('rows',len(rows),'finite',sum(r[6] is not None for r in rows),'archive extent',dates.min(),dates.max())
    for v in attrs: print(v,attrs[v])
