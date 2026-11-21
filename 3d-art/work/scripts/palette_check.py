"""Compare a render's measured palette against the audit's referenced style.

The audit intake sets a target: six-colour palette of a render vs
`analysis/palette/italian.json`, weighted mean dE <= 6, and measured scene luma
/ saturation bands. This script measures exactly that, from PNG bytes, so the
comparison is a number instead of a claim.

Usage:
    python palette_check.py RENDER [--ref cityrt-audit/analysis/palette/italian.json]
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

D65 = np.array([0.95047, 1.00000, 1.08883])


def srgb_to_linear(c):
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def rgb_to_lab(rgb):
    """rgb in 0..1 sRGB -> CIE Lab (D65)."""
    lin = srgb_to_linear(np.clip(rgb, 0.0, 1.0))
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ m.T / D65
    f = np.where(xyz > 0.008856, np.cbrt(xyz), (7.787 * xyz) + 16.0 / 116.0)
    return np.stack([116.0 * f[..., 1] - 16.0,
                     500.0 * (f[..., 0] - f[..., 1]),
                     200.0 * (f[..., 1] - f[..., 2])], axis=-1)


def kmeans(points, k=6, iters=24, seed=3):
    rng = np.random.default_rng(seed)
    chosen = [points[rng.integers(len(points))]]
    for _ in range(k - 1):
        d = np.min(((points[:, None, :] - np.array(chosen)[None]) ** 2).sum(-1), axis=1)
        probs = d / d.sum()
        chosen.append(points[rng.choice(len(points), p=probs)])
    centres = np.array(chosen, dtype=np.float64)
    for _ in range(iters):
        d = ((points[:, None, :] - centres[None]) ** 2).sum(-1)
        labels = d.argmin(axis=1)
        for j in range(k):
            if np.any(labels == j):
                centres[j] = points[labels == j].mean(axis=0)
    counts = np.bincount(labels, minlength=k).astype(np.float64)
    weights = counts / counts.sum()
    order = np.argsort(weights)[::-1]
    return centres[order], weights[order]


def mean_saturation(rgb):
    mx = rgb.max(axis=-1)
    mn = rgb.min(axis=-1)
    return float(np.mean(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0.0)))


def measure(path):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    im = im.resize((320, max(1, int(320 * h / w))), Image.LANCZOS)
    rgb = np.asarray(im, dtype=np.float64) / 255.0
    flat = rgb.reshape(-1, 3)
    luma = 0.2126 * flat[:, 0] + 0.7152 * flat[:, 1] + 0.0722 * flat[:, 2]
    centres, weights = kmeans(flat, k=6)
    return {
        'file': path.replace('\\', '/'),
        'size': [w, h],
        'mean_luma': round(float(luma.mean()), 4),
        'luma_std': round(float(luma.std()), 4),
        'mean_saturation': round(mean_saturation(flat), 4),
        'palette': [
            {'hex': '#%02x%02x%02x' % tuple(int(round(c * 255)) for c in col),
             'srgb': [round(float(v), 3) for v in col],
             'weight': round(float(wt), 4)}
            for col, wt in zip(centres, weights)
        ],
        '_rgb': [col.tolist() for col in centres],
        '_weights': [float(w) for w in weights],
    }


def hex_to_rgb(value):
    value = value.lstrip('#')
    return [int(value[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]


def compare(measured, ref_path):
    with open(ref_path, encoding='utf-8') as fh:
        ref = json.load(fh)
    ref_cols = [hex_to_rgb(c['hex']) for c in ref['palette']['colors']]
    ref_w = [c['weight'] for c in ref['palette']['colors']]
    stats = ref['palette']['stats']

    ref_lab = rgb_to_lab(np.array(ref_cols))
    out_lab = rgb_to_lab(np.array(measured['_rgb']))
    d_est = np.sqrt(((ref_lab[:, None, :] - out_lab[None, :, :]) ** 2).sum(-1))
    nearest = d_est.min(axis=1)
    weighted_de = float(np.dot(nearest, np.array(ref_w)) / np.sum(ref_w))

    # which rendered colour each reference family landed on, for the write-up
    pairs = []
    for i, colour in enumerate(ref['palette']['colors']):
        j = int(d_est[i].argmin())
        pairs.append({'ref': colour['hex'], 'ref_weight': round(colour['weight'], 3),
                      'render': measured['palette'][j]['hex'],
                      'dE': round(float(nearest[i]), 2)})

    return {
        'reference': ref_path.replace('\\', '/'),
        'ref_mean_luma': round(stats['meanLuma'] / 255.0, 4),
        'ref_luma_std': round(stats['lumaStdDev'] / 255.0, 4),
        'ref_mean_saturation': round(stats['meanSaturation'], 4),
        'luma_delta': round(measured['mean_luma'] - stats['meanLuma'] / 255.0, 4),
        'sat_delta': round(measured['mean_saturation'] - stats['meanSaturation'], 4),
        'weighted_mean_dE': round(weighted_de, 2),
        'target_dE': 6.0,
        'pass': bool(weighted_de <= 6.0),
        'pairs': pairs,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('images', nargs='+')
    ap.add_argument('--ref', default=r'cityrt-audit\analysis\palette\italian.json')
    ap.add_argument('--json-out', default=None)
    args = ap.parse_args()

    report = {'ref': args.ref, 'renders': []}
    for path in args.images:
        m = measure(path)
        c = compare(m, args.ref)
        row = {k: v for k, v in m.items() if not k.startswith('_')}
        row['vs_ref'] = c
        report['renders'].append(row)
        print('%s  luma %.3f (ref %.3f, d%+.3f)  sat %.3f (ref %.3f, d%+.3f)  '
              'weighted dE %.2f  %s' % (
                  os.path.basename(path), m['mean_luma'], c['ref_mean_luma'],
                  c['luma_delta'], m['mean_saturation'], c['ref_mean_saturation'],
                  c['sat_delta'], c['weighted_mean_dE'],
                  'PASS' if c['pass'] else 'OVER-TARGET'))
        print('   palette: ' + '  '.join('%s(%.2f)' % (p['hex'], p['weight'])
                                         for p in m['palette']))
        worst = sorted(c['pairs'], key=lambda p: -p['dE'])[:3]
        print('   worst ref matches: ' + '; '.join(
            '%s->%s dE %.1f' % (p['ref'], p['render'], p['dE']) for p in worst))
    if args.json_out:
        tmp = args.json_out + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(report, fh, indent=2)
        os.replace(tmp, args.json_out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
