"""Phase 06 · reopen the delivered .blend files and re-import every GLB.

    blender -b --factory-startup --python verify_exports.py

For each deliverable:
  * scene.blend / globe.blend / common-kit.blend are reopened and checked for
    packed images, water object, cameras, lights and object counts;
  * every GLB is imported into a clean temporary scene, and its bounds,
    orientation, object counts, material names, water object, cameras and lights
    are recorded; a shaded 960x540 shot of each import is saved under
    `work/renders/import-check/` so an unexpected result can be inspected later.

Writes `work/reports/import-check.json`. Nothing is claimed that was not read
back from the file.
"""
import json
import os
import struct
import sys

import bpy
from mathutils import Vector

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
OUTPUT = os.path.join(ART, 'output')
REPORTS = os.path.join(ART, 'work', 'reports')
SHOTS = os.path.join(ART, 'work', 'renders', 'import-check')

BLENDS = [
    ('globe', os.path.join(OUTPUT, 'globe', 'globe.blend')),
    ('kit', os.path.join(OUTPUT, 'kit', 'common-kit.blend')),
    ('kodingareng', os.path.join(OUTPUT, 'coasts', 'kodingareng', 'scene.blend')),
    ('tunda', os.path.join(OUTPUT, 'coasts', 'tunda', 'scene.blend')),
    ('amur', os.path.join(OUTPUT, 'coasts', 'amur', 'scene.blend')),
]
GLBS = [
    ('globe', os.path.join(OUTPUT, 'globe', 'globe.glb')),
    ('kit', os.path.join(OUTPUT, 'kit', 'common-kit.glb')),
    ('kodingareng', os.path.join(OUTPUT, 'coasts', 'kodingareng', 'coast.glb')),
    ('tunda', os.path.join(OUTPUT, 'coasts', 'tunda', 'coast.glb')),
    ('amur', os.path.join(OUTPUT, 'coasts', 'amur', 'coast.glb')),
]


def glb_json(path):
    with open(path, 'rb') as fh:
        magic, version, total = struct.unpack('<4sII', fh.read(12))
        length, chunk_type = struct.unpack('<II', fh.read(8))
        doc = json.loads(fh.read(length).decode('utf-8'))
    return doc


def check_blend(label, path):
    bpy.ops.wm.open_mainfile(filepath=path)
    scene = bpy.context.scene
    # only file-backed images matter for portability; "Render Result" and
    # "Viewer Node" are built-ins with no path
    images = [im for im in bpy.data.images
              if im.source == 'FILE' or (im.filepath and im.filepath != '<builtin>')]
    packed = [im.name for im in images if im.packed_file is not None]
    meshes = [ob for ob in scene.objects if ob.type == 'MESH']
    water = [ob.name for ob in scene.objects if ob.name.startswith('ENV_Water')]
    return {
        'kind': 'blend', 'label': label, 'path': path.replace('\\', '/'),
        'bytes': os.path.getsize(path),
        'scene': scene.name,
        'objects': len(scene.objects),
        'mesh_objects': len(meshes),
        'materials': len(bpy.data.materials),
        'images': len(images),
        'images_packed': len(packed),
        'all_file_images_packed': len(packed) == len(images),
        'water_objects': water,
        'cameras': sorted(ob.name for ob in scene.objects if ob.type == 'CAMERA'),
        'lights': sorted(ob.name for ob in scene.objects if ob.type == 'LIGHT'),
        'has_section_mesh': any(ob.name.startswith('SEC_') for ob in scene.objects),
    }


def check_glb(label, path):
    doc = glb_json(path)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    scene = bpy.context.scene
    objs = [ob for ob in scene.objects]
    meshes = [ob for ob in objs if ob.type == 'MESH']
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for ob in meshes:
        for corner in ob.bound_box:
            world = ob.matrix_world @ Vector(corner)
            lo = Vector((min(lo[i], world[i]) for i in range(3)))
            hi = Vector((max(hi[i], world[i]) for i in range(3)))
    dims = [round(hi[i] - lo[i], 3) for i in range(3)] if meshes else [0, 0, 0]

    mats = sorted({(ob.data.materials[0].name if ob.data and ob.data.materials
                    and ob.data.materials[0] else None) for ob in meshes} - {None})
    missing_images = [im.name for im in bpy.data.images
                      if im.source == 'FILE' and not im.packed_file]
    shot = os.path.join(SHOTS, '%s_import.png' % label)
    os.makedirs(SHOTS, exist_ok=True)
    try:
        scene.render.engine = 'BLENDER_WORKBENCH'
        scene.display.shading.light = 'STUDIO'
        scene.display.shading.color_type = 'MATERIAL'
        scene.render.resolution_x = 960
        scene.render.resolution_y = 540
        scene.render.image_settings.file_format = 'PNG'
        if not any(ob.type == 'CAMERA' for ob in objs):
            cam_data = bpy.data.cameras.new('IMPORT_CAM')
            cam = bpy.data.objects.new('IMPORT_CAM', cam_data)
            scene.collection.objects.link(cam)
            radius = max(dims) if meshes else 10.0
            cam.location = (radius * 1.4, -radius * 1.6, radius * 1.1)
            direction = (Vector((0, 0, 0)) - cam.location).normalized()
            cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
            scene.camera = cam
        scene.render.filepath = shot
        bpy.ops.render.render(write_still=True)
    except Exception as exc:
        shot = 'render failed: %s' % exc

    return {
        'kind': 'glb', 'label': label, 'path': path.replace('\\', '/'),
        'bytes': os.path.getsize(path),
        'json_cameras': len(doc.get('cameras', [])),
        'json_lights': len((doc.get('extensions') or {}).get(
            'KHR_lights_punctual', {}).get('lights', [])),
        'json_meshes': len(doc.get('meshes', [])),
        'json_nodes': len(doc.get('nodes', [])),
        'json_images': len(doc.get('images', [])),
        'imported_objects': len(objs),
        'imported_meshes': len(meshes),
        'materials': len(mats),
        'material_names': mats[:8],
        'dimensions_m': dims,
        'min': [round(v, 2) for v in lo], 'max': [round(v, 2) for v in hi],
        'water_objects': [ob.name for ob in objs if 'Water' in ob.name] if label != 'globe' else [],
        'missing_images': missing_images,
        'shot': shot,
    }


def main():
    results = {'blends': [], 'glbs': []}
    for label, path in BLENDS:
        if not os.path.exists(path):
            results['blends'].append({'label': label, 'error': 'missing'})
            continue
        try:
            results['blends'].append(check_blend(label, path))
        except Exception as exc:
            results['blends'].append({'label': label, 'error': str(exc)})
    for label, path in GLBS:
        if not os.path.exists(path):
            results['glbs'].append({'label': label, 'error': 'missing'})
            continue
        try:
            results['glbs'].append(check_glb(label, path))
        except Exception as exc:
            results['glbs'].append({'label': label, 'error': str(exc)})

    os.makedirs(REPORTS, exist_ok=True)
    target = os.path.join(REPORTS, 'import-check.json')
    tmp = target + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(results, fh, indent=2)
    os.replace(tmp, target)
    print('IMPORT-CHECK', target)
    for row in results['blends']:
        print('BLEND', row.get('label'), row.get('objects'), 'packed',
              row.get('images_packed'), '/', row.get('images'))
    for row in results['glbs']:
        print('GLB', row.get('label'), row.get('bytes'), 'meshes', row.get('imported_meshes'),
              'dims', row.get('dimensions_m'), 'cams', row.get('json_cameras'),
              'lights', row.get('json_lights'))


if __name__ == '__main__':
    main()
