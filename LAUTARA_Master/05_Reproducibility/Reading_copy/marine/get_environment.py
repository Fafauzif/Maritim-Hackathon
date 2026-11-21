"""Download public historical archives and aggregate UTC/wall-clock days.

Open-Meteo historical weather: ECMWF ERA5; Marine wave models: MFWAM and ERA5-Ocean;
Open-Meteo Marine Best Match current: Copernicus Marine SMOC. NASA POWER: MERRA-2.
Python standard library and pandas dependencies.
"""
import csv
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from datetime import date,datetime,timedelta,timezone
import hashlib
import json
from pathlib import Path
import urllib.request as req
import urllib.parse as parse
import pandas as pd

ROOT=Path(__file__).resolve().parent
RAW=ROOT/'environment_raw'
SITES={'Tunda':(-5.81151,106.27811,7,'2023-10-12','2023-11-11'),
       'Kodingareng':(-5.14905,119.26473,8,'2020-02-01','2020-10-31')}
ERA='https://archive-api.open-meteo.com/v1/archive'
MAR='https://marine-api.open-meteo.com/v1/marine'
POW='https://power.larc.nasa.gov/api/temporal/daily/point'

def download(task):
    site,model,(lat,lon,offset,start,end)=task
    early=(date.fromisoformat(start)-timedelta(days=1)).isoformat()
    if model=='merra2':
        target=POW
        params={'longitude':lon,'latitude':lat,'start':start.replace('-',''),'end':end.replace('-',''),
                'parameters':'PRECTOTCORR,WS10M,WD10M','community':'AG','format':'JSON','time-standard':'UTC'}
    else:
        params={'longitude':lon,'latitude':lat,'start_date':early,'end_date':end,'timezone':'GMT','wind_speed_unit':'ms'}
        if model=='era5':
            target=ERA
            params.update(models='era5',hourly='precipitation,wind_speed_10m,wind_direction_10m',cell_selection='nearest')
        else:
            target=MAR
            fields='ocean_current_velocity,ocean_current_direction' if model=='best_match' else 'wave_height,wave_direction,wave_period'
            params.update(models=model,hourly=fields,cell_selection='sea')
    address=target+'?'+parse.urlencode(params)
    f=RAW/f'{site}_{model}.json'
    RAW.mkdir(exist_ok=True)
    if not f.exists():
        with req.urlopen(address,timeout=30) as response:
            f.write_bytes(response.read())
    content=f.read_bytes()
    return task,json.loads(content),{'site':site,'model':model,'url':address,'sha256':hashlib.sha256(content).hexdigest()}

if __name__=='__main__':
    tasks=[(s,m,coord) for s,coord in SITES.items()
           for m in ['era5','era5_ocean','merra2']+(['meteofrance_wave','best_match'] if s=='Tunda' else [])]
    rs=[]
    ds=[]
    manifests=[]
    with ThreadPoolExecutor() as pool:
        for (site,model,point),d,manifest in pool.map(download,tasks):
            _,_,offset,start,end=point
            if model=='merra2':
                dates=d['properties']['parameter']['PRECTOTCORR']
                for k,v in dates.items():
                    ds.append(dict(site=site,model=model,utc_day=datetime.strptime(k,'%Y%m%d').date(),rain_mm=v))
                manifest.update(header=d['header'],geometry=d['geometry'],fields=d['parameters'])
            else:
                df=pd.DataFrame(d['hourly'])
                df['utc_timestamp']=pd.to_datetime(df.pop('time'),utc=True)
                df['local_timestamp']=df.utc_timestamp.dt.tz_convert(timezone(timedelta(hours=offset)))
                df['utc_day']=df.utc_timestamp.dt.date
                df['local_day']=df.local_timestamp.dt.date
                df['site']=site
                df['model']=model
                df['grid_lat']=d['latitude']
                df['grid_lon']=d['longitude']
                # Open-Meteo ocean-current unit must be verified from response, because the
                # request wind_speed_unit option applies differently by variable/provider.
                for key in ['ocean_current_velocity','wind_speed_10m']:
                    if key in df:
                        unit=d['hourly_units'][key]
                        assert unit in ['m/s','km/h'],unit
                        if unit=='km/h': df[key]/=3.6
                rs.append(df)
                manifest.update(grid_lat=d['latitude'],grid_lon=d['longitude'],fields=d['hourly_units'])
            manifests.append(manifest)
    out=pd.concat(rs,ignore_index=True)
    out.to_csv(ROOT/'environment_hourly.csv',index=False)
    p=pd.DataFrame(ds)
    assert all(m['header']['time_standard']=='UTC' for m in manifests if m['model']=='merra2')
    p.to_csv(ROOT/'nasa_power_daily.csv',index=False)
    for s,(_,_,_,a,b) in SITES.items():
        sample=out[(out.site==s)&(out.model=='era5')]
        local=sample[(sample.local_day>=date.fromisoformat(a))&(sample.local_day<=date.fromisoformat(b))]
        utc=sample[(sample.utc_day>=date.fromisoformat(a))&(sample.utc_day<=date.fromisoformat(b))]
        assert (local.groupby('local_day').size()==24).all()
        assert (utc.groupby('utc_day').size()==24).all()
    (ROOT/'environment_manifest.json').write_text(json.dumps(manifests,indent=2))
    print('rows',len(out),len(ds))
    for m in manifests:
        print(m['site'],m['model'],m.get('grid_lat'),m.get('grid_lon'),m.get('fields'))
