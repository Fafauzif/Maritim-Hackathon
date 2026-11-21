"""Contact sheets + numeric render verification for The Ocean Has Floors.

No image is ever attached to the conversation: every render is measured with
Pillow/numpy and, when a human review is wanted, tiled into ONE sheet on disk.

Usage (bundled python):
    python contact_sheet.py stats  <glob-or-dir> [more...]
    python contact_sheet.py sheet  --out PATH --cols N --thumb W image=LABEL ...
    python contact_sheet.py parity --site kodingareng ...
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BG = (26, 26, 30)
FG = (238, 238, 230)
ACCENT = (200, 180, 120)


# ----------------------------------------------------------------------------
# measurement
# ----------------------------------------------------------------------------

def measure(path):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im, dtype=np.float32) / 255.0
    h, w, _ = a.shape
    luma = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

    # sharpness: variance of a 4-neighbour Laplacian on luma
    lap = (4 * luma[1:-1, 1:-1] - luma[:-2, 1:-1] - luma[2:, 1:-1]
           - luma[1:-1, :-2] - luma[1:-1, 2:])
    sharp = float(lap.var())

    # quantised colour spread: how many 32-step buckets hold 99% of pixels
    q = (a * 7.999).astype(np.int32)
    codes = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
    counts = np.bincount(codes.ravel(), minlength=512)
    order = np.argsort(counts)[::-1]
    cum = np.cumsum(counts[order]) / float(w * h)
    buckets99 = int(np.searchsorted(cum, 0.99) + 1)

    # background estimate from the 4 corner blocks (16 px)
    k = max(4, min(h, w) // 32)
    corners = np.concatenate([a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3),
                              a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3)])
    bg = corners.mean(axis=0)
    dist = np.abs(a - bg).sum(axis=2)
    content = dist > 0.18

    def edge_frac(mask):
        n = {'top': mask[0].mean(), 'bottom': mask[-1].mean(),
             'left': mask[:, 0].mean(), 'right': mask[:, -1].mean()}
        return {key: round(float(v), 3) for key, v in n.items()}

    return {
        'path': path.replace('\\', '/'),
        'bytes': os.path.getsize(path),
        'wh': [w, h],
        'mean_rgb': [round(float(a[..., i].mean()), 4) for i in range(3)],
        'luma_mean': round(float(luma.mean()), 4),
        'luma_std': round(float(luma.std()), 4),
        'sharpness_lapvar': round(sharp, 1),
        'color_buckets_99pct': buckets99,
        'content_frac': round(float(content.mean()), 4),
        'edge_content': edge_frac(content),
        'near_black_frac': round(float((luma < 0.02).mean()), 4),
        'near_white_frac': round(float((luma > 0.98).mean()), 4),
    }


def stats(paths):
    rows = [measure(p) for p in paths]
    for r in rows:
        e = r['edge_content']
        print(f"{r['path']:58s} {r['wh'][0]}x{r['wh'][1]} "
              f"luma={r['luma_mean']:.3f}/{r['luma_std']:.3f} "
              f"sharp={r['sharpness_lapvar']:>9.1f} "
              f"content={r['content_frac']:.3f} "
              f"buckets={r['color_buckets_99pct']:>3d} "
              f"edges T{e['top']:.2f} B{e['bottom']:.2f} "
              f"L{e['left']:.2f} R{e['right']:.2f} "
              f"black={r['near_black_frac']:.3f} white={r['near_white_frac']:.3f}")
    return rows


# ----------------------------------------------------------------------------
# sheet composition
# ----------------------------------------------------------------------------

def _font(size):
    for candidate in (r'C:\Windows\Fonts\segoeui.ttf',
                      r'C:\Windows\Fonts\arial.ttf',
                      r'C:\Windows\Fonts\consola.ttf'):
        if os.path.exists(candidate):
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                pass
    return ImageFont.load_default()


def sheet(items, out, cols=3, thumb_w=640, caption_h=34, title=None):
    """items: list of (path, label). One PNG on disk, never an inline image."""
    thumbs = []
    for path, label in items:
        im = Image.open(path).convert('RGB')
        w, h = im.size
        th = int(round(thumb_w * h / w))
        thumbs.append((im.resize((thumb_w, th), Image.LANCZOS), label, th))
    cell_h = max(t[2] for t in thumbs) + caption_h
    rows = (len(thumbs) + cols - 1) // cols
    header = 56 if title else 0
    W = cols * thumb_w + (cols + 1) * 12
    H = header + rows * (cell_h + 12) + 12
    canvas = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    if title:
        draw.text((14, 12), title, font=_font(24), fill=FG)
    f = _font(16)

    def fit(label, width):
        size = 16
        while size > 8:
            font = _font(size)
            if draw.textlength(label, font=font) <= width - 4:
                return font, label
            size -= 1
        font = _font(8)
        while label and draw.textlength(label + '...', font=font) > width - 4:
            label = label[:-1]
        return font, label + '...'

    for i, (im, label, th) in enumerate(thumbs):
        r, c = divmod(i, cols)
        x = 12 + c * (thumb_w + 12)
        y = header + 12 + r * (cell_h + 12)
        canvas.paste(im, (x, y))
        font, text = fit(label, thumb_w)
        draw.text((x + 2, y + th + 8), text, font=font, fill=ACCENT)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out, optimize=True)
    return {'path': out, 'size': [W, H], 'items': len(items),
            'bytes': os.path.getsize(out)}


def downsample(paths, out_dir, widths=(320,)):
    os.makedirs(out_dir, exist_ok=True)
    made = []
    for p in paths:
        im = Image.open(p).convert('RGB')
        for w in widths:
            h = int(round(w * im.size[1] / im.size[0]))
            target = os.path.join(out_dir, f'{os.path.splitext(os.path.basename(p))[0]}_{w}.png')
            im.resize((w, h), Image.LANCZOS).save(target, optimize=True)
            made.append({'path': target, 'wh': [w, h]})
    return made


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='cmd', required=True)

    sp = sub.add_parser('stats')
    sp.add_argument('paths', nargs='+')

    ss = sub.add_parser('sheet')
    ss.add_argument('--out', required=True)
    ss.add_argument('--cols', type=int, default=3)
    ss.add_argument('--thumb', type=int, default=640)
    ss.add_argument('--title', default=None)
    ss.add_argument('items', nargs='+', help='path=LABEL')

    sd = sub.add_parser('down')
    sd.add_argument('--out-dir', required=True)
    sd.add_argument('--widths', default='320')
    sd.add_argument('paths', nargs='+')

    args = ap.parse_args(argv)

    if args.cmd == 'stats':
        expanded = []
        for p in args.paths:
            if os.path.isdir(p):
                for name in sorted(os.listdir(p)):
                    if name.lower().endswith('.png'):
                        expanded.append(os.path.join(p, name))
            else:
                expanded.append(p)
        stats(expanded)
        return 0

    if args.cmd == 'down':
        widths = [int(x) for x in args.widths.split(',')]
        print(json.dumps(downsample(args.paths, args.out_dir, widths), indent=2))
        return 0

    items = []
    for raw in args.items:
        path, _, label = raw.partition('=')
        items.append((path, label or os.path.basename(path)))
    print(json.dumps(sheet(items, args.out, cols=args.cols, thumb_w=args.thumb,
                           title=args.title), indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
