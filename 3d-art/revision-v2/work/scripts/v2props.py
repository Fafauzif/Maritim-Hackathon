"""V2 props: authored houses, landmarks, jetty, boats, vegetation and water FX.

Everything is deterministic and built for glTF survival: no render-only tricks,
all silhouette detail is real geometry, all materials are Principled constants.
"""
import math
import os
import sys

import bmesh
import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base")
for p in (HERE, BASE):
    if p not in sys.path:
        sys.path.insert(0, p)

import site_lib as L
import v2sites as S


# ---------------------------------------------------------------------------
# materials
# ---------------------------------------------------------------------------
def make_materials(palette):
    m = {}
    m["wall_a"] = L.make_material("MAT_Wall_A", palette["wall_a"], rough=0.93)
    m["wall_b"] = L.make_material("MAT_Wall_B", palette["wall_b"], rough=0.93)
    m["wall_c"] = L.make_material("MAT_Wall_C", palette["wall_c"], rough=0.93)
    m["roof_a"] = L.make_material("MAT_Roof_A", palette["roof_a"], rough=0.95)
    m["roof_b"] = L.make_material("MAT_Roof_B", palette["roof_b"], rough=0.95)
    m["roof_c"] = L.make_material("MAT_Roof_C", palette["roof_c"], rough=0.95)
    m["trim"] = L.make_material("MAT_Trim", palette["trim"], rough=0.82)
    m["glass"] = L.make_material("MAT_Window", palette["glass"], rough=0.45)
    m["timber"] = L.make_material("MAT_Timber", palette["timber"], rough=0.9)
    m["deck_a"] = L.make_material("MAT_Deck_Light", palette["deck"], rough=0.9)
    d2 = tuple(min(1.0, c * 0.78) for c in palette["deck"])
    m["deck_b"] = L.make_material("MAT_Deck_Dark", d2, rough=0.92)
    m["hull"] = L.make_material("MAT_Hull", palette["hull"], rough=0.72)
    m["stripe"] = L.make_material("MAT_HullStripe", palette["hull_stripe"], rough=0.62)
    m["leaf_a"] = L.make_material("MAT_Leaf_A", palette["leaf"], rough=0.95)
    lb = (min(1.0, palette["leaf"][0] * 1.16 + 0.03),
          min(1.0, palette["leaf"][1] * 1.12 + 0.03),
          palette["leaf"][2])
    m["leaf_b"] = L.make_material("MAT_Leaf_B", lb, rough=0.95)
    m["trunk"] = L.make_material("MAT_Trunk", palette["trunk"], rough=0.95)
    m["shrub"] = L.make_material("MAT_Shrub", palette["veg"], rough=0.96)
    sb = tuple(min(1.0, c * 1.18 + 0.02) for c in palette["veg"])
    m["shrub_b"] = L.make_material("MAT_Shrub_B", sb, rough=0.96)
    m["path"] = L.make_material("MAT_Path", tuple(c * 0.94 + 0.03 for c in palette["sand"]),
                                rough=0.97)
    m["foam"] = L.make_material("MAT_Foam", tuple(c * 0.90 for c in palette["foam"]),
                                rough=0.86)
    m["reef"] = L.make_material("MAT_Reef", palette["bed_shallow"], rough=0.95)
    reef2 = (min(1.0, palette["bed_shallow"][0] * 0.82 + 0.05),
             min(1.0, palette["bed_shallow"][1] * 0.9 + 0.04),
             min(1.0, palette["bed_shallow"][2] * 0.86))
    m["reef_b"] = L.make_material("MAT_Reef_B", reef2, rough=0.95)
    m["mangrove"] = L.make_material("MAT_Mangrove", tuple(c * 0.9 for c in palette["leaf"]),
                                    rough=0.96)
    m["ink"] = L.make_material("MAT_Ink", (0.085, 0.080, 0.075), rough=1.0)
    m["lamp"] = L.make_material("MAT_Lamp", (1.0, 0.86, 0.55), rough=0.4,
                                emission=(1.0, 0.80, 0.46), emission_strength=0.6)
    m["stone"] = L.make_material("MAT_Stone", (0.52, 0.51, 0.46), rough=0.95)
    m["metal"] = L.make_material("MAT_Metal", (0.32, 0.35, 0.36), rough=0.55, metallic=0.6)
    m["crate"] = L.make_material("MAT_Crate", (0.55, 0.42, 0.27), rough=0.9)
    m["net"] = L.make_material("MAT_Net", (0.30, 0.42, 0.38), rough=0.95)
    return m


# ---------------------------------------------------------------------------
# local mesh builder with named material slots
# ---------------------------------------------------------------------------
class B:
    """Tiny local builder: verts/faces/material-name per face, resolved at end."""

    def __init__(self):
        self.v = []
        self.f = []
        self.m = []

    def quad(self, a, b, c, d, mat):
        n = len(self.v)
        self.v.extend([a, b, c, d])
        self.f.append((n, n + 1, n + 2, n + 3))
        self.m.append(mat)

    def tri(self, a, b, c, mat):
        n = len(self.v)
        self.v.extend([a, b, c])
        self.f.append((n, n + 1, n + 2))
        self.m.append(mat)

    def box(self, center, size, mat, rz=0.0):
        cx, cy, cz = center
        hx, hy, hz = size[0] / 2.0, size[1] / 2.0, size[2] / 2.0
        pts = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
               (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]
        ca, sa = math.cos(rz), math.sin(rz)
        w = [(cx + x * ca - y * sa, cy + x * sa + y * ca, cz + z) for x, y, z in pts]
        n = len(self.v)
        self.v.extend(w)
        for face in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                     (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            self.f.append(tuple(n + i for i in face))
            self.m.append(mat)

    def prism_z(self, pts2d, z0, z1, mat):
        n = len(pts2d)
        for (x, y) in pts2d:
            self.v.append((x, y, z0))
        for (x, y) in pts2d:
            self.v.append((x, y, z1))
        for i in range(n):
            j = (i + 1) % n
            self.f.append((i, j, j + n, i + n))
            self.m.append(mat)
        self.f.append(tuple(range(n - 1, -1, -1)))
        self.m.append(mat)
        self.f.append(tuple(range(n, 2 * n)))
        self.m.append(mat)

    def finish(self, name, mats, collection, recalc=True):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.v, [], self.f)
        me.update()
        slots = []
        for mat_name in self.m:
            if mat_name not in slots:
                slots.append(mat_name)
        for mat_name in slots:
            me.materials.append(mats[mat_name])
        me.polygons.foreach_set("material_index", [slots.index(x) for x in self.m])
        if recalc:
            bm = bmesh.new()
            bm.from_mesh(me)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            bm.to_mesh(me)
            bm.free()
        me.validate()
        ob = bpy.data.objects.new(name, me)
        collection.objects.link(ob)
        return ob


