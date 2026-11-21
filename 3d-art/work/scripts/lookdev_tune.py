"""Lookdev tuning: render the same camera under candidate light/transform rigs.

Run inside Blender after a coast scene is open:

    import lookdev_tune
    lookdev_tune.run('kodingareng')      # writes work/renders/lookdev/*.png

Then measure the PNGs with palette_check.py and pick the variant that lands in
the audit's measured band (luma ~0.55, saturation ~0.36). No image is attached
to the conversation: the decision is made from numbers on disk.
"""
import os
import sys

import bpy

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
OUT = os.path.join(ART, 'work', 'renders', 'lookdev')

# name, view transform, look, exposure, sun energy, fill energy, world strength
VARIANTS = [
    ('A_baseline',        'AgX', 'AgX - Medium High Contrast', 0.10, 4.6, 320.0, 0.62),
    ('B_punch',           'AgX', 'AgX - Punchy',               0.00, 5.2, 180.0, 0.38),
    ('C_punch_deep',      'AgX', 'AgX - Punchy',              -0.20, 5.6, 150.0, 0.30),
    ('D_high_contrast',   'AgX', 'AgX - High Contrast',        0.00, 5.0, 200.0, 0.35),
    ('E_pbr_neutral',     'Khronos PBR Neutral', 'None',       0.00, 5.0, 180.0, 0.35),
    ('F_pbr_neutral_dk',  'Khronos PBR Neutral', 'None',      -0.15, 5.4, 150.0, 0.28),
    ('G_base_contrast',   'AgX', 'AgX - Base Contrast',        0.10, 5.2, 200.0, 0.40),
    ('H_standard',        'Standard', 'None',                 -0.30, 4.2, 160.0, 0.30),
]


def _set_world_strength(strength):
    world = bpy.context.scene.world
    if not world or not world.node_tree:
        return
    for node in world.node_tree.nodes:
        if node.type == 'BACKGROUND':
            node.inputs['Strength'].default_value = strength


def apply_rig(view_transform, look, exposure, sun, fill, world_strength):
    scene = bpy.context.scene
    vs = scene.view_settings
    vs.view_transform = view_transform
    try:
        vs.look = look
    except TypeError:
        vs.look = 'None'
    vs.exposure = exposure
    sun_ob = bpy.data.objects.get('LGT_Sun_Key')
    if sun_ob and sun_ob.data:
        sun_ob.data.energy = sun
    fill_ob = bpy.data.objects.get('LGT_Sky_Fill')
    if fill_ob and fill_ob.data:
        fill_ob.data.energy = fill
    _set_world_strength(world_strength)


def run(site='kodingareng', camera='COAST_OVERVIEW', res=(960, 540), samples=32):
    os.makedirs(OUT, exist_ok=True)
    import scene_build as SC
    scene = bpy.context.scene
    made = []
    for name, vt, look, exp, sun, fill, world in VARIANTS:
        apply_rig(vt, look, exp, sun, fill, world)
        path = os.path.join(OUT, '%s_%s.png' % (site, name))
        info = SC.render_still(scene, camera, path, res=res, engine='BLENDER_EEVEE',
                               samples=samples, hide=('SEC_Section',))
        made.append({'variant': name, 'path': info['path'], 'bytes': info['bytes'],
                     'rig': {'view_transform': vt, 'look': look, 'exposure': exp,
                             'sun': sun, 'fill': fill, 'world': world}})
    # leave the scene on the baseline rig; the winner is applied deliberately
    name, vt, look, exp, sun, fill, world = VARIANTS[0]
    apply_rig(vt, look, exp, sun, fill, world)
    print('lookdev variants written to', OUT)
    return made


def apply_winner(view_transform, look, exposure, sun, fill, world_strength):
    apply_rig(view_transform, look, exposure, sun, fill, world_strength)
    return {'view_transform': view_transform, 'look': look, 'exposure': exposure,
            'sun': sun, 'fill': fill, 'world': world_strength}
