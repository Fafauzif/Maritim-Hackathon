"""Phase 04 · split a travel scene into its two render passes.

Blender 5.2 cannot keyframe `Collection.hide_render`, and rendering both passes
from one session hung the headless renderer. The film is therefore rendered as
two scene files with fixed visibility:

    04-travelA-<site>.blend   frames 1-108   surface world, travel camera
    04-travelB-<site>.blend   frames 109-132 cutaway, section camera

Both write into the same `frame_####.png` sequence, so the two shots concatenate
into one film at encode time.

    python-free; run inside Blender:
    import travel_passes; travel_passes.build_all()
"""
import os
import sys

import bpy

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
CHECKPOINTS = os.path.join(ART, 'work', 'checkpoints')
FRAMES = os.path.join(ART, 'work', 'renders', 'travel-frames')

CUT_FRAME = 109
END_FRAME = 132
SURFACE = ('ENV_Land', 'ENV_Water', 'BLD_Village', 'VEG_Scatter')


def _set_visibility(section_visible):
    for name in SURFACE:
        coll = bpy.data.collections.get(name)
        if coll:
            coll.hide_render = section_visible
    sec = bpy.data.collections.get('SEC_Section')
    if sec:
        sec.hide_render = not section_visible


def _save(site, tag, start, end, section_visible):
    scene = bpy.context.scene
    _set_visibility(section_visible)
    scene.frame_start = start
    scene.frame_end = end
    scene.render.filepath = os.path.join(FRAMES, site, 'frame_')
    if section_visible:
        cam = bpy.data.objects.get('COAST_SECTION')
        if cam:
            scene.camera = cam
    else:
        cam = bpy.data.objects.get('TRAVEL_CAM')
        if cam:
            scene.camera = cam
    out = os.path.join(CHECKPOINTS, '04-travel%s-%s.blend' % (tag, site))
    bpy.ops.wm.save_as_mainfile(filepath=out)
    return out


def build(site):
    src = os.path.join(CHECKPOINTS, '04-travel-%s.blend' % site)
    bpy.ops.wm.open_mainfile(filepath=src)
    a = _save(site, 'A', 1, CUT_FRAME - 1, False)
    bpy.ops.wm.open_mainfile(filepath=src)
    b = _save(site, 'B', CUT_FRAME, END_FRAME, True)
    return {'site': site, 'passA': a, 'passB': b}


def build_all():
    out = {}
    for site in ('kodingareng', 'tunda', 'amur'):
        out[site] = build(site)
    print('TRAVEL-PASSES', {k: (v['passA'].split('\\')[-1], v['passB'].split('\\')[-1])
                           for k, v in out.items()})
    return out
