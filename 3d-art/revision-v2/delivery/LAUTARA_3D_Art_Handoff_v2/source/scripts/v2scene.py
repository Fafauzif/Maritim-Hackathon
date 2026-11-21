"""V2 scene assembly: terrain, water, anchors, cameras, section, look and render."""
import json
import math
import os
import sys

import bpy
import bmesh
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base")
for p in (HERE, BASE):
    if p not in sys.path:
        sys.path.insert(0, p)

import site_lib as L
import v2sites as S
import v2props as V

WATER_Z = 0.0

LOOK = {
    "view_transform": "Khronos PBR Neutral",
    "look": "None",
    "exposure": -0.56,
    "grade_sat": 0.96,
    "sun": 4.3,
    "fill": 170.0,
    "world": 0.46,
    "engine": "BLENDER_EEVEE",
    "samples_still": 40,
    "samples_anim": 14,
}


# ---------------------------------------------------------------------------
# scene scaffolding
# ---------------------------------------------------------------------------
def reset_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in list(bpy.data.collections):
        bpy.data.collections.remove(coll)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)
    for mat in list(bpy.data.materials):
        if mat.users == 0:
            bpy.data.materials.remove(mat)
    scene = bpy.context.scene
    scene.name = "CoastScene"
    return scene


def make_collections(scene):
    names = ["ENV_Land", "ENV_Water", "BLD_Village", "PROP_Survey", "VEG_Scatter",
             "FX_Water", "SEC_Section", "SEC_Stage", "CAM_Rigs", "LGT_Rig",
             "GUIDE_Authoring"]
    cols = {}
    for n in names:
        c = bpy.data.collections.new(n)
        scene.collection.children.link(c)
        cols[n] = c
    return cols


# ---------------------------------------------------------------------------
# terrain and water
# ---------------------------------------------------------------------------
def build_terrain(site, mats, collection):
    ext = site["extent"]
    step = site["terrain_step"]
    n = int(round(ext / step)) + 1
    xs = np.linspace(-ext / 2, ext / 2, n)
    ys = np.linspace(-ext / 2, ext / 2, n)
    X, Y = np.meshgrid(xs, ys)
    h = S.terrain_heights(site, X, Y)
    pal = site["palette"]

    stops = np.array([-6.8, -3.4, -1.35, -0.18, 0.55, 2.1, 4.0], dtype=np.float32)
    cols = [pal["bed_deep"], pal["bed_deep"], pal["bed_shallow"], pal["sand"],
            pal["sand"], pal["ground"], pal["veg"]]
    col_arr = np.array(cols, dtype=np.float32)
    flat_h = h.ravel()
    rgb = np.empty((flat_h.size, 3), dtype=np.float32)
    for c in range(3):
        rgb[:, c] = np.interp(flat_h, stops, col_arr[:, c])
    # fine tonal variation, deterministic, small enough to stay in family
    wiggle = (0.022 * np.sin(X.ravel() / 6.1 + 0.3) * np.cos(Y.ravel() / 5.4) +
              0.012 * np.sin(X.ravel() / 2.3 + 1.7))
    rgb = np.clip(rgb + wiggle[:, None], 0, 1)

    terrain_mat = L.make_material("MAT_Terrain_VCol", pal["ground"], rough=0.97)
    nt = terrain_mat.node_tree
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_name = "Col"
    bsdf = next((nd for nd in nt.nodes if nd.type == "BSDF_PRINCIPLED"), None)
    if bsdf:
        nt.links.new(attr.outputs["Color"], bsdf.inputs["Base Color"])

    me = bpy.data.meshes.new("ENV_Terrain")
    nx, ny = n, n
    verts = np.empty((ny * nx, 3), dtype=np.float32)
    verts[:, 0] = X.ravel()
    verts[:, 1] = Y.ravel()
    verts[:, 2] = h.ravel()
    quads = np.empty(((ny - 1) * (nx - 1), 4), dtype=np.int32)
    idx = np.arange(ny * nx).reshape(ny, nx)
    quads[:, 0] = idx[:-1, :-1].ravel()
    quads[:, 1] = idx[:-1, 1:].ravel()
    quads[:, 2] = idx[1:, 1:].ravel()
    quads[:, 3] = idx[1:, :-1].ravel()
    me.vertices.add(ny * nx)
    me.vertices.foreach_set("co", verts.ravel())
    me.loops.add(quads.size)
    me.loops.foreach_set("vertex_index", quads.ravel())
    me.polygons.add(len(quads))
    me.polygons.foreach_set("loop_start", np.arange(0, quads.size, 4, dtype=np.int32))
    for mat in (terrain_mat,):
        me.materials.append(mat)
    me.update()
    me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    me.validate()
    ob = bpy.data.objects.new("ENV_Terrain", me)
    collection.objects.link(ob)
    try:
        attr_data = me.color_attributes.new(name="Col", type="FLOAT_COLOR", domain="POINT")
        rgba = np.empty((nx * ny, 4), dtype=np.float32)
        rgba[:, :3] = rgb
        rgba[:, 3] = 1.0
        attr_data.data.foreach_set("color", rgba.ravel())
    except Exception as exc:
        print("WARN terrain colour attribute:", exc)
    return ob, (xs, ys, h)


