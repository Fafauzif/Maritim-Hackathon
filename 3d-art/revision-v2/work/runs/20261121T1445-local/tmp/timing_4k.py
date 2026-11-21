import os, time, json
import bpy
REPO = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon"
RUN = os.path.join(REPO, "3d-art", "revision-v2", "work", "runs", "20261121T1445-local")
SRC = os.path.join(REPO, "3d-art", "output", "coasts", "kodingareng", "scene.blend")
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene
sc.camera = bpy.data.objects["COAST_OVERVIEW"]
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x, sc.render.resolution_y = 3840, 2160
sc.render.resolution_percentage = 100
sc.eevee.taa_render_samples = 32
sc.render.image_settings.file_format = 'PNG'
p = os.path.join(RUN, "tmp", "timing-4k.png")
sc.render.filepath = p
t = time.time()
bpy.ops.render.render(write_still=True)
print("TIMING4K", json.dumps({"seconds": round(time.time()-t,2), "bytes": os.path.getsize(p)}))
