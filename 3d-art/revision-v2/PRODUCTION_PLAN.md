# The Ocean Has Floors · v2 implementation plan

**Goal.** Produce revised source files, runtime GLBs, 4K art, evaluated travel media and a clean packaged handoff for the whole asset set. **Spec.** `ART_DIRECTION.md` and `HANDOFF_CONTRACT.md` set visual, evidence and interoperability requirements. **Stack.** Discover DSH’s configured Blender MCP, installed Blender, render engines and encoder. Default to Eevee and H.264. Use local Blender Python for reproducible builds and inspected MCP calls for interactive work.

The owner has approved the full local execution. The Kodingareng look proof is the first internal review gate. Use a real visual check and continue when the proof meets the acceptance criteria. Preserve a way to retry and report exceptions explicitly. Work in one safe Blender production session at a time. Independent agents in DSH may inspect code, render proofs or verify archives read-only when available. Keep scene editing and render ownership with one writer.

## Decisions that apply throughout

- Resolve the repo root with `git rev-parse --show-toplevel` where possible or verify the three project folders and baseline outputs manually. Use the current local source. Record actual Git hash, dirty status and v1 input hashes. Never overwrite v1 or unrelated unsaved work.
- Use run-specific directories and atomic writes for the ledger and published outputs. Write production scripts under v2. Parameterize paths instead of copying hard-coded Windows roots. Stage only finished, reviewed assets in the final package tree.
- Before work on a requirement, record what fails or what is missing in v1. End each phase with evidence from the actual output. For artwork, inspect images with meaningful comparisons. For runtime, run fresh import and mapping checks. The v1 file checker is a baseline check only.
- Blockers to watch closely are version/path mismatch, loss of v1 state, visually unreviewable frames, incorrect boat/jetty and section placement, GLB water and transform regressions, backfilled false science, incomplete animation frames, and final archive dependencies that only exist on the artist’s PC.

### Planned entry points

Create or adapt these under `V2/work/scripts/` inside DSH. These are implementation tasks in the local run.

| Script | Interface and role |
|---|---|
| `build_v2.py` | Blender script invoked with `-- --repo-root <root> --run-root <run> --target <kit|globe|kodingareng|tunda|amur>`. Rebuild a bounded target to a distinct checkpoint using v2 sources. A single run config supplies the look recipe, unique site layout and renderer choice. |
| `render_v2.py` | Background Blender render entry with `-- --run-root <run> --task <shot-id> --profile <proof|final>` plus optional `--frame-start N --frame-end N`. Load actual registered scene/camera settings and save only its result. Use per-shot frame directories and fixed visibility. |
| `export_v2.py` | Blender entry with `-- --run-root <run> --staging-root <bundle> --asset-id <id>`. Export explicit object sets and required empties from a verified checkpoint. Keep outlines/extra render geometry out of the portable copy whenever they fail import or render tests. |
| `validate_v2.py` | Standard Python entry with `--bundle-root <bundle> --report <json>`, returns nonzero on absent, corrupt, misidentified or unreferenced required outputs. Checks inventory, manifests, GLB structure, paths, digests, anchor transforms and advertised media according to the contract. Support a provisional mode or validate subgroups during the run. |
| `verify_blender_assets_v2.py` | Blender entry with `-- --bundle-root <bundle> --asset-id <id> --report <json>`. One clean app process per independently reopened BLEND or a reliably reset scene between GLB imports. Save metrics and matching representative previews. |
| `build_handoff_v2.py` | Standard Python entry with `--staging-root <bundle> --out <zip> --verify-extract <dir>`. Validate structure, hash all payload files except the hash list itself, write atomically, extract independently and verify archive checksums and path safety. Phase 7 checks content with Blender and encoder tools from the extraction. |

If an existing script already has the needed behavior, wrap or adapt the minimum parts into v2. Separation by task can be preserved through subcommands when it keeps inputs and outputs inspectable. Document actual commands and supported options in final `source/BUILD.md`.

### Command templates for the Windows local run

Set the variables from preflight. Keep absolute paths in the transient run config or shell, and relative paths inside the shipped project.