def build_water(site, palette, collection):
    ext = site["extent"] + 320.0
    mat = L.make_material("ENV_Water_Mat", palette["water"], rough=0.80,
                          alpha=palette["water_alpha"])
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=ext / 2)
    me = bpy.data.meshes.new("ENV_Water")
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new("ENV_Water", me)
    ob.location = (0, 0, WATER_Z)
    collection.objects.link(ob)
    ob["waterline"] = "Z=0"
    return ob


# ---------------------------------------------------------------------------
# empties / cameras
# ---------------------------------------------------------------------------
def make_empty(name, location, collection, size=3.0):
    ob = bpy.data.objects.new(name, None)
    ob.empty_display_type = "PLAIN_AXES"
    ob.empty_display_size = size
    ob.location = location
    collection.objects.link(ob)
    return ob


def make_camera(name, lens, collection, ortho_scale=None):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    data.clip_start = 0.5
    data.clip_end = 5000.0
    if ortho_scale:
        data.type = "ORTHO"
        data.ortho_scale = ortho_scale
    ob = bpy.data.objects.new(name, data)
    collection.objects.link(ob)
    return ob


def track_to(ob, target):
    con = ob.constraints.new("TRACK_TO")
    con.target = target
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    return con


def build_anchors_and_cameras(site, cols, scene, boat_pos, jetty_base, jetty_end,
                              section_axis, section_info):
    coll = cols["CAM_Rigs"]
    bx, by = boat_pos[0], boat_pos[1]
    rigs = {}

    make_empty("COAST_ORIGIN", (0, 0, 0), coll, 10)
    make_empty("ORBIT_SITE", (0, 0, 0), coll, 9)
    make_empty("ORBIT_WATERFRONT", (bx * 0.65, by * 0.85, 1.5), coll, 6)
    t_survey = make_empty("TARGET_SURVEY", (bx, by, 1.4), coll, 5)
    make_empty("ANCHOR_VESSEL", (bx, by, 0.0), coll, 4)
    make_empty("ANCHOR_JETTY", (jetty_end[0], jetty_end[1], 0.6), coll, 4)
    a = make_empty("SECTION_A", (section_axis[0][0], section_axis[0][1], 0.0), coll, 6)
    b = make_empty("SECTION_B", (section_axis[1][0], section_axis[1][1], 0.0), coll, 6)
    a["role"] = "section offshore end"
    b["role"] = "section inland end"

    ov = site["overview"]
    cam = make_camera("COAST_OVERVIEW", ov["lens"], coll)
    cam.location = ov["pos"]
    ov_t = make_empty("TARGET_OVERVIEW", ov["target"], coll, 6)
    track_to(cam, ov_t)
    rigs["COAST_OVERVIEW"] = cam

    plan = make_camera("COAST_PLAN", 50.0, coll, ortho_scale=site["plan_scale"])
    pc = site.get("plan_center", (0.0, 0.0))
    plan.location = (pc[0], pc[1], 720.0)
    plan.rotation_euler = (0.0, 0.0, 0.0)
    rigs["COAST_PLAN"] = plan

    ap = site["approach"]
    cam_ap = make_camera("COAST_APPROACH", ap["lens"], coll)
    cam_ap.location = ap["pos"]
    ap_t = make_empty("TARGET_APPROACH", ap["target"], coll, 5)
    track_to(cam_ap, ap_t)
    rigs["COAST_APPROACH"] = cam_ap

    det = site["detail"]
    cam_det = make_camera("COAST_DETAIL", det["lens"], coll)
    cam_det.location = det["pos"]
    det_t = make_empty("TARGET_DETAIL", det["target"], coll, 4)
    track_to(cam_det, det_t)
    rigs["COAST_DETAIL"] = cam_det

    # section camera
    (ax, ay), (bx2, by2) = section_axis
    vx, vy = bx2 - ax, by2 - ay
    vlen = math.hypot(vx, vy)
    ux, uy = vx / vlen, vy / vlen
    nx, ny = uy, -ux
    if section_info and "nrm" in section_info:
        nx, ny = section_info["nrm"]
    else:
        # choose the side that is water, so the section reads from offshore
        midx, midy = ax + vx * 0.5, ay + vy * 0.5
        h_plus = S.height_at(site, midx + nx * 40, midy + ny * 40)
        h_minus = S.height_at(site, midx - nx * 40, midy - ny * 40)
        if h_plus > h_minus:
            nx, ny = -nx, -ny
    z_lo, z_hi = section_info["z_lo"], section_info["z_hi"]
    band = z_hi - z_lo
    ortho_h = band * 1.14
    ortho_w = ortho_h * 16.0 / 9.0
    ortho_w = max(96.0, min(178.0, ortho_w)) * 0.92
    ortho_h = ortho_w * 9.0 / 16.0
    z_mid = (z_lo + z_hi) / 2 - 0.02 * ortho_h
    # focus the frame between the survey boat and the landing root, so the boat,
    # jetty and the nearest houses all read inside the same crop
    t_boat = (boat_pos[0] - ax) * ux + (boat_pos[1] - ay) * uy
    t_jet = (jetty_base[0] - ax) * ux + (jetty_base[1] - ay) * uy
    t_focus = max(0.0, min(vlen, 0.5 * (t_boat + t_jet) + 2.0))
    fx, fy = ax + ux * t_focus, ay + uy * t_focus
    sec = make_camera("COAST_SECTION", 50.0, coll, ortho_scale=ortho_w)
    standoff = 150.0
    sec.location = (fx + nx * standoff, fy + ny * standoff, z_mid)
    sec_t = make_empty("TARGET_SECTION", (fx, fy, z_mid), coll, 6)
    track_to(sec, sec_t)
    sec.data.clip_start = 1.0
    sec.data.clip_end = 1200.0
    rigs["COAST_SECTION"] = sec
    sec["ortho_width_m"] = ortho_w
    sec["standoff_m"] = standoff
    sec["view_normal"] = [nx, ny, 0.0]
    sec["section_band_z"] = [z_lo, z_hi]
    sec["focus_t"] = round(t_focus, 3)

    scene.camera = cam
    return rigs, {"section_axis": section_axis, "normal": (nx, ny),
                  "ortho_w": ortho_w, "z_lo": z_lo, "z_hi": z_hi, "z_mid": z_mid,
                  "standoff": standoff, "mid": (fx, fy), "focus_t": t_focus}


