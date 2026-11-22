"""The documentary cut: shots S1-S8 built on the 3D coast footage, the archive figures and the verified rows."""
import math, os
import numpy as np
import skia
from gfx import *
from scenes import (kicker, reading, draw_map, graticule, pin, team_slot, tile, bearing_vec,
                    s2_proj, S2_BBOX, s6_proj, S6_BBOX, TUNDA, KODI, AMUR, SURF, DEEP, ART,
                    NAMES, MEMBERS, TEAM_NAME, INSTITUTION)

S4_STATION = (1660, 520)
S4_AB = 520
WATER_Y = 471
REEL = f'{ART}/coast-reel.mp4'
TRAVEL = {k: f'{ART}/coasts/{k}/travel.mp4' for k in ('tunda', 'kodingareng', 'amur')}

def title(c, kick, line1, t, t0, x=110, y=120, size=46, col=T1):
    kicker(c, kick, x, y, lin(t, t0, 0.7))
    text(c, line1, x, y + size + 16, size, 'light', col, lin(t, t0 + 0.3, 1.1))

def caption(c, lines, x, y, t, t0, step=0.25):
    for i, (s, size, kind, col) in enumerate(lines):
        text(c, s, x, y, size, kind, col, lin(t, t0 + i * step, 0.8))
        y += size * 1.5

def vignette_band(c, y0, y1, a=0.75):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)],
                                        [skia.Color4f(0, 0, 0, 0), skia.Color4f(0.016, 0.024, 0.031, a)])
    p = skia.Paint(Shader=sh)
    c.drawRect(skia.Rect.MakeLTRB(0, y0, 1920, y1), p)
    c.drawRect(skia.Rect.MakeLTRB(0, y1, 1920, 1080), paint(STAGE, a))

# =====================================================================
def s1(c, t, tl):
    """Globe → descent to Pulau Tunda → the missing day."""
    T = tl['T']
    tw = T['o2'] - 0.8                      # scan wipe from the globe to Tunda
    if t < tw + 1.4:
        draw_footage(c, REEL, 0.0 + max(t - 0.3, 0) * 0.42, reveal=lin(t, 0.3, 2.2), grade='globe')
    if t > tw:
        draw_footage(c, TRAVEL['tunda'], min((t - tw) * 0.5, 5.0), reveal=lin(t, tw, 1.4))
    # readings over the globe
    kicker(c, '27 OCTOBER 2023', 110, 120, lin(t, T['o1'] + 0.4, 0.8), WARM)
    text(c, 'Waters off Jakarta', 110, 182, 46, 'light', T1, lin(t, T['o1'] + 1.0, 1.2) * (1 - lin(t, tw, 0.5)))
    # readings over Tunda
    if t > tw + 0.8:
        text(c, 'Pulau Tunda', 110, 182, 46, 'light', T1, lin(t, tw + 1.0, 1.2))
        text(c, 'BANTEN · 5.81° S  106.28° E', 110, 216, 13, 'med', T3, lin(t, tw + 1.6, 1.0))
        kc = T['o2'] + 3.6
        reading(c, 'SAND ABOARD AT INSPECTION', '≈ 24,000 m³', 110, 300, lin(t, kc, 0.9), 40, WARM, 'thin')
        text(c, 'KKP RELEASE, 29 OCT 2023 · SOURCE SUSPECTED, NOT A VERIFIED LOCATION', 110, 374, 12, 'med', T3, lin(t, kc + 0.6, 1.2))
    # the archive timeline: 24 Oct – 2 Nov
    ka = T['o3'] + 0.2
    if t > ka:
        vignette_band(c, 600, 760, 0.9)
        x0, x1, y = 160, 1760, 900
        days = list(range(24, 32)) + [1, 2]
        kt = eout(lin(t, ka, 1.2))
        c.drawLine(x0, y, mix(x0, x1, kt), y, paint(T3, 0.8, stroke=1, cap_round=False))
        kicker(c, 'SATELLITE ARCHIVE · SENTINEL-1, SENTINEL-2, LANDSAT 8/9 · STUDY FOOTPRINT', x0, 715, lin(t, ka, 0.9), T2)
        step = (x1 - x0) / (len(days) - 1)
        for i, d in enumerate(days):
            x = x0 + i * step
            a = lin(t, ka + 0.3 + i * 0.06, 0.4)
            c.drawLine(x, y - 8, x, y + 8, paint(T3, a, stroke=1, cap_round=False))
            text(c, f'{d} {"OCT" if d > 20 else "NOV"}', x, y + 38, 16, 'med', T3, a, 'center')
        for d, tt in ((26, T['o4'] + 1.4), (31, T['o4'] + 3.0)):
            x = x0 + days.index(d) * step
            k = lin(t, tt, 0.6)
            tile(c, x - 60, y - 140, 120, 100, 'lit', k)
            text(c, 'SCENE', x, y - 82, 17, 'semi', T1, k, 'center')
            c.drawLine(x, y - 40, x, y - 40 + 32 * eout(k), paint(ECHO, 1, stroke=1.3, cap_round=False))
        x = x0 + days.index(27) * step
        tm = T['o4'] + 5.6
        km = lin(t, tm, 0.9)
        tile(c, x - 60, y - 140, 120, 100, 'missing', km)
        text(c, 'NO IMAGE', x, y - 82, 17, 'semi', T1, lin(t, tm + 0.3, 0.6), 'center')
        node(c, x, y, 12, lin(t, ka + 0.9, 0.5), t=t)
        text(c, 'INSPECTION', x, y + 68, 18, 'semi', WARM, lin(t, ka + 1.1, 0.6), 'center')
        w_ = label_tag(c, 'MEASURED · catalog search', x0, 1010, lin(t, tm + 0.8, 0.8))

