 // i18n-skip: shader comments, not UI
#include <packing>
uniform sampler2D tNormal;
uniform sampler2D tDepth;
uniform vec2 uEdgeRes;      // edge/prepass target size (px)
uniform vec2 uRes;          // screen size (px) — the wobble field lives in screen pixels at any supersampling
uniform float uNear, uFar;
uniform vec2 uFog;           // the scene's linear fog (near, far): the lines sink into the haze with the fills
uniform vec2 uTanHalf;       // tan of the camera's half field of view (x, y): the view ray of a pixel
uniform float uBoil;
uniform float uEdgeLine;    // line radius in prepass px (= uLine × supersampling)
uniform float uWobble;      // screen px
uniform float uDetail;      // 0..1 how strongly small far detail loses its lines
uniform float uInner;       // 0..1 interior crease lines (window frames, panels); silhouettes and steps always stay
uniform float uNrmOct;      // 1: tNormal is the two-byte octahedral prepass (NRM_OCT), 0: xyz in four bytes
varying vec2 vUv;
${$}
${Ye}
vec3 nrmOf(vec4 t) { return uNrmOct > 0.5 ? ik_octDec(t.xy) : t.xyz * 2.0 - 1.0; }
float viewZ(vec2 uv) {
  float d = texture2D(tDepth, uv).x;
  return -perspectiveDepthToViewZ(d, uNear, uFar);
}
vec3 nrm(vec2 uv) { return nrmOf(texture2D(tNormal, uv)); }

