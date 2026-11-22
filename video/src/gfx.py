"""Shared drawing kit, documentary treatment: black ground, cold echo lines, one warm accent,
thin Montserrat type written on by a scan bar, instrument readouts beside their objects."""
import math, os
import numpy as np
import skia

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080

def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

# ---------- palette ----------
STAGE = '#040608'
ECHO = '#B3DBFF'        # cold echo: lines, modelled values, rings
SCAN = '#FFFFFF'        # scan front
WARM = '#F2C48D'        # one warm accent: the target / the signal (station, field request)
RED = '#FF8C78'         # only for a value over a limit
T1, T2, T3 = '#EEF2F6', '#C4CED8', '#96A2B0'
HAIR = '#2A3642'        # hairlines, empty frames
PLATE = '#070B10'

# legacy names used by the scenes
TEAL = ECHO; TEAL_HI = SCAN; TEAL_LIP = HAIR
AMBER = WARM; AMBER_LIP = HAIR
CYAN = ECHO; CYAN_LIP = HAIR
WHITE = T1; WHITE_LIP = HAIR
GREY = '#4A5561'; GREY_LIP = HAIR
CARD = PLATE; CARD_LIP = HAIR
CREAM = T1; MUTED = T3

_FD = f'{ROOT}/fonts/montserrat'
# weight per component: titles/big numbers ExtraLight, headings Light, body Regular,
# readouts/tags Medium, kickers SemiBold
_TF = {
    'thin': 'Montserrat-ExtraLight.ttf', 'thin_it': 'Montserrat-ExtraLightItalic.ttf',
    'light': 'Montserrat-Light.ttf', 'light_it': 'Montserrat-LightItalic.ttf',
    'reg': 'Montserrat-Regular.ttf', 'med': 'Montserrat-Medium.ttf',
    'semi': 'Montserrat-SemiBold.ttf', 'bold': 'Montserrat-Bold.ttf',
    'serif': 'Montserrat-Light.ttf', 'serif_it': 'Montserrat-LightItalic.ttf',
}
_tfc, _fc = {}, {}
MIN_TEXT = 18

def font(kind, size):
    key = (kind, round(size, 1))
    if key not in _fc:
        if kind not in _tfc:
            _tfc[kind] = skia.Typeface.MakeFromFile(f'{_FD}/{_TF[kind]}')
        f = skia.Font(_tfc[kind], size)
        f.setSubpixel(True)
        f.setEdging(skia.Font.Edging.kAntiAlias)
        f.setHinting(skia.FontHinting.kNone)
        _fc[key] = f
    return _fc[key]

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def lin(t, t0, d):
    return clamp((t - t0) / d) if d > 0 else float(t >= t0)