# ---------------------------------------------------------------------------
# section builder
# ---------------------------------------------------------------------------
def _extrude_section(points_sz, origin, u, nrm, thickness, mat, name, collection,
                     zscale):
    """Extrude a closed 2D profile given in (s, z) world metres around the cut."""
    ax, ay = origin
    ux, uy = u
    nx, ny = nrm
    half = thickness / 2.0
    verts = []
    for side in (-1, 1):
        for (ss, zz) in points_sz:
            verts.append((ax + ux * ss + nx * half * side,
                          ay + uy * ss + ny * half * side,
                          zz * zscale))
    n = len(points_sz)
    faces = []
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, j + n, i + n))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    me.update()
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    return ob


def _section_front_profile(points_sz, origin, u, nrm, mat, name, collection, zscale,
                          offset, thickness=0.25):
    """A thin opaque silhouette pushed in front of the cut slab.

    Section props otherwise sit inside the water/land volume and are tinted or
    hidden by it. The boat is drawn as a front-facing cutout so its hull reads
    against the water column without exploding the whole section.
    """
    ax, ay = origin
    ux, uy = u
    nx, ny = nrm
    half = thickness / 2.0
    verts = []
    for side in (-1, 1):
        for (ss, zz) in points_sz:
            verts.append((ax + ux * ss + nx * (offset + half * side),
                          ay + uy * ss + ny * (offset + half * side),
                          zz * zscale))
    n = len(points_sz)
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, j + n, i + n))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    me.update()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    return ob


def _section_line(points_sz, origin, u, nrm, thickness, mat, name, collection, zscale,
                  offset=0.0):
    ax, ay = origin
    ux, uy = u
    nx, ny = nrm
    half = thickness / 2.0
    verts, faces = [], []
    for i, (ss, zz) in enumerate(points_sz):
        verts.extend([(ax + ux * ss - nx * (half - offset),
                       ay + uy * ss - ny * (half - offset), zz * zscale),
                      (ax + ux * ss + nx * (half + offset),
                       ay + uy * ss + ny * (half + offset), zz * zscale)])
        if i > 0:
            k = i * 2
            faces.append((k - 2, k - 1, k + 1, k))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    me.update()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    return ob


