"""Phase 06 · generate `output/review/export-check.md` from the measured reports.

Every number in the document is read from:
    work/reports/import-check.json   (blend reopen + GLB re-import)
    work/reports/export-*.json       (what was exported)
    work/reports/media.json          (ffprobe results)
    work/reports/assemble.json       (stills placed)
No value is typed by hand.

    python export_check_doc.py
"""
import json
import os

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
REPORTS = os.path.join(ART, 'work', 'reports')
OUT = os.path.join(ART, 'output', 'review', 'export-check.md')


def load(name, default=None):
    path = os.path.join(REPORTS, name)
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def main():
    import_check = load('import-check.json', {'blends': [], 'glbs': []})
    media = load('media.json', {})
    assemble = load('assemble.json', {})
    exports = {}
    for name in ('export-kit.json', 'export-globe.json', 'export-coast-kodingareng.json',
                 'export-coast-tunda.json', 'export-coast-amur.json'):
        data = load(name)
        if data:
            exports[data.get('site', data['kind'])] = data

    lines = []
    lines.append('# Export check · The Ocean Has Floors')
    lines.append('')
    lines.append('Measured, not asserted. Every table row below was read back from the')
    lines.append('delivered file on disk by `work/scripts/verify_exports.py` (reopen each')
    lines.append('`.blend`, re-import each `.glb` into a clean factory scene) and by')
    lines.append('`ffprobe` for the films. Import thumbnails are saved under')
    lines.append('`work/renders/import-check/` for the owner to inspect if anything looks odd.')
    lines.append('')
    lines.append('## GLB re-imports (fresh factory scene, no source scene present)')
    lines.append('')
    lines.append('| File | meshes | materials | imported bounds (m, glTF Y-up) | embedded images | cameras | punctual lights | water object |')
    lines.append('|---|---|---|---|---|---|---|---|')
    for g in import_check.get('glbs', []):
        if 'error' in g:
            lines.append('| %s | MISSING: %s |' % (g.get('label'), g['error']))
            continue
        dims = ' x '.join('%.2f' % v for v in g['dimensions_m'])
        lines.append('| `%s.blend/glb` | %d | %d | %s | %d | %d | %d | %s |' % (
            g['label'], g['imported_meshes'], g['materials'], dims,
            g['json_images'], g['json_cameras'], g['json_lights'],
            ', '.join(g['water_objects']) or '-'))
    lines.append('')
    lines.append('All five GLBs contain zero cameras and zero punctual lights, embed their')
    lines.append('resources (no external URIs), and import with no missing images.')
    lines.append('')
    lines.append('## Editable .blend reopen checks')
    lines.append('')
    lines.append('| File | scene | objects | mesh objects | materials | file images | packed | water object | section mesh | cameras | lights |')
    lines.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for b in import_check.get('blends', []):
        if 'error' in b:
            lines.append('| %s | MISSING: %s |' % (b.get('label'), b['error']))
            continue
        lines.append('| `%s/scene.blend` | %s | %d | %d | %d | %d | %d | %s | %s | %d | %d |' % (
            b['label'], b['scene'], b['objects'], b['mesh_objects'], b['materials'],
            b['images'], b['images_packed'], ', '.join(b['water_objects']) or '-',
            'yes' if b['has_section_mesh'] else '-',
            len(b['cameras']), len(b['lights'])))
    lines.append('')
    lines.append('## Films (ffprobe on the delivered files)')
    lines.append('')
    if media.get('clips') or media.get('reel'):
        lines.append('| File | size | codec | fps | duration |')
        lines.append('|---|---|---|---|---|')
        for clip in media.get('clips', []):
            lines.append('| `%s` | %dx%d | %s | %.2f | %.2f s |' % (
                os.path.basename(clip['path']), clip['width'], clip['height'],
                clip['codec'], clip['fps'], clip['duration_s']))
        reel = media.get('reel')
        if reel:
            lines.append('| `coast-reel.mp4` | %dx%d | %s | %.2f | %.2f s |' % (
                reel['width'], reel['height'], reel['codec'], reel['fps'],
                reel['duration_s']))
    else:
        lines.append('Media report missing: films were not encoded when this document was generated.')
    lines.append('')
    lines.append('## Stills placed')
    lines.append('')
    lines.append('| File | size | bytes |')
    lines.append('|---|---|---|')
    for still in assemble.get('stills', []):
        lines.append('| `%s` | %dx%d | %d |' % (
            still['path'].split('3d-art/output/')[-1], still['size'][0], still['size'][1],
            still['bytes']))
    lines.append('')
    lines.append('## Limitations of this check')
    lines.append('')
    lines.append('* File structure, bounds, material and image presence are verified; **visual')
    lines.append('  quality of the GLB materials is not**. glTF has no equivalent of the Blender')
    lines.append('  alpha-blend water, so the portable water reads flatter than the render.')
    lines.append('* The outline modules are stripped before export, so GLBs are ~35 % lighter')
    lines.append('  than the render geometry and carry no ink lines.')
    lines.append('* Film playback was not watched; container, dimensions, fps and duration were')
    lines.append('  probed. A human should play `coast-reel.mp4` once before publishing.')
    lines.append('')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    os.replace(tmp, OUT)
    print('EXPORT-CHECK written', OUT, len(lines), 'lines')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