def eio(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2

def eout(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3

def eback(x, s=1.6):
    return eout(x)  # no bounce in this treatment

def fade(t, t0, d=0.45, t1=None, d1=0.45):
    a = eout(lin(t, t0, d))
    if t1 is not None:
        a *= 1 - eio(lin(t, t1, d1))
    return a

def mix(a, b, k):
    return a + (b - a) * k

# ---------- paints ----------
def paint(color, a=1.0, stroke=None, blur=None, cap_round=True):
    r, g, b, a0 = hexc(color) if isinstance(color, str) else color
    p = skia.Paint(AntiAlias=True, Color4f=skia.Color4f(r, g, b, clamp(a0 * a)))
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        if cap_round:
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p

# ---------- type ----------
def _track(s, size, kind, track):
    if track is None:
        track = size * 0.14 if (s.upper() == s and any(ch.isalpha() for ch in s) and size <= 24) else 0.0
    return track

def text_width(s, size, kind='reg', track=None):
    size = max(size, MIN_TEXT)
    tr = _track(s, size, kind, track)
    return font(kind, size).measureText(s) + tr * max(len(s) - 1, 0)

def _draw_tracked(c, s, x, y, f, p, tr):
    if tr == 0:
        c.drawString(s, x, y, f, p)
        return
    for ch in s:
        c.drawString(ch, x, y, f, p)
        x += f.measureText(ch) + tr

def text(c, s, x, y, size, kind='reg', color=T1, a=1.0, align='left', glow=None, track=None, op=1.0):
    """Text is written on by a scan bar: `a` is the write progress (0..1), not an opacity."""
    if a <= 0.003 or op <= 0.003:
        return 0
    size = max(size, MIN_TEXT)          # phone floor: nothing on screen below ~1/72 of the frame height
    f = font(kind, size)
    tr = _track(s, size, kind, track)
    w = text_width(s, size, kind, tr)
    if align == 'center':
        x -= w / 2
    elif align == 'right':
        x -= w
    p = paint(color, op)
    halo = paint('#000000', op * 0.55, blur=max(2.0, size * 0.12))   # keeps small text legible over footage
    if a < 0.999:
        k = eout(a)
        xe = x + (w + 6) * k
        c.save(); c.clipRect(skia.Rect.MakeLTRB(x - 4, y - size * 1.2, xe, y + size * 0.5))
        _draw_tracked(c, s, x, y, f, halo, tr)
        _draw_tracked(c, s, x, y, f, p, tr)
        c.restore()
        c.drawLine(xe, y - size * 0.95, xe, y + size * 0.25, paint(SCAN, op * 0.9 * (1 - k * 0.6), stroke=1.2, cap_round=False))
    else:
        _draw_tracked(c, s, x, y, f, halo, tr)
        _draw_tracked(c, s, x, y, f, p, tr)
    return w

def wrap(s, size, kind, maxw):
    words, lines, cur = s.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if text_width(t, size, kind) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines

def text_block(c, s, x, y, size, maxw, kind='reg', color=T1, a=1.0, lh=1.42, align='left', op=1.0):
    lines = wrap(s, size, kind, maxw)
    n = len(lines)
    for i, ln in enumerate(lines):
        ai = clamp(a * n - i) if a < 0.999 else 1.0
        text(c, ln, x, y + i * size * lh, size, kind, color, ai, align, op=op)

# ---------- plates, labels, frames ----------
def ticks(c, x, y, w, h, color=ECHO, a=1.0, L=12):
    p = paint(color, a, stroke=1.3, cap_round=False)
    for (px, py, dx, dy) in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        c.drawLine(px, py, px + L * dx, py, p); c.drawLine(px, py, px, py + L * dy, p)

def chunk(c, x, y, w, h, fill=PLATE, lip=None, a=1.0, r=None, lift=None, stroke=None, glow=None):
    """A reading plate: near-black, hairline border, corner ticks. Accent fills become thin tinted frames."""
    if a <= 0.003:
        return
    if fill in (PLATE, CARD) or fill.lower() in ('#070b10', '#10262b', '#132c31'):
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(PLATE, 0.86 * a))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(HAIR, a, stroke=1))
        ticks(c, x, y, w, h, stroke or ECHO, a * 0.55)
    else:
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(fill, a * 0.14))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(fill, a * 0.9, stroke=1.2))

def hatch(c, x, y, w, h, color=GREY, a=1.0, r=0, gap=10, width=1):
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    p = paint(color, a * 0.7, stroke=width, cap_round=False)
    k = -h
    while k < w:
        c.drawLine(x + k, y + h, x + k + h, y, p)
        k += gap
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(color, a, stroke=1))

def chip(c, x, y, label, fill=PLATE, lip=None, fg=T1, a=1.0, size=15, kind='med', pad=14, h=None, dot=None, align='left', hatched=False, outline=True):
    """A small all-caps reading in a hairline frame."""
    s = label.upper()
    size = min(size, 18)
    w = text_width(s, size, kind) + pad * 2 + (18 if dot else 0)
    h = h or size * 2.1
    if align == 'center':
        x -= w / 2
    elif align == 'right':
        x -= w
    if a <= 0.003:
        return w
    k = eout(a)
    if hatched:
        hatch(c, x, y, w * k, h, GREY, 1.0, gap=8)
    elif outline:
        c.drawRect(skia.Rect.MakeXYWH(x, y, w * k, h), paint(PLATE, 0.8))
        edge = fg if fill not in (PLATE, CARD) else HAIR
        c.drawRect(skia.Rect.MakeXYWH(x, y, w * k, h), paint(edge, 0.9, stroke=1))
    tx = x + pad
    if dot:
        c.drawRect(skia.Rect.MakeXYWH(tx, y + h / 2 - 3, 6, 6), paint(dot, k))
        tx += 18
    text(c, s, tx, y + h / 2 + size * 0.36, size, kind, fg, a)
    return w

def source_tag(c, s, x, y, a=1.0, align='left', size=14):
    text(c, s, x, y, size, 'reg', T3, a, align, track=0.3)

