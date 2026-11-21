"""V2 site definitions, terrain fields, shorelines, paths and safe water spots.

Coordinate convention: +X east, +Y north, +Z up, 1 unit = 1 m, water at Z=0.
All fields are analytic so the same height function feeds terrain, paths,
placements, section sampling and boat-draft rejection.
"""
import math

import numpy as np

WATER_Z = 0.0

# ---------------------------------------------------------------------------
# site definitions
# ---------------------------------------------------------------------------
SITES = {
    "kodingareng": {
        "label": "Kodingareng Lompo",
        "kind": "island",
        "extent": 360.0,
        "terrain_step": 1.7,
        "base": -7.6,
        "island": {
            "center": (0.0, 0.0),
            "r_mean": 94.0,
            "r_wave": [(2, 15.0, 0.55), (3, 9.0, 1.35), (5, 6.0, 0.20), (7, 3.5, 2.10)],
            "plateau": 1.75,
            "shelf": -2.35,
            "beach_width": 15.0,
            "relief": [(1.25, (-24.0, -18.0), (58.0, 42.0)),
                       (0.85, (36.0, 26.0), (40.0, 30.0))],
            "spits": [((104.0, -48.0), (42.0, 13.0), 1.05, 0.55),
                      ((-82.0, 34.0), (28.0, 18.0), 0.55, -0.25)],
        },
        "jetty": {"base": (10.0, -86.0), "direction": (0.10, -1.0), "length": 54.0,
                  "width": 3.4, "deck_z": 0.62},
        "boat_target": (10.0, -146.0),
        "settle": {"lane_seed": 4, "density": 0.90, "count": 34},
        "landmark": {"kind": "landing_pavilion", "xy": (4.0, -83.5),
                     "rotation": -0.10},
        "plaza": {"xy": (0.0, -76.0), "radii": (15.0, 10.0), "rotation": 0.1},
        "lanes": [
            [(-70.0, -34.0), (-52.0, -48.0), (-28.0, -62.0), (-8.0, -73.0), (0.0, -78.0)],
            [(-52.0, -48.0), (-44.0, -70.0), (-38.0, -82.0), (-30.0, -86.0)],
            [(-28.0, -62.0), (-18.0, -46.0), (-22.0, -28.0), (-34.0, -16.0)],
            [(-8.0, -73.0), (10.0, -70.0), (24.0, -60.0), (30.0, -44.0)],
            [(-44.0, -70.0), (-60.0, -62.0), (-72.0, -50.0)],
            [(-70.0, -34.0), (-58.0, -18.0), (-40.0, -8.0), (-20.0, -2.0)],
            [(-70.0, -34.0), (-78.0, -22.0), (-82.0, -8.0), (-74.0, 8.0)],
            [(-34.0, -16.0), (-12.0, -8.0), (10.0, -2.0), (26.0, 8.0)],
            [(30.0, -44.0), (48.0, -36.0), (62.0, -22.0), (66.0, -4.0)],
            [(8.0, -73.0), (18.0, -60.0), (24.0, -44.0), (26.0, -26.0)],
        ],
        "land_limits": {"x0": -98.0, "x1": 84.0, "y0": -94.0, "y1": 62.0},
        "vegetation": {"palms": 64, "shrubs": 120, "reeds": 0, "mangroves": 18,
                       "clusters": [(-58.0, -20.0, 35.0, 26), (34.0, 10.0, 34.0, 30),
                                    (-10.0, 44.0, 40.0, 24), (-70.0, 30.0, 28.0, 18)]},
        "reef": {"count": 26, "center": (0.0, 0.0), "r0": 96.0, "r1": 168.0,
                 "depth": 2.6, "size": (10.0, 24.0)},
        "ripples": 12,
        "overview": {"pos": (10.0, -310.0, 235.0), "target": (0.0, -50.0, 0.0), "lens": 36.0},
        "approach": {"pos": (64.0, -228.0, 54.0), "target": (6.0, -128.0, 2.0), "lens": 48.0},
        "detail": {"pos": (55.0, -190.0, 24.0), "target": (0.0, -115.0, 2.5), "lens": 42.0},
        "plan_scale": 470.0,
        "plan_center": (0.0, -20.0),
        "section_exag": 3.2,
        "section_fill": 0.90,
        "section_ortho_w": 138.0,
        "palette": {
            "wall_a": (0.84, 0.75, 0.61),
            "wall_b": (0.72, 0.60, 0.47),
            "wall_c": (0.90, 0.84, 0.73),
            "roof_a": (0.55, 0.24, 0.16),
            "roof_b": (0.26, 0.40, 0.37),
            "roof_c": (0.44, 0.34, 0.25),
            "trim": (0.90, 0.86, 0.78),
            "glass": (0.10, 0.12, 0.14),
            "timber": (0.31, 0.21, 0.13),
            "deck": (0.42, 0.30, 0.19),
            "hull": (0.88, 0.85, 0.78),
            "hull_stripe": (0.22, 0.36, 0.47),
            "sand": (0.76, 0.68, 0.51),
            "bed_shallow": (0.47, 0.56, 0.46),
            "bed_deep": (0.16, 0.27, 0.30),
            "ground": (0.49, 0.50, 0.32),
            "veg": (0.27, 0.39, 0.23),
            "leaf": (0.24, 0.40, 0.22),
            "trunk": (0.34, 0.26, 0.17),
            "water": (0.20, 0.48, 0.52),
            "water_alpha": 0.84,
            "sky_top": (0.36, 0.54, 0.68),
            "sky_horizon": (0.86, 0.83, 0.72),
            "foam": (0.93, 0.92, 0.84),
        },
        "front": -1.0,
    },
    "tunda": {
        "label": "Pulau Tunda",
        "kind": "island",
        "extent": 400.0,
        "terrain_step": 1.8,
        "base": -8.4,
        "island": {
            "center": (0.0, 0.0),
            "r_mean": 126.0,
            "r_wave": [(2, 16.0, 2.10), (3, 12.0, -0.40), (4, 8.0, 1.90), (6, 5.0, 0.30)],
            "plateau": 2.35,
            "shelf": -2.7,
            "beach_width": 18.0,
            "relief": [(1.85, (-36.0, 34.0), (58.0, 48.0)),
                       (1.10, (44.0, -24.0), (44.0, 36.0))],
            "cove": {"theta": 3.75, "depth": 24.0, "width": 0.42},
            "spits": [((118.0, 58.0), (34.0, 20.0), 0.85, 0.55),
                      ((60.0, -104.0), (38.0, 18.0), 0.50, -0.35)],
        },
        "jetty": {"base": (-96.0, -48.0), "direction": (-0.80, -0.60), "length": 42.0,
                  "width": 3.0, "deck_z": 0.58},
        "boat_target": (-124.0, -76.0),
        "settle": {"lane_seed": 11, "density": 0.86, "count": 40},
        "landmark": {"kind": "landing_shelter", "xy": (-92.0, -45.0), "rotation": 0.6},
        "plaza": {"xy": (-86.0, -38.0), "radii": (16.0, 12.0), "rotation": 0.55},
        "lanes": [
            [(-62.0, -26.0), (-78.0, -34.0), (-90.0, -41.0), (-96.0, -47.0)],
            [(-62.0, -26.0), (-48.0, -10.0), (-44.0, 12.0), (-50.0, 30.0)],
            [(-62.0, -26.0), (-82.0, -18.0), (-98.0, -6.0), (-106.0, 10.0)],
            [(-44.0, 12.0), (-20.0, 18.0), (6.0, 14.0), (24.0, 6.0)],
            [(-78.0, -34.0), (-70.0, -52.0), (-60.0, -64.0)],
            [(-50.0, 30.0), (-46.0, 48.0), (-54.0, 66.0), (-66.0, 78.0)],
            [(24.0, 6.0), (46.0, 0.0), (62.0, 12.0), (68.0, 30.0)],
            [(-98.0, -6.0), (-82.0, 8.0), (-62.0, 14.0), (-44.0, 12.0)],
            [(-10.0, -46.0), (-26.0, -40.0), (-44.0, -32.0), (-62.0, -26.0)],
        ],
        "land_limits": {"x0": -118.0, "x1": 116.0, "y0": -96.0, "y1": 92.0},
        "vegetation": {"palms": 52, "shrubs": 220, "reeds": 0, "mangroves": 34,
                       "clusters": [(-92.0, 6.0, 46.0, 34), (40.0, 44.0, 54.0, 38),
                                    (20.0, -50.0, 44.0, 30), (-48.0, 58.0, 40.0, 26)]},
        "reef": {"count": 18, "center": (0.0, 0.0), "r0": 128.0, "r1": 196.0,
                 "depth": 3.0, "size": (9.0, 18.0)},
        "ripples": 10,
        "overview": {"pos": (-10.0, -390.0, 270.0), "target": (0.0, -20.0, 0.0), "lens": 34.0},
        "approach": {"pos": (-172.0, -168.0, 54.0), "target": (-104.0, -56.0, 2.0), "lens": 54.0},
        "detail": {"pos": (-160.0, -132.0, 30.0), "target": (-112.0, -68.0, 2.5), "lens": 40.0},
        "plan_scale": 560.0,
        "plan_center": (0.0, -5.0),
        "section_exag": 3.2,
        "section_fill": 0.90,
        "section_ortho_w": 148.0,
        "palette": {
            "wall_a": (0.80, 0.70, 0.56),
            "wall_b": (0.66, 0.56, 0.43),
            "wall_c": (0.87, 0.81, 0.68),
            "roof_a": (0.48, 0.22, 0.15),
            "roof_b": (0.34, 0.29, 0.21),
            "roof_c": (0.27, 0.36, 0.30),
            "trim": (0.88, 0.84, 0.75),
            "glass": (0.09, 0.11, 0.12),
            "timber": (0.30, 0.21, 0.14),
            "deck": (0.39, 0.29, 0.19),
            "hull": (0.86, 0.84, 0.78),
            "hull_stripe": (0.25, 0.38, 0.44),
            "sand": (0.78, 0.72, 0.56),
            "bed_shallow": (0.39, 0.53, 0.44),
            "bed_deep": (0.14, 0.25, 0.28),
            "ground": (0.38, 0.46, 0.27),
            "veg": (0.19, 0.33, 0.18),
            "leaf": (0.21, 0.38, 0.20),
            "trunk": (0.33, 0.25, 0.16),
            "water": (0.17, 0.44, 0.47),
            "water_alpha": 0.82,
            "sky_top": (0.38, 0.55, 0.67),
            "sky_horizon": (0.85, 0.84, 0.76),
            "foam": (0.92, 0.91, 0.84),
        },
        "front": -1.0,
    },
    "amur": {
        "label": "Razdolnaya mouth, northern Amur Bay",
        "kind": "estuary",
        "extent": 480.0,
        "terrain_step": 1.9,
        "base": -6.6,
        "estuary": {
            "channel_width": 58.0,
            "width_gain": 74.0,
            "width_y0": 190.0,
            "center_x": 22.0,
            "sin_amp": 26.0,
            "sin_len": 92.0,
            "bh": 1.45,
            "bank": 38.0,
            "marsh": 0.30,
            "creeks": [(-60.0, 0.40), (12.0, -0.35), (86.0, 0.30)],
        },
        "jetty": {"base": (94.0, 58.0), "direction": (-1.0, -0.06), "length": 48.0,
                  "width": 3.2, "deck_z": 0.70},
        "boat_target": (42.0, 52.0),
        "settle": {"lane_seed": 23, "density": 0.84, "count": 22},
        "landmark": {"kind": "working_landing", "xy": (98.0, 64.0), "rotation": math.pi},
        "plaza": {"xy": (104.0, 72.0), "radii": (18.0, 13.0), "rotation": math.pi},
        "lanes": [
            [(92.0, 54.0), (104.0, 62.0), (112.0, 76.0), (108.0, 94.0)],
            [(104.0, 62.0), (88.0, 80.0), (82.0, 100.0), (88.0, 118.0)],
            [(112.0, 76.0), (132.0, 82.0), (148.0, 96.0), (154.0, 118.0)],
            [(104.0, 62.0), (116.0, 46.0), (128.0, 30.0)],
            [(108.0, 94.0), (126.0, 100.0), (138.0, 114.0), (132.0, 132.0)],
            [(88.0, 118.0), (104.0, 128.0), (122.0, 124.0), (132.0, 132.0)],
        ],
        "land_limits": {"x0": 70.0, "x1": 174.0, "y0": 20.0, "y1": 150.0},
        "vegetation": {"palms": 0, "shrubs": 120, "reeds": 360, "mangroves": 26,
                       "clusters": [(-104.0, 58.0, 60.0, 30), (-92.0, -8.0, 52.0, 24),
                                    (142.0, 112.0, 46.0, 22), (150.0, 36.0, 34.0, 16)]},
        "marsh": {"pools": [(-104.0, 26.0), (-126.0, 86.0), (-74.0, 116.0)],
                  "pools_r": (22.0, 14.0), "bank_pools": [(146.0, 58.0), (158.0, 130.0)]},
        "sandbars": [(-32.0, -72.0, 28.0, 12.0, -0.25), (18.0, -124.0, 34.0, 14.0, -0.35)],
        "reef": {"count": 0, "center": (0.0, 0.0), "r0": 0.0, "r1": 0.0,
                 "depth": 2.0, "size": (0.0, 0.0)},
        "ripples": 14,
        "overview": {"pos": (10.0, -140.0, 150.0), "target": (55.0, 55.0, 0.0), "lens": 40.0},
        "approach": {"pos": (4.0, -78.0, 46.0), "target": (54.0, 58.0, 2.0), "lens": 58.0},
        "detail": {"pos": (8.0, -12.0, 28.0), "target": (55.0, 50.0, 2.5), "lens": 42.0},
        "plan_scale": 500.0,
        "plan_center": (20.0, 10.0),
        "section_exag": 3.0,
        "section_fill": 0.92,
        "section_ortho_w": 190.0,
        "palette": {
            "wall_a": (0.67, 0.61, 0.52),
            "wall_b": (0.55, 0.48, 0.40),
            "wall_c": (0.75, 0.70, 0.62),
            "roof_a": (0.33, 0.26, 0.22),
            "roof_b": (0.27, 0.32, 0.36),
            "roof_c": (0.38, 0.31, 0.25),
            "trim": (0.80, 0.76, 0.68),
            "glass": (0.08, 0.10, 0.11),
            "timber": (0.29, 0.22, 0.16),
            "deck": (0.35, 0.28, 0.20),
            "hull": (0.82, 0.82, 0.78),
            "hull_stripe": (0.24, 0.33, 0.42),
            "sand": (0.66, 0.60, 0.46),
            "bed_shallow": (0.36, 0.42, 0.38),
            "bed_deep": (0.13, 0.21, 0.24),
            "ground": (0.44, 0.44, 0.29),
            "veg": (0.31, 0.33, 0.21),
            "leaf": (0.36, 0.38, 0.24),
            "trunk": (0.31, 0.25, 0.18),
            "water": (0.16, 0.31, 0.35),
            "water_alpha": 0.88,
            "sky_top": (0.43, 0.53, 0.61),
            "sky_horizon": (0.82, 0.81, 0.75),
            "foam": (0.88, 0.87, 0.81),
        },
        "front": -1.0,
    },
}


