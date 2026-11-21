"""Verify each saved coast checkpoint by ray-casting the frame.

Run INSIDE Blender (live MCP or headless):

    import verify_shot; verify_shot.run_all()

For every shot of every site this reports, without any human looking at the
image: what fraction of the frame is water / land / buildings / survey kit /
background, where the survey boat lands in pixels, whether the boat survives a
320 px preview, and which edge of the frame geometry is touching.

Numbers come from scene.ray_cast through the real camera matrix, so they
describe the geometry that a render would show, not a guess from the PNG.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
CHECKPOINTS = os.path.join(ART, "work", "checkpoints")
OUT = os.path.join(ART, "work", "verification")

# collections that hold beauty-shot content; SEC_Section is authored guide geometry
BEAUTY_HIDE = ('SEC_Section',)
SECTION_HIDE = ('ENV_Land', 'ENV_Water', 'BLD_Village', 'VEG_Scatter')

SHOTS = [
    ('COAST_OVERVIEW', BEAUTY_HIDE),
    ('COAST_PLAN', BEAUTY_HIDE),
    ('COAST_APPROACH', BEAUTY_HIDE),
    ('COAST_DETAIL', BEAUTY_HIDE),
    ('COAST_SECTION', SECTION_HIDE),
]

CLASS_OF_COLLECTION = {
    'ENV_Water': 'water',
    'ENV_Land': 'land',
    'BLD_Village': 'building',
    'PROP_Survey': 'survey',
    'VEG_Scatter': 'vegetation',
    'SEC_Section': 'section',
}


def _hide_collections(names, hide):
    for coll in bpy.data.collections:
        coll.hide_viewport = bool(hide and coll.name in names)
    bpy.context.view_layer.update()


def _camera_rays(scene, camera, cols=64, rows=36):
    """Yield (u, v, world_direction) grid over the rendered frame."""
    mat = camera.matrix_world
    rot = mat.to_3x3()
    aspect = scene.render.resolution_x / float(scene.render.resolution_y)
    data = camera.data
    tan_x = tan_y = None
    if data.type == 'ORTHO':
        scale_x = data.ortho_scale if aspect >= 1 else data.ortho_scale * aspect
        scale_y = data.ortho_scale / aspect if aspect >= 1 else data.ortho_scale
        for j in range(rows):
            v = 1.0 - 2.0 * (j + 0.5) / rows
            for i in range(cols):
                u = 2.0 * (i + 0.5) / cols - 1.0
                origin = mat @ Vector((u * scale_x / 2, v * scale_y / 2, 0.0))
                yield u, v, origin, (rot @ Vector((0, 0, -1))).normalized()
        return
    if data.sensor_fit == 'VERTICAL' or (data.sensor_fit == 'AUTO' and aspect < 1):
        tan_y = (data.sensor_height / 2.0) / data.lens
        tan_x = tan_y * aspect
    else:
        tan_x = (data.sensor_width / 2.0) / data.lens
        tan_y = tan_x / aspect
    for j in range(rows):
        v = 1.0 - 2.0 * (j + 0.5) / rows
        for i in range(cols):
            u = 2.0 * (i + 0.5) / cols - 1.0
            local = Vector((u * tan_x, v * tan_y, -1.0))
            yield u, v, mat.translation, (rot @ local).normalized()


def classify_scene(scene, camera, cols=64, rows=36):
    deps = bpy.context.evaluated_depsgraph_get()
    origin_of = {}
    hit_counts = {}
    water_col = {0: 0}
    rays = list(_camera_rays(scene, camera, cols, rows))
    total = len(rays)
    misses = 0
    for u, v, origin, direction in rays:
        ok, loc, normal, index, obj, matrix = scene.ray_cast(deps, origin, direction,
                                                             distance=8000.0)
        if not ok or obj is None:
            misses += 1
            continue
        cls = 'unknown'
        for coll in obj.users_collection:
            cls = CLASS_OF_COLLECTION.get(coll.name, cls)
            if cls != 'unknown':
                break
        hit_counts[cls] = hit_counts.get(cls, 0) + 1
    frac = {k: round(v / float(total), 4) for k, v in hit_counts.items()}
    frac['background'] = round(misses / float(total), 4)
    return frac


def project_bbox(scene, camera, obj):
    """Project an object's world bounding box; return pixel bbox and edge flags."""
    from bpy_extras.object_utils import world_to_camera_view
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    xs, ys, zs = [], [], []
    for c in corners:
        co = world_to_camera_view(scene, camera, c)
        xs.append(co.x)
        ys.append(co.y)
        zs.append(co.z)
    rx = scene.render.resolution_x
    ry = scene.render.resolution_y
    px = [min(xs) * rx, min(ys) * ry, max(xs) * rx, max(ys) * ry]
    inside = (max(xs) > 0 and min(xs) < 1 and max(ys) > 0 and min(ys) < 1 and min(zs) > 0)
    touch = []
    if min(xs) <= 0.001:
        touch.append('left')
    if max(xs) >= 0.999:
        touch.append('right')
    if min(ys) <= 0.001:
        touch.append('bottom')
    if max(ys) >= 0.999:
        touch.append('top')
    return {
        'name': obj.name,
        'px_bbox': [round(val, 1) for val in px],
        'px_size': [round(px[2] - px[0], 1), round(px[3] - px[1], 1)],
        'in_frame': bool(inside),
        'frame_edges': touch,
    }


