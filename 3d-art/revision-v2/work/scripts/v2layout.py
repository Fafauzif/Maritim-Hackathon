"""V2 layout: lane-driven settlement, safe boats, vegetation patches and site build."""
import math
import os
import sys

import bpy
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base")
for p in (HERE, BASE):
    if p not in sys.path:
        sys.path.insert(0, p)

import site_lib as L
import props_build as P
import v2sites as S
import v2props as V
import v2scene as SC

MI = dict(wall_a=0, wall_b=1, wall_c=2, roof_a=3, roof_b=4, roof_c=5, trim=6,
          glass=7, timber=8, deck_a=9, deck_b=10, hull=11, stripe=12,
          leaf_a=13, leaf_b=14, trunk=15)


# ---------------------------------------------------------------------------
# 2D helpers
# ---------------------------------------------------------------------------
def _dist_point_seg(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    L2 = vx * vx + vy * vy
    if L2 <= 1e-9:
        return math.hypot(wx, wy)
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / L2))
    return math.hypot(px - (ax + vx * t), py - (ay + vy * t))


def _point_in_poly(px, py, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if ((y1 > py) != (y2 > py)) and (px < (x2 - x1) * (py - y1) / (y2 - y1) + x1):
            inside = not inside
    return inside


def _poly_overlap(a, b):
    """SAT overlap test for two convex polygons (both are rectangles)."""
    for poly in (a, b):
        for i in range(len(poly)):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % len(poly)]
            nx, ny = -(y2 - y1), (x2 - x1)
            L2 = nx * nx + ny * ny
            if L2 <= 1e-12:
                continue
            a_proj = [nx * p[0] + ny * p[1] for p in a]
            b_proj = [nx * p[0] + ny * p[1] for p in b]
            if max(a_proj) <= min(b_proj) or max(b_proj) <= min(a_proj):
                return False
    return True


def _obb(cx, cy, w, d, rot):
    c, s = math.cos(rot), math.sin(rot)
    pts = []
    for lx, ly in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)):
        pts.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    return pts