def build_section(site, mats, palette, collection, stage_collection, axis,
                  boat_pos, jetty_base, jetty_end, houses, section_info):
    pal = palette
    land_mat = L.make_material("MAT_Section_Land", tuple(c * 0.92 for c in pal["sand"]),
                               rough=0.97)
    soil_mat = L.make_material("MAT_Section_Soil", tuple(c * 0.76 for c in pal["ground"]),
                               rough=0.97)
    strata_mat = L.make_material("MAT_Section_Strata_A",
                                 tuple(min(1.0, c * 0.9 + 0.04) for c in pal["timber"]),
                                 rough=0.98)
    bed_mat = L.make_material("MAT_Section_Bed", tuple(c * 0.72 for c in pal["bed_deep"]),
                              rough=0.98)
    water_mat = L.make_material("MAT_Section_Water",
                                tuple(min(1.0, c * 1.12 + 0.03) for c in pal["water"]),
                                rough=0.12, alpha=0.46)
    ink = L.make_material("MAT_Section_Ink", (0.085, 0.078, 0.070), rough=1.0)
    cream = L.make_material("MAT_Section_Cream", (0.94, 0.91, 0.83), rough=0.95)
    wall_mat = L.make_material("MAT_Section_Wall", pal["wall_a"], rough=0.92)
    backdrop_mat = bpy.data.materials.new("MAT_Section_Backdrop")
    backdrop_mat.use_nodes = True
    bnt = backdrop_mat.node_tree
    bnt.nodes.clear()
    bem = bnt.nodes.new("ShaderNodeEmission")
    bem.inputs["Color"].default_value = (0.74, 0.70, 0.62, 1.0)
    bem.inputs["Strength"].default_value = 1.0
    bout = bnt.nodes.new("ShaderNodeOutputMaterial")
    bnt.links.new(bem.outputs[0], bout.inputs["Surface"])
    hull_mat = L.make_material("MAT_Section_Hull", pal["hull"], rough=0.8)
    roof_mat = L.make_material("MAT_Section_Roof", pal["roof_a"], rough=0.9)
    timber_mat = L.make_material("MAT_Section_Timber", pal["timber"], rough=0.9)
    leaf_mat = L.make_material("MAT_Section_Leaf", pal["leaf"], rough=0.95)

    (ax, ay), (bx, by) = axis
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    u = (dx / length, dy / length)
    nrm = (-u[1], u[0])
    # choose the camera side here, once, and hand the same normal to the camera
    # and to the backdrop. Choosing it twice put the cream backdrop in front of
    # the Amur cut.
    mid_tmp = (ax + dx * 0.5, ay + dy * 0.5)
    h_plus = S.height_at(site, mid_tmp[0] + nrm[0] * 40, mid_tmp[1] + nrm[1] * 40)
    h_minus = S.height_at(site, mid_tmp[0] - nrm[0] * 40, mid_tmp[1] - nrm[1] * 40)
    if h_plus > h_minus:
        nrm = (-nrm[0], -nrm[1])
    n = 220
    ts = np.linspace(0.0, 1.0, n)
    xs = ax + dx * ts
    ys = ay + dy * ts
    hs = np.array([S.height_at(site, float(x), float(y)) for x, y in zip(xs, ys)])
    ss = ts * length

    exag = float(site["section_exag"])
    floor = float(min(hs.min(), 0.0)) - 2.4
    thick = np.maximum(hs - floor, 0.08)
    verts, faces = [], []
    # build the solid cut as one mesh with stratified material bands
    def slab(z0s, z1s, mat_index):
        base = len(verts)
        for i in range(n):
            for side in (-1, 1):
                verts.append((xs[i] + nrm[0] * 1.5 * side,
                              ys[i] + nrm[1] * 1.5 * side,
                              z0s[i] * exag))
        nonlocal faces
        # front/back faces
        for i in range(n - 1):
            a = base + i * 2
            faces.append((a, a + 2, a + 3, a + 1))
            faces.append((a + 1, a + 3, a + 2, a))
    # Instead of one mesh per band, build four closed slabs with separate names.
    def solid_slab(z0s, z1s, mat, name):
        b = V.B()
        for i in range(n - 1):
            p0 = (xs[i], ys[i], z0s[i] * exag)
            p1 = (xs[i + 1], ys[i + 1], z0s[i + 1] * exag)
            p2 = (xs[i + 1], ys[i + 1], z1s[i + 1] * exag)
            p3 = (xs[i], ys[i], z1s[i] * exag)
            pa = (xs[i] + nrm[0] * 3.0, ys[i] + nrm[1] * 3.0, p0[2])
            pb = (xs[i + 1] + nrm[0] * 3.0, ys[i + 1] + nrm[1] * 3.0, p1[2])
            pc = (xs[i + 1] + nrm[0] * 3.0, ys[i + 1] + nrm[1] * 3.0, p2[2])
            pd = (xs[i] + nrm[0] * 3.0, ys[i] + nrm[1] * 3.0, p3[2])
            b.quad(p0, p1, p2, p3, "m")     # near face
            b.quad(pd, pc, pb, pa, "m")     # far face
            b.quad(p3, p2, pc, pd, "m")     # top
            b.quad(pa, pb, p1, p0, "m")     # bottom
        ob = b.finish(name, {"m": mat}, collection)
        return ob

    sections = []
    deep_bottom = np.full_like(hs, floor)
    sections.append(solid_slab(deep_bottom, floor + 0.50 * thick, bed_mat, "SECTION_Bed"))
    sections.append(solid_slab(floor + 0.50 * thick, floor + 0.78 * thick, strata_mat,
                               "SECTION_Strata_A"))
    sections.append(solid_slab(floor + 0.78 * thick, floor + 0.93 * thick, soil_mat,
                               "SECTION_Soil"))
    sections.append(solid_slab(floor + 0.93 * thick, hs, land_mat, "SECTION_Land"))
    # vegetation cap: a thin surface strip following the land profile only
    cap_pts = [(float(ss[i]), float(max(hs[i], 0.0) + 0.16)) for i in range(n)
               if hs[i] > 0.30]
    if len(cap_pts) >= 2:
        _section_line(cap_pts, (ax, ay), u, nrm, 1.2,
                      L.make_material("MAT_Section_Topsoil",
                                      tuple(c * 0.84 for c in pal["veg"]), rough=0.98),
                      "SECTION_Topsoil", collection, exag)
    # water column above the bed, clipped just below Z=0 (1.5 cm sliver avoids
    # zero-area faces over dry land while staying invisible)
    sections.append(solid_slab(np.minimum(hs, -0.015), np.zeros_like(hs), water_mat,
                               "SECTION_Water"))

    # profile + waterline ink lines
    prof = [(float(ss[i]), float(hs[i])) for i in range(n)]
    ink_line = _section_line(prof, (ax, ay), u, nrm, 0.22, ink, "SECTION_ProfileLine",
                             collection, exag)
    wl = [(0.0, 0.0), (length, 0.0)]
    _section_line(wl, (ax, ay), u, nrm, 0.30, cream, "SECTION_Waterline", collection, exag)
    _section_line([(0.0, 0.0), (length, 0.0)], (ax, ay), u, nrm, 0.10, ink,
                  "SECTION_WaterlineInk", collection, exag)

    # boat silhouette at the cut, projected along the axis
    bt = (boat_pos[0] - ax) * u[0] + (boat_pos[1] - ay) * u[1]
    jt = (jetty_base[0] - ax) * u[0] + (jetty_base[1] - ay) * u[1]
    t_focus = max(0.0, min(length, 0.5 * (bt + jt) + 2.0))
    # Props must sit proud of the 3 m cut slab or the water/land slabs hide them.
    pt = 3.6
    boat_profile = [(bt - 5.4, 0.0), (bt - 5.4, 0.72), (bt - 4.1, 0.78),
                    (bt - 2.6, 0.78), (bt - 2.0, 2.35), (bt + 1.4, 2.35),
                    (bt + 1.9, 0.80), (bt + 4.4, 0.74), (bt + 5.3, 0.55),
                    (bt + 4.2, 0.05), (bt + 2.2, -0.92), (bt - 3.6, -0.92)]
    _section_front_profile(boat_profile, (ax, ay), u, nrm, hull_mat, "SECTION_Boat",
                           collection, exag, offset=2.2, thickness=0.30)
    _section_line([(bt - 5.4, 0.02), (bt - 5.4, 0.72), (bt - 4.1, 0.78),
                   (bt - 2.6, 0.78), (bt - 2.0, 2.35), (bt + 1.4, 2.35),
                   (bt + 1.9, 0.80), (bt + 4.4, 0.74), (bt + 5.3, 0.55),
                   (bt + 4.2, 0.05), (bt + 2.2, -0.92), (bt - 3.6, -0.92),
                   (bt - 5.4, 0.02)],
                  (ax, ay), u, nrm, 0.18, ink, "SECTION_BoatSheerLine", collection,
                  exag, offset=2.38)
    _section_line([(bt - 3.6, -0.92), (bt + 2.2, -0.92), (bt + 4.2, 0.05)],
                  (ax, ay), u, nrm, 0.14, ink, "SECTION_BoatKeelLine", collection, exag)
    cabin = [(bt - 2.0, 0.80), (bt - 2.0, 2.35), (bt + 1.4, 2.35), (bt + 1.4, 0.80)]
    _section_front_profile(cabin, (ax, ay), u, nrm, cream, "SECTION_BoatCabin",
                           collection, exag, offset=2.24, thickness=0.26)
    mast = [(bt + 0.8, 2.35), (bt + 0.9, 2.35), (bt + 0.9, 4.3), (bt + 0.8, 4.3)]
    _extrude_section(mast, (ax, ay), u, nrm, 1.2, timber_mat, "SECTION_BoatMast",
                     collection, exag)
    # jetty crossing the cut
    jt_end = (jetty_end[0] - ax) * u[0] + (jetty_end[1] - ay) * u[1]
    deck_z = site["jetty"]["deck_z"]
    if abs(jt_end - jt) > 2.0:
        s0, s1 = min(jt, jt_end), max(jt, jt_end)
        deck = [(s0, deck_z - 0.14), (s1, deck_z - 0.14), (s1, deck_z + 0.14),
                (s0, deck_z + 0.14)]
        _extrude_section(deck, (ax, ay), u, nrm, pt, timber_mat, "SECTION_JettyDeck",
                         collection, exag)
        _section_line([(s0, deck_z + 0.16), (s1, deck_z + 0.16)], (ax, ay), u, nrm,
                      0.14, ink, "SECTION_JettyDeckLine", collection, exag)
        # piles down to the sampled bed
        for frac in (0.15, 0.45, 0.78, 0.98):
            sp = s0 + (s1 - s0) * frac
            ix = ax + (dx / length) * sp
            iy = ay + (dy / length) * sp
            bed = min(S.height_at(site, ix, iy), 0.0)
            pile = [(sp - 0.13, bed), (sp + 0.13, bed), (sp + 0.13, deck_z),
                    (sp - 0.13, deck_z)]
            _extrude_section(pile, (ax, ay), u, nrm, pt, timber_mat,
                             "SECTION_JettyPile_%d" % int(frac * 100), collection, exag)
    # nearest readable houses framing the landing
    def house_dist(h):
        cx, cy = h["xy"]
        return abs((cx - ax) * -u[1] + (cy - ay) * u[0])

    near = []
    for h in houses:
        cx, cy = h["xy"]
        sp = (cx - ax) * u[0] + (cy - ay) * u[1]
        if house_dist(h) < 26.0 and abs(sp - t_focus) < 50.0:
            near.append((sp, h))
    near = sorted(near, key=lambda p: abs(p[0] - t_focus))[:3]
    for k, (sp, h) in enumerate(near):
        cx, cy = h["xy"]
        base_h = S.height_at(site, cx, cy)
        w = h["w"]
        wall_h = h["wall_h"]
        roof_h = h["roof_h"]
        body = [(sp - w / 2, base_h), (sp - w / 2, base_h + wall_h),
                (sp + w / 2, base_h + wall_h), (sp + w / 2, base_h)]
        _extrude_section(body, (ax, ay), u, nrm, pt, wall_mat,
                         "SECTION_House_%d" % k, collection, exag)
        roof = [(sp - w / 2 - 0.5, base_h + wall_h),
                (sp, base_h + wall_h + roof_h),
                (sp + w / 2 + 0.5, base_h + wall_h)]
        _extrude_section([(sp - w / 2 - 0.5, base_h + wall_h - 0.12),
                          (sp, base_h + wall_h + roof_h),
                          (sp + w / 2 + 0.5, base_h + wall_h - 0.12)],
                         (ax, ay), u, nrm, pt, roof_mat,
                         "SECTION_HouseRoof_%d" % k, collection, exag)
        _section_line(roof, (ax, ay), u, nrm, 0.16, ink,
                      "SECTION_HouseRoofLine_%d" % k, collection, exag)
    # landing pavilion: posts, deck and hipped roof silhouette
    lm_xy = site.get("landmark", {}).get("xy")
    if lm_xy:
        sp = (lm_xy[0] - ax) * u[0] + (lm_xy[1] - ay) * u[1]
        if abs(sp - t_focus) < 58.0:
            base_h = S.height_at(site, lm_xy[0], lm_xy[1])
            deck = [(sp - 5.2, base_h + 0.55), (sp + 5.2, base_h + 0.55),
                    (sp + 5.2, base_h + 0.85), (sp - 5.2, base_h + 0.85)]
            _extrude_section(deck, (ax, ay), u, nrm, pt, timber_mat,
                             "SECTION_PavilionDeck", collection, exag)
            for dxp in (-4.4, -1.6, 1.6, 4.4):
                post = [(sp + dxp - 0.14, base_h), (sp + dxp + 0.14, base_h),
                        (sp + dxp + 0.14, base_h + 3.6), (sp + dxp - 0.14, base_h + 3.6)]
                _extrude_section(post, (ax, ay), u, nrm, pt, timber_mat,
                                 "SECTION_PavilionPost_%d" % int(dxp * 10), collection, exag)
            roof = [(sp - 6.2, base_h + 3.6), (sp - 2.0, base_h + 5.1),
                    (sp + 2.0, base_h + 5.1), (sp + 6.2, base_h + 3.6)]
            _extrude_section(roof, (ax, ay), u, nrm, pt, roof_mat,
                             "SECTION_PavilionRoof", collection, exag)
            _section_line([(sp - 6.2, base_h + 3.6), (sp - 2.0, base_h + 5.1),
                           (sp + 2.0, base_h + 5.1), (sp + 6.2, base_h + 3.6)],
                          (ax, ay), u, nrm, 0.16, ink, "SECTION_PavilionRoofLine",
                          collection, exag)
    # palms on the dry side of the cut for scale
    count = 0
    for off in (-44, -34, -24, 22, 32, 42):
        sp = t_focus + off
        ix = ax + u[0] * sp
        iy = ay + u[1] * sp
        base_h = S.height_at(site, ix, iy)
        if base_h < 0.65 or count >= 3:
            continue
        trunk = [(sp - 0.22, base_h), (sp + 0.22, base_h),
                 (sp + 0.14, base_h + 6.4), (sp - 0.14, base_h + 6.4)]
        _extrude_section(trunk, (ax, ay), u, nrm, 1.0, timber_mat,
                         "SECTION_Palm_%d" % count, collection, exag)
        crown = [(sp - 2.6, base_h + 6.2), (sp - 1.1, base_h + 7.2),
                 (sp, base_h + 6.4), (sp + 1.2, base_h + 7.3),
                 (sp + 2.7, base_h + 6.1), (sp, base_h + 6.7)]
        _extrude_section(crown, (ax, ay), u, nrm, 1.4, leaf_mat,
                         "SECTION_PalmCrown_%d" % count, collection, exag)
        count += 1

    # backdrop for clean section stills only
    mx, my = ax + dx * 0.5, ay + dy * 0.5
    back_off = -42.0   # opposite side from the camera, behind the cut
    plane_c = (mx + nrm[0] * back_off, my + nrm[1] * back_off)
    pverts = [(plane_c[0] + u[0] * -220 + nrm[0] * 0, plane_c[1] + u[1] * -220, -140),
              (plane_c[0] + u[0] * 220, plane_c[1] + u[1] * 220, -140),
              (plane_c[0] + u[0] * 220, plane_c[1] + u[1] * 220, 180),
              (plane_c[0] + u[0] * -220, plane_c[1] + u[1] * -220, 180)]
    pme = bpy.data.meshes.new("SEC_Backdrop")
    pme.from_pydata(pverts, [], [(0, 1, 2, 3)])
    pme.materials.append(backdrop_mat)
    pme.update()
    pob = bpy.data.objects.new("SEC_Backdrop", pme)
    stage_collection.objects.link(pob)

    info = {
        "z_lo": float(floor * exag),
        "z_hi": float((max(hs.max(), 0.0) + 6.2) * exag),
        "exag": exag,
        "floor": floor,
        "length": length,
        "axis": axis,
        "u": u,
        "nrm": nrm,
        "objects": [s.name for s in sections],
    }
    return info


