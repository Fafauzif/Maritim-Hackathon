"""Scene faces S1-S8, documentary treatment. Each draw(c, t, tl) paints one flat face in its own coords."""
import json, math, os
import numpy as np
import skia
from gfx import *

TEAM_NAME = '[Team name]'
INSTITUTION = '[Institution]'
NAMES = ['Daniel Ferdiansyah', 'Daniel Angger', 'Salwa Alifia', 'Fauzi Fadhlurohman']
MEMBERS = ' · '.join(NAMES)
TEAM_DIR = f'{ROOT}/assets/team'          # drop 01.jpg … 04.jpg here; empty slots render as frames

ART = f'{ROOT}/../3d-art/revision-v2/delivery/LAUTARA_3D_Art_Handoff_v2/media'
DEPTH = json.load(open(f'{ROOT}/../LAUTARA_Master/05_Reproducibility/Depth_case_verified.json'))
EX = DEPTH['example']
SURF, DEEP = EX['0.494'], EX['9.573']
assert DEPTH['eastward_component_sign_surface_then_deeper']['W / E'] == 96 and DEPTH['days'] == 274

def kicker(c, s, x, y, a, color=ECHO):
    text(c, s, x, y, 15, 'semi', color, a, track=3.0)

def heading(c, kick, title, t, t0, x=110, y=120, a_out=None):
    kicker(c, kick, x, y, lin(t, t0, 0.6))
    text(c, title, x, y + 62, 46, 'light', T1, lin(t, t0 + 0.3, 1.0))
    c.drawLine(x, y + 92, x + 64 * eout(lin(t, t0 + 0.5, 0.8)), y + 92, paint(ECHO, 0.8, stroke=1.2, cap_round=False))

def reading(c, label, value, x, y, a, vsize=34, vcol=T1, vkind='light'):
    text(c, label, x, y, 13, 'med', T3, a)
    text(c, value, x, y + vsize + 8, vsize, vkind, vcol, a)

# ---------- map data ----------
_geo = None
def countries():
    global _geo
    if _geo is None:
        _geo = json.load(open(f'{ROOT}/assets/countries50.geojson'))['features']
    return _geo

_paths = {}
def map_paths(key, proj, bbox):
    if key in _paths:
        return _paths[key]
    out = []
    lo0, la0, lo1, la1 = bbox
    for f in countries():
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        p = skia.Path(); hit = False
        for poly in polys:
            ring = np.asarray(poly[0])
            if ring[:, 0].max() < lo0 or ring[:, 0].min() > lo1 or ring[:, 1].max() < la0 or ring[:, 1].min() > la1:
                continue
            hit = True
            xy = [proj(x, y) for x, y in ring]
            p.moveTo(*xy[0])
            for q in xy[1:]:
                p.lineTo(*q)
            p.close()
        if hit:
            out.append((f['properties']['ADMIN'], p))
    _paths[key] = out
    return out

def draw_map(c, key, proj, bbox, k, focus=('Indonesia',), focus2=(), W_=1920):
    """Coastlines appear where a vertical scan has passed (k = scan progress across the face)."""
    if k <= 0:
        return
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, W_ * eio(k), 1080))
    for name, p in map_paths(key, proj, bbox):
        if name in focus or name in focus2:
            c.drawPath(p, paint('#0A1119', 1))
            c.drawPath(p, paint(ECHO, 0.62, stroke=1.1))
        else:
            c.drawPath(p, paint('#06090D', 1))
            c.drawPath(p, paint(T3, 0.22, stroke=0.8))
    c.restore()
    if k < 1:
        xe = W_ * eio(k)
        c.drawLine(xe, 0, xe, 1080, paint(ECHO, 0.35, stroke=12, blur=10))
        c.drawLine(xe, 0, xe, 1080, paint(SCAN, 0.9, stroke=1.2, cap_round=False))

def graticule(c, proj, lons, lats, a):
    p = paint(HAIR, a * 0.8, stroke=1, cap_round=False)
    for lo in lons:
        x0, y0 = proj(lo, lats[0]); x1, y1 = proj(lo, lats[-1]); c.drawLine(x0, y0, x1, y1, p)
    for la in lats:
        x0, y0 = proj(lons[0], la); x1, y1 = proj(lons[-1], la); c.drawLine(x0, y0, x1, y1, p)

def pin(c, x, y, label, sub, t, t0, side='right', warm=False):
    a = lin(t, t0, 0.5)
    if a <= 0:
        return
    col = WARM if warm else ECHO
    ping(c, x, y, t, t0, R=160, dur=1.6, color=col, rings=2)
    c.drawCircle(x, y, 3.4, paint(col, 1))
    c.drawCircle(x, y, 11, paint(col, 0.8, stroke=1.2))
    dx = 70 if side == 'right' else -70
    lx = x + dx
    leader(c, x + (12 if side == 'right' else -12), y - 8, lx, y - 34, a)
    al = 'left' if side == 'right' else 'right'
    text(c, label, lx + (6 if side == 'right' else -6), y - 38, 22, 'med', T1, lin(t, t0 + 0.2, 0.7), al)
    text(c, sub.upper(), lx + (6 if side == 'right' else -6), y - 14, 12, 'med', T3, lin(t, t0 + 0.4, 0.7), al)

