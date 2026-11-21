# Building-language observations (inferred from published renders)

**Confidence: inferred.** These notes come from four inspected 1200×800 style previews
(`european`, `cyberpunk`, `japanese`, `medieval`) plus the shipped per-style description
strings. No 3D model, grid constant, or triangle budget was ever observed: the client is
behind authentication and no glTF/GLB was served to an anonymous session.

## Camera and composition

| Property | Observation | Confidence |
|---|---|---|
| Projection | Elevated axonometric; parallel verticals, no strong perspective | inferred |
| Pitch | ~35–40° above the horizon | inferred |
| Framing | Identical crop across styles: 3–4 city blocks visible, horizon absent | inferred |
| Scale cue | Streets, sidewalks and building frontages share one modular rhythm | inferred |
| Rotation | Camera rotated ~20–35° off the street grid so blocks read as volumes | inferred |

## Shared structural vocabulary

Every inspected style builds from the same primitives, restyled:

- **Perimeter blocks** with enclosed courtyards; rectangular footprints snapped to a grid.
- **Street walls**: continuous frontage, varied heights, corner buildings articulated.
- **Roofs carry identity**: mansard + dormers (european), steep tile + gables (medieval),
  flat + rooftop machinery (japanese/cyberpunk), spires and towers as landmarks.
- **Ground plane is flat** with roads, lane markings, sidewalk strips and green blocks
  drawn as flat colour regions — no terrain relief visible in these four crops.
- **Street furniture and props** are dense but small: bollards, benches, awnings, planters,
  utility boxes, roof vents, chimneys, antennae, signage.
- **Vegetation** is blob/cone canopy, individually placed, never instanced forests at this zoom.

## Per-style architecture language (from shipped strings + renders)

| Style | Key | Architectural references in the shipped description | Seen in render |
|---|---|---|---|
| European | `european` | Haussmann boulevards, Dutch gables, Fachwerk, mansards, wrought-iron balconies | yes |
| Japanese | `japanese` | Machiya lattices, tiled cornices, lanterns, narrow towers, pagodas | yes |
| Slavic | `slavic` | Izbas with carved window frames, terems, merchant houses, apartment blocks with yards | no |
| Arabic | `arabic` | Whitewashed/ochre walls, arches, mashrabiya, domes, riad courtyards, windcatchers, bazaars | no |
| American | `american` | Porched suburbs, brick Main Street, diners, Art Deco and glass towers | no |
| Italian | `italian` | Palazzi with shutters, terracotta roofs, loggias, portico arcades, piazzas, campaniles | no |
| Scandinavian | `scandinavian` | Painted wooden houses, steep roofs, grass roofs, pale timber, brick and copper | no |
| Futurist | `futurist` | White streamlined towers, rings and discs, hanging gardens, monorail, floating terraces | no |
| Cyberpunk | `cyberpunk` | Neon megablocks, holo-signs, cables and pipes, capsule hotels, noodle bars, dark concrete, rain | yes |
| Fantasy | `fantasy` | Crooked half-timbered houses with overhanging floors, cap roofs, turrets, glowing crystals | no |
| Medieval | `medieval` | Walled old town, tall gables, steep tile roofs with dormer rows, red Fachwerk, stone tower-houses, arcades, town hall with belfry, cathedral | yes |
| Metropolis | `metropolis` | Modern megacity, glass supertalls with lit crowns, sky gardens, sky bridges and pools, media screens, helipads | no |
| British | `british` | Red and yellow brick terraces, coloured doors, chimney rows, crescents, corner pubs, Victorian stations, 1960s concrete | no |
| Brazil | `brazil` | Pastel colonial rows under tile, azulejo facades, concrete waves and pilotis, cobogó screens, boteco corners, palms, mosaic promenades | no |

## What is missing for a measurable kit

- Absolute module size (metres per city cell) — needs in-game grid or model bounds.
- Triangle budgets, LOD tiers, texture sizes — needs model payloads.
- Roof height ratios and facade bay rhythm — measurable from orthographic captures at a
  known zoom, or from GLB bounds.
- Collision/module footprint rules — needs the placed-building data.

Until those exist, `KIT-SPEC.md` states relative proportions and labels every absolute
number an assumption.