def _mesh_object(name, me, collection, location=(0, 0, 0), rotation=0.0):
    ob = bpy.data.objects.new(name, me)
    ob.location = location
    ob.rotation_euler = (0.0, 0.0, rotation)
    collection.objects.link(ob)
    return ob


# ---------------------------------------------------------------------------
# houses
# ---------------------------------------------------------------------------
HOUSE_VARIANTS = [
    # key, w, d, wall_h, roof_h, roof, wall, roof_mat, stilt, porch, storeys
    ("A", 6.4, 5.2, 2.75, 1.55, "gable", "wall_a", "roof_a", 0.0, True, 1),
    ("B", 9.8, 5.4, 2.95, 1.65, "hip", "wall_b", "roof_b", 0.0, False, 1),
    ("C", 5.4, 5.4, 2.60, 1.15, "flat", "wall_c", "roof_c", 0.0, True, 1),
    ("D", 8.0, 6.0, 3.05, 1.85, "gable", "wall_b", "roof_a", 0.0, True, 2),
    ("E", 6.0, 5.0, 2.70, 1.45, "hip", "wall_a", "roof_c", 0.75, False, 1),
    ("F", 10.2, 6.2, 3.10, 1.75, "hip", "wall_c", "roof_a", 0.0, False, 2),
    ("G", 5.8, 4.8, 2.55, 1.30, "gable", "wall_a", "roof_b", 0.0, True, 1),
    ("H", 7.2, 5.6, 2.85, 1.50, "gable", "wall_b", "roof_c", 0.0, False, 1),
]


def house_mesh(name, mats, w, d, wall_h, roof_h, roof, wall_mat, roof_mat,
               stilt=0.0, porch=True, storeys=1):
    """Detailed authored house in local space, origin at footprint centre ground."""
    b = B()
    timber, trim, glass, deck = "timber", "trim", "glass", "deck_a"
    z0 = stilt
    plinth = 0.18
    # foundation / plinth
    if stilt > 0.0:
        n_posts = 4
        for sx in (-1, 1):
            for sy in (-1, 1):
                b.box((sx * (w / 2 - 0.45), sy * (d / 2 - 0.45), stilt / 2),
                      (0.28, 0.28, stilt), timber)
        # cross braces
        b.box((0, -d / 2 + 0.45, stilt * 0.45), (w - 1.0, 0.14, 0.14), timber)
        b.box((0, d / 2 - 0.45, stilt * 0.45), (w - 1.0, 0.14, 0.14), timber)
        b.box((0, 0, stilt - 0.10), (w + 0.30, d + 0.30, 0.18), deck)
        b.box((0, 0, stilt - 0.02), (w + 0.05, d + 0.05, 0.05), timber)
    else:
        b.box((0, 0, plinth / 2), (w + 0.24, d + 0.24, plinth), "stone")
        b.box((0, 0, plinth + 0.02), (w + 0.06, d + 0.06, 0.05), timber)

    body_z = z0 + plinth
    wall_top = body_z + wall_h * storeys
    b.box((0, 0, (body_z + wall_top) / 2), (w, d, wall_h * storeys), wall_mat)
    # corner trim posts and top fascia
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((sx * (w / 2 - 0.09), sy * (d / 2 - 0.09), (body_z + wall_top) / 2),
                  (0.18, 0.18, wall_h * storeys), trim)
    b.box((0, 0, wall_top - 0.09), (w + 0.10, d + 0.10, 0.18), trim)

    # door on the -Y facade with frame and step
    b.box((0, -d / 2 - 0.025, body_z + 1.03), (1.06, 0.10, 2.02), timber)
    b.box((0, -d / 2 - 0.075, body_z + 2.06), (1.30, 0.06, 0.16), trim)
    b.box((-0.62, -d / 2 - 0.075, body_z + 1.03), (0.10, 0.06, 2.10), trim)
    b.box((0.62, -d / 2 - 0.075, body_z + 1.03), (0.10, 0.06, 2.10), trim)
    b.box((0, -d / 2 - 0.42, body_z - 0.08), (1.3, 0.7, 0.22), "stone")

    # windows, frames and shutters on both long faces
    win_y = body_z + wall_h * 0.60
    for sx in (-1, 1):
        b.box((sx * w * 0.29, -d / 2 - 0.03, win_y), (1.10, 0.07, 0.92), glass)
        b.box((sx * w * 0.29, -d / 2 - 0.07, win_y + 0.50), (1.30, 0.05, 0.10), trim)
        b.box((sx * w * 0.29, -d / 2 - 0.07, win_y - 0.50), (1.30, 0.05, 0.10), trim)
        b.box((sx * w * 0.29 - 0.60, -d / 2 - 0.07, win_y), (0.10, 0.05, 1.04), trim)
        b.box((sx * w * 0.29 + 0.60, -d / 2 - 0.07, win_y), (0.10, 0.05, 1.04), trim)
        # shutters (one side open)
        b.box((sx * w * 0.29 - 0.88, -d / 2 - 0.12, win_y), (0.34, 0.05, 0.96),
              wall_mat, rz=0.0)
    # greenery side openings
    for sy in (-1, 1):
        b.box((-w / 2 - 0.03, sy * d * 0.20, win_y), (0.07, 1.00, 0.86), glass)
        b.box((-w / 2 - 0.07, sy * d * 0.20, win_y + 0.47), (0.05, 1.20, 0.10), trim)
        b.box((-w / 2 - 0.07, sy * d * 0.20, win_y - 0.47), (0.05, 1.20, 0.10), trim)

    if storeys >= 2:
        b.box((0, 0, body_z + wall_h), (w + 0.16, d + 0.16, 0.16), trim)
        b.box((0, -d / 2 - 0.16, body_z + wall_h + 0.95), (w * 0.62, 0.10, 0.86), glass)
        b.box((0, -d / 2 - 0.22, body_z + wall_h + 0.50), (w * 0.62 + 0.30, 0.16, 0.10), trim)
        b.box((0, -d / 2 - 0.22, body_z + wall_h + 1.40), (w * 0.62 + 0.30, 0.16, 0.10), trim)
        for sx in (-1, 1):
            b.box((sx * (w * 0.31 + 0.15), -d / 2 - 0.22, body_z + wall_h + 0.95),
                  (0.12, 0.12, 1.0), trim)

    # porch
    if porch:
        pw = min(w * 0.72, 4.6)
        pd = 1.55
        pz = body_z
        b.box((0, -d / 2 - pd / 2, pz - 0.10), (pw, pd, 0.20), deck)
        for sx in (-1, 1):
            b.box((sx * (pw / 2 - 0.14), -d / 2 - pd + 0.14, pz + 1.02),
                  (0.16, 0.16, 2.05), timber)
        b.box((0, -d / 2 - pd - 0.02, pz + 2.10), (pw + 0.24, 0.16, 0.14), timber)
        # shed porch roof
        b.quad((-pw / 2 - 0.22, -d / 2 - pd - 0.15, pz + 2.16),
               (pw / 2 + 0.22, -d / 2 - pd - 0.15, pz + 2.16),
               (pw / 2 + 0.22, -d / 2 + 0.05, pz + 2.55),
               (-pw / 2 - 0.22, -d / 2 + 0.05, pz + 2.55), roof_mat)
        b.box((0, -d / 2 - pd - 0.16, pz + 2.16), (pw + 0.46, 0.10, 0.10), trim)
        # steps from ground to porch
        b.box((0, -d / 2 - pd - 0.28, pz - 0.34), (1.4, 0.55, 0.24), "stone")
        b.box((0, -d / 2 - pd - 0.52, pz - 0.58), (1.4, 0.45, 0.22), "stone")

    # roof
    top = wall_top
    ov = 0.52
    if roof == "flat":
        b.box((0, 0, top + 0.16), (w + 0.44, d + 0.44, 0.30), roof_mat)
        # parapet
        for sx in (-1, 1):
            b.box((sx * (w / 2 + 0.16), 0, top + 0.50), (0.16, d + 0.44, 0.62), roof_mat)
        for sy in (-1, 1):
            b.box((0, sy * (d / 2 + 0.16), top + 0.50), (w + 0.12, 0.16, 0.62), roof_mat)
        b.box((0, -d / 2 - 0.05, top + 0.16), (w + 0.44, 0.12, 0.10), trim)
        # roof vent + tank
        b.box((w * 0.24, d * 0.08, top + 0.62), (0.55, 0.55, 0.55), "metal")
        b.box((0.55, 0.55, top + 0.42), (0.7, 0.7, 0.85), "metal")
    elif roof == "hip":
        hw, hd = w / 2 + ov, d / 2 + ov
        r = w * 0.24
        r0 = (-r, 0, top + roof_h)
        r1 = (r, 0, top + roof_h)
        e = [(-hw, -hd, top), (hw, -hd, top), (hw, hd, top), (-hw, hd, top)]
        b.quad(e[0], e[1], r1, r0, roof_mat)
        b.quad(e[2], e[3], r0, r1, roof_mat)
        b.tri(e[1], e[2], r1, roof_mat)
        b.tri(e[3], e[0], r0, roof_mat)
        # ridge + eave fascia
        b.box((0, 0, top + roof_h - 0.02), (2 * r + 0.22, 0.16, 0.13), trim)
        for sx in (-1, 1):
            b.box((sx * hw, 0, top - 0.02), (0.10, 2 * hd + 0.12, 0.10), trim)
        b.box((0, -hd, top - 0.02), (2 * hw + 0.10, 0.10, 0.10), trim)
        b.box((0, hd, top - 0.02), (2 * hw + 0.10, 0.10, 0.10), trim)
    elif roof == "pyramid":
        hw, hd = w / 2 + ov, d / 2 + ov
        apex = (0, 0, top + roof_h)
        e = [(-hw, -hd, top), (hw, -hd, top), (hw, hd, top), (-hw, hd, top)]
        for i in range(4):
            b.tri(e[i], e[(i + 1) % 4], apex, roof_mat)
    else:  # gable, ridge along X
        hw, hd = w / 2 + ov, d / 2 + ov
        ridge = top + roof_h
        b.quad((-hw, -hd, top), (hw, -hd, top), (hw, 0, ridge), (-hw, 0, ridge), roof_mat)
        b.quad((hw, hd, top), (-hw, hd, top), (-hw, 0, ridge), (hw, 0, ridge), roof_mat)
        # gable end triangles in wall tone
        b.tri((-hw, -hd, top), (-hw, 0, ridge), (-hw, hd, top), wall_mat)
        b.tri((hw, hd, top), (hw, 0, ridge), (hw, -hd, top), wall_mat)
        b.box((0, 0, ridge - 0.02), (2 * hw + 0.10, 0.16, 0.13), trim)
        b.box((0, -hd, top - 0.02), (2 * hw + 0.10, 0.10, 0.10), trim)
        b.box((0, hd, top - 0.02), (2 * hw + 0.10, 0.10, 0.10), trim)
        # small roof vent
        b.box((w * 0.18, 0, top + roof_h * 0.55), (0.42, 0.42, 0.55), roof_mat)
        b.box((w * 0.18, 0, top + roof_h * 0.55 + 0.34), (0.56, 0.56, 0.10), trim)
    return b


