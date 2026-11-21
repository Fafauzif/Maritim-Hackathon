"""V2 globe: corrected locators, orthographic hero view, packed Earth art.

    blender -b --factory-startup --python build_globe_v2.py -- --run-root <run>
"""
import json
import math
import os
import sys

import bpy
import bmesh
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base")
for p in (HERE, BASE):
    if p not in sys.path:
        sys.path.insert(0, p)
import v2scene as SC

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GLOBE_REF = os.path.join(REPO, "3d-art", "references", "globe")
if GLOBE_REF not in sys.path:
    sys.path.insert(0, GLOBE_REF)
import make_globe_seed as G  # noqa: E402

RADIUS = 10.0
TEXTURE = os.path.join(GLOBE_REF, "earth-base-color.jpg")
ANCHORS = {
    "kodingareng": ("Kodingareng Lompo", -5.14905, 119.26473),
    "tunda": ("Pulau Tunda", -5.81151, 106.27811),
    "amur": ("Razdolnaya mouth", 43.32556, 131.80778),
}
PROBES = [
    ("Sahara land", 23.0, 10.0, "land"),
    ("Central Pacific", 0.0, -140.0, "ocean"),
    ("Antarctica painted land", -80.0, 0.0, "land"),
    ("Indian Ocean", -10.0, 80.0, "ocean"),
    ("Siberia land", 60.0, 100.0, "land"),
    ("Australia interior", -25.0, 134.0, "land"),
    ("North America", 40.0, -100.0, "land"),
    ("Atlantic Ocean", 0.0, -30.0, "ocean"),
    ("Atlantic Ocean north", 40.0, -40.0, "ocean"),
]


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def marker_materials():
    accent = bpy.data.materials.get("MAT_Globe_Marker")
    if accent is None:
        accent = bpy.data.materials.new("MAT_Globe_Marker")
        accent.use_nodes = True
        bsdf = accent.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Base Color"].default_value = (0.96, 0.50, 0.12, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.35
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (0.96, 0.50, 0.12, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 1.2
    rim = bpy.data.materials.get("MAT_Globe_Marker_Ring")
    if rim is None:
        rim = bpy.data.materials.new("MAT_Globe_Marker_Ring")
        rim.use_nodes = True
        b = rim.node_tree.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = (0.965, 0.94, 0.86, 1.0)
        b.inputs["Roughness"].default_value = 0.7
        if "Emission Color" in b.inputs:
            b.inputs["Emission Color"].default_value = (0.98, 0.92, 0.80, 1.0)
            b.inputs["Emission Strength"].default_value = 0.5
    return accent, rim


def add_marker(name, lat, lon, coll, accent, rim):
    direction = G.surface_xyz(1.0, lon, lat)
    base = G.surface_xyz(RADIUS, lon, lat)
    # thin stem
    me = bpy.data.meshes.new("MK_Stem_" + name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.045,
                          radius2=0.03, depth=0.34)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(rim)
    stem = bpy.data.objects.new("MK_Stem_" + name, me)
    stem.location = base + direction * 0.17
    stem.rotation_mode = "QUATERNION"
    stem.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(direction)
    coll.objects.link(stem)
    # flat ring marker sitting just above the texture
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.21,
                          radius2=0.21, depth=0.018)
    me = bpy.data.meshes.new("MK_Ring_" + name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(rim)
    ring = bpy.data.objects.new("MK_Ring_" + name, me)
    ring.location = base + direction * 0.012
    ring.rotation_mode = "QUATERNION"
    ring.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(direction)
    coll.objects.link(ring)
    # accent disc
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.12,
                          radius2=0.12, depth=0.05)
    me = bpy.data.meshes.new("MK_Disc_" + name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(accent)
    disc = bpy.data.objects.new("MK_Disc_" + name, me)
    disc.location = base + direction * 0.035
    disc.rotation_mode = "QUATERNION"
    disc.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(direction)
    coll.objects.link(disc)
    anchor = bpy.data.objects.new("ANCHOR_" + name, None)
    anchor.empty_display_type = "PLAIN_AXES"
    anchor.empty_display_size = 0.4
    anchor.location = base
    anchor["lat"] = lat
    anchor["lon"] = lon
    anchor["role"] = "globe locator from project place board"
    coll.objects.link(anchor)


def texture_probe(image):
    width, height = image.size
    buf = np.empty(width * height * 4, dtype=np.float32)
    image.pixels.foreach_get(buf)
    rgba = buf.reshape(height, width, 4)

    def sample(lat, lon):
        u = (lon + 180.0) / 360.0
        v = (lat + 90.0) / 180.0
        x = int(min(width - 1, max(0, round(u * width))))
        y = int(min(height - 1, max(0, round(v * height))))
        return rgba[y, x, :3]

    rows = []
    for label, lat, lon, expect in PROBES:
        rgb = sample(lat, lon)
        r, g, b = (float(c) for c in rgb)
        is_water = b > r and b > 0.22
        is_ice = r > 0.7 and g > 0.7 and b > 0.7
        ok = {"land": not is_water and not is_ice, "ocean": is_water,
              "ice": is_ice}[expect]
        rows.append({"label": label, "lat": lat, "lon": lon, "expected": expect,
                     "rgb": [round(r, 3), round(g, 3), round(b, 3)], "ok": bool(ok)})
    return rows


def build(run_root):
    # clean scene
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in list(bpy.data.collections):
        bpy.data.collections.remove(coll)
    scene = bpy.context.scene
    scene.name = "Earth_Globe"
    globe_coll = bpy.data.collections.new("GLOBE_Surface")
    scene.collection.children.link(globe_coll)
    marker_coll = bpy.data.collections.new("GLOBE_Markers")
    scene.collection.children.link(marker_coll)
    cam_coll = bpy.data.collections.new("GLOBE_Cameras")
    scene.collection.children.link(cam_coll)
    light_coll = bpy.data.collections.new("GLOBE_Lights")
    scene.collection.children.link(light_coll)

    globe = bpy.data.objects.new("Earth_Surface", G.make_mesh(RADIUS))
    globe_coll.objects.link(globe)
    globe.data.materials.append(G.make_material(TEXTURE))
    globe["radius"] = RADIUS
    globe["anchor_convention"] = "+X lon 0, +Y lon 90E, +Z north"
    globe["art_note"] = "Natural Earth 1:10m land, repainted colour art; not a data layer"
    globe["georeferenced"] = False

    accent, rim = marker_materials()
    for key, (label, lat, lon) in ANCHORS.items():
        add_marker(key, lat, lon, marker_coll, accent, rim)

    # dark illustrated space, with a soft cool key and rim
    world = bpy.data.worlds.get("Earth_World") or bpy.data.worlds.new("Earth_World")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.012, 0.020, 0.030, 1.0)
    bg.inputs["Strength"].default_value = 1.0
    scene.world = world

    key = bpy.data.lights.new("GLOBE_Key_Sun", "SUN")
    key.energy = 5.0
    key.angle = math.radians(8.0)
    key.color = (1.0, 0.95, 0.87)
    key_ob = bpy.data.objects.new("GLOBE_Key_Sun", key)
    key_ob.location = G.surface_xyz(2.0, 96.0, 26.0)
    aim(key_ob, (0, 0, 0))
    light_coll.objects.link(key_ob)

    rim = bpy.data.lights.new("GLOBE_Rim_Sun", "SUN")
    rim.energy = 1.8
    rim.angle = math.radians(35.0)
    rim.color = (0.55, 0.76, 1.0)
    rim_ob = bpy.data.objects.new("GLOBE_Rim_Sun", rim)
    rim_ob.location = G.surface_xyz(2.0, 285.0, -8.0)
    aim(rim_ob, (0, 0, 0))
    light_coll.objects.link(rim_ob)

    # orthographic hero camera showing the full globe with all three locators
    hero = bpy.data.objects.new("GLOBE_HOME", bpy.data.cameras.new("GLOBE_HOME"))
    hero.data.type = "ORTHO"
    hero.data.ortho_scale = 21.4
    hero.data.clip_start = 0.5
    hero.data.clip_end = 200.0
    hero.location = G.surface_xyz(3.0 * RADIUS, 118.0, 18.0)
    aim(hero, (0, 0, 0))
    cam_coll.objects.link(hero)
    scene.camera = hero

    region_cams = {}
    for site, (label, lat, lon) in ANCHORS.items():
        cam = bpy.data.objects.new("GLOBE_REGION_" + site,
                                   bpy.data.cameras.new("GLOBE_REGION_" + site))
        cam.data.lens = 62.0
        cam.data.clip_start = 0.5
        cam.data.clip_end = 200.0
        cam.location = G.surface_xyz(2.25 * RADIUS, lon + 3.0,
                                     max(-62.0, min(62.0, lat + 14.0)))
        marker = bpy.data.objects.get("ANCHOR_" + site)
        aim(cam, marker.location if marker else (0, 0, 0))
        cam_coll.objects.link(cam)
        region_cams[site] = cam

    # reel orbit animation: 24 deg over 144 frames (6 s)
    orbit = bpy.data.objects.new("GLOBE_ORBIT", None)
    orbit.empty_display_type = "CIRCLE"
    orbit.empty_display_size = 1.3 * RADIUS
    cam_coll.objects.link(orbit)
    reel = bpy.data.objects.new("GLOBE_REEL", bpy.data.cameras.new("GLOBE_REEL"))
    reel.data.type = "ORTHO"
    reel.data.ortho_scale = 21.6
    reel.data.clip_start = 0.5
    reel.data.clip_end = 200.0
    reel.parent = orbit
    reel.location = G.surface_xyz(3.0 * RADIUS, 0.0, 18.0)
    cam_coll.objects.link(reel)
    con = reel.constraints.new("TRACK_TO")
    con.target = orbit
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    orbit.rotation_euler = (0.0, 0.0, math.radians(110.0))
    orbit.keyframe_insert("rotation_euler", frame=1)
    orbit.rotation_euler = (0.0, 0.0, math.radians(134.0))
    orbit.keyframe_insert("rotation_euler", frame=144)

    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 64
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.fps = 24
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "Khronos PBR Neutral"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.05
    scene.view_settings.gamma = 1.0
    try:
        scene.eevee.use_raytracing = True
    except Exception:
        pass

    image = bpy.data.images.get("earth-base-color.jpg") or bpy.data.images.load(TEXTURE)
    probes = texture_probe(image)

    os.makedirs(os.path.join(run_root, "checkpoints"), exist_ok=True)
    path = os.path.join(run_root, "checkpoints", "globe.blend")
    bpy.ops.wm.save_as_mainfile(filepath=path)
    made = {}
    proof = os.path.join(run_root, "proofs", "look", "globe_overview.png")
    made["overview"] = SC.render_still(scene, "GLOBE_HOME", proof, res=(3840, 2160),
                                       samples=64, hide=())
    for site, cam in region_cams.items():
        made[site] = SC.render_still(
            scene, cam.name,
            os.path.join(run_root, "proofs", "look", "globe_region_%s.png" % site),
            res=(1920, 1080), samples=32, hide=())
    bpy.ops.wm.save_as_mainfile(filepath=path)
    stats = {
        "checkpoint": path,
        "radius": RADIUS,
        "anchors": {k: {"lat": v[1], "lon": v[2], "label": v[0]}
                    for k, v in ANCHORS.items()},
        "anchor_nodes": {k: [round(c, 4) for c in G.surface_xyz(RADIUS, v[2], v[1])]
                         for k, v in ANCHORS.items()},
        "orientation_probes": probes,
        "orientation_ok": all(p["ok"] for p in probes),
        "cameras": [o.name for o in scene.objects if o.type == "CAMERA"],
        "render": {k: {"path": v["path"], "bytes": v["bytes"]} for k, v in made.items()},
    }
    with open(os.path.join(run_root, "logs", "build-globe.json"), "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2)
    print("GLOBE " + json.dumps({"checkpoint": path,
                                 "orientation_ok": stats["orientation_ok"],
                                 "render_bytes": made["overview"]["bytes"]}))


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    run_root = None
    i = 0
    while i < len(argv):
        if argv[i] == "--run-root":
            run_root = argv[i + 1]; i += 2
        else:
            i += 1
    if not run_root:
        raise SystemExit("need --run-root")
    build(run_root)
