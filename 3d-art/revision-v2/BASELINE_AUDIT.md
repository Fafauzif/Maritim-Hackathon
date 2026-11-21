# Baseline audit · Maritim-Hackathon a0295d3

Audit of the checked-out master and the owner's context pack. V1 is the starting point for a new art revision. This document records evidence and limitations for DSH to recheck locally.

## Inventory and validation

- `3d-art/output/` holds 33 files. Three complete coast folders each contain `scene.blend`, `coast.glb`, three 3840×2160 PNGs, a travel film, and a review note. Globe, shared kit, reel and review folder complete the set. `3d-art/tools/check_delivery.py` returned 33/33. It checks the original artifact names and basic structures. It does not cover v2 or replace visual review.
- All five GLBs were re-imported in Blender 4.3.2 during the audit. Coast GLB sizes were roughly 3.0 MB Kodingareng, 4.6 MB Tunda, and 3.3 MB Amur. Rendered triangle counts calculated across all mesh instances were approximately 128k, 156k, and 137k respectively. Coast scene exports have independent water, visible props, and target empties. Active shareable cameras and sections are in the editable source. The portable GLBs exclude cameras, lights, outline modifiers and section geometry. Water exports as a glTF BLEND material.
- A read-only audit decoded all four baseline video streams with FFmpeg. Metadata showed 1920×1080, 24 fps, 5.5 s per coast and a 20.5 s combined reel. Decoding proves stream integrity. It leaves continuity and styling to playback review.
- Baseline files report Blender 5.2.2 on Windows with Eevee and an RTX 4060 Laptop GPU. The audit's Blender 4.3.2 rejected the Kodingareng editable file header. Reopen with the local authoring setup. The baseline work tree is about 1.3 GiB and the original output about 126 MiB. Keep raw sequences and historical checkpoints out of the friend ZIP.
- CityRT audit tools ran 12 of 14 tests successfully in the audit environment. Two browser tests required local Playwright/browser configuration. The evidence check flagged three document hash mismatches, and the coverage file contains stale assertions alongside later live evidence. The user-supplied screenshots, inspectable visual captures, and the existing art bible are sufficient for creative direction. The v2 art run does not depend on repairing or rerunning the website audit.
- There is no playable product in this checkout. `blender-mcp/` is a local Blender tool bridge. The product mockups come from the seven-page brief, not a shipped app. The functional build has a separate owner.

## Where to work

| Existing source | Reuse and verify for v2 |
|---|---|
| `3d-art/work/scripts/site_build.py` | Site settings, height field, terrain, independent water plane, palette, section location/exaggeration. Redesign silhouettes, shallow bands and habitat cues within the illustrative scope. |
| `3d-art/work/scripts/props_build.py`, `kit_build.py` | Four house variants, basic jetty, hulls, palms, shrubs and reeds. Build the local revisions from reusable components. Verify full rotated bounds and actual site placement. |
| `3d-art/work/scripts/scene_build.py`, `look_rig.py`, `run_build.py` | Named collections and cameras, section builder, lighting/compositor and orchestration. Keep stable collection names where possible, use version-appropriate APIs and test revised builders in v2. |
| `3d-art/work/scripts/globe_build.py`, `references/globe/` | Natural Earth-based globe, UV function, palette seed and regional cameras. Correct all three locators from the place board and rebuild the markers, region targets, exports and related media. |
| `3d-art/work/scripts/travel_build.py`, `travel_passes.py`, `render_pass.py`, `encode_media.py` | Existing camera path, separate fixed-visibility shot files and H.264 sequence pipeline. Port away from absolute Windows paths and cache by exact scene and settings. |
| `3d-art/work/scripts/export_build.py`, `verify_exports.py`, `verify_shot.py`, `verify_320.py` | Baseline Blender export and re-import, camera-ray geometry, legibility probes. Extend for separate section exports, runtime view comparison, material and anchor validation. |
| `3d-art/work/scripts/assemble_outputs.py`, `3d-art/tools/check_delivery.py`, `3d-art/output/review/` | Baseline assembly, path inventory, deviations and review format. Write a new handoff with v2 truth. Legacy mesh and node counts vary between reports and final files. Recompute from final bytes. |
| `3d-art/brief/`, `3d-art/references/places/`, `cityrt-audit/docs/` | Workflow references, place identity boards and visual vocabulary. V2 decisions in this extracted plan take precedence. |

Several orchestration, render and QA scripts and the PowerShell wrapper assume one Windows user's local folder or program paths. Create path-parameterized v2 entry points. `3d-art/work/progress.json` and the v1 resume prompt refer to a finished run. Use the new ledger and resume prompt.

## Priority defects and proof

| Defect | Concrete v2 test |
|---|---|
| Settlements read like scattered similar blocks, with little path hierarchy. | Lay out connected lanes and distinct waterfront landmarks. Verify actual rotated footprints, adjacency, frontages and access on a top-down clay proof. Compare beauty and imported looks at 960 and 320 px. |
| Procedural placement can put a Kodingareng boat on dry ground. Existing jetty deck starts can miss the land height and the old rail can rotate across its span. | Sample terrain under all hulls, check draft and shore clearance, run along-shore/jetty cameras, match dry route to gangway and deck, and verify rails run along the pier. |
| Boat loft and extra coplanar faces can create flicker. | Inspect at grazing angles in Blender and clean import. Confirm no overlapping faces, outward normals and consistent hull, deck and trim slots. |
| Dark cutaways crop or lose the bottom and boat. | Show a readable waterline, continuous bed, shoreline landmark and boat in a lit side section. Map A-to-B and section anchor transforms explicitly. |
| Globe locators don't match the project's place board. | Update all three and verify marker orientation and location in source, GLB, region shots and final reel. Tunda moves approximately 68 km. |
| Pipeline polish and delivery checks don’t carry from Blender to runtime. | Verify every v2 GLB in a fresh import with test lighting and show matching camera contact sheets. Validate air-gapped bundle extraction, missing textures, axes and launch notes. |
