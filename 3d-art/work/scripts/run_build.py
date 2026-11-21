"""Entry point: build one coastal scene and save its checkpoint.

Called inside Blender:
    import run_build; result = run_build.build("kodingareng", phase="01")
"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else \
    r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art\work\scripts"
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import site_lib as L
import site_build as SB
import props_build as P
import scene_build as SC

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
CHECKPOINTS = os.path.join(ART, "work", "checkpoints")


def build(site_key, phase="01", save=True):
    site = SB.SITES[site_key]
    palette = site["palette"]

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    target = os.path.join(CHECKPOINTS, "%s-%s.blend" % (phase, site_key))
    os.makedirs(CHECKPOINTS, exist_ok=True)
    # park the currently-open scene in a scratch file: never overwrite another
    # site's checkpoint with whatever happened to be open in the session
    scratch = os.path.join(CHECKPOINTS, '_autosave-before-build.blend')
    bpy.ops.wm.save_as_mainfile(filepath=scratch)

    scene = SC.reset_scene()
    cols = SC.make_collections(scene)
    mats = P.site_materials(palette)

    terrain, (xs, ys, hgrid) = SB.build_terrain(site, palette, cols['ENV_Land'])
    water = SB.build_water(site, palette, cols['ENV_Water'])
    houses = P.place_settlement(site, mats, cols['BLD_Village'], xs, ys, hgrid)
    jetty = P.build_jetty(site, mats, cols['PROP_Survey'], xs, ys, hgrid)
    boat, extra_boats = P.build_boats(site, mats, cols['PROP_Survey'])
    veg = P.scatter_vegetation(site, mats, cols['VEG_Scatter'], xs, ys, hgrid)
    land_cut, bed_cut, water_cut, section_info = SC.build_section(
        site, mats, palette, cols['SEC_Section'])
    rigs = SC.build_camera_rig(site, palette, cols['CAM_Rigs'], scene,
                               section_info=section_info)
    SC.build_lighting(palette, cols['LGT_Rig'])
    SC.build_world(palette, scene)
    import look_rig
    grade = SC.build_compositor(scene, saturation=look_rig.RIG['grade_sat'])
    rig_applied = look_rig.apply(scene)

    # section geometry is authoring/guide content: never in the main beauty shots
    cols['SEC_Section'].hide_render = True

    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    # colour management belongs to look_rig.py alone: a second place that sets
    # view transform / exposure silently undid the measured look rig before.

    if save:
        bpy.ops.wm.save_as_mainfile(filepath=target)

    tris = 0
    for ob in list(bpy.context.scene.objects):
        if ob.type == 'MESH' and ob.data:
            me = ob.data
            tris += len(me.polygons) * 2
    objects = len(bpy.context.scene.objects)
    return {
        'site': site_key,
        'label': site['label'],
        'checkpoint': target,
        'scene': scene.name,
        'collections': sorted(c.name for c in bpy.data.collections),
        'objects': objects,
        'triangles_est': tris,
        'houses': houses,
        'vegetation': veg,
        'cameras': sorted(rigs.keys()),
        'terrain_verts': len(terrain.data.vertices),
        'boats': 1 + len(extra_boats),
        'has_section': land_cut is not None,
        'grade': grade,
        'rig': rig_applied,
    }
