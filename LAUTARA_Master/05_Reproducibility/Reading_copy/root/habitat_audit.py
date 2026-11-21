"""Rasterize archived reef footprints against measured Sentinel-2 SCL scenes."""
import argparse,csv,json,urllib.request,urllib.parse
from datetime import date,timedelta
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
from osgeo import gdal,ogr,osr

CATA='https://earth-search.aws.element84.com/v1/search'
REEF='https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1/query'
SITES={
 'Tunda':(106.27811,-5.81151,32748,'48MXU',[('historical','2023-10-15','2024-02-14'),('baseline_check','2025-06-01','2026-02-28')]),
 'Kodingareng':(119.26473,-5.14905,32750,'50MQV',[('historical','2020-02-01','2020-11-01'),('baseline_check','2025-06-01','2026-02-28')]),
}
gdal.UseExceptions()
for k,v in {'GDAL_DISABLE_READDIR_ON_OPEN':'EMPTY_DIR','GDAL_HTTP_TIMEOUT':'8','CPL_VSIL_CURL_ALLOWED_EXTENSIONS':'.tif','GDAL_HTTP_MAX_RETRY':'0'}.items():
    gdal.SetConfigOption(k,v)
def get_json(url,params):
    with urllib.request.urlopen(url+'?'+urllib.parse.urlencode(params),timeout=25) as r:
        return json.load(r)
def wgs_epsg(epsg):
    s=osr.SpatialReference()
    s.ImportFromEPSG(epsg)
    s.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    return s
def catalog(lon,lat,tile,start,end):
    query={'collections':'sentinel-2-l2a','bbox':','.join(str(a) for a in (lon-.029,lat-.029,lon+.029,lat+.029)),
           'datetime':start+'T00:00:00Z/'+end+'T23:59:59Z','limit':100}
    first,last=date.fromisoformat(start),date.fromisoformat(end)
    series=[]
    while first<=last:
        till=min(last,first+timedelta(days=79))
        query['datetime']=first.isoformat()+'T00:00:00Z/'+till.isoformat()+'T23:59:59Z'
        page=get_json(CATA,query)
        series.extend(page['features'])
        assert page.get('context',{}).get('matched',len(page['features']))<=len(page['features'])
        first=till+timedelta(days=1)
    grouped={}
    for item in series:
        if f'_{tile}_' in item['id']:
            dt=item['properties']['datetime'][:10]
            if (dt not in grouped or item['properties'].get('updated','')>=grouped[dt]['properties'].get('updated','')):
                grouped[dt]=item
    return list(grouped.values())
def geom_layer(geojson,sr):
    raw=ogr.Open(str(geojson))
    a=raw.GetLayer()
    trans=osr.CoordinateTransformation(wgs_epsg(4326),sr)
    dest=ogr.GetDriverByName('Memory').CreateDataSource('')
    layer=dest.CreateLayer('reef',sr)
    for fst in a:
        geo=fst.GetGeometryRef().Clone()
        geo.Transform(trans)
        feat=ogr.Feature(layer.GetLayerDefn())
        feat.SetGeometry(geo)
        layer.CreateFeature(feat)
    return dest,layer
