#!/usr/bin/env python3
"""Download reproducible daily precipitation subsets and preserve source responses."""
import argparse
import concurrent.futures as cf
import hashlib
import json
from datetime import date
from pathlib import Path
import time
import urllib.parse
import urllib.request

BASE=Path(__file__).resolve().parent
RAW=BASE / 'raw'
POWER='https://power.larc.nasa.gov/api/temporal/daily/point'
CLIMATE='https://climateserv.servirglobal.net/api'
CPC='https://psl.noaa.gov/thredds/ncss/grid/Datasets/cpc_global_precip'
# Reproducible proxy coordinates, deliberately not assumed watershed polygons.
PROXIES={
    'Tunda':{
        'points':[(106.10,-6.10),(106.20,-6.15),(106.30,-6.20),(106.40,-6.20),(106.20,-6.40),(106.40,-6.40)],
        'box':[106.10,-6.47,106.45,-6.07],
        'event_year':2023,'start':'2023-09-01','end':'2023-11-30','center':(106.26,-6.25)
    },
    'Kodingareng':{
        'points':[(119.50,-5.15),(119.60,-5.15),(119.70,-5.15),(119.50,-5.35),(119.60,-5.35),(119.70,-5.35)],
        'box':[119.46,-5.38,119.76,-5.10],
        'event_year':2020,'start':'2020-01-15','end':'2020-11-15','center':(119.61,-5.25)
    },
    'Amur':{
        'points':[(131.78,43.48),(131.88,43.59),(131.98,43.70),(131.78,43.80),(131.88,43.51),(131.98,43.62)],
        'box':[131.74,43.42,132.05,43.85],
        'event_year':2023,'start':'2023-07-20','end':'2023-09-15','center':(131.90,43.64)
    },
}

def query(url,data):
    return url+'?'+urllib.parse.urlencode(data)

def request(url):
    err=None
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                return r.read()
        except Exception as e:
            err=e
            time.sleep(i+1)
    raise err

def record(path, url, payload, **meta):
    path.write_bytes(payload)
    path.with_suffix(path.suffix+'.source.json').write_text(json.dumps({
        'url':url,'sha256':hashlib.sha256(payload).hexdigest(),**meta},indent=2))

def power(site,i,point):
    path=RAW/f'{site}_IMERG_p{i}.json'
    if path.exists(): return
    lon,lat=point
    url=query(POWER,{'parameters':'IMERG_PRECTOT','community':'AG','longitude':lon,'latitude':lat,
                     'start':'20190101','end':'20251231','format':'JSON','time-standard':'UTC'})
    payload=request(url)
    data=json.loads(payload)
    if 'IMERG' not in data['header']['sources']:
        raise ValueError((site,i,data['header']))
    record(path,url,payload,point=point,provider='NASA POWER',product='IMERG_PRECTOT')
    print(path.name,len(data['properties']['parameter']['IMERG_PRECTOT']),flush=True)

def cpc(site,year,point):
    path=RAW/f'{site}_CPC_{year}.csv'
    if path.exists(): return
    lon,lat=point
    url=query(f'{CPC}/precip.{year}.nc',{'var':'precip','latitude':lat,'longitude':lon,
             'time_start':f'{year}-01-01T00:00:00Z','time_end':f'{year}-12-31T00:00:00Z','accept':'csv'})
    payload=request(url)
    if not payload.startswith(b'time,'):
        raise ValueError(payload[:300])
    record(path,url,payload,point=point,provider='NOAA Physical Sciences Laboratory',product='CPC global unified gauge daily precipitation')
    print(path.name,len(payload),flush=True)

def chirps(site,start,end,box):
    path=RAW/f'{site}_CHIRPS.json'
    if path.exists(): return
    west,south,east,north=box
    polygon={'type':'Polygon','coordinates':[[[west,south],[east,south],[east,north],[west,north],[west,south]]]}
    url=query(CLIMATE+'/submitDataRequest/',{'datatype':0,
        'begintime':date.fromisoformat(start).strftime('%m/%d/%Y'),
        'endtime':date.fromisoformat(end).strftime('%m/%d/%Y'),
        'intervaltype':0,'operationtype':5,'dateType_Category':'default',
        'geometry':json.dumps(polygon,separators=(',',':'))})
    job_path=RAW/f'{site}_CHIRPS_job.json'
    if job_path.exists():
        job=json.loads(job_path.read_text())[0]
    else:
        payload=request(url)
        job=json.loads(payload)[0]
        record(job_path,url,payload,provider='SERVIR ClimateSERV',product='UCSB CHIRPS')
    pr=query(CLIMATE+'/getDataRequestProgress/',{'id':job})
    result=query(CLIMATE+'/getDataFromRequest/',{'id':job})
    for i in range(100):
        progress=json.loads(request(pr))[0]
        if progress == 100: break
        if progress < 0: raise ValueError((site,progress))
        time.sleep(3)
    else: raise TimeoutError(site)
    payload=request(result)
    data=json.loads(payload)
    if not data.get('data'): raise ValueError(data)
    record(path,result,payload,submit_url=url,proxy_box=box,provider='SERVIR ClimateSERV',product='UCSB CHIRPS')
    print(path.name,len(data['data']),flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--only', choices=['all','IMERG','CPC','CHIRPS'],default='all')
    args=ap.parse_args()
    RAW.mkdir(exist_ok=True)
    tasks=[]
    # Event data first, then antecedent baseline.
    for site,value in PROXIES.items():
        if args.only in ('all','CHIRPS'):
            tasks.append((chirps,(site,value['start'],value['end'],value['box'])))
        if args.only in ('all','CPC'):
            tasks.append((cpc,(site,value['event_year'],value['center'])))
    for site,value in PROXIES.items():
        if args.only in ('all','IMERG'):
            tasks.extend((power,(site,i,point)) for i,point in enumerate(value['points']))
        if args.only in ('all','CPC'):
            tasks.extend((cpc,(site,y,value['center'])) for y in range(2019,2026) if y != value['event_year'])
    errors=[]
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        jobs={ex.submit(fun,*argv):(fun.__name__,argv) for fun,argv in tasks}
        for job in cf.as_completed(jobs):
            try: job.result()
            except Exception as e:
                errors.append((jobs[job],str(e)))
                print(jobs[job],repr(e),flush=True)
    if errors:
        (RAW/'errors.json').write_text(json.dumps(errors,indent=2))
        raise SystemExit('Some retrievals failed. See raw/errors.json.')

if __name__=='__main__': main()
