# CityRT Blender kit specification

Blueprint for the later Blender 5.2 + Blender MCP run. Nothing here was authored in Blender;
this run only produced the measurements and rules the kit must satisfy.

Legend: **[measured]** has a value behind it in this repo · **[inferred]** derived from renders
or shipped text · **[assumption]** a planning number with no direct evidence.

## 1. Scene setup

| Setting | Value |
|---|---|
| Unit system | Metric, 1 Blender unit = 1 m |
| Grid cell | **5 m** **[inferred]** — shipped text says "every ~5 m of frontage" and gives cell footprints |
| Origin | Base-centre of each building's plot; Z up in Blender, +Y up on glTF export |
| Up axis / scale | Export scale 1.0, apply transforms; no unit scaling |
| Collection layout | `CITYRT/<style>/<category>/<variant>`; one collection per style bucket |
| Naming | `cityrt_<style>_<cat>_<stem>_<variant>` e.g. `cityrt_european_res_rowhouse_a` |
| Camera | One shared camera preset: elevated axonometric, 35–40° pitch, 20–35° yaw **[inferred]** |

## 2. Module and footprint ladder

Each building must snap to one of these plot sizes. Values in metres at 5 m/cell.

| Class | Cells **[measured from shipped text]** | Metres | Category examples |
|---|---|---|---|
| Kiosk | 2×1 | 10×5 | corner shop, kebab stand |
| Small | 2×2 | 10×10 | bakery, clinic, workshop |
| Standard A | 3×2 | 15×10 | townhouse, tavern, diner |
| Standard B | 3×3 | 15×15 | apartment, office, shop row |
| Large | 4×4 | 20×20 | department store, school, hospital |
| Industrial | 6×5 | 30×25 | factory, warehouse, plant hall |
| Landmark | 12×9 | 60×45 | cathedral, castle, stadium, mega-factory |

Growth rules (must be parametric, not fixed meshes) — 134 shipped examples exist in
`analysis/catalog/catalog-analysis.json` (field `growthRules`):

- **wider** → repeat a bay / service bay / shopfront unit
- **deeper** → add courtyard wing, service yard, rear hall
- **level** → add a floor (and correspondingly taller roof stack)

## 3. Height policy **[assumption]**

No height constant was observable. Planning values at 3.2 m floor-to-floor with a pitched roof:

| Class | Floors | Body height | Notes |
|---|---|---|---|
| Kiosk / small | 1–2 | 3.2–6.4 m | flat or shallow mono-pitch roof |
| Standard | 3–5 | 9.6–16 m | mansard/gable adds 3–6 m |
| Large | 4–7 | 12.8–22.4 m | landmark towers exempt |
| Industrial | 1–2 tall | 6–14 m | sawtooth or long gable |
| Landmark | varies | up to ~60 m | spires/cathedral towers tallest |

These are labelled assumptions; replace them the moment an authenticated capture gives floor
heights.

## 4. Materials

Shading model: **matte, flat-colour, no textures, no specular** — see `ART-BIBLE.md` §5.

| Slot | Principled BSDF | Notes |
|---|---|---|
| Wall | Base colour = style wall family, Roughness 0.90, Metallic 0, Specular 0.2 | per-building hue jitter ±4 % |
| Trim / cornice | Base colour = wall tuned ±10 % luma, Roughness 0.85 | geometry only, no decals |
| Roof tile | Base colour = roof family, Roughness 0.95 | hue jitter per block ±5 % |
| Glass | Base colour = dark tint `#2E3A44`-ish or style tint, Roughness 0.35, Metallic 0, **no transmission** | flat quad inset 2 cm |
| Metal | Metallic 0.2, Roughness 0.7 | railings, trims, frames |
| Emissive (cyberpunk only) | Emission colour = accent pair, Strength 4.0 | signage and window strips |
| Vegetation | Base colour = skin `leaf` colour, Roughness 1.0 | ellipsoid/cone primitives |
| Ground / road | Flat colours from skin palette; markings as separate flat meshes | no displacement |

Palette inputs, per style:

- accent pair — `analysis/styles/styles-static.json` (`color`, `accent`) **[measured]**
- scene palette — `analysis/palette/<style>.json` **[measured]**
- map skin overrides — `analysis/skins-static.json` (`grass`, `leaf`, `soil`, `water`, `sky`, `desat`) **[measured]**

## 5. Detail hierarchy (build in this order)

1. **Roof system** — type, pitch, dormers, chimneys, ridge, parapet, rooftop plant.
2. **Street facades** — window grid, shopfront/arcade, cornice, balconies.
3. **Entrance** — door, steps, awning, hanging sign.
4. **Plot-edge props** — fence, bins, planters, bollards, vehicles.
5. **Landmark silhouette** — spires, domes, towers, cranes.

Ordinary buildings need tiers 1–3; heroes need all five.

## 6. Detail budget **[assumption]**

No triangle counts were observable. Planning caps sized for a browser city builder:

| Tier | Target tris | Max tris |
|---|---|---|
| Hero / landmark | 8 000 | 15 000 |
| Ordinary building | 2 500 | 5 000 |
| Prop | 300 | 800 |
| Tree / vegetation | 200 | 600 |

LOD ladder: L0 = full, L1 ≈ 40 % tris (drop props, simplify dormers), L2 ≈ 15 % (silhouette +
roof only). Every LOD keeps the same footprint and roofline so swapping does not pop.

## 7. Export

- Format: **glTF binary (.glb)**, +Y up, scale 1.0, no cameras/lights exported.
- One material per slot, plain PBR metallic-roughness; no texture maps in v1.
- Apply modifiers, triangulate on export, origin at base centre, empty parent per building.
- Keep `< 5 000` tris and one 4-material draw batch for ordinary buildings so a city keeps
  a manageable draw-call count **[assumption]**.

## 8. Acceptance tests (run before calling the kit done)

| # | Test | Pass |
|---|---|---|
| 1 | Palette vs measured scene palette (ΔE) | mean ΔE ≤ 6 for the 6-colour palette |
| 2 | Luma / saturation band | within ±10 % luma, ±0.05 saturation of the style's measured value |
| 3 | Silhouette aspect | within ±10 % of the style mean (1.04–1.38) |
| 4 | Grid snap | every building footprint is one row of the ladder, ±0 cm |
| 5 | Growth rules | wider/deeper/level variants exist for each standard building |
| 6 | Detail hierarchy | tiers 1–3 present on ordinary, 1–5 on heroes |
| 7 | Camera compare | side-by-side against `evidence/style-previews/<style>.webp` at the shared camera preset |
| 8 | Night style | cyberpunk renders with emissive signage above wall luminance, no daylight tint |

Tests 1–3 and 7 are pixel checks; 4–6 and 8 are structural/blender-scene checks. A later run
should automate 1–3 with the same `Palette` module used here.

## 9. Explicitly out of scope for this spec

- Shader graph / pipeline fidelity — renderer is UNOBSERVED.
- Day-night cycle, traffic, construction pacing — simulation is UNOBSERVED.
- Third-party style motifs that are trademarks (specific brands on cyberpunk signage): use
  generic signage, not identifiable logos.
