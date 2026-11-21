# CityRT art bible

**Status:** derived from 15 official renders (14 style heroes + 824 building studio renders),
the shipped style registry, the shipped map-skin palettes, and the shipped catalog text.
The live 3D client was unreachable (CityRT auth outage), so anything that can only be seen in
motion or in-engine — shaders, light rig, post effects, simulation — is marked
**UNOBSERVED** instead of guessed. Evidence references are repo-relative.

---

## 1. Design pillars

1. **Architectural realism, toy finish.** Massing and ornament follow real references
   (Haussmann Paris, Japanese shotengai/machiya, German Altstadt, cyberpunk Tokyo). The finish
   is a clean miniature: flat matte colour, crisp edges, no grime, no photorealism.
2. **Geometry does the talking.** Identity comes from modelled relief — dormers, cornices,
   chimneys, balconies, awnings, rooftop plant, signage — not from texture maps or normal maps.
   (`analysis/geometry/observations.md`)
3. **One camera, many worlds.** Every style is framed by the same elevated axonometric camera
   at roughly 35–40° pitch. Styles differ in palette, silhouette and props, never in viewpoint.
4. **Dense but legible.** Roofs and courtyards are busy with props; the street grid and block
   edges stay unmistakable. Readability at the default zoom outranks ornament count.
5. **Two mood registers.** 11 of 12 catalogued styles are bright daytime palettes
   (building luma 130–184). `cyberpunk` alone is a dark register (luma 99.9) carried by
   emissive signage. Treat it as the deliberate exception, not a tint sliders preset.

## 2. Camera and composition

| Property | Value | Confidence |
|---|---|---|
| Projection | Elevated axonometric; parallel verticals | inferred from 15 renders |
| Pitch | ~35–40° above horizon | inferred |
| Yaw | ~20–35° off the street grid | inferred |
| Framing | 3–4 blocks fill a 3:2 frame; no horizon, no sky except ground vignette | inferred |
| Subject | Buildings sit on a small ground patch with a soft contact shadow | observed (studio renders) |
| Silhouette footprint | Building-only silhouette aspect ≈ 1.0–1.4 (style means 1.04–1.38) | measured, `analysis/catalog/catalog-summary.json` |

Implication for Blender: model for a fixed 3/4 axonometric view. Any face that never appears
in that view is low priority; roof tops and two street facades carry nearly all the read.

## 3. Rendering model (captured from the authenticated client)

CityRT is **Three.js + a custom ink-and-wash post pipeline**. Details in
`analysis/rendering/renderer-verdict.md` and `analysis/rendering/ink-pipeline.md`.

- **Geometry is procedural**, built in code (`geo-*`, `shapes-*`, `shared_kit-*`), not imported
  glTF: the whole session served zero `.glb`/`.gltf` files. Instancing is heavy.
- **The signature layer is hand-drawn ink**: depth/normal edge lines (`uInk`, `uLineAlpha`,
  `uInkCrisp`), animated line boil (`uBoil`, `uWobble`, `uJitter`), hatching in shadow
  (`uHatchPx`, `uCon`, `uDetail`), paper texture and stains (`uPaper`, `uStain`), warm vignette
  (`uVignette`), and hatched sky (`uSkyTop`/`uSkyBot`/`uSkyHatch`).
- **Wash shading** replaces plain diffuse: the material patch does
  `outgoingLight = mix(outgoingLight, sketch, clamp(uDesat + uInfo*0.82, 0, 1))`, so lit
  surfaces keep a sketch tone and shadow pools like watercolour.
- **Paper is warm cream** `vec3(0.955, 0.925, 0.855)` ≈ `#F3ECE0` — the same tone the website
  uses as `#F3EDE0`.
- **Night is a separate lighting model** (`uNight`); windows light up one by one.
- **Idle policy**: ~30 FPS while the camera is still, full refresh while moving.

Four user-selectable **look presets** define how strong the ink layer reads:

| Preset | Character | Key values |
|---|---|---|
| `classic` (default) | dense hatching, grain, paper | hatch 1, grain 1, paper 1, stain 1, vignette 0.55, line 0.92, pen 1, wobble 1 |
| `clean` | light sketch: hatch only in shadowed walls | hatch 0.8, ground 0.12, grain 0.35, paper 0.5, vignette 0.3, pen 0.45 |
| `wash` | pure ink contour, no hatching, flat washes | hatch 0, wash 1, width 0.69, line 1, wobble 0 |
| `pencil` | soft sparse pencil texture | hatch 0.75, spacing 1.55, grain 0.55, paper 0.75, wobble 1.1 |

The official style previews read closest to a low-hatch setting; do not assume `classic`
densities when matching them.

**Still unmeasured:** exact renderer constructor arguments, camera body (module failed to
download), shadow-map size, per-quality post chain.

## 4. Palette system

Three layers stack, in this order:

1. **Style accent pair** (shipped, exact): `color` = warm/base signature, `accent` = cool
   contrast. Use as the two anchor hues for signage, trim, UI chips and hero props.
2. **Material family tables** (shipped, exact): the game ships complete hex families per
   surface class, and different styles use different tables. Representative values:

| Family | Default table (`pal-T-INdQBs.js`) | Second table (`pal-Doxq3a-X.js`) |
|---|---|---|
| plaster | `#F1E5C8 #EEDDB4 #F3EAD6 #EBD5B5 #E9D0C6 #DDE2C8 #DAD4E2` | `#EFE8D8 #EAE0CA #E8DCC0 #E3D2AE #E6D3C3` |
| stone | `#A9A08F #9E9686 #B5AC9A #A39C8C #B0A48E` | `#C9BFA9 #BFB49C #C4B9A2 #B8AE98` |
| slate roof | `#4F5F86 #5A5486 #6A5A8C #47607A #7A4E6E #3F6F78` | `#5A5E66 #53575E #62656A` |
| shingle / tile | `#9A4E3C #A85A42 #8E4A3A #7D5A45` | `#9A4A36 #A65A3E #8C4434 #9A5B44` |
| timber | `#5A4032 #4E3A2E #654634 #4A3A34` | `#7A3328 #843A2C #6E3226 #7E4030` |
| brick | — | `#9E4A36 #A8553E #94473A #A35A44` |
| ochre / sandstone | — | `#D9BF8E #D3B07A #CFA67A` / `#C3A07E #BC9473 #B2735A` |
| doors | `#A8473C #4F7A4E #3F5F86 #C99A3A #7A4E6E #6F5A4B` | `#5E3A2A #6E4230 #4E3426 #3F4A3A` |
| lawn | `#9DBA74 #A3BE78 #96B470` | `#A2B97A #9DB474 #A7BC7E` |
| metals | gold `#D9A94E`, copper `#5E9A88`, bronze `#A8743A`, iron `#3A3532` | gold `#C9A13B`, copper `#5E9A88`, lead `#7A7E84` |

Full families (39 + 49 entries, including `flowers`, `mushroom`, `cloth`, `stained`, `cobble`,
`path`, `glaze`) are in `analysis/game/art-systems.json`.

3. **Map skin** (shipped, 10 options): overrides grass, leaf, soil, water, sky and applies a
   desaturation factor 0.05–1.0. `blueprint` and `moon` at desat 1.0 are fully monochrome.

Anchor values (measured scene luma / saturation):

| Register | Styles | Luma band | Saturation band |
|---|---|---|---|
| Bright civic | arabic, futurist, slavic, japanese, italian, american, brazil | 139–150 | 0.20–0.36 |
| Muted historic | european, scandinavian, metropolis, british | 127–142 | 0.20–0.31 |
| Shadowed historic | medieval, fantasy | 109–114 | 0.33–0.37 |
| Night | cyberpunk | 88.6 | 0.21 |

Rules:

- Keep the scene in **one register per city**. Mixing a night style with bright daylight props
  breaks the read.
- Saturation is **low-to-moderate**, concentrated in accents and vegetation. Walls are
  desaturated stone/brick/timber tones; roofs and signs carry chroma.
- `cyberpunk` is the only style where emissive surfaces may exceed the wall luminance.

## 5. Material rules (for a Blender rebuild)

