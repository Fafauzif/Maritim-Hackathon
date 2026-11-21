#!/usr/bin/env python3
"""Enumerate and audit historical QA coverage for two fixed coastal footprints.
Run using Python with numpy and osgeo bindings. For Landsat only, public
Planetary Computer signing is used and the short-lived SAS is never persisted.
"""
import argparse
import csv
import json
import math
import time
import urllib.parse
import urllib.request
from calendar import monthrange
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from pathlib import Path

import numpy as np
from osgeo import gdal, ogr, osr

ROOT = Path(__file__).resolve().parent
SITES = {
    "Tunda": (106.27811, -5.81151, 32748, "48MXU"),
    "Kodingareng Lompo": (119.26473, -5.14905, 32750, "50MQV"),
}
END = date(2026, 10, 31)
START = date(2019, 1, 1)
L_START = date(2025, 1, 1)
QA_COLLECTIONS = {
    "Sentinel-2": ("https://earth-search.aws.element84.com/v1/search", "sentinel-2-c1-l2a", "scl"),
    "Landsat 8/9": ("https://planetarycomputer.microsoft.com/api/stac/v1/search", "landsat-c2-l2", "qa_pixel"),
}
FIELDS = ["site","sensor","date","utc","id","platform","catalog_cloud_pct","asset_url","epsg","cell_m","n_pixels","clear_pct","water_pct",
          "pct_ne","pct_nw","pct_se","pct_sw","reef_pixels","reef_clear_pct","reef_water_pct","status","error"]
gdal.UseExceptions()
for name, val in {
    "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    "GDAL_HTTP_TIMEOUT": "7",
    "GDAL_HTTP_MAX_RETRY": "1",
    "CPL_VSIL_CURL_USE_HEAD": "NO",
    "GDAL_HTTP_MULTIPLEX": "YES",
    "VSI_CACHE": "TRUE",
}.items():
    gdal.SetConfigOption(name, val)


def get_json(url):
    for try_no in range(3):
        try:
            with urllib.request.urlopen(url, timeout=12) as f:
                return json.load(f)
        except Exception:
            if try_no == 2:
                raise
            time.sleep(1 + try_no)


def windows(sensor):
    lo = START if sensor == "Sentinel-2" else L_START
    while lo < END:
        mo3 = lo.month + 2
        hi = min(END, date(lo.year, mo3, monthrange(lo.year, mo3)[1]))
        yield lo, hi
        lo = hi + timedelta(days=1)


def query(job):
    site, sensor, lo, hi = job
    url, coll, asset = QA_COLLECTIONS[sensor]
    x,y,epsg,tile = SITES[site]
    cache = ROOT / "cache" / (site.split()[0] + "_" + sensor.replace(" ", "").replace("/", "-") + f"_{lo:%Y%m%d}.json")
    if cache.exists():
        return json.loads(cache.read_text())
    bbox = ",".join(f"{k:.6f}" for k in (x-.033,y-.033,x+.033,y+.033))
    query_args = {"collections":coll,"bbox":bbox,"datetime":f"{lo}T00:00:00Z/{hi}T23:59:59Z","limit":"100"}
    page = get_json(url+"?"+urllib.parse.urlencode(query_args))
    matched = page.get("numberMatched")
    fs = list(page["features"])
    seen = set()
    while matched is None or len(fs) < matched:
        next_page = next((a["href"] for a in page.get("links",[]) if a["rel"]=="next"),None)
        if not next_page:
            break
        if next_page in seen:
            raise ValueError(f"Repeated pagination token: {job}")
        seen.add(next_page)
        page = get_json(next_page)
        fs.extend(page["features"])
    if matched is not None and matched != len(fs):
        raise ValueError(f"Partial catalog result for {job}")
    out = []
    for f in fs:
        p = f["properties"]
        if sensor == "Sentinel-2" and f"_T{tile}_" not in f["id"]:
            continue
        if sensor == "Landsat 8/9" and p.get("platform") not in {"landsat-8","landsat-9"}:
            continue
        out.append(dict(site=site,sensor=sensor,date=p["datetime"][:10],utc=p["datetime"],id=f["id"],
                        platform=p.get("platform",""),catalog_cloud_pct=p.get("eo:cloud_cover",""),
                        asset_url=f["assets"][asset]["href"]))
    cache.write_text(json.dumps(out))
    return out


def projected(x,y,srs):
    wgs = osr.SpatialReference()
    wgs.ImportFromEPSG(4326)
    wgs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    return osr.CoordinateTransformation(wgs, srs).TransformPoint(x, y)[:2]


def reef_mask(width, height, srs, geotransform):
    reef_path = ROOT / "tunda_reef.geojson"
    if not reef_path.exists():
        return None
    src = ogr.Open(str(reef_path))
    layer = src.GetLayer()
    src_srs = layer.GetSpatialRef()
    src_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    trans = osr.CoordinateTransformation(src_srs,srs)
    vector = ogr.GetDriverByName("Memory").CreateDataSource("")
    out = vector.CreateLayer("reef", srs)
    for feat in layer:
        geom = feat.GetGeometryRef().Clone()
        if geom.Transform(trans) != 0:
            raise ValueError("Failed to project historical reef")
        row = ogr.Feature(out.GetLayerDefn())
        row.SetGeometry(geom)
        out.CreateFeature(row)
    raster = gdal.GetDriverByName("MEM").Create("",width,height,1,gdal.GDT_Byte)
    raster.SetGeoTransform(geotransform)
    raster.SetSpatialRef(srs)
    gdal.RasterizeLayer(raster,[1],out,burn_values=[1])
    return raster.ReadAsArray() == 1


