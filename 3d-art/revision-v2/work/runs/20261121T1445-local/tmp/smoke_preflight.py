"""Phase-0 smoke: open v1 coast, time a small EEVEE render, export+reimport GLB."""
import json
import os
import time

import bpy

REPO = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon"
RUN = os.path.join(REPO, "3d-art", "revision-v2", "work", "runs", "20261121T1445-local")
SRC = os.path.join(REPO, "3d-art", "output", "coasts", "kodingareng", "scene.blend")
OUT_PNG = os.path.join(RUN, "tmp", "smoke-render.png")
OUT_GLB = os.path.join(RUN, "tmp", "smoke-export.glb")
report = {"blender": bpy.app.version_string, "source": SRC}

t0 = time.time()
bpy.ops.wm.open_mainfile(filepath=SRC)
report["open_seconds"] = round(time.time() - t0, 2)
scene = bpy.context.scene
report["scene"] = scene.name
report["objects"] = len(scene.objects)
report["collections"] = [c.name for c in bpy.data.collections]
report["cameras"] = [o.name for o in scene.objects if o.type == 'CAMERA']
report["engine"] = scene.render.engine
report["dirty"] = bpy.data.is_dirty

# small render timing
scene.camera = bpy.data.objects.get("COAST_OVERVIEW")
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 480
scene.render.resolution_y = 270
scene.render.resolution_percentage = 100
try:
    scene.eevee.taa_render_samples = 8
except Exception:
    pass
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = OUT_PNG
t0 = time.time()
bpy.ops.render.render(write_still=True)
report["render_seconds"] = round(time.time() - t0, 2)
report["render_bytes"] = os.path.getsize(OUT_PNG) if os.path.exists(OUT_PNG) else 0

# select exportable objs
for ob in scene.objects:
    ob.select_set(False)
used = []
for coll_name in ('ENV_Land', 'ENV_Water', 'BLD_Village', 'PROP_Survey',
                  'VEG_Scatter', 'CAM_Rigs'):
    coll = bpy.data.collections.get(coll_name)
    if coll:
        for ob in coll.all_objects:
            if ob.type in ('MESH', 'EMPTY'):
                ob.select_set(True)
                used.append(ob)
for ob in bpy.data.objects:
    if ob.type == 'MESH':
        for mod in list(ob.modifiers):
            if 'Outline' in mod.name:
                ob.modifiers.remove(mod)
t0 = time.time()
bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format='GLB', use_selection=True,
                          export_cameras=False, export_lights=False, export_apply=True,
                          export_yup=True, export_extras=True)
report["export_seconds"] = round(time.time() - t0, 2)
report["glb_bytes"] = os.path.getsize(OUT_GLB)

# fresh import
bpy.ops.wm.read_factory_settings(use_empty=True)
t0 = time.time()
bpy.ops.import_scene.gltf(filepath=OUT_GLB)
report["import_seconds"] = round(time.time() - t0, 2)
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
report["import_meshes"] = len(meshes)
report["import_materials"] = len(bpy.data.materials)
report["import_cameras"] = len([o for o in bpy.context.scene.objects if o.type == 'CAMERA'])
report["import_lights"] = len([o for o in bpy.context.scene.objects if o.type == 'LIGHT'])
report["import_has_water"] = any(o.name.startswith('ENV_Water') for o in bpy.context.scene.objects)
diff = bpy.context.scene.view_settings.view_transform
report["import_view_transform"] = diff
open(os.path.join(RUN, "logs", "smoke-preflight.json"), "w", encoding="utf-8").write(
    json.dumps(report, indent=2))
print("SMOKE " + json.dumps(report))