# =====================================================================
def s2(c, t, tl):
    """Title, the team, then the answer to the competition question on a frame of its own."""
    T, D = tl['T'], tl['D']
    t0 = tl['start']['S2']
    tw = T['t2'] - 0.4                       # the team and title give way to the answer
    img = image(f'{ART}/coasts/tunda/detail.png', grade='cold_dark')
    draw_image(c, img, 0, 0, 1920, 1080, lin(t, t0 - 0.4, 1.8))
    vignette_band(c, 300, 640, 0.92)
    out = 1 - lin(t, tw, 0.6)
    if out > 0:
        kicker(c, 'LAUTARA 2026 · RUSSIA–INDONESIA MARITIME HACKATHON', 110, 130, min(lin(t, t0 + 0.2, 0.9), out))
        text(c, 'The Ocean Has Floors', 110, 236, 96, 'thin', T1, min(lin(t, t0 + 0.4, 1.4), out), track=-0.5)
        seg = "We are Daniel Ferdiansyah, Daniel Angger, Salwa Alifia and Fauzi Fadhlurohman."
        sw, sh, gap = 190, 238, 24
        xs0, ys = 110, 560
        for i, nm in enumerate(NAMES):
            key = 'Daniel Angger' if i == 1 else nm.split()[0]
            tn = T['t1'] + D['t1'] * seg.index(key) / len(seg) - 0.2
            x = xs0 + i * (sw + gap)
            team_slot(c, i, x, ys, sw, sh, min(lin(t, tn, 0.7), out), t)
            text(c, nm, x, ys + sh + 36, 18, 'med', T1, min(lin(t, tn + 0.3, 0.8), out))
        text(c, f'{TEAM_NAME} · {INSTITUTION}'.upper(), xs0, ys + sh + 80, 18, 'semi', ECHO, min(lin(t, T['t1'] + 2.5, 1.0), out))
    if t < tw:
        return
    # the answer
    c.drawRect(skia.Rect.MakeXYWH(0, 0, 1920, 1080), paint(STAGE, 0.55 * eout(lin(t, tw, 0.8))))
    kicker(c, 'THE MOST IMPORTANT CHALLENGE FACING MARITIME AFFAIRS TODAY', 160, 250, lin(t, T['t2'], 1.0))
    text(c, 'A blind spot.', 160, 350, 80, 'thin', T1, lin(t, T['t2'] + 5.6, 1.0), track=-0.5)
    t3 = T['t3']
    text(c, 'Sand extraction moves sediment below the surface,', 160, 470, 44, 'light', T1, lin(t, t3 + 0.2, 1.6))
    text(c, 'often on days no satellite can see.', 160, 528, 44, 'light', T1, lin(t, t3 + 2.4, 1.4))
    text(c, 'Coastal decisions are made half blind.', 160, 610, 44, 'light', ECHO, lin(t, t3 + 5.4, 1.6))
    t4 = T['t4']
    kicker(c, 'WHY IT MATTERS MOST', 160, 730, lin(t, t4 + 0.2, 0.8), WARM)
    text(c, 'Fishing grounds, reefs and new ports all depend on', 160, 782, 30, 'reg', T2, lin(t, t4 + 3.2, 1.4))
    text(c, 'knowing where that sediment goes.', 160, 824, 30, 'reg', T2, lin(t, t4 + 4.6, 1.2))

