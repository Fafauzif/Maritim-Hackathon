# Audit intake — CityRT style → coastal production rules

Resolved audit root: `cityrt-audit/` (read in place, unmodified).
Docs date/version: written against the shipped style registry; `evidence/manifest.json` present (278 KB).
Two style families were considered and one primary selected; no CityRT mesh, texture, shader or code is imported.

## Assumed → actual path map

The brief names four inputs that **do not exist** in this audit. The real substitutes used are listed here so no rule below claims a path that is not there.

| Brief-named input | Exists? | Actual substitute used |
|---|---|---|
| `analysis/geometry/building-language.md` | no | `analysis/geometry/observations.md` (4.3 KB) + `docs/ART-BIBLE.md` §6 |
| `analysis/geometry/metrics.json` | no | `analysis/catalog/catalog-summary.json` (18 KB, measured aspect/luma bands) |
| `analysis/constants.json` | no | `analysis/catalog/catalog-analysis.json` (52 KB), `analysis/styles/styles-static.json` |
| `evidence/styles/<id>/{overview,mid,street,night}.png` | no | `evidence/style-previews/<style>.webp` (14) and `evidence/catalog/img/*.webp` (824) |

Everything else the brief names is present: `docs/ART-BIBLE.md`, `KIT-SPEC.md`, `STYLE-MATRIX.md`, `UNKNOWNS.md`, `COVERAGE.md`, `analysis/palette/*.json` (17), `analysis/rendering/{ink-pipeline,renderer-verdict}.md`, `analysis/styles/styles-static.json`, `analysis/game/{art-systems,look-and-shaders,rendering-extract}.json`, `evidence/manifest.json`.

## Style decision

- **Primary family: `italian`** (STYLE-MATRIX row 6). Rationale: it is the closest measured register to the brief's Kodingareng direction — warm plaster walls, terracotta tile roofs, shutters, loggias — and its measured bands (scene luma 141.3, sat 0.36, building luma 153.0, building sat 0.34, silhouette aspect 1.25) sit in the bright-civic band the coastal brief asks for.
- **Secondary measured influence: `slavic`** (row 3, luma 139.9 / sat 0.29, accents `#B7684F` / `#6F8661`) — used only for the Amur bank/brick/timber register, because the site is Russian Far East.
- **Landscape mood override:** map skins `tropics` (water `#6CD2C6`, sky `#8EC3E6`) for the two Indonesian sites and `tundra`/`autumn` greys for Amur. Map skins are landscape overrides, not city styles, and are used only for water/sky/vegetation.

## Production rules (eight transfers)

| # | Dimension | Evidence label | Observed reference / actual path | Coastal production rule | Test |
|---|---|---|---|---|---|
| 1 | Camera | observed | `docs/ART-BIBLE.md` §2 ("elevated axonometric, pitch ~35–40°, yaw ~20–35°"); measured in `analysis/catalog/catalog-summary.json` | Every coast overview is authored at a high oblique in the 35–40° pitch class, framed with no horizon and a soft contact shadow; `COAST_APPROACH` moves to the same class closer in | Compare 960 px and 320 px proofs of all three; boat, landing and open water must survive the shrink |
| 2 | Massing / grid | observed | `docs/ART-BIBLE.md` §6; footprint ladder from `analysis/catalog/catalog-analysis.json` | Place village buildings on a **5 m cell grid**, with 2×1…4×4 footprints (10×5 … 20×20 m). No free-floating arbitrary spacing | Count building centres against the 5 m grid; every footprint drawn from the ladder |
| 3 | Detail hierarchy | derived | `docs/ART-BIBLE.md` §6 tiers 1–5 | Tier 1 (roof type, pitch, ridge, chimney, eaves) and tier 2 (window rhythm, facade bands) must be modelled on every ordinary building; tier 3 (door, steps, awning) on the hero waterfront buildings | Roofs must read at 320 px; window rhythm must repeat exactly per building |
| 4 | Light | observed | `docs/ART-BIBLE.md` §5, §8; `analysis/rendering/renderer-verdict.md` | One shared daylight rig per scene: elevated key sun, ambient sky fill, soft contact shadows, no specular sheen. No second mood register inside one scene | Grayscale read of the overview: land silhouette, anchor and vessel still identifiable |
| 5 | Palette | observed | `analysis/palette/*.json`; ART-BIBLE §4 hex families (`plaster #F1E5C8…#EEDDB4`, tile `#9A4E3C…#A85A42`, slate `#4F5F86…`) | Walls desaturated stone/plaster; chroma concentrated in roofs, vegetation, doors and the accent pair. Keep one register per scene. Pixel samples are display-referred, not base-colour inputs | Six-colour palette of a render vs `analysis/palette/italian.json`; mean ΔE ≤ 6 target |
| 6 | Material finish | observed | `docs/ART-BIBLE.md` §5 table | Principled, Metallic 0, Roughness 0.85–1.0 on walls/brick/timber; roofs ≥0.9; windows are **flat tinted quads, not transmissive**; metal reads by silhouette | Inspect a close-up crop: no sheen, no glass transmission, flat roof fields |
| 7 | Water / edges | derived + design target | ART-BIBLE §5 (ground flat); `STYLE-MATRIX.md` map skin `tropics` (`#6CD2C6` bright water) | One calm opaque-ish water surface at Z=0, a clear shoreline band, broad luminance change shallow→deep rather than animated high-frequency normals. Distinct export-safe water object | Section and overview must show the same waterline; no z-fighting at the shore band |
| 8 | Motion | derived | `renderer-verdict.md` (idle ~30 FPS, `camSlow` 0.25 default — a slow camera), ART-BIBLE §9 | Slow eased camera moves, 1–2 s settles, 2–4 s transitions; no overshoot, no roll; hold a quiet beat at the cutaway reveal | 540p animatic scrubbed start/middle/end against the move list |

## Deliberate deviations from the CityRT look

The audit's signature layer is a Three.js **ink-and-wash post pipeline** (hand-drawn ink edges, animated line boil `uBoil`/`uWobble`/`uJitter`, hatching, paper `#F3ECE0`, warm vignette). A full port of that pipeline is out of scope for a Blender Eevee delivery; it is approximated (paper-toned background, warm vignette, matte flat materials, inverted-hull silhouette lines on hero geometry) and the shortfall is recorded in `output/review/deviations.md`. This is labelled **design target**, not an audit-backed claim of equivalence.
