"""Props, settlement, section, cameras, lighting and render helpers."""
import math
import os

import bmesh
import bpy
import numpy as np

import site_lib as L
from site_lib import box_mesh, mesh_from, add_outline, smoothstep

WATER_Z = 0.0


# ----------------------------------------------------------------------------
# materials for one site
# ----------------------------------------------------------------------------

def site_materials(palette):
    m = {}
    m['wall_a'] = L.make_material('MAT_Wall_A', palette["wall_a"], rough=0.92)
    m['wall_b'] = L.make_material('MAT_Wall_B', palette["wall_b"], rough=0.92)
    m['wall_c'] = L.make_material('MAT_Wall_C', palette["wall_c"], rough=0.92)
    m['roof_a'] = L.make_material('MAT_Roof_A', palette["roof_a"], rough=0.94)
    m['roof_b'] = L.make_material('MAT_Roof_B', palette["roof_b"], rough=0.94)
    m['trim'] = L.make_material('MAT_Trim', palette["trim"], rough=0.82)
    m['glass'] = L.make_material('MAT_Window', palette["glass"], rough=0.55)
    m['timber'] = L.make_material('MAT_Timber', palette["timber"], rough=0.9)
    m['deck'] = L.make_material('MAT_Deck', palette["deck"], rough=0.9)
    m['hull'] = L.make_material('MAT_Hull', palette["hull"], rough=0.75)
    m['stripe'] = L.make_material('MAT_HullStripe', palette["hull_stripe"], rough=0.7)
    m['leaf'] = L.make_material('MAT_Leaf', palette["leaf"], rough=0.95)
    m['trunk'] = L.make_material('MAT_Trunk', palette["trunk"], rough=0.95)
    m['reef'] = L.make_material('MAT_Bush', palette["veg"], rough=0.95)
    return m


# ----------------------------------------------------------------------------
# mesh builder
# ----------------------------------------------------------------------------

class MB:
    """Accumulate vertices/faces with per-face material indices."""

    def __init__(self):
        self.verts = []
        self.faces = []
        self.mats = []

    def quad(self, p0, p1, p2, p3, mi):
        n = len(self.verts)
        self.verts.extend([p0, p1, p2, p3])
        self.faces.append((n, n + 1, n + 2, n + 3))
        self.mats.append(mi)

    def tri(self, p0, p1, p2, mi):
        n = len(self.verts)
        self.verts.extend([p0, p1, p2])
        self.faces.append((n, n + 1, n + 2))
        self.mats.append(mi)

    def box(self, center, size, mi, rot_z=0.0):
        cx, cy, cz = center
        hx, hy, hz = size[0] / 2, size[1] / 2, size[2] / 2
        local = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
                 (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]
        ca, sa = math.cos(rot_z), math.sin(rot_z)
        pts = []
        for x, y, z in local:
            pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca, cz + z))
        n = len(self.verts)
        self.verts.extend(pts)
        for f in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                  (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            self.faces.append(tuple(n + i for i in f))
            self.mats.append(mi)

    def to_mesh(self, name, materials, collection):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.verts, [], self.faces)
        me.update()
        for mat in materials:
            me.materials.append(mat)
        if self.mats:
            me.polygons.foreach_set('material_index', self.mats)
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        me.validate()
        ob = bpy.data.objects.new(name, me)
        collection.objects.link(ob)
        return ob


# ----------------------------------------------------------------------------
# buildings
# ----------------------------------------------------------------------------

def _detach(ob):
    """Keep the mesh datablock, drop the prototype object from the scene."""
    me = ob.data
    bpy.data.objects.remove(ob, do_unlink=True)
    return me