```powershell
$V2 = Join-Path $repoRoot '3d-art/revision-v2'
$scriptRoot = Join-Path $V2 'work/scripts'
& $blender --background --factory-startup --python-exit-code 1 --python (Join-Path $scriptRoot 'build_v2.py') -- --repo-root $repoRoot --run-root $runRoot --target kodingareng
if ($LASTEXITCODE -ne 0) { throw 'V2 build failed. Inspect its run log.' }
& $blender --background --factory-startup --python-exit-code 1 --python (Join-Path $scriptRoot 'render_v2.py') -- --run-root $runRoot --task 'kodingareng-travel-a' --profile final --frame-start 1 --frame-end 132
if ($LASTEXITCODE -ne 0) { throw 'V2 render failed. Inspect frame coverage and logs.' }
& $python (Join-Path $scriptRoot 'validate_v2.py') --bundle-root $bundleRoot --report $reportPath
if ($LASTEXITCODE -ne 0) { throw 'V2 pack validation failed. See the report.' }
```

The frame range above illustrates argument passing. The run's shot registration defines the actual A/B ranges. Time at least three representative full-resolution samples and project the low and high estimate across missing frames. Estimate sequence space as the measured upper sample size multiplied by remaining frames plus current staged bytes, candidate ZIP, extraction space and free-space reserve. Recalculate after each cohort. For long work, record render IDs and a recoverable checkpoint before handing control to the background process. Continue a different non-mutating task only when it does not contend for the GPU or the same files.

### Phase 0 · preflight and protect the baseline

Inputs are repo, local MCP connection, local Blender, filesystem and encoder. Produce `<run>/logs/preflight.md`, run ledger, baseline hash list and disposable probe.

- [ ] Inspect repository status and required v1 scenes/media without pulling or modifying the user's working branch. Read the v1 workflow and portability notes. Record exact paths, selected v1 state and hashes of the 33 baseline outputs.
- [ ] Discover scene info, execute-Python and viewport/read-image capabilities. Check the live Blender file path and dirty state before changing anything. Use a separate safe production scene or an explicitly saved copy. Never clear a user’s active work.
- [ ] Test path parity with a file written by Blender under the run directory and read by DSH, then read a small file produced by DSH from Blender. Reconcile PowerShell, Windows, WSL or mounted paths with measured behavior. Keep data output under the repo’s v2 folder.
- [ ] Measure Blender versions through both MCP and the CLI. In a fresh process, open a copy of one coast, inspect objects, render a small frame, and export and re-import a GLB. Confirm the actual v1 grade and source portability can be inspected. Verify encoder and existing available disk/memory. Probe FFmpeg or Blender's H.264 support. Open or transmit an actual image to establish the visual review route.
- [ ] Assess whether a CLI image can be read, an MCP screenshot is available, or DSH can read the PNG through a separate image-capable host. If none works, continue objective work with review sheets on disk and mark visual approval pending. Do not substitute numeric colour checks for seeing the artwork.
- [ ] Confirm the baseline survived preflight. Write versioned paths, discovered executable locations for this run, sample timings, renderer, recovery route, and the initial ledger. Proceed once safe Blender access and source recovery exist.

**Evidence.** Scene-open log or documented rebuild route, real probe PNG and GLB with verification, verified existing outputs. If source cannot open, first use an already installed compatible local Blender. If unavailable, prove the GLBs and use v1 builders/anchors to reconstruct v2 authoring cameras, sections and lost render effects. Preserve original files. If both local Blender control paths are unavailable, report the exact missing capability and still complete any independent inventory.

### Phase 1 · reference, lighting and scale proof

Produce `<run>/proofs/look/`, `<run>/proofs/look/decision.md`, and reusable v2 palette/camera settings.

- [ ] Curate matched v1 images from `output/coasts/kodingareng/`. Place them next to the two user reference sheets and the newest shot. Identify which modifications affect composition, recognizable silhouette, material hierarchy, water and edge treatment.
- [ ] Build a small representative waterfront proof in a copy or rebuilt sandbox. Include at least two roof families, boat, shore-to-deck transition, foliage and editable water. Create the matched A/B/C images in the art spec. Inspect a high oblique and a slightly steeper camera from the same subject area. Use the same crop and scale for visual comparisons.
- [ ] Render 960×540 and derive 320 px contact sheets, plus a grayscale proof so material and lighting contrast can be judged independently of hue. Produce a same-angle GLB import proof with representative lighting using the portable water material. Judge the roof/land separation, jetty approach, survey boat read, and room for overlays.
- [ ] Pick one curve for lighting, palettes and contours. Record examples that show the improvement and what the portable model does differently. Carry visual evidence into later tasks. If silhouette, alpha sorting, or saturation fails, fix the cause and rerun a contained proof. The final result should look like an illustrated miniature suited to the officer’s map.
- [ ] Record the chosen contour method and image export transform for the verified Blender version. Apply it once. Keep pose, light direction and framing stable during comparison.

