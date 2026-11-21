
uniform sampler2D tCur, tHist, tDepth;
uniform mat4 uInvVP, uPrevVP;
uniform vec2 uRes, uJitter;
uniform float uBlend;
varying vec2 vUv;
void main() {
  vec4 cur = texture2D(tCur, vUv);
  // the history is read in place, texel for texel (the camera stood still for every frame in it): no resampling, no
  // blur — the running mean of the jittered frames is a box-filtered supersample of the pixel
  vec4 h = texture2D(tHist, vUv);
  vec2 px = 1.0 / uRes;
  vec4 mn = cur, mx = cur, c;
  c = texture2D(tCur, vUv + vec2(-px.x, 0.0)); mn = min(mn, c); mx = max(mx, c);
  c = texture2D(tCur, vUv + vec2( px.x, 0.0)); mn = min(mn, c); mx = max(mx, c);
  c = texture2D(tCur, vUv + vec2(0.0, -px.y)); mn = min(mn, c); mx = max(mx, c);
  c = texture2D(tCur, vUv + vec2(0.0,  px.y)); mn = min(mn, c); mx = max(mx, c);
  c = texture2D(tCur, vUv + vec2(-px.x, -px.y)); mn = min(mn, c); mx = max(mx, c);
  c = texture2D(tCur, vUv + vec2( px.x, -px.y)); mn = min(mn, c); mx = max(mx, c);
  c = texture2D(tCur, vUv + vec2(-px.x,  px.y)); mn = min(mn, c); mx = max(mx, c);
  c = texture2D(tCur, vUv + vec2( px.x,  px.y)); mn = min(mn, c); mx = max(mx, c);
  h = clamp(h, mn, mx);
  gl_FragColor = mix(cur, h, uBlend);
}