# =====================================================================
def team_slot(c, i, x, y, w, h, a, t):
    if a <= 0:
        return
    fn = f'{TEAM_DIR}/{i + 1:02d}.jpg'
    if os.path.exists(fn):
        import cv2
        im = cv2.imread(fn); ih, iw = im.shape[:2]
        s = max(w * 2 / iw, h * 2 / ih)
        cw, ch = int(w * 2 / s), int(h * 2 / s)
        x0, y0 = (iw - cw) // 2, max(0, (ih - ch) // 3)
        img = image(fn, crop=(x0, y0, x0 + cw, y0 + ch), grade='desat')
        draw_image(c, img, x, y, w, h, a, scan='y')
    else:
        k = eio(a)
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h * k), paint(PLATE, 0.9))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h * k))
        for gx in range(1, 4):
            c.drawLine(x + w * gx / 4, y, x + w * gx / 4, y + h, paint(HAIR, 0.6, stroke=1, cap_round=False))
        cx, cy = x + w / 2, y + h * 0.42
        c.drawCircle(cx, cy, w * 0.17, paint(T3, 0.5, stroke=1))
        c.drawArc(skia.Rect.MakeXYWH(cx - w * 0.32, cy + w * 0.22, w * 0.64, w * 0.6), 180, 180, False, paint(T3, 0.5, stroke=1))
        text(c, f'PHOTO {i + 1:02d}', cx, y + h - 16, 11, 'med', T3, 1.0, 'center')
        c.restore()
        if k < 1:
            c.drawLine(x, y + h * k, x + w, y + h * k, paint(SCAN, 0.9, stroke=1.2, cap_round=False))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(ECHO, 0.35 * eout(a), stroke=1))
    ticks(c, x - 6, y - 6, w + 12, h + 12, ECHO, 0.7 * eout(a), L=10)

def s1(c, t, tl):
    T, D = tl['T'], tl['D']
    nx, ny = 1035, 930            # proposed station, by the jetty
    # radial ping from the station reveals the coast (black means not yet seen)
    k = lin(t, 0.25, 5.0)
    R = 40 + 2300 * eout(k)
    img = image(f'{ART}/coasts/kodingareng/godview.png', grade='cold_dark')
    if k > 0:
        c.save()
        cp = skia.Path(); cp.addCircle(nx, ny, R)
        c.clipPath(cp, skia.ClipOp.kIntersect, True)
        c.drawImageRect(img, skia.Rect.MakeXYWH(0, 0, 1920, 1080), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), skia.Paint())
        # echo geometry over the freshly scanned water
        for i in range(1, 14):
            rr = i * 150
            if rr < R:
                c.drawCircle(nx, ny, rr, paint(ECHO, 0.10 * (1 - rr / 2300), stroke=1))
        c.restore()
        if k < 1:
            c.drawCircle(nx, ny, R, paint(ECHO, 0.35, stroke=14, blur=10))
            c.drawCircle(nx, ny, R, paint(SCAN, 0.9, stroke=1.5))
    for t0 in (0.25, 2.2, 4.1):
        ping(c, nx, ny, t, t0, R=700, dur=2.6, color=WARM if t0 == 0.25 else ECHO, a=0.8)
    if t > 0.2:
        node(c, nx, ny, 16, lin(t, 0.2, 0.3), t=t)
    a = lin(t, 2.0, 0.7)
    leader(c, nx + 14, ny - 12, nx + 80, ny - 60, a)
    text(c, 'S-01 · PROPOSED STATION', nx + 88, ny - 64, 13, 'med', WARM, lin(t, 2.2, 0.8))
    text(c, '5.155° S  119.262° E · ILLUSTRATIVE', nx + 88, ny - 42, 12, 'med', T3, lin(t, 2.5, 0.8))

    # title, top left, never centred
    tt = T['s1b'] + 4.3
    x0 = 110
    kicker(c, 'LAUTARA 2026 · RUSSIA–INDONESIA MARITIME HACKATHON', x0, 150, lin(t, tt - 0.2, 0.9))
    text(c, 'The Ocean Has Floors', x0, 250, 84, 'thin', T1, lin(t, tt, 1.4), track=-0.5)
    kr = eout(lin(t, tt + 0.6, 1.0))
    c.drawLine(x0, 290, x0 + 120 * kr, 290, paint(ECHO, 0.9, stroke=1.4, cap_round=False))
    text(c, 'KODINGARENG LOMPO · SOUTH SULAWESI · 5°08′ S  119°16′ E', x0, 324, 13, 'med', T3, lin(t, tt + 0.9, 1.0))
    tb = T['s1c'] + 6.4
    text(c, 'Blind spots in time.', x0, 400, 36, 'light', T2, lin(t, tb, 0.9))
    text(c, 'Blind spots in depth.', x0, 448, 36, 'light', ECHO, lin(t, tb + 1.1, 0.9))

    # the team: four photo slots, each written on as the name is spoken
    seg = "We are Daniel Ferdiansyah, Daniel Angger, Salwa Alifia and Fauzi Fadhlurohman. This is The Ocean Has Floors."
    sw, sh, gap = 190, 238, 24
    xs0 = 110
    ys = 560
    for i, nm in enumerate(NAMES):
        tn = T['s1b'] + D['s1b'] * seg.index(nm.split()[0] if i != 1 else 'Daniel Angger') / len(seg) - 0.25
        x = xs0 + i * (sw + gap)
        team_slot(c, i, x, ys, sw, sh, lin(t, tn, 0.7), t)
        text(c, nm, x, ys + sh + 34, 17, 'med', T1, lin(t, tn + 0.3, 0.8))
        text(c, f'MEMBER {i + 1:02d}', x, ys + sh + 56, 11, 'semi', T3, lin(t, tn + 0.5, 0.8))
    text(c, f'{TEAM_NAME} · {INSTITUTION}'.upper(), xs0, ys + sh + 96, 13, 'semi', ECHO, lin(t, T['s1b'] + 3.6, 1.0))

    # the line leaves along the title rule toward the next station
    out = [(x0 + 120, 290), (1000, 290), (1000, 560), (1920, 560)]
    line(c, out, eio(lin(t, tb + 2.4, 1.6)), a=1.0)

# =====================================================================
S2_BBOX = (92, -13, 144, 9)
def s2_proj(lon, lat):
    return 70 + (lon - 94) * 36.0, 330 + (7 - lat) * 36.0