**Gate.** A reviewer can identify the shore route, landing, boat and at least two building types in reduced views. Step from source render to lightweight GLB without losing the key layout or separations. Evidence includes matched images and a factual rationale.

### Phase 2 · shared kit, materials and authored placement

Produce packed `source/kit/common-kit.blend`, `runtime/kit/common-kit.glb`, `media/kit/asset-sheet.png` and the instance/placement rules used by all site builders.

- [ ] Audit the existing kit by stable object ID, dimensions, material, pivot and site usages. Keep proven asset silhouettes and clean geometry where practical.
- [ ] Make region-appropriate families using the art spec. Upgrade roofs, eaves, shutters, doors, stilts, steps, props, mooring rails, structural supports, cabins, working boats, palms, shrubs and reeds. Retain old kit concepts in improved form and add only modules that appear in approved scenes. Preserve editable material alternatives and include named exemplars on a clear kit sheet.
- [ ] Work out survey and local hull draft, bow orientation and origin. Remove duplicate loft faces and assign material by intended face groups. Build the pier route, decking and parallel rails with correct local axes. Use linked meshes or instances for repeated modules when possible.
- [ ] Implement dry and wet placement assertions against actual final geometry. House corners and footprints must register to lanes and valid base height or intentional stilt positions. Sample underside of hull at centre, bow, stern, both sides and enough intermediate points to catch visible intersections. Below-water keel stays clear of the bed. Gangway connects dry surface to landing and deck in the direction of its path. Rail and struts follow the actual pier geometry.
- [ ] Check each kit mesh in a Blender proof and after clean GLB import. Check sensible pivots, meaningful names, normals, no accidental doubles, stable dimensions and roughness. Log portable defaults and the intended low-complexity differences.

**Gate.** The reusable parts are separately selectable and plausible at shared scale. Their exported appearance matches the important materials and silhouette. The asset sheet documents every kit component referenced in the final manifest.

### Phase 3 · all three coasts, sections and stills

Stage the three primary source scenes, all coast and section GLBs, five clean stills per site, and three site review entries. Complete the same sequence for each site with unique authored composition.

- [ ] Kodingareng first. Reshape the shore around lanes, waterfront, open water and the refitted jetty. Use the approved kit, bespoke landing detail and layered vegetation. Move all failed hull placements to navigable-looking art water, and re-anchor the cut line through the intended vessel target.
- [ ] Tunda. Apply the common visual style to a greener coast with variation in shoreline and vegetation structure and a sheltered landing. Keep the access/gangway convincing. Use Tunda-specific silhouette and palette cues.
- [ ] Amur. Redesign the river-to-bay shallows and low wetland bands, with varied asymmetry, a legible working landing and sufficient open estuary. A denser small landing cluster can aid navigation while retaining wetland geography.
- [ ] For each site, validate collisions, hull depth, route continuity and paired transforms. Keep water independent, verify Z=0 in the sea-level convention, and test its shoreline sorted correctly from all mandatory angles. If alpha fails in import, prefer a simpler shaded opaque or lightly blended portable material while preserving the shared water node and documenting changes.
- [ ] Regenerate the A–B cut from the revised geometry and relocate the shared point anchors. Close wet/dry topology and use a coherent section light. Compare original and revised profile, canvas fill and label space. Inspect in side view and compare the section against the overhead photo-style proof. Record exaggeration around Z=0 and explicitly label illustrated bed provenance in the docs. Use the same camera, framing and background for the two Kodingareng evidence plates, then give the separate section explanation its own framing and evidence label.
- [ ] Save named camera presets and the default viewport. At proof resolution inspect overhead, north-up plan, approach, detail, and cutaway for each site. Record frame targets, land/water shares where useful, hull positions and any failed object-space check. Iterate on composition before enabling the final 4K render batch.
- [ ] Stage `scene.blend`, `coast.glb`, `section.glb`, five clean PNGs and the two fixed-view plus one section pitch plate. Keep a route through the v2 run for review and export regeneration.