def house_mesh(name, mats, w, d, wall_h, roof_h=1.5, roof='gable',
               stilt=0.0, ridge_axis='x', windows=True, chimney=False):
    """Local-space house. Origin at footprint centre on the ground."""
    mb = MB()
    MI_WALL, MI_ROOF_A, MI_ROOF_B, MI_TRIM, MI_GLASS, MI_TIMBER = 0, 1, 2, 3, 4, 5
    material_list = [mats['wall_a'], mats['roof_a'], mats['roof_b'],
                     mats['trim'], mats['glass'], mats['timber']]

    z0 = stilt
    if stilt > 0.0:
        for sx in (-1, 1):
            for sy in (-1, 1):
                mb.box((sx * (w / 2 - 0.5), sy * (d / 2 - 0.5), stilt / 2),
                       (0.26, 0.26, stilt), MI_TIMBER)
        mb.box((0, 0, stilt + 0.08), (w + 0.2, d + 0.2, 0.16), MI_TRIM)

    # walls
    mb.box((0, 0, z0 + wall_h / 2), (w, d, wall_h), MI_WALL)

    # door + windows on the -Y facade
    mb.box((0, -d / 2 - 0.03, z0 + 1.0), (0.95, 0.08, 2.0), MI_TIMBER)
    if windows:
        for sx in (-1, 1):
            mb.box((sx * w * 0.28, -d / 2 - 0.03, z0 + wall_h * 0.62),
                   (min(1.1, w * 0.22), 0.07, 0.85), MI_GLASS)
        for sy in (-1, 1):
            mb.box((-w / 2 - 0.03, sy * d * 0.22, z0 + wall_h * 0.62),
                   (0.07, min(1.0, d * 0.22), 0.8), MI_GLASS)

    top = z0 + wall_h
    ov = 0.36
    if roof == 'flat':
        mb.box((0, 0, top + 0.14), (w + 0.3, d + 0.3, 0.28), MI_ROOF_A)
    elif roof == 'hip':
        hw, hd = w / 2 + ov, d / 2 + ov
        ridge_y = 0.0
        r0 = (-w * 0.28, ridge_y, top + roof_h)
        r1 = (w * 0.28, ridge_y, top + roof_h)
        e = [(-hw, -hd, top), (hw, -hd, top), (hw, hd, top), (-hw, hd, top)]
        mb.quad(e[0], e[1], r1, r0, MI_ROOF_A)          # south slope
        mb.quad(e[2], e[3], r0, r1, MI_ROOF_A)          # north slope
        mb.tri(e[1], e[2], r1, MI_ROOF_A)               # east hip
        mb.tri(e[3], e[0], r0, MI_ROOF_A)               # west hip
    else:  # gable
        if ridge_axis == 'x':
            hw, hd = w / 2 + ov, d / 2 + ov
            ridge = top + roof_h
            mb.quad((-hw, -hd, top), (hw, -hd, top), (hw, 0, ridge), (-hw, 0, ridge), MI_ROOF_A)
            mb.quad((hw, hd, top), (-hw, hd, top), (-hw, 0, ridge), (hw, 0, ridge), MI_ROOF_A)
            mb.tri((-hw, -hd, top), (-hw, 0, ridge), (-hw, hd, top), MI_TRIM)
            mb.tri((hw, hd, top), (hw, 0, ridge), (hw, -hd, top), MI_TRIM)
        else:
            hw, hd = w / 2 + ov, d / 2 + ov
            ridge = top + roof_h
            mb.quad((-hw, -hd, top), (-hw, hd, top), (0, hd, ridge), (0, -hd, ridge), MI_ROOF_A)
            mb.quad((hw, hd, top), (hw, -hd, top), (0, -hd, ridge), (0, hd, ridge), MI_ROOF_A)
            mb.tri((-hw, -hd, top), (0, -hd, ridge), (hw, -hd, top), MI_TRIM)
            mb.tri((hw, hd, top), (0, hd, ridge), (-hw, hd, top), MI_TRIM)
    if chimney:
        mb.box((w * 0.28, d * 0.18, top + roof_h * 0.55 + 0.4), (0.5, 0.5, 1.3), MI_TIMBER)
        mb.box((w * 0.28, d * 0.18, top + roof_h * 0.55 + 1.08), (0.62, 0.62, 0.12), MI_TRIM)
    return _detach(mb.to_mesh(name, material_list, bpy.context.scene.collection))


def house_variants(mats, site):
    """Four footprint families drawn from the audit's 5 m cell ladder."""
    stilt = 0.75 if site.get("stilt") else 0.0
    variants = [
        # name,        w,   d,  wall, roof_h, roof,      ridge
        ('H_A', 6.0, 5.0, 2.8, 1.5, 'gable', 'x'),
        ('H_B', 10.0, 5.0, 3.0, 1.6, 'hip', 'x'),
        ('H_C', 5.0, 5.0, 2.7, 1.2, 'flat', 'x'),
        ('H_D', 15.0, 10.0, 3.4, 2.0, 'gable', 'y'),
    ]
    meshes = []
    for name, w, d, wall, rh, kind, ridge in variants:
        me = house_mesh(name, mats, w, d, wall, rh, roof=kind, stilt=stilt,
                        ridge_axis=ridge, chimney=(name in ('H_B', 'H_D')))
        meshes.append(me)
    return meshes


