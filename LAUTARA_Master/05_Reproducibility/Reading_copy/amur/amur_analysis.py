"""Reproduce Amur Bay optical and rainfall analysis for LAUTARA.
Run with system Python plus GDAL, NumPy, matplotlib (no accounts required).
"""
import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from osgeo import gdal, osr

BASE = Path(__file__).resolve().parent
YEARS = range(2019, 2027)
LON, LAT = 131.80778, 43.32556
BBOX = '131.72,43.19,131.91,43.33'
TILE = 'T52TGP'
COLLECTION = 'sentinel-2-c1-l2a'
# Rectangles, kilometers east/north of the mapped mouth in UTM 52N.
ZONES = {'mouth': (-.7,.7,-2.7,-1.3),
         'west': (-.7,.7,-6.7,-5.3),
         'east': (4.3,5.7,-6.7,-5.3)}
COLORS = {'mouth':'#E69F00','west':'#CC79A7','east':'#56B4E9'}
MAP = (-6.4,8.1,-10.1,2.6)
CLOUD = (3,8,9,10)
MIN_WATER = .90
gdal.UseExceptions()
for key, val in {'GDAL_DISABLE_READDIR_ON_OPEN':'EMPTY_DIR','GDAL_HTTP_TIMEOUT':'12',
                 'CPL_VSIL_CURL_ALLOWED_EXTENSIONS':'.tif','GDAL_HTTP_MAX_RETRY':'2'}.items():
    gdal.SetConfigOption(key,val)
wgs, utm = osr.SpatialReference(), osr.SpatialReference()
wgs.ImportFromEPSG(4326)
wgs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
utm.ImportFromEPSG(32652)
CX,CY,_ = osr.CoordinateTransformation(wgs,utm).TransformPoint(LON,LAT)

def json_cached(path,url):
    if not path.exists():
        with urlopen(url, timeout=30) as response:
            path.write_bytes(response.read())
    return json.loads(path.read_text())

def catalog(year):
    query = urlencode({'collections':COLLECTION,'bbox':BBOX,
                       'datetime':f'{year}-07-01T00:00:00Z/{year}-09-30T23:59:59Z',
                       'limit':100})
    data=json_cached(BASE/f'stac_{year}.json',f'https://earth-search.aws.element84.com/v1/search?{query}')
    assert len(data['features']) == data['numberMatched'] == data['numberReturned'], year
    selected = {}
    for item in data['features']:
        if TILE in item['id']:
            assert item['properties']['proj:epsg'] == 32652
            d = item['properties']['datetime'][:10]
            if d in selected:
                raise ValueError(f'Duplicate target tile on {d}')
            selected[d] = item
    return selected

def raster_zone(item,key,zone,out_res=None):
    asset = item['assets'][key]
    ds = gdal.Open('/vsicurl/'+asset['href'])
    x0, dx, _, y0, _, dy = ds.GetGeoTransform()
    assert dy == -dx and ds.GetSpatialRef().GetAuthorityCode(None) == '32652'
    a,b,c,d = zone
    i1,i2 = [int(np.ceil((CX+v*1000-x0)/dx-.5)) for v in (a,b)]
    j1,j2 = [int(np.ceil((y0-CY-v*1000)/dx-.5)) for v in (d,c)]
    kwargs = {'buf_xsize': int(round((i2-i1)*dx/out_res)),
              'buf_ysize': int(round((j2-j1)*dx/out_res))} if out_res else {}
    vals = ds.ReadAsArray(i1,j1,i2-i1,j2-j1,**kwargs)
    ext = ((x0+i1*dx-CX)/1000,(x0+i2*dx-CX)/1000,(y0+j2*dy-CY)/1000,(y0+j1*dy-CY)/1000)
    r = asset.get('raster:bands',[{}])[0]
    return vals, ext, r.get('scale',1),r.get('offset',0)

def scl_pixels(item):
    """Count class-6 water and cloud classes on three fixed receptor footprints."""
    r = {n: raster_zone(item,'scl',p) for n,p in ZONES.items()}
    row = {}
    for n,(z,_,_,_) in r.items():
        row[f'{n}_water_pct'] = 100*float(np.mean(z==6))
        row[f'{n}_cloud_pct'] = 100*float(np.mean(np.isin(z,CLOUD)))
        row[f'{n}_ice_pct'] = 100*float(np.mean(z==11))
    return row,r

