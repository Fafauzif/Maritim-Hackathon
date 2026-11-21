"""Scene assembly: section slab, camera rigs, lighting, world, compositor, render."""
import math
import os

import bpy
import numpy as np

import site_lib as L
from site_lib import smoothstep
import props_build as P

WATER_Z = 0.0
ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"


# ----------------------------------------------------------------------------
# collections
# ----------------------------------------------------------------------------

def reset_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in list(bpy.data.collections):
        bpy.data.collections.remove(coll)
    scene = bpy.context.scene
    scene.name = 'CoastScene'
    return scene


def make_collections(scene):
    names = ['ENV_Land', 'ENV_Water', 'BLD_Village', 'PROP_Survey',
             'VEG_Scatter', 'SEC_Section', 'CAM_Rigs', 'LGT_Rig', 'GUIDE_Authoring']
    cols = {}
    for n in names:
        c = bpy.data.collections.new(n)
        scene.collection.children.link(c)
        cols[n] = c
    return cols


# ----------------------------------------------------------------------------
# section slab
# ----------------------------------------------------------------------------

def sample_axis(site, n=150):
    (ax, ay), (bx, by) = site["section_axis"]
    ts = np.linspace(0.0, 1.0, n)
    xs = ax + (bx - ax) * ts
    ys = ay + (by - ay) * ts
    return ts, xs, ys


def terrain_at(site, x, y):
    """Point-sample the same height field used for the terrain mesh."""
    arr_x = np.array([x])
    arr_y = np.array([y])
    from site_build import terrain_heights
    return float(terrain_heights(site, arr_x, arr_y)[0, 0])


def build_section(site, mats, palette, collection, depth=3.0):
    (ax, ay), (bx, by) = site["section_axis"]
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux                      # perpendicular, defines slab thickness
    ts, xs, ys = sample_axis(site, 150)
    hs = np.array([terrain_at(site, float(x), float(y)) for x, y in zip(xs, ys)])

    land_mat = L.make_material('MAT_Section_Land', (0.58, 0.50, 0.38), rough=0.95)
    bed_mat = L.make_material('MAT_Section_Bed', (0.34, 0.33, 0.28), rough=0.95)
    water_mat = L.make_material('MAT_Section_Water', palette["water"], rough=0.2,
                                alpha=0.45)
    cap_mat = L.make_material('MAT_Section_Cap', (0.86, 0.83, 0.74), rough=0.9)

    def slab(z_lo, z_hi, mat, name):
        verts, faces = [], []
        n = len(xs)
        for i in range(n):
            x = float(xs[i]); y = float(ys[i])
            fx, fy = x - px * depth / 2, y - py * depth / 2
            bx2, by2 = x + px * depth / 2, y + py * depth / 2
            verts.extend([(fx, fy, float(z_lo[i])), (fx, fy, float(z_hi[i])),
                          (bx2, by2, float(z_lo[i])), (bx2, by2, float(z_hi[i]))])
        for i in range(n - 1):
            a = i * 4
            b = (i + 1) * 4
            faces.append((a + 0, b + 0, b + 1, a + 1))      # front
            faces.append((a + 2, a + 3, b + 3, b + 2))      # back
            faces.append((a + 1, b + 1, b + 3, a + 3))      # top
            faces.append((a + 0, a + 2, b + 2, b + 0))      # bottom
        faces.append((0, 1, 3, 2))
        e = (n - 1) * 4
        faces.append((e + 0, e + 2, e + 3, e + 1))
        ob = L.mesh_from(name, verts, faces, [mat], collection)
        return ob

    uppers = np.maximum(hs, 0.0)
    lowers = np.minimum(hs, 0.0)

    # A cross-section must be SOLID: the old version drew land only from Z=0 up
    # and bed only below Z=0, so under dry land the cut was a void and the frame
    # measured 65-78% empty. Build one continuous block from a floor to the
    # terrain surface, then lay the water column on top of the seabed part.
    floor = float(min(float(hs.min()), 0.0)) - 2.0
    thick = np.maximum(hs - floor, 0.05)

    deep_mat = L.make_material('MAT_Section_Bed', (0.27, 0.27, 0.25), rough=0.95)
    mid_mat = L.make_material('MAT_Section_StratA', (0.44, 0.38, 0.30), rough=0.95)
    soil_mat = L.make_material('MAT_Section_Land', (0.60, 0.51, 0.38), rough=0.95)
    grass_mat = L.make_material('MAT_Section_Topsoil', (0.33, 0.40, 0.24), rough=0.95)
    water_mat = L.make_material('MAT_Section_Water', palette["water"], rough=0.2,
                                alpha=0.42)
    cap_mat = L.make_material('MAT_Section_Cap', (0.86, 0.83, 0.74), rough=0.9)

    rock = slab(np.full_like(hs, floor), floor + 0.55 * thick, deep_mat, 'SEC_BedCut')
    mid = slab(floor + 0.55 * thick, floor + 0.85 * thick, mid_mat, 'SEC_Stratum_A')
    land = slab(floor + 0.85 * thick, hs, soil_mat, 'SEC_LandCut')
    grass = slab(np.maximum(hs - 0.18, 0.0), np.maximum(hs, 0.0), grass_mat, 'SEC_Grass')
    water = slab(np.minimum(hs, 0.0), np.zeros_like(hs), water_mat, 'SEC_WaterBody')

    # surface line + measuring marker
    mb = P.MB()
    for i in range(len(xs) - 1):
        x0, y0 = float(xs[i]), float(ys[i])
        x1, y1 = float(xs[i + 1]), float(ys[i + 1])
        n = len(mb.verts)
        mb.verts.extend([(x0 - px * depth / 2, y0 - py * depth / 2, 0.04),
                         (x0 + px * depth / 2, y0 + py * depth / 2, 0.04),
                         (x1 + px * depth / 2, y1 + py * depth / 2, 0.04),
                         (x1 - px * depth / 2, y1 - py * depth / 2, 0.04)])
        mb.faces.append((n, n + 1, n + 2, n + 3))
        mb.mats.append(0)
    mb.to_mesh('SEC_WaterLine', [cap_mat], collection)

    # Vertical exaggeration: sections are illustrations, and a true-scale 7 m
    # water column over a 130 m cut is unreadable. Documented in review.md.
    zexag = float(site.get("section_exag", 2.2))
    for ob in (rock, mid, land, grass, water):
        ob.scale = (1.0, 1.0, zexag)

    # Report the world-space vertical band of the cut so the section camera can
    # frame it exactly instead of guessing a lens and distance.
    bounds = {
        'z_lo': float(floor * zexag),
        'z_hi': float(max(hs.max(), 0.0) * zexag),
        'zexag': zexag,
        'floor': floor,
        'center': (float(np.mean(xs)), float(np.mean(ys))),
        'length': float(length),
    }
    return land, rock, water, bounds


