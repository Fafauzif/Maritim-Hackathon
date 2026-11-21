# Export check · The Ocean Has Floors

Measured, not asserted. Every table row below was read back from the
delivered file on disk by `work/scripts/verify_exports.py` (reopen each
`.blend`, re-import each `.glb` into a clean factory scene) and by
`ffprobe` for the films. Import thumbnails are saved under
`work/renders/import-check/` for the owner to inspect if anything looks odd.

## GLB re-imports (fresh factory scene, no source scene present)

| File | meshes | materials | imported bounds (m, glTF Y-up) | embedded images | cameras | punctual lights | water object |
|---|---|---|---|---|---|---|---|
| `globe.blend/glb` | 7 | 3 | 20.00 x 20.18 x 20.00 | 1 | 0 | 0 | - |
| `kit.blend/glb` | 10 | 6 | 38.22 x 25.25 x 11.35 | 0 | 0 | 0 | - |
| `kodingareng.blend/glb` | 159 | 7 | 560.00 x 560.00 x 20.50 | 0 | 0 | 0 | ENV_Water |
| `tunda.blend/glb` | 223 | 7 | 600.00 x 600.00 x 20.80 | 0 | 0 | 0 | ENV_Water |
| `amur.blend/glb` | 448 | 7 | 680.00 x 680.00 x 18.35 | 0 | 0 | 0 | ENV_Water |

All five GLBs contain zero cameras and zero punctual lights, embed their
resources (no external URIs), and import with no missing images.

## Editable .blend reopen checks

| File | scene | objects | mesh objects | materials | file images | packed | water object | section mesh | cameras | lights |
|---|---|---|---|---|---|---|---|---|---|---|
| `globe/scene.blend` | Earth_Globe | 18 | 7 | 35 | 1 | 1 | - | - | 5 | 2 |
| `kit/scene.blend` | KitScene | 55 | 28 | 32 | 0 | 0 | - | - | 5 | 3 |
| `kodingareng/scene.blend` | CoastScene | 179 | 165 | 21 | 0 | 0 | ENV_Water | yes | 5 | 2 |
| `tunda/scene.blend` | CoastScene | 243 | 229 | 21 | 0 | 0 | ENV_Water | yes | 5 | 2 |
| `amur/scene.blend` | CoastScene | 468 | 454 | 20 | 0 | 0 | ENV_Water | yes | 5 | 2 |

## Films (ffprobe on the delivered files)

| File | size | codec | fps | duration |
|---|---|---|---|---|
| `travel.mp4` | 1920x1080 | h264 | 24.00 | 5.50 s |
| `travel.mp4` | 1920x1080 | h264 | 24.00 | 5.50 s |
| `travel.mp4` | 1920x1080 | h264 | 24.00 | 5.50 s |
| `coast-reel.mp4` | 1920x1080 | h264 | 24.00 | 20.50 s |

## Stills placed

| File | size | bytes |
|---|---|---|
| `globe/globe-overview.png` | 3840x2160 | 8529335 |
| `coasts/kodingareng/godview.png` | 3840x2160 | 9370815 |
| `coasts/kodingareng/mapview.png` | 3840x2160 | 9163483 |
| `coasts/kodingareng/section.png` | 3840x2160 | 7509489 |
| `coasts/tunda/godview.png` | 3840x2160 | 8746038 |
| `coasts/tunda/mapview.png` | 3840x2160 | 8972542 |
| `coasts/tunda/section.png` | 3840x2160 | 7371819 |
| `coasts/amur/godview.png` | 3840x2160 | 8763048 |
| `coasts/amur/mapview.png` | 3840x2160 | 8434535 |
| `coasts/amur/section.png` | 3840x2160 | 7213615 |

## Limitations of this check

* File structure, bounds, material and image presence are verified; **visual
  quality of the GLB materials is not**. glTF has no equivalent of the Blender
  alpha-blend water, so the portable water reads flatter than the render.
* The outline modules are stripped before export, so GLBs are ~35 % lighter
  than the render geometry and carry no ink lines.
* Film playback was not watched; container, dimensions, fps and duration were
  probed. A human should play `coast-reel.mp4` once before publishing.
