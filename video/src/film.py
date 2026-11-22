"""One continuous camera flight over flat scene faces, rendered with skia under true perspective."""
import math, os, subprocess, sys, json
import numpy as np
import skia
sys.path.insert(0, os.path.dirname(__file__))
import gfx
from gfx import W, H, ROOT, hexc, clamp, lin, eio, mix
import scenes
import shots
from timeline import build

FPS = 24
F = 1600.0
NEAR = 40.0
TL = build()
S = TL['start']; T = TL['T']

X, Y, Z = np.eye(3)

class Face:
    def __init__(self, name, O, U, V, w, h, draw):
        self.name, self.O, self.U, self.V, self.w, self.h, self.draw = name, np.array(O, float), np.array(U, float), np.array(V, float), w, h, draw
        self.N = np.cross(self.U, self.V)

    def world(self, u, v):
        return self.O + u * self.U + v * self.V

def _s4(c, t, tl):
    shots.s4(c, t, tl, clip_k=eio(lin(t, S['S5'] - 0.7, 1.3)))

FACES = [
    Face('S1', (0, 0, 0), X, Y, 1920, 1080, shots.s1),
    Face('S2', (3000, -500, 700), X, Y, 1920, 1080, shots.s2),
    Face('S3', (6200, 0, 0), X, Y, 1920, 3240, shots.s3),
    Face('S4', (6200, 3800, 0), X, Y, 1920, 1080, _s4),
    Face('S5', (6200, 3800 + scenes.S4_AB, -scenes.WATER_Y), X, Z, 1920, 1080, shots.s5),
    Face('S6', (9400, 3800, 0), X, Y, 1920, 1080, shots.s6),
    Face('S7', (12200, 3800, 0), X, Y, 1920, 1080, shots.s7),
    Face('S8', (12200, 5100, 0), X, Y, 1920, 1080, shots.s8),
]
FD = {f.name: f for f in FACES}
ACTIVE = {'S1': (None, 'S2'), 'S2': ('S1', 'S3'), 'S3': ('S2', 'S5'), 'S4': ('S3', 'S6'), 'S5': ('S4', 'S6'),
          'S6': ('S5', 'S7'), 'S7': ('S6', 'S8'), 'S8': ('S7', None)}

# ---------- camera ----------
def home(face, u=960, v=540, zoom=1.0):
    f = FD[face]
    P = f.world(u, v)
    C = P - f.N * (F / zoom)
    R = np.stack([f.U, f.V, f.N])
    return C, R