# ----------------------------------------------------------------------------
# cameras and empties
# ----------------------------------------------------------------------------

def make_empty(name, location, collection, size=3.0):
    ob = bpy.data.objects.new(name, None)
    ob.empty_display_type = 'PLAIN_AXES'
    ob.empty_display_size = size
    ob.location = location
    collection.objects.link(ob)
    return ob


def make_camera(name, lens, collection, ortho_scale=None):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.5
    data.clip_end = 4000.0
    if ortho_scale:
        data.type = 'ORTHO'
        data.ortho_scale = ortho_scale
    ob = bpy.data.objects.new(name, data)
    collection.objects.link(ob)
    return ob


def track_to(ob, target):
    con = ob.constraints.new('TRACK_TO')
    con.target = target
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    return con


def build_camera_rig(site, palette, collection, scene, section_info=None):
    rigs = {}
    s = site
    bx, by = s["boat"]

    e_orbit = make_empty('ORBIT_SITE', (0, 0, 0), collection, 8)
    e_water = make_empty('ORBIT_WATERFRONT', (bx * 0.55, by * 0.75, 1.0), collection, 6)
    e_boat = make_empty('TARGET_SURVEY', (bx, by, 1.2), collection, 5)

    cam = make_camera('COAST_OVERVIEW', s["overview"]["lens"], collection)
    cam.location = s["overview"]["pos"]
    tgt = make_empty('TARGET_OVERVIEW', s["overview"]["target"], collection, 6)
    track_to(cam, tgt)
    rigs['COAST_OVERVIEW'] = cam

    plan = make_camera('COAST_PLAN', 50.0, collection, ortho_scale=s["plan_scale"])
    plan.location = (0.0, 0.0, 620.0)
    plan.rotation_euler = (0.0, 0.0, 0.0)
    rigs['COAST_PLAN'] = plan

    app = make_camera('COAST_APPROACH', s["approach"]["lens"], collection)
    app.location = s["approach"]["pos"]
    tgt_app = make_empty('TARGET_APPROACH', s["approach"]["target"], collection, 5)
    track_to(app, tgt_app)
    rigs['COAST_APPROACH'] = app

    # Section: an orthographic camera square-on to the A-B plane, framed on the
    # waterfront/boat end of the cut. A perspective camera at scene distance
    # reduced a 134 m x 24 m cut to a thin ribbon in 88% empty sky.
    (ax, ay), (bx2, by2) = s["section_axis"]
    vx, vy = bx2 - ax, by2 - ay
    vlen = math.hypot(vx, vy)
    ux, uy = vx / vlen, vy / vlen
    nx, ny = uy, -ux                       # camera side; north ends up on the right
    info = section_info or {'z_lo': -8.0, 'z_hi': 8.0}
    z_lo, z_hi = info['z_lo'], info['z_hi']
    band = max(0.1, z_hi - z_lo)
    # Fill the 16:9 frame with the part of the cut that carries the story: the
    # land band plus the shallow-to-deep water column. Islands crop the deepest
    # bed tip (the diagram reads as continuing below frame); the estuary keeps
    # the whole column because the river channel IS the subject.
    fill = float(s.get("section_fill", 0.72))
    frame_h = max(12.0, band * fill)
    aspect = 16.0 / 9.0
    ortho_w = min(96.0, max(54.0, frame_h * aspect))
    frame_h = ortho_w / aspect
    z_mid = z_hi + 0.06 * frame_h - 0.5 * frame_h
    # centre the cut on the survey boat's projection onto the axis
    t_boat = ((bx - ax) * ux + (by - ay) * uy)
    t_boat = max(0.0, min(vlen, t_boat))
    cx, cy = ax + ux * t_boat, ay + uy * t_boat
    standoff = 140.0
    sec = make_camera('COAST_SECTION', 50.0, collection, ortho_scale=ortho_w)
    sec.location = (cx + nx * standoff, cy + ny * standoff, z_mid)
    e_sec = make_empty('TARGET_SECTION', (cx, cy, z_mid), collection, 6)
    track_to(sec, e_sec)
    sec.data.clip_start = 1.0
    sec.data.clip_end = 900.0
    rigs['COAST_SECTION'] = sec

    det = make_camera('COAST_DETAIL', s["detail"]["lens"], collection)
    det.location = s["detail"]["pos"]
    tgt_det = make_empty('TARGET_DETAIL', s["detail"]["target"], collection, 4)
    track_to(det, tgt_det)
    rigs['COAST_DETAIL'] = det

    scene.camera = cam
    return rigs


