"""Phase 04 · the Earth globe scene.

Builds `work/checkpoints/04-globe.blend` from the supplied Natural Earth-based
colour art: a UV-mapped sphere with validated orientation, three original
locator markers, a wide hero camera and one regional camera per coast.

Orientation is verified against the texture itself (sample known land/seas at
their expected UV) before any render is trusted.

Run inside Blender:
    import globe_build; globe_build.build()
"""
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
GLOBE_REF = os.path.join(ART, 'references', 'globe')
if GLOBE_REF not in sys.path:
    sys.path.insert(0, GLOBE_REF)
import make_globe_seed as G  # noqa: E402  (provided starter: mesh + packed material)

CHECKPOINTS = os.path.join(ART, 'work', 'checkpoints')
RENDERS = os.path.join(ART, 'work', 'renders', 'globe')

RADIUS = 10.0
TEXTURE = os.path.join(GLOBE_REF, 'earth-base-color.jpg')

# indicative art anchors only — not survey coordinates
ANCHORS = {
    'kodingareng': ('Kodingareng Lompo', -5.09, 119.30),
    'tunda': ('Pulau Tunda', -5.79, 105.66),
    'amur': ('Razdolnaya mouth', 43.25, 131.80),
}

# known points used to prove the texture is not mirrored or upside down
# The supplied art repaints Antarctica in the same sand tone as other land, so
# the probe set uses land/ocean pairs that survive a mirror or a flip.
ORIENTATION_PROBES = [
    ('Sahara land', 23.0, 10.0, 'land'),
    ('Central Pacific', 0.0, -140.0, 'ocean'),
    ('Antarctica painted land', -80.0, 0.0, 'land'),
    ('Indian Ocean', -10.0, 80.0, 'ocean'),
    ('Siberia land', 60.0, 100.0, 'land'),
    ('Australia interior', -25.0, 134.0, 'land'),
    ('North America', 40.0, -100.0, 'land'),
    ('Atlantic Ocean', 0.0, -30.0, 'ocean'),
    ('Atlantic Ocean north', 40.0, -40.0, 'ocean'),
]


def surface_xyz(radius, longitude, latitude):
    return G.surface_xyz(radius, longitude, latitude)


def new_scene(name):
    scene = bpy.data.scenes.get(name)
    if scene:
        return scene
    scene = bpy.data.scenes.new(name)
    bpy.context.window.scene = scene
    return scene


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def add_marker(scene, name, lat, lon, collection):
    direction = surface_xyz(1.0, lon, lat)
    base = surface_xyz(RADIUS, lon, lat)
    accent = bpy.data.materials.get('MAT_Globe_Marker')
    if accent is None:
        accent = bpy.data.materials.new('MAT_Globe_Marker')
        accent.use_nodes = True
        bsdf = accent.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = (0.95, 0.55, 0.12, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4
        if 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = (0.95, 0.55, 0.12, 1.0)
            bsdf.inputs['Emission Strength'].default_value = 0.6
    dark = bpy.data.materials.get('MAT_Globe_Marker_Ring')
    if dark is None:
        dark = bpy.data.materials.new('MAT_Globe_Marker_Ring')
        dark.use_nodes = True
        b = dark.node_tree.nodes.get('Principled BSDF')
        b.inputs['Base Color'].default_value = (0.08, 0.07, 0.06, 1.0)
        b.inputs['Roughness'].default_value = 0.8

    # stem: a thin cone that points away from the surface
    import bmesh
    def cone_mesh(name_, r1, r2, depth, mat):
        me = bpy.data.meshes.new(name_)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r1,
                              radius2=r2, depth=depth)
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mat)
        return me

    stem_me = cone_mesh('MK_Stem_' + name, 0.055, 0.03, 0.42, dark)
    stem = bpy.data.objects.new('MK_Stem_' + name, stem_me)
    stem.location = base + direction * 0.21
    stem.rotation_mode = 'QUATERNION'
    stem.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(direction)
    collection.objects.link(stem)

    tip_me = cone_mesh('MK_Tip_' + name, 0.13, 0.0, 0.26, accent)
    tip = bpy.data.objects.new('MK_Tip_' + name, tip_me)
    tip.location = base + direction * 0.46
    tip.rotation_mode = 'QUATERNION'
    tip.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(direction)
    collection.objects.link(tip)

    anchor = bpy.data.objects.new('ANCHOR_' + name, None)
    anchor.empty_display_type = 'PLAIN_AXES'
    anchor.empty_display_size = 0.5
    anchor.location = base
    anchor['lat'] = lat
    anchor['lon'] = lon
    anchor['role'] = 'globe locator, indicative only'
    collection.objects.link(anchor)
    return anchor


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
    for label, lat, lon, expect in ORIENTATION_PROBES:
        rgb = sample(lat, lon)
        r, g, b = (float(c) for c in rgb)
        is_water = b > r and b > 0.25
        is_ice = r > 0.75 and g > 0.75 and b > 0.75
        ok = {'land': not is_water and not is_ice,
              'ocean': is_water,
              'ice': is_ice or (r > 0.6 and g > 0.6 and b > 0.6)}[expect]
        rows.append({'label': label, 'lat': lat, 'lon': lon, 'expected': expect,
                     'rgb': [round(r, 3), round(g, 3), round(b, 3)], 'ok': bool(ok)})
    return rows