# ---------------------------------------------------------------------------
# settlement
# ---------------------------------------------------------------------------
def place_settlement(site, mats, cols, rng):
    """Place houses along authored lanes, facing the lane, with real yards."""
    coll = cols["BLD_Village"]
    s = site["settle"]
    target = int(s.get("count", 30))
    density = float(s.get("density", 0.75))
    lim = site["land_limits"]
    plaza = site["plaza"]
    lm = site["landmark"]
    lane_polys = site["lanes"]
    placed = []
    counters = {"slots": 0, "limits": 0, "blocked": 0, "terrain": 0, "density": 0}
    obstacles = []          # (poly, margin)
    house_meta = []
    variants = list(V.HOUSE_VARIANTS)

    def blocked(x, y, w, d, rot):
        poly = _obb(x, y, w, d, rot)
        # houses
        for (op, m) in obstacles:
            if _poly_overlap(poly, op):
                return True
        # plaza
        px, py = plaza["xy"]
        rx, ry = plaza["radii"]
        if ((x - px) / (rx + 2.5)) ** 2 + ((y - py) / (ry + 2.5)) ** 2 < 1.0:
            return True
        # landmark
        if math.hypot(x - lm["xy"][0], y - lm["xy"][1]) < 9.0:
            return True
        # jetty corridor
        j = site["jetty"]
        jx, jy = j["base"]
        dx, dy = j["direction"]
        Ln = math.hypot(dx, dy)
        ux, uy = dx / Ln, dy / Ln
        ex, ey = jx + ux * (j["length"] + 8), jy + uy * (j["length"] + 8)
        if _dist_point_seg(x, y, jx - ux * 8, jy - uy * 8, ex, ey) < 6.0:
            return True
        # lanes (keep carriageway clear)
        for polyline in lane_polys:
            for i in range(len(polyline) - 1):
                if _dist_point_seg(x, y, polyline[i][0], polyline[i][1],
                                   polyline[i + 1][0], polyline[i + 1][1]) < 3.3 + d * 0.15:
                    return True
        return False

    def terrain_ok(x, y, w, d, rot, stilt):
        pts = _obb(x, y, w + 0.5, d + 0.5, rot)
        hs = [S.height_at(site, px, py) for (px, py) in pts]
        if min(hs) < (0.30 if stilt else 0.45):
            return False
        if max(hs) - min(hs) > 1.75:
            return False
        if max(hs) > 5.5:
            return False
        return True

    # slot candidates from each lane, both sides
    slots = []
    for li, poly in enumerate(lane_polys):
        pts = V._catmull_rom(poly, 6)
        acc = 0.0
        last = None
        for i, (x, y) in enumerate(pts):
            if last is not None:
                acc += math.hypot(x - last[0], y - last[1])
            last = (x, y)
            if acc < 7.4:
                continue
            acc = 0.0
            tx, ty = pts[min(i + 1, len(pts) - 1)][0] - pts[max(i - 1, 0)][0], \
                     pts[min(i + 1, len(pts) - 1)][1] - pts[max(i - 1, 0)][1]
            Ln = math.hypot(tx, ty) or 1.0
            nx, ny = -ty / Ln, tx / Ln
            for side in (-1, 1):
                slots.append((x, y, nx * side, ny * side, li))

    rng.shuffle(slots)
    for pass_i in range(3):
        for (x, y, nx, ny, li) in slots:
            if len(placed) >= target:
                break
            key, w, d, wall_h, roof_h, roof, wall_mat, roof_mat, vs, porch, storeys = \
                variants[rng.integers(0, len(variants))]
            stilt = vs
            offset = 4.2 + d / 2.0
            hx = x + nx * offset
            hy = y + ny * offset
            if not (lim["x0"] <= hx <= lim["x1"] and lim["y0"] <= hy <= lim["y1"]):
                counters["limits"] += 1
                continue
            # front (-Y local) faces the lane => -n
            rot = math.atan2(-nx, ny)
            if blocked(hx, hy, w, d, rot):
                counters["blocked"] += 1
                continue
            if not terrain_ok(hx, hy, w, d, rot, stilt):
                counters["terrain"] += 1
                continue
            if rng.random() > density:
                counters["density"] += 1
                continue
            name = "BLD_House_%03d" % len(placed)
            b = V.house_mesh(name, mats, w, d, wall_h, roof_h, roof, wall_mat,
                             roof_mat, stilt=stilt, porch=porch, storeys=storeys)
            ob = b.finish(name, mats, coll)
            base_z = max(S.height_at(site, px, py) for (px, py) in
                         _obb(hx, hy, w + 1.0, d + 1.0, rot))
            # flat stone pad so a house reads as on-grade on sloping ground
            pad = V.B()
            pad.box((0, 0, -0.40), (w + 1.0, d + 1.0, 0.82), "stone")
            pad_ob = pad.finish(name + "_Pad", mats, coll)
            pad_ob.location = (hx, hy, base_z)
            pad_ob.rotation_euler = (0.0, 0.0, rot)
            ob.location = (hx, hy, base_z + 0.03)
            ob.rotation_euler = (0.0, 0.0, rot)
            placed.append(ob)
            poly = _obb(hx, hy, w + 0.6, d + 0.6, rot)
            obstacles.append((poly, 0.0))
            house_meta.append({"name": name, "xy": (hx, hy), "w": w, "d": d,
                               "wall_h": wall_h, "roof_h": roof_h, "variant": key,
                               "rotation": rot})
        if len(placed) >= target:
            break

    # landmark building + community hall
    lm = site["landmark"]
    ground = S.height_at(site, lm["xy"][0], lm["xy"][1])
    if lm["kind"] == "landing_pavilion":
        ob = V.pavilion_mesh(mats, coll, "BLD_LandingPavilion")
        ob.location = (lm["xy"][0], lm["xy"][1], max(ground - 0.15, 0.05))
        ob.rotation_euler = (0, 0, lm["rotation"])
    elif lm["kind"] == "landing_shelter":
        ob = V.pavilion_mesh(mats, coll, "BLD_LandingShelter", w=9.4, d=6.8)
        ob.location = (lm["xy"][0], lm["xy"][1], max(ground - 0.15, 0.05))
        ob.rotation_euler = (0, 0, lm["rotation"])
    else:
        ob = V.working_landing_mesh(mats, coll, "BLD_WorkingLanding")
        ob.location = (lm["xy"][0], lm["xy"][1], max(ground - 0.25, 0.0))
        ob.rotation_euler = (0, 0, lm["rotation"])
    obstacles.append((_obb(lm["xy"][0], lm["xy"][1], 12, 9, lm["rotation"]), 0.0))
    # community hall near the plaza
    px, py = site["plaza"]["xy"]
    hx = px + (site["plaza"]["radii"][0] + 9.0) * math.cos(0.7)
    hy = py + (site["plaza"]["radii"][1] + 9.0) * math.sin(0.7)
    hh = S.height_at(site, hx, hy)
    if hh > 0.5:
        hall = V.community_hall_mesh(mats, coll, "BLD_CommunityHall")
        hall.location = (hx, hy, hh - 0.08)
        hall.rotation_euler = (0, 0, 0.7)
        obstacles.append((_obb(hx, hy, 14, 9, 0.7), 0.0))
    counters["slots"] = len(slots)
    counters["placed"] = len(placed)
    return placed, house_meta, obstacles, counters