# ----------------------------------------------------------------------------
# lighting and world
# ----------------------------------------------------------------------------

def build_lighting(palette, collection):
    sun_data = bpy.data.lights.new('LGT_Sun_Key', 'SUN')
    sun_data.energy = 4.6
    sun_data.angle = math.radians(2.5)
    sun_data.color = (1.0, 0.96, 0.90)
    sun = bpy.data.objects.new('LGT_Sun_Key', sun_data)
    sun.rotation_euler = (math.radians(46), math.radians(4), math.radians(214))
    collection.objects.link(sun)

    fill_data = bpy.data.lights.new('LGT_Sky_Fill', 'AREA')
    fill_data.energy = 320.0
    fill_data.size = 260.0
    fill_data.color = (0.86, 0.92, 1.0)
    fill = bpy.data.objects.new('LGT_Sky_Fill', fill_data)
    fill.location = (-180.0, -120.0, 220.0)
    fill.rotation_euler = (math.radians(28), 0.0, math.radians(-35))
    collection.objects.link(fill)
    return sun, fill


def build_world(palette, scene):
    world = bpy.data.worlds.get('WD_Coast')
    if world is None:
        world = bpy.data.worlds.new('WD_Coast')
    scene.world = world
    try:
        world.use_nodes = True
    except Exception:
        pass
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    coord = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(coord.outputs['Generated'], sep.inputs[0])
    nt.links.new(sep.outputs['Z'], ramp.inputs[0])
    nt.links.new(ramp.outputs['Color'], bg.inputs['Color'])
    nt.links.new(bg.outputs[0], out.inputs['Surface'])
    ramp.color_ramp.elements[0].position = 0.30
    ramp.color_ramp.elements[0].color = (*palette["sky_horizon"], 1.0)
    ramp.color_ramp.elements[1].position = 0.78
    ramp.color_ramp.elements[1].color = (*palette["sky_top"], 1.0)
    bg.inputs['Strength'].default_value = 0.62
    return world