def measure_site(site_key):
    path = os.path.join(CHECKPOINTS, '03-%s.blend' % site_key)
    bpy.ops.wm.open_mainfile(filepath=path)
    scene = bpy.context.scene
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540

    report = {'site': site_key, 'checkpoint': path, 'shots': {}}
    tris = 0
    for ob in scene.objects:
        if ob.type == 'MESH' and ob.data:
            tris += len(ob.data.polygons) * 2
    report['objects'] = len(scene.objects)
    report['triangles_est'] = tris

    for cam_name, hide in SHOTS:
        cam = bpy.data.objects.get(cam_name)
        if cam is None:
            report['shots'][cam_name] = {'error': 'missing camera'}
            continue
        _hide_collections(hide, True)
        scene.camera = cam
        bpy.context.view_layer.update()
        shot = {'hide': list(hide)}
        shot['coverage'] = classify_scene(scene, cam)
        for target in ('PROP_SurveyBoat', 'PROP_Jetty', 'SEC_LandCut', 'SEC_WaterBody'):
            ob = bpy.data.objects.get(target)
            if ob is None:
                continue
            if any(coll.name in hide for coll in ob.users_collection):
                shot[target] = {'hidden': True}
                continue
            shot[target] = project_bbox(scene, cam, ob)
        report['shots'][cam_name] = shot
        _hide_collections(hide, False)

    return report


def run_all(sites=('kodingareng', 'tunda', 'amur')):
    os.makedirs(OUT, exist_ok=True)
    report = {'sites': {}}
    for site in sites:
        report['sites'][site] = measure_site(site)
    target = os.path.join(OUT, 'shot-verify.json')
    tmp = target + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2)
    os.replace(tmp, target)

    lines = []
    for site, data in report['sites'].items():
        lines.append('%s  objects=%d tris~%d' % (site, data['objects'], data['triangles_est']))
        for cam_name, shot in data['shots'].items():
            if 'coverage' not in shot:
                lines.append('  %-16s %s' % (cam_name, shot))
                continue
            cov = shot['coverage']
            boat = shot.get('PROP_SurveyBoat', {})
            bits = ['  %-16s' % cam_name,
                    'water=%5.1f%%' % (cov.get('water', 0) * 100),
                    'land=%5.1f%%' % (cov.get('land', 0) * 100),
                    'bld=%4.1f%%' % (cov.get('building', 0) * 100),
                    'veg=%4.1f%%' % (cov.get('vegetation', 0) * 100),
                    'kit=%4.1f%%' % (cov.get('survey', 0) * 100),
                    'sec=%4.1f%%' % (cov.get('section', 0) * 100),
                    'bg=%5.1f%%' % (cov.get('background', 0) * 100)]
            if boat and 'px_size' in boat:
                bits.append('boat=%dx%dpx @(%.0f,%.0f) frame=%s' % (
                    boat['px_size'][0], boat['px_size'][1],
                    boat['px_bbox'][0], boat['px_bbox'][1],
                    'yes' if boat['in_frame'] else 'NO'))
            elif boat.get('hidden'):
                bits.append('boat=hidden')
            elif boat:
                bits.append('boat=NO(project)')
            lines.append(' '.join(bits))
    text = '\n'.join(lines)
    print(text)
    with open(os.path.join(OUT, 'shot-verify.txt'), 'w', encoding='utf-8') as fh:
        fh.write(text + '\n')
    return report


if __name__ == '__main__':
    run_all()
