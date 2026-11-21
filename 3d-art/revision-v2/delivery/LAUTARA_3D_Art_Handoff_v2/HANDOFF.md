# HANDOFF - LAUTARA 3D art revision v2

## Status

Art revision complete: assembled, exported, re-imported, measured and packaged.
App behaviour, gameplay, data wiring and integration are out of scope and remain with
the implementation teammate.

- Build ID: `20261121T1445-local`
- Base commit: `e07093ef34118bc3e686257accbbfe6246595153`
- Blender: 5.2.2 LTS (build `d13f752e3b9c`)
- Zip: `LAUTARA_3D_Art_Handoff_v2.zip` (hash list in SHA256SUMS.txt)
- Runtime assets: 14.2 MiB
- Validation: 38 pass, 0 fail,
  0 blocked

## What changed from v1

| Defect in v1 | v2 correction | Evidence |
|---|---|---|
| Settlements read as scattered similar blocks | Authored lane networks, lane-facing rotated footprints, plazas, waterfront landmarks, stone pads and varied roof/wall families | 96 houses across the three coasts; lane/obstacle rejection counters in `work/runs/20261121T1445-local/logs/build-*.json` |
| Boats could sit on dry ground / shallow bed | Hull footprint sampled at ten points; survey boat only placed where the full footprint bed is below clearance (target >= 1.55 m); local craft >= 0.95 m | boat bed maxima -6.695, -7.396, -6.6 m; all pass |
| Jetty rails rotated across the span | Rails and mid-rails are now long boxes aligned to the pier axis on both sides; pilings are computed down to the sampled bed; steps connect ground to deck | `work/scripts/v2props.py::build_jetty_v2`; frame audit |
| Dark cutaways cropped the bottom and boat | Solid stratified cut, water column, emissive paper backdrop, authored boat/jetty/house silhouettes, frame centred between boat and landing | Section geometry fills 55.2% (Kodingareng), 52.1% (Tunda), 56.6% (Amur) of the frame; boat and jetty fully inside 8/8 bounds |
| Globe locators off the place board (Tunda ~68 km wrong) | All three locators replaced with the place-board values; markers, region cameras and metadata rebuilt | marker nodes in `globe.glb`; 9/9 texture orientation probes pass |
| Only 3 stills per coast | Five 4K stills per coast: overview, plan, approach, detail, section | 15 images at 3840x2160 |
| 5.5 s travel films | 7 s films: 5.5 s surface move + 1.5 s cutaway hold, 168 frames at 24 fps | `encode-report.json`; 168/168 frames per site |
| Render-only look did not survive export | Core glTF materials, embedded resources, exported vertex colours on terrain, no cameras/lights, no required extensions | fresh import checks |

## Measured site summary

| Site | Houses | Coast tris | Boat bed max Z (m) | Clearance | Section cut len (m) | Exag |
|---|---:|---:|---:|---|---:|---:|
| Kodingareng Lompo | 34 | 161,852 | -6.695 | pass | 189.8 | 3.2 |
| Pulau Tunda | 40 | 189,358 | -7.396 | pass | 169.3 | 3.2 |
| Razdolnaya mouth / northern Amur Bay | 22 | 184,951 | -6.6 | pass | 182.3 | 3.0 |

## Composition (QA coverage pass, not delivery art)