TUNDA, KODI, AMUR = (106.275, -5.81), (119.27, -5.135), (131.95, 43.25)

def s2(c, t, tl):
    T = tl['T']; t0 = tl['start']['S2']
    graticule(c, s2_proj, list(range(95, 145, 5)), list(range(-10, 10, 5)), lin(t, t0, 1.0))
    draw_map(c, 's2', s2_proj, S2_BBOX, lin(t, t0 - 0.3, 2.6))
    source_tag(c, 'MAP · NATURAL EARTH', 1810, 1040, lin(t, t0 + 2, 0.8), 'right', size=12)
    # the global figure, as a reading
    tc = T['s2a'] + 1.0
    kicker(c, 'SAND AND SEDIMENT DREDGED FROM SEAS AND COASTS', 110, 120, lin(t, tc - 0.6, 0.8))
    kv = eout(lin(t, tc, 1.8))
    lo, hi = 4 * kv, 8 * kv
    text(c, f'{lo:.0f}–{hi:.0f}', 104, 250, 128, 'thin', T1, lin(t, tc - 0.2, 0.6), track=-2)
    bx = 104 + text_width('4–8', 128, 'thin', -2) + 36
    text(c, 'billion tonnes a year', bx, 210, 36, 'light', T1, lin(t, tc + 0.4, 1.0))
    text(c, 'estimated, worldwide', bx, 252, 22, 'reg', T3, lin(t, tc + 0.8, 1.0))
    kb = lin(t, T['s2b'] + 0.3, 0.8)
    chip(c, 110, 290, 'UNEP estimate · all marine dredging, not only illegal mining', PLATE, None, T2, kb)
    kq = T['s2c'] + 2.6
    text(c, 'Where did the fine sediment go,', 1810, 250, 34, 'light', T1, lin(t, kq, 1.0), 'right')
    text(c, 'and how deep?', 1810, 296, 34, 'light', ECHO, lin(t, kq + 0.9, 0.8), 'right')
    tx, ty = s2_proj(*TUNDA); kx, ky = s2_proj(*KODI)
    pin(c, tx, ty, 'Pulau Tunda', 'Banten', t, T['s2d'] + 2.4, 'left')
    pin(c, kx, ky, 'Kodingareng Lompo', 'off Makassar · South Sulawesi', t, T['s2d'] + 4.0)
    entry = [(0, 560), (110, 560), (110, 400)]
    line(c, entry, eio(lin(t, t0 + 0.1, 1.2)), a=1.0, head=False)
    arc = bezier((110, 400), (300, 420), (tx - 60, ty - 160), (tx, ty - 12), 40) + \
        bezier((tx, ty - 12), (tx + 200, ty - 200), (kx - 220, ky - 210), (kx, ky - 12), 60)
    line(c, arc, eio(lin(t, T['s2d'] + 2.0, 2.6)))
    out = bezier((kx, ky - 12), (kx + 260, ky - 120), (1700, 520), (1920, 480), 40)
    line(c, out, eio(lin(t, tl['end']['S2'] - 1.0, 1.0)), head=False)

# =====================================================================
def tile(c, x, y, w, h, kind, a, label=None, sub=None, lift=None, r=None):
    if a <= 0.003:
        return
    k = eout(a)
    if kind == 'lit':
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(ECHO, 0.16 * k))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(ECHO, 0.35 * k, stroke=6, blur=5))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(ECHO, k, stroke=1.3))
        fg = T1
    elif kind == 'dim':
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint('#2A3946', k))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint('#3E4E5C', k, stroke=1))
        fg = T3
    else:
        hatch(c, x, y, w, h, '#7C8896', k * 0.8, gap=10 if w > 80 else 8)
        fg = T3
    if label:
        text(c, label, x + 20, y + 44, 24, 'light', fg, a)
    if sub:
        text(c, sub.upper(), x + 20, y + h - 22, 11, 'med', fg, a)

