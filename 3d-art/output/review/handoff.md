# Handoff · The Ocean Has Floors

A three-coast Blender art set made for the Maritim Hackathon: **Kodingareng Lompo**,
**Pulau Tunda**, and the **Razdolnaya river mouth in northern Amur Bay**, plus a real-outline
Earth, three travel films and a connecting reel.

Open `coasts/<site>/scene.blend` in Blender 5.2.2, press **Numpad 0**, and the coast opens on
its god's-eye camera. Everything below is meant to be navigated, not just viewed.

## What to look at first

| Order | File | What it proves |
|---|---|---|
| 1 | `globe/globe-overview.png` | Recognizable Earth, three locators, real continent outlines |
| 2 | `coast-reel.mp4` | Earth to each coast and back, 20.5 s, 1920x1080 24 fps |
| 3 | `coasts/<site>/travel.mp4` | One coast's flight: overview, approach, parallax, cutaway reveal |
| 4 | `coasts/<site>/godview.png` | 3840x2160 high-oblique hero |
| 5 | `coasts/<site>/mapview.png` | 3840x2160 north-up survey plan |
| 6 | `coasts/<site>/section.png` | 3840x2160 A-B cutaway, same boat and shoreline |
| 7 | `review/parity-sheet.png` | All three coasts side by side at equal scale |
| 8 | `kit/common-kit.blend`, `kit/asset-sheet.png` | The reusable module library |

## Cameras (present in every coast scene)

| Camera | Type / lens | Framing |
|---|---|---|
| `COAST_OVERVIEW` | perspective, 58/55/58 mm | high oblique, ~40 deg, land + open water + jetty + boat |
| `COAST_PLAN` | orthographic, scale 330/380/460 | exact nadir, north up, whole site with margin |
| `COAST_APPROACH` | perspective, 50/70/74 mm | mid-distance waterfront with readable building scale |
| `COAST_DETAIL` | perspective, 40/40/38 mm | jetty landing / bank close-up, signature place detail |
| `COAST_SECTION` | orthographic, 54-96 | square-on A-B cut, boat on the waterline |
| `TRAVEL_CAM` | perspective, 58 mm | animated film path: overview -> approach -> lateral -> push |

In the travel files (`work/checkpoints/04-travel-<site>.blend` in the working tree) the
timeline markers `TRAVEL_OVERVIEW` (frame 1) and `TRAVEL_CUTAWAY` (frame 109) bind the
cameras, so scrubbing the timeline plays the edit.

## Scene structure (every coast)

Collections are stable and named for reuse and export:

* `ENV_Land` - vertex-coloured terrain mesh (one object, ~200k quads)
* `ENV_Water` - separate water plane at Z = 0, `ENV_Water_Mat`
* `BLD_Village` - houses as mesh instances from the 4-variant footprint ladder
* `PROP_Survey` - jetty module, survey boat, local craft
* `VEG_Scatter` - palms, shrubs, reed clumps
* `SEC_Section` - authored cutaway slabs (strata, grass cap, water body) + water line;
  **hidden in every beauty shot**, shown only by `COAST_SECTION`
* `CAM_Rigs` - the five cameras, `ORBIT_SITE`, `ORBIT_WATERFRONT`, `TARGET_SURVEY`,
  `TARGET_SECTION`, `TARGET_OVERVIEW`, `TARGET_APPROACH`, `TARGET_DETAIL`
* `LGT_Rig` - `LGT_Sun_Key` and `LGT_Sky_Fill`
* `CAM_Travel` - the film camera and its target (travel files only)

## How to explore

* **Orbit**: select any coast collection and use Numpad 0 to leave camera view; orbit around
  `ORBIT_SITE`, or around `ORBIT_WATERFRONT`/`TARGET_SURVEY` for the waterfront. Cameras use
  `TRACK_TO` constraints, so moving a target reframes the shot.
* **Plan**: `COAST_PLAN` is an orthographic nadir camera; east is +X (image right) and north
  is +Y (image up).
* **Cutaway**: switch to `COAST_SECTION`; the boat sits on the waterline and the same jetty
  is behind it. Toggle the `SEC_Section` collection to compare the cut with the surface scene.
* **Films**: the travel `.blend` files contain the animated camera and the marker-bound cut.

## Units, scale, versions

* 1 Blender unit = 1 metre. +X east, +Y north, +Z up, water surface at Z = 0.
* Coast scenes are ~340-460 m across; globe scene radius is 10 BU (a viewport convenience,
  not a world scale).
* Authored and rendered in **Blender 5.2.2 LTS**, Eevee, on an RTX 4060 Laptop (8 GB).
  Python API 5.2; the compositor grade uses the 5.2 node-group compositor API.
* Colour: `Khronos PBR Neutral`, exposure -0.35, Hue/Sat grade 1.2 (see
  `work/scripts/look_rig.py` in the working tree).

## Export notes

* Every `.blend` here has its images packed; nothing points at an external texture path.
* The GLBs are binary glTF 2.0, **Y-up** (glTF convention), embedded buffers and images,
  **no cameras and no lights**, and no inverted-hull outline modifiers (those are a render
  trick). Water is a separate `ENV_Water` mesh in the coast GLBs. Section meshes are excluded
  from the coast GLBs; they are authoring/illustration content.
* `globe.glb` carries the equirectangular Earth texture embedded plus the three locator
  markers; `common-kit.glb` carries the modular library (houses, jetty, boats, vegetation).
* Re-import checks, dimensions and material counts are in `review/export-check.md`.

## Attribution

* Earth colour art: made with **[Natural Earth](https://www.naturalearthdata.com/) 1:10m Land**
  (public domain), repainted by the project authors. Keep this credit with derived art.
* Local coast geometry is original and illustrative, informed by the place reference boards
  in the handoff ZIP (`references/places/`). No source imagery was copied into textures.
* CityRT audit rules are used as design guidance only; no CityRT mesh, texture, shader or
  code is included.

## Known limitations (read before judging the cutaways)

* Seabed profiles are illustrative, not surveyed; sections are vertically exaggerated
  (x4.0 islands, x3.4 Amur) and cropped to the boat-centred waterfront.
* Globe locators are indicative art positions, not survey coordinates.
* Village building counts are rule-driven (5 m grid + lane mask), not measured.
* Water is a calm flat alpha plane with no animated normals; the GLB version reads flatter
  than the render.
* The ink-and-wash post pipeline from the audit is approximated, not ported
  (see `review/deviations.md`).
* Amur's village reads sparse at overview scale; the shortest remaining path to improve it is
  a denser lane mask around the landing.
