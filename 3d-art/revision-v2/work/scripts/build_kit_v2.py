"""V2 common kit scene: authored components + labelled asset sheet.

    blender -b --factory-startup --python build_kit_v2.py -- --run-root <run>
"""
import json
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base")
for p in (HERE, BASE):
    if p not in sys.path:
        sys.path.insert(0, p)

import site_lib as L
import v2props as V
import v2scene as SC

KIT_PALETTE = dict(
    wall_a=(0.84, 0.75, 0.61), wall_b=(0.72, 0.60, 0.47), wall_c=(0.90, 0.84, 0.73),
    roof_a=(0.55, 0.24, 0.16), roof_b=(0.26, 0.40, 0.37), roof_c=(0.44, 0.34, 0.25),
    trim=(0.90, 0.86, 0.78), glass=(0.10, 0.12, 0.14), timber=(0.31, 0.21, 0.13),
    deck=(0.42, 0.30, 0.19), hull=(0.88, 0.85, 0.78),
    hull_stripe=(0.22, 0.36, 0.47), sand=(0.76, 0.68, 0.51),
    bed_shallow=(0.47, 0.56, 0.46), bed_deep=(0.16, 0.27, 0.30),
    ground=(0.49, 0.50, 0.32), veg=(0.27, 0.39, 0.23),
    leaf=(0.24, 0.40, 0.22), trunk=(0.34, 0.26, 0.17),
    water=(0.20, 0.48, 0.52), water_alpha=0.84,
    sky_top=(0.36, 0.54, 0.68), sky_horizon=(0.86, 0.83, 0.72),
    foam=(0.93, 0.92, 0.84),
)


def reset():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in list(bpy.data.collections):
        bpy.data.collections.remove(coll)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)
    sc = bpy.context.scene
    sc.name = "KitScene"
    return sc


def new_coll(scene, name):
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    return c


def label(text, location, collection, mats, size=0.95):
    curve = bpy.data.curves.new("LBL_" + text.replace(" ", "_"), "FONT")
    curve.body = text
    curve.size = size
    curve.align_x = "CENTER"
    ob = bpy.data.objects.new("LBL_" + text.replace(" ", "_"), curve)
    ob.location = location
    ob.rotation_euler = (math.radians(90), 0, 0)
    collection.objects.link(ob)
    ob.data.materials.append(mats["ink"])
    return ob


def kit_jetty(mats, collection):
    b = V.B()
    length, width = 12.0, 3.0
    for i in range(6):
        x = -length / 2 + (i + 0.5) * 2.0
        b.box((x, 0, 0.6), (1.95, width, 0.12), "deck_a" if i % 2 == 0 else "deck_b")
        b.box((x, 0, 0.46), (0.15, width + 0.1, 0.12), "timber")
    for side in (-1, 1):
        b.box((0, side * (width / 2 - 0.18), 0.36), (length, 0.22, 0.22), "timber")
        b.box((0, side * (width / 2 - 0.10), 1.58), (length - 1.0, 0.08, 0.08), "trim")
        b.box((0, side * (width / 2 - 0.10), 1.14), (length - 1.0, 0.06, 0.06), "trim")
        for i in range(5):
            x = -length / 2 + 1.0 + i * 2.5
            b.box((x, side * (width / 2 - 0.10), 1.05), (0.08, 0.08, 1.05), "trim")
            b.box((x, side * (width / 2 - 0.25), -0.65), (0.26, 0.26, 3.0), "timber")
    return b.finish("KIT_JETTY", mats, collection)