def build(render=True):
    scene = new_scene('Earth_Globe')
    bpy.context.window.scene = scene
    # keep the globe scene self-contained
    for ob in list(scene.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in list(scene.collection.children):
        scene.collection.children.unlink(coll)

    globe_coll = bpy.data.collections.new('GLOBE_Surface')
    scene.collection.children.link(globe_coll)
    marker_coll = bpy.data.collections.new('GLOBE_Markers')
    scene.collection.children.link(marker_coll)
    cam_coll = bpy.data.collections.new('GLOBE_Cameras')
    scene.collection.children.link(cam_coll)
    light_coll = bpy.data.collections.new('GLOBE_Lights')
    scene.collection.children.link(light_coll)

    globe = bpy.data.objects.new('Earth_Surface', G.make_mesh(RADIUS))
    globe_coll.objects.link(globe)
    globe.data.materials.append(G.make_material(TEXTURE))
    globe['radius'] = RADIUS
    globe['anchor_convention'] = '+X lon 0, +Y lon 90E, +Z north'
    globe['art_note'] = 'Natural Earth 1:10m land, repainted colour art; not a data layer'

    for key, (label, lat, lon) in ANCHORS.items():
        add_marker(scene, key, lat, lon, marker_coll)

    world = bpy.data.worlds.get('Earth_World') or bpy.data.worlds.new('Earth_World')
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    bg.inputs['Color'].default_value = (0.012, 0.020, 0.030, 1.0)
    bg.inputs['Strength'].default_value = 0.9
    scene.world = world

    key = bpy.data.lights.new('GLOBE_Key_Sun', 'SUN')
    key.energy = 3.4
    key.angle = math.radians(6.0)
    key.color = (1.0, 0.96, 0.90)
    key_ob = bpy.data.objects.new('GLOBE_Key_Sun', key)
    key_ob.location = surface_xyz(2.0, 95.0, 35.0)
    aim(key_ob, (0, 0, 0))
    light_coll.objects.link(key_ob)

    rim = bpy.data.lights.new('GLOBE_Rim_Sun', 'SUN')
    rim.energy = 1.1
    rim.angle = math.radians(30.0)
    rim.color = (0.55, 0.75, 1.0)
    rim_ob = bpy.data.objects.new('GLOBE_Rim_Sun', rim)
    rim_ob.location = surface_xyz(2.0, 275.0, -10.0)
    aim(rim_ob, (0, 0, 0))
    light_coll.objects.link(rim_ob)

    # --- cameras -----------------------------------------------------------
    home = bpy.data.objects.new('GLOBE_HOME', bpy.data.cameras.new('GLOBE_HOME'))
    home.data.lens = 52.0
    home.data.clip_start = 0.5
    home.data.clip_end = 400.0
    # 6R keeps the whole limb inside a 16:9 frame at 52 mm (2*asin(1/6) = 19.2 deg
    # of a 26 deg vertical field) and still frames both Indonesian anchors and Amur.
    home.location = surface_xyz(6.0 * RADIUS, 118.0, 16.0)
    aim(home, (0, 0, 0))
    cam_coll.objects.link(home)
    scene.camera = home

    region_cams = {}
    for site, (label, lat, lon) in ANCHORS.items():
        cam = bpy.data.objects.new('GLOBE_REGION_' + site, bpy.data.cameras.new('GLOBE_REGION_' + site))
        cam.data.lens = 70.0
        cam.data.clip_start = 0.5
        cam.data.clip_end = 400.0
        cam.location = surface_xyz(2.05 * RADIUS, lon + 4.0, max(-68.0, min(68.0, lat + 20.0)))
        marker = bpy.data.objects.get('ANCHOR_' + site)
        aim(cam, marker.location if marker else (0, 0, 0))
        cam_coll.objects.link(cam)
        region_cams[site] = cam

    # slow reel orbit: parented camera swinging 24 deg of longitude over 72 frames
    orbit = bpy.data.objects.new('GLOBE_ORBIT', None)
    orbit.empty_display_type = 'CIRCLE'
    orbit.empty_display_size = 1.4 * RADIUS
    cam_coll.objects.link(orbit)
    reel = bpy.data.objects.new('GLOBE_REEL', bpy.data.cameras.new('GLOBE_REEL'))
    reel.data.lens = 52.0
    reel.data.clip_start = 0.5
    reel.data.clip_end = 400.0
    reel.parent = orbit
    reel.location = surface_xyz(6.0 * RADIUS, 0.0, 16.0)
    cam_coll.objects.link(reel)
    con = reel.constraints.new('TRACK_TO')
    con.target = orbit
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    orbit.rotation_euler = (0.0, 0.0, math.radians(104.0))
    orbit.keyframe_insert('rotation_euler', frame=1)
    orbit.rotation_euler = (0.0, 0.0, math.radians(128.0))
    orbit.keyframe_insert('rotation_euler', frame=72)
    # 5.2 layered actions: default Bezier interpolation with auto-clamped handles
    # is what we want here, so the handles are left alone.

    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
    scene.view_settings.exposure = 0.25
    scene.render.image_settings.file_format = 'PNG'

    # --- verify orientation against the texture itself ---------------------
    image = bpy.data.images.get('earth-base-color.jpg') or bpy.data.images.load(TEXTURE)
    probes = texture_probe(image)

    os.makedirs(CHECKPOINTS, exist_ok=True)
    checkpoint = os.path.join(CHECKPOINTS, '04-globe.blend')
    bpy.ops.wm.save_as_mainfile(filepath=checkpoint)

    renders = {}
    if render:
        os.makedirs(RENDERS, exist_ok=True)
        import scene_build as SC
        renders['overview'] = SC.render_still(scene, 'GLOBE_HOME',
                                              os.path.join(RENDERS, 'globe-overview-4k.png'),
                                              res=(3840, 2160), engine='BLENDER_EEVEE',
                                              samples=48)
        for site, cam in region_cams.items():
            renders['region_' + site] = SC.render_still(
                scene, cam.name, os.path.join(RENDERS, 'globe-region-%s.png' % site),
                res=(1920, 1080), engine='BLENDER_EEVEE', samples=32)

    return {
        'checkpoint': checkpoint,
        'objects': len(scene.objects),
        'anchors': {k: {'lat': v[1], 'lon': v[2]} for k, v in ANCHORS.items()},
        'orientation_probes': probes,
        'orientation_ok': all(p['ok'] for p in probes),
        'renders': {k: {'bytes': v.get('bytes'), 'path': v.get('path')} for k, v in renders.items()},
    }
