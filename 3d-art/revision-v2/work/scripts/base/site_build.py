"""Build one coastal diorama scene for The Ocean Has Floors.

Usage inside Blender (live MCP or headless):
    import site_build; site_build.build("kodingareng", stage="finish")

Sites: kodingareng, tunda, amur.
"""
import math
import os

import bpy
import bmesh
import numpy as np

import site_lib as L
from site_lib import smoothstep, box_mesh, grid_mesh, mesh_from, add_outline

ART = r"C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon\3d-art"
WATER_Z = 0.0

# ----------------------------------------------------------------------------
# site definitions
# ----------------------------------------------------------------------------

SITES = {
    "kodingareng": {
        "label": "Kodingareng Lompo",
        "kind": "island",
        "extent": 340.0,
        "center": (0.0, 0.0),
        "island_r": 104.0,
        "island_h": 2.7,
        "base": -7.6,
        "settle": {"x0": -86.0, "x1": -8.0, "y0": -92.0, "y1": -28.0,
                   "cluster_anchor": (-46.0, -58.0), "cluster_r": 30.0,
                   "cluster_count": 2, "cluster_spread": 26.0},
        "jetty": {"base": (12.0, -52.0), "direction": (0.12, -1.0), "length": 46.0},
        "boat": (20.0, -78.0),
        "section_axis": ((20.0, -110.0), (20.0, 24.0)),
        "section_fill": 0.72,
        "section_exag": 4.0,
        "overview": {"pos": (2.0, -244.0, 198.0), "target": (6.0, -38.0, 2.0), "lens": 58.0},
        "approach": {"pos": (75.0, -170.0, 58.0), "target": (-6.0, -60.0, 2.0), "lens": 50.0},
        "detail": {"pos": (55.0, -120.0, 16.0), "target": (5.0, -70.0, 3.0), "lens": 40.0},
        "plan_scale": 330.0,
        "palette": {
            "wall_a": (0.88, 0.82, 0.71),
            "wall_b": (0.82, 0.74, 0.60),
            "wall_c": (0.91, 0.88, 0.80),
            "roof_a": (0.50, 0.20, 0.13),
            "roof_b": (0.30, 0.42, 0.40),
            "trim": (0.93, 0.91, 0.86),
            "glass": (0.10, 0.13, 0.16),
            "timber": (0.33, 0.22, 0.14),
            "deck": (0.44, 0.33, 0.22),
            "hull": (0.90, 0.89, 0.86),
            "hull_stripe": (0.28, 0.38, 0.52),
            "sand": (0.80, 0.73, 0.56),
            "bed_shallow": (0.55, 0.66, 0.58),
            "bed_deep": (0.20, 0.31, 0.33),
            "ground": (0.52, 0.55, 0.33),
            "veg": (0.30, 0.42, 0.24),
            "leaf": (0.28, 0.45, 0.26),
            "trunk": (0.36, 0.28, 0.19),
            "water": (0.30, 0.62, 0.62),
            "water_alpha": 0.80,
            "sky_top": (0.46, 0.64, 0.80),
            "sky_horizon": (0.87, 0.90, 0.87),
        },
        "stilt": True,
        "vegetation": {"palms": 46, "bushes": 80, "reeds": 0},
        "front": -1.0,   # village faces -Y (south)
    },
    "tunda": {
        "label": "Pulau Tunda",
        "kind": "island",
        "extent": 380.0,
        "center": (5.0, 15.0),
        "island_r": 146.0,
        "island_h": 3.5,
        "base": -8.2,
        "settle": {"x0": -132.0, "x1": -40.0, "y0": -72.0, "y1": 22.0,
                   "cluster_anchor": (-88.0, -29.0), "cluster_r": 32.0,
                   "cluster_count": 2, "cluster_spread": 30.0},
        "jetty": {"base": (-88.0, -30.0), "direction": (-0.85, -0.53), "length": 40.0},
        "boat": (-116.0, -52.0),
        "section_axis": ((-155.0, -74.0), (-37.0, -8.0)),
        "section_fill": 0.72,
        "section_exag": 4.0,
        "overview": {"pos": (-44.0, -252.0, 206.0), "target": (-46.0, -16.0, 2.0), "lens": 55.0},
        "approach": {"pos": (-178.0, -112.0, 48.0), "target": (-104.0, -46.0, 1.0), "lens": 70.0},
        "detail": {"pos": (-150.0, -95.0, 15.0), "target": (-108.0, -45.0, 3.0), "lens": 40.0},
        "plan_scale": 380.0,
        "palette": {
            "wall_a": (0.74, 0.66, 0.55),
            "wall_b": (0.63, 0.55, 0.45),
            "wall_c": (0.84, 0.80, 0.70),
            "roof_a": (0.45, 0.24, 0.16),
            "roof_b": (0.30, 0.36, 0.28),
            "trim": (0.88, 0.85, 0.78),
            "glass": (0.09, 0.12, 0.13),
            "timber": (0.34, 0.25, 0.17),
            "deck": (0.40, 0.31, 0.21),
            "hull": (0.88, 0.88, 0.85),
            "hull_stripe": (0.26, 0.36, 0.44),
            "sand": (0.75, 0.68, 0.52),
            "bed_shallow": (0.48, 0.58, 0.50),
            "bed_deep": (0.17, 0.27, 0.29),
            "ground": (0.40, 0.48, 0.29),
            "veg": (0.22, 0.36, 0.20),
            "leaf": (0.24, 0.42, 0.24),
            "trunk": (0.34, 0.26, 0.18),
            "water": (0.26, 0.55, 0.56),
            "water_alpha": 0.82,
            "sky_top": (0.44, 0.62, 0.78),
            "sky_horizon": (0.88, 0.90, 0.86),
        },
        "stilt": False,
        "vegetation": {"palms": 30, "bushes": 150, "reeds": 0},
        "front": -1.0,
    },
    "amur": {
        "label": "Razdolnaya mouth, northern Amur Bay",
        "kind": "estuary",
        "extent": 460.0,
        "base": -6.6,
        "settle": {"x0": 80.0, "x1": 150.0, "y0": 58.0, "y1": 150.0,
                   "cluster_anchor": (95.0, 100.0), "cluster_r": 28.0,
                   "cluster_count": 1, "cluster_spread": 0.0},
        "jetty": {"base": (62.0, 96.0), "direction": (-1.0, -0.06), "length": 44.0},
        "boat": (28.0, 90.0),
        "section_axis": ((-60.0, 90.0), (110.0, 90.0)),
        "section_fill": 0.95,
        "section_exag": 3.4,
        "overview": {"pos": (10.0, -160.0, 195.0), "target": (24.0, 70.0, 2.0), "lens": 58.0},
        "approach": {"pos": (-14.0, -66.0, 34.0), "target": (32.0, 88.0, 1.0), "lens": 74.0},
        "detail": {"pos": (24.0, 34.0, 12.0), "target": (44.0, 92.0, 3.0), "lens": 38.0},
        "plan_scale": 460.0,
        "palette": {
            "wall_a": (0.63, 0.58, 0.50),
            "wall_b": (0.52, 0.46, 0.40),
            "wall_c": (0.72, 0.68, 0.60),
            "roof_a": (0.34, 0.26, 0.22),
            "roof_b": (0.28, 0.31, 0.33),
            "trim": (0.78, 0.75, 0.68),
            "glass": (0.09, 0.11, 0.12),
            "timber": (0.30, 0.23, 0.17),
            "deck": (0.36, 0.29, 0.21),
            "hull": (0.84, 0.85, 0.84),
            "hull_stripe": (0.24, 0.33, 0.42),
            "sand": (0.62, 0.58, 0.45),
            "bed_shallow": (0.42, 0.47, 0.43),
            "bed_deep": (0.16, 0.24, 0.28),
            "ground": (0.46, 0.46, 0.30),
            "veg": (0.36, 0.38, 0.24),
            "leaf": (0.40, 0.42, 0.26),
            "trunk": (0.32, 0.26, 0.19),
            "water": (0.24, 0.40, 0.45),
            "water_alpha": 0.86,
            "sky_top": (0.52, 0.62, 0.72),
            "sky_horizon": (0.84, 0.85, 0.83),
        },
        "stilt": False,
        "vegetation": {"palms": 0, "bushes": 90, "reeds": 320},
        "front": -1.0,
    },
}