float edgeAt(vec2 uv) {
  vec2 t = uEdgeLine / uEdgeRes;
  float zc = viewZ(uv);
  if (zc > uFar * 0.98) {
    // sky pixel: only outline if a neighbor is geometry (silhouette handled from geometry side)
    return 0.0;
  }
  float zl = viewZ(uv - vec2(t.x, 0.0)), zr = viewZ(uv + vec2(t.x, 0.0));
  float zd = viewZ(uv - vec2(0.0, t.y)), zu = viewZ(uv + vec2(0.0, t.y));
#ifdef IK_EDGE_CROSS
  // (a phone's thin pen, IK_EDGE_CROSS: the diagonal depth taps left out — 4 of the pass's 18 texture reads)
  float zdl = zc, zur = zc, zdr = zc, zul = zc;
#else
  float zdl = viewZ(uv + vec2(-t.x, -t.y)), zur = viewZ(uv + vec2(t.x, t.y));
  float zdr = viewZ(uv + vec2(t.x, -t.y)), zul = viewZ(uv + vec2(-t.x, t.y));
#endif
  // second derivative of INVERSE depth: 1/z of any plane is linear in screen space, so planes give exactly 0 — even
  // ground at a grazing angle near the horizon, whose z itself bends like a hyperbola (the old z-laplacian / z grew as
  // z²/h² there and its threshold drew soft iso-lines over the far fields: «waves» at eye level and over the hills).
  // × zc keeps the scale of the old measure for creases (Δ(1/z) ≈ −Δz / z²), silhouettes stay large.
  float iz = 1.0 / zc;
  float lap = abs(1.0 / zl + 1.0 / zr - 2.0 * iz) + abs(1.0 / zd + 1.0 / zu - 2.0 * iz)
            + 0.5 * (abs(1.0 / zdl + 1.0 / zur - 2.0 * iz) + abs(1.0 / zdr + 1.0 / zul - 2.0 * iz));
  // silhouette against sky: neighbor is background
  float far = uFar * 0.98;
  float sil = max(max(step(far, zl), step(far, zr)), max(step(far, zd), step(far, zu)));
  vec4 n0 = texture2D(tNormal, uv), nl = texture2D(tNormal, uv - vec2(t.x, 0.0)), nr = texture2D(tNormal, uv + vec2(t.x, 0.0));
  vec4 nd = texture2D(tNormal, uv - vec2(0.0, t.y)), nu = texture2D(tNormal, uv + vec2(0.0, t.y));
  vec3 nc = nrmOf(n0);
  // a surface seen almost edge-on (the ground from eye level, far fields and slopes) turns its gentle real relief into
  // large depth curvature on screen: the small-crease band of the test fired over whole patches of meadow — soft dark
  // rings and arcs («волны» in the walk). There only real steps count (a hill's crest over the land behind, a kerb
  // from the side); every other surface keeps the full test.
  vec3 ray = normalize(vec3((uv * 2.0 - 1.0) * uTanHalf, -1.0));
  float graze = smoothstep(0.05, 0.2, abs(dot(nc, ray)));
  float lz = lap * zc;
  float de = max(smoothstep(0.012, 0.035, lz) * graze, smoothstep(0.25, 0.5, lz));
  float ne = 0.0;
  ne = max(ne, 1.0 - dot(nc, nrmOf(nl)));
  ne = max(ne, 1.0 - dot(nc, nrmOf(nr)));
  ne = max(ne, 1.0 - dot(nc, nrmOf(nd)));
  ne = max(ne, 1.0 - dot(nc, nrmOf(nu)));
  float nE = smoothstep(0.22, 0.45, ne) * uInner;
  // the pen skips small detail far away: a normal crease stays only if the surfaces ~2 screen px to either side
  // still differ (a real wall corner, ridge, eave). Window frames, recess sides, tile rows — thinner than that on
  // screen — fade out with depth instead of flickering as sub-pixel lines while the camera moves.
  float dsup = uDetail * smoothstep(80.0, 230.0, zc);
  if (dsup > 0.001 && nE > 0.001) {
    vec2 R = 2.0 / uRes;                       // 2 screen px (in uv), at any supersampling
    float wx = 1.0 - dot(nrm(uv - vec2(R.x, 0.0)), nrm(uv + vec2(R.x, 0.0)));
    float wy = 1.0 - dot(nrm(uv - vec2(0.0, R.y)), nrm(uv + vec2(0.0, R.y)));
    nE *= mix(1.0, smoothstep(0.12, 0.3, max(wx, wy)), dsup);
  }
  // lines fade & thin with distance (like a pen lifting on far detail)
  float dist = smoothstep(160.0, 900.0, zc);
  // …and vanish into the haze exactly as the fills do (three's linear fog: smoothstep over view depth). Without it the
  // far mountains' ridges and creases stayed at 35 % ink over fills already gone to sky colour: «waves» hanging in the sky
  float haze = uFog.y > uFog.x ? smoothstep(uFog.x, uFog.y, zc) : 0.0;
  // no ink on and around what asks for none (alpha 0 in the normal target: the artist people drawn without lines,
  // traffic/crowd ?lpink=0) — lines behind them stop at their edge instead of crossing them
  float keep = step(0.5, min(min(n0.a, nl.a), min(min(nr.a, nd.a), nu.a)));
  return max(max(de, nE), sil) * (1.0 - dist * 0.65) * (1.0 - haze) * keep;
}

void main() {
  // the hand wobble only when there is one: every player's look («Тушь и размывка», core/look.js) has none, and its two
  // value noises per pixel were multiplied by 0 — a quarter of this pass at «Ультра»'s 6400 × 3600 (2.56 → 1.95 ms, the
  // ink the same to the last texel, 2026-11-07); a uniform's branch: every pixel takes the same way
  vec2 uvw = vUv;
  if (uWobble > 0.0) {
    vec2 px = vUv * uRes;
    vec2 wob = vec2(n2(px / 70.0 + uBoil * 13.1), n2(px / 70.0 + 31.7 + uBoil * 7.3)) - 0.5;
    uvw += wob * 2.0 * uWobble / uRes;
  }
  gl_FragColor = vec4(edgeAt(uvw), 0.0, 0.0, 1.0);
}