def s3(c, t, tl):
    T = tl['T']; t0 = tl['start']['S3']
    spine = [(0, 560), (60, 560)] + [(60, y) for y in range(560, 3241, 40)]
    sp = mix(0.0, 0.28, eio(lin(t, t0, 2.0)))
    sp = max(sp, mix(0.28, 0.62, eio(lin(t, T['s3d'] - 0.8, 1.4))))
    sp = max(sp, mix(0.62, 1.0, eio(lin(t, T['s3e'] - 0.8, 1.4))))
    line(c, spine, sp)
    # ---- part A: one inspection, no image of the day
    heading(c, 'BLIND SPOT IN TIME', 'One inspection. No image of the day.', t, T['s3a'] - 0.2)
    ty, tw, th = 520, 360, 230
    xs = (300, 760, 1220)
    tA = T['s3c']
    tile(c, xs[0], ty, tw, th, 'lit', lin(t, tA + 2.6, 0.6), '26 Oct 2023', 'scene acquired')
    tile(c, xs[2], ty, tw, th, 'lit', lin(t, tA + 4.0, 0.6), '31 Oct 2023', 'scene acquired')
    tile(c, xs[1], ty, tw, th, 'missing', lin(t, tA + 5.9, 0.9), '27 Oct 2023', 'no scene in the archive searched')
    km = lin(t, T['s3b'] + 2.0, 0.6)
    if km > 0:
        mx = xs[1] + tw / 2
        c.drawLine(mx, ty - 150, mx, ty - 150 + 140 * eout(km), paint(WARM, 0.8, stroke=1, cap_round=False))
        node(c, mx, ty - 150, 14, km, t=t)
        text(c, 'KKP INSPECTION · 27 OCT 2023', mx + 26, ty - 160, 14, 'semi', WARM, lin(t, T['s3b'] + 2.3, 0.8))
        text(c, 'linked to a suspected source near Tunda', mx + 26, ty - 134, 18, 'reg', T2, lin(t, T['s3b'] + 2.7, 0.9))
    br = [(60, 380), (xs[0] + tw / 2, 380), (xs[0] + tw / 2, ty)]
    line(c, br, eio(lin(t, tA + 2.2, 1.0)))
    bridge = bezier((xs[0] + tw, ty + 60), (xs[0] + tw + 120, ty + 60), (xs[2] - 120, ty + 60), (xs[2], ty + 60), 30)
    line(c, bridge, eio(lin(t, tA + 4.2, 1.2)), head=False)
    ka = lin(t, tA + 6.4, 0.8)
    w_ = label_tag(c, 'MEASURED · catalog search', 300, 830, ka)
    source_tag(c, 'Sentinel-1, Sentinel-2 and Landsat 8/9 catalogs over the study footprint · KKP release, 29 Oct 2023', 300 + w_ + 18, 850, ka)
    # ---- part B: wet season
    yb = 1080
    heading(c, 'WET SEASON · NOV 2025 – FEB 2026', 'A clear view of the water, almost never.', t, T['s3d'] - 0.4, y=yb + 120)
    rows = (('Pulau Tunda', 27, 13, yb + 420, T['s3d'] + 4.2), ('Kodingareng Lompo', 28, None, yb + 640, T['s3d'] + 9.4))
    for name, n, lit, y, ts in rows:
        text(c, name, 110, y - 30, 22, 'med', T1, lin(t, ts - 0.6, 0.7))
        text(c, f'{n} SATELLITE DATES', 110, y - 8 + 64, 11, 'med', T3, lin(t, ts, 0.7))
        sz, gap = 36, 9
        for i in range(n):
            tile(c, 400 + i * (sz + gap), y - 30, sz, sz, 'lit' if i == lit else 'dim', lin(t, ts + i * 0.05, 0.25))
        kk = clamp(lin(t, ts, n * 0.05 + 0.3))
        shown = (1 if lit is not None and kk * n > lit else 0)
        text(c, f'{shown}/{n}', 1810, y + 6, 64, 'thin', ECHO if shown else T1, lin(t, ts - 0.3, 0.6), 'right')
    kb = lin(t, T['s3d'] + 4.0, 0.8)
    w_ = label_tag(c, 'MEASURED · satellite screen', 110, yb + 820, kb)
    source_tag(c, 'Sentinel-2 dates passing a water-only screen: at least 90% of a 1.5–3 km ring around the island clear', 110 + w_ + 18, yb + 840, kb)
    # ---- part C: rainy days
    yc = 2160
    heading(c, 'RAINY DAYS · NOV – DEC 2025 · BOTH ISLANDS', 'When runoff matters most.', t, T['s3e'] - 0.5, y=yc + 120)
    ts = T['s3e'] + 0.6
    rng = np.random.default_rng(11)
    kinds = ['missing'] * 49 + ['dim'] * 22
    rng.shuffle(kinds)
    kinds.insert(41, 'lit')
    cols, sz, gap = 18, 58, 12
    for i, kd in enumerate(kinds):
        x = 110 + (i % cols) * (sz + gap); y = yc + 330 + (i // cols) * (sz + gap)
        tile(c, x, y, sz, sz, kd, lin(t, ts + i * 0.03, 0.25))
    kk = clamp(lin(t, ts, 72 * 0.03))
    text(c, f'{1 if kk > 42 / 72 else 0}/72', 1810, yc + 420, 120, 'thin', ECHO, lin(t, ts, 0.6), 'right')
    text(c, 'RAINY SITE-DAYS WITH A USABLE VIEW', 1810, yc + 460, 12, 'med', T3, lin(t, ts + 0.4, 0.8), 'right')
    kl = ts + 2.4
    lx = 1400
    for j, (kd, lab) in enumerate((('lit', 'usable view · 1'), ('dim', 'image failed the screen · 22'), ('missing', 'no image acquired · 49'))):
        yy = yc + 540 + j * 44
        tile(c, lx, yy - 18, 22, 22, kd, lin(t, kl + j * 0.2, 0.4))
        text(c, lab.upper(), lx + 38, yy, 13, 'med', T2, lin(t, kl + j * 0.2, 0.8))
    kq = lin(t, kl, 0.8)
    w_ = label_tag(c, 'MEASURED · rain + satellite record', 110, yc + 650, kq)
    source_tag(c, 'Site-days with ≥10 mm regional IMERG rain · Sentinel-2 + Landsat 8/9 broad quality screen', 110, yc + 710, kq)

# =====================================================================
S4_STATION = (1660, 520)
S4_AB = 520

def bearing_vec(b):
    r = math.radians(b)
    return math.sin(r), -math.cos(r)

def s4(c, t, tl, clip_k=0.0):
    T = tl['T']; t0 = tl['start']['S4']
    if clip_k > 0:
        c.save(); c.clipRect(skia.Rect.MakeLTRB(-10, -10, 1930, mix(1090, S4_AB, clip_k)))
    img = image(f'{ART}/coasts/kodingareng/mapview.png', grade='cold')
    draw_image(c, img, 0, 0, 1920, 1080, lin(t, t0 - 1.2, 2.4), scan='y')
    # survey grid over the overhead view
    gp = paint(ECHO, 0.07 * lin(t, t0, 1.0), stroke=1, cap_round=False)
    for gx in range(0, 1921, 120):
        c.drawLine(gx, 0, gx, 1080, gp)
    for gy in range(0, 1081, 120):
        c.drawLine(0, gy, 1920, gy, gp)
    kc = lin(t, T['s4b'] + 1.0, 0.8)
    ticks(c, 40, 40, 1840, 1000, ECHO, 0.8 * eout(kc), L=60)
    text(c, 'ONE ~9 KM MODEL CELL COVERS THIS WHOLE VIEW', 1860, 1012, 13, 'semi', ECHO, kc, 'right')
    sx, sy = S4_STATION
    path = [(60, 0), (60, 140)] + bezier((60, 140), (60, 420), (sx - 520, sy), (sx - 180, sy), 50)
    line(c, path, eio(lin(t, t0 - 0.6, 2.4)))
    # the dial: an instrument beside its object
    tsl = T['s4c'] + 2.6
    ks = eio(lin(t, tsl, 2.2))
    b0, b1 = float(SURF['towards_deg']), float(DEEP['towards_deg']) + 360
    b = mix(b0, b1, ks)
    sp = mix(float(SURF['speed_m_s']), float(DEEP['speed_m_s']), ks)
    ad = lin(t, T['s4b'] + 3.5, 0.9)
    if ad > 0:
        R = 160
        c.drawCircle(sx, sy, R + 40, paint(PLATE, 0.55 * eout(ad)))
        c.drawArc(skia.Rect.MakeXYWH(sx - R, sy - R, 2 * R, 2 * R), -90, 360 * eout(ad), False, paint(ECHO, 0.9, stroke=1.3))
        for d in range(0, 360, 10):
            vx, vy = bearing_vec(d)
            L = 14 if d % 90 == 0 else (8 if d % 30 == 0 else 4)
            c.drawLine(sx + vx * R, sy + vy * R, sx + vx * (R - L), sy + vy * (R - L), paint(ECHO, 0.7 * eout(ad), stroke=1, cap_round=False))
        for d, lab in ((0, 'N'), (90, 'E'), (180, 'S'), (270, 'W')):
            vx, vy = bearing_vec(d)
            text(c, lab, sx + vx * (R + 22), sy + vy * (R + 22) + 5, 13, 'semi', T3, ad, 'center')
        vx, vy = bearing_vec(b)
        tip = (sx + vx * (R - 22), sy + vy * (R - 22))
        c.drawLine(sx, sy, *tip, paint(ECHO, 0.4 * eout(ad), stroke=8, blur=5))
        c.drawLine(sx, sy, *tip, paint(SCAN, eout(ad), stroke=2.2))
        px, py = -vy, vx
        hp = skia.Path()
        hp.moveTo(tip[0] + vx * 12, tip[1] + vy * 12)
        hp.lineTo(tip[0] + px * 9, tip[1] + py * 9)
        hp.lineTo(tip[0] - px * 9, tip[1] - py * 9)
        hp.close()
        c.drawPath(hp, paint(SCAN, eout(ad)))
        # bearing arc from north to the current heading
        c.drawArc(skia.Rect.MakeXYWH(sx - R + 30, sy - R + 30, 2 * R - 60, 2 * R - 60), -90, (b % 360), False, paint(ECHO, 0.35 * eout(ad), stroke=1))
        node(c, sx, sy, 12, ad, t=t)
        text(c, 'S-01 · ILLUSTRATIVE STATION', sx, sy + R + 52, 12, 'semi', WARM, lin(t, T['s4b'] + 4.0, 0.8), 'center')
    # left plate: depth slider and readings
    ka = lin(t, T['s4b'] - 0.2, 0.8)
    if ka > 0:
        chunk(c, 110, 220, 500, 620, PLATE, None, eout(ka))
        kicker(c, 'VIEWING DEPTH', 150, 272, ka)
        trk = (170, 330, 660)
        c.drawLine(trk[0], trk[1], trk[0], trk[2], paint(HAIR, 1, stroke=1.5, cap_round=False))
        c.drawLine(trk[0], trk[1], trk[0], mix(trk[1], trk[2], ks), paint(ECHO, 1, stroke=2, cap_round=False))
        for yy, lab in ((trk[1], '0.5 M'), (trk[2], '9.6 M')):
            c.drawLine(trk[0] - 8, yy, trk[0] + 8, yy, paint(T3, 1, stroke=1, cap_round=False))
            text(c, lab, trk[0] + 20, yy + 5, 12, 'med', T3, ka)
        hy = mix(trk[1], trk[2], ks)
        c.drawRect(skia.Rect.MakeXYWH(trk[0] - 9, hy - 5, 18, 10), paint(WARM, eout(ka)))
        dm = mix(0.494, 9.573, ks)
        dir_lab = 'TOWARD WEST' if ks < 0.5 else 'TOWARD NORTHEAST'
        text(c, f'{dm:.1f} m', 260, 420, 88, 'thin', T1, ka, track=-1)
        reading(c, 'MODELLED CURRENT · DAILY MEAN', f'{sp:.3f} m/s', 264, 480, ka, 34, ECHO)
        reading(c, 'BEARING', f'{b % 360:05.1f}°', 264, 576, ka, 34, ECHO)
        text(c, dir_lab, 264, 650, 13, 'semi', ECHO, ka)
        w_ = label_tag(c, 'MODELLED', 150, 770, ka)
        source_tag(c, 'Copernicus GLORYS12', 150 + w_ + 14, 790, ka)
    heading(c, 'BLIND SPOT IN DEPTH', 'Satellites see the surface.', t, T['s4a'] - 0.4, x=110, y=110)
    chip(c, 1810, 96, '16 Apr 2020 · UTC', PLATE, None, T1, lin(t, T['s4b'] + 0.5, 0.8), align='right', dot=ECHO)
    kf = lin(t, T['s4d'] + 0.8, 0.8)
    if kf > 0:
        chunk(c, 660, 870, 900, 120, PLATE, None, eout(kf))
        text(c, '96/274', 700, 950, 64, 'thin', ECHO, kf, track=-1)
        text(c, 'DAYS, FEB–OCT 2020', 960, 920, 13, 'semi', T3, kf)
        text(c, 'surface heading west, deeper layer heading east', 960, 952, 21, 'reg', T1, lin(t, T['s4d'] + 1.2, 1.0))
        k96 = eout(lin(t, T['s4d'] + 1.2, 1.4))
        c.drawLine(960, 968, 1520, 968, paint(HAIR, 1, stroke=3, cap_round=False))
        c.drawLine(960, 968, 960 + 560 * 96 / 274 * k96, 968, paint(ECHO, 1, stroke=3, cap_round=False))
    source_tag(c, 'MODELLED · Copernicus GLORYS12 daily mean · cell centre 5.1667° S, 119.25° E · scene art illustrative', 110, 1050, lin(t, t0 + 1, 1.0), size=12)
    if clip_k > 0:
        c.restore()

# =====================================================================
WATER_Y = 471
def s5(c, t, tl):
    T = tl['T']; t0 = tl['start']['S5']
    img = image(f'{ART}/coasts/kodingareng/section.png', grade='cold')
    c.drawImageRect(img, skia.Rect.MakeXYWH(0, 0, 1920, 1080), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), skia.Paint())
    c.drawLine(0, WATER_Y, 1920, WATER_Y, paint(ECHO, 0.35, stroke=1, cap_round=False))
    text(c, 'B', 40, WATER_Y - 24, 28, 'light', T2, 1.0)
    text(c, 'A', 1880, WATER_Y - 24, 28, 'light', T2, 1.0, 'right')
    kicker(c, 'THE OCEAN HAS FLOORS · PROPOSED WORKSPACE', 110, 110, lin(t, T['s5a'], 0.8))
    text(c, 'Section A–B through S-01', 110, 172, 46, 'light', T1, lin(t, T['s5a'] + 0.3, 1.0))
    bx = 1500
    node(c, bx, WATER_Y, 12, lin(t, t0, 0.4), t=t)
    kd = eout(lin(t, T['s5b'] + 8.6, 1.4))
    if kd > 0:
        yd = mix(WATER_Y, 760, kd)
        c.drawLine(bx, WATER_Y + 8, bx, yd, paint(WARM, 0.9, stroke=1.3, cap_round=False))
        for yy in range(WATER_Y + 40, int(yd), 40):
            c.drawLine(bx - 6, yy, bx + 6, yy, paint(WARM, 0.6, stroke=1, cap_round=False))
        c.drawRect(skia.Rect.MakeXYWH(bx - 7, yd - 7, 14, 14), paint(WARM, 1))
        a = lin(t, T['s5b'] + 9.6, 0.8)
        leader(c, bx + 12, yd, bx + 60, yd, a)
        text(c, 'PROPOSED SAMPLE DEPTH', bx + 70, yd - 8, 12, 'semi', T3, a)
        text(c, '9.6 m', bx + 70, yd + 30, 34, 'light', WARM, a)
    kc = T['s5c']
    label_tag(c, 'MODELLED · current at 9.6 m', 110, 240, lin(t, kc + 0.6, 0.6))
    label_tag(c, 'MEASURED · awaiting field data', 110, 288, lin(t, kc + 1.5, 0.6))
    pm = lin(t, kc + 2.4, 0.6)
    chip(c, 110, 336, 'MISSING · local current profile', PLATE, None, T2, pm, size=14, kind='semi', pad=12, hatched=True)
    td = T['s5d']
    kb = lin(t, td + 0.2, 0.6)
    press = clamp(lin(t, td + 1.3, 0.25))
    bw = chip(c, 1810, 880, '+ Request field check', WARM, None, WARM, kb, size=16, kind='semi', align='right')
    if 0 < press < 1:
        c.drawRect(skia.Rect.MakeXYWH(1810 - bw, 880, bw, 33.6), paint(WARM, 0.35 * (1 - press)))
    cx, cy, cw, ch = 690, 210, 720, 700
    kl = lin(t, td + 1.6, 0.8)
    line(c, bezier((1810 - bw, 897), (1500, 897), (1500, 560), (cx + cw, 560), 50), eio(kl), color=WARM, a=1.0)
    ak = lin(t, td + 2.0, 0.6)
    if ak > 0:
        chunk(c, cx, cy, cw, ch * eout(ak), PLATE, None, 1.0)
        kicker(c, 'FIELD BRIEF · DRAFT FOR REVIEW', cx + 40, cy + 54, lin(t, td + 2.2, 0.8), WARM)
        text(c, 'KR-01 Kodingareng baseline survey', cx + 40, cy + 108, 32, 'light', T1, lin(t, td + 2.4, 1.0))
        rows = [('Station', 'S-01 · illustrative waypoint'), ('When', 'Pre-work visit · 08:00–10:00 WITA'),
                ('Current check', 'Profiler at S-01 · 0.5 m and 9.6 m'), ('Sediment baseline', 'Paired water bottles at both depths'),
                ('Review and return', 'Supervisor signs · results return to KR-01')]
        for i, (k_, v_) in enumerate(rows):
            ar = lin(t, td + 2.6 + i * 0.5, 0.7)
            yy = cy + 180 + i * 84
            c.drawLine(cx + 40, yy - 32, cx + 40 + (cw - 80) * eout(ar), yy - 32, paint(HAIR, 1, stroke=1, cap_round=False))
            text(c, k_.upper(), cx + 40, yy, 12, 'semi', T3, ar)
            text(c, v_, cx + 40, yy + 32, 23, 'reg', T1, ar)
        kt = lin(t, td + 6.6, 0.6)
        if kt > 0:
            yy = cy + ch - 70
            p = skia.Path(); p.moveTo(cx + 44, yy); p.lineTo(cx + 54, yy + 10); p.lineTo(cx + 72, yy - 10)
            pm2 = skia.PathMeasure(p, False); sg = skia.Path(); pm2.getSegment(0, pm2.getLength() * eout(kt), sg, True)
            c.drawPath(sg, paint(ECHO, 1, stroke=2))
            text(c, 'REVIEWED · VERSION 1', cx + 88, yy + 6, 14, 'semi', ECHO, kt)
        kr = lin(t, T['s5e'] + 1.6, 0.6)
        label_tag(c, 'MEASURED · attached', cx + 380, cy + ch - 90, kr)
    te = T['s5e']
    kr = lin(t, te + 0.2, 1.8)
    if kr > 0:
        path = bezier((1500, WATER_Y - 20), (1500, 300), (1460, 230), (cx + cw, cy + 40), 50)
        line(c, path, eio(kr), color=T1, a=1.0)
        text(c, 'READINGS + SAMPLE IDS → KR-01', 1540, 300, 13, 'semi', T1, lin(t, te + 0.5, 0.8))
    label_tag(c, 'DESIGN CONCEPT · illustrative station and seabed · vertical exaggeration ×3.2', 110, 1000, 1.0)
    line(c, bezier((cx + 40, cy + ch), (cx + 40, 1100), (300, 1000), (-40, 1080), 40), eio(lin(t, tl['end']['S5'] - 1.0, 1.0)), head=False)