**Gate.** Three complete distinct worlds in Blender and import tests, 15 clean stills, both view variants capable of using the same scene anchors, no blocked site left as a placeholder. Run matched 960 and 320 comparisons. The annotated plates show the verified regional model pair without placing measured layers against an unrelated illustrative bed.

### Phase 4 · globe and destination transitions

Stage new globe source, GLB, 4K locator overview and the budget-friendly globe travel shots.

- [ ] Reuse the rights-cleared Natural Earth base and orientation probes. Improve art-grade shading, simplified coast fill, look consistency and marker treatment. Keep original asset work and provenance.
- [ ] Replace all three marker coordinates with the referenced place defaults. Confirm sign, hemisphere, longitude ordering, texture seam and location using known visual landmarks. Calculate the geographic forward projection with the existing sphere convention and check actual exported marker positions on the sphere after basis conversion. Retarget regional cameras and design legible marker separation for the two Indonesian sites. Keep `ANCHOR_<site>` stable.
- [ ] Match tone, travel pacing and screen direction between globe shot and its three local edits. Animate stable eased global motion and use a considered editorial transition into each independently scaled coast. Deliver clean opening and closing shots for the reel pipeline. Photograph title/labels separately or document their placement if the globe overview is intended as an annotated review view.
- [ ] Test pack/reopen for globe images and compare local region, locator position and camera screenshots in GLB. Refresh the globe still from final selected settings.

**Gate.** Three correct locators and camera targets in Blender and GLB, recognizable geography, packed image, coherent visual treatment, reusable markers and clips.

### Phase 5 · travel films and combined reel

Produce three 1080p travel films and one 1080p reel with reproducible sequences. Preserve ability to adjust the edit.

- [ ] Make matching animatics at 540p or lower using each approved scene. Hold the establishing shot long enough to identify location, show movement and parallax, then reveal the same landmark in the section and hold long enough to read it. Default 7 s/168 frames at 24 fps per site, including roughly 1.5 s for section. Globe intro/outro default 4 s and 2 s. Start offsets and actual frame boundaries belong in shot registration.
- [ ] Use a dedicated overview shot scene/checkpoint and a separate fixed-visibility cutaway shot scene/checkpoint or derived render process. The v1 Blender setup could neither keyframe that collection visibility reliably nor render two such passes in one process without hanging. Recheck behavior on the actual version. Keep an editable path for both views and a documented frame-exact edit.
- [ ] Sample an early, midpoint and last/near-cut PNG for each rig at actual 1080p settings. Derive a range for elapsed time and sample disk requirements. Leave enough free space for full sequences, staging, ZIP and independent extraction with a reserve. Run one GPU render at a time. Use command templates in the documented actual local shell.
- [ ] Register exact sequence range and a key derived from source and relevant dependencies, camera, render settings, frame rate and scene signature. Render to numbered PNGs, validate full decode, dimensions and exact expected frame indices. Resume missing/corrupt frames under the same key; use a new key when inputs change. Keep sequence render logs. Avoid skipping a frame by comparing file counts alone.
- [ ] Encode reviewed source sequences atomically to H.264/yuv420p MP4. Build reel from approved global intro, Kodingareng, Tunda, Amur and return. Preserve batch stdout/stderr and time each step. With `ffprobe` available, verify dimensions, frame rate, codec, duration and frame count. Decode full streams with `ffmpeg -v error -xerror -i <file> -map 0:v:0 -f null -`, or test a working equivalent.
- [ ] View every clip and the reel if the harness can view video. Otherwise inspect image samples across the edit, including at least ±2 frames around every cut, then record the review as a sampled visual check. Check black or repeated frames outside planned holds, shoreline pops, clipping, brightness jumps, material shimmer and camera ease. Resolve faults and re-encode only affected output.

**Gate.** Exactly three revised travel clips plus reel with complete decodable frame ranges, matching camera and scene versions and recorded cut checks. Capture enough proof for the owner or teammate to evaluate the complete sequence.

### Phase 6 · export validation and technical review

Use the final candidate assets and all site, globe, kit and camera proofs. Produce `review/runtime-parity.png`, `review/validation.json` and `review/review-report.md`.