def build_travel_rig(site, scene, rigs):
    """Editable seven-second travel rig: overview -> approach -> lateral -> push,
    then a marked cut to the square-on section camera with a slow axis drift."""
    coll = bpy.data.collections.get("CAM_Rigs") or scene.collection
    cam = make_camera("TRAVEL_CAM", 40.0, coll)
    ov = site["overview"]
    ap = site["approach"]
    tgt = make_empty("TRAVEL_TARGET", ov["target"], coll, 3.0)
    track_to(cam, tgt)
    ov_pos, ov_tgt = Vector(ov["pos"]), Vector(ov["target"])
    ap_pos, ap_tgt = Vector(ap["pos"]), Vector(ap["target"])
    look = (ap_tgt - ap_pos)
    look.z = 0.0
    look.normalize()
    side = Vector((-look.y, look.x, 0.0))
    lat_pos = ap_pos + side * 16.0
    lat_tgt = ap_tgt + side * 5.0
    boat = Vector((site["_boat_pos"][0], site["_boat_pos"][1], 2.0))
    push_pos = ap_pos.lerp(boat, 0.26)
    push_tgt = ap_tgt.lerp(boat, 0.32)
    for frame, pos, target in ((1, ov_pos, ov_tgt), (62, ap_pos, ap_tgt),
                               (100, lat_pos, lat_tgt), (132, push_pos, push_tgt)):
        cam.location = pos
        cam.keyframe_insert("location", frame=frame)
        tgt.location = target
        tgt.keyframe_insert("location", frame=frame)
    # ease the path: auto-clamped Bezier is the default; leave handles coherent
    for fc in cam.animation_data.action.fcurves if hasattr(cam.animation_data.action, "fcurves") else []:
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
    # section hold: slow drift along the A-B axis for the last 1.5 s
    sec_cam = bpy.data.objects.get("COAST_SECTION")
    sec_t = bpy.data.objects.get("TARGET_SECTION")
    if sec_cam and sec_t:
        ax, ay = site["_axis"][0]
        bx, by = site["_axis"][1]
        L = math.hypot(bx - ax, by - ay) or 1.0
        ux, uy = (bx - ax) / L, (by - ay) / L
        start = sec_cam.location.copy()
        tstart = sec_t.location.copy()
        for frame, off in ((133, 0.0), (168, 2.6)):
            sec_cam.location = start + Vector((ux * off, uy * off, 0.0))
            sec_cam.keyframe_insert("location", frame=frame)
            sec_t.location = tstart + Vector((ux * off, uy * off, 0.0))
            sec_t.keyframe_insert("location", frame=frame)
    for m in list(scene.timeline_markers):
        scene.timeline_markers.remove(m)
    m1 = scene.timeline_markers.new("TRAVEL_SURFACE", frame=1)
    m1.camera = cam
    m2 = scene.timeline_markers.new("TRAVEL_CUTAWAY", frame=133)
    m2.camera = sec_cam if sec_cam else cam
    scene.frame_start = 1
    scene.frame_end = 168
    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene["travel_edit"] = json.dumps({
        "fps": 24, "frames": 168, "surface_frames": [1, 132],
        "cutaway_frames": [133, 168], "cut_frame": 133,
        "shot": "overview -> approach -> lateral -> push -> section hold",
        "render_note": "surface and cutaway use fixed collection visibility in two passes",
    })
    return {"camera": cam.name, "target": tgt.name, "cut_frame": 133,
            "frame_end": 168}