def _sample_height(xs, ys, h, x, y):
    i = int(np.clip((x - xs[0]) / (xs[1] - xs[0]), 0, len(xs) - 2))
    j = int(np.clip((y - ys[0]) / (ys[1] - ys[0]), 0, len(ys) - 2))
    return float(h[j, i])


def place_settlement(site, mats, collection, xs, ys, hgrid):
    """Cluster the village along the shore with real lanes between rows.

    Houses snap to the audit's 5 m cell ladder, each cluster faces the water, and
    a share of cells stays empty so the settlement reads as streets, not a slab.
    """
    meshes = house_variants(mats, site)
    rng = np.random.default_rng(7)
    s = site["settle"]
    cx, cy = s["cluster_anchor"]
    cluster_r = s.get("cluster_r", 34.0)
    placed = 0

    centres = [(cx, cy)]
    if s.get("cluster_count", 1) > 1:
        ring_r = s.get("cluster_spread", 46.0)
        for k in range(1, s["cluster_count"]):
            a = 2 * math.pi * k / s["cluster_count"] + 0.6
            centres.append((cx + math.cos(a) * ring_r, cy + math.sin(a) * ring_r))

    occupied = set()
    for (ccx, ccy) in centres:
        n = int(cluster_r / 2.5)
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                gx = round((ccx + i * 5.0) / 5.0) * 5.0
                gy = round((ccy + j * 5.0) / 5.0) * 5.0
                if math.hypot(gx - ccx, gy - ccy) > cluster_r:
                    continue
                if not (s["x0"] - 8 <= gx <= s["x1"] + 8 and s["y0"] - 8 <= gy <= s["y1"] + 8):
                    continue
                z = _sample_height(xs, ys, hgrid, gx, gy)
                if z < 0.6 or z > 6.5:
                    continue
                # lanes: leave a share of cells empty, denser near the waterfront
                lane_keep = 0.78 if z < 2.4 else 0.58
                if rng.random() > lane_keep:
                    continue
                variant = int(rng.choice([0, 0, 0, 2, 1]))
                w = [6.0, 10.0, 5.0, 15.0][variant]
                d = [5.0, 5.0, 5.0, 10.0][variant]
                # face the water, snapped to 90 degrees so footprints do not interpenetrate
                ang = math.atan2(gy - site.get("center", (0, 0))[1], gx - site.get("center", (0, 0))[0])
                ang = round((ang - math.pi / 2) / (math.pi / 2)) * (math.pi / 2)
                rot90 = int(round(abs(ang) / (math.pi / 2))) % 2
                span_x, span_y = (w, d) if rot90 == 0 else (d, w)
                cells = set()
                for ix in range(int(math.ceil(span_x / 5.0))):
                    for iy in range(int(math.ceil(span_y / 5.0))):
                        cells.add((int(round(gx / 5.0)) + ix, int(round(gy / 5.0)) + iy))
                if cells & occupied:
                    continue
                ob = bpy.data.objects.new('BLD_House_%03d' % placed, meshes[variant])
                ob.location = (gx, gy, z - 0.06)
                ob.rotation_euler = (0.0, 0.0, ang)
                collection.objects.link(ob)
                occupied |= cells
                placed += 1
                if placed >= 92:
                    return placed
    return placed


# ----------------------------------------------------------------------------
# jetty, boats
# ----------------------------------------------------------------------------

