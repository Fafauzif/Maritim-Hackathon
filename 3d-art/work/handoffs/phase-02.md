# Phase 02 handoff · original kit + look development

Status: **complete.** Image rule respected: 0 images attached.

## Artifacts

| Artifact | Path |
|---|---|
| Kit scene (editable) | `work/checkpoints/02-kit.blend` -> promoted to `output/kit/common-kit.blend` |
| Asset sheet render | `work/renders/kit/asset-sheet.png` -> `output/kit/asset-sheet.png` |
| Material proofs (4 palettes) | `work/renders/kit/material-{plaster-tile,timber-hull,land-water,amur-accents}.png` |
| Kit GLB | `output/kit/common-kit.glb` (10 meshes, 6 materials, 82 KB, no cameras/lights) |
| Build script | `work/scripts/kit_build.py` |

## What is in the kit

Four house variants from the audit's 5 m footprint ladder (6x5 gable stilt, 10x5 hip,
5x5 flat stilt, 15x10 gable), a 12 m jetty module, a 9.5 m survey boat, a 6.4 m local craft,
palm / shrub / reed meshes, and 16 material swatches in four families: plaster+tile,
timber+hull, land+water, Amur accents. The scene also carries `KIT_SHEET_CAM` and four
`KIT_MAT_CAM_n` close-ups.

## Measured

* asset sheet 1920x1080: luma 0.594, content 0.943, 25 colour buckets, no dead frame edges.
* material proofs 1280x720: content 0.42-0.99 (three fill the frame, one shows the swatch row).
* Kit GLB re-imports at bounds 38.22 x 25.25 x 11.35 m with 0 cameras and 0 lights.

## Note on the look rig

Phase 02's "commit to a look recipe" decision was made by measurement, not taste: eight rig
candidates and two exposure/saturation sweeps were rendered to disk and scored against the
audit's measured band (`work/verification/lookdev-*.json`). The winner lives in
`work/scripts/look_rig.py` and is the single owner of colour management for all scenes.

## Open issues

* The asset sheet is a catalogue, not a hero beauty shot; the backdrop occupies roughly the
  top quarter of the frame by design.
* Materials are untextured Principled colours. No 1K/2K textures were authored; the brief
  allows procedural colours and reserves textures for hero items.
