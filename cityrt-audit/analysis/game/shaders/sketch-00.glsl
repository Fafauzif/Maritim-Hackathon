
{
  float swN = ik_noise(vWPos.xz * 0.42 + vec2(vWPos.y * 0.23, 0.0)) * 0.65 + ik_noise(vWPos.xz * 1.9 + vWPos.y) * 0.35;
  float swFront = uWashY + (swN - 0.5) * 1.9;
  float swCol = 1.0 - smoothstep(swFront - 0.22, swFront + 0.22, vWPos.y);
  float swEdge = exp(-pow((vWPos.y - swFront + 0.25) / 0.5, 2.0)) * uWashA;
  vec3 swPaper = vec3(0.955, 0.925, 0.855);
  vec3 swSketch = mix(sketch * vec3(1.0, 0.985, 0.95), swPaper, 0.46);
  // pencil lines of the sketch: a faint graphite tint in the hatch strokes
  swSketch *= 1.0 - 0.1 * (1.0 - smoothstep(0.35, 0.8, lit));
  // co-op: another player's building is sketched in that player's ink (uTint.rgb, strength uTint.a; 0 = graphite)
  float swInk = 1.0 - smoothstep(0.45, 0.92, dot(swSketch, vec3(0.3333)));
  swSketch = mix(swSketch, mix(swPaper, uTint.rgb, 0.5 + 0.42 * swInk), uTint.a);
  vec3 wet = outgoingLight * (1.0 - 0.2 * swEdge) + vec3(0.02, 0.01, 0.0) * swEdge;
  float k = clamp(uDesat * (1.0 - swCol), 0.0, 1.0);
  outgoingLight = mix(wet, swSketch, k);
  outgoingLight = mix(outgoingLight, sketch, clamp(uInfo * 0.82, 0.0, 1.0));
}
