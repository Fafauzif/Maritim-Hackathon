
uniform sampler2D tCur;
uniform vec2 uRes;
uniform float uSharp;       // unsharp mask after the accumulation (the mean of jittered frames softens lines by ~½ px)
varying vec2 vUv;
void main() {
  vec4 c = texture2D(tCur, vUv);
  if (uSharp > 0.0) {
    vec2 o = 1.0 / uRes;
    vec4 nb = 0.25 * (texture2D(tCur, vUv + vec2(o.x, 0.0)) + texture2D(tCur, vUv - vec2(o.x, 0.0)) + texture2D(tCur, vUv + vec2(0.0, o.y)) + texture2D(tCur, vUv - vec2(0.0, o.y)));
    c.rgb = max(c.rgb + (c.rgb - nb.rgb) * uSharp, 0.0);
  }
  gl_FragColor = c;
  #include <colorspace_fragment>
}