# =====================================================================
S6_BBOX = (88, -14, 152, 56)
def s6_proj(lon, lat):
    return 80 + (lon - 92) * 15.6, 1000 - (lat + 12) * 14.6

def s6(c, t, tl):
    T = tl['T']; t0 = tl['start']['S6']
    graticule(c, s6_proj, list(range(95, 150, 10)), list(range(-10, 56, 10)), lin(t, t0, 1.0))
    draw_map(c, 's6', s6_proj, S6_BBOX, lin(t, t0 - 0.6, 2.4), focus=('Indonesia',), focus2=('Russia',), W_=960)
    source_tag(c, 'MAP · NATURAL EARTH', 110, 1050, lin(t, t0 + 2, 0.8), size=12)
    pts = {n: s6_proj(*ll) for n, ll in (('tunda', TUNDA), ('kodi', KODI), ('amur', AMUR))}
    root = (900, 1120)
    tb = T['s6a'] + 0.4
    for i, (n, lab, sub, side) in enumerate((('tunda', 'Pulau Tunda', 'Indonesia', 'left'), ('kodi', 'Kodingareng Lompo', 'Indonesia', 'right'), ('amur', 'Amur Bay', 'Razdolnaya estuary · Russia', 'left'))):
        x, y = pts[n]
        ctrl = (x + 220, y + 320) if n == 'amur' else (x + 80, y + 170)
        br = bezier(root, (root[0] + 40, root[1] - 300), ctrl, (x, y + 14), 50)
        line(c, br, eio(lin(t, tb + i * 0.15, 1.6)))
        pin(c, x, y, lab, sub, t, tb + 1.2 + i * 0.15, side)
    tb2 = T['s6b']
    ki = lin(t, tb2 + 1.0, 1.2)
    if T['s6d'] + 0.2 < t:
        ki = 1 - lin(t, T['s6d'] + 0.2, 0.6)
    img = image(f'{ROOT}/assets/amur_optical_counterexample.png', crop=(1497, 122, 2720, 1196), grade='desat')
    if ki > 0:
        kicker(c, 'AMUR BAY · RAZDOLNAYA ESTUARY · RUSSIA', 1000, 96, ki)
        draw_image(c, img, 1000, 120, 520, 457, ki)
        c.drawRect(skia.Rect.MakeXYWH(1000, 120, 520, 457), paint(ECHO, 0.4 * eout(ki), stroke=1))
        text(c, '6 SEP 2023 · SENTINEL-2 TRUE COLOUR', 1000, 605, 12, 'semi', T2, ki)
        text_block(c, 'Landsat 9 imaged the same water eighteen minutes later.', 1560, 150, 24, 300, 'light', T1, ki)
        text_block(c, 'In both missions the west box was brighter in the red band than the east box.', 1560, 270, 18, 300, 'reg', T3, ki)
        text_block(c, 'Contains modified Copernicus Sentinel data 2023 · USGS Landsat 9 · team archive figure', 1560, 520, 12, 300, 'reg', T3, ki)
    kb = lin(t, tb2 + 5.5, 0.8)
    if T['s6d'] + 0.2 < t:
        kb = 1 - lin(t, T['s6d'] + 0.2, 0.6)
    bars = (('6 Sep · Sentinel-2', 0.0552, tb2 + 6.0), ('6 Sep · Landsat 9', 0.0646, tb2 + 6.6), ('12 Jul · Landsat · before the floods', 0.0961, T['s6c'] + 0.6))
    if kb > 0:
        kicker(c, 'WEST MINUS EAST RED REFLECTANCE', 1000, 680, kb, T2)
        label_tag(c, 'MEASURED', 1810 - text_width('MEASURED', 14, 'semi') - 42, 658, kb)
        for i, (lab, v, tv) in enumerate(bars):
            y = 730 + i * 70
            kv = eout(lin(t, tv, 1.0))
            av = min(kb, lin(t, tv - 0.2, 0.5))
            text(c, lab.upper(), 1000, y, 12, 'med', T3, av)
            c.drawLine(1000, y + 18, 1560, y + 18, paint(HAIR, av, stroke=8, cap_round=False))
            c.drawLine(1000, y + 18, 1000 + 560 * v / 0.1 * kv, y + 18, paint(ECHO if i < 2 else SCAN, av, stroke=8, cap_round=False))
            text(c, f'+{v * kv:.4f}', 1810, y + 26, 34, 'thin', T1, av, 'right')
    kq = lin(t, T['s6c'] + 2.8, 1.0)
    if T['s6d'] + 0.2 < t:
        kq = 1 - lin(t, T['s6d'] + 0.2, 0.6)
    text(c, 'Brightness alone does not prove dredging.', 1000, 990, 30, 'light', T1, kq)
    text(c, 'Rivers move sediment too.', 1000, 1030, 20, 'reg', T3, kq)
    ap = lin(t, T['s6d'] + 0.6, 0.8)
    if ap > 0:
        x0, y0 = 1000, 300
        chunk(c, x0, y0, 820, 440, PLATE, None, eout(ap))
        kicker(c, 'CASE PACKET · SAME EVIDENCE RULES', x0 + 44, y0 + 64, ap)
        rows = (('Indonesia', 'Kodingareng Lompo · Pulau Tunda'), ('Russia', 'Amur Bay · Razdolnaya estuary'))
        for i, (k_, v_) in enumerate(rows):
            yy = y0 + 140 + i * 74
            text(c, k_, x0 + 44, yy, 28, 'light', T1, lin(t, T['s6d'] + 0.9 + i * 0.3, 0.8))
            text(c, v_.upper(), x0 + 260, yy - 4, 13, 'med', T3, lin(t, T['s6d'] + 1.1 + i * 0.3, 0.8))
        text_block(c, 'Each team reviews the other’s case and records what it would change, and why.', x0 + 44, y0 + 320, 26, 720, 'light', ECHO, lin(t, T['s6d'] + 1.8, 1.4))
    line(c, bezier((1410, 740), (1410, 1000), (1700, 1080), (1920, 1060), 40), eio(lin(t, tl['end']['S6'] - 1.0, 1.0)), head=False)