# ----------------------------------------------------------------------------
# terrain
# ----------------------------------------------------------------------------

def terrain_heights(site, xs, ys):
    X, Y = np.meshgrid(xs, ys)
    if site["kind"] == "island":
        cx, cy = site["center"]
        R, hmax, base = site["island_r"], site["island_h"], site["base"]
        r = np.hypot(X - cx, Y - cy)
        t = np.clip((R - r) / (0.32 * R), 0.0, 1.0)
        s = t * t * (3.0 - 2.0 * t)
        h = base + (hmax - base) * s
        h = h + 0.9 * np.clip(1.0 - r / R, 0.0, 1.0) * s
        # secondary lobe so the silhouette is not a perfect disc
        lobe = np.exp(-(((X - (cx + 0.45 * R)) / (0.5 * R)) ** 2 +
                        ((Y - (cy + 0.30 * R)) / (0.4 * R)) ** 2))
        h = h + 1.5 * lobe * s
        # inland relief so the island is not a smooth dome
        h = h + 0.85 * s * np.exp(-(((X - (cx - 0.30 * R)) / (0.34 * R)) ** 2 +
                                    ((Y - (cy - 0.35 * R)) / (0.30 * R)) ** 2))
        h = h + 0.55 * np.sin(X / 19.0) * np.cos(Y / 15.0) * s
        h = h + 0.22 * np.sin(X / 8.0 + 1.3) * np.cos(Y / 7.0) * s
        return h
    # estuary: water in the middle, low banks east/west and to the north
    base = site["base"]
    banks = np.maximum(np.abs(X) - 54.0, Y - 74.0)
    s = smoothstep(0.0, 36.0, banks)
    h = base + 8.0 * s
    channel = np.exp(-(((X - 26.0 * np.sin((Y - 40.0) / 62.0)) / 34.0) ** 2)) * smoothstep(38.0, 74.0, Y)
    h = h - 5.4 * channel
    h = h + 0.18 * np.sin(X / 21.0) * np.cos(Y / 17.0)
    return h