LABEL_COL = {'MODELLED': ECHO, 'MEASURED': T1, 'DESIGN CONCEPT': T3, 'MISSING': GREY}

def label_tag(c, kind, x, y, a=1.0, align='left'):
    """MODELLED / MEASURED / DESIGN CONCEPT / MISSING evidence labels."""
    col = LABEL_COL[kind.split(' ·')[0]]
    return chip(c, x, y, kind, col, None, col, a, size=14, kind='semi', pad=12, dot=col)

def leader(c, x0, y0, x1, y1, a=1.0, color=T3):
    k = eout(a)
    c.drawLine(x0, y0, mix(x0, x1, k), mix(y0, y1, k), paint(color, 0.7, stroke=1, cap_round=False))

# ---------- the Line of Evidence ----------
def polyline_len(pts):
    pts = np.asarray(pts, float)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    return pts, np.concatenate([[0], np.cumsum(seg)])

def partial(pts, p, p0=0.0):
    pts, cum = polyline_len(pts)
    L = cum[-1]
    if L <= 0 or p <= p0:
        return None, None
    def at(s):
        i = int(np.clip(np.searchsorted(cum, s) - 1, 0, len(pts) - 2))
        k = (s - cum[i]) / max(cum[i + 1] - cum[i], 1e-9)
        return pts[i] + (pts[i + 1] - pts[i]) * k, i
    s0, s1 = p0 * L, clamp(p) * L
    a0, i0 = at(s0)
    a1, i1 = at(s1)
    out = [a0] + [pts[j] for j in range(i0 + 1, i1 + 1)] + [a1]
    return out, a1

def line(c, pts, p=1.0, color=ECHO, width=2.0, a=1.0, head=True, p0=0.0, glow=True):
    """The one shared function that draws the evidence line, everywhere in the film."""
    if a <= 0.003:
        return None
    sub, hd = partial(pts, p, p0)
    if sub is None:
        return None
    path = skia.Path()
    path.moveTo(*sub[0])
    for q in sub[1:]:
        path.lineTo(*q)
    w = min(width, 2.4)
    if glow:
        c.drawPath(path, paint(color, a * 0.28, stroke=w * 4, blur=w * 2.2))
    c.drawPath(path, paint(color, a, stroke=w))
    if head and p < 0.999:
        c.drawCircle(hd[0], hd[1], 7, paint(SCAN, a * 0.5, blur=6))
        c.drawCircle(hd[0], hd[1], 2.6, paint(SCAN, a))
    return hd

def bezier(p0, p1, p2, p3, n=48):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.asarray, (p0, p1, p2, p3))
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3).tolist()

def node(c, x, y, r=14, a=1.0, color=WARM, lip=None, sx=1.0, sy=1.0, glow=True, t=None):
    """Target marker: a warm point with a ring, and slow range rings when t is given."""
    if a <= 0.003:
        return
    c.drawCircle(x, y, 9, paint(color, a * 0.45, blur=8))
    c.drawCircle(x, y, 3.6, paint(color, a))
    c.drawCircle(x, y, r * 0.8, paint(color, a * 0.85, stroke=1.3))
    if t is not None:
        for i in range(2):
            k = ((t * 0.45 + i * 0.5) % 1.0)
            c.drawCircle(x, y, r + 70 * k, paint(color, a * 0.5 * (1 - k), stroke=1))

def ping(c, x, y, t, t0, R=900, dur=2.4, a=1.0, color=ECHO, rings=3):
    """Radial ping: a ring of light runs out from the source; echoes decay behind it."""
    k = lin(t, t0, dur)
    if k <= 0 or k >= 1:
        return
    r = R * eout(k)
    c.drawCircle(x, y, r, paint(color, a * (1 - k) * 0.35, stroke=10, blur=8))
    c.drawCircle(x, y, r, paint(SCAN, a * (1 - k), stroke=1.4))
    for i in range(1, rings + 1):
        rr = r - i * 70
        if rr > 0:
            c.drawCircle(x, y, rr, paint(color, a * (1 - k) * 0.45 / i, stroke=1))

