
uniform sampler2D tColor;
uniform sampler2D tInk;
uniform sampler2D tPaper;    // baked screen-static layers (PAPER_FRAG)
uniform vec2 uRes;
uniform vec2 uEdgeRes;
uniform float uInkTent;     // 1 = tent-filtered ink (4 bilinear taps), 0 = plain box (1 tap)
uniform float uInkTentR;    // the tent's tap offset in ink texels (0.75: the desktop's supersampled ink)
uniform float uInkCrisp;    // 1 = the ink comes from a smaller target: its bilinear edge is cut back to a one-pixel edge
uniform float uBoil;
uniform float uLineAlpha;
uniform float uPen;         // 0..1 strength of the pen pressure / break modulation
uniform vec3 uInk;
uniform vec3 uSkyTop, uSkyBot, uSkyHatch;
uniform float uNight;
uniform float uVignette;
uniform float uPaper;
uniform float uTime;
uniform float uSkyHatchK;
uniform float uStain;
uniform float uGrade, uExpo, uSat, uCon, uLift, uShK, uHiK;   // (env/looks.js, an experiment) the light look's colour grade
uniform vec3 uShTint, uHiTint;
varying vec2 vUv;
${$}
void main() {
  vec4 col = texture2D(tColor, vUv);
  vec4 pap = texture2D(tPaper, vUv);

  // ---- sky (behind everything) ----
  float gy = vUv.y;
  vec3 sky = mix(uSkyBot, uSkyTop, smoothstep(0.0, 1.0, gy));
  // pencil hatch on the sky, diagonal strokes (screen space, like a drawn background; baked)
  sky = mix(sky, uSkyHatch, pap.x * uSkyHatchK);
  // (max: an additive glow — a signal's or a lamp's halo — writes alpha past 1 into the float target; 1 − a went negative
  // and took the sky off the street under it: a black blot round every lit signal, owner 2026-10-26)
  vec3 base = col.rgb + sky * max(0.0, 1.0 - col.a);

  // ---- ink lines (coverage from the edge pass; bilinear fetch = box filter of the supersampled lines) ----
  float e;
  if (uInkTent > 0.5) {
    // separable tent over 4×4 prepass texels (weights .25 .75 .75 .25) = 4 bilinear taps at ±0.75 texel: a softer
    // reconstruction filter than the 2×2 box, so a line sliding by a fraction of a pixel changes its pixels smoothly
    vec2 o = uInkTentR / uEdgeRes;
    e = 0.25 * (texture2D(tInk, vUv + vec2(-o.x, -o.y)).r + texture2D(tInk, vUv + vec2(o.x, -o.y)).r
              + texture2D(tInk, vUv + vec2(-o.x, o.y)).r + texture2D(tInk, vUv + vec2(o.x, o.y)).r);
    e = min(1.0, e * mix(1.0, 1.12, uInkTentR / 0.75));   // the wider filter spreads a thin line a little: keep its ink as dark as before
  } else e = texture2D(tInk, vUv).r;
  if (uInkCrisp > 0.0) {
    // the coverage upscaled from the 3D pass's smaller target is a soft ramp; its 0.5 crossing is the line's edge: cut
    // it to a screen pixel (fwidth) — faint strokes keep their own tone (max), lines get the full screen sharpness
    float fw = clamp(fwidth(e), 0.08, 0.6);
    e = mix(e, max(smoothstep(0.5 - 0.5 * fw, 0.5 + 0.5 * fw, e), e), uInkCrisp);
  }
  // pen pressure / breaks (baked)
  float ink = clamp(e * mix(1.0, pap.y, uPen), 0.0, 1.0) * uLineAlpha;
  // at night the fills get dark, so the pen goes darker (a touch blue) too; otherwise outlines read as light halos
  // around trees and buildings. NB these are LINEAR values: the old (0.075, 0.07, 0.12) is sRGB ≈ (77, 74, 97) —
  // lighter than the night walls, so every outline and thin object (bench slats, railings) turned pale lavender.
  vec3 inkCol = mix(uInk, vec3(0.011, 0.010, 0.019), uNight);
  // (the pen never comes out lighter than the surface under it: on a dark night wall — a gothic castle under a gloomy
  // filter — the fixed night ink read as pale grey outlines, owner 2026-10-26)
  inkCol = min(inkCol, base * 0.45);
  vec3 c = mix(base, inkCol, ink);

  // ---- paper (baked) ----
  c *= mix(1.0, pap.z, uPaper);
  c *= mix(vec3(1.0), mix(vec3(1.0), vec3(0.97, 0.94, 0.89), pap.w), uPaper * uStain);

  // ---- colour grade (a light look: exposure, contrast about mid grey, split tone, saturation, film lift) ----
  if (uGrade > 0.5) {
    c *= uExpo;
    float gl = dot(c, vec3(0.2126, 0.7152, 0.0722));
    c = 0.18 * pow(max(c, 0.0) / 0.18, vec3(uCon));
    vec3 sht = uShTint / max(0.01, dot(uShTint, vec3(0.2126, 0.7152, 0.0722)));
    vec3 hit = uHiTint / max(0.01, dot(uHiTint, vec3(0.2126, 0.7152, 0.0722)));
    float hl = smoothstep(0.05, 0.6, gl);
    c *= mix(vec3(1.0), sht, uShK * (1.0 - hl)) * mix(vec3(1.0), hit, uHiK * hl);
    float l2 = dot(c, vec3(0.2126, 0.7152, 0.0722));
    c = max(mix(vec3(l2), c, uSat), 0.0);
    c = uLift + c * (1.0 - uLift);
  }

  // ---- vignette ----
  vec2 q = vUv - 0.5;
  float v = smoothstep(0.35, 0.95, length(q * vec2(uRes.x / uRes.y, 1.0) * 0.9));
  c = mix(c, c * vec3(0.78, 0.7, 0.62), v * uVignette);

  gl_FragColor = vec4(c, 1.0);
  #include <colorspace_fragment>
}