# ---------------------------------------------------------------------------
# boats
# ---------------------------------------------------------------------------
def place_boats(site, mats, cols, rng):
    coll = cols["PROP_Survey"]
    j = site["jetty"]
    jx, jy = j["base"]
    dx, dy = j["direction"]
    Ln = math.hypot(dx, dy)
    ux, uy = dx / Ln, dy / Ln
    bow_rot = math.atan2(-ux, uy)
    target = site["boat_target"]
    x, y, maxh, minh, ok = S.find_water_spot(site, target[0], target[1], 10.6, 3.0,
                                             bow_rot, clear=1.55, max_radius=48.0)
    boat = V.boat_mesh_v2(mats, coll, "PROP_SurveyBoat", length=10.6, width=3.0,
                          cabin=True, draft=0.95)
    boat.location = (x, y, 0.0)
    boat.rotation_euler = (0, 0, bow_rot)
    boat["clearance"] = {"max_bed_z": round(float(maxh), 3), "ok": bool(ok)}
    local = []
    n_local = 3 if site["kind"] == "island" else 2
    for i in range(n_local):
        if site["kind"] == "island":
            ang = bow_rot + math.pi + (i - (n_local - 1) / 2) * 0.7
            dist = 5.5 + i * 2.7
            tx = jx + ux * (j["length"] + 5.0) + math.cos(ang) * dist
            ty = jy + uy * (j["length"] + 5.0) + math.sin(ang) * dist
        else:
            ang = bow_rot + math.pi + (i - 0.5) * 0.8
            tx = x + (i - (n_local - 1) / 2) * 14.0
            ty = y + 12.0 + i * 3.0
        lx, ly, mh, mnh, lok = S.find_water_spot(site, tx, ty, 6.4, 1.9, ang,
                                                 clear=0.95, max_radius=32.0)
        ob = V.outrigger_mesh_v2(mats, coll, "PROP_LocalBoat_%d" % i)
        ob.location = (lx, ly, 0.0)
        ob.rotation_euler = (0, 0, ang)
        ob["clearance"] = {"max_bed_z": round(float(mh), 3), "ok": bool(lok)}
        local.append(ob)
    return boat, local, (x, y), (maxh, minh, ok)