def build_jetty(site, mats, collection, xs, ys, hgrid):
    mb = MB()
    MI_DECK, MI_POST, MI_RAIL = 0, 1, 2
    mats_list = [mats['deck'], mats['timber'], mats['trim']]
    bx, by = site["jetty"]["base"]
    dx, dy = site["jetty"]["direction"]
    L_ = math.hypot(dx, dy)
    ux, uy = dx / L_, dy / L_
    length = site["jetty"]["length"]
    width = 3.2
    ang = math.atan2(uy, ux)
    # deck: planks as one slab, in short segments over depth
    seg = 2.0
    n = int(length / seg)
    for i in range(n):
        t = (i + 0.5) * seg
        cx = bx + ux * t
        cy = by + uy * t
        mb.box((cx, cy, 0.55), (seg + 0.06, width, 0.18), MI_DECK, rot_z=ang)
    # pilings
    for i in range(n + 1):
        t = i * seg
        cx = bx + ux * t
        cy = by + uy * t
        for side in (-1, 1):
            px = cx - uy * side * (width / 2 - 0.25)
            py = cy + ux * side * (width / 2 - 0.25)
            mb.box((px, py, -1.6), (0.28, 0.28, 4.4), MI_POST, rot_z=ang)
    # rails
    for side in (-1, 1):
        for i in range(0, n, 2):
            t = i * seg + seg / 2
            cx = bx + ux * t - uy * side * (width / 2 - 0.1)
            cy = by + uy * t + ux * side * (width / 2 - 0.1)
            mb.box((cx, cy, 1.15), (0.12, 0.12, 1.0), MI_RAIL, rot_z=ang)
        t0 = 1.0
        t1 = length - 1.0
        cx = bx + ux * (t0 + t1) / 2 - uy * side * (width / 2 - 0.1)
        cy = by + uy * (t0 + t1) / 2 + ux * side * (width / 2 - 0.1)
        mb.box((cx, cy, 1.62), (0.1, t1 - t0, 0.1), MI_RAIL, rot_z=ang)
    ob = mb.to_mesh('PROP_Jetty', mats_list, collection)
    return ob


def boat_mesh(name, mats, collection, length=9.5, width=2.8, cabin=True):
    """Workboat: lofted hull + gunwale + cabin + rails, one mesh."""
    mb = MB()
    MI_HULL, MI_STRIPE, MI_DECK, MI_TRIM, MI_GLASS = 0, 1, 2, 3, 4
    mats_list = [mats['hull'], mats['stripe'], mats['deck'], mats['trim'], mats['glass']]

    stations = [(-length / 2, width * 0.82, 0.0),
                (-length * 0.15, width, 0.06),
                (length * 0.22, width * 0.86, 0.10),
                (length / 2, 0.28, 0.28)]
    hull_top = 0.62
    hull_bottom = -0.75
    rings = []
    for y, w, lift in stations:
        hw = w / 2
        rings.append([
            (-hw * 0.55, y, hull_bottom + lift),
            (hw * 0.55, y, hull_bottom + lift),
            (hw, y, hull_bottom + 0.55 + lift),
            (hw, y, hull_top + lift),
            (-hw, y, hull_top + lift),
            (-hw, y, hull_bottom + 0.55 + lift),
        ])
    for a, b in zip(rings[:-1], rings[1:]):
        for i in range(6):
            j = (i + 1) % 6
            mb.quad(a[i], a[j], b[j], b[i], MI_HULL)
    # transom
    stern = rings[0]
    mb.quad(stern[0], stern[1], stern[2], stern[5], MI_HULL)
    mb.quad(stern[5], stern[2], stern[3], stern[4], MI_HULL)
    # deck: one quad strip between the two gunwale tops
    for a, b in zip(rings[:-1], rings[1:]):
        mb.quad(a[3], b[3], b[4], a[4], MI_DECK)
    # stripe along the sheer
    for a, b in zip(rings[:-1], rings[1:]):
        mb.quad(a[2], b[2], b[3], a[3], MI_STRIPE)
    if cabin:
        mb.box((0, -0.6, hull_top + 0.85), (1.9, 2.6, 1.5), MI_TRIM)
        mb.box((0, 0.75, hull_top + 0.95), (1.7, 0.12, 1.0), MI_GLASS)
        mb.box((0, -0.6, hull_top + 1.65), (2.1, 2.8, 0.16), MI_DECK)
        mb.box((0, 2.2, hull_top + 0.9), (0.16, 0.16, 1.2), MI_TRIM)
    # foredeck rails
    for side in (-1, 1):
        mb.box((side * width * 0.34, length * 0.30, hull_top + 0.35),
               (0.09, 2.4, 0.09), MI_TRIM)
    return mb.to_mesh(name, mats_list, collection)


def build_boats(site, mats, collection):
    bx, by = site["boat"]
    main = boat_mesh('PROP_SurveyBoat', mats, collection)
    main.location = (bx, by, 0.0)
    main.rotation_euler = (0, 0, math.radians(24))
    add_outline(main, 0.045)
    extra = []
    if site["kind"] == "island":
        for i, (dx, dy, rot) in enumerate([(-14, -6, 1.1), (16, 8, -0.6)]):
            ob = boat_mesh('PROP_LocalBoat_%d' % i, mats, collection,
                           length=6.4, width=1.9, cabin=False)
            ob.location = (bx + dx, by + dy, 0.0)
            ob.rotation_euler = (0, 0, rot)
            extra.append(ob)
    return main, extra


