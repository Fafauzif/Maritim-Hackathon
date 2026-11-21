"""Does the shot still read at 320 px?

The brief puts a hard test on the proofs: "at 320 px, name the distinct shape,
shore anchor and boat for each coast". This script measures that instead of
asserting it:

* the survey boat's projected pixel box (from verify_shot.py) is rescaled to the
  320 px derivative and compared against a ring of surrounding pixels, so we
  know whether the boat separates from the water behind it;
* Otsu thresholding splits the thumbnail into two luma classes and reports the
  minority share, which is the silhouette surviving the shrink.

Usage (bundled python):
    python verify_320.py work/verification/shot-verify.json
"""
import json
import os
import sys

import numpy as np
from PIL import Image

ART = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ring_contrast(gray, box):
    h, w = gray.shape
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w - 1, x1), min(h - 1, y1)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return None
    inner = gray[y0:y1, x0:x1]
    pad = max(3, (x1 - x0) // 2)
    ox0, oy0 = max(0, x0 - pad), max(0, y0 - pad)
    ox1, oy1 = min(w, x1 + pad), min(h, y1 + pad)
    outer = gray[oy0:oy1, ox0:ox1].copy()
    outer[(oy0 - y0):(oy0 - y0) + inner.shape[0],
          (ox0 - x0):(ox0 - x0) + inner.shape[1]] = np.nan
    outer_mean = float(np.nanmean(outer))
    inner_mean = float(inner.mean())
    span = float(inner.max() - inner.min())
    return {'inner_mean': round(inner_mean, 4), 'ring_mean': round(outer_mean, 4),
            'abs_delta': round(abs(inner_mean - outer_mean), 4),
            'inner_span': round(span, 4)}


def otsu(gray):
    hist, _ = np.histogram(gray, bins=64, range=(0.0, 1.0))
    total = hist.sum()
    if total == 0:
        return None
    centre = (np.arange(64) + 0.5) / 64.0
    w0 = np.cumsum(hist) / total
    m0 = np.cumsum(hist * centre) / np.maximum(np.cumsum(hist), 1)
    m1 = (np.cumsum((hist * centre)[::-1])[::-1] / np.maximum(np.cumsum(hist)[::-1], 1))[::-1]
    between = w0 * (1 - w0) * (m0 - m1) ** 2
    k = int(np.nanargmax(between))
    thr = centre[k]
    frac = float((gray < thr).mean())
    return {'threshold': round(float(thr), 4), 'dark_frac': round(frac, 4),
            'split_ok': bool(0.04 <= frac <= 0.96)}


def main():
    report_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        ART, 'work', 'verification', 'shot-verify.json')
    with open(report_path, encoding='utf-8') as fh:
        report = json.load(fh)

    out = {'shots': {}}
    for site, data in report['sites'].items():
        for cam, shot in data['shots'].items():
            if cam not in ('COAST_OVERVIEW', 'COAST_SECTION'):
                continue
            boat = shot.get('PROP_SurveyBoat') or {}
            base = 'kodingareng' if site == 'kodingareng' else site
            thumb_dir = os.path.join(ART, 'work', 'renders', 'blockout', '320')
            thumb = os.path.join(thumb_dir, '%s_%s_320.png' % (site, 'overview' if cam == 'COAST_OVERVIEW' else 'section'))
            entry = {'thumb': thumb.replace('\\', '/')}
            if not os.path.exists(thumb):
                entry['error'] = 'no 320 derivative'
                out['shots']['%s/%s' % (site, cam)] = entry
                continue
            gray = np.asarray(Image.open(thumb).convert('L'), dtype=np.float32) / 255.0
            scale = 320.0 / 960.0
            if boat.get('px_bbox'):
                # verify_shot reports Blender view coordinates (origin bottom-left);
                # PIL rows start at the top, so the y pair has to be flipped.
                bx0, by0, bx1, by1 = boat['px_bbox']
                box = [bx0 * scale, (540.0 - by1) * scale,
                       bx1 * scale, (540.0 - by0) * scale]
                entry['boat_box_320'] = [round(v, 1) for v in box]
                entry['boat_contrast'] = ring_contrast(gray, box)
                entry['boat_reads'] = bool(
                    entry['boat_contrast'] and
                    (entry['boat_contrast']['abs_delta'] >= 0.035 or
                     entry['boat_contrast']['inner_span'] >= 0.12))
            entry['thumbnail'] = otsu(gray)
            out['shots']['%s/%s' % (site, cam)] = entry

    target = os.path.join(ART, 'work', 'verification', 'verify-320.json')
    tmp = target + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2)
    os.replace(tmp, target)

    for key, entry in out['shots'].items():
        c = entry.get('boat_contrast') or {}
        t = entry.get('thumbnail') or {}
        print('%-24s boat %s dL=%.3f span=%.3f reads=%s | otsu dark=%.2f split=%s' % (
            key,
            entry.get('boat_box_320'),
            c.get('abs_delta', -1), c.get('inner_span', -1),
            entry.get('boat_reads'),
            t.get('dark_frac', -1), t.get('split_ok')))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