# ---------------------------------------------------------------------------
# vegetation
# ---------------------------------------------------------------------------
def place_vegetation(site, mats, cols, rng, obstacles, house_meta):
    coll = cols["VEG_Scatter"]
    cfg = site["vegetation"]
    lim = site["land_limits"]
    j = site["jetty"]
    jx, jy = j["base"]
    dx, dy = j["direction"]
    Ln = math.hypot(dx, dy)
    jx2, jy2 = jx + dx / Ln * (j["length"] + 6), jy + dy / Ln * (j["length"] + 6)
    lm = site["landmark"]["xy"]
    plaza = site["plaza"]
    lane_polys = site["lanes"]

    def blocked(x, y, margin=0.0):
        for (poly, m) in obstacles:
            if _point_in_poly(x, y, poly):
                return True
        if ((x - plaza["xy"][0]) / (plaza["radii"][0] + 1.5)) ** 2 + \
           ((y - plaza["xy"][1]) / (plaza["radii"][1] + 1.5)) ** 2 < 1.0:
            return True
        if math.hypot(x - lm[0], y - lm[1]) < 7.5:
            return True
        if _dist_point_seg(x, y, jx, jy, jx2, jy2) < 4.0:
            return True
        for poly in lane_polys:
            for i in range(len(poly) - 1):
                if _dist_point_seg(x, y, poly[i][0], poly[i][1],
                                   poly[i + 1][0], poly[i + 1][1]) < 2.2:
                    return True
        return False

    def make_instances(mesh, count, h_lo, h_hi, scale_lo, scale_hi, prefix,
                       clusters=None, radius=None, avoid=True, slope_max=0.45):
        made = 0
        tries = 0
        max_tries = max(600, count * 45)
        while made < count and tries < max_tries:
            tries += 1
            if clusters:
                cx, cy, cr, _w = clusters[rng.integers(0, len(clusters))]
                a = rng.uniform(0, 2 * math.pi)
                r = cr * math.sqrt(rng.random())
                x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
            else:
                x = rng.uniform(-site["extent"] / 2 + 18, site["extent"] / 2 - 18)
                y = rng.uniform(-site["extent"] / 2 + 18, site["extent"] / 2 - 18)
            if not (lim["x0"] - 24 <= x <= lim["x1"] + 24 and
                    lim["y0"] - 24 <= y <= lim["y1"] + 24):
                continue
            h = S.height_at(site, x, y)
            if not (h_lo <= h <= h_hi):
                continue
            if avoid and blocked(x, y):
                continue
            e = 1.2
            gx = (S.height_at(site, x + e, y) - S.height_at(site, x - e, y)) / (2 * e)
            gy = (S.height_at(site, x, y + e) - S.height_at(site, x, y - e)) / (2 * e)
            if math.hypot(gx, gy) > slope_max:
                continue
            ob = bpy.data.objects.new("%s_%04d" % (prefix, made), mesh)
            s = rng.uniform(scale_lo, scale_hi)
            ob.scale = (s, s, s * rng.uniform(0.85, 1.15))
            ob.rotation_euler = (0, 0, rng.uniform(0, 6.28))
            ob.location = (x, y, h - 0.10)
            coll.objects.link(ob)
            made += 1
        return made

    counts = {}
    if cfg.get("palms", 0):
        proto = V.palm_mesh_v2(mats, coll, "VEG_PalmMesh")
        mesh = proto.data
        bpy.data.objects.remove(proto, do_unlink=True)
        counts["palms"] = make_instances(mesh, cfg["palms"], 0.85, 3.1, 0.78, 1.18,
                                         "VEG_Palm", clusters=cfg.get("clusters"))
    if cfg.get("shrubs", 0):
        proto = V.shrub_mesh_v2(mats, coll, "VEG_ShrubMesh", 0)
        mesh = proto.data
        bpy.data.objects.remove(proto, do_unlink=True)
        counts["shrubs"] = make_instances(mesh, cfg["shrubs"], 0.65, 4.1, 0.75, 1.75,
                                          "VEG_Shrub", clusters=cfg.get("clusters"),
                                          slope_max=0.7)
    if cfg.get("mangroves", 0):
        proto = V.mangrove_mesh_v2(mats, coll, "VEG_MangroveMesh")
        mesh = proto.data
        bpy.data.objects.remove(proto, do_unlink=True)
        counts["mangroves"] = make_instances(mesh, cfg["mangroves"], -0.35, 0.55,
                                             0.75, 1.15, "VEG_Mangrove",
                                             clusters=cfg.get("clusters"),
                                             slope_max=1.0)
    if cfg.get("reeds", 0):
        proto = V.reed_mesh_v2(mats, coll, "VEG_ReedMesh")
        mesh = proto.data
        bpy.data.objects.remove(proto, do_unlink=True)
        counts["reeds"] = make_instances(mesh, cfg["reeds"], -0.55, 1.0, 0.9, 1.6,
                                         "VEG_Reed", clusters=cfg.get("clusters"),
                                         slope_max=1.1)
    return counts


# ---------------------------------------------------------------------------
# terrestrial detail
# ---------------------------------------------------------------------------
def add_ground_detail(site, mats, cols, rng, obstacles):
    made = {}
    # paths
    for i, lane in enumerate(site["lanes"]):
        ob = V.path_ribbon(site, mats, cols["ENV_Land"], lane, width=2.3,
                           name="ENV_Lane_%02d" % i)
        if ob:
            made.setdefault("lanes", []).append(ob.name)
    # plaza
    p = site["plaza"]
    ob = V.plaza_mesh(site, mats, cols["ENV_Land"], p["xy"], p["radii"],
                      p["rotation"], "ENV_Plaza")
    if ob:
        made["plaza"] = ob.name
    # crates near the landing
    lm = site["landmark"]["xy"]
    crates = V.crates_and_props(site, mats, cols["PROP_Survey"], rng,
                                site["plaza"]["xy"], count=9)
    made["crates"] = [c.name for c in crates]
    return made