# =====================================================================
def title_lockup(c, t, t0, x=160, y=520):
    kicker(c, 'LAUTARA 2026 · RUSSIA–INDONESIA MARITIME HACKATHON', x, y - 110, lin(t, t0 - 0.2, 0.9))
    text(c, 'The Ocean Has Floors', x, y, 104, 'thin', T1, lin(t, t0, 1.6), track=-0.5)
    k = eout(lin(t, t0 + 0.7, 1.0))
    c.drawLine(x, y + 46, x + 140 * k, y + 46, paint(ECHO, 0.9, stroke=1.4, cap_round=False))

def s7(c, t, tl):
    T = tl['T']
    x = 160
    tc = T['s7c']
    out = tc - 0.4
    a1 = lin(t, T['s7a'] + 0.2, 0.9) if t < out else 1 - lin(t, out, 0.5)
    text(c, 'The sea is not flat.', x, 330, 56, 'light', T1, a1)
    a2 = lin(t, T['s7a'] + 2.4, 0.9) if t < out else 1 - lin(t, out, 0.5)
    text(c, 'Neither is the evidence.', x, 400, 56, 'light', ECHO, a2)
    a3 = lin(t, T['s7b'] + 0.3, 1.4) if t < out else 1 - lin(t, out, 0.5)
    text(c, 'Young people can build the tools that show what we cannot yet see.', x, 480, 26, 'reg', T2, a3)
    a4 = lin(t, tc, 1.2) if t < tc + 4.4 else 1 - lin(t, tc + 4.4, 0.6)
    text(c, 'See further, before decisions are made.', x, 560, 64, 'thin', T1, a4, track=-0.5)
    k = eio(lin(t, tc + 0.3, 1.6))
    if a4 > 0:
        line(c, [(x, 600), (x + 1180, 600)], k, a=1.0, head=k < 1)
        ping(c, x + 1180, 600, t, tc + 1.9, R=260, dur=2.0)
    if t > tc + 4.6:
        title_lockup(c, t, tc + 5.0)