| Site | View | Land | Water | Buildings | Jetty | Boat |
|---|---|---:|---:|---:|---:|---:|
| Kodingareng Lompo | overview | 16.5% | 75.1% | 4.5% | 0.9% | 0.57% |
| Kodingareng Lompo | approach | 8.8% | 81.0% | 5.4% | 1.4% | 1.22% |
| Kodingareng Lompo | detail | 4.5% | 68.8% | 7.4% | 1.9% | 2.52% |
| Kodingareng Lompo | section | 0.0% | 0.0% | 0.0% | 0.0% | 0.00% |
| Pulau Tunda | overview | 31.6% | 61.9% | 3.0% | 0.1% | 0.35% |
| Pulau Tunda | approach | 16.9% | 67.2% | 9.7% | 1.2% | 1.51% |
| Pulau Tunda | detail | 12.6% | 70.9% | 9.8% | 1.3% | 1.99% |
| Pulau Tunda | section | 0.0% | 0.0% | 0.0% | 0.0% | 0.00% |
| Razdolnaya mouth / northern Amur Bay | overview | 17.7% | 75.5% | 3.1% | 0.3% | 0.32% |
| Razdolnaya mouth / northern Amur Bay | approach | 7.3% | 82.8% | 4.4% | 1.2% | 0.87% |
| Razdolnaya mouth / northern Amur Bay | detail | 8.1% | 78.7% | 6.0% | 1.6% | 1.56% |
| Razdolnaya mouth / northern Amur Bay | section | 0.0% | 0.0% | 0.0% | 0.0% | 0.00% |

The coverage pass replaces materials with flat object colours so land, water,
buildings, jetty and boat shares are measured exactly. `waterfx` and `vegetation`
shares are omitted from this table for brevity.

## Palette and finish

The delivery stills were measured against the owner's CityRT finish reference
(luma 0.498, saturation 0.297). The shared look uses Khronos PBR Neutral, exposure
-0.56, Hue/Sat 0.96, warm key and cool fill, matte water roughness 0.80.

| View | Luma | Saturation | Edge density | Blown pixels (>0.90) |
|---|---:|---:|---:|---:|
| Kodingareng Lompo - overview | 0.560 | 0.305 | 0.0048 | 0.00% |
| Kodingareng Lompo - plan | 0.567 | 0.307 | 0.0062 | 0.00% |
| Kodingareng Lompo - approach | 0.560 | 0.292 | 0.0062 | 0.01% |
| Kodingareng Lompo - detail | 0.547 | 0.258 | 0.0101 | 0.01% |
| Kodingareng Lompo - section | 0.550 | 0.188 | 0.0014 | 0.00% |
| Pulau Tunda - overview | 0.538 | 0.307 | 0.0095 | 0.00% |
| Pulau Tunda - plan | 0.539 | 0.324 | 0.0060 | 0.00% |
| Pulau Tunda - approach | 0.518 | 0.321 | 0.0100 | 0.00% |
| Pulau Tunda - detail | 0.518 | 0.323 | 0.0113 | 0.00% |
| Pulau Tunda - section | 0.607 | 0.176 | 0.0013 | 0.00% |
| Razdolnaya mouth / northern Amur Bay - overview | 0.497 | 0.260 | 0.0074 | 0.00% |
| Razdolnaya mouth / northern Amur Bay - plan | 0.547 | 0.250 | 0.0037 | 0.00% |
| Razdolnaya mouth / northern Amur Bay - approach | 0.483 | 0.253 | 0.0067 | 0.00% |
| Razdolnaya mouth / northern Amur Bay - detail | 0.477 | 0.262 | 0.0091 | 0.00% |
| Razdolnaya mouth / northern Amur Bay - section | 0.461 | 0.200 | 0.0021 | 0.00% |
| Globe - overview | 0.370 | 0.666 | 0.0030 | 0.10% |

## Runtime inventory