def analyze(item):
    row = {'date':item['properties']['datetime'][:10],'item':item['id'],
           'utc':item['properties']['datetime'],'tile_cloud_pct':item['properties']['eo:cloud_cover'],
           'scl_href':item['assets']['scl']['href'],'red_href':item['assets']['red']['href']}
    for n in ZONES:
        row.update({f'{n}_water_pct':None,f'{n}_cloud_pct':None,f'{n}_ice_pct':None,f'{n}_red':None,f'{n}_green':None})
    row['error']=''
    try:
        quality, scl = scl_pixels(item)
        row.update(quality)
        # Keep optically plausible dates to test thresholds down to 60%.
        eligible=[n for n in ZONES if row[f'{n}_water_pct']>=60]
        for n in eligible:
            mask, ext, _, _ = scl[n]
            for band in ('red','green'):
                # Use the exact 20 m SCL cell edge extent for physically aligned 10 m inputs.
                vals, check, scale,off = raster_zone(item,band,ext)
                assert vals.shape == (mask.shape[0]*2,mask.shape[1]*2)
                assert np.max(abs(np.array(check)-np.array(ext)))<1e-8
                fine = mask.repeat(2,axis=0).repeat(2,axis=1)==6
                row[f'{n}_{band}'] = float(np.median(vals[fine & (vals != 0)]*scale+off))
    except Exception as e:
        row['error']=type(e).__name__+': '+str(e)
    return row

def save_rows(path,rows):
    with path.open('w',newline='') as out:
        w=csv.DictWriter(out,fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

def set_style():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelcolor':'#324d5b',
                          'text.color':'#193641','axes.edgecolor':'#a2b5bd','xtick.color':'#516475',
                          'ytick.color':'#516475','axes.titleweight':'bold'})

def sample_maps(features,dates,filename):
    set_style()
    fig,axarr=plt.subplots(1,len(dates),figsize=(11.4,5.5),layout='constrained')
    for ax,d in zip(axarr,dates):
        a,ext,_,_ = raster_zone(features[d],'visual',MAP)
        ax.imshow(a.transpose(1,2,0),extent=ext)
        for n,(l,r,b,t) in ZONES.items():
            ax.add_patch(Rectangle((l,b),r-l,t-b,edgecolor=COLORS[n],facecolor='none',lw=2))
            ax.text((l+r)/2,b-.35,n.capitalize(),ha='center',va='top',fontweight='bold',
                    fontsize=9,color='white',bbox={'facecolor':'#172b36','alpha':.72,'pad':1.5,'linewidth':0})
        ax.scatter([0],[0],c='white',s=16,linewidth=.8,edgecolors='black',zorder=5)
        ax.text(-.25,.31,'Razdolnaya mouth',ha='right',va='bottom',color='white',fontsize=8,
                bbox={'facecolor':'#172b36','alpha':.72,'pad':1.5,'linewidth':0})
        ax.text(7,1.85,'↑ N',color='white',fontweight='bold',ha='center')
        ax.plot([-5.9,-3.9],[-9.5,-9.5],color='white',lw=2.2)
        ax.text(-4.9,-9.38,'2 km',color='white',ha='center',va='bottom',fontsize=8)
        ax.set(xlabel='Kilometers east of river mouth',title=f'{date.fromisoformat(d):%d %B %Y}',
               xticks=[-5,0,5],yticks=[-10,-5,0])
    axarr[0].set_ylabel('Kilometers north of river mouth')
    fig.savefig(BASE/filename,dpi=240)
    plt.close(fig)

def rain_data():
    param={'latitude':43.8,'longitude':131.85,'start_date':'2023-06-26','end_date':'2023-09-30',
           'daily':'precipitation_sum','timezone':'UTC','models':'era5'}
    raw=json_cached(BASE/'era5_openmeteo_point.json','https://archive-api.open-meteo.com/v1/archive?'+urlencode(param))
    return {date.fromisoformat(d): p for d,p in zip(raw['daily']['time'],raw['daily']['precipitation_sum'])}

def qualifying(row,zones=('west','east'),threshold=90):
    return all(row[z+'_water_pct'] is not None and row[z+'_water_pct']>=threshold and row[z+'_red'] is not None for z in zones)

