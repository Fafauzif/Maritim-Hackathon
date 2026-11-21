# Phase 06 handoff · export, re-import, deliver

Status: **complete.** `tools/check_delivery.py` reports **33/33** artifacts passing.
Image rule respected: 0 images attached.

## Delivery inventory (`3d-art/output/`)

```text
globe/        globe.blend            globe.glb             globe-overview.png 3840x2160
kit/          common-kit.blend       common-kit.glb        asset-sheet.png 1920x1080
coasts/
  kodingareng/ scene.blend coast.glb godview.png mapview.png section.png travel.mp4 review.md
  tunda/       scene.blend coast.glb godview.png mapview.png section.png travel.mp4 review.md
  amur/        scene.blend coast.glb godview.png mapview.png section.png travel.mp4 review.md
review/       parity-sheet.png audit-intake.md handoff.md export-check.md deviations.md
coast-reel.mp4 1920x1080 24fps 20.5 s
```

## Export + re-import results (measured, `work/reports/import-check.json`)

| File | meshes (glTF JSON) | imported objects | bounds (m, Y-up) | images | cameras | lights |
|---|---|---|---|---|---|---|
| globe.glb | 7 (nodes) | 7 | 20.0 x 20.19 x 20.0 | 1 embedded | 0 | 0 |
| common-kit.glb | 10 | 10 | 38.22 x 25.25 x 11.35 | 0 | 0 | 0 |
| kodingareng/coast.glb | 9 meshes / 159 nodes | 159 | 560 x 560 x 20.5 | 0 | 0 | 0 |
| tunda/coast.glb | 9 / 223 | 223 | 600 x 600 x 20.8 | 0 | 0 | 0 |
| amur/coast.glb | 9 / 448 | 448 | 680 x 680 x 18.4 | 0 | 0 | 0 |

All five GLBs: zero cameras, zero punctual lights, embedded buffers, no missing images.
Water is a separate `ENV_Water` object in every coast GLB. Outline modifiers were stripped
before export (render trick, not art geometry).

The five `.blend` files were reopened from the output folder: 5 cameras + 2 lights each
(5 + 3 for the kit), water object present, `SEC_*` section meshes present only in the coast
scenes, globe carries its packed earth texture.

## Films (ffprobe on the delivered files, `work/reports/media.json`)

| File | dimensions | fps | duration | bytes |
|---|---|---|---|---|
| kodingareng/travel.mp4 | 1920x1080 | 24.0 | 5.5 s | 5.0 MB |
| tunda/travel.mp4 | 1920x1080 | 24.0 | 5.5 s | 3.8 MB |
| amur/travel.mp4 | 1920x1080 | 24.0 | 5.5 s | 1.9 MB |
| coast-reel.mp4 | 1920x1080 | 24.0 | 20.5 s | 11.1 MB |

Frame-level verification: each film's frame 109 is the cutaway (content 0.842 / 0.652 /
0.340 = the section fills the frame) and the hold drifts rather than freezing. Reel boundaries
were sampled at frames 0, 71, 72, 203, 204, 335, 336, 467, 468, 491 and confirmed:
globe -> Kodingareng -> Tunda -> Amur -> globe.

## Two render bugs worth remembering

* **Collection visibility cannot be keyframed** in Blender 5.2 (`hide_render` is not
  animatable). The first film cut showed the section camera with the whole scene visible, so
  the cutaway was occluded. Fixed by rendering each shot as its own scene file with fixed
  visibility (`04-travelA/B-<site>.blend`) and concatenating at encode time.
* **A single headless Blender session rendering two animation passes hung** with no CPU
  progress. Splitting into two processes fixed it; both passes then rendered in ~110 s each.

## Check

```
python 3d-art/tools/check_delivery.py 3d-art/output
33/33 required artifacts passed file checks.
```

Not claimed: film playback was not watched, and GLB visual material fidelity was not judged
beyond dimensions, materials, water presence and import thumbnails. Those are recorded as
limits in `output/review/export-check.md`.