| Surface | Rule | Basis |
|---|---|---|
| Walls (plaster/stone) | Principled, Roughness 0.85–1.0, Metallic 0, flat base colour, no map | matte renders |
| Brick / timber | Same roughness band; colour variation per building, not per brick | renders show flat brick fields |
| Roof tile / slate | Roughness 0.9+, slight hue variation between blocks; no specular sheen | renders |
| Glass / windows | **Not transmissive.** Flat tinted quad, low roughness, slight emissive at night styles | no reflections visible; windows are flat colour blocks |
| Metal (railings, trims) | Metallic 0–0.3, Roughness 0.6–0.8; reads by silhouette, not shine | renders |
| Neon / signs (`cyberpunk`) | Emission strength 3–8, saturated accent pair, bloom expected **but unverified** | neon-dominant renders |
| Vegetation | Flat saturated green/seasonal skin colour, no texture | renders |
| Ground | Flat colour planes; road markings painted, not modelled | renders |

## 6. Building language and detail budget

**Grid (inferred, high confidence):** placement is cell-based and one cell ≈ **5 m** of street
frontage. Evidence: shipped descriptions say "every ~5 m of frontage — one more service bay"
and give footprint ranges in cells: `2×1`, `2×2`, `3×2`, `3×3`, `4×4`, `6×5`, `12×9`
(`analysis/catalog/catalog-analysis.json`).

**Footprint ladder:**

| Class | Cells | Metres (at 5 m/cell) | Examples |
|---|---|---|---|
| Kiosk / small service | 2×1, 2×2 | 10×5, 10×10 | corner shop, bakery |
| Standard building | 3×2, 3×3 | 15×10, 15×15 | townhouse, apartment, office |
| Large building | 4×4 | 20×20 | department store, school |
| Industrial block | 6×5 | 30×25 | factory, warehouse |
| Landmark | 12×9 | 60×45 | cathedral, castle, mega-plant |

**Detail hierarchy** (what must be modelled, in order):

1. Roof: type, pitch, dormers, chimneys, ridge, parapet, rooftop plant.
2. Street facade: window grid, ground-floor shopfront/arcade, cornice, balconies.
3. Entrance: door, steps, awning, sign.
4. Props at plot edge: fence, bins, planters, bollards, vehicles.
5. Landmark-specific silhouette: spires, domes, towers, cranes.

**Windows are the rhythm instrument.** Bay width and floor height should repeat; variation
comes from height, roof, colour and props, not from irregular fenestration.

**Growth rules are part of the art.** 134 shipped buildings describe parametric extension
("wider → more bays; deeper → service yard; level → more floors"). A kit that only ships fixed
blocks will look wrong when tiled. See `analysis/catalog/catalog-analysis.json` (field `growthRules`).

## 7. Per-style vocabulary (from shipped descriptions)

| Style | Must-have motifs |
|---|---|
| European | Haussmann boulevards, Dutch gables, Fachwerk, mansards, wrought-iron balconies |
| Japanese | machiya lattices, tiled cornices, lanterns, narrow towers, pagodas |
| Slavic | carved izba frames, terem towers, merchant houses, brick + panel five-storey blocks with yards |
| Arabic | whitewashed/ochre walls, arches, mashrabiya, domes, riad courtyards, windcatchers, bazaars |
| American | porched suburbs, brick Main Street, diners, Art Deco, glass towers |
| Italian | palazzi with shutters, terracotta roofs, loggias, portico arcades, piazzas, campaniles |
| Scandinavian | painted timber, steep roofs, grass roofs, pale wood, brick, copper |
| Futurist | white streamlined towers, rings/discs, hanging gardens, monorail, floating terraces |
| Cyberpunk | neon megablocks, holo-signs, cables/pipes, capsule hotels, noodle bars, dark concrete |
| Fantasy | crooked overhanging Fachwerk, cap roofs, turrets, glowing crystals, taverns, wizard towers |
| Medieval | walled old town, tall gables, steep roofs with dormer rows, red Fachwerk, stone tower-houses, arcades, belfry town hall, cathedral |
| Metropolis | glass supertalls with lit crowns, sky gardens, sky bridges and pools, media screens, helipads |
| British | red/yellow brick terraces, coloured doors, chimney rows, crescents, corner pubs, Victorian stations, 1960s concrete |
| Brazil | pastel colonial rows, azulejo facades, concrete waves and pilotis, cobogó screens, boteco corners, palms, mosaic promenades |