def event_plot(rows,rain):
    set_style()
    rows=[r for r in rows if r['date'].startswith('2023')]
    dates=[date.fromisoformat(r['date']) for r in rows]
    fig,axes=plt.subplots(3,1,figsize=(11.2,7.2),sharex=True,layout='constrained',
                         gridspec_kw={'height_ratios':[1,1.1,1.3]})
    for ax in axes:
        for start,end in ((date(2023,8,10),date(2023,8,14)),
                          (date(2023,8,24),date(2023,8,28)),
                          (date(2023,8,30),date(2023,9,2))):
            ax.axvspan(start,end,color='#d5e7ec',alpha=.65,lw=0)
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.24)
    ax=axes[0]; ax.bar(list(rain),list(rain.values()),color='#417a86',width=.8)
    ax.set_ylabel('Daily rainfall\n(mm)')
    ax.set_title('River context, satellite opportunity, and observed optical contrast',loc='left')
    ax.text(date(2023,7,2),max(rain.values())*.92,'ERA5 near lower basin, shaded = published flood windows',fontsize=9,ha='left')
    ax=axes[1]
    for z in ZONES:
        ax.scatter(dates,[r[f'{z}_water_pct'] for r in rows],s=31,c=COLORS[z],edgecolors='#36505a',
                   linewidths=.3,label=z.capitalize(),alpha=.95,marker={'mouth':'^','west':'o','east':'s'}[z])
    ax.axhline(90,color='#65828c',ls='--',lw=1)
    ax.set_ylabel('SCL water-class\npixels (%)')
    ax.legend(loc='upper left',bbox_to_anchor=(0,1.21),ncols=3,frameon=False,fontsize=8)
    ax=axes[2]
    chosen=[r for r in rows if qualifying(r)]
    ax.axhline(0,lw=.9,color='#81949b')
    ax.scatter([date.fromisoformat(r['date']) for r in chosen],
               [r['west_red']-r['east_red'] for r in chosen],
               s=39,c='#783572',zorder=5)
    ax.set_ylabel('West minus east\nred-band reflectance')
    relaxed=[r for r in rows if qualifying(r,threshold=75) and not qualifying(r)]
    ax.scatter([date.fromisoformat(r['date']) for r in relaxed],
               [r['west_red']-r['east_red'] for r in relaxed],s=46,
               facecolors='white',edgecolors='#783572',label='Passes 75%, fails 90%')
    ax.legend(loc='upper right',fontsize=8,frameon=False)
    for r in chosen + relaxed:
        d=date.fromisoformat(r['date'])
        ax.annotate(d.strftime('%d %b'),(d,r['west_red']-r['east_red']),
                    textcoords='offset points',xytext=(4,5),fontsize=8)
    ax.set_xlim(date(2023,7,1),date(2023,9,30))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO,interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.set_xlabel('Date (UTC), 2023')
    fig.savefig(BASE/'amur_event_timeline.png',dpi=240)
    plt.close(fig)

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--only-year',type=int)
    a=p.parse_args()
    years=(a.only_year,) if a.only_year else YEARS
    with ThreadPoolExecutor(max_workers=5) as pool:
        features={k:v for catalogued in pool.map(catalog,years) for k,v in catalogued.items()}
    print(f'{len(features)} dates in study tile',flush=True)
    ordered=[features[k] for k in sorted(features)]
    output=BASE/('amur_daily_'+str(a.only_year)+'.csv' if a.only_year else 'amur_daily_2019_2026.csv')
    if not output.exists():
        with ThreadPoolExecutor(max_workers=12) as pool:
            rows=list(pool.map(analyze,ordered))
        save_rows(output,rows)
    else:
        with output.open() as h:
            rows=list(csv.DictReader(h))
        for r in rows:
            for k in r:
                if k.endswith(('_pct','_red','_green')):
                    r[k]=float(r[k]) if r[k] else None
    print('errors',[(r['date'],r['error']) for r in rows if r['error']],flush=True)
    for y in years:
        vals=[r for r in rows if r['date'].startswith(str(y))]
        print(y,len(vals),sum(qualifying(r) for r in vals),flush=True)
        for r in vals:
            if y==2023:
                print(r['date'],r['tile_cloud_pct'],r['mouth_water_pct'],r['west_water_pct'],r['east_water_pct'],
                      r['mouth_red'],r['west_red'],r['east_red'],flush=True)
    if 2023 in years:
        weather=rain_data()
        rr=[{'date_utc':str(d),'precipitation_mm':v,
             'preceding_3_complete_utc_days_mm':sum(weather[d-timedelta(days=k)] for k in range(1,4))
             if all(d-timedelta(days=k) in weather for k in range(1,4)) else None} for d,v in weather.items()]
        save_rows(BASE/'amur_rainfall_daily_2023.csv',rr)
        event_plot(rows,weather)
        sample_maps(features,['2023-08-27','2023-09-06','2023-09-21'],'amur_scene_comparison.png')
        sample_maps(features,['2023-07-28','2023-09-06'],'amur_optical_counterexample.png')
if __name__=='__main__':
    main()
