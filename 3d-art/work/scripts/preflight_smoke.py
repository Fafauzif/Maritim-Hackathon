"""Phase 00 preflight: disposable smoke scene + render + path parity proof.

Run inside the live Blender session. Saves a checkpoint, renders a PNG, and
reports exactly where the ochre sphere lands on screen so the image can be
verified independently of "the render call returned".
"""
import bpy
import os
import math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
CKPT = os.path.join(ART, "work", "checkpoints", "00-preflight.blend")
PNG = os.path.join(ART, "work", "renders", "smoke.png")
os.makedirs(os.path.dirname(CKPT), exist_ok=True)
os.makedirs(os.path.dirname(PNG), exist_ok=True)

scene = bpy.context.scene

# Leave Edit Mode if the artist left an object mid-edit; never discard their file.
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

# Save a disposable working file BEFORE building, so nothing lives unsaved.
bpy.ops.wm.save_as_mainfile(filepath=CKPT)

# ---- rebuild a clean smoke scene (data-level, context independent) ----
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
for coll in list(bpy.data.collections):
    bpy.data.collections.remove(coll)

col = bpy.data.collections.new("COL_SMOKE")
scene.collection.children.link(col)

def material(name, rgba, rough=0.7, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Roughness"].default_value = rough
        bsdf.inputs["Metallic"].default_value = metallic
    return m

m_teal = material("MAT_TealFloor", (0.05, 0.42, 0.45, 1.0), rough=0.35)
m_ochre = material("MAT_OchreSphere", (0.77, 0.45, 0.05, 1.0), rough=0.45)
m_grey = material("MAT_SlopeBlock", (0.55, 0.56, 0.58, 1.0), rough=0.8)

# teal floor
floor_mesh = bpy.data.meshes.new("SM_Smoke_Floor")
floor_mesh.from_pydata(
    [(-5, -5, 0), (5, -5, 0), (5, 5, 0), (-5, 5, 0)], [], [(0, 1, 2, 3)]
)
floor_mesh.materials.append(m_teal)
floor = bpy.data.objects.new("SM_Smoke_Floor", floor_mesh)
col.objects.link(floor)

# sloped block (asymmetric reference)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.6, 0.4, 0.6))
block = bpy.context.active_object
block.name = "SM_Smoke_Slope"
block.scale = (2.2, 1.4, 1.2)
block.rotation_euler = (0.0, math.radians(22), math.radians(-14))
block.data.materials.append(m_grey)
for c in list(block.users_collection):
    c.objects.unlink(block)
col.objects.link(block)

# ochre sphere - the landmark whose screen position gets reported
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.62, segments=48, ring_count=24,
                                     location=(1.55, -1.05, 0.95))
sphere = bpy.context.active_object
sphere.name = "SM_Smoke_OchreSphere"
sphere.data.materials.append(m_ochre)
for c in list(sphere.users_collection):
    c.objects.unlink(sphere)
col.objects.link(sphere)

# camera + target
cam_data = bpy.data.cameras.new("CAM_Smoke")
cam_data.lens = 42
cam = bpy.data.objects.new("CAM_Smoke", cam_data)
col.objects.link(cam)
cam.location = (4.6, -6.2, 3.9)
scene.camera = cam

target = bpy.data.objects.new("TARGET_Smoke", None)
col.objects.link(target)
target.location = (0.0, 0.0, 0.75)
con = cam.constraints.new('TRACK_TO')
con.target = target
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'

# sun + sky
sun_data = bpy.data.lights.new("LGT_Smoke_Sun", 'SUN')
sun_data.energy = 3.5
sun_data.angle = math.radians(4)
sun = bpy.data.objects.new("LGT_Smoke_Sun", sun_data)
col.objects.link(sun)
sun.rotation_euler = (math.radians(52), math.radians(8), math.radians(35))

world = scene.world or bpy.data.worlds.new("WD_Smoke")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value = (0.55, 0.68, 0.82, 1.0)
    bg.inputs["Strength"].default_value = 1.1

# render settings: 960x540 Eevee
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
try:
    scene.view_settings.view_transform = 'AgX'
except Exception:
    pass

bpy.context.view_layer.update()

# where does the ochre sphere land on screen?
co = world_to_camera_view(scene, cam, sphere.matrix_world.translation)
px = (round(co.x * 960), round((1.0 - co.y) * 540))   # top-left origin, like an image
fraction_from_left = round(co.x, 3)
fraction_from_top = round(1.0 - co.y, 3)

scene.render.filepath = PNG
bpy.ops.render.render(write_still=True)
png_exists = os.path.exists(PNG)
png_size = os.path.getsize(PNG) if png_exists else 0

bpy.ops.wm.save_as_mainfile(filepath=CKPT)

gpu = {}
try:
    prefs = bpy.context.preferences.addons.get('cycles')
    if prefs:
        cp = prefs.preferences
        gpu["compute_device_type"] = cp.compute_device_type
        gpu["devices"] = [d.name for d in cp.devices if d.use]
except Exception as exc:
    gpu["probe_error"] = str(exc)

result = {
    "checkpoint": CKPT,
    "png_path": PNG,
    "png_exists": png_exists,
    "png_bytes": png_size,
    "png_pixels": (960, 540),
    "blender": bpy.app.version_string,
    "engine": scene.render.engine,
    "gpu": gpu,
    "sphere_screen_px_top_left_origin": px,
    "sphere_fraction_from_left": fraction_from_left,
    "sphere_fraction_from_top": fraction_from_top,
    "sphere_visible_in_frame": bool(0.0 < co.x < 1.0 and 0.0 < co.z < 1.0 and co.z > 0.0),
    "objects": sorted(o.name for o in scene.objects),
    "collections": [c.name for c in bpy.data.collections],
    "filepath": bpy.data.filepath,
}