def build_house_object(name, mats, variant, collection, location, rotation,
                       stilt=None):
    key, w, d, wall_h, roof_h, roof, wall_mat, roof_mat, vs, porch, storeys = variant
    if stilt is None:
        stilt = vs
    b = house_mesh(name, mats, w, d, wall_h, roof_h, roof, wall_mat, roof_mat,
                   stilt=stilt, porch=porch, storeys=storeys)
    return _place(b, name, mats, collection, location, rotation)


def _place(builder, name, mats, collection, location, rotation, z=None):
    ob = builder.finish(name, mats, collection)
    ob.location = (location[0], location[1], location[2] if z is None else z)
    ob.rotation_euler = (0.0, 0.0, rotation)
    return ob


def house_footprint(variant, rot, stilt=0.0):
    key, w, d, wall_h, roof_h, roof, wall_mat, roof_mat, vs, porch, storeys = variant
    span_x, span_y = w, d
    c, s = math.cos(rot), math.sin(rot)
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        lx, ly = sx * (span_x / 2 + 0.3), sy * (span_y / 2 + 0.3)
        pts.append((lx * c - ly * s, lx * s + ly * c))
    return pts


# ---------------------------------------------------------------------------
# landmarks
# ---------------------------------------------------------------------------
def pavilion_mesh(mats, collection, name="BLD_LandingPavilion", w=10.5, d=7.5,
                  platform=0.85, height=3.0):
    b = B()
    # platform on piles
    b.box((0, 0, platform - 0.10), (w, d, 0.22), "deck_a")
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((sx * (w / 2 - 0.45), sy * (d / 2 - 0.45), platform / 2),
                  (0.30, 0.30, platform), "timber")
    for i in range(-2, 3):
        b.box((0, i * d / 5.0, platform * 0.45), (w - 0.9, 0.16, 0.16), "timber")
    # corner posts
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((sx * (w / 2 - 0.35), sy * (d / 2 - 0.35), platform + height / 2),
                  (0.26, 0.26, height), "timber")
    # back wall (shelter)
    b.box((0, d / 2 - 0.15, platform + height * 0.48), (w - 0.8, 0.16, height * 0.96), "wall_b")
    # bench + counter
    b.box((0, d * 0.24, platform + 0.42), (w - 2.2, 0.55, 0.18), "deck_b")
    b.box((0, d * 0.24, platform + 0.24), (w - 2.8, 0.24, 0.35), "timber")
    # hipped roof
    top = platform + height
    hw, hd = w / 2 + 0.9, d / 2 + 0.9
    r = 1.2
    r0, r1 = (-r, 0, top + 1.7), (r, 0, top + 1.7)
    e = [(-hw, -hd, top), (hw, -hd, top), (hw, hd, top), (-hw, hd, top)]
    b.quad(e[0], e[1], r1, r0, "roof_a")
    b.quad(e[2], e[3], r0, r1, "roof_a")
    b.tri(e[1], e[2], r1, "roof_a")
    b.tri(e[3], e[0], r0, "roof_a")
    b.box((0, 0, top + 1.66), (2 * r + 0.2, 0.16, 0.14), "trim")
    for sx in (-1, 1):
        b.box((sx * hw, 0, top - 0.03), (0.10, 2 * hd, 0.12), "trim")
    b.box((0, -hd, top - 0.03), (2 * hw, 0.10, 0.12), "trim")
    b.box((0, hd, top - 0.03), (2 * hw, 0.10, 0.12), "trim")
    # steps on the water side
    for i in range(3):
        b.box((0, -d / 2 - 0.45 - i * 0.55, platform - 0.15 - i * 0.22),
              (2.6 - i * 0.2, 0.58, 0.20), "stone")
    # railing around platform edge (three sides)
    for sx in (-1, 1):
        b.box((sx * (w / 2 - 0.08), -d * 0.10, platform + 0.55),
              (0.09, d * 0.8, 0.09), "trim")
        for sy in (-1, 0, 1):
            b.box((sx * (w / 2 - 0.08), sy * d * 0.34, platform + 0.30),
                  (0.09, 0.09, 0.62), "trim")
    # crates and a barrel beside the shelter
    b.box((-w / 2 - 0.8, -1.2, 0.35), (0.9, 0.9, 0.7), "crate")
    b.box((-w / 2 - 0.7, -0.2, 0.28), (0.65, 0.65, 0.56), "crate")
    return b.finish(name, mats, collection)