# ----------------------------------------------------------------------------
# compositor: paper wash + vignette
# ----------------------------------------------------------------------------

def build_compositor(scene, saturation=1.0):
    """Best-effort ink/paper grading. Blender 5.2 moved the compositor from
    `scene.node_tree` to `scene.compositing_node_group`; if either the accessor
    or a node type is missing, this reports a reason instead of failing a build.

    `saturation` is the measured lookdev knob: the audit's reference style sits
    at mean saturation 0.36, and AgX alone lands near 0.14, so the grade has to
    push chroma back after the tone map.
    """
    status = {'ok': False, 'reason': 'unavailable', 'saturation': saturation}
    try:
        scene.use_nodes = True
    except Exception:
        pass
    tree = getattr(scene, 'compositing_node_group', None)
    if tree is None and hasattr(scene, 'node_tree'):
        tree = getattr(scene, 'node_tree', None)
    if tree is None:
        try:
            tree = bpy.data.node_groups.new('NT_CoastGrade', 'CompositorNodeTree')
            if hasattr(scene, 'compositing_node_group'):
                scene.compositing_node_group = tree
        except Exception as exc:
            status['reason'] = 'no compositor tree: %s' % exc
            return status
    if tree is None:
        return status
    try:
        tree.nodes.clear()
        # Blender 5.2: a compositor tree IS a node group, and `CompositorNodeComposite`
        # no longer exists. The render result leaves through a group output socket,
        # which must be declared on the group interface first.
        if not [i for i in tree.interface.items_tree]:
            tree.interface.new_socket(name='Image', in_out='OUTPUT',
                                      socket_type='NodeSocketColor')
        rl = tree.nodes.new('CompositorNodeRLayers')
        hsv = tree.nodes.new('CompositorNodeHueSat')
        hsv.inputs['Saturation'].default_value = float(saturation)
        out = tree.nodes.new('NodeGroupOutput')
        tree.links.new(rl.outputs['Image'], hsv.inputs['Image'])
        tree.links.new(hsv.outputs['Image'], out.inputs['Image'])
        scene.render.use_compositing = True
        status = {'ok': True, 'reason': 'hue/sat group output', 'saturation': saturation}
    except Exception as exc:
        status = {'ok': False, 'reason': 'node build failed: %s' % exc}
    return status


# ----------------------------------------------------------------------------
# render
# ----------------------------------------------------------------------------

def render_still(scene, camera_name, path, res=(960, 540), engine='BLENDER_EEVEE',
                 samples=48, hide=(), show=()):
    cam = bpy.data.objects.get(camera_name)
    if cam is None:
        raise RuntimeError('missing camera %s' % camera_name)
    scene.camera = cam
    # reset every collection to visible, then apply this shot's visibility set
    for coll in bpy.data.collections:
        coll.hide_render = False
    for name in hide:
        coll = bpy.data.collections.get(name)
        if coll:
            coll.hide_render = True
    for name in show:
        coll = bpy.data.collections.get(name)
        if coll:
            coll.hide_render = False
    scene.render.engine = engine
    if engine == 'BLENDER_EEVEE':
        for attr, val in (('taa_render_samples', samples),):
            if hasattr(scene.eevee, attr):
                try:
                    setattr(scene.eevee, attr, val)
                except Exception:
                    pass
    elif engine == 'BLENDER_WORKBENCH':
        shading = scene.display.shading
        shading.light = 'STUDIO'
        style = os.environ.get('OCEAN_CLAY_STYLE', 'MATERIAL')
        shading.color_type = style
        if style == 'SINGLE':
            shading.single_color = (0.62, 0.62, 0.60)
        shading.show_shadows = True
        shading.shadow_intensity = 0.45
        shading.show_cavity = True
        shading.cavity_type = 'BOTH'
        shading.curvature_ridge_factor = 1.2
        shading.curvature_valley_factor = 1.2
        scene.display.render_aa = '8'
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    produced = path if os.path.exists(path) else scene.render.frame_path(frame=scene.frame_current)
    return {
        'path': produced,
        'exists': os.path.exists(produced),
        'bytes': os.path.getsize(produced) if os.path.exists(produced) else 0,
        'resolution': [scene.render.resolution_x, scene.render.resolution_y],
        'camera': camera_name,
        'engine': scene.render.engine,
    }