## 8. Lighting and time of day

Measured from the client:

- **Day length: 24 real minutes by default**, user-settable 4–120 minutes
  (`daylight-xoA8egPB.js`, pref `dayMinutes`; `sky` is an hour 0–24).
- Day/night can be switched off entirely (`dayNight` pref); the sky hour advances with a speed
  multiplier (game offers ×3) and pauses with the simulation.
- Night uses a distinct lighting model (`uNight`) and windows light up one by one (shipped tip
  text). `cyberpunk` is the style built around this register.
- Light preset preferences: `lightMorning`, `lightDay`, `lightEvening`, `lightNight`, each
  defaulting to `now` — i.e. the game normally follows the simulated time.

Recreation guidance: build a **24-minute day cycle** (or fixed presets mapped to clock hours),
with a warm low sun at morning/evening, high sun at noon, and a blue-shifted night where only
windows and signage are emissive. A one-off dusk preset is not enough; the cycle is the default.

## 9. Motion and feel

Measured from the client and its shipped preferences:

- **Idle vs moving render policy**: ~30 FPS while the camera is still; full display refresh while
  the camera moves.
- **Camera smoothing** pref `camSlow` defaults to `0.25` (a slow-camera mode for filming).
- **Simulation speed** options include ×3; the world pauses when the menu is open (`menuPause`).
- **Day length** 24 minutes default (see §8).
- Undo of any construction refunds fully (shipped tip), autosave ≈ every minute, `Ctrl+S` quicksave.

Still unmeasured: tick rate, vehicle speeds, construction duration, growth cadence. Their
modules did not download before the server returned 500 (`newgame`, `launch`, `lens` chunks).

## 10. Do / don't checklist

**Do**

- Model for a fixed elevated axonometric camera; prioritise roofs and two street facades.
- Carry identity in geometry: dormers, cornices, chimneys, awnings, planters, signage.
- Keep walls matte and desaturated; put chroma in roofs, signage, vegetation and the accent pair.
- Hold one 5 m cell grid and one footprint ladder so blocks tile.
- Ship each style as a vocabulary set, not a colour LUT: same cell grid, different motifs.
- Give cyberpunk real emissive signage geometry; a dark tint alone will not read as cyberpunk.
- Build the **ink-and-paper layer**: paper `#F3ECE0`, ink edges on silhouettes/creases, hatch in
  shadow, occasional line wobble, warm vignette (`analysis/rendering/ink-pipeline.md`).
- Drive a **24-minute day cycle** with a night model where windows light individually.

**Don't**

- Don't add specular sheen, reflections, glass transmission or photographic grunge.
- Don't render it as clean PBR: without the ink/hatch/paper layer it is a different art style.
- Don't use uniform hatching everywhere; it concentrates in shadow, on walls and in the sky.
- Don't make windows irregular row-by-row; variation belongs to building-level parameters.
- Don't mix two environments (map skins) or two mood registers in one city.
- Don't exceed the silhouette aspect band 1.0–1.4 for ordinary buildings.

## 11. Verification procedure

A later Blender run should be judged against these checks, not against taste:

1. **Palette:** 6-colour palette of a render vs `analysis/palette/<style>.json`; mean ΔE ≤ 6.
2. **Luma/saturation:** scene mean luma within ±10 %, saturation within ±0.05 of the style's
   measured band.
3. **Silhouette:** building bbox aspect within ±10 % of the style's measured mean
   (1.04–1.38 band).
4. **Grid:** every building snaps to the 5 m cell ladder; footprints come from the shipped
   ladder (2×1 … 12×9).
5. **Detail hierarchy:** all five tiers present on hero buildings; tiers 1–3 mandatory on
   ordinary buildings.
6. **Camera:** render from the same 35–40° pitch / 20–35° yaw and compare against the style
   hero render side by side.