def working_landing_mesh(mats, collection, name="BLD_WorkingLanding", w=9.0):
    """Amur working landing: deck, gantry frame, boathouse and stores."""
    b = B()
    # timber deck
    b.box((0, 0, 0.55), (w, 7.0, 0.24), "deck_a")
    for i in range(5):
        b.box((-w / 2 + i * w / 4.0, 0, 0.42), (0.18, 7.0, 0.12), "deck_b")
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((sx * (w / 2 - 0.6), sy * 2.8, -0.6), (0.32, 0.32, 2.2), "timber")
    # gantry / crane frame over the water side
    for sx in (-1, 1):
        b.box((sx * 2.2, -5.6, 2.5), (0.24, 0.24, 4.2), "metal")
    b.box((0, -5.6, 4.65), (4.8, 0.28, 0.30), "metal")
    b.box((0, -5.0, 4.10), (0.10, 0.10, 1.0), "metal")
    b.box((0, -5.0, 3.65), (0.55, 0.55, 0.35), "metal")
    # boathouse on shore side
    b.box((0.6, 2.2, 1.75), (5.2, 3.4, 2.4), "wall_b")
    b.box((0.6, 0.45, 1.25), (2.6, 0.10, 2.3), "timber")
    b.box((0.6, 2.2, 2.98), (6.0, 4.2, 0.26), "roof_b")
    b.box((0.6, 2.2, 3.12), (6.2, 0.18, 0.14), "trim")
    # stores / crates / barrels
    for i, (x, y, s) in enumerate(((-4.0, 1.2, 0.9), (-4.2, 2.4, 0.75), (-3.5, 3.2, 0.6))):
        b.box((x, y, 0.4 + s / 2 - 0.2), (s, s, s), "crate")
    b.box((4.0, 2.6, 0.42), (0.7, 0.7, 0.84), "metal")
    b.box((4.1, 1.4, 0.36), (0.65, 0.65, 0.72), "net")
    return b.finish(name, mats, collection)


def community_hall_mesh(mats, collection, name="BLD_CommunityHall", w=13.0, d=8.0):
    b = B()
    b.box((0, 0, 0.22), (w + 0.4, d + 0.4, 0.34), "stone")
    b.box((0, 0, 1.7), (w, d, 3.0), "wall_a")
    b.box((0, 0, 3.25), (w + 0.4, d + 0.4, 0.24), "trim")
    # long windows
    for i in range(4):
        b.box((-w * 0.36 + i * w * 0.24, -d / 2 - 0.04, 2.0), (1.15, 0.08, 1.05), "glass")
        b.box((-w * 0.36 + i * w * 0.24, -d / 2 - 0.08, 2.58), (1.35, 0.05, 0.10), "trim")
        b.box((-w * 0.36 + i * w * 0.24, -d / 2 - 0.08, 1.42), (1.35, 0.05, 0.10), "trim")
    # double door
    b.box((0, -d / 2 - 0.05, 1.35), (2.4, 0.10, 2.6), "timber")
    b.box((0, -d / 2 - 0.10, 2.72), (2.8, 0.08, 0.18), "trim")
    # hip roof
    top = 3.37
    hw, hd = w / 2 + 1.0, d / 2 + 1.0
    r0, r1 = (-2.0, 0, top + 2.0), (2.0, 0, top + 2.0)
    e = [(-hw, -hd, top), (hw, -hd, top), (hw, hd, top), (-hw, hd, top)]
    b.quad(e[0], e[1], r1, r0, "roof_c")
    b.quad(e[2], e[3], r0, r1, "roof_c")
    b.tri(e[1], e[2], r1, "roof_c")
    b.tri(e[3], e[0], r0, "roof_c")
    b.box((0, 0, top + 1.96), (4.2, 0.18, 0.16), "trim")
    return b.finish(name, mats, collection)