def s8(c, t, tl):
    t0 = tl['start']['S8']
    x = 160
    text(c, 'The Ocean Has Floors', x, 170, 56, 'thin', T1, lin(t, t0 + 0.3, 1.2))
    text(c, f'{TEAM_NAME} · {INSTITUTION}'.upper(), x, 222, 14, 'semi', ECHO, lin(t, t0 + 0.6, 1.0))
    text(c, MEMBERS, x, 262, 21, 'med', T1, lin(t, t0 + 0.8, 1.2))
    text(c, 'LAUTARA 2026 · RUSSIA–INDONESIA MARITIME HACKATHON', x, 300, 12, 'semi', T3, lin(t, t0 + 1.0, 1.0))
    c.drawLine(x, 340, x + 1600 * eout(lin(t, t0 + 1.0, 1.2)), 340, paint(HAIR, 1, stroke=1, cap_round=False))
    credits = [
        ('DATA', 'E.U. Copernicus Marine Service Information (GLORYS12) · Contains modified Copernicus Sentinel data (Sentinel-1, Sentinel-2) · USGS Landsat 8/9 · NASA GPM IMERG · KKP official release, 29 Oct 2023 · UNEP sand and sustainability estimate · Natural Earth'),
        ('RESEARCH', 'Team analysis: Coastal Sediment Diagnostic; Before the Plume Reaches the Reef. Wahyudi et al. (2023), Pulau Tunda.'),
        ('PICTURE', 'Motion graphics built in code by the team. 3D coast art made by the team in Blender. Island, seabed and station are illustrative.'),
        ('VOICE', 'Narration generated with Kokoro-82M text-to-speech (Apache-2.0) from the team’s script.'),
        ('TYPE', 'Montserrat, SIL Open Font License.'),
        ('SOUND', 'Sound credits: none.'),
    ]
    y = 400
    for i, (k, v) in enumerate(credits):
        ti = t0 + 1.2 + i * 0.25
        text(c, k, x, y + 4, 12, 'semi', ECHO, lin(t, ti, 0.6))
        lines = wrap(v, 19, 'reg', 1300)
        for j, ln in enumerate(lines):
            text(c, ln, x + 200, y + 4 + j * 30, 19, 'reg', T2, lin(t, ti + 0.1 + j * 0.15, 0.8))
        y += 30 * len(lines) + 24
    xx = x
    for kind in ('MODELLED', 'MEASURED', 'DESIGN CONCEPT'):
        xx += label_tag(c, kind, xx, 940, lin(t, t0 + 2.6, 0.8)) + 16
    text(c, 'Every number in this film carries one of these labels.', xx + 10, 963, 16, 'reg', T3, lin(t, t0 + 2.8, 1.0))
