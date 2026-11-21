# Phase 04 handoff · Earth, god's-eye travel and cutaways

Status: **complete.** Globe still, three travel films and the connecting reel are delivered; see phase-06.md.
Image rule respected: 0 images attached.

## Globe

| Item | Value |
|---|---|
| Scene | `work/checkpoints/04-globe.blend` -> `output/globe/globe.blend` |
| Mesh | UV sphere radius 10, 192 x 96 (18k faces), explicit per-face UVs, antimeridian split on -X |
| Texture | supplied `earth-base-color.jpg` (4096x2048, Natural Earth 1:10m repaint), packed |
| Orientation proof | 9 land/ocean probes through the texture's own UV convention, all pass (see `work/reports` in deviations) |
| Cameras | `GLOBE_HOME` (52 mm at 6R, globe fills ~83 % of frame height, no clipping), `GLOBE_REGION_<site>` (70 mm), `GLOBE_REEL` (parented to `GLOBE_ORBIT`, 104 deg -> 128 deg over 72 frames) |
| Markers | 3 original stems + tips + `ANCHOR_<site>` empties at the indicative lat/lon |
| Lights | `GLOBE_Key_Sun` (3.4), `GLOBE_Rim_Sun` (1.1), dark teal world |
| Stills | `work/renders/final-4k/globe_overview.png` 3840x2160; three region renders in `work/renders/globe/` |
| GLB | `output/globe/globe.glb`, 7 meshes, 1 embedded image, 0 cameras/lights, re-imports at 20 x 20.19 x 20 m |

## Travel rigs

| Site | File | Frames | Cut frame | Path |
|---|---|---|---|---|
| Kodingareng | `04-travel-kodingareng.blend` | 132 | 109 | overview -> approach -> 20 m lateral -> push |
| Tunda | `04-travel-tunda.blend` | 132 | 109 | same intent, different geography |
| Amur | `04-travel-amur.blend` | 132 | 109 | same intent, river-bank framing |

1920x1080, 24 fps, Eevee 16 samples, timelime markers bind `TRAVEL_CAM` and then
`COAST_SECTION`, so the edit plays in Blender by scrubbing.

## Known constraint

The travel films are two-shot edits (animated camera, then a cut to the square-on ortho
section). A single continuous camera move into the cut is not attempted; the travel brief
allows an edited match cut and the deviation is recorded in `output/review/deviations.md`.

## Next

Phase 05 renders the ten 4K stills and the parity sheet; phase 06 encodes the films, exports
GLBs and re-imports them.