# ---------------------------------------------------------------------------
# jetty
# ---------------------------------------------------------------------------
def build_jetty_v2(site, mats, collection, name="PROP_Jetty"):
    j = site["jetty"]
    (bx, by), (dx, dy), length, width = j["base"], j["direction"], j["length"], j["width"]
    Ln = math.hypot(dx, dy)
    ux, uy = dx / Ln, dy / Ln
    ang = math.atan2(uy, ux)
    deck_z = j["deck_z"]
    # find the actual shoreline near the requested base
    shore = S.find_shore_point(site, (bx, by), (ux, uy), max_r=30.0,
                               z_lo=0.15, z_hi=0.9) or (bx, by, 0.4)
    bx, by = shore[0], shore[1]
    b = B()
    seg = 2.15
    n = int(length / seg)
    # stringers
    for side in (-1, 1):
        cx = bx + ux * length / 2 - uy * side * (width / 2 - 0.22)
        cy = by + uy * length / 2 + ux * side * (width / 2 - 0.22)
        b.box((cx, cy, deck_z - 0.20), (length, 0.28, 0.26), "timber", rz=ang)
    # cross beams + planks
    for i in range(n):
        t = (i + 0.5) * seg
        cx, cy = bx + ux * t, by + uy * t
        b.box((cx, cy, deck_z - 0.07), (seg + 0.05, width, 0.13),
              "deck_a" if i % 2 == 0 else "deck_b", rz=ang)
        b.box((cx, cy, deck_z - 0.22), (0.20, width + 0.15, 0.14), "timber", rz=ang)
    # ramp / steps at the root: connect terrain to deck
    ground = S.height_at(site, bx - ux * 2.2, by - uy * 2.2)
    rise = deck_z - ground
    steps = max(2, int(abs(rise) / 0.22))
    for k in range(steps):
        t = -1.8 - k * 0.55
        z = ground + rise * (k + 1) / (steps + 1)
        cx, cy = bx + ux * t, by + uy * t
        b.box((cx, cy, z - 0.10), (1.1, width * 0.82, 0.20), "stone", rz=ang)
    # pilings, computed down to the actual bed
    for i in range(n + 1):
        t = i * seg
        cx, cy = bx + ux * t, by + uy * t
        for side in (-1, 1):
            px = cx - uy * side * (width / 2 - 0.28)
            py = cy + ux * side * (width / 2 - 0.28)
            bed = S.height_at(site, px, py)
            top = deck_z - 0.18
            bottom = min(bed - 0.6, top - 1.2)
            hh = top - bottom
            b.box((px, py, (top + bottom) / 2), (0.30, 0.30, hh), "timber", rz=ang)
            # cross-brace to its pair
            if i < n:
                nx = bx + ux * ((i + 1) * seg) - uy * side * (width / 2 - 0.28)
                ny = by + uy * ((i + 1) * seg) + ux * side * (width / 2 - 0.28)
                b.box(((px + nx) / 2, (py + ny) / 2, deck_z - 0.85),
                      (seg, 0.12, 0.12), "timber", rz=ang)
    # rails run ALONG the pier on both sides
    rail_z = deck_z + 0.96
    for side in (-1, 1):
        ox = -uy * side * (width / 2 - 0.12)
        oy = ux * side * (width / 2 - 0.12)
        t0, t1 = 1.0, length - 0.8
        cx = bx + ux * (t0 + t1) / 2 + ox
        cy = by + uy * (t0 + t1) / 2 + oy
        b.box((cx, cy, rail_z), (t1 - t0, 0.10, 0.10), "trim", rz=ang)
        b.box((cx, cy, rail_z - 0.42), (t1 - t0, 0.08, 0.08), "trim", rz=ang)
        for i in range(0, n, 2):
            t = i * seg + 0.5
            px = bx + ux * t + ox
            py = by + uy * t + oy
            b.box((px, py, deck_z + 0.52), (0.10, 0.10, 1.02), "trim", rz=ang)
    # bollards
    for t in (3.0, length * 0.55, length - 3.0):
        px = bx + ux * t - uy * (width / 2 - 0.55)
        py = by + uy * t + ux * (width / 2 - 0.55)
        b.box((px, py, deck_z + 0.22), (0.24, 0.24, 0.55), "metal")
    # lamp posts at root and end
    for t in (1.6, length - 2.0):
        px = bx + ux * t - uy * (width / 2 - 0.28)
        py = by + uy * t + ux * (width / 2 - 0.28)
        b.box((px, py, deck_z + 1.85), (0.10, 0.10, 3.1), "timber")
        b.box((px, py, deck_z + 3.45), (0.36, 0.36, 0.28), "lamp")
    ob = b.finish(name, mats, collection)
    ob["base"] = [round(bx, 4), round(by, 4), round(float(shore[2]), 4)]
    ob["direction"] = [round(ux, 5), round(uy, 5)]
    ob["length_m"] = float(length)
    ob["width_m"] = float(width)
    ob["deck_z"] = float(deck_z)
    ob["end"] = [round(bx + ux * length, 4), round(by + uy * length, 4), float(deck_z)]
    return ob


# ---------------------------------------------------------------------------
# boats
# ---------------------------------------------------------------------------
def _hull_rings(length, width, depth, sheer, bow_lift=0.28):
    stations = [
        (-length / 2, width * 0.86, 0.0, sheer - 0.06),
        (-length * 0.24, width, 0.0, sheer),
        (0.0, width, 0.02, sheer + 0.04),
        (length * 0.26, width * 0.88, 0.06, sheer + 0.10),
        (length * 0.44, width * 0.62, 0.16, sheer + 0.22),
        (length / 2, 0.10, bow_lift, sheer + 0.40),
    ]
    return stations


def boat_mesh_v2(mats, collection, name, length=10.6, width=3.0, cabin=True,
                 draft=0.95, survey=True):
    b = B()
    sheer = 0.72
    rings = []
    for y, w, lift, top in _hull_rings(length, width, draft, sheer):
        hw = w / 2.0
        rings.append([
            (-hw * 0.42, y, lift - draft),
            (hw * 0.42, y, lift - draft),
            (hw, y, lift - draft + 0.55),
            (hw, y, top),
            (-hw, y, top),
            (-hw, y, lift - draft + 0.55),
        ])
    for a, c in zip(rings[:-1], rings[1:]):
        for i in range(6):
            j = (i + 1) % 6
            b.quad(a[i], a[j], c[j], c[i], "hull")
    # transom
    st = rings[0]
    b.quad(st[0], st[1], st[2], st[5], "hull")
    b.quad(st[5], st[2], st[3], st[4], "hull")
    # deck
    for a, c in zip(rings[:-1], rings[1:]):
        b.quad(a[3], c[3], c[4], a[4], "deck_a")
    # sheer stripe + gunwale cap
    for a, c in zip(rings[:-1], rings[1:]):
        b.quad(a[2], c[2], c[3], a[3], "stripe")
        b.quad(a[3], c[3], c[4], a[4], "trim")
    # keel strip
    for a, c in zip(rings[:-1], rings[1:]):
        b.quad(a[0], c[0], c[1], a[1], "hull")
    if cabin:
        b.box((0, -length * 0.06, sheer + 0.72), (width * 0.66, length * 0.27, 1.42), "trim")
        b.box((0, -length * 0.06, sheer + 1.44), (width * 0.70, length * 0.30, 0.14), "deck_a")
        # cabin windows
        for sx in (-1, 1):
            for i in (-1, 1):
                b.box((sx * (width * 0.34 + 0.01), -length * 0.06 + i * 0.55,
                       sheer + 0.92), (0.06, 0.62, 0.44), "glass")
        b.box((0, -length * 0.06 - length * 0.145, sheer + 0.96),
              (width * 0.46, 0.07, 0.48), "glass")
        b.box((0, -length * 0.06, sheer + 1.52), (width * 0.46, length * 0.20, 0.10),
              "trim")
        # mast, radar dome, antennas
        b.box((0, length * 0.16, sheer + 1.62), (0.12, 0.12, 1.4), "metal")
        b.box((0, length * 0.16, sheer + 2.30), (0.42, 0.42, 0.18), "metal")
        b.box((0, length * 0.16, sheer + 2.52), (0.14, 0.14, 0.34), "trim")
        b.box((0, length * 0.26, sheer + 2.05), (0.05, 0.05, 1.0), "metal")
        # railings
        for sx in (-1, 1):
            b.box((sx * width * 0.43, length * 0.26, sheer + 0.92),
                  (0.08, length * 0.44, 0.08), "trim")
            b.box((sx * width * 0.43, length * 0.26, sheer + 0.52),
                  (0.08, length * 0.44, 0.08), "trim")
            for i in (-1, 0, 1):
                b.box((sx * width * 0.43, length * 0.26 + i * length * 0.16,
                       sheer + 0.68), (0.08, 0.08, 0.72), "trim")
        # sampling winch at stern
        b.box((0, -length * 0.38, sheer + 0.55), (1.5, 0.9, 0.30), "metal")
        b.box((0, -length * 0.38, sheer + 0.90), (0.55, 0.55, 0.42), "metal")
        b.box((0, -length * 0.38, sheer + 1.20), (0.10, 1.5, 0.10), "metal")
        # fenders
        for i in (-1, 1):
            b.box((i * width * 0.52, -length * 0.16, sheer - 0.20),
                  (0.18, 0.32, 0.62), "net")
    else:
        # simple canopy
        if survey is False:
            b.box((0, -length * 0.04, sheer + 0.58), (width * 0.66, length * 0.26, 0.50), "trim")
            for sx in (-1, 1):
                for i in (-1, 1):
                    b.box((sx * width * 0.30, -length * 0.04 + i * length * 0.10,
                           sheer + 0.30), (0.08, 0.08, 0.60), "timber")
            b.box((0, -length * 0.04, sheer + 0.88), (width * 0.74, length * 0.30, 0.10),
                  "roof_c")
    return b.finish(name, mats, collection)