# ----------------------------------------------------------------------------
# vegetation
# ----------------------------------------------------------------------------

def palm_mesh(mats, collection):
    mb = MB()
    MI_TRUNK, MI_LEAF = 0, 1
    mats_list = [mats['trunk'], mats['leaf']]
    h = 7.0
    for i in range(6):
        t = i / 6.0
        r = 0.30 - 0.16 * t
        mb.box((0.12 * t * t, 0.0, h * (t + 0.08)), (r, r, h / 6.0 + 0.1), MI_TRUNK)
    crown = (0.12, 0.0, h * 1.05)
    for k in range(7):
        a = 2 * math.pi * k / 7 + 0.3
        ca, sa = math.cos(a), math.sin(a)
        tip = (crown[0] + ca * 3.4, crown[1] + sa * 3.4, crown[2] - 1.5)
        mid = (crown[0] + ca * 1.9, crown[1] + sa * 1.9, crown[2] + 0.2)
        left = (mid[0] - sa * 0.85, mid[1] + ca * 0.85, mid[2] - 0.25)
        right = (mid[0] + sa * 0.85, mid[1] - ca * 0.85, mid[2] - 0.25)
        mb.tri(crown, left, mid, MI_LEAF)
        mb.tri(crown, mid, right, MI_LEAF)
        mb.tri(left, tip, mid, MI_LEAF)
        mb.tri(mid, tip, right, MI_LEAF)
    return _detach(mb.to_mesh('PROP_Palm', mats_list, collection))


def bush_mesh(mats, collection):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
    me = bpy.data.meshes.new('PROP_Bush')
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mats['reef'])
    ob = bpy.data.objects.new('PROP_Bush', me)
    collection.objects.link(ob)
    bpy.data.objects.remove(ob, do_unlink=True)
    return me


def reed_mesh(mats, collection):
    mb = MB()
    for k in range(5):
        a = 2 * math.pi * k / 5
        ca, sa = math.cos(a), math.sin(a)
        w = 0.055
        mb.tri((-w * sa, w * ca, 0.0), (w * sa, -w * ca, 0.0),
               (0.14 * ca, 0.14 * sa, 1.5), 0)
    return _detach(mb.to_mesh('PROP_Reed', [mats['leaf']], collection))


def scatter_vegetation(site, mats, collection, xs, ys, hgrid):
    rng = np.random.default_rng(21)
    cfg = site["vegetation"]
    palm = palm_mesh(mats, collection)
    bush = bush_mesh(mats, collection)
    reed = reed_mesh(mats, collection)
    placed = 0

    def scatter(mesh, count, z_lo, z_hi, scale_lo, scale_hi, avoid=None):
        nonlocal placed
        made = 0
        tries = 0
        while made < count and tries < count * 40:
            tries += 1
            x = rng.uniform(-site["extent"] / 2 + 20, site["extent"] / 2 - 20)
            y = rng.uniform(-site["extent"] / 2 + 20, site["extent"] / 2 - 20)
            z = _sample_height(xs, ys, hgrid, x, y)
            if not (z_lo <= z <= z_hi):
                continue
            if avoid is not None and avoid(x, y):
                continue
            ob = bpy.data.objects.new('VEG_%04d' % placed, mesh)
            s = rng.uniform(scale_lo, scale_hi)
            ob.scale = (s, s, s * rng.uniform(0.85, 1.15))
            ob.rotation_euler = (0, 0, rng.uniform(0, 6.28))
            ob.location = (x, y, z - 0.1)
            collection.objects.link(ob)
            placed += 1
            made += 1

    # keep the settled waterfront clear
    s = site["settle"]
    def in_settle(x, y):
        return s["x0"] - 6 <= x <= s["x1"] + 6 and s["y0"] - 6 <= y <= s["y1"] + 6

    if cfg["palms"]:
        scatter(palm, cfg["palms"], 0.9, 3.2, 0.8, 1.25, avoid=in_settle)
    scatter(bush, cfg["bushes"], 0.7, 3.4, 0.7, 1.8)
    if cfg["reeds"]:
        scatter(reed, cfg["reeds"], -0.6, 1.4, 0.8, 1.5)
    return placed
