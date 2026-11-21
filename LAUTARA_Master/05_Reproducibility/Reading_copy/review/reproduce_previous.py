#!/usr/bin/env python3
"""Recalculate the original audit figures from the PDF's embedded scene tables."""
import argparse
import csv
import io
from datetime import date
from collections import defaultdict

import fitz

def parse(doc, attachment):
    return list(csv.DictReader(io.StringIO(doc.embfile_get(attachment).decode("utf-8-sig"))))

def use_screen(row, water, cloud, date_key, water_threshold, tile_threshold):
    return (date.fromisoformat(row[date_key]), float(row[water]) >= water_threshold, float(row[cloud]) <= tile_threshold)

def summarize(rows, water, cloud, date_key, water_threshold=90.0, tile_threshold=20.0):
    windows = defaultdict(list)
    for r in rows:
        windows[r["window"]].append(use_screen(r, water, cloud, date_key, water_threshold, tile_threshold))
    results = {}
    for window, v in windows.items():
        d, local, tile = zip(*sorted(v))
        assert len(set(d)) == len(d), "Deduplication rules needed when multiple rows share a date"
        ld = [u for u, l in zip(d, local) if l]
        td = [u for u, t in zip(d, tile) if t]
        period_gap = lambda days: max(((q-p).days for p,q in zip(days[:-1], days[1:])), default=None)
        results[window] = dict(days=len(d), tile=len(td), local=len(ld),
            local_only=len(set(ld)-set(td)), tile_only=len(set(td)-set(ld)),
            longest_pass_interval_days=(period_gap(ld), period_gap(td)))
    return results

def main():
    p = argparse.ArgumentParser()
    p.add_argument("pdf")
    a = p.parse_args()
    with fitz.open(a.pdf) as doc:
        tunda = parse(doc, "Tunda_110_Acquisitions.csv")
        koding = parse(doc, "Kodingareng_59_Acquisitions.csv")
        historical = parse(doc, "Tunda_2023_Event_Windows.csv")
        quadrants = parse(doc, "Tunda_Quadrant_Sensitivity.csv")
        primary = ("primary_water_percent", "tile_cloud_percent", "date")
        tp90 = summarize(tunda, *primary)
        tp95 = summarize(tunda, *primary, water_threshold=95.0)
        tp40 = summarize(tunda, *primary, tile_threshold=40.0)
        ks = summarize(koding, "water_1500_3000", "tile_cloud", "utc_date")
        print("Tunda, strict 90% local vs 20% tile:", tp90)
        print("Tunda at 95% local:", tp95)
        print("Tunda at 40% tile:", tp40)
        print("Kodingareng, strict 90% local vs 20% tile:", ks)
        print("Oct–Nov archive dates:", [item['utc_date'] for item in historical])
        print("19 Dec 2025:", {key: row[key] for row in quadrants if row["date"] == "2025-12-19" for key in ("primary_clear_percent","NE","NW","SE","SW")})
        assert sum(x["days"] for x in tp90.values()) == 110
        assert sum(x["local"] for x in tp90.values()) == 52
        assert sum(x["tile"] for x in tp90.values()) == 29
        assert sum(x["local_only"] for x in tp90.values()) == 23
        assert sum(x["days"] for x in ks.values()) == 59
        assert sum(x["local_only"] for x in ks.values()) == 1
        assert sum(x["tile_only"] for x in ks.values()) == 2
        assert "2023-10-27" not in [item["utc_date"] for item in historical]
        print("Original diagnostic anchors reproduced.")

if __name__ == "__main__":
    main()