def outrigger_mesh_v2(mats, collection, name, length=6.2, width=1.35):
    b = B()
    sheer = 0.46
    rings = []
    for y, w, lift, top in _hull_rings(length, width, 0.55, sheer, bow_lift=0.22):
        hw = w / 2.0
        rings.append([(-hw * 0.35, y, lift - 0.55), (hw * 0.35, y, lift - 0.55),
                      (hw, y, lift - 0.12), (hw, y, top), (-hw, y, top),
                      (-hw, y, lift - 0.12)])
    for a, c in zip(rings[:-1], rings[1:]):
        for i in range(6):
            j = (i + 1) % 6
            b.quad(a[i], a[j], c[j], c[i], "hull")
    st = rings[0]
    b.quad(st[0], st[1], st[2], st[5], "hull")
    b.quad(st[5], st[2], st[3], st[4], "hull")
    for a, c in zip(rings[:-1], rings[1:]):
        b.quad(a[3], c[3], c[4], a[4], "deck_a")
        b.quad(a[2], c[2], c[3], a[3], "stripe")
    # outrigger floats and booms
    for side in (-1, 1):
        fy = side * (width / 2 + 1.35)
        for i in (-1, 0, 1):
            b.box((0, i * length * 0.18, sheer + 0.02), (2.9, 0.12, 0.12), "timber")
        b.box((0, fy, 0.0), (0.42, length * 0.55, 0.34), "hull")
        b.box((0, fy, 0.02), (0.34, length * 0.40, 0.20), "stripe")
    # little canopy
    b.box((0, -length * 0.05, sheer + 0.55), (width * 0.72, length * 0.24, 0.42), "trim")
    for sx in (-1, 1):
        b.box((sx * width * 0.28, -length * 0.05, sheer + 0.26), (0.07, 0.07, 0.50), "timber")
    return b.finish(name, mats, collection)


# ---------------------------------------------------------------------------
# vegetation
# ---------------------------------------------------------------------------
def palm_mesh_v2(mats, collection, name="VEG_PalmMesh", height=7.6):
    b = B()
    segs = 7
    for i in range(segs):
        t0, t1 = i / segs, (i + 1) / segs
        r0 = 0.34 * (1.0 - 0.55 * t0)
        r1 = 0.34 * (1.0 - 0.55 * t1)
        cx0 = 0.55 * t0 * t0
        cx1 = 0.55 * t1 * t1
        z0, z1 = height * t0, height * t1
        pts0 = [(cx0 + math.cos(a) * r0, math.sin(a) * r0, z0)
                for a in np.linspace(0, 2 * math.pi, 7)[:-1]]
        pts1 = [(cx1 + math.cos(a) * r1, math.sin(a) * r1, z1)
                for a in np.linspace(0, 2 * math.pi, 7)[:-1]]
        for k in range(6):
            b.quad(pts0[k], pts0[(k + 1) % 6], pts1[(k + 1) % 6], pts1[k], "trunk")
    crown = (0.55, 0.0, height)
    for k in range(9):
        a = 2 * math.pi * k / 9 + 0.2
        ca, sa = math.cos(a), math.sin(a)
        # two-segment drooping frond
        p0 = crown
        p1 = (crown[0] + ca * 1.5, crown[1] + sa * 1.5, crown[2] + 0.35)
        p2 = (crown[0] + ca * 3.2, crown[1] + sa * 3.2, crown[2] - 0.35)
        p3 = (crown[0] + ca * 4.1, crown[1] + sa * 4.1, crown[2] - 1.15)
        l1 = (crown[0] + ca * 1.6 + sa * 0.55, crown[1] + sa * 1.6 - ca * 0.55,
              crown[2] + 0.05)
        r1 = (crown[0] + ca * 1.6 - sa * 0.55, crown[1] + sa * 1.6 + ca * 0.55,
              crown[2] + 0.05)
        l2 = (crown[0] + ca * 3.1 + sa * 0.40, crown[1] + sa * 3.1 - ca * 0.40,
              crown[2] - 0.65)
        r2 = (crown[0] + ca * 3.1 - sa * 0.40, crown[1] + sa * 3.1 + ca * 0.40,
              crown[2] - 0.65)
        b.quad(p0, l1, p2, p1, "leaf_a")
        b.quad(p0, p1, p2, r1, "leaf_b")
        b.quad(p1, l2, p3, p2, "leaf_b")
        b.quad(p1, p2, p3, r2, "leaf_a")
    # coconuts
    for k in range(4):
        a = 2 * math.pi * k / 4
        b.box((crown[0] + 0.32 * math.cos(a), crown[1] + 0.32 * math.sin(a),
               crown[2] - 0.22), (0.22, 0.22, 0.22), "trunk")
    return b.finish(name, mats, collection)