def quat(R):
    m = R.T
    tr = m.trace()
    if tr > 0:
        s = math.sqrt(tr + 1) * 2
        q = [0.25 * s, (m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s, (m[1, 0] - m[0, 1]) / s]
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        q = [(m[2, 1] - m[1, 2]) / s, 0.25 * s, (m[0, 1] + m[1, 0]) / s, (m[0, 2] + m[2, 0]) / s]
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        q = [(m[0, 2] - m[2, 0]) / s, (m[0, 1] + m[1, 0]) / s, 0.25 * s, (m[1, 2] + m[2, 1]) / s]
    else:
        s = math.sqrt(1 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        q = [(m[1, 0] - m[0, 1]) / s, (m[0, 2] + m[2, 0]) / s, (m[1, 2] + m[2, 1]) / s, 0.25 * s]
    return np.array(q)

def qmat(q):
    w, x, y, z = q / np.linalg.norm(q)
    m = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    return m.T

def slerp(q0, q1, k):
    d = float(np.dot(q0, q1))
    if d < 0:
        q1, d = -q1, -d
    if d > 0.9995:
        return q0 + (q1 - q0) * k
    th = math.acos(d)
    return (math.sin((1 - k) * th) * q0 + math.sin(k * th) * q1) / math.sin(th)

def keyframes():
    K = []
    def hold(t, pose):
        K.append((t, pose))
    hold(0.0, home('S1', 960, 540, 1.0))
    hold(S['S2'] - 0.6, home('S1', 960, 540, 1.04))
    def fly(t0, t1, pose):
        K.append((t0, K[-1][1])); K.append((t1, pose))
    fly(S['S2'] - 0.5, S['S2'] + 1.0, home('S2'))
    fly(S['S3'] - 0.5, S['S3'] + 1.0, home('S3', 960, 540))
    fly(T['c1'] - 0.9, T['c1'] + 0.3, home('S3', 960, 1620))
    fly(T['c2'] - 1.1, T['c2'] + 0.1, home('S3', 960, 2700))
    fly(S['S4'] - 0.5, S['S4'] + 0.9, home('S4'))
    fly(S['S5'] - 0.7, S['S5'] + 1.5, home('S5'))
    fly(S['S6'] - 0.5, S['S6'] + 1.1, home('S6'))
    fly(S['S7'] - 0.5, S['S7'] + 1.0, home('S7'))
    fly(S['S8'] - 0.4, S['S8'] + 1.0, home('S8'))
    return K

KF = keyframes()

def camera(t):
    if t <= KF[0][0]:
        C, R = KF[0][1]
    elif t >= KF[-1][0]:
        C, R = KF[-1][1]
    else:
        i = max(j for j in range(len(KF) - 1) if KF[j][0] <= t)
        (t0, (C0, R0)), (t1, (C1, R1)) = KF[i], KF[i + 1]
        k = eio((t - t0) / max(t1 - t0, 1e-6))
        C = C0 + (C1 - C0) * k
        dist = np.linalg.norm(C1 - C0)
        fwd = R0[2] + R1[2]
        if np.linalg.norm(fwd) > 1e-3 and dist > 1:
            C = C - fwd / np.linalg.norm(fwd) * 0.16 * dist * math.sin(math.pi * k)
        R = qmat(slerp(quat(R0), quat(R1), k))
    return C, R

def project(C, R, P):
    p = R @ (P - C)
    if p[2] < NEAR:
        return None
    return (F * p[0] / p[2] + W / 2, F * p[1] / p[2] + H / 2)

def homography(C, R, f):
    Kc = np.array([[F, 0, W / 2], [0, F, H / 2], [0, 0, 1]])
    Hm = Kc @ np.stack([R @ f.U, R @ f.V, R @ (f.O - C)], axis=1)
    Hm = Hm / Hm[2, 2] if abs(Hm[2, 2]) > 1e-9 else Hm
    return skia.Matrix.MakeAll(Hm[0, 0], Hm[0, 1], Hm[0, 2], Hm[1, 0], Hm[1, 1], Hm[1, 2], Hm[2, 0], Hm[2, 1], Hm[2, 2])

def depth(C, R, P):
    return (R @ (P - C))[2]

def draw_face(c, C, R, f, t):
    m = 0.45 if f.name == 'S5' else 1.6
    if f.name == 'S1' and t > S['S2'] + 1.0:
        return
    if t < S[f.name] - m or t > TL['end'][f.name] + (1.6 if f.name != 'S4' else 1.8):
        return
    corners = [f.world(u, v) for u, v in ((0, 0), (f.w, 0), (0, f.h), (f.w, f.h))]
    zs = [depth(C, R, P) for P in corners]
    if max(zs) < NEAR:
        return
    if f.name == 'S4' and C[2] > -60:
        return  # camera has passed beneath the overhead plane during the orbit
    pts = [project(C, R, P) for P in corners]
    if all(p is not None for p in pts):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if max(xs) < -50 or min(xs) > W + 50 or max(ys) < -50 or min(ys) > H + 50:
            return
        c.save(); c.concat(homography(C, R, f)); f.draw(c, t, TL); c.restore()
        return
    n = 8  # partially behind the camera: draw only the grid cells in front
    for i in range(n):
        for j in range(n):
            u0, u1 = f.w * i / n, f.w * (i + 1) / n
            v0, v1 = f.h * j / n, f.h * (j + 1) / n
            if all(depth(C, R, f.world(u, v)) > NEAR for u, v in ((u0, v0), (u1, v0), (u0, v1), (u1, v1))):
                c.save(); c.concat(homography(C, R, f)); c.clipRect(skia.Rect.MakeLTRB(u0, v0, u1, v1)); f.draw(c, t, TL); c.restore()

CONNECT = []  # documentary cut: shots change by scan wipes and camera moves, no connector lines

def draw_connectors(c, C, R, t):
    for fa, pa, fb, pb, t0, d in CONNECT:
        k = eio(lin(t, t0, d))
        if k <= 0 or t > t0 + d + 4:
            continue
        A, B = FD[fa].world(*pa), FD[fb].world(*pb)
        dist = np.linalg.norm(B - A)
        c1 = A - FD[fa].N * 0.25 * dist + (B - A) * 0.25
        c2 = B - FD[fb].N * 0.25 * dist - (B - A) * 0.25
        ts = np.linspace(0, 1, 60)[:, None]
        P = (1 - ts) ** 3 * A + 3 * (1 - ts) ** 2 * ts * c1 + 3 * (1 - ts) * ts ** 2 * c2 + ts ** 3 * B
        scr = [project(C, R, p) for p in P]
        run = [s for s in scr if s is not None]
        if len(run) > 2:
            gfx.line(c, run, k, a=1.0)

# ---------- stage, grain, vignette ----------
def _stage():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.array(hexc(gfx.STAGE)[:3], np.float32) * 255
    g = np.exp(-(((xx - W * 0.55) / (W * 0.55)) ** 2 + ((yy - H * 0.35) / (H * 0.6)) ** 2))
    img = base[None, None, :] + g[..., None] * np.array([2, 6, 10], np.float32)
    vig = 1 - 0.38 * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2, 0, 1) ** 1.3
    rgba = np.dstack([img, np.full((H, W), 255, np.float32)]).astype(np.uint8)
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType), vig[..., None]

