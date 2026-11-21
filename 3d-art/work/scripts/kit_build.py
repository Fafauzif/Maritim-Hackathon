"""Phase 02 · original modular kit and material gallery.

Builds `work/checkpoints/02-kit.blend`: the shared asset library photographed as
an asset sheet for `output/kit/asset-sheet.png`, plus a material strip used as the
three-palette lookdev proof.

Run inside Blender:
    import kit_build; kit_build.build()
"""
import math
import os

import bmesh
import bpy

import site_lib as L
import props_build as P
import scene_build as SC
import look_rig

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
CHECKPOINTS = os.path.join(ART, "work", "checkpoints")
RENDERS = os.path.join(ART, "work", "renders", "kit")

KIT_PALETTE = {
    "wall_a": (0.86, 0.80, 0.69), "wall_b": (0.74, 0.66, 0.55),
    "wall_c": (0.91, 0.87, 0.78), "roof_a": (0.52, 0.22, 0.14),
    "roof_b": (0.30, 0.40, 0.37), "trim": (0.93, 0.91, 0.86),
    "glass": (0.10, 0.13, 0.16), "timber": (0.33, 0.22, 0.14),
    "deck": (0.44, 0.33, 0.22), "hull": (0.90, 0.89, 0.86),
    "hull_stripe": (0.28, 0.38, 0.52), "sand": (0.80, 0.73, 0.56),
    "bed_shallow": (0.55, 0.66, 0.58), "bed_deep": (0.20, 0.31, 0.33),
    "ground": (0.52, 0.55, 0.33), "veg": (0.30, 0.42, 0.24),
    "leaf": (0.28, 0.45, 0.26), "trunk": (0.36, 0.28, 0.19),
    "water": (0.30, 0.62, 0.62), "water_alpha": 0.80,
    "sky_top": (0.46, 0.64, 0.80), "sky_horizon": (0.87, 0.90, 0.87),
}

# a catalogue needs even, bright light: the coast rig is a daylight look, not a
# bench setup, so the kit overrides exposure / fill / world on top of it
KIT_RIG = {'exposure': -0.05, 'world': 0.55, 'sun': 4.0, 'fill': 420.0}


def reset():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in list(bpy.data.collections):
        bpy.data.collections.remove(coll)
    scene = bpy.context.scene
    scene.name = 'KitScene'
    return scene


def new_collection(scene, name):
    coll = bpy.data.collections.new(name)
    scene.collection.children.link(coll)
    return coll


def label(text, location, collection, size=0.8):
    curve = bpy.data.curves.new('LBL_' + text.replace(' ', '_'), 'FONT')
    curve.body = text
    curve.size = size
    curve.align_x = 'CENTER'
    ob = bpy.data.objects.new('LBL_' + text.replace(' ', '_'), curve)
    ob.location = location
    ob.rotation_euler = (math.radians(90), 0, 0)
    collection.objects.link(ob)
    mat = L.make_material('MAT_Label_Ink', (0.10, 0.10, 0.11), rough=0.9)
    ob.data.materials.append(mat)
    return ob


def swatch_sphere(name, material, location, collection, radius=0.5):
    me = bpy.data.meshes.new('SW_' + name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=radius)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(material)
    ob = bpy.data.objects.new('SW_' + name, me)
    ob.location = location
    collection.objects.link(ob)
    return ob


