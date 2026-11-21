"""Text-mode look at a render: coarse luminance map plus band statistics.

This is the replacement for attaching an image to the conversation. It prints
ASCII so the shape can be judged from numbers alone, and refuses to be a
substitute for a real review: it says what the pixels are, not whether they are
beautiful.

Usage:
    python ascii_probe.py IMAGE [IMAGE ...] [--grid 56x22] [--bands 6]
"""
import argparse

import numpy as np
from PIL import Image

CHARS = " .:-=+*#%@"


def probe(path, gw=56, gh=22, bands=6):
    im = Image.open(path).convert('L')
    small = np.asarray(im.resize((gw, gh), Image.BOX), dtype=np.float32) / 255.0
    lo, hi = float(small.min()), float(small.max())
    print('== %s  %dx%d  luma %.3f..%.3f' % (path, im.size[0], im.size[1], lo, hi))
    for row in small:
        print('   |' + ''.join(CHARS[min(9, int((v - lo) / (hi - lo + 1e-6) * 9.999))]
                              for v in row) + '|')

    full = np.asarray(im, dtype=np.float32) / 255.0
    h, w = full.shape
    step = h // bands
    print('   horizontal bands (top -> bottom):')
    for b in range(bands):
        strip = full[b * step:(b + 1) * step if b < bands - 1 else h]
        print('     band %d  luma %.3f  std %.3f  p10 %.3f  p90 %.3f' % (
            b, strip.mean(), strip.std(),
            np.percentile(strip, 10), np.percentile(strip, 90)))
    # left/right third balance: composition check without eyes
    third = w // 3
    print('   vertical thirds luma: L %.3f  C %.3f  R %.3f' % (
        full[:, :third].mean(), full[:, third:2 * third].mean(),
        full[:, 2 * third:].mean()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('images', nargs='+')
    ap.add_argument('--grid', default='56x22')
    ap.add_argument('--bands', type=int, default=6)
    args = ap.parse_args()
    gw, gh = (int(v) for v in args.grid.lower().split('x'))
    for path in args.images:
        probe(path, gw, gh, args.bands)


if __name__ == '__main__':
    main()