STAGE_IMG, VIG = None, None
GRAIN = None

def render_once(surface, t):
    c = surface.getCanvas()
    c.clear(skia.Color4f(*hexc(gfx.STAGE)))
    c.drawImage(STAGE_IMG, 0, 0)
    C, R = camera(t)
    for f in FACES:
        f.draw_t = t
        draw_face(c, C, R, f, t)
    draw_connectors(c, C, R, t)
    return surface.makeImageSnapshot().toarray()[..., :3]

def cam_speed(t):
    C0, R0 = camera(t); C1, R1 = camera(t - 1 / 60)
    return np.linalg.norm(C0 - C1) + 1600 * np.linalg.norm(R0 - R1)

def frame(surface, t, idx):
    sp = cam_speed(t)
    if sp > 6:
        n = int(clamp(sp / 5, 2, 12))
        acc = np.zeros((H, W, 3), np.float32)
        for k in range(n):
            acc += render_once(surface, t - k / (60 * n))
        img = acc / n
    else:
        img = render_once(surface, t).astype(np.float32)
    img = img * VIG + GRAIN[idx % len(GRAIN)]
    return np.clip(img, 0, 255).astype(np.uint8)

def init():
    global STAGE_IMG, VIG, GRAIN
    STAGE_IMG, VIG = _stage()
    rng = np.random.default_rng(5)
    GRAIN = [rng.uniform(-0.8, 0.8, (H, W, 1)).astype(np.float32)]  # static sub-LSB dither, no moving grain

def make_surface():
    return skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))

def render_chunk(args):
    i0, i1, path = args
    init()
    surf = make_surface()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for i in range(i0, i1):
        p.stdin.write(frame(surf, i / FPS, i).tobytes())
    p.stdin.close(); p.wait()
    return path

def stills(times, outdir):
    import cv2
    init(); surf = make_surface()
    os.makedirs(outdir, exist_ok=True)
    for t in times:
        img = frame(surf, t, 0)
        cv2.imwrite(f'{outdir}/t{t:07.2f}.jpg', cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        stills([float(x) for x in sys.argv[2].split(',')], f'{ROOT}/out/stills')
    elif sys.argv[1] == 'render':
        from multiprocessing import Pool
        t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0
        t1 = float(sys.argv[3]) if len(sys.argv) > 3 else TL['total']
        n0, n1 = int(t0 * FPS), int(math.ceil(t1 * FPS))
        workers = 10
        step = math.ceil((n1 - n0) / workers)
        os.makedirs(f'{ROOT}/out/chunks', exist_ok=True)
        jobs = [(a, min(a + step, n1), f'{ROOT}/out/chunks/c{a:06d}.mp4') for a in range(n0, n1, step)]
        with Pool(workers) as pool:
            paths = pool.map(render_chunk, jobs)
        with open(f'{ROOT}/out/chunks/list.txt', 'w') as fh:
            for pth in paths:
                fh.write(f"file '{pth}'\n")
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{ROOT}/out/chunks/list.txt', '-c', 'copy', f'{ROOT}/out/silent.mp4'], check=True)
        print('done', n1 - n0, 'frames')
