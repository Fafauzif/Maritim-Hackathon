"""One shared look rig for all three coasts.

Every coast is lit and graded by exactly these numbers so the three scenes stay
comparable. The values were chosen by rendering a sweep of candidate rigs and
measuring the PNGs against the audit's reference band (luma 0.554, saturation
0.362 in `cityrt-audit/analysis/palette/italian.json`) rather than by eye.

Change a value here, rebuild all three scenes, and re-run the palette check.
"""
import bpy

RIG = {
    'view_transform': 'Khronos PBR Neutral',
    'look': 'None',
    'exposure': -0.35,
    'sun': 5.4,
    'fill': 150.0,
    'world': 0.28,
    'grade_sat': 1.2,
    'engine': 'BLENDER_EEVEE',
    'samples': 32,
}


def apply(scene=None, rig=None):
    rule = dict(RIG, **(rig or {}))
    scene = scene or bpy.context.scene
    vs = scene.view_settings
    vs.view_transform = rule['view_transform']
    try:
        vs.look = rule['look']
    except TypeError:
        vs.look = 'None'
    vs.exposure = rule['exposure']
    sun = bpy.data.objects.get('LGT_Sun_Key')
    if sun and sun.data:
        sun.data.energy = rule['sun']
    fill = bpy.data.objects.get('LGT_Sky_Fill')
    if fill and fill.data:
        fill.data.energy = rule['fill']
    world = scene.world
    if world and world.node_tree:
        for node in world.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs['Strength'].default_value = rule['world']
    tree = getattr(scene, 'compositing_node_group', None)
    if tree:
        for node in tree.nodes:
            if 'HueSat' in node.bl_idname:
                node.inputs['Saturation'].default_value = rule['grade_sat']
    return dict(rule)
