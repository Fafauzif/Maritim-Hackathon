import json
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view

run = sys.argv[sys.argv.index("--") + 1]
out = sys.argv[sys.argv.index("--") + 2]
bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints", "globe.blend"))
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = 3840, 2160
sc.camera = bpy.data.objects["GLOBE_HOME"]
bpy.context.view_layer.update()
res = {}
for site in ("kodingareng", "tunda", "amur"):
    ob = bpy.data.objects["ANCHOR_" + site]
    uv = world_to_camera_view(sc, sc.camera, ob.matrix_world.translation)
    res[site] = {"uv": [round(uv.x, 5), round(uv.y, 5)], "z": round(uv.z, 4)}
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=2)
print("GLOBE_MARKERS " + json.dumps(res))