| Asset | Kind | Bytes | Triangles | Nodes | Bounds (m, glTF X/Y/Z) |
|---|---|---:|---:|---:|---|
| `runtime/globe/globe.glb` | globe | 1,784,408 | 36,996 | 13 | 20.0 x 20.0 x 20.0 |
| `runtime/kit/common-kit.glb` | kit | 307,452 | 5,013 | 16 | 50.8 x 10.3 x 37.5 |
| `runtime/coasts/kodingareng/coast.glb` | coast | 3,447,240 | 152,276 | 333 | 680.0 x 20.5 x 680.0 |
| `runtime/coasts/kodingareng/section.glb` | section | 537,224 | 9,574 | 36 | 16.1 x 57.4 x 189.6 |
| `runtime/coasts/tunda/coast.glb` | coast | 3,800,568 | 179,824 | 416 | 720.0 x 20.7 x 720.0 |
| `runtime/coasts/tunda/section.glb` | section | 535,020 | 9,532 | 36 | 134.3 x 59.9 x 108.5 |
| `runtime/coasts/amur/coast.glb` | coast | 3,933,760 | 175,349 | 549 | 800.0 x 17.3 x 800.0 |
| `runtime/coasts/amur/section.glb` | section | 535,296 | 9,600 | 36 | 182.0 x 44.5 x 17.4 |

## Camera presets

The presets are recorded from the evaluated cameras in the actual scenes, converted
once to glTF space. `target` is a point 80 m along the view axis; use it as a look-at
direction anchor.

| Site | Preset | Type | Position (glTF) | Target (glTF) | FOV / Width |
|---|---|---|---|---|---|
| kodingareng | `COAST_OVERVIEW` | perspective | `20.0, 150.0, 210.0` | `11.4, 85.9, 163.0` | 29.8 deg vertical |
| kodingareng | `COAST_PLAN` | orthographic | `0.0, 720.0, 20.0` | `0.0, 640.0, 20.0` | 470.0 m ortho width |
| kodingareng | `COAST_APPROACH` | perspective | `64.0, 54.0, 228.0` | `27.4, 21.2, 164.9` | 23.8 deg vertical |
| kodingareng | `COAST_DETAIL` | perspective | `55.0, 24.0, 190.0` | `8.9, 6.0, 127.1` | 27.1 deg vertical |
| kodingareng | `COAST_SECTION` | orthographic | `-140.9, -4.8, 124.3` | `-61.1, -4.8, 118.9` | 106.0 m ortho width |
| tunda | `COAST_OVERVIEW` | perspective | `-56.0, 240.0, 320.0` | `-54.8, 190.0, 257.5` | 28.4 deg vertical |
| tunda | `COAST_PLAN` | orthographic | `0.0, 720.0, 5.0` | `0.0, 640.0, 5.0` | 560.0 m ortho width |
| tunda | `COAST_APPROACH` | perspective | `-172.0, 54.0, 168.0` | `-133.4, 24.5, 104.4` | 21.2 deg vertical |
| tunda | `COAST_DETAIL` | perspective | `-160.0, 30.0, 132.0` | `-114.6, 4.0, 71.5` | 28.4 deg vertical |
| tunda | `COAST_SECTION` | orthographic | `-201.6, -5.3, -55.3` | `-151.5, -5.3, 7.1` | 113.9 m ortho width |
| amur | `COAST_OVERVIEW` | perspective | `10.0, 150.0, 140.0` | `24.4, 102.0, 77.6` | 28.4 deg vertical |
| amur | `COAST_PLAN` | orthographic | `20.0, 720.0, -10.0` | `20.0, 640.0, -10.0` | 500.0 m ortho width |
| amur | `COAST_APPROACH` | perspective | `4.0, 46.0, 78.0` | `30.4, 22.8, 6.2` | 19.8 deg vertical |
| amur | `COAST_DETAIL` | perspective | `8.0, 28.0, 12.0` | `53.9, 3.1, -48.6` | 27.1 deg vertical |
| amur | `COAST_SECTION` | orthographic | `81.4, -5.2, 95.0` | `75.3, -5.2, 15.2` | 88.3 m ortho width |

## Anchors (glTF, metres)