# =====================================================================
def s3(c, t, tl):
    """Scale, then the cloudy record (face 1920 x 3240)."""
    T = tl['T']; t0 = tl['start']['S3']
    # ---- A: the global figure over the globe
    img = image(f'{ART}/globe/globe-overview.png', grade='cold_dark')
    draw_image(c, img, 0, 0, 1920, 1080, lin(t, t0 - 0.5, 2.0))
    vignette_band(c, 500, 900, 0.6)
    tc = T['g1'] + 0.6
    kicker(c, 'SAND AND SEDIMENT DREDGED FROM SEAS AND COASTS · EACH YEAR', 110, 600, lin(t, tc - 0.6, 1.0))
    kv = eout(lin(t, tc + 0.4, 2.2))
    text(c, f'{4 * kv:.0f}–{8 * kv:.0f}', 104, 760, 150, 'thin', T1, lin(t, tc, 0.6), track=-3)
    bx = 104 + text_width('4–8', 150, 'thin', -3) + 40
    text(c, 'billion tonnes', bx, 712, 40, 'light', T1, lin(t, tc + 0.8, 1.0))
    text(c, 'estimated, worldwide', bx, 756, 22, 'reg', T3, lin(t, tc + 1.2, 1.0))
    chip(c, 110, 820, 'UNEP estimate · all dredging, not only mining', PLATE, None, T2, lin(t, T['g1'] + 8.6, 0.8))
    # ---- B: the cloudy record
    yb = 1080
    title(c, 'NOVEMBER 2025 – FEBRUARY 2026 · WET SEASON', 'Clear views of the water', t, T['c1'] + 0.2, y=yb + 120)
    rows = (('tunda', 'Pulau Tunda', 27, 13, yb + 440, T['c1'] + 6.0), ('kodingareng', 'Kodingareng Lompo', 28, None, yb + 700, T['c1'] + 12.6))
    for key, name, n, lit, y, ts in rows:
        th = image(f'{ART}/coasts/{key}/godview.png', grade='cold')
        draw_image(c, th, 110, y - 120, 256, 144, lin(t, ts - 1.4, 1.0))
        c.drawRect(skia.Rect.MakeXYWH(110, y - 120, 256, 144), paint(ECHO, 0.35 * lin(t, ts - 1.4, 1.0), stroke=1))
        text(c, name, 400, y - 92, 22, 'med', T1, lin(t, ts - 1.0, 0.8))
        text(c, f'{n} SENTINEL-2 DATES', 400, y - 66, 11, 'med', T3, lin(t, ts - 0.8, 0.8))
        sz, gap = 34, 8
        for i in range(n):
            tile(c, 400 + i * (sz + gap), y - 40, sz, sz, 'lit' if i == lit else 'dim', lin(t, ts + i * 0.05, 0.25))
        kk = clamp(lin(t, ts, n * 0.05 + 0.3))
        shown = 1 if lit is not None and kk * n > lit else 0
        text(c, f'{shown}/{n}', 1810, y - 4, 72, 'thin', ECHO if shown else T1, lin(t, ts - 0.3, 0.6), 'right')
    kb = lin(t, T['c1'] + 8.0, 0.8)
    w_ = label_tag(c, 'MEASURED · satellite screen', 110, yb + 840, kb)
    source_tag(c, 'Water-only screen: at least 90% of a 1.5–3 km ring around the island clear', 110 + w_ + 18, yb + 860, kb)
    # ---- C: rainy days
    yc = 2160
    title(c, 'RAINY DAYS · NOVEMBER – DECEMBER 2025 · BOTH ISLANDS', 'When runoff is highest', t, T['c2'] - 0.4, y=yc + 120)
    ts = T['c2'] + 0.6
    rng = np.random.default_rng(11)
    kinds = ['missing'] * 49 + ['dim'] * 22
    rng.shuffle(kinds)
    kinds.insert(41, 'lit')
    cols, sz, gap = 18, 58, 12
    for i, kd in enumerate(kinds):
        tile(c, 110 + (i % cols) * (sz + gap), yc + 330 + (i // cols) * (sz + gap), sz, sz, kd, lin(t, ts + i * 0.03, 0.25))
    kk = clamp(lin(t, ts, 72 * 0.03))
    text(c, f'{1 if kk > 42 / 72 else 0}/72', 1810, yc + 420, 120, 'thin', ECHO, lin(t, ts, 0.6), 'right')
    text(c, 'RAINY DAYS WITH A USABLE VIEW', 1810, yc + 460, 18, 'med', T2, lin(t, ts + 0.4, 0.8), 'right')
    kl = ts + 2.4
    for j, (kd, lab) in enumerate((('lit', 'usable view · 1'), ('dim', 'image failed the screen · 22'), ('missing', 'no image acquired · 49'))):
        yy = yc + 540 + j * 44
        tile(c, 1400, yy - 18, 22, 22, kd, lin(t, kl + j * 0.2, 0.4))
        text(c, lab.upper(), 1440, yy, 18, 'med', T1, lin(t, kl + j * 0.2, 0.8))
    kq = lin(t, kl, 0.8)
    label_tag(c, 'MEASURED · rain + satellite record', 110, yc + 650, kq)
    source_tag(c, 'Each island counted per day · ≥10 mm regional IMERG rain · Sentinel-2 + Landsat 8/9 broad quality screen', 110, yc + 710, kq)

# =====================================================================
def s4(c, t, tl, clip_k=0.0):
    """Kodingareng: descent footage, then two depths on one day."""
    T = tl['T']; t0 = tl['start']['S4']
    if clip_k > 0:
        c.save(); c.clipRect(skia.Rect.MakeLTRB(-10, -10, 1930, mix(1090, S4_AB, clip_k)))
    tw = T['d2'] - 0.6
    if t < tw + 1.6:
        draw_footage(c, TRAVEL['kodingareng'], min(max(t - t0 + 0.4, 0) * 0.45, 5.0), reveal=lin(t, t0 - 0.8, 1.6))
        a = 1 - lin(t, tw, 0.4)
        kicker(c, 'KODINGARENG LOMPO · OFF MAKASSAR · SOUTH SULAWESI', 110, 120, lin(t, T['d1'] - 0.2, 0.9) * a)
        text(c, 'An island of fishing families', 110, 182, 46, 'light', T1, lin(t, T['d1'] + 0.4, 1.2) * a)
        text(c, 'MAKASSAR NEW PORT DREDGING · FEBRUARY – OCTOBER 2020', 110, 226, 13, 'med', WARM, lin(t, T['d1'] + 5.2, 1.0) * a)
        text(c, 'Fishers raised concerns about the work · Kurniawati et al. 2021', 110, 254, 18, 'reg', T2, lin(t, T['d1'] + 7.0, 1.2) * a)
    if t > tw:
        img = image(f'{ART}/coasts/kodingareng/mapview.png', grade='cold')
        draw_image(c, img, 0, 0, 1920, 1080, lin(t, tw, 1.4), scan='y')
        kc = lin(t, T['d2'] + 1.0, 0.8)
        ticks(c, 40, 40, 1840, 1000, ECHO, 0.8 * eout(kc), L=60)
        text(c, 'ONE ~9 KM MODEL CELL COVERS THIS WHOLE VIEW', 1860, 1012, 13, 'semi', ECHO, kc, 'right')
        sx, sy = S4_STATION
        tsl = T['d3'] + 0.2
        ks = eio(lin(t, tsl, 2.6))
        b0, b1 = float(SURF['towards_deg']), float(DEEP['towards_deg']) + 360
        b = mix(b0, b1, ks)
        sp = mix(float(SURF['speed_m_s']), float(DEEP['speed_m_s']), ks)
        ad = lin(t, T['d2'] + 2.0, 0.9)
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
            hp = skia.Path(); hp.moveTo(tip[0] + vx * 12, tip[1] + vy * 12)
            hp.lineTo(tip[0] + px * 9, tip[1] + py * 9); hp.lineTo(tip[0] - px * 9, tip[1] - py * 9); hp.close()
            c.drawPath(hp, paint(SCAN, eout(ad)))
            c.drawArc(skia.Rect.MakeXYWH(sx - R + 30, sy - R + 30, 2 * R - 60, 2 * R - 60), -90, (b % 360), False, paint(ECHO, 0.35 * eout(ad), stroke=1))
            node(c, sx, sy, 12, ad, t=t)
            text(c, 'S-01 · ILLUSTRATIVE STATION', sx, sy + R + 56, 17, 'semi', WARM, lin(t, T['d2'] + 2.5, 0.8), 'center')
        ka = lin(t, T['d2'] + 0.2, 0.8)
        if ka > 0:
            chunk(c, 110, 220, 500, 620, PLATE, None, eout(ka))
            kicker(c, 'DEPTH BELOW SURFACE', 150, 272, ka)
            trk = (170, 330, 660)
            c.drawLine(trk[0], trk[1], trk[0], trk[2], paint(HAIR, 1, stroke=1.5, cap_round=False))
            c.drawLine(trk[0], trk[1], trk[0], mix(trk[1], trk[2], ks), paint(ECHO, 1, stroke=2, cap_round=False))
            for yy, lab in ((trk[1], '0.5 M'), (trk[2], '9.6 M')):
                c.drawLine(trk[0] - 8, yy, trk[0] + 8, yy, paint(T3, 1, stroke=1, cap_round=False))
                text(c, lab, trk[0] + 20, yy + 5, 12, 'med', T3, ka)
            hy = mix(trk[1], trk[2], ks)
            c.drawRect(skia.Rect.MakeXYWH(trk[0] - 9, hy - 5, 18, 10), paint(WARM, eout(ka)))
            text(c, f'{mix(0.494, 9.573, ks):.1f} m', 260, 420, 88, 'thin', T1, ka, track=-1)
            reading(c, 'MODELLED CURRENT · DAILY MEAN', f'{sp:.3f} m/s', 264, 480, ka, 34, ECHO)
            reading(c, 'BEARING', f'{b % 360:05.1f}°', 264, 576, ka, 34, ECHO)
            text(c, 'TOWARD WEST' if ks < 0.5 else 'TOWARD NORTHEAST', 264, 650, 13, 'semi', ECHO, ka)
            w_ = label_tag(c, 'MODELLED', 150, 770, ka)
            source_tag(c, 'Copernicus GLORYS12', 150 + w_ + 14, 790, ka)
        title(c, '16 APRIL 2020 · UTC', 'One place, one day, two depths', t, T['d2'] - 0.2, x=110, y=110, size=40)
        kf = lin(t, T['d4'] + 0.6, 0.8)
        if kf > 0:
            chunk(c, 110, 862, 860, 150, PLATE, None, eout(kf))
            text(c, '96/274', 150, 952, 72, 'thin', ECHO, kf, track=-1)
            text(c, 'DAYS, FEB–OCT 2020', 430, 912, 18, 'semi', T3, kf)
            text(c, 'surface west, deeper water east', 430, 950, 24, 'reg', T1, lin(t, T['d4'] + 1.0, 1.0))
            k96 = eout(lin(t, T['d4'] + 1.0, 1.4))
            c.drawLine(430, 978, 930, 978, paint(HAIR, 1, stroke=4, cap_round=False))
            c.drawLine(430, 978, 430 + 500 * 96 / 274 * k96, 978, paint(ECHO, 1, stroke=4, cap_round=False))
        source_tag(c, 'MODELLED · Copernicus GLORYS12 daily mean · cell centre 5.1667° S, 119.25° E · scene art illustrative', 1000, 1050, lin(t, T['d2'] + 1, 1.0), size=12)
    if clip_k > 0:
        c.restore()

# =====================================================================
def s5(c, t, tl):
    T = tl['T']; t0 = tl['start']['S5']
    img = image(f'{ART}/coasts/kodingareng/section.png', grade='cold')
    c.drawImageRect(img, skia.Rect.MakeXYWH(0, 0, 1920, 1080), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), skia.Paint())
    c.drawLine(0, WATER_Y, 1920, WATER_Y, paint(ECHO, 0.35, stroke=1, cap_round=False))
    text(c, 'B', 40, WATER_Y - 24, 28, 'light', T2, 1.0)
    text(c, 'A', 1880, WATER_Y - 24, 28, 'light', T2, 1.0, 'right')
    kicker(c, 'PROPOSED · A PLANNING TOOL FOR COASTAL MONITORING OFFICERS', 110, 110, lin(t, T['p1'], 0.9))
    text(c, 'The Ocean Has Floors', 110, 180, 56, 'thin', T1, lin(t, T['p1'] + 4.6, 1.4), track=-0.5)
    text(c, 'SECTION A–B THROUGH STATION S-01', 110, 214, 13, 'med', T3, lin(t, T['p2'] + 5.0, 1.0))
    bx = 1500
    node(c, bx, WATER_Y, 12, lin(t, T['p2'] + 2.0, 0.4), t=t)
    kd = eout(lin(t, T['p2'] + 6.4, 1.4))
    if kd > 0:
        yd = mix(WATER_Y, 760, kd)
        c.drawLine(bx, WATER_Y + 8, bx, yd, paint(WARM, 0.9, stroke=1.3, cap_round=False))
        for yy in range(WATER_Y + 40, int(yd), 40):
            c.drawLine(bx - 6, yy, bx + 6, yy, paint(WARM, 0.6, stroke=1, cap_round=False))
        c.drawRect(skia.Rect.MakeXYWH(bx - 7, yd - 7, 14, 14), paint(WARM, 1))
        a = lin(t, T['p2'] + 7.4, 0.8)
        leader(c, bx + 12, yd, bx + 60, yd, a)
        text(c, 'PROPOSED SAMPLE DEPTH', bx + 70, yd - 10, 17, 'semi', T2, a)
        text(c, '9.6 m', bx + 70, yd + 36, 44, 'light', WARM, a)
    kc = T['p3']
    gone = 1 - lin(t, T['p4'] + 0.4, 0.5)
    label_tag(c, 'MODELLED · current at 9.6 m', 110, 260, min(lin(t, kc + 1.6, 0.6), gone))
    label_tag(c, 'MEASURED · awaiting field data', 110, 312, min(lin(t, kc + 2.4, 0.6), gone))
    chip(c, 110, 364, 'MISSING · local current profile', PLATE, None, T1, min(lin(t, kc + 3.2, 0.6), gone), size=14, kind='semi', pad=12, hatched=True)
    td = T['p4']
    kb = lin(t, td - 0.2, 0.6)
    press = clamp(lin(t, td + 0.4, 0.25))
    bw = chip(c, 1810, 880, '+ Request field check', WARM, None, WARM, kb, size=16, kind='semi', align='right')
    if 0 < press < 1:
        c.drawRect(skia.Rect.MakeXYWH(1810 - bw, 880, bw, 33.6), paint(WARM, 0.35 * (1 - press)))
    cx, cy, cw, ch = 690, 250, 720, 680
    line(c, bezier((1810 - bw, 897), (1500, 897), (1500, 600), (cx + cw, 600), 50), eio(lin(t, td + 0.6, 0.8)), color=WARM)
    ak = lin(t, td + 1.0, 0.6)
    if ak > 0:
        chunk(c, cx, cy, cw, ch * eout(ak), PLATE, None, 1.0)
        kicker(c, 'FIELD BRIEF · DRAFT FOR REVIEW', cx + 40, cy + 54, lin(t, td + 1.2, 0.8), WARM)
        text(c, 'KR-01 Kodingareng baseline survey', cx + 40, cy + 108, 32, 'light', T1, lin(t, td + 1.4, 1.0))
        rows = [('Station', 'S-01 · illustrative waypoint'), ('When', 'Pre-work visit · 08:00–10:00 WITA'),
                ('Depths and instruments', 'Profiler at 0.5 m and 9.6 m · paired water bottles'),
                ('Review and return', 'Supervisor signs · results return to KR-01')]
        anchors = (2.0, 3.0, 3.9, 6.2)
        for i, (k_, v_) in enumerate(rows):
            ar = lin(t, td + anchors[i], 0.7)
            yy = cy + 180 + i * 84
            c.drawLine(cx + 40, yy - 32, cx + 40 + (cw - 80) * eout(ar), yy - 32, paint(HAIR, 1, stroke=1, cap_round=False))
            text(c, k_.upper(), cx + 40, yy, 12, 'semi', T3, ar)
            text(c, v_, cx + 40, yy + 32, 23, 'reg', T1, ar)
        kt = lin(t, td + 7.0, 0.6)
        if kt > 0:
            yy = cy + ch - 70
            p = skia.Path(); p.moveTo(cx + 44, yy); p.lineTo(cx + 54, yy + 10); p.lineTo(cx + 72, yy - 10)
            pm2 = skia.PathMeasure(p, False); sg = skia.Path(); pm2.getSegment(0, pm2.getLength() * eout(kt), sg, True)
            c.drawPath(sg, paint(ECHO, 1, stroke=2))
            text(c, 'SIGNED · SUPERVISOR · VERSION 1', cx + 88, yy + 6, 14, 'semi', ECHO, kt)
        label_tag(c, 'MEASURED · attached', cx + 440, cy + ch - 90, lin(t, td + 10.6, 0.6))
    kr = lin(t, td + 9.0, 1.8)
    if kr > 0:
        line(c, bezier((1500, WATER_Y - 20), (1500, 300), (1460, 230), (cx + cw, cy + 40), 50), eio(kr), color=T1)
        text(c, 'READINGS + SAMPLE IDS → KR-01', 1540, 300, 13, 'semi', T1, lin(t, td + 9.3, 0.8))
    label_tag(c, 'DESIGN CONCEPT · illustrative station and seabed · vertical exaggeration ×3.2', 110, 1000, 1.0)

# =====================================================================
def s6(c, t, tl):
    """Amur Bay: descent footage, the archive scene, the same rules."""
    T = tl['T']; t0 = tl['start']['S6']
    tw = T['r2'] - 0.5
    if t < tw + 1.6:
        draw_footage(c, TRAVEL['amur'], min(max(t - t0 + 0.3, 0) * 0.6, 5.0), reveal=lin(t, t0 - 0.8, 1.6))
        a = 1 - lin(t, tw, 0.4)
        kicker(c, 'AMUR BAY · PRIMORSKY KRAI · RUSSIA', 110, 120, lin(t, T['r1'] + 0.8, 0.9) * a)
        text(c, 'Where the Razdolnaya meets the sea', 110, 182, 46, 'light', T1, lin(t, T['r1'] + 2.4, 1.3) * a)
        text(c, 'RIVER MOUTH · NEAR VLADIVOSTOK · 43.3° N  131.9° E', 110, 216, 13, 'med', T3, lin(t, T['r1'] + 3.4, 1.0) * a)
    if t <= tw:
        return
    k = lin(t, tw, 1.4)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, 1920, 1080 * eio(k)))
    c.drawRect(skia.Rect.MakeXYWH(0, 0, 1920, 1080), paint(STAGE, 1))
    c.restore()
    if k < 1:
        c.drawLine(0, 1080 * eio(k), 1920, 1080 * eio(k), paint(SCAN, 0.9, stroke=1.4, cap_round=False))
    graticule(c, s6_proj, list(range(95, 150, 10)), list(range(-10, 56, 10)), lin(t, tw + 0.6, 1.0))
    draw_map(c, 's6', s6_proj, S6_BBOX, lin(t, tw + 0.4, 2.2), focus=('Indonesia',), focus2=('Russia',), W_=960)
    source_tag(c, 'MAP · NATURAL EARTH', 110, 1050, lin(t, tw + 2, 0.8), size=12)
    pts = {n: s6_proj(*ll) for n, ll in (('tunda', TUNDA), ('kodi', KODI), ('amur', AMUR))}
    pin(c, *pts['amur'], 'Amur Bay', 'Razdolnaya estuary · Russia', t, tw + 1.6, 'left')
    tb = T['r4'] + 0.2
    root = (900, 1120)
    for i, (n, lab, sub, side) in enumerate((('tunda', 'Pulau Tunda', 'Indonesia', 'left'), ('kodi', 'Kodingareng Lompo', 'Indonesia', 'right'), ('amur', None, None, None))):
        x, y = pts[n]
        ctrl = (x + 220, y + 320) if n == 'amur' else (x + 80, y + 170)
        line(c, bezier(root, (root[0] + 40, root[1] - 300), ctrl, (x, y + 14), 50), eio(lin(t, tb + i * 0.15, 1.6)))
        if lab:
            pin(c, x, y, lab, sub, t, tb + 1.0 + i * 0.15, side)
    tr = T['r2']
    ki = lin(t, tr + 0.4, 1.2)
    if T['r4'] < t:
        ki = 1 - lin(t, T['r4'], 0.6)
    img = image(f'{ROOT}/assets/amur_optical_counterexample.png', crop=(1497, 122, 2720, 1196), grade='desat')
    if ki > 0:
        kicker(c, '6 SEPTEMBER 2023 · RAZDOLNAYA RIVER MOUTH', 1000, 96, ki)
        draw_image(c, img, 1000, 120, 520, 457, ki)
        c.drawRect(skia.Rect.MakeXYWH(1000, 120, 520, 457), paint(ECHO, 0.4 * eout(ki), stroke=1))
        text(c, 'SENTINEL-2 TRUE COLOUR · TEAM ARCHIVE FIGURE', 1000, 605, 12, 'semi', T2, ki)
        reading(c, 'LANDSAT 9, SAME WATER', '+18 min', 1560, 150, lin(t, tr + 3.6, 1.0), 40, T1, 'thin')
        text_block(c, 'Both missions recorded a brighter west box than east box in the red band.', 1560, 250, 18, 300, 'reg', T3, lin(t, tr + 8.0, 1.4))
        text_block(c, 'Contains modified Copernicus Sentinel data 2023 · USGS Landsat 9', 1560, 520, 12, 300, 'reg', T3, ki)
    kb = lin(t, tr + 7.6, 0.8)
    if T['r4'] < t:
        kb = 1 - lin(t, T['r4'], 0.6)
    bars = (('6 Sep · Sentinel-2', 0.0552, tr + 8.2), ('6 Sep · Landsat 9', 0.0646, tr + 8.7), ('12 Jul · Landsat · before the floods', 0.0961, T['r3'] + 0.8))
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
    kq = lin(t, T['r3'] + 4.6, 1.2)
    if T['r4'] < t:
        kq = 1 - lin(t, T['r4'], 0.6)
    text(c, 'River or dredger? Brightness alone cannot say.', 1000, 1000, 28, 'light', T1, kq)
    ap = lin(t, T['r4'] + 0.6, 0.8)
    if ap > 0:
        x0, y0 = 1000, 300
        chunk(c, x0, y0, 820, 440, PLATE, None, eout(ap))
        kicker(c, 'SHARED CASE REVIEW · SAME EVIDENCE RULES', x0 + 44, y0 + 64, ap)
        for i, (k_, v_) in enumerate((('Indonesia', 'Kodingareng Lompo · Pulau Tunda'), ('Russia', 'Amur Bay · Razdolnaya estuary'))):
            yy = y0 + 140 + i * 74
            text(c, k_, x0 + 44, yy, 28, 'light', T1, lin(t, T['r4'] + 0.9 + i * 0.3, 0.8))
            text(c, v_.upper(), x0 + 260, yy - 4, 13, 'med', T3, lin(t, T['r4'] + 1.1 + i * 0.3, 0.8))
        label_tag(c, 'DESIGN CONCEPT · proposed exchange', x0 + 44, y0 + 340, lin(t, T['r4'] + 2.0, 0.8))

