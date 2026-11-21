# The CityRT ink-and-wash pipeline

Reverse-engineered from the authenticated client bundles (`evidence/game-bundles/`). This is
the part of the style a plain 3D recreation will miss unless it is reproduced deliberately.

## Layers, in render order

1. **Three.js scene** — procedural geometry, instanced meshes, PBR-ish materials
   (`materials-C1pDfKA6.js`).
2. **Wash material injection** — `washmat-Bp0o3aa1.js` patches the lighting result:
   `outgoingLight = mix(outgoingLight, sketch, clamp(uDesat + uInfo*0.82, 0, 1))`.
   A height-driven wash front (`uWashY ± noise(uWashY)`) tints geometry like watercolour pooling.
3. **Sketch/ink pass** — `sketch-C5kxZCCL.js`: depth+normal edge extraction (`uNrmOct`,
   `uEdgeRes`, `uInvVP`), ink lines (`uInk`, `uInkCrisp`, `uInkTent`), hatching (`uHatchPx`,
   `uCon`, `uDetail`), hand-drawn jitter (`uWobble`, `uBoil`, `uJitter`, `uTime`).
4. **Paper and grade** — `uPaper`, `uPaperK`, `uStain`, `uVignette`, `uGrade`, `uSat`,
   `uExpo`, `uTint`, plus sky hatching (`uSkyTop`, `uSkyBot`, `uSkyHatch`).
5. **Night variant** — `uNight` switches the lighting model; shipped UI says windows light up
   one by one at night, and there is a ×3 speed control to watch it.

## Paper base colour

From the wash shader: `swPaper = vec3(0.955, 0.925, 0.855)` — a warm cream, sRGB
≈ `#F3ECE0`. The marketing site background `#F3EDE0` matches it almost exactly, so the UI and
the renderer share one paper tone. Any faithful recreation should use this as the canvas colour.

## Line behaviour

`uBoil`/`uWobble`/`uJitter` animate the linework. This is not an artefact: it is authored
instability, so edges shimmer slightly frame to frame like hand-inked animation. The `wash`
preset sets `wobble: 0` (clean vector ink) while `classic` and `pencil` keep it at 1–1.1.

## What is genuinely stylised vs. realistic

- Massing, ornament and architectural vocabulary are realistic (see catalog).
- Shading is **not** PBR-photographic: the sketch layer dominates, with hatching in shadow,
  paper show-through in light, and line work on silhouettes and creases.
- Night is blue-shifted with point lights dominating (`uNight`, window emissives).

## Reproduction options for a Blender pipeline

Ordered by fidelity per effort:

1. **Blender + Freestyle line render + compositor paper** — closest with built-in tools:
   Freestyle (crease/silhouette edges), noise-distorted line, paper texture, vignette, hatching
   in shadow areas via a material-driven mask.
2. **Geometry-based outlines + procedural hatch shader** — inverted-hull or solidified outlines
   plus a shader that samples a hatch texture by light direction and shadow terminator.
3. **Render and post in 2D** — render clean passes (albedo, depth, normals, shadows) and apply
   an ink/wash post pipeline equivalent to the game's uniforms. Highest fidelity, most work,
   and easiest to match numerically because every parameter above is a number.

Whichever path is chosen, the acceptance test is the same: compare against a captured in-game
frame at the same camera and look preset, and match hatch density, line weight, paper tone,
vignette and night shift. All five now have numeric targets.