def build(save=True, render_draft=True):
    scene = reset()
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080

    stage = new_collection(scene, 'KIT_Stage')
    structures = new_collection(scene, 'KIT_Structures')
    survey = new_collection(scene, 'KIT_Survey')
    plants = new_collection(scene, 'KIT_Vegetation')
    finishes = new_collection(scene, 'KIT_Finishes')
    rig = new_collection(scene, 'KIT_Rig')

    mats = P.site_materials(KIT_PALETTE)

    # ---------------------------------------------------------------- stage
    ground_mat = L.make_material('MAT_Kit_Ground', (0.70, 0.70, 0.66), rough=0.95)
    backdrop_mat = L.make_material('MAT_Kit_Backdrop', (0.86, 0.86, 0.83), rough=0.95)
    L.mesh_from('KIT_Ground', [(-70, -50, 0), (70, -50, 0), (70, 40, 0), (-70, 40, 0)],
                [(0, 1, 2, 3)], [ground_mat], stage)
    L.mesh_from('KIT_Backdrop', [(-70, 24, 0), (70, 24, 0), (70, 24, 34), (-70, 24, 34)],
                [(0, 1, 2, 3)], [backdrop_mat], stage)

    # ----------------------------------------------------------- structures
    variants = [
        ('H_A  6x5 gable stilt', 6.0, 5.0, 2.8, 1.5, 'gable', 'x', 0.75, -17.0),
        ('H_B  10x5 hip', 10.0, 5.0, 3.0, 1.6, 'hip', 'x', 0.0, -8.0),
        ('H_C  5x5 flat stilt', 5.0, 5.0, 2.7, 1.2, 'flat', 'x', 0.75, 0.5),
        ('H_D  15x10 gable', 15.0, 10.0, 3.4, 2.0, 'gable', 'y', 0.0, 10.0),
    ]
    for name, w, d, wall, rh, roof, ridge, stilt, x in variants:
        me = P.house_mesh(name.split()[0], mats, w, d, wall, roof_h=rh, roof=roof,
                          stilt=stilt, ridge_axis=ridge, chimney=('H_B' in name or 'H_D' in name))
        ob = bpy.data.objects.new('KIT_House_' + me.name, me)
        ob.location = (x, 8.0, 0.0)
        structures.objects.link(ob)
        L.add_outline(ob, 0.03)
        label(name, (x, 3.4, 0.05), structures, size=0.9)

    # jetty module
    jetty = P.build_jetty({'jetty': {'base': (0.0, 0.0), 'direction': (1.0, 0.0),
                                     'length': 12.0}}, mats, survey, None, None, None)
    jetty.location = (-20.0, -2.0, 0.0)
    label('JETTY MODULE 12 m', (-14.0, -4.6, 0.05), survey, size=0.9)

    boat = P.boat_mesh('KIT_SurveyBoat', mats, survey)
    boat.location = (-2.0, -1.5, 0.0)
    boat.rotation_euler = (0, 0, math.radians(-14))
    L.add_outline(boat, 0.035)
    label('SURVEY BOAT 9.5 m', (-2.0, -4.6, 0.05), survey, size=0.9)

    local = P.boat_mesh('KIT_LocalBoat', mats, survey, length=6.4, width=1.9, cabin=False)
    local.location = (8.0, -1.0, 0.0)
    local.rotation_euler = (0, 0, math.radians(10))
    label('LOCAL CRAFT 6.4 m', (8.0, -4.6, 0.05), survey, size=0.9)

    # ----------------------------------------------------------- vegetation
    palm = P.palm_mesh(mats, plants)
    bush = P.bush_mesh(mats, plants)
    reed = P.reed_mesh(mats, plants)
    for me, name, x, scale in ((palm, 'PALM', -17.0, (1.0, 1.0, 1.0)),
                               (bush, 'SHRUB', -11.0, (1.5, 1.5, 1.1)),
                               (reed, 'REED CLUMP', -5.5, (1.4, 1.4, 1.4))):
        ob = bpy.data.objects.new('KIT_' + name, me)
        ob.location = (x, -8.5, 0.0)
        ob.scale = scale
        plants.objects.link(ob)
        label(name, (x, -10.4, 0.05), plants, size=0.9)

    # ------------------------------------------------- finishes / swatches
    groups = [
        ('PLASTER + TILE', [KIT_PALETTE['wall_a'], KIT_PALETTE['wall_b'],
                            KIT_PALETTE['roof_a'], KIT_PALETTE['trim']], -19.0),
        ('TIMBER + HULL', [KIT_PALETTE['timber'], KIT_PALETTE['deck'],
                           KIT_PALETTE['hull'], KIT_PALETTE['hull_stripe']], -8.5),
        ('LAND + WATER', [KIT_PALETTE['sand'], KIT_PALETTE['leaf'],
                          KIT_PALETTE['ground'], KIT_PALETTE['water']], 2.0),
        ('AMUR ACCENTS', [(0.63, 0.58, 0.50), (0.34, 0.26, 0.22),
                          (0.36, 0.29, 0.21), (0.24, 0.40, 0.45)], 12.5),
    ]
    for gi, (title, entries, x0) in enumerate(groups):
        for i, rgb in enumerate(entries):
            mat = L.make_material('MAT_KIT_%d_%d' % (gi, i), rgb, rough=0.9)
            swatch_sphere('%d_%d' % (gi, i), mat, (x0 + i * 1.25, -15.5, 0.5), finishes)
        label(title, (x0 + 1.9, -17.6, 0.05), finishes, size=0.85)

    # ------------------------------------------------------------ lighting
    SC.build_lighting(KIT_PALETTE, rig)
    SC.build_world(KIT_PALETTE, scene)
    look_rig.apply(scene, dict(look_rig.RIG, **KIT_RIG))
    # even bench fill from above
    fill_data = bpy.data.lights.new('KIT_Top_Softbox', 'AREA')
    fill_data.energy = 900.0
    fill_data.size = 26.0
    fill_data.color = (1.0, 0.98, 0.95)
    top = bpy.data.objects.new('KIT_Top_Softbox', fill_data)
    top.location = (0.0, 2.0, 24.0)
    top.rotation_euler = (0.0, 0.0, 0.0)
    rig.objects.link(top)

    # ------------------------------------------------------------- cameras
    cam = SC.make_camera('KIT_SHEET_CAM', 50.0, rig)
    cam.location = (2.0, -38.0, 14.0)
    target = SC.make_empty('KIT_SHEET_TARGET', (0.0, 4.0, 2.6), rig, 3.0)
    SC.track_to(cam, target)
    scene.camera = cam

    material_cams = []
    for gi, (title, entries, x0) in enumerate(groups):
        c = SC.make_camera('KIT_MAT_CAM_%d' % gi, 45.0, rig)
        c.location = (x0 + 1.9, -21.0, 3.0)
        t = SC.make_empty('KIT_MAT_TARGET_%d' % gi, (x0 + 1.9, -15.5, 0.55), rig, 1.0)
        SC.track_to(c, t)
        material_cams.append(('KIT_MAT_CAM_%d' % gi, title))

    os.makedirs(CHECKPOINTS, exist_ok=True)
    checkpoint = os.path.join(CHECKPOINTS, '02-kit.blend')
    if save:
        bpy.ops.wm.save_as_mainfile(filepath=checkpoint)

    made = {}
    if render_draft:
        os.makedirs(RENDERS, exist_ok=True)
        made['sheet'] = SC.render_still(scene, 'KIT_SHEET_CAM',
                                        os.path.join(RENDERS, 'asset-sheet.png'),
                                        res=(1920, 1080), engine='BLENDER_EEVEE', samples=48)
        for cam_name, title in material_cams:
            slug = title.lower().replace(' + ', '-').replace(' ', '-')
            made['mat_' + slug] = SC.render_still(
                scene, cam_name, os.path.join(RENDERS, 'material-%s.png' % slug),
                res=(1280, 720), engine='BLENDER_EEVEE', samples=48)
    return {
        'checkpoint': checkpoint,
        'objects': len(scene.objects),
        'collections': sorted(c.name for c in bpy.data.collections),
        'materials': len(bpy.data.materials),
        'renders': {k: {'bytes': v.get('bytes'), 'path': v.get('path')} for k, v in made.items()},
    }