def build(run_root):
    scene = reset()
    mats = V.make_materials(KIT_PALETTE)
    cols = {n: new_coll(scene, n) for n in
            ("KIT_Structures", "KIT_Survey", "KIT_Vegetation", "KIT_Props",
             "KIT_Stage", "KIT_Rig", "KIT_Labels")}
    # stage
    L.mesh_from("KIT_Ground", [(-60, -40, 0), (60, -40, 0), (60, 40, 0), (-60, 40, 0)],
                [(0, 1, 2, 3)],
                [L.make_material("MAT_Kit_Ground", (0.73, 0.72, 0.67), rough=0.97)],
                cols["KIT_Stage"])
    L.mesh_from("KIT_Backdrop", [(-60, 30, 0), (60, 30, 0), (60, 30, 34), (-60, 30, 34)],
                [(0, 1, 2, 3)],
                [L.make_material("MAT_Kit_Backdrop", (0.88, 0.87, 0.83), rough=0.95)],
                cols["KIT_Stage"])

    # structures
    houses = [("A", -18.0, 12.0), ("B", -6.0, 12.0), ("C", 6.0, 12.0), ("D", 18.0, 12.0)]
    for key, x, y in houses:
        var = next(v for v in V.HOUSE_VARIANTS if v[0] == key)
        _, w, d, wall_h, roof_h, roof, wm, rm, stilt, porch, storeys = var
        b = V.house_mesh("KIT_HOUSE_" + key, mats, w, d, wall_h, roof_h, roof, wm, rm,
                         stilt=stilt, porch=porch, storeys=storeys)
        ob = b.finish("KIT_HOUSE_" + key, mats, cols["KIT_Structures"])
        ob.location = (x, y, 0)
        label("HOUSE " + key, (x, y - d / 2 - 2.2, 0.02), cols["KIT_Labels"], mats)
    pav = V.pavilion_mesh(mats, cols["KIT_Structures"], "KIT_PAVILION")
    pav.location = (-16.0, 2.0, 0.0)
    label("LANDING PAVILION", (-16.0, -2.6, 0.02), cols["KIT_Labels"], mats)
    land = V.working_landing_mesh(mats, cols["KIT_Structures"], "KIT_WORKING_LANDING")
    land.location = (0.0, 2.0, 0.0)
    label("WORKING LANDING", (0.0, -2.6, 0.02), cols["KIT_Labels"], mats)
    hall = V.community_hall_mesh(mats, cols["KIT_Structures"], "KIT_COMMUNITY_HALL")
    hall.location = (18.0, 2.0, 0.0)
    label("COMMUNITY HALL", (18.0, -2.6, 0.02), cols["KIT_Labels"], mats)

    # survey
    jet = kit_jetty(mats, cols["KIT_Survey"])
    jet.location = (-19.0, -8.0, 0.0)
    label("JETTY MODULE 12 m", (-19.0, -13.0, 0.02), cols["KIT_Labels"], mats)
    boat = V.boat_mesh_v2(mats, cols["KIT_Survey"], "KIT_BOAT_SURVEY", length=10.6,
                          width=3.0, cabin=True, draft=0.95)
    boat.location = (-1.0, -8.0, 0.0)
    boat.rotation_euler = (0, 0, math.radians(8))
    label("SURVEY BOAT 10.6 m", (-1.0, -13.0, 0.02), cols["KIT_Labels"], mats)
    local = V.outrigger_mesh_v2(mats, cols["KIT_Survey"], "KIT_BOAT_LOCAL")
    local.location = (17.0, -8.0, 0.0)
    local.rotation_euler = (0, 0, math.radians(-12))
    label("LOCAL OUTRIGGER 6.2 m", (17.0, -13.0, 0.02), cols["KIT_Labels"], mats)

    # vegetation
    for maker, name, x, disp in (
            (V.palm_mesh_v2, "KIT_PALM", -18.0, "PALM"),
            (V.shrub_mesh_v2, "KIT_SHRUB", -8.0, "SHRUB CLUSTER"),
            (V.reed_mesh_v2, "KIT_REED", 2.0, "REED CLUMP"),
            (V.mangrove_mesh_v2, "KIT_MANGROVE", 12.0, "MANGROVE")):
        ob = maker(mats, cols["KIT_Vegetation"], name)
        ob.location = (x, -18.0, 0.0)
        label(disp, (x, -21.5, 0.02), cols["KIT_Labels"], mats)

    # props
    b = V.B()
    b.box((0, 0, 0.42), (0.9, 0.9, 0.84), "crate")
    b.box((0, 0, 0.86), (0.95, 0.10, 0.05), "timber")
    b.box((0, 0, 0.62), (0.10, 0.95, 0.05), "timber")
    c1 = b.finish("KIT_CRATE", mats, cols["KIT_Props"])
    c1.location = (21.0, -18.0, 0.0)
    label("CARGO CRATE", (21.0, -21.5, 0.02), cols["KIT_Labels"], mats)
    b = V.B()
    for i in range(8):
        r = 0.34 - i * 0.015
        b.box((0, 0, 0.06 + i * 0.10), (r * 2, r * 2, 0.10), "metal")
    c2 = b.finish("KIT_BARREL", mats, cols["KIT_Props"])
    c2.location = (25.5, -18.0, 0.0)
    label("MOORING BARREL", (25.5, -21.5, 0.02), cols["KIT_Labels"], mats)

    # lighting
    SC.LOOK.update({"exposure": -0.18, "grade_sat": 1.0, "sun": 4.0,
                    "fill": 380.0, "world": 0.55})
    SC.build_lighting(KIT_PALETTE, cols["KIT_Rig"])
    SC.build_world(KIT_PALETTE, scene)
    fill_data = bpy.data.lights.new("KIT_Top_Softbox", "AREA")
    fill_data.energy = 1100.0
    fill_data.size = 30.0
    fill_data.color = (1.0, 0.97, 0.92)
    top = bpy.data.objects.new("KIT_Top_Softbox", fill_data)
    top.location = (0.0, -2.0, 28.0)
    top.rotation_euler = (0.0, 0.0, 0.0)
    cols["KIT_Rig"].objects.link(top)
    SC.build_compositor(scene)
    SC.apply_look(scene)

    # orthographic catalogue camera
    cam = SC.make_camera("KIT_SHEET_CAM", 50.0, cols["KIT_Rig"], ortho_scale=70.0)
    cam.location = (0.0, -70.0, 32.0)
    tgt = SC.make_empty("KIT_SHEET_TARGET", (0.0, -2.0, 3.4), cols["KIT_Rig"], 3.0)
    SC.track_to(cam, tgt)
    scene.camera = cam
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 2560
    scene.render.resolution_y = 1440
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = SC.LOOK["view_transform"]
    scene.view_settings.exposure = SC.LOOK["exposure"]

    os.makedirs(os.path.join(run_root, "checkpoints"), exist_ok=True)
    path = os.path.join(run_root, "checkpoints", "kit.blend")
    bpy.ops.wm.save_as_mainfile(filepath=path)
    proof = os.path.join(run_root, "proofs", "look", "kit_asset-sheet.png")
    made = SC.render_still(scene, "KIT_SHEET_CAM", proof, res=(2560, 1440),
                           samples=48, hide=())
    bpy.ops.wm.save_as_mainfile(filepath=path)
    stats = {"checkpoint": path, "objects": len(scene.objects),
             "meshes": len([o for o in scene.objects if o.type == "MESH"]),
             "components": sorted(o.name for o in scene.objects
                                  if o.name.startswith("KIT_") and o.type == "MESH"),
             "render": made}
    with open(os.path.join(run_root, "logs", "build-kit.json"), "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2)
    print("KIT " + json.dumps({"checkpoint": path, "components": len(stats["components"]),
                              "render_bytes": made["bytes"]}))


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