def shrub_mesh_v2(mats, collection, name="VEG_ShrubMesh", variant=0):
    b = B()
    # three lumpy rounded masses
    blobs = [((0, 0, 0.55), (0.85, 0.85, 0.72)),
             ((0.55, 0.20, 0.42), (0.62, 0.58, 0.52)),
             ((-0.48, -0.25, 0.40), (0.55, 0.52, 0.48))]
    for (cx, cy, cz), (rx, ry, rz) in blobs:
        seg, rings = 8, 5
        verts = []
        for j in range(1, rings):
            phi = math.pi * j / rings
            for i in range(seg):
                th = 2 * math.pi * i / seg
                verts.append((cx + rx * math.sin(phi) * math.cos(th),
                              cy + ry * math.sin(phi) * math.sin(th),
                              cz + rz * math.cos(phi)))
        top = len(verts)
        verts.append((cx, cy, cz + rz))
        bot = len(verts)
        verts.append((cx, cy, cz - rz * 0.6))
        start = len(b.v)
        b.v.extend(verts)
        for j in range(rings - 2):
            for i in range(seg):
                a = start + j * seg + i
                c = start + j * seg + (i + 1) % seg
                d = start + (j + 1) * seg + i
                e = start + (j + 1) * seg + (i + 1) % seg
                b.f.append((a, c, e, d))
                b.m.append("shrub" if variant == 0 else "shrub_b")
        for i in range(seg):
            a = start + (rings - 2) * seg + i
            c = start + (rings - 2) * seg + (i + 1) % seg
            b.f.append((a, c, top))
            b.m.append("shrub" if variant == 0 else "shrub_b")
            d = start + i
            e = start + (i + 1) % seg
            b.f.append((d, bot, e))
            b.m.append("shrub" if variant == 0 else "shrub_b")
    return b.finish(name, mats, collection)


def reed_mesh_v2(mats, collection, name="VEG_ReedMesh"):
    b = B()
    for k in range(11):
        a = 2 * math.pi * k / 11 + 0.3
        rad = 0.10 + 0.16 * (k % 3) / 2.0
        cx, cy = math.cos(a) * rad, math.sin(a) * rad
        h = 1.25 + 0.55 * ((k * 37) % 11) / 10.0
        lean = 0.16 + 0.10 * ((k * 13) % 5) / 4.0
        w = 0.045
        px, py = -math.sin(a), math.cos(a)
        b.tri((cx - px * w, cy - py * w, 0.0), (cx + px * w, cy + py * w, 0.0),
              (cx + math.cos(a) * lean, cy + math.sin(a) * lean, h), "leaf_a")
        if k % 2 == 0:
            b.tri((cx - px * w, cy - py * w, 0.0),
                  (cx + math.cos(a) * lean, cy + math.sin(a) * lean, h),
                  (cx + math.cos(a) * 0.02, cy + math.sin(a) * 0.02, h * 0.8),
                  "leaf_b")
    return b.finish(name, mats, collection)


def mangrove_mesh_v2(mats, collection, name="VEG_MangroveMesh"):
    b = B()
    # arching roots
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.2
        x0, y0 = math.cos(a) * 0.9, math.sin(a) * 0.9
        x1, y1 = math.cos(a) * 0.55, math.sin(a) * 0.55
        b.box((x0, y0, 0.45), (0.10, 0.10, 1.0), "timber")
        b.box((x1 * 1.2, y1 * 1.2, 0.95), (0.08, 0.08, 0.55), "timber")
    b.box((0, 0, 1.15), (0.36, 0.36, 1.3), "timber")
    # canopy lumps
    for (cx, cy, cz, r) in ((0, 0, 1.95, 1.25), (0.7, 0.4, 1.75, 0.85),
                            (-0.6, -0.4, 1.72, 0.8), (0.2, -0.7, 1.68, 0.72)):
        seg, rings = 7, 4
        verts = []
        for j in range(1, rings):
            phi = math.pi * j / rings
            for i in range(seg):
                th = 2 * math.pi * i / seg
                verts.append((cx + r * math.sin(phi) * math.cos(th),
                              cy + r * 0.9 * math.sin(phi) * math.sin(th),
                              cz + r * 0.62 * math.cos(phi)))
        top = len(verts)
        verts.append((cx, cy, cz + r * 0.62))
        start = len(b.v)
        b.v.extend(verts)
        for j in range(rings - 2):
            for i in range(seg):
                p = start + j * seg + i
                q = start + j * seg + (i + 1) % seg
                rr = start + (j + 1) * seg + i
                ss = start + (j + 1) * seg + (i + 1) % seg
                b.f.append((p, q, ss, rr))
                b.m.append("mangrove")
        for i in range(seg):
            b.f.append((start + (rings - 2) * seg + i,
                        start + (rings - 2) * seg + (i + 1) % seg, top))
            b.m.append("mangrove")
    return b.finish(name, mats, collection)


# ---------------------------------------------------------------------------
# paths, plaza, shore foam, reef, ripples
# ---------------------------------------------------------------------------
def _catmull_rom(points, samples_per_seg=8):
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for k in range(samples_per_seg):
            t = k / samples_per_seg
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    return out


def path_ribbon(site, mats, collection, points, width=2.3, name="ENV_Path"):
    """Terrain-following lane ribbon; keeps above water only."""
    sm = _catmull_rom(points, 8)
    verts, faces, mats_i = [], [], []
    prev = None
    for i, (x, y) in enumerate(sm):
        h = S.height_at(site, x, y)
        if h < 0.18:
            prev = None
            continue
        # tangent
        if i == 0:
            nx, ny = sm[1][0] - x, sm[1][1] - y
        elif i == len(sm) - 1:
            nx, ny = x - sm[i - 1][0], y - sm[i - 1][1]
        else:
            nx, ny = sm[i + 1][0] - sm[i - 1][0], sm[i + 1][1] - sm[i - 1][1]
        Ln = math.hypot(nx, ny) or 1.0
        nx, ny = -ny / Ln, nx / Ln
        a = (x + nx * width / 2, y + ny * width / 2, h + 0.06)
        b = (x - nx * width / 2, y - ny * width / 2, h + 0.06)
        if prev is not None:
            n = len(verts)
            verts.extend([prev[0], prev[1], b, a])
            faces.append((n, n + 1, n + 2, n + 3))
            mats_i.append(0)
        prev = (a, b)
    if not faces:
        return None
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mats["path"])
    me.polygons.foreach_set("material_index", mats_i)
    me.update()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    return ob


def plaza_mesh(site, mats, collection, xy, radii, rotation, name="ENV_Plaza"):
    cx, cy = xy
    rx, ry = radii
    seg, rings = 28, 6
    verts = [(cx, cy, S.height_at(site, cx, cy) + 0.07)]
    for r in range(1, rings + 1):
        f = r / rings
        for i in range(seg):
            a = 2 * math.pi * i / seg
            x = cx + math.cos(a) * rx * f
            y = cy + math.sin(a) * ry * f
            # rotate the ellipse
            xr = cx + (x - cx) * math.cos(rotation) - (y - cy) * math.sin(rotation)
            yr = cy + (x - cx) * math.sin(rotation) + (y - cy) * math.cos(rotation)
            verts.append((xr, yr, S.height_at(site, xr, yr) + 0.07))
    faces = []
    for i in range(seg):
        faces.append((0, 1 + i, 1 + (i + 1) % seg))
    for r in range(rings - 1):
        b0 = 1 + r * seg
        b1 = 1 + (r + 1) * seg
        for i in range(seg):
            faces.append((b0 + i, b1 + i, b1 + (i + 1) % seg, b0 + (i + 1) % seg))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mats["path"])
    me.update()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    return ob


