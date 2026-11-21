
uniform vec2 uRes;
uniform float uBoil;
uniform float uPaperK;      // screen px per paper px: max(1, pixel ratio / 2) — a phone's 3× keeps the grain of a 2× screen
varying vec2 vUv;
${$}
void main() {
  vec2 px = vUv * uRes / uPaperK;
  float hd = dot(px, normalize(vec2(1.0, 0.62))) / 7.0;
  float lineId = floor(hd);
  float hs = abs(fract(hd + (n2(vec2(dot(px, vec2(-0.62, 1.0)) * 0.012, lineId)) - 0.5) * 0.5) - 0.5);
  float strokes = (1.0 - smoothstep(0.06, 0.2, hs)) * step(0.35, n2(vec2(dot(px, vec2(-0.62, 1.0)) * 0.01 + lineId * 3.7, lineId)));
  float boil = uBoil;
  float press = 0.72 + 0.28 * n2(px / 22.0 + boil * 5.0);
  float br = smoothstep(0.08, 0.2, n2(px / 9.0 + boil * 3.0 + 50.0));
  float g = n2(px * 0.9) * 0.45 + n2(px * 0.31) * 0.3 + n2(px * 0.045) * 0.25;
  float fib = smoothstep(0.93, 1.0, n2(vec2(px.x * 0.04 + px.y * 0.25, px.y * 0.04 - px.x * 0.02)));
  float stain = n2(px / 380.0) * 0.6 + n2(px / 140.0) * 0.4;
  gl_FragColor = vec4(strokes, press * mix(1.0, br, 0.35), 0.92 + 0.08 * g - fib * 0.03, stain);
}
