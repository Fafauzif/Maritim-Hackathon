"""Phase 04 · per-coast travel camera: overview -> approach -> lateral -> cutaway.

Loads a saved `03-<site>.blend`, adds an animated `TRAVEL_CAM` (tracked to a
`TRAVEL_TARGET` empty), binds the section camera to a timeline marker at the cut,
sets 1920x1080 / 24 fps render settings and saves `04-travel-<site>.blend`.
The film is then rendered headless so the interactive session stays usable.

Run inside Blender:
    import travel_build; travel_build.build('kodingareng')
"""
import math
import os
import sys

import bpy
from mathutils import Vector

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
SCRIPTS = os.path.join(ART, 'work', 'scripts')
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

CHECKPOINTS = os.path.join(ART, 'work', 'checkpoints')
FRAMES = os.path.join(ART, 'work', 'renders', 'travel-frames')

CUT_FRAME = 109
END_FRAME = 132   # 5.5 s at 24 fps


def _look_at(obj, target_ob):
    con = obj.constraints.new('TRACK_TO')
    con.target = target_ob
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    return con


def build(site_key, save=True):
    import scene_build as SC
    import site_build as SB

    src = os.path.join(CHECKPOINTS, '03-%s.blend' % site_key)
    bpy.ops.wm.open_mainfile(filepath=src)
    scene = bpy.context.scene
    site = SB.SITES[site_key]

    coll = bpy.data.collections.get('CAM_Travel')
    if coll is None:
        coll = bpy.data.collections.new('CAM_Travel')
        scene.collection.children.link(coll)

    # ---- travel camera -----------------------------------------------------
    cam = SC.make_camera('TRAVEL_CAM', 58.0, coll)
    tgt = SC.make_empty('TRAVEL_TARGET', site['overview']['target'], coll, 3.0)
    _look_at(cam, tgt)

    ov_pos = Vector(site['overview']['pos'])
    ov_tgt = Vector(site['overview']['target'])
    ap_pos = Vector(site['approach']['pos'])
    ap_tgt = Vector(site['approach']['target'])

    # lateral axis: perpendicular to the approach look direction, in the ground plane
    look = (ap_tgt - ap_pos)
    look.z = 0.0
    look.normalize()
    side = Vector((-look.y, look.x, 0.0))
    lateral_pos = ap_pos + side * 20.0
    lateral_tgt = ap_tgt + side * 6.0
    boat = Vector((site['boat'][0], site['boat'][1], 2.0))
    push_pos = ap_pos.lerp(boat, 0.28)
    push_tgt = ap_tgt.lerp(boat, 0.35)

    for frame, pos, tgt_pos in (
            (1, ov_pos, ov_tgt),
            (52, ap_pos, ap_tgt),
            (78, lateral_pos, lateral_tgt),
            (CUT_FRAME - 1, push_pos, push_tgt)):
        cam.location = pos
        cam.keyframe_insert('location', frame=frame)
        tgt.location = tgt_pos
        tgt.keyframe_insert('location', frame=frame)

    # ---- cut to the cutaway ------------------------------------------------
    for marker in list(scene.timeline_markers):
        scene.timeline_markers.remove(marker)
    m1 = scene.timeline_markers.new('TRAVEL_OVERVIEW', frame=1)
    m1.camera = cam
    m2 = scene.timeline_markers.new('TRAVEL_CUTAWAY', frame=CUT_FRAME)
    m2.camera = bpy.data.objects.get('COAST_SECTION')

    # Blender 5.2 refuses to keyframe Collection.hide_render, so the cutaway is
    # rendered as a second pass with its own fixed visibility (see
    # render_pass.py::travel) and the two shots are concatenated at encode time.

    # keep the cutaway hold alive: a 3 m drift along the A-B axis over the hold
    sec_cam = bpy.data.objects.get('COAST_SECTION')
    sec_tgt = bpy.data.objects.get('TARGET_SECTION')
    if sec_cam and sec_tgt:
        axis = (site['section_axis'][1][0] - site['section_axis'][0][0],
                site['section_axis'][1][1] - site['section_axis'][0][1])
        length = (axis[0] ** 2 + axis[1] ** 2) ** 0.5 or 1.0
        ux, uy = axis[0] / length, axis[1] / length
        start = sec_cam.location.copy()
        for frame, offset in ((CUT_FRAME, 0.0), (END_FRAME, 3.0)):
            sec_cam.location = start + Vector((ux * offset, uy * offset, 0.0))
            sec_cam.keyframe_insert('location', frame=frame)
        tstart = sec_tgt.location.copy()
        for frame, offset in ((CUT_FRAME, 0.0), (END_FRAME, 3.0)):
            sec_tgt.location = tstart + Vector((ux * offset, uy * offset, 0.0))
            sec_tgt.keyframe_insert('location', frame=frame)

    scene.frame_start = 1
    scene.frame_end = END_FRAME
    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.engine = 'BLENDER_EEVEE'
    try:
        scene.eevee.taa_render_samples = 16
    except Exception:
        pass
    scene.render.image_settings.file_format = 'PNG'
    out_dir = os.path.join(FRAMES, site_key)
    os.makedirs(out_dir, exist_ok=True)
    scene.render.filepath = os.path.join(out_dir, 'frame_')

    target = os.path.join(CHECKPOINTS, '04-travel-%s.blend' % site_key)
    if save:
        bpy.ops.wm.save_as_mainfile(filepath=target)

    return {
        'checkpoint': target,
        'site': site_key,
        'frames': END_FRAME,
        'cut_frame': CUT_FRAME,
        'fps': 24,
        'resolution': [1920, 1080],
        'camera_path': {
            'overview': [round(v, 1) for v in ov_pos],
            'approach': [round(v, 1) for v in ap_pos],
            'lateral': [round(v, 1) for v in lateral_pos],
            'push': [round(v, 1) for v in push_pos],
        },
        'markers': [m.name for m in scene.timeline_markers],
        'frames_dir': out_dir,
    }
