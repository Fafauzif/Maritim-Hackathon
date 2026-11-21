"""Phase 06 · assemble the delivery: stills, contact sheets, parity sheet.

Copies the rendered 4K stills into the exact output contract paths, builds
`output/review/parity-sheet.png` (three coasts side by side, equal scale) and
`output/kit/asset-sheet.png`, and prints a manifest of what it placed.

    python assemble_outputs.py
"""
import json
import os
import shutil

from PIL import Image

import contact_sheet as CS

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
RENDERS = os.path.join(ART, 'work', 'renders')
OUTPUT = os.path.join(ART, 'output')
SITES = ('kodingareng', 'tunda', 'amur')
REPORT = os.path.join(ART, 'work', 'reports', 'assemble.json')


def copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    im = Image.open(dst)
    return {'path': dst.replace('\\', '/'), 'bytes': os.path.getsize(dst),
            'size': list(im.size)}


def main():
    manifest = {'stills': [], 'sheets': [], 'missing': []}

    mapping = {
        'globe_overview.png': os.path.join(OUTPUT, 'globe', 'globe-overview.png'),
    }
    for site in SITES:
        for slug, name in (('godview', 'godview.png'), ('mapview', 'mapview.png'),
                           ('section', 'section.png')):
            mapping['%s_%s.png' % (site, slug)] = os.path.join(
                OUTPUT, 'coasts', site, name)

    for src_name, dst in mapping.items():
        src = os.path.join(RENDERS, 'final-4k', src_name)
        if not os.path.exists(src):
            manifest['missing'].append(src.replace('\\', '/'))
            continue
        manifest['stills'].append(copy(src, dst))

    # asset sheet
    sheet_src = os.path.join(RENDERS, 'kit', 'asset-sheet.png')
    if os.path.exists(sheet_src):
        manifest['sheets'].append(copy(sheet_src, os.path.join(OUTPUT, 'kit', 'asset-sheet.png')))
    else:
        manifest['missing'].append(sheet_src.replace('\\', '/'))

    # parity sheet: one row per coast, godview / mapview / section at equal scale
    items = []
    labels = []
    for site in SITES:
        label = {'kodingareng': 'Kodingareng Lompo', 'tunda': 'Pulau Tunda',
                 'amur': 'Razdolnaya / Amur'}[site]
        for slug, name in (('godview', 'GOD VIEW'), ('mapview', 'MAP VIEW'),
                           ('section', 'SECTION')):
            path = os.path.join(RENDERS, 'final-4k', '%s_%s.png' % (site, slug))
            if not os.path.exists(path):
                continue
            items.append((path, '%s · %s' % (label, name)))
    if len(items) == 9:
        out = os.path.join(OUTPUT, 'review', 'parity-sheet.png')
        info = CS.sheet(items, out, cols=3, thumb_w=1200, caption_h=40,
                        title='The Ocean Has Floors - coast parity, equal 3840x2160 source, 1200 px tiles')
        manifest['sheets'].append({'path': out.replace('\\', '/'),
                                   'bytes': info['bytes'], 'size': info['size'],
                                   'tiles': info['items']})
    else:
        manifest['missing'].append('parity source tiles: %d/9' % len(items))

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    tmp = REPORT + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, indent=2)
    os.replace(tmp, REPORT)
    print('ASSEMBLE placed', len(manifest['stills']), 'stills,',
          len(manifest['sheets']), 'sheets; missing', len(manifest['missing']))
    for entry in manifest['missing']:
        print('  MISSING', entry)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