def build_lighting(palette, collection):
    sun_data = bpy.data.lights.new("LGT_Sun_Key", "SUN")
    sun_data.energy = LOOK["sun"]
    sun_data.angle = math.radians(3.4)
    sun_data.color = (1.0, 0.945, 0.855)
    sun = bpy.data.objects.new("LGT_Sun_Key", sun_data)
    sun.rotation_euler = (math.radians(47), math.radians(3), math.radians(212))
    collection.objects.link(sun)

    fill_data = bpy.data.lights.new("LGT_Sky_Fill", "AREA")
    fill_data.energy = LOOK["fill"]
    fill_data.size = 300.0
    fill_data.color = (0.72, 0.84, 1.0)
    fill = bpy.data.objects.new("LGT_Sky_Fill", fill_data)
    fill.location = (-190.0, -140.0, 235.0)
    fill.rotation_euler = (math.radians(26), 0.0, math.radians(-38))
    collection.objects.link(fill)

    # soft warm bounce from the sea side
    bounce_data = bpy.data.lights.new("LGT_Water_Bounce", "AREA")
    bounce_data.energy = 60.0
    bounce_data.size = 240.0
    bounce_data.color = (0.80, 0.88, 0.90)
    bounce = bpy.data.objects.new("LGT_Water_Bounce", bounce_data)
    bounce.location = (40.0, -220.0, 40.0)
    bounce.rotation_euler = (math.radians(70), 0.0, math.radians(10))
    collection.objects.link(bounce)
    return sun, fill, bounce


