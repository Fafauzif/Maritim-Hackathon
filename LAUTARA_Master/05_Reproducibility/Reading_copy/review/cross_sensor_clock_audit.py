#!/usr/bin/env python3
"""Inventory scoped image acquisitions and metadata clocks around the Tunda inspection."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
BBOX = "106.198,-5.857,106.327,-5.764"
WINDOW = "2023-10-12T00:00:00Z/2023-11-11T23:59:59Z"
CATALOGS = [
    ("element84-s2", "https://earth-search.aws.element84.com/v1/search", "sentinel-2-c1-l2a"),
    ("element84-l89", "https://earth-search.aws.element84.com/v1/search", "landsat-c2-l2"),
    ("mpc-l89", "https://planetarycomputer.microsoft.com/api/stac/v1/search", "landsat-c2-l2"),
    ("nasa-hls-l30", "https://cmr.earthdata.nasa.gov/stac/LPCLOUD/search", "HLSL30.v2.0"),
    ("nasa-hls-s30", "https://cmr.earthdata.nasa.gov/stac/LPCLOUD/search", "HLSS30.v2.0"),
    ("copernicus-s1", "https://stac.dataspace.copernicus.eu/v1/search", "sentinel-1-grd"),
    ("copernicus-s2", "https://stac.dataspace.copernicus.eu/v1/search", "sentinel-2-l2a"),
]

def query(spec, refresh=False):
    name, endpoint, collection = spec
    path = ROOT / f"tunda_event_{name}.json"
    q = urlencode(dict(bbox=BBOX, datetime=WINDOW, collections=collection, limit=100))
    if path.exists() and not refresh:
        res = json.loads(path.read_text())
    else:
        with urlopen(f"{endpoint}?{q}", timeout=40) as f:
            res = json.load(f)
        path.write_text(json.dumps(res))
    features = res["features"]
    matched = res.get("numberMatched") or res.get("context", {}).get("matched")
    if (matched is not None and matched != len(features)) or len(features) == 100:
        raise RuntimeError(f"{name} requires pagination. Recheck the query scope.")
    return [
        {
            "query": name,
            "scene": feat["id"],
            "platform": f.get("platform"),
            "acquisition": f.get("datetime") or f.get("start_datetime"),
            "catalog_created": f.get("created"),
            "updated": f.get("updated"),
            "published": f.get("published"),
            "cloud": f.get("eo:cloud_cover"),
            "landsat_collection_category": f.get("landsat:collection_category"),
            "processing_time": f.get("s2:generation_time") or f.get("processing:datetime"),
            "product_baseline": f.get("s2:processing_baseline") or f.get("processing:version"),
            "sentinel_product_id": f.get("s2:product_uri") or f.get("s2:product_id"),
        }
        for feat in features for f in [feat.get("properties", {})]
    ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="request current catalog data")
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = [r for batch in pool.map(lambda spec: query(spec, args.refresh), CATALOGS) for r in batch]
    with (ROOT / "tunda_event_sensor_clocks.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for name, _, _ in CATALOGS:
        dates = sorted({r["acquisition"][:10] for r in rows if r["query"] == name})
        print(name, len(dates), ", ".join(dates))
    assert all(r["acquisition"][:10] != "2023-10-27" for r in rows), "A same-day scene is listed. Revisit the finding."

if __name__ == "__main__":
    main()
