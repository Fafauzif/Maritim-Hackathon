# Renderer verdict (authenticated client captured 2026-11-21)

**Status: RESOLVED.** The client bundles were captured from the signed-in game and analysed
statically. This supersedes the earlier "unknown" verdict, which was based on the
unauthenticated marketing shell.

## Engine

| Fact | Value | Evidence |
|---|---|---|
| Engine | **Three.js** | `three.core-DdSv55GA.js` (369 KB) + `materials-C1pDfKA6.js` (439 KB) in `evidence/game-bundles/` |
| Renderer | `WebGLRenderer` | 39 references; `materials` bundle contains the renderer class |
| WebGL2 | yes (`getContext('webgl2')` present) | `boot-DntyKGy4.js` |
| Tone mapping | `ACESFilmicToneMapping` is supported and referenced; exact assignment not yet isolated | 42 `toneMapping` refs, 3 `ACESFilmic` |
| Shadow map | PCF soft supported (`PCFSoftShadowMap` = 2) | `materials` bundle enum |
| Instancing | heavy use (`InstancedMesh` 43 refs) | whole-bundle scan |
| Buildings | **procedural geometry**, not imported glTF | zero model/`.glb`/`.ktx2` HTTP responses across the whole session; `geo-*`, `shapes-*`, `shared_kit-*`, `geom-*` modules build geometry in code |
| Idle frame policy | ~30 FPS while the camera is still, full refresh while moving | shipped UI text in `en-C1arqVDc.js` |

## The actual visual identity: an ink-and-wash post pipeline

CityRT is not a plain flat-shaded 3D game. It renders Three.js geometry through a **custom
hand-drawn ink/wash layer**. Evidence: `sketch-C5kxZCCL.js`, `washmat-Bp0o3aa1.js`,
`post-BtPl7EWO.js`, plus 53 shader uniforms extracted from them.

The wash material injects into the lighting result:

```glsl
outgoingLight = mix(outgoingLight, sketch, clamp(uDesat + uInfo * 0.82, 0.0, 1.0));
```

and the sketch shader family uses these uniforms (complete list in
`analysis/game/art-systems.json`):

| Group | Uniforms |
|---|---|
| Ink lines | `uInk`, `uLine`, `uLineAlpha`, `uInkCrisp`, `uInkTent`, `uInkTentR`, `uWidth?` (`uEdgeLine`, `uEdgeRes`) |
| Hand-drawn movement | `uWobble`, `uBoil`, `uJitter`, `uTime`, `uOffset` |
| Hatching | `uHatchPx`, `uCon`, `uDetail`, `uInner`, `uNrmOct` |
| Paper | `uPaper`, `uPaperK`, `uStain`, `uVignette`, `uGrain?` (`uDetail`) |
| Sky | `uSkyTop`, `uSkyBot`, `uSkyHatch`, `uSkyHatchK`, `uGrade` |
| Light/shadow | `uShadowSoft`, `uShK`, `uShTint`, `uCamDir`, `uNight`, `uHiK`, `uHiTint`, `uLift` |
| Colour | `uDesat`, `uSat`, `uTint`, `uExpo`, `uBlend`, `uMix` |
| Camera reconstruction | `uInvVP`, `uPrevVP`, `uNear`, `uFar`, `uTanHalf`, `uRes` |

Notable: `uBoil` + `uWobble` + `uJitter` mean the linework is deliberately unstable over time —
an animated hand-drawn "line boil". This single detail explains the reference renders' character
and is the hardest thing to fake in a plain 3D render.

## Look presets (user-facing, exact values)

`look-DZfJ2UwR.js` ships four presets. Every parameter is a float in the shipped data:

| Param | `classic` (default) | `clean` | `wash` | `pencil` |
|---|---|---|---|---|
| hatch | 1 | 0.8 | 0 | 0.75 |
| ground | 1 | 0.12 | 0 | 0.45 |
| cross | 1 | 0.25 | 0 | 0.4 |
| dark | 0.55 | 0.42 | 0.4 | 0.32 |
| spacing | 1 | 1.25 | 1.2 | 1.55 |
| wash | 0 | 0.35 | 1 | 0.4 |
| lift | 0 | 0.2 | 0.1 | 0.3 |
| fill | 1 | 0 | 0 | 0.35 |
| grain | 1 | 0.35 | 0.25 | 0.55 |
| paper | 1 | 0.5 | 0.55 | 0.75 |
| stain | 1 | 0.4 | 0.6 | 0.7 |
| vignette | 0.55 | 0.3 | 0.3 | 0.4 |
| sky | 0.16 | 0.05 | 0 | 0.08 |
| line | 0.92 | 0.9 | 1 | 0.85 |
| width | 1 | 1 | 0.69 | 0.95 |
| inner | 1 | 0.85 | 0.87 | 0.75 |
| pen | 1 | 0.45 | 0.92 | 0.7 |
| wobble | 1 | 0.8 | 0 | 1.1 |

The marketing style renders used for the earlier palette work correspond most closely to a low
hatch/low grain setting — the shipped preview images show far less hatching than `classic`.

## Graphics quality controls (from `quality-BJbdVyLr.js`)

LocalStorage keys, stepped values, defaults on:

| Setting | Steps | Default |
|---|---|---|
| `sks.quality.msaa` | 0, 2, 4, 8 | 0 |
| `sks.quality.frame` (render scale) | 0, 1, 1.25, 1.5, 1.75, 2, 2.5, 3 | 0 |
| `sks.quality.edge` (edge/ink resolution) | 0, 1, 1.5, 2, 2.5, 3, 4 | 0 |

## What remains unmeasured

- Exact renderer constructor arguments (antialias, pixel ratio, tone-mapping numeric value).
- Camera body: fov/near/far/pitch/yaw/zoom limits (module `lens-*` failed to download: HTTP 500).
- Shadow map size and cascade count.
- Which post passes run per quality tier.

These are narrow now; the architecture and the artistic system are known.
