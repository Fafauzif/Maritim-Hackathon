# Renderer verdict (unauthenticated, 2026-11-21)

## Status

**Renderer family: unknown.** The 3D client was not reachable, so no engine fingerprint,
shader source, or draw-call evidence exists. This file records what *is* established and
what a future run must capture.

## What was established

| Question | Answer | Evidence |
|---|---|---|
| Is the 3D client served to anonymous visitors? | No | `evidence/scripts/public/` holds all 25 chunks referenced by the loader; largest is 148 KB (`main-B5x1aucL.js`) and none contains `WebGLRenderer`, `THREE`, `babylon`, `pc.Application`, or a wasm binary |
| What does the public site ship? | An SSR marketing shell + client-side route chunks | `index-BOyK8tfh.js` is a 1.8 KB Vite loader whose dependency map names 25 assets |
| Where is the game client? | Behind authentication | `/en/login?next=play` is the gated entry; `/en/play` is a 404 route (the `next` value is an action, not a path) |
| Is WebGL used at all in the shell? | No canvas is created by the public shell | `canvas` appears once in `main-B5x1aucL.js`; no context creation |

## What the published renders show about the rendering model

Four 1200×800 style previews were inspected visually (`european`, `cyberpunk`, `japanese`,
`medieval`). They are the strongest available rendering evidence and support these
*observations about output*, not about implementation:

- **Fixed elevated axonometric camera**, roughly 35–40° pitch, consistent framing across all
  four previews. No wide-angle perspective distortion; parallel verticals.
- **Flat, matte shading.** No specular highlights, no glass reflections, no visible normal
  maps. Facades read as flat colour with geometric relief (cornices, ledges, dormers).
- **Soft directional shadowing** with contact darkening at ground level; direction appears
  consistent (sun from upper-left in `european`).
- **Detail is geometry, not texture.** Window grids, balconies, chimneys, roof clutter,
  AC units, awnings and signage are modelled. Signage text is geometry/emissive.
- **Emissive accents are style-specific**: `cyberpunk` uses saturated neon signage against
  dark concrete; `european`/`medieval`/`japanese` use no emissive glow outdoors.
- **Vegetation is simplified**: ellipsoid/cone canopies, saturated greens, no leaf cards
  visible at this resolution.

Whether the implementation is Three.js, a custom WebGL renderer, or a wasm engine is
**not determinable** from these images.

## What the next authenticated run must capture

1. `WebGLRenderingContext` / `WebGL2RenderingContext` shader sources via pre-navigation hook
   (already implemented in `tools/browser/probe.js`).
2. `WEBGL_debug_renderer_info` unmasked renderer and vendor (verified working on this host).
3. Draw-call counts per frame at the default camera; shadow-map configuration.
4. Post-processing pass list (bloom/vignette/SSAO/outline) from shader source.
5. Model and texture payloads from the authenticated network log.

## Contradiction to resolve

Marketing copy says "nine personalities". The shipped client registers **14** style records
and **14** preview images (`analysis/styles/styles-static.json`). The nine might be a
game-mode subset, a curation, or stale copy. Until the in-game picker is observable, this
audit documents all 14 as the superset and marks the discrepancy as open.