def add_water_detail(site, mats, cols, rng, boat_pos):
    made = {}
    ob = V.shore_foam(site, mats, cols["FX_Water"])
    if ob:
        made["foam"] = ob.name
    reefs = V.reef_patches(site, mats, cols["FX_Water"], rng)
    made["reefs"] = len(reefs)
    ripples = V.ripple_marks(site, mats, cols["FX_Water"], rng)
    made["ripples"] = len(ripples)
    return made


# ---------------------------------------------------------------------------
# whole site
# ---------------------------------------------------------------------------
def build_site(site_key, run_root=None):
    site = S.SITES[site_key]
    S.set_grad_site(site)
    scene = SC.reset_scene()
    cols = SC.make_collections(scene)
    mats = V.make_materials(site["palette"])
    rng = np.random.default_rng(100 + list(S.SITES).index(site_key))

    terrain, (xs, ys, hgrid) = SC.build_terrain(site, mats, cols["ENV_Land"])
    water = SC.build_water(site, site["palette"], cols["ENV_Water"])

    houses, house_meta, obstacles, settle_counts = place_settlement(site, mats, cols, rng)
    jetty = V.build_jetty_v2(site, mats, cols["PROP_Survey"])
    boat, local_boats, boat_pos, boat_clear = place_boats(site, mats, cols, rng)
    # actual jetty base/end
    j = site["jetty"]
    jb = tuple(jetty.get("base", j["base"]))
    je = tuple(jetty.get("end", (j["base"][0] + j["direction"][0] * j["length"],
                                 j["base"][1] + j["direction"][1] * j["length"])))
    direction = (je[0] - jb[0], je[1] - jb[1])
    dl = math.hypot(*direction)
    direction = (direction[0] / dl, direction[1] / dl)
    # section line: offshore beyond the survey boat, inland behind the landing
    axis = ((boat_pos[0] + direction[0] * 30.0, boat_pos[1] + direction[1] * 30.0),
            (jb[0] - direction[0] * 100.0, jb[1] - direction[1] * 100.0))
    site["_axis"] = axis
    site["_jetty_base"] = jb
    site["_jetty_end"] = je
    site["_boat_pos"] = boat_pos
    site["_boat_clear"] = boat_clear
    site["_direction"] = direction

    veg_counts = place_vegetation(site, mats, cols, rng, obstacles, house_meta)
    ground = add_ground_detail(site, mats, cols, rng, obstacles)
    fx = add_water_detail(site, mats, cols, rng, boat_pos)

    # section first (fills SEC_Section), then cameras use its measured band
    sec_info = SC.build_section(site, mats, site["palette"], cols["SEC_Section"],
                                cols["SEC_Stage"], axis, boat_pos, jb, je,
                                house_meta, None)
    rigs, cam_info = SC.build_anchors_and_cameras(site, cols, scene, boat_pos, jb, je,
                                                  axis, sec_info)
    travel = SC.build_travel_rig(site, scene, rigs)
    SC.build_lighting(site["palette"], cols["LGT_Rig"])
    SC.build_world(site["palette"], scene)
    grade = SC.build_compositor(scene)
    look = SC.apply_look(scene)

    # section geometry is authoring-only in the beauty scene
    cols["SEC_Section"].hide_render = True
    cols["SEC_Stage"].hide_render = True
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.frame_start = 1
    scene.frame_end = 168
    scene.render.fps = 24
    scene.camera = rigs["COAST_OVERVIEW"]

    stats = {
        "site": site_key,
        "label": site["label"],
        "objects": len(scene.objects),
        "houses": len(houses),
        "settlement_slots": settle_counts,
        "vegetation": veg_counts,
        "boats": 1 + len(local_boats),
        "boat_clearance": {"max_bed_z": round(float(boat_clear[0]), 3),
                           "min_bed_z": round(float(boat_clear[1]), 3) if boat_clear[1] is not None else None,
                           "ok": bool(boat_clear[2])},
        "section": {"axis": axis, "exag": sec_info["exag"],
                    "z_lo": round(sec_info["z_lo"], 3), "z_hi": round(sec_info["z_hi"], 3),
                    "ortho_w": round(cam_info["ortho_w"], 2)},
        "ground_detail": ground,
        "water_detail": fx,
        "cameras": sorted(rigs.keys()) + ["TRAVEL_CAM"],
        "travel": travel,
        "empty_nodes": sorted(o.name for o in scene.objects if o.type == "EMPTY"),
        "terrain_vertices": len(terrain.data.vertices),
        "grade": grade,
        "look": look,
        "collections": sorted(c.name for c in bpy.data.collections),
    }
    return scene, stats






