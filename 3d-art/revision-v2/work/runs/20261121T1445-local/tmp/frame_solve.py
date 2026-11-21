"""Evaluate candidate overview cameras by projecting the island boundary + boat."""
import math
import sys
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

blend, out = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.open_mainfile(filepath=blend)
scene = bpy.context.scene
site = bpy.data.objects["COAST_ORIGIN"].get("site_key")
boat = bpy.data.objects["PROP_SurveyBoat"].matrix_world.translation.copy()
jetty = bpy.data.objects["PROP_Jetty"].matrix_world.translation.copy()
print("SITE", site, "BOAT", tuple(round(v, 1) for v in boat))

# island boundary (radius depends on site; use a circle that covers the land)
R = {"kodingareng": 104, "tunda": 145, "amur": 0}.get(site, 104)
scene.render.resolution_x, scene.render.resolution_y = 3840, 2160

camp = scene.objects.new if False else None
cd = bpy.data.cameras.new("CAND")
cam = bpy.data.objects.new("CAND", cd)
scene.collection.objects.link(cam)
scene.camera = cam


def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def eval_cam(pos, target, lens):
    cam.location = pos
    cd.lens = lens
    look_at(cam, target)
    bpy.context.view_layer.update()
    pts = []
    if R:
        for i in range(48):
            a = 2 * math.pi * i / 48
            pts.append(Vector((math.cos(a) * R, math.sin(a) * R, 0)))
    pts += [boat, boat + Vector((0, 0, 4.0)), jetty]
    uv = [world_to_camera_view(scene, cam, p) for p in pts]
    xs = [u.x for u in uv]
    ys = [u.y for u in uv]
    inside = sum(1 for u in uv if 0 <= u.x <= 1 and 0 <= u.y <= 1 and u.z > 0)
    return {"pos": [round(v, 1) for v in pos], "target": [round(v, 1) for v in target],
            "lens": lens, "bbox": [round(min(xs), 3), round(min(ys), 3),
                                   round(max(xs), 3), round(max(ys), 3)],
            "inside": inside, "n": len(uv),
            "island_area_frac": round((max(xs) - min(xs)) * (max(ys) - min(ys)), 3)}


CANDIDATES = {
    "kodingareng": [
        ((28, -340, 258), (0, -78, 0), 38),
        ((10, -310, 235), (0, -50, 0), 36),
        ((5, -305, 235), (0, -55, 0), 34),
        ((20, -300, 225), (0, -55, 0), 34),
        ((0, -290, 215), (0, -58, 0), 33),
        ((0, -280, 210), (0, -60, 0), 32),
        ((10, -300, 220), (0, -62, 0), 35),
        ((0, -285, 205), (0, -55, 0), 32),
    ],
    "tunda": [
        ((-56, -320, 240), (-50, -20, 0), 40),
        ((-30, -320, 245), (-30, -30, 0), 36),
        ((-20, -320, 250), (-20, -30, 0), 34),
        ((-10, -310, 240), (-20, -40, 0), 33),
    ],
    "amur": [
        ((8, -168, 202), (38, 50, 0), 56),
        ((20, -150, 190), (45, 45, 0), 48),
        ((30, -140, 180), (50, 40, 0), 45),
        ((0, -150, 180), (40, 40, 0), 44),
    ],
}
res = [eval_cam(*c) for c in CANDIDATES.get(site, CANDIDATES["kodingareng"])]
for r in res:
    print("CAND", r)
with open(out, "w", encoding="utf-8") as fh:
    import json
    json.dump(res, fh, indent=2)
