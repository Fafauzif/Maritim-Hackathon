"""Measure final PNGs (palette, contrast, edge density) and reference distances."""
import argparse
import json
import os

import numpy as np
from PIL import Image

REF_LUMA = 0.498
REF_SAT = 0.297


def stats(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255.0
    h, w, _ = a.shape
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    sat = np.where(mx > 1e-5, (mx - mn) / np.maximum(mx, 1e-5), 0)
    luma = 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]
    gx = np.abs(np.diff(luma, axis=1))
    gy = np.abs(np.diff(luma, axis=0))
    edge = float(((gx > 0.08).mean() + (gy > 0.08).mean()) / 2)
    # 3x3 tile luma for layout consistency
    tiles = []
    for j in range(3):
        row = []
        for i in range(3):
            t = luma[j * h // 3:(j + 1) * h // 3, i * w // 3:(i + 1) * w // 3]
            row.append(round(float(t.mean()), 3))
        tiles.append(row)
    return {
        "size": [w, h],
        "meanRgb": [round(float(x), 4) for x in a.mean(axis=(0, 1))],
        "luma": round(float(luma.mean()), 4),
        "sat": round(float(sat.mean()), 4),
        "edgeDensity": round(edge, 5),
        "darkShare": round(float((luma < 0.12).mean()), 4),
        "brightShare": round(float((luma > 0.9).mean()), 4),
        "tilesLuma": tiles,
        "referenceDelta": {"luma": round(float(luma.mean()) - REF_LUMA, 4),
                           "sat": round(float(sat.mean()) - REF_SAT, 4)},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    base = os.path.join(a.run_root, "renders", "final-4k")
    out = {}
    for site in ("kodingareng", "tunda", "amur"):
        for slug in ("godview", "mapview", "approach", "detail", "section"):
            p = os.path.join(base, site, slug + ".png")
            if os.path.exists(p):
                out["%s/%s" % (site, slug)] = stats(p)
    p = os.path.join(base, "globe", "globe-overview.png")
    if os.path.exists(p):
        out["globe/overview"] = stats(p)
    p = os.path.join(a.run_root, "proofs", "look", "kit_asset-sheet.png")
    if os.path.exists(p):
        out["kit/asset-sheet"] = stats(p)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    for k, v in out.items():
        print(k, "luma", v["luma"], "sat", v["sat"], "edge", v["edgeDensity"],
              "bright", v["brightShare"])


if __name__ == "__main__":
    main()
