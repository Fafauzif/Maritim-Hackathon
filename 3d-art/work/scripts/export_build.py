"""Phase 06 · promote scenes and export GLBs.

    blender -b 02-kit.blend   --python export_build.py -- kit
    blender -b 04-globe.blend --python export_build.py -- globe
    blender -b 03-kodingareng.blend --python export_build.py -- coast kodingareng

Each mode:
  * packs external images into the .blend,
  * writes the editable scene to `output/`,
  * strips render-only outline modifiers and guide objects, then exports a
    GLB with no cameras and no lights,
  * records object/mesh/material/texture counts as JSON for export-check.md.

Cameras and lights are excluded from every GLB by exporter flags; the section
mesh, the kit stage and its swatch spheres are excluded by selection.
"""
import json
import os
import sys

import bpy

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
OUTPUT = os.path.join(ART, 'output')
CHECKPOINTS = os.path.join(ART, 'work', 'checkpoints')
REPORTS = os.path.join(ART, 'work', 'reports')

COAST_EXPORT_COLLECTIONS = ('ENV_Land', 'ENV_Water', 'BLD_Village', 'PROP_Survey',
                            'VEG_Scatter', 'CAM_Rigs')
COAST_SKIP_PREFIX = ('LBL_',)


def _pack(scene):
    try:
        bpy.ops.file.pack_all()
        return True
    except Exception as exc:
        print('pack_all failed:', exc)
        return False


def _strip_render_only():
    """Remove inverted-hull outline modifiers: they are a render trick, not art
    geometry, and they would triple the exported polygon count."""
    removed = 0
    for ob in bpy.data.objects:
        if ob.type != 'MESH':
            continue
        for mod in list(ob.modifiers):
            if 'Outline' in mod.name or 'InkOutline' in mod.name:
                ob.modifiers.remove(mod)
                removed += 1
    return removed


def _select_objects(objs):
    for ob in bpy.context.scene.objects:
        ob.select_set(False)
    for ob in objs:
        ob.select_set(True)
    if objs:
        bpy.context.view_layer.objects.active = objs[0]


def _glb(path, used_objects, extra_args=None):
    _select_objects(used_objects)
    args = dict(
        filepath=path,
        export_format='GLB',
        use_selection=True,
        export_cameras=False,
        export_lights=False,
        export_apply=True,
        export_yup=True,
        export_extras=True,
    )
    if extra_args:
        args.update(extra_args)
    bpy.ops.export_scene.gltf(**args)
    return {'path': path, 'bytes': os.path.getsize(path)}


def _scene_stats(scene):
    meshes = [ob for ob in scene.objects if ob.type == 'MESH']
    tris = 0
    for ob in meshes:
        if ob.data:
            tris += len(ob.data.polygons) * 2
    return {
        'objects': len(scene.objects),
        'mesh_objects': len(meshes),
        'triangles_est': tris,
        'materials': len(bpy.data.materials),
        'images': len(bpy.data.images),
        'has_water_object': any(ob.name.startswith('ENV_Water') for ob in scene.objects),
        'cameras': sorted(ob.name for ob in scene.objects if ob.type == 'CAMERA'),
        'lights': sorted(ob.name for ob in scene.objects if ob.type == 'LIGHT'),
    }


def _report(name, data):
    os.makedirs(REPORTS, exist_ok=True)
    path = os.path.join(REPORTS, 'export-%s.json' % name)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2)
    os.replace(tmp, path)
    print('REPORT', path)


def export_coast(site):
    scene = bpy.context.scene
    out_dir = os.path.join(OUTPUT, 'coasts', site)
    os.makedirs(out_dir, exist_ok=True)
    packed = _pack(scene)

    blend_path = os.path.join(out_dir, 'scene.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    removed = _strip_render_only()
    used = []
    for coll_name in COAST_EXPORT_COLLECTIONS:
        coll = bpy.data.collections.get(coll_name)
        if not coll:
            continue
        for ob in coll.all_objects:
            if ob.type in ('MESH', 'EMPTY') and not ob.name.startswith(COAST_SKIP_PREFIX):
                used.append(ob)

    glb = _glb(os.path.join(out_dir, 'coast.glb'), used)
    report = {
        'kind': 'coast', 'site': site, 'packed': packed,
        'blend': blend_path, 'glb': glb, 'outline_modifiers_removed': removed,
        'exported_objects': len(used),
        'scene_stats': _scene_stats(scene),
        'export': {'cameras': False, 'lights': False, 'yup': True, 'apply': True,
                   'collections': list(COAST_EXPORT_COLLECTIONS)},
    }
    _report('coast-' + site, report)
    return report


def export_globe():
    # only the globe scene belongs in the deliverable
    for sc in list(bpy.data.scenes):
        if sc.name != 'Earth_Globe':
            bpy.data.scenes.remove(sc)
    scene = bpy.data.scenes.get('Earth_Globe')
    bpy.context.window.scene = scene
    out_dir = os.path.join(OUTPUT, 'globe')
    os.makedirs(out_dir, exist_ok=True)
    packed = _pack(scene)
    blend_path = os.path.join(out_dir, 'globe.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    used = [ob for ob in scene.objects if ob.name.startswith(('Earth_Surface', 'MK_', 'ANCHOR_'))]
    globe = _glb(os.path.join(out_dir, 'globe.glb'), used)
    report = {
        'kind': 'globe', 'packed': packed, 'blend': blend_path, 'glb': globe,
        'exported_objects': len(used),
        'scene_stats': _scene_stats(scene),
        'anchors': sorted(ob.name for ob in scene.objects if ob.name.startswith('ANCHOR_')),
    }
    _report('globe', report)
    return report


def export_kit():
    scene = bpy.context.scene
    out_dir = os.path.join(OUTPUT, 'kit')
    os.makedirs(out_dir, exist_ok=True)
    packed = _pack(scene)
    blend_path = os.path.join(out_dir, 'common-kit.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    used = []
    for coll_name in ('KIT_Structures', 'KIT_Survey', 'KIT_Vegetation'):
        coll = bpy.data.collections.get(coll_name)
        if not coll:
            continue
        used.extend([ob for ob in coll.all_objects if ob.type in ('MESH', 'EMPTY')])
    used.extend([ob for ob in scene.objects
                 if ob.name.startswith('KIT_House_') and ob not in used])
    removed = _strip_render_only()
    kit = _glb(os.path.join(out_dir, 'common-kit.glb'), used)
    report = {
        'kind': 'kit', 'packed': packed, 'blend': blend_path, 'glb': kit,
        'outline_modifiers_removed': removed, 'exported_objects': len(used),
        'scene_stats': _scene_stats(scene),
    }
    _report('kit', report)
    return report


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    if not argv:
        raise SystemExit('need a mode: kit|globe|coast <site>')
    mode = argv[0]
    if mode == 'coast':
        report = export_coast(argv[1])
    elif mode == 'globe':
        report = export_globe()
    elif mode == 'kit':
        report = export_kit()
    else:
        raise SystemExit('unknown mode ' + mode)
    print('EXPORTED', json.dumps({k: v for k, v in report.items()
                                  if k in ('kind', 'site', 'glb', 'exported_objects')}))


if __name__ == '__main__':
    main()