def analyze(x,cent,sr,geojson):
    label,scene=x
    utc=scene['properties']['datetime']
    href=scene['assets']['scl']['href']
    st={'group':label,'date':utc[:10],'observed_utc':utc,'id':scene['id'],'scl_url':href,'tile_cloud_pct':scene['properties']['eo:cloud_cover']}
    tmp=f"/vsimem/reef-{scene['id']}.tif"
    try:
        if not href.startswith('https:'):
            raise ValueError('No public COG')
        for host in ['https://s3.us-west-2.amazonaws.com/sentinel-cogs/','https://sentinel-cogs.s3.amazonaws.com/','https://sentinel-cogs.s3.us-west-2.amazonaws.com/']:
            try:
                mirror=host+urllib.parse.urlparse(href).path.lstrip("/")
                with urllib.request.urlopen(mirror,timeout=9) as obj:
                    data=obj.read()
                if data[:2] not in {b'II',b'MM'} or len(data)<1000:
                    raise ValueError('Invalid COG')
                break
            except Exception:
                data=None
        if data is None:
            raise ValueError('Source COG unavailable after trying three endpoints')
        gdal.FileFromMemBuffer(tmp,data)
        ds=gdal.Open(tmp)
        X,dx,_,Y,_,dy=ds.GetGeoTransform()
        cx,cy=cent
        ix,iy=int((cx-X)/dx),int((cy-Y)/dy)
        q=int(3100/dx)+2
        a,b=ix-q,iy-q
        n=2*q+1
        s=ds.ReadAsArray(a,b,n,n)
        east=X+(a+np.arange(n)+.5)*dx-cx
        north=Y+(b+np.arange(n)+.5)*dy-cy
        radius=np.hypot(east[None,:],north[:,None])
        ring=(radius>=1500)&(radius<=3000)
        raw,reef=geom_layer(geojson,sr)
        mem=gdal.GetDriverByName('MEM').Create('',n,n,1,gdal.GDT_Byte)
        mem.SetGeoTransform((X+a*dx,dx,0,Y+b*dy,0,dy))
        mem.SetProjection(sr.ExportToWkt())
        gdal.RasterizeLayer(mem,[1],reef,burn_values=[1])
        rh=(mem.ReadAsArray()==1)&(radius<=3000)
        west=rh&(east[None,:]<0)
        east_r=rh&~west
        for name,foot in [('ring',ring),('reef',rh),('west',west),('east',east_r)]:
            st[name+'_pixels']=int(foot.sum())
            st[name+'_broad_pct']=100*float(np.isin(s[foot],[2,4,5,6]).mean()) if foot.any() else ''
            st[name+'_water_pct']=100*float((s[foot]==6).mean()) if foot.any() else ''
        st['reef_overlap_ring_pct']=100*float((rh&ring).sum()/rh.sum()) if rh.any() else ''
        st['status']='read'
    except Exception as e:
        st['status']=str(e)
    finally:
        if gdal.VSIStatL(tmp) is not None:
            gdal.Unlink(tmp)
    return st
def main():
    arg=argparse.ArgumentParser()
    arg.add_argument('--out',type=Path,default=Path(__file__).parent)
    arg.add_argument('--cached',action='store_true')
    args=arg.parse_args()
    args.out.mkdir(exist_ok=True,parents=True)
    for site,(lon,lat,epsg,tile,windows) in SITES.items():
        reef=next((args.out/n for n in [site.lower()+'_reefs.geojson','koding_reefs.geojson'] if (args.out/n).exists() and (site=='Kodingareng' or n!='koding_reefs.geojson')),None)
        if reef is None:
            reef=args.out/(site.lower()+'_reefs.geojson')
            out=get_json(REEF,{'where':'1=1','geometry':','.join(str(a) for a in (lon-.045,lat-.045,lon+.045,lat+.045)),
                     'geometryType':'esriGeometryEnvelope','inSR':'4326','outSR':'4326','outFields':'OBJECTID','f':'geojson'})
            assert out['type']=='FeatureCollection' and out['features'],site
            reef.write_text(json.dumps(out))
        sr=wgs_epsg(epsg)
        cent=osr.CoordinateTransformation(wgs_epsg(4326),sr).TransformPoint(lon,lat)[:2]
        if args.cached:
            paths=({'historical':['tunda_history.json'],'baseline_check':['tunda_first.json','tunda_second.json']} if site=='Tunda' else
                   {'historical':['koding_history.json'],'baseline_check':['koding_first.json','koding_second.json']})
            tasks=[]
            for label, names in paths.items():
                unique={}
                for name in names:
                    for item in json.loads((args.out/'habitat_stac'/name).read_text())['features']:
                        day=item['properties']['datetime'][:10]
                        if f'_{tile}_' in item['id'] and item['assets']['scl']['href'].startswith('https://'):
                            unique[day]=item
                tasks.extend((label,item) for item in unique.values())
        else:
            tasks=[(label,f) for label,start,end in windows for f in catalog(lon,lat,tile,start,end)]
        print(site,'date groups',[(l,sum(x[0]==l for x in tasks)) for l,*_ in windows],flush=True)
        with ThreadPoolExecutor(max_workers=12) as pool:
            rows=list(pool.map(lambda row:analyze(row,cent,sr,reef),tasks))
        fields=list(dict.fromkeys(k for row in rows for k in row.keys()))
        with open(args.out/(site.lower()+'_habitat_scl.csv'),'w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields)
            w.writeheader()
            w.writerows(sorted(rows,key=lambda r:r['date']))
        print(site,'read',sum(r['status']=='read' for r in rows),flush=True)

if __name__=='__main__':
    main()
