# Blender workstation workflow

**Target workstation:** Blender 5.2.2, RTX 4060 Laptop, 8 GB VRAM. Confirm the actual version and add-on capabilities, the evaluation mode, the active scene path, a local write path, effective renderer and observed memory needs. Treat every number below as a starting production budget. The project’s actual style notes may influence these values. Three separate local scenes and a separate globe keep edit and render costs predictable.

## Use the installed MCP

1. In DSH, enumerate connected MCP tools and their schemas. Depending on the installed implementation, there may be a scene summary, screenshot/viewport/render view, and an execute-Python tool. Discover what actually exists. Keep a plain record of the names and tool result behavior in `work/tooling.md`.
2. See the running scene summary before acting. Never clear an unsaved artist file through a tool call. Open a new Blender scene/starter for production or use a clean second Blender instance with its intended MCP attachment. Save every checkpoint inside this art folder.
3. Write reusable scripts under `work/scripts/`. Keep scripts split by operation with explicit paths and parameters. Use Blender MCP for bounded modeling/editing calls and visual checks. Do not send a giant unreviewable one-shot script. Repeating a stage should rebuild only the collections owned by that stage or create a versioned scene. Check the active file and collection ownership before deleting generated items. 
4. Use the verified Blender executable for background rendering when a synchronous MCP call would tie up the editor. Use saved scenes and actual output paths. Check whether the Blender process and DSH see the same filesystem, particularly under WSL. Use Windows Blender and compatible local paths unless the connected setup proves otherwise. Do not rely on a guessed install location.
5. For each render, log engine, scene, camera, resolution, render time and observed memory where measurable. Screenshot capture shows a real viewport state; final inspection requires image bytes or a human viewing the logged file. An image path by itself is not a review.

## Render budget and recovery

| Work | Starting point | Scale up if |
|---|---|---|
| Blockout stills | 960×540, Eevee, simple ambient and one sun. Inspect a 320 px derivative as well. | The place and boat are legible before materials. |
| Look development | 1440×810 or 1920×1080 drafts with the actual render engine; one still at a time. | No obvious glare, aliasing or memory pressure. |
| Final stills | 3840×2160. Eevee as a predictable default. Test Cycles + OptiX on a saved comparison shot if it improves the cutaway/reflections within budget. | The revision sheet supports the improvement; final files from all three coasts use a comparable finish. |
| Animation | 24 fps. Use a 540p animatic before 1080p. In final motion use frame sequences and encode afterward, so an interruption only costs unfinished frames. | Time a small start/middle/end sample. Keep 3 concurrent jobs off one laptop GPU. |
| Geometry | Instanced modules and vegetation. Start under roughly 300k evaluated triangles per local view, with a written reason for expensive silhouettes. | Inspect measured triangle counts, memory, and actual visual contribution. |
| Textures | Shared palette or 1K atlas on most parts, 2K where a hero object or coastline earns it. The supplied globe image may be larger for coastline clarity. | Look for reuse first. Pack textures and confirm GLB import. |

Use surface materials before costly volumetric water. For the cutaway, a well-shaped clipping edge, mesh seabed and readable tonal separation can look better than stacking several transparent volumes. Keep stationary shoreline landmarks and a crisp horizon or crop where needed. Streamline unseen portions and repeated details before cutting any assigned coast. Lower draft settings or isolate a heavy asset when a render fails. Keep each final still target at 4K unless a concrete blocker remains. Record GPU fallback and actual settings.

## Headless examples

These are examples of invocation shape. Use the executable and scene created on the workstation. Set the desired camera and render size in the saved file or via a small pre-render script. Check actual permissions and validate filenames.

```powershell
& $blender -b $savedScene -o "$renderDir/wide_####" -F PNG -f 1
& $blender -b $savedScene -o "$renderDir/travel_####" -F PNG -s 1 -e 24 -a
```

A PNG frame folder survives a renderer interruption. Inspect coverage and actual frame count before encoding. Use an existing video encoder or Blender's video sequencer, H.264/MP4 at 24 fps. Do not install toolchains or download large assets automatically when the provided workflow already suffices. Use the documented input order for Blender CLI and the capabilities present in the installed version. Reference: https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html

For a known renderer on NVIDIA, compare Eevee and Cycles in one contained benchmark. OptiX availability depends on installed Blender and drivers. Use measured behavior and the version from the machine. Reference: https://docs.blender.org/manual/en/5.2/render/cycles/gpu_rendering.html
