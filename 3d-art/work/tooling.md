# Tooling — what actually exists

Probed 2026-11-21 in this session. Nothing here is assumed from the brief.

## Blender / MCP

| Item | Actual value | How verified |
|---|---|---|
| Blender version | **5.2.2 LTS** | `bpy.app.version_string` from live session |
| Session file at start | default untitled startup (Cube, Camera, Light) | `mcp__blender__get_scene_info` |
| Render engine default | `BLENDER_EEVEE` | scene report; engines available: EEVEE, WORKBENCH, CYCLES |
| GPU / backend | **NVIDIA GeForce RTX 4060 Laptop GPU**, compute device type **OPTIX** | Cycles preferences probe |
| Python in Blender | 3.13.13 | skill `env_report.py` |
| Rigify | available | `env_report.py` |

## MCP tools discovered

| Tool | Behaviour |
|---|---|
| `mcp__blender__get_scene_info` | structured scene JSON: objects, transforms, collections, materials, cameras, lights |
| `mcp__blender__get_object_info` | per-object transform, bbox, modifier stack, counts |
| `mcp__blender__execute_blender_code` | executes Python in the live session; returns `result` dict, captured `stdout`/`stderr`; returns image content if `result["image_base64"]` is set |
| `mcp__blender__get_viewport_screenshot` | OpenGL preview render from active camera as PNG |

There is no `look`/`render` tool distinct from these; final inspection therefore uses either `execute_blender_code` returning `image_base64` or a rendered PNG read back through the harness image channel.

## Path parity

- Harness workspace: `C:\Users\fauzi\OneDrive\Desktop\DSH\Maritim Hackathon`
- Blender writes to the same absolute path: `preflight_smoke.py` saved `00-preflight.blend` and rendered `work/renders/smoke.png` (510,318 bytes), and the harness read the same bytes back at the same path. **Same filesystem, same paths.**
- `bpy.data.filepath` after save: `...\3d-art\work\checkpoints\00-preflight.blend`

## Headless renderer for final work

`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` exists (5.2 install tree; 4.5 also installed and unused). Reserved for 4K stills and animation frame sequences so the interactive session is not blocked.

## Encoders / checkers

| Tool | Path / version |
|---|---|
| ffmpeg | `C:\Users\fauzi\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe` |
| python | 3.14.4 (`python --version`) |
| delivery checker | `3d-art\tools\check_delivery.py`, expects **33** artifacts |

## Known behaviour notes

- Running `bpy.ops.object.select_all` failed once with `context is incorrect` while the startup Cube was in **EDIT_MESH** mode. Scripts must set OBJECT mode and prefer the data API.
- `material.use_nodes` / `world.use_nodes` emit `DeprecationWarning` in 5.2 (removal planned for 6.0). Harmless; noted so it is not mistaken for an error later.

## Blender 5.2 API facts learned the hard way (2026-11-21, phase 03)

| Fact | Detail |
|---|---|
| **Compositor output node is gone** | `CompositorNodeComposite` raises `Node type undefined`. A compositor tree in 5.2 is a node group: declare an `Image` output socket on `scene.compositing_node_group.interface` and terminate with `NodeGroupOutput`. Until this was fixed the Hue/Sat grade silently did nothing (nodes existed, no output). |
| Compositor access | `scene.compositing_node_group` (not `scene.node_tree`); `scene.render.use_compositing` must stay true. |
| Ortho framing | `ortho_scale` maps to the **width** when `sensor_fit='AUTO'` and resolution is 16:9. Verified by projecting local ±scale/2 through `world_to_camera_view` → x = 1.0 / 0.0. Vertical extent = `ortho_scale / aspect`. |
| Dynamic enum introspection | `view_settings.bl_rna...enum_items` returns only `NONE` for view transforms/looks. Probe by assigning candidate strings in `try/except` instead. Available transforms: AgX, Standard, Khronos PBR Neutral, Filmic, False Color, Raw. Available looks include AgX Punchy / High / Medium High / Base / Very Low / Very High. |
| Workbench clay | `scene.display.shading.color_type` accepts `MATERIAL` (uses `mat.diffuse_color`), `SINGLE`, `TEXTURE`, `OBJECT`, `VERTEX`. `SINGLE` produced unreadable flat clay; `MATERIAL` + shadows + cavity reads. |
| Colour management ownership | `run_build.py` used to re-impose AgX/exposure after `look_rig.apply`, silently undoing the measured rig. `look_rig.py` is now the only writer — do not set view transform anywhere else. |
| Material cache invalidation | Opening another `.blend` invalidates Python-held datablock references (`ReferenceError: StructRNA of type Material has been removed`). `site_lib.ink_material()` revalidates its cache every call; do the same for any cached datablock. |
| Save-before-rebuild hazard | `run_build.build()` used to `save_as_mainfile(target)` *before* rebuilding, which could write the wrong site's scene into another checkpoint. It now parks the open file in `work/checkpoints/_autosave-before-build.blend`. |

## Verification tooling added this run (`work/scripts/`)

| Script | What it proves |
|---|---|
| `verify_shot.py` | ray-casts 64×36 grid through each camera; classifies frame share as water/land/buildings/vegetation/survey-kit/section/background; projects the survey boat to pixels. Writes `work/verification/shot-verify.json` + `.txt`. |
| `verify_320.py` | rescales the boat box to the 320 px derivative, measures luma contrast against a surrounding ring and the inner span; Otsu-splits the thumbnail for silhouette survival. |
| `contact_sheet.py` | tiles renders into ONE labelled PNG on disk (`stats`, `down`, `sheet` subcommands) — the only allowed visual-review artifact. |
| `palette_check.py` | k-means 6-colour palette + luma/saturation of a render vs `cityrt-audit/analysis/palette/<style>.json`, weighted CIE76 ΔE. |
| `ascii_probe.py` | luminance map + band/thirds statistics as text, for shape debugging without an image. |
| `look_rig.py` | single shared light/colour-manager rig for all three coasts (values chosen by measured sweeps, see `work/verification/lookdev-*.json`). |