def material_bands(palette):
    return [
        L.make_material('MAT_Bed_Deep', palette["bed_deep"], rough=0.95),
        L.make_material('MAT_Bed_Shallow', palette["bed_shallow"], rough=0.95),
        L.make_material('MAT_Sand', palette["sand"], rough=0.92),
        L.make_material('MAT_Ground', palette["ground"], rough=0.95),
        L.make_material('MAT_Vegetation', palette["veg"], rough=0.95),
    ]


def build_terrain(site, palette, collection):
    ext = site["extent"]
    step = 1.4 if ext <= 380 else 1.8
    n = int(ext / step)
    xs = np.linspace(-ext / 2, ext / 2, n)
    ys = np.linspace(-ext / 2, ext / 2, n)
    h = terrain_heights(site, xs, ys)

    # Smooth height-keyed vertex colours: no stair-stepped material bands.
    stops = [-3.6, -1.15, 0.12, 1.15, 2.7]
    cols = [palette["bed_deep"], palette["bed_shallow"], palette["sand"],
            palette["ground"], palette["veg"]]
    stops = np.array(stops, dtype=np.float32)
    col_arr = np.array(cols, dtype=np.float32)
    flat_h = h.ravel()
    rgb = np.empty((flat_h.size, 3), dtype=np.float32)
    for c in range(3):
        rgb[:, c] = np.interp(flat_h, stops, col_arr[:, c])

    terrain_mat = L.make_material('MAT_Terrain_VCol', palette["ground"], rough=0.96)
    nt = terrain_mat.node_tree
    attr = nt.nodes.new('ShaderNodeAttribute')
    attr.attribute_name = 'Col'
    bsdf = None
    for node in nt.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            bsdf = node
            break
    if bsdf:
        nt.links.new(attr.outputs['Color'], bsdf.inputs['Base Color'])

    ob = grid_mesh('ENV_Terrain', xs, ys, h.astype(np.float32), [terrain_mat],
                   collection=collection)
    me = ob.data
    try:
        attrib = me.color_attributes.new(name='Col', type='FLOAT_COLOR', domain='POINT')
        flat_rgba = np.empty((flat_h.size, 4), dtype=np.float32)
        flat_rgba[:, :3] = rgb
        flat_rgba[:, 3] = 1.0
        attrib.data.foreach_set('color', flat_rgba.ravel())
    except Exception:
        pass
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    return ob, (xs, ys, h)


def build_water(site, palette, collection, extent=None):
    ext = extent or site["extent"] + 220.0
    mat = L.make_material('ENV_Water_Mat', palette["water"], rough=0.16,
                          alpha=palette["water_alpha"])
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=ext / 2)
    me = bpy.data.meshes.new('ENV_Water')
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new('ENV_Water', me)
    ob.location = (0, 0, WATER_Z)
    collection.objects.link(ob)
    return ob