def build_world(palette, scene):
    world = bpy.data.worlds.get("WD_Coast") or bpy.data.worlds.new("WD_Coast")
    scene.world = world
    try:
        world.use_nodes = True
    except Exception:
        pass
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(coord.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs[0], out.inputs["Surface"])
    ramp.color_ramp.elements[0].position = 0.34
    ramp.color_ramp.elements[0].color = (*palette["sky_horizon"], 1.0)
    ramp.color_ramp.elements[1].position = 0.82
    ramp.color_ramp.elements[1].color = (*palette["sky_top"], 1.0)
    bg.inputs["Strength"].default_value = LOOK["world"]
    return world


def build_compositor(scene):
    status = {"ok": False, "reason": "unavailable"}
    try:
        scene.use_nodes = True
    except Exception:
        pass
    tree = getattr(scene, "compositing_node_group", None)
    if tree is None:
        try:
            tree = bpy.data.node_groups.new("NT_CoastGrade", "CompositorNodeTree")
            scene.compositing_node_group = tree
        except Exception as exc:
            status["reason"] = "no tree: %s" % exc
            return status
    try:
        tree.nodes.clear()
        if not [i for i in tree.interface.items_tree]:
            tree.interface.new_socket(name="Image", in_out="OUTPUT",
                                      socket_type="NodeSocketColor")
        rl = tree.nodes.new("CompositorNodeRLayers")
        hsv = tree.nodes.new("CompositorNodeHueSat")
        hsv.inputs["Saturation"].default_value = LOOK["grade_sat"]
        out = tree.nodes.new("NodeGroupOutput")
        tree.links.new(rl.outputs["Image"], hsv.inputs["Image"])
        tree.links.new(hsv.outputs["Image"], out.inputs["Image"])
        scene.render.use_compositing = True
        status = {"ok": True, "reason": "hue/sat", "saturation": LOOK["grade_sat"]}
    except Exception as exc:
        status["reason"] = "node build failed: %s" % exc
    return status