def _chain_contour(segs, tol=6.0):
    """Chain unordered marching-squares segments into ordered polylines."""
    pool = list(segs)
    lines = []
    while pool:
        a, b = pool.pop(0)
        line = [a, b]
        changed = True
        while changed and pool:
            changed = False
            head = line[0]
            tail = line[-1]
            for idx, (p, q) in enumerate(pool):
                if math.hypot(p[0] - tail[0], p[1] - tail[1]) < tol:
                    line.append(q); pool.pop(idx); changed = True; break
                if math.hypot(q[0] - tail[0], q[1] - tail[1]) < tol:
                    line.append(p); pool.pop(idx); changed = True; break
                if math.hypot(q[0] - head[0], q[1] - head[1]) < tol:
                    line.insert(0, p); pool.pop(idx); changed = True; break
                if math.hypot(p[0] - head[0], p[1] - head[1]) < tol:
                    line.insert(0, q); pool.pop(idx); changed = True; break
        # thin out dense marching-squares points for a clean ribbon
        if len(line) > 3:
            out = [line[0]]
            for p in line[1:]:
                if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= 2.2:
                    out.append(p)
            if out[-1] != line[-1]:
                out.append(line[-1])
            lines.append(out)
        elif len(line) >= 2:
            lines.append(line)
    return lines


def shore_foam(site, mats, collection, name="FX_ShoreFoam"):
    S.set_grad_site(site)
    segs = S.zero_contour_segments(site, step=3.0)
    lines = _chain_contour(segs, tol=6.5)
    verts, faces = [], []
    for line in lines:
        if len(line) < 2:
            continue
        # tangent + landward normal per point
        pts = []
        for i, (x, y) in enumerate(line):
            if i == 0:
                tx, ty = line[1][0] - x, line[1][1] - y
            elif i == len(line) - 1:
                tx, ty = x - line[i - 1][0], y - line[i - 1][1]
            else:
                tx, ty = line[i + 1][0] - line[i - 1][0], line[i + 1][1] - line[i - 1][1]
            L = math.hypot(tx, ty) or 1.0
            nx, ny = -ty / L, tx / L
            gx = (S.height_at(site, x + 1.5, y) - S.height_at(site, x - 1.5, y)) / 3.0
            gy = (S.height_at(site, x, y + 1.5) - S.height_at(site, x, y - 1.5)) / 3.0
            if nx * gx + ny * gy < 0:
                nx, ny = -nx, -ny
            pts.append(((x + nx * 1.35, y + ny * 1.35),
                        (x - nx * 0.45, y - ny * 0.45)))
        base = len(verts)
        for (pin, pout) in pts:
            verts.append((pin[0], pin[1], 0.045))
            verts.append((pout[0], pout[1], 0.045))
        for i in range(len(pts) - 1):
            k = base + i * 2
            faces.append((k, k + 1, k + 3, k + 2))
    if not faces:
        return None
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mats["foam"])
    me.update()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    return ob


def _ellipse_ring(cx, cy, rx, ry, z, seg=18):
    pts = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        pts.append((cx + math.cos(a) * rx, cy + math.sin(a) * ry, z))
    return pts


def reef_patches(site, mats, collection, rng):
    cfg = site.get("reef") or {}
    n = int(cfg.get("count", 0))
    if n <= 0:
        return []
    made = []
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(cfg["r0"], cfg["r1"])
        x = cfg["center"][0] + math.cos(a) * rr
        y = cfg["center"][1] + math.sin(a) * rr
        if S.height_at(site, x, y) > -1.6:
            continue
        rx = rng.uniform(*cfg["size"])
        ry = rx * rng.uniform(0.45, 0.8)
        z = -rng.uniform(1.1, cfg["depth"])
        verts = _ellipse_ring(x, y, rx, ry, z)
        # raised centre + a clean triangle fan (no two-vertex edge faces)
        verts.append((x, y, z + rng.uniform(0.25, 0.6)))
        c = len(verts) - 1
        faces = [(i2, (i2 + 1) % (len(verts) - 1), c) for i2 in range(len(verts) - 1)]
        me = bpy.data.meshes.new("FX_Reef_%02d" % i)
        me.from_pydata(verts, [], faces)
        me.materials.append(mats["reef" if i % 3 else "reef_b"])
        me.update()
        ob = bpy.data.objects.new("FX_Reef_%02d" % i, me)
        ob.location = (0, 0, 0)
        collection.objects.link(ob)
        made.append(ob)
    return made


def ripple_marks(site, mats, collection, rng, count=None):
    n = count if count is not None else site.get("ripples", 10)
    made = []
    for i in range(n):
        # scatter on water near the built waterfront and around the boat
        for _ in range(40):
            x = rng.uniform(-site["extent"] * 0.32, site["extent"] * 0.32)
            y = rng.uniform(-site["extent"] * 0.38, site["extent"] * 0.20)
            if S.height_at(site, x, y) < -0.9:
                break
        else:
            continue
        rx = rng.uniform(1.8, 4.8)
        ry = rx * rng.uniform(0.16, 0.28)
        seg = 14
        verts = []
        for k in range(seg + 1):
            a = math.pi * (0.08 + 0.84 * k / seg)
            verts.append((x + math.cos(a) * rx, y + math.sin(a) * ry, 0.035))
        for k in range(seg + 1):
            a = math.pi * (0.08 + 0.84 * k / seg)
            verts.append((x + math.cos(a) * rx * 0.88, y + math.sin(a) * ry * 0.88 + 0.22, 0.035))
        faces = []
        for k in range(seg):
            faces.append((k, k + 1, seg + 2 + k, seg + 1 + k))
        me = bpy.data.meshes.new("FX_Ripple_%02d" % i)
        me.from_pydata(verts, [], faces)
        me.materials.append(mats["foam"])
        me.update()
        ob = bpy.data.objects.new("FX_Ripple_%02d" % i, me)
        collection.objects.link(ob)
        made.append(ob)
    return made


def crates_and_props(site, mats, collection, rng, near, count=7):
    made = []
    for i in range(count):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(4.0, 12.0)
        x, y = near[0] + math.cos(a) * r, near[1] + math.sin(a) * r
        h = S.height_at(site, x, y)
        if h < 0.25:
            continue
        s = rng.uniform(0.45, 0.85)
        b = B()
        b.box((0, 0, s / 2), (s, s, s), "crate")
        b.box((0, 0, s * 0.72), (s * 1.04, s * 0.10, 0.05), "timber")
        ob = b.finish("PROP_Crate_%02d" % i, mats, collection)
        ob.location = (x, y, h)
        ob.rotation_euler = (0, 0, rng.uniform(0, 3.14))
        made.append(ob)
    return made
