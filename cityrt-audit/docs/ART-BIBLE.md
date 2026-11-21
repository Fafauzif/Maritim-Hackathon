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

## 3. Rendering model (observed output)

- **Flat, matte, unlit-looking shading.** No specular highlights, no reflections, no visible
  normal maps, no gloss on glass. (`analysis/rendering/renderer-verdict.md`)
- **Soft directional shadows** with ambient contact darkening under props and eaves. Sun
  direction reads from upper-left in the evening/european render.
- **No outline pass** visible at 1200 px: edges are defined by colour change and contact shadow,
  not by ink lines.
- **Emissive accents inside `cyberpunk` only**: neon signage and lit windows against dark
  concrete. Daytime styles have no bloom or glow outdoors.
- **Vegetation is primitive**: ellipsoid/cone canopies in saturated green, no leaf cards.

**UNOBSERVED:** tone mapping, exposure, shadow technique (cascade count / PCF radius), any
post-processing, anti-aliasing mode, texture usage. Do not claim these until the client is
captured.

## 4. Palette system

Three layers stack, in this order:

1. **Style accent pair** (shipped, exact): `color` = warm/base signature, `accent` = cool
   contrast. Use as the two anchor hues for signage, trim, UI chips and hero props.
2. **Style scene palette** (measured, 6 colours per style): full-scene k-means including
   ground and roofs. See `analysis/palette/<style>.json`.
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
blocks will look wrong when tiled. See `analysis/catalog/catalog-analysis.json.growthRules`.

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

Observed: a single dominant sun with soft shadows and strong ambient fill (shadow cores stay
coloured, never black). **UNOBSERVED:** whether the game has a day/time cycle, whether style
choice pins a time of day, and any night lighting besides cyberpunk emissives.

Recommendation until observed: author three fixed light presets in Blender — `day` (default for
11 styles), `dusk` (fantasy/medieval mood option), `night` (cyberpunk) — do not build a cycle.

## 9. Motion and feel

**UNOBSERVED.** The only behavioural facts shipped publicly: it is a city builder with roads,
districts, schools, hospitals and a budget; it runs online with friends; the client understands
`map`, `scenario`, `room`, `host` URL parameters. Simulation cadence, camera easing and
construction timing need an authenticated capture (`analysis/simulation/observations.md`).

## 10. Do / don't checklist

**Do**

- Model for a fixed elevated axonometric camera; prioritise roofs and two street facades.
- Carry identity in geometry: dormers, cornices, chimneys, awnings, planters, signage.
- Keep walls matte and desaturated; put chroma in roofs, signage, vegetation and the accent pair.
- Hold one 5 m cell grid and one footprint ladder so blocks tile.
- Ship each style as a vocabulary set, not a colour LUT: same cell grid, different motifs.
- Give cyberpunk real emissive signage geometry; a dark tint alone will not read as cyberpunk.

**Don't**

- Don't add specular sheen, reflections, glass transmission or grunge textures.
- Don't add ink outlines; the reference has none at capture resolution.
- Don't make windows irregular row-by-row; variation belongs to building-level parameters.
- Don't mix two environments (map skins) or two mood registers in one city.
- Don't exceed the silhouette aspect band 1.0–1.4 for ordinary buildings.
- Don't claim a shader/light/cycle match without an authenticated capture.

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