# ---------------------------------------------------------------------------
# analytic terrain
# ---------------------------------------------------------------------------
def _island_edge(theta, island):
    r = np.full_like(theta, island["r_mean"], dtype=np.float64)
    for k, amp, phase in island["r_wave"]:
        r = r + amp * np.cos(k * theta + phase)
    cove = island.get("cove")
    if cove:
        d = np.angle(np.exp(1j * (theta - cove["theta"])))
        r = r - cove["depth"] * np.exp(-(d / cove["width"]) ** 2)
    return r


def terrain_heights(site, X, Y):
    """Vectorised terrain height in metres (water at 0)."""
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    if site["kind"] == "island":
        isl = site["island"]
        cx, cy = isl["center"]
        dx, dy = X - cx, Y - cy
        th = np.arctan2(dy, dx)
        edge = _island_edge(th, isl)
        rr = np.hypot(dx, dy)
        # offshore shelf -> beach -> plateau
        t_land = np.clip((edge - rr) / isl["beach_width"], 0.0, 1.0)
        s_land = t_land * t_land * (3.0 - 2.0 * t_land)
        t_shelf = np.clip((rr - edge) / 92.0, 0.0, 1.0)
        s_shelf = t_shelf * t_shelf * (3.0 - 2.0 * t_shelf)
        h = isl["shelf"] + (site["base"] - isl["shelf"]) * s_shelf
        h = h + (isl["plateau"] - isl["shelf"]) * s_land
        # inland relief (rounded hills), damped by shore rise
        for amp, (ox, oy), (sx, sy) in isl["relief"]:
            h = h + amp * np.exp(-(((X - cx - ox) / sx) ** 2 +
                                   ((Y - cy - oy) / sy) ** 2)) * s_land
        # low-frequency unevenness, strongest inland
        h = h + 0.44 * np.sin(X / 23.0 + 0.4) * np.cos(Y / 19.0) * s_land
        h = h + 0.16 * np.sin(X / 7.5 + 1.3) * np.cos(Y / 6.5 + 0.2) * s_land
        # sand spits / bars
        for (sx, sy), (rx, ry), amp, lift in isl.get("spits", []):
            m = np.exp(-(((X - sx) / rx) ** 2 + ((Y - sy) / ry) ** 2))
            h = h + amp * m + lift * m * (h < 0.0)
        return h

    est = site["estuary"]
    # centreline of the Razdolnaya channel, river enters from +Y
    yb = np.clip((Y - est["width_y0"]), -240.0, 240.0)
    xc = est["center_x"] + est["sin_amp"] * np.sin(yb / est["sin_len"])
    half = est["channel_width"] + est["width_gain"] * np.clip((est["width_y0"] - Y) / 420.0, 0.0, 1.0)
    d = np.abs(X - xc)
    bank = np.clip((d - half) / est["bank"], 0.0, 1.0)
    s = bank * bank * (3.0 - 2.0 * bank)
    h = -est["channel_width"] * 0.0 + site["base"] + (est["bh"] - site["base"]) * s
    # west bank is a low marsh bench, east bank a slightly higher terrace
    west = (X < xc).astype(np.float64)
    h = h - west * est["marsh"] * s
    # marsh pools and tidal creeks
    for cx, cy in site.get("marsh", {}).get("pools", []):
        rx, ry = site["marsh"]["pools_r"]
        m = np.exp(-(((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2))
        h = h - 0.55 * m
    for cx, cy in site["marsh"].get("bank_pools", []):
        m = np.exp(-(((X - cx) / 20.0) ** 2 + ((Y - cy) / 12.0) ** 2))
        h = h - 0.45 * m
    for py, amp in est["creeks"]:
        creek = np.exp(-(((Y - py) / 12.0) ** 2)) * np.exp(-((d - half - 18.0) / 22.0) ** 2)
        h = h - 1.5 * creek
    # sand bars
    for cx, cy, rx, ry, z in site.get("sandbars", []):
        m = np.exp(-(((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2))
        h = np.maximum(h, np.minimum(z, h + 1.0 * m))
    # gentle undulation, kept low so the estuary stays flat
    h = h + 0.20 * np.sin(X / 26.0 + 0.7) * np.cos(Y / 21.0) * s
    return h


def height_at(site, x, y):
    h = terrain_heights(site, np.array([x], dtype=float), np.array([y], dtype=float))
    return float(np.asarray(h).reshape(-1)[0])


# ---------------------------------------------------------------------------
# shoreline extraction (marching squares on h=0)
# ---------------------------------------------------------------------------
def zero_contour_segments(site, step=3.0, bounds=None):
    ext = site["extent"] * 0.5 + 40.0
    if bounds:
        x0, x1, y0, y1 = bounds
    else:
        x0, x1, y0, y1 = -ext, ext, -ext, ext
    xs = np.arange(x0, x1 + step, step)
    ys = np.arange(y0, y1 + step, step)
    X, Y = np.meshgrid(xs, ys)
    H = terrain_heights(site, X, Y)
    segs = []
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            h00, h10 = H[j, i], H[j, i + 1]
            h01, h11 = H[j + 1, i], H[j + 1, i + 1]
            pts = []
            if (h00 > 0) != (h10 > 0):
                t = h00 / (h00 - h10)
                pts.append((xs[i] + t * step, ys[j]))
            if (h10 > 0) != (h11 > 0):
                t = h10 / (h10 - h11)
                pts.append((xs[i + 1], ys[j] + t * step))
            if (h11 > 0) != (h01 > 0):
                t = h11 / (h11 - h01)
                pts.append((xs[i + 1] - t * step, ys[j + 1]))
            if (h01 > 0) != (h00 > 0):
                t = h01 / (h01 - h00)
                pts.append((xs[i], ys[j + 1] - t * step))
            if len(pts) == 2:
                segs.append((pts[0], pts[1]))
            elif len(pts) == 4:
                segs.append((pts[0], pts[1]))
                segs.append((pts[2], pts[3]))
    return segs


def shore_ribbon_points(segs, width_land=2.4, width_sea=1.0):
    """Convert contour segments into a landward ribbon footprint.

    Returns list of (p_in, p_out) quad vertex pairs, where p_in is landward.
    """
    quads = []
    for (a, b) in segs:
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        if L < 1e-6:
            continue
        # normal; choose landward using the site's terrain gradient
        nx, ny = -dy / L, dx / L
        mx, my = (ax + bx) / 2, (ay + by) / 2
        eps = 1.0
        gx = _grad_x(mx, my)
        gy = _grad_y(mx, my)
        if nx * gx + ny * gy < 0:
            nx, ny = -nx, -ny
        p_in = (mx + nx * width_land, my + ny * width_land)
        p_out = (mx - nx * width_sea, my - ny * width_sea)
        quads.append((p_in, p_out))
    return quads


_GRAD_SITE = None


def _grad_x(x, y):
    s = _GRAD_SITE
    e = 1.5
    return (height_at(s, x + e, y) - height_at(s, x - e, y)) / (2 * e)


def _grad_y(x, y):
    s = _GRAD_SITE
    e = 1.5
    return (height_at(s, x, y + e) - height_at(s, x, y - e)) / (2 * e)


def set_grad_site(site):
    global _GRAD_SITE
    _GRAD_SITE = site


# ---------------------------------------------------------------------------
# safe water spot for hulls
# ---------------------------------------------------------------------------
def hull_footprint(x, y, length, width, rot):
    """Sample points around a hull rectangle in world coordinates."""
    c, s = math.cos(rot), math.sin(rot)
    pts = []
    for lx, ly in [(-length / 2, 0), (length / 2, 0), (0, -width / 2), (0, width / 2),
                   (-length / 2, -width / 2), (-length / 2, width / 2),
                   (length / 2, -width / 2), (length / 2, width / 2),
                   (-length / 4, 0), (length / 4, 0)]:
        pts.append((x + lx * c - ly * s, y + lx * s + ly * c))
    return pts


def find_water_spot(site, cx, cy, length, width, rot, clear=1.25, max_radius=46.0,
                    step=4.0):
    """Nearest point to (cx, cy) where the whole hull footprint has clearance."""
    best = None
    r = 0.0
    while r <= max_radius:
        n = max(1, int(r / step) * 8)
        for k in range(n):
            a = 2 * math.pi * k / n
            x = cx + math.cos(a) * r
            y = cy + math.sin(a) * r
            hs = [height_at(site, px, py) for px, py in
                  hull_footprint(x, y, length, width, rot)]
            if max(hs) <= -clear:
                score = r + 0.15 * min(hs)
                if best is None or score < best[0]:
                    best = (score, x, y, max(hs), min(hs))
        if best is not None and r >= 8.0:
            break
        r += step
    if best is None:
        # relax: prefer the deepest spot within reach
        for k in range(48):
            a = 2 * math.pi * k / 48
            x = cx + math.cos(a) * max_radius
            y = cy + math.sin(a) * max_radius
            hs = [height_at(site, px, py) for px, py in
                  hull_footprint(x, y, length, width, rot)]
            if max(hs) < 0:
                return (x, y, max(hs), min(hs), False)
        return (cx, cy, height_at(site, cx, cy), None, False)
    return (best[1], best[2], best[3], best[4], True)


def find_shore_point(site, near, direction, max_r=40.0, z_lo=0.15, z_hi=0.85):
    """Walk along a direction to find where the shore sits near the target."""
    dx, dy = direction
    L = math.hypot(dx, dy) or 1.0
    dx, dy = dx / L, dy / L
    best = None
    for t in np.arange(0.0, max_r, 1.0):
        x, y = near[0] + dx * t, near[1] + dy * t
        h = height_at(site, x, y)
        if z_lo <= h <= z_hi:
            return (x, y, h)
        if best is None or abs(h - 0.45) < abs(best[2] - 0.45):
            best = (x, y, h)
    return best









