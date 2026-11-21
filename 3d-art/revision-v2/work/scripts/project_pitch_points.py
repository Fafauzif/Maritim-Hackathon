import json
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view

run = sys.argv[sys.argv.index("--") + 1]
out = sys.argv[sys.argv.index("--") + 2]
bpy.ops.wm.open_mainfile(filepath=os.path.join(run, "checkpoints", "coast-kodingareng.blend"))
scene = bpy.context.scene
scene.render.resolution_x, scene.render.resolution_y = 3840, 2160
result = {}
for cam_name in ("COAST_APPROACH", "COAST_SECTION"):
    cam = bpy.data.objects[cam_name]
    scene.camera = cam
    bpy.context.view_layer.update()
    points = {}
    for name in ("SECTION_A", "SECTION_B", "ANCHOR_VESSEL", "ANCHOR_JETTY",
                 "PROP_SurveyBoat", "PROP_Jetty", "BLD_LandingPavilion"):
        ob = bpy.data.objects.get(name)
        if not ob:
            continue
        uv = world_to_camera_view(scene, cam, ob.matrix_world.translation)
        points[name] = [round(uv.x, 5), round(uv.y, 5), round(uv.z, 4)]
    result[cam_name] = points
with open(out, "w", encoding="utf-8") as fh:
    json.dump(result, fh, indent=2)
print("PITCH_POINTS " + json.dumps(result))