| Site | Node | glTF position |
|---|---|---|
| kodingareng | `COAST_ORIGIN` | `[0.000, 0.000, -0.000]` |
| kodingareng | `ORBIT_SITE` | `[0.000, 0.000, -0.000]` |
| kodingareng | `ORBIT_WATERFRONT` | `[6.500, 1.500, 124.100]` |
| kodingareng | `TARGET_SURVEY` | `[10.000, 1.400, 146.000]` |
| kodingareng | `ANCHOR_JETTY` | `[15.373, 0.600, 139.732]` |
| kodingareng | `ANCHOR_VESSEL` | `[10.000, 0.000, 146.000]` |
| kodingareng | `SECTION_A` | `[12.985, 0.000, 175.851]` |
| kodingareng | `SECTION_B` | `[0.050, 0.000, -13.504]` |
| tunda | `COAST_ORIGIN` | `[0.000, 0.000, -0.000]` |
| tunda | `ORBIT_SITE` | `[0.000, 0.000, -0.000]` |
| tunda | `ORBIT_WATERFRONT` | `[-80.600, 1.500, 64.600]` |
| tunda | `TARGET_SURVEY` | `[-124.000, 1.400, 76.000]` |
| tunda | `ANCHOR_JETTY` | `[-129.600, 0.600, 73.200]` |
| tunda | `ANCHOR_VESSEL` | `[-124.000, 0.000, 76.000]` |
| tunda | `SECTION_A` | `[-148.000, 0.000, 94.000]` |
| tunda | `SECTION_B` | `[-16.000, 0.000, -12.000]` |
| amur | `COAST_ORIGIN` | `[0.000, 0.000, -0.000]` |
| amur | `ORBIT_SITE` | `[0.000, 0.000, -0.000]` |
| amur | `ORBIT_WATERFRONT` | `[27.300, 1.500, -44.200]` |
| amur | `TARGET_SURVEY` | `[42.000, 1.400, -52.000]` |
| amur | `ANCHOR_JETTY` | `[46.086, 0.600, -55.125]` |
| amur | `ANCHOR_VESSEL` | `[42.000, 0.000, -52.000]` |
| amur | `SECTION_A` | `[12.054, 0.000, -50.203]` |
| amur | `SECTION_B` | `[193.820, 0.000, -63.989]` |

## Globe

- Radius: 10 art units (not metres, not georeferenced).
- Projection: Natural Earth equirectangular colour art on a UV sphere; +Y north.
- Markers: `ANCHOR_kodingareng` (-5.14905, 119.26473),
  `ANCHOR_tunda` (-5.81151, 106.27811),
  `ANCHOR_amur` (43.32556, 131.80778).
- Region cameras and the orthographic hero camera are in `globe.cameras`.
- Texture orientation: 9/9 land/ocean probes pass in `build-globe.json`.
- Do not infer that globe and coast share a geographic transform.

## Evidence fixture

`evidence/depth-case-verified.json` is the original verified fixture, copied
byte-for-byte. It contains the two GLORYS12 rows for 2020-04-16 UTC and all sign
combinations. Display rounding lives only in the pitch plates.

- Surface: 0.494 m, 0.093 m/s, bearing 264 deg toward (west)
- Deeper: 9.573 m, 0.074 m/s, bearing 45 deg toward (northeast)
- Cell centre: approximately -5.1667 deg, 119.2500 deg; one ~9 km cell
- The cell is not the proposed station S-01 and not the disputed extraction
  coordinate. The scene origin is art-local.

## Media

- Three 7 s travel films, 1920x1080, 24 fps, H.264/yuv420p, 168 frames each.
- One 27 s reel: 96 globe intro frames + 3x168 coast frames + 48 globe outro frames.
- Full decode checks in `encode-report.json`.
- Fifteen clean 4K stills and one 4K globe still; kit sheet at 2560x1440.
- Pitch plates are annotated, presentation-only media.

## Verification

Validation items are recorded in `review/validation.json` with state and evidence
paths.