def fraction(array):
    return round(float(array.mean()) * 100, 6) if array.size else ""


def read(job):
    row, token, use_reef = job
    row = row.copy()
    try:
        is_s2 = row["sensor"] == "Sentinel-2"
        if not is_s2 and not token:
            raise ValueError("No authorized public SAS obtained")
        uri = row["asset_url"]
        if not is_s2:
            uri += "?" + token
        ds = gdal.Open("/vsicurl/" + uri)
        srs = ds.GetSpatialRef()
        x0, dx, xr, y0, yr, dy = ds.GetGeoTransform()
        if xr or yr or abs(dx+dy) > 1e-5 or dx not in (20,30):
            raise ValueError(f"Unexpected QA raster grid: {dx},{xr},{yr},{dy}")
        lon, lat, *_ = SITES[row["site"]]
        cx, cy = projected(lon, lat, srs)
        ix, iy = math.floor((cx-x0)/dx), math.floor((cy-y0)/dy)
        radius_px = math.ceil(3000/dx)+1
        left, top = ix-radius_px, iy-radius_px
        side = 2*radius_px+1
        if left < 0 or top < 0 or left+side > ds.RasterXSize or top+side > ds.RasterYSize:
            raise ValueError("QA raster does not span the local analysis window")
        values = ds.ReadAsArray(left, top, side, side)
        x = x0 + dx*(np.arange(left,left+side)+.5)-cx
        y = y0 + dy*(np.arange(top,top+side)+.5)-cy
        distance = np.hypot(x[None,:], y[:,None])
        mask = (distance>=1500)&(distance<=3000)
        if is_s2:
            view = np.isin(values,[2,4,5,6])
            water = values==6
        else:
            view = (values & 0x3f)==0
            water = view & ((values & 0x80)>0)
        row.update(epsg=srs.GetAuthorityCode(None),cell_m=dx,n_pixels=int(mask.sum()),
                   clear_pct=fraction(view[mask]),water_pct=fraction(water[mask]),status="ok")
        for suffix, q in {"ne":(x[None,:]>=0)&(y[:,None]>=0),"nw":(x[None,:]<0)&(y[:,None]>=0),
                          "se":(x[None,:]>=0)&(y[:,None]<0),"sw":(x[None,:]<0)&(y[:,None]<0)}.items():
            row[f"pct_{suffix}"]=fraction(view[mask&q])
        if row["site"]=="Tunda" and use_reef:
            reef = reef_mask(side,side,srs,(x0+left*dx,dx,0,y0+top*dy,0,dy))
            if reef is not None:
                reef &= distance <= 3000
                row.update(reef_pixels=int(reef.sum()),reef_clear_pct=fraction(view[reef]),reef_water_pct=fraction(water[reef]))
    except Exception as e:
        row.update(status="failed", error=str(e).split("?",1)[0][:250])
    return row


def run(args):
    (ROOT / "cache").mkdir(exist_ok=True)
    jobs=[(site,sensor,lo,hi) for sensor in args.sensor for site in SITES for lo,hi in windows(sensor)]
    with ThreadPoolExecutor(max_workers=12) as pool:
        rows=[r for out in pool.map(query,jobs) for r in out]
    rows.sort(key=lambda r:(r["site"],r["sensor"],r["utc"],r["id"]))
    if len({(r["site"], r["id"]) for r in rows}) != len(rows):
        raise ValueError("Duplicate scene ID")
    tag = ("sentinel" if args.sensor==["Sentinel-2"] else "landsat" if args.sensor==["Landsat 8/9"] else "full")
    fp=ROOT/f"{tag}_coverage.csv"
    fields=FIELDS
    token=None
    if "Landsat 8/9" in args.sensor and not args.catalog_only:
        token=get_json("https://planetarycomputer.microsoft.com/api/sas/v1/token/landsateuwest/landsat-c2")["token"]
    print(f"{tag}: {len(rows)} catalog rows",flush=True)
    if args.catalog_only:
        with fp.open("w") as f:
            w=csv.DictWriter(f,fields); w.writeheader();w.writerows(rows)
        return
    prior={}
    if fp.exists():
        with fp.open() as f:
            prior={(r["site"],r["id"]):r for r in csv.DictReader(f) if r["status"]=="ok"}
    checkpoint=fp.with_suffix(".pending.csv")
    with checkpoint.open("w") as f, ThreadPoolExecutor(max_workers=args.workers) as pool:
        w=csv.DictWriter(f,fields)
        w.writeheader()
        for row in prior.values():
            w.writerow(row)
        work=[pool.submit(read,(r,token,args.reef)) for r in rows if (r["site"],r["id"]) not in prior]
        out=list(prior.values())
        for i,done in enumerate(as_completed(work),1):
            row=done.result()
            out.append(row);w.writerow(row);f.flush()
            if i%100==0:
                print(f"{tag}: {i}/{len(work)} reads",flush=True)
    with fp.open("w") as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(sorted(out,key=lambda r:(r["site"],r["sensor"],r["utc"],r["id"])))
    checkpoint.unlink()
    print(f"{tag}: {len(out)} rows; {sum(r['status']!='ok' for r in out)} read errors")
    

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--sensor",action="append",choices=QA_COLLECTIONS)
    parser.add_argument("--workers",type=int,default=24)
    parser.add_argument("--reef",action="store_true")
    parser.add_argument("--catalog-only",action="store_true")
    a=parser.parse_args()
    a.sensor=a.sensor or list(QA_COLLECTIONS)
    run(a)