# ---------- images ----------
_img = {}
def image(path, crop=None, grade=None):
    key = (path, crop, grade)
    if key not in _img:
        import cv2
        arr = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGBA if arr.shape[2] == 3 else cv2.COLOR_BGRA2RGBA)
        if crop:
            x0, y0, x1, y1 = crop
            arr = arr[y0:y1, x0:x1]
        rgb = arr[..., :3].astype(np.float32) / 255
        if grade in ('cold', 'cold_dark'):   # scanned look: low-key cold monochrome with a little colour left
            lum = rgb @ np.array([0.3, 0.59, 0.11], np.float32)
            lum = np.clip((lum - 0.16) * 1.35, 0, 1) ** 1.5
            mono = lum[..., None] * np.array([0.58, 0.74, 0.92], np.float32) * (0.66 if grade == 'cold_dark' else 0.82)
            rgb = mono * 0.85 + rgb * 0.15 * lum[..., None]
        elif grade == 'desat':
            lum = (rgb @ np.array([0.3, 0.59, 0.11], np.float32))[..., None]
            rgb = (rgb * 0.7 + lum * 0.3) * 0.92
        elif isinstance(grade, tuple):
            k, tint = grade
            rgb = rgb * k + np.array(tint, np.float32) / 255
        arr[..., :3] = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
        _img[key] = skia.Image.fromarray(np.ascontiguousarray(arr), colorType=skia.kRGBA_8888_ColorType)
    return _img[key]

def draw_image(c, img, x, y, w, h, a=1.0, r=0, scan='x'):
    """Images are revealed by a scan front (a = reveal progress), never faded in."""
    if a <= 0.003:
        return
    k = eio(a) if a < 0.999 else 1.0
    c.save()
    if scan == 'x':
        c.clipRect(skia.Rect.MakeXYWH(x, y, w * k, h))
    else:
        c.clipRect(skia.Rect.MakeXYWH(x, y, w, h * k))
    c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), skia.Paint(AntiAlias=True))
    c.restore()
    if k < 1:
        if scan == 'x':
            xe = x + w * k
            c.drawLine(xe, y, xe, y + h, paint(ECHO, 0.5, stroke=10, blur=8))
            c.drawLine(xe, y, xe, y + h, paint(SCAN, 0.95, stroke=1.4, cap_round=False))
        else:
            ye = y + h * k
            c.drawLine(x, ye, x + w, ye, paint(ECHO, 0.5, stroke=10, blur=8))
            c.drawLine(x, ye, x + w, ye, paint(SCAN, 0.95, stroke=1.4, cap_round=False))

# ---------- footage from the 3D art (graded, read sequentially) ----------
class Footage:
    _open = {}

    def __init__(self, path, grade='cold', scale=1.0):
        self.path, self.grade = path, grade
        self.idx, self.img = -1, None

    @classmethod
    def get(cls, path, grade='cold'):
        key = (path, grade)
        if key not in cls._open:
            cls._open[key] = Footage(path, grade)
        return cls._open[key]

    def frame(self, sec):
        import cv2
        if not hasattr(self, 'cap'):
            self.cap = cv2.VideoCapture(self.path)
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        i = int(clamp(sec * self.fps, 0, self.n - 1))
        if i == self.idx or (i < self.idx and self.img is not None and self.idx - i < 3):
            return self.img
        if i != self.idx + 1:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, bgr = self.cap.read()
        if not ok:
            return self.img
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255
        if self.grade in ('cold', 'cold_dark'):
            lum = rgb @ np.array([0.3, 0.59, 0.11], np.float32)
            lum = np.clip((lum - 0.16) * 1.35, 0, 1) ** 1.5
            rgb = lum[..., None] * np.array([0.58, 0.74, 0.92], np.float32) * (0.66 if self.grade == 'cold_dark' else 0.82) * 0.85 + rgb * 0.15 * lum[..., None]
        elif self.grade == 'globe':
            lum = rgb @ np.array([0.3, 0.59, 0.11], np.float32)
            rgb = lum[..., None] * np.array([0.5, 0.68, 0.9], np.float32) * 0.75
        rgba = np.dstack([(np.clip(rgb, 0, 1) * 255).astype(np.uint8), np.full(rgb.shape[:2], 255, np.uint8)])
        self.img = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)
        self.idx = i
        return self.img

def draw_footage(c, path, sec, x=0, y=0, w=1920, h=1080, reveal=1.0, grade='cold', scan='x'):
    img = Footage.get(path, grade).frame(sec)
    if img is not None:
        draw_image(c, img, x, y, w, h, reveal, scan=scan)