| Check | State | Evidence |
|---|---|---|
| doc-start_here.md | pass | `START_HERE.md` |
| doc-handoff.md | pass | `HANDOFF.md` |
| doc-attribution.md | pass | `ATTRIBUTION.md` |
| inventory-sums | pass |  |
| inventory-clean | pass |  |
| manifest | pass | `runtime/asset-manifest.json` |
| manifest-no-private-paths | pass | `runtime/asset-manifest.json` |
| glb-runtime/globe/globe.glb | pass | `runtime/globe/globe.glb` |
| glb-runtime/kit/common-kit.glb | pass | `runtime/kit/common-kit.glb` |
| glb-runtime/coasts/kodingareng/coast.glb | pass | `runtime/coasts/kodingareng/coast.glb` |
| glb-runtime/coasts/kodingareng/section.glb | pass | `runtime/coasts/kodingareng/section.glb` |
| glb-runtime/coasts/tunda/coast.glb | pass | `runtime/coasts/tunda/coast.glb` |
| glb-runtime/coasts/tunda/section.glb | pass | `runtime/coasts/tunda/section.glb` |
| glb-runtime/coasts/amur/coast.glb | pass | `runtime/coasts/amur/coast.glb` |
| glb-runtime/coasts/amur/section.glb | pass | `runtime/coasts/amur/section.glb` |
| asset-globe | pass | `runtime/globe/globe.glb` |
| asset-kit | pass | `runtime/kit/common-kit.glb` |
| asset-coast_kodingareng | pass | `runtime/coasts/kodingareng/coast.glb` |
| asset-section_kodingareng | pass | `runtime/coasts/kodingareng/section.glb` |
| asset-coast_tunda | pass | `runtime/coasts/tunda/coast.glb` |
| asset-section_tunda | pass | `runtime/coasts/tunda/section.glb` |
| asset-coast_amur | pass | `runtime/coasts/amur/coast.glb` |
| asset-section_amur | pass | `runtime/coasts/amur/section.glb` |
| anchors-kodingareng | pass | `runtime/coasts/kodingareng/coast.glb`, `runtime/coasts/kodingareng/section.glb` |
| anchors-tunda | pass | `runtime/coasts/tunda/coast.glb`, `runtime/coasts/tunda/section.glb` |
| anchors-amur | pass | `runtime/coasts/amur/coast.glb`, `runtime/coasts/amur/section.glb` |
| camera-presets | pass | `runtime/asset-manifest.json` |
| clean-stills | pass | `media/coasts` |
| image-media/globe/globe-overview.png | pass | `media/globe/globe-overview.png` |
| image-media/kit/asset-sheet.png | pass | `media/kit/asset-sheet.png` |
| motion | pass | `media/coasts`, `media/coast-reel.mp4` |
| pitch-plates | pass | `media/pitch` |
| evidence | pass | `evidence/depth-case-verified.json` |
| review-review/before-after.png | pass | `review/before-after.png` |
| review-review/parity-sheet.png | pass | `review/parity-sheet.png` |
| review-review/runtime-parity.png | pass | `review/runtime-parity.png` |
| review-review/review-report.md | pass | `review/review-report.md` |
| editable-sources | pass | `source` |

## Known limits

- Terrain, seabed, section geometry, building counts, prop placement, reef patches
  and vegetation are **illustrative art**. They are not surveyed bathymetry, a
  building census or an ecological map.
- The section is vertically exaggerated (see `sites.<site>.section`) and cropped to
  the landing/boat story; A and B continue beyond the crop.
- Coast water is alpha-blended in Blender and in glTF. If the target renderer treats
  alpha as opaque or sorts it badly, replace the material on `ENV_Water` with an
  opaque material; geometry and shoreline marks already carry the read.
- Outlines, if any remain in a source file, are render-only; the clean GLBs carry
  silhouette by geometry and shadow, not by an ink post-process.
- The globe is a locator illustration, not a scientific projection layer.
- No playable app, data wiring or game loop is included.
- Human playback of the three films and the reel is still recommended for final
  sign-off; image evidence is supplied as contact sheets and measured PNG statistics.