# =====================================================================
def s7(c, t, tl):
    """Pull back to the planet; the answer restated; the title."""
    T = tl['T']; t0 = tl['start']['S7']
    draw_footage(c, REEL, 25.0 + clamp((t - t0) * 0.08, 0, 1.9), reveal=lin(t, t0 - 0.6, 2.0), grade='globe')
    vignette_band(c, 260, 640, 0.9)
    x = 160
    e2, e3 = T['e2'], T['e3']
    out = e3 + tl['D']['e3'] + 0.6
    def a(t0_, d=1.2):
        return lin(t, t0_, d) if t < out else 1 - lin(t, out, 0.6)
    text(c, 'Sand extraction will continue.', x, 600, 40, 'light', T2, a(T['e1']))
    kicker(c, 'THE CHALLENGE', x, 690, a(e2), WARM)
    text(c, 'See what it moves, below the surface and on unseen days,', x, 750, 40, 'light', T1, a(e2 + 1.0, 2.0))
    text(c, 'before decisions are made.', x, 802, 40, 'light', T1, a(e2 + 3.6, 1.4))
    text(c, 'The right place. The right depth.', x, 930, 64, 'thin', ECHO, a(e3 + 4.6, 1.6), track=-0.5)
    if t > out + 0.4:
        kicker(c, 'LAUTARA 2026 · RUSSIA–INDONESIA MARITIME HACKATHON', x, 790, lin(t, out + 0.4, 0.9))
        text(c, 'The Ocean Has Floors', x, 900, 104, 'thin', T1, lin(t, out + 0.6, 1.6), track=-0.5)