def apply_look(scene):
    vs = scene.view_settings
    vs.view_transform = LOOK["view_transform"]
    try:
        vs.look = LOOK["look"]
    except Exception:
        vs.look = "None"
    vs.exposure = LOOK["exposure"]
    vs.gamma = 1.0
    ee = scene.eevee
    for attr, val in (("taa_render_samples", LOOK["samples_still"]),
                      ("use_shadows", True), ("use_raytracing", True),
                      ("ray_tracing_method", "SCREEN")):
        try:
            setattr(ee, attr, val)
        except Exception:
            pass
    for attr, val in (("ray_tracing_options", None),):
        pass
    sun = bpy.data.objects.get("LGT_Sun_Key")
    if sun and sun.data:
        sun.data.energy = LOOK["sun"]
    fill = bpy.data.objects.get("LGT_Sky_Fill")
    if fill and fill.data:
        fill.data.energy = LOOK["fill"]
    world = scene.world
    if world and world.node_tree:
        for node in world.node_tree.nodes:
            if node.type == "BACKGROUND":
                node.inputs["Strength"].default_value = LOOK["world"]
    return dict(LOOK)


# ---------------------------------------------------------------------------
# render helpers
# ---------------------------------------------------------------------------
def set_visibility(show=(), hide=()):
    for coll in bpy.data.collections:
        coll.hide_render = False
    for name in hide:
        c = bpy.data.collections.get(name)
        if c:
            c.hide_render = True
    for name in show:
        c = bpy.data.collections.get(name)
        if c:
            c.hide_render = False


def render_still(scene, camera_name, path, res=(3840, 2160), samples=None,
                 hide=(), show=(), engine="BLENDER_EEVEE"):
    cam = bpy.data.objects.get(camera_name)
    if cam is None:
        raise RuntimeError("missing camera %s" % camera_name)
    # Timeline markers bound to cameras override scene.camera at the marker frame
    # (frame 1 of the travel edit). Park them for stills, then restore them.
    marker_state = [(m, m.camera) for m in scene.timeline_markers]
    for m in scene.timeline_markers:
        m.camera = None
    try:
        scene.camera = cam
        bpy.context.view_layer.update()
        set_visibility(show=show, hide=hide)
        scene.render.engine = engine
        if engine == "BLENDER_EEVEE":
            try:
                scene.eevee.taa_render_samples = samples or LOOK["samples_still"]
            except Exception:
                pass
        scene.render.resolution_x, scene.render.resolution_y = res
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = "PNG"
        scene.render.image_settings.color_mode = "RGB"
        scene.render.film_transparent = False
        os.makedirs(os.path.dirname(path), exist_ok=True)
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
    finally:
        for m, c in marker_state:
            m.camera = c
    produced = path if os.path.exists(path) else scene.render.frame_path(frame=scene.frame_current)
    return {"path": produced, "exists": os.path.exists(produced),
            "bytes": os.path.getsize(produced) if os.path.exists(produced) else 0,
            "resolution": list(res), "camera": camera_name, "engine": scene.render.engine}


def render_anim(scene, path_prefix, frame_start, frame_end, res=(1920, 1080),
                samples=None, hide=(), show=()):
    set_visibility(show=show, hide=hide)
    scene.render.engine = "BLENDER_EEVEE"
    if samples:
        try:
            scene.eevee.taa_render_samples = samples
        except Exception:
            pass
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.frame_start = frame_start
    scene.frame_end = frame_end
    os.makedirs(os.path.dirname(path_prefix), exist_ok=True)
    scene.render.filepath = path_prefix
    bpy.ops.render.render(animation=True)
    return {"frames": [frame_start, frame_end], "prefix": path_prefix}