- [ ] Freeze candidate source scenes and export GLBs with explicit collection selection, node and material naming. Keep cast shadows, render grades and stylization in authoring sources. Use baked/simple compatible materials where needed. Implement manifest entries from the actual exported bytes. Audit buffer/texture embedding, GLB version, axes, bounds, exact named nodes, node uniqueness, and coast versus section transform agreement.
- [ ] Use neutral baseline for web compatibility. Test all eight GLBs in independently reset or fresh Blender launches, then each of the five BLEND files in fresh launches with auto-execution disabled when feasible. Take visual parity images for all coasts, the cutaways, the kit and globe under controlled test lighting. Confirm materials, no missing textures, separate water, named transforms and composition.
- [ ] For object-space checks, use a point with three unequal components on each adjustable coast to expose an axis error. Compare A/B and landmark positions to the manifest in both exported files in glTF axes, expected coordinate tolerance ≤1 cm. Derive and verify camera/projection descriptors for the important named views. If the actual teammate loader is available, test loading from a staged asset copy as an additional verification.
- [ ] Generate tri/mesh/node/material/bounds/texture report from final geometry and bytes. Review payload sizes and actual loading where possible. Fix accidental duplication, unnecessary alpha blending, texture packing and unused or oversized geometry. Keep an importable uncompressed base. Explain only significant remaining deviations.
- [ ] Verify evidence fixture integrity and three pitch plates. The two comparison base images must be identically aligned outside the overlay region. Check date, units, current bearing and scientific qualifiers. Clean media/GLBs keep the field request and data overlays available to teammates as separate inputs.
- [ ] Generate side-by-side baseline/revision shots at comparable crops and an all-site equal-display-size parity sheet. Compare each expected output family for an actual visual or technical improvement. Update the per-site review and note scopes and limited validation. Where an optional external integration test was unavailable, label it distinctly from the required portable import check.

**Gate.** Eight GLBs validated and imported, five editable source scenes reopen, all assets align and match the reviewed stills and media, source and evidence provenance match the provided context.

### Phase 7 · teammate handoff and clean extraction

Produce `V2/delivery/LAUTARA_3D_Art_Handoff_v2.zip` and a verified clean-room extraction report.

- [ ] Write the teammate `START_HERE.md` with the asset load order, stable paths, two import examples in plain terms, target/object axes, camera presets, water and section handling, and the intended roles for each site. Include final `HANDOFF.md`, attributions, scene and scripts `BUILD.md`, checks, resolved defects and limits. Bundled authoring scripts may have exact relative paths or include every small input they need for reproduction. No private paths or raster inputs with unconfirmed redistribution.
- [ ] Run `validate_v2.py` on the candidate package root. Reject unrecognized archive roots, traversal, external asset URIs, unexpectedly missing dependencies, bad checksums, stale v1 backups and accidental screenshot/audit artifacts. Stage only the contract payload. Include some images as visual evidence, with matching source and clean import comparisons.
- [ ] Run `build_handoff_v2.py` and extract into a separate fresh test directory outside the repo. Verify SHA-256 for every listed file and compare extracted names. Reopen all five primary editable scenes and import all eight GLBs from this independent copy. Check filenames with spaces if that matches the user's workstation. Confirm scene data, embedded textures, the manifest and final media don’t depend on the original working tree to open. Decode the extracted videos or verify their hashes match the full-decode-checked files.
- [ ] Follow the teammate START_HERE from that extracted copy and verify the described path and commands. Recheck the original baseline hash list. Promote the validated ZIP to its final path and only then mark the ledger completed. If a blocking acceptance item remains, preserve the tested partial without giving it the final-ready label and identify the minimal recovery.
- [ ] Return the user the exact ZIP path and an overview of improved assets, passed checks and limitations. The user can pass that one ZIP to the teammate.

**Gate.** A fresh archive extraction, actual opens/imports, verified content and documented handoff. The user’s 3D assignment can conclude at this point.

## Render timing and checkpoint request

Estimate the run from proof timings rather than a fixed target. Budget multiple hours for look, authoring, all-coast parity, high-resolution renders and full delivery verification. On a laptop GPU, try Eevee first and profile before branching renderer. Prioritize restoring a stable renderer rather than discarding one coast. Keep proof and final batches resumable. Use the recovery routine for time limits or interrupted background jobs.

Planning method used to structure the gates and testable phases. [Superpowers writing plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) · [Executing plans](https://github.com/obra/superpowers/blob/main/skills/executing-plans/SKILL.md)