def s8(c, t, tl):
    t0 = tl['start']['S8']
    x = 160
    text(c, 'The Ocean Has Floors', x, 170, 56, 'thin', T1, lin(t, t0 + 0.3, 1.2))
    text(c, f'{TEAM_NAME} · {INSTITUTION}'.upper(), x, 222, 14, 'semi', ECHO, lin(t, t0 + 0.6, 1.0))
    text(c, MEMBERS, x, 262, 21, 'med', T1, lin(t, t0 + 0.8, 1.2))
    text(c, 'LAUTARA 2026 · RUSSIA–INDONESIA MARITIME HACKATHON', x, 300, 12, 'semi', T3, lin(t, t0 + 1.0, 1.0))
    credits = [
        ('DATA', 'E.U. Copernicus Marine Service Information (GLORYS12) · Contains modified Copernicus Sentinel data (Sentinel-1, Sentinel-2) · USGS Landsat 8/9 · NASA GPM IMERG · KKP official release, 29 Oct 2023 · UNEP sand and sustainability estimate · Natural Earth'),
        ('RESEARCH', 'Team analysis: Coastal Sediment Diagnostic; Before the Plume Reaches the Reef. Kurniawati et al. (2021), Kodingareng fishers. Wahyudi et al. (2023), Pulau Tunda.'),
        ('PICTURE', 'Coast, globe and section footage made by the team in Blender; graphics built in code. Island, seabed and station are illustrative.'),
        ('VOICE', 'Narration generated with Kokoro-82M text-to-speech (Apache-2.0) from the team’s script.'),
        ('TYPE', 'Montserrat, SIL Open Font License.'),
        ('SOUND', 'CC0 recordings via Openverse/Freesound by Bitbeast, Jummit, Kingofgamers_cz, Kinoton, Luis0413, SamsterBirdies, Sillyslimeball, beskhu, dslrguide, hth2000, jbum, malle99, paespedro, qubodup, snowflakes. Additional sounds generated with Earshot (MIT) and by the team in code; placed with the Real SFX workflow.'),
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
        xx += label_tag(c, kind, xx, 960, lin(t, t0 + 2.6, 0.8)) + 16
    text(c, 'Every number in this film carries one of these labels.', xx + 10, 983, 16, 'reg', T3, lin(t, t0 + 2.8, 1.0))
