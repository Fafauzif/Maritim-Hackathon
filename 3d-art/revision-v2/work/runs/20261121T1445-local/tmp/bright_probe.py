import bpy, math, json
import numpy as np
from mathutils import Vector

bpy.ops.wm.open_mainfile(filepath=r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\checkpoints\coast-kodingareng.blend")
sc = bpy.context.scene
cam = bpy.data.objects["COAST_OVERVIEW"]
sc.camera = cam
bpy.context.view_layer.update()
mw = cam.matrix_world
aspect = 16 / 9
lens = cam.data.lens
sensor = 36.0
hf = 2 * math.atan(sensor / (2 * lens))
vf = 2 * math.atan((sensor / aspect) / (2 * lens))
dg = bpy.context.evaluated_depsgraph_get()
img = bpy.data.images.load(r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\revision-v2\work\runs\20261121T1445-local\proofs\look\kodingareng_godview.png")
w, h = img.size
px = np.empty(w * h * 4, dtype=np.float32)
img.pixels.foreach_get(px)
im = px.reshape(h, w, 4)[:, :, :3]
luma = 0.2126 * im[:, :, 0] + 0.7152 * im[:, :, 1] + 0.0722 * im[:, :, 2]
counts = {}
for j in range(40):
    for i in range(40):
        u = (i + 0.5) / 40
        v = 1 - (j + 0.5) / 40
        pxx, pyy = int(u * w), int((1 - v) * h)
        if luma[min(pyy, h - 1), min(pxx, w - 1)] <= 0.9:
            continue
        x = (2 * u - 1) * math.tan(hf / 2)
        y = (2 * v - 1) * math.tan(vf / 2)
        d = (mw.to_3x3() @ Vector((x, y, -1))).normalized()
        hit, loc, norm, idx, ob, m = sc.ray_cast(dg, mw.translation, d)
        key = (ob.name if hit else "MISS", (ob.active_material.name if (hit and ob and ob.active_material) else None))
        counts[key] = counts.get(key, 0) + 1
print("BRIGHT_HITS " + json.dumps({str(k): val for k, val in sorted(counts.items(), key=lambda kv: -kv[1])[:15]}, default=str))

