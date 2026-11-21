# The Ocean Has Floors — Blender Art Production Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` (native) or `subagent-driven-development` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This is an art-production run, not a code change: each task's "test" is an inspected image or an executed checker, never a claim.

**Goal:** Author, render, inspect and deliver 33 Blender artifacts — three equally polished stylized coastal worlds (Kodingareng Lompo, Pulau Tunda, Razdolnaya mouth/Amur Bay), a real-outline Earth, a shared asset kit, three travel films and one reel — passing `tools/check_delivery.py`.

**Architecture:** Seven sequential phases matching `3d-art/prompts/00-06`. Independent `.blend` per coast plus a separate globe scene keeps edit and render cost bounded on 8 GB VRAM. Blockout parity is proven across all three coasts *before* detail work begins, so no single site gets ahead. Every render is read back through the image-return channel before it counts.

**Tech Stack:** Blender 5.2.2 at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe` (headless for 4K and animation, MCP `execute_blender_code` for interactive edits), Blender MCP (`mcp__blender__*`), Python 3.14.4 for the delivery checker, ffmpeg for MP4 encoding.

**Spec:** `3d-art/DSH_START_PROMPT.md`, `3d-art/brief/*.md` (7 files), `3d-art/prompts/*.md` (7 phase prompts), `3d-art/brief/OUTPUT_CONTRACT.md` (authoritative file list).

## Decisions locked (2026-11-21)

- **Autonomy:** full autonomous run 00 → 06; interrupt the owner only on a hard blocker (no Blender/MCP, unrecoverable render failure, missing audit data that cannot be substituted).
- **Film:** full scope — 3 × `travel.mp4` plus `coast-reel.mp4`, animatics first, frame sequences resumable.
- **Renderer:** Eevee for all finals, plus **one contained Cycles/OptiX comparison** shot, documented; do not mix renderers across the three coasts.
- **Execution:** Native — this session executes every phase; one independent visual review pass at the end (phase 05 step 1 may dispatch a reviewer subagent).

## Global Constraints

- Blender **5.2.2**, RTX 4060 Laptop, **8 GB VRAM**; confirm actual version/devices before trusting any budget.
- Final stills **3840 × 2160** (10 required: globe overview + godview/mapview/section × 3 coasts).
- Films: **1920 × 1080**, **24 fps** target; reel target **22–30 s** (target, not an encoded requirement).
- Local units **metres**; **+X east, +Y north, +Z up**; water surface at **Z = 0**.
- Globe: radius **~10 Blender units**, **+Z north**, longitude **0° on +X**, **90° on +Y**; marker `R*(cos φ cos λ, cos φ sin λ, sin φ)`.
- Camera coverage: `GLOBE_HOME`, `GLOBE_REGION`, `COAST_OVERVIEW`, `COAST_PLAN`, `COAST_APPROACH`, `COAST_SECTION`, `COAST_DETAIL`.
- Empties per coast: `ORBIT_SITE`, `ORBIT_WATERFRONT`, `TARGET_SURVEY`; section axis **A** and **B** fixed empties.
- Geometry: start **under ~300k evaluated triangles** per local view; exceed only with a written reason.
- Textures: **1K** shared atlas for most parts, **2K** selectively for hero/coastline; globe image may be larger.
- All authored output lives under `3d-art/`; `cityrt-audit/` is **read-only**; no extracted CityRT meshes/shaders/code may be imported.
- Never clear the user's unsaved artist file. Work in a new saved scene under `3d-art/`.
- Do not describe a file as validated or visually reviewed if only its existence was checked.
- `check_delivery.py` must exit **0** with **33/33** artifacts.
- GPU: run final stills sequentially; do not stack 3 concurrent jobs on one laptop GPU.

## Review Focus

1. **The audit's real layout differs from the paths the briefs name.** The briefs expect `analysis/geometry/building-language.md`, `metrics.json`, `analysis/constants.json` and `evidence/styles/<id>/{overview,mid,street,night}.png`. None of those exist. What the audit actually has is richer in places and different in name: `docs/ART-BIBLE.md` (15 KB), `KIT-SPEC.md`, `STYLE-MATRIX.md`, `UNKNOWNS.md`, `COVERAGE.md`; `analysis/palette/*.json` (17 style palettes + `previews-summary.json`), `analysis/geometry/observations.md`, `analysis/rendering/{ink-pipeline,renderer-verdict}.md`, `analysis/styles/styles-static.json`, `analysis/catalog/{building-palettes,catalog-analysis,catalog-summary}.json`, `analysis/game/{art-systems,look-and-shaders,rendering-extract}.json` + 40 GLSL shaders, `analysis/simulation/observations.md`; `evidence/style-previews/*.webp` (14), `evidence/catalog/img/*.webp` (824), `evidence/manifest.json` (278 KB). A person expects "audit-backed" to mean a real file with a real path. **Every intake rule must cite an actual existing path**, and the intake must map assumed→actual. Tested in Task 1.
2. **4K on 8 GB VRAM with voluminous water.** Expect OOM or a silently empty render. A reasonable person expects a 3840×2160 PNG with real content. Tested in Task 6 (pixel dimensions read from the file, not the render property) and Task 5 (volume hidden fallback).
3. **Section cut integrity.** Z-fighting, loose Boolean faces, transparent sorting, boat drift or a water plane that moves break the deliverable's central idea. Tested in Tasks 5–6 (boat/land landmark masked pairs).
4. **GLB portability.** Cameras/lights leaking into exports, unpacked textures, axis or scale flips make an apparently complete delivery unusable. Tested in Task 7 (five re-imports in fresh scenes).
5. **Frames-vs-encode failure.** An interruption must not cost a whole film. Tested in Task 5 (resumable frame sequences; missing frames recorded, not hidden).

---

### Task 1: Preflight and audit intake (phase 00)

**Files:**
- Create: `3d-art/work/progress.json`, `3d-art/work/tooling.md`, `3d-art/work/evidence.md`, `3d-art/work/scripts/preflight_smoke.py`, `3d-art/work/checkpoints/00-preflight.blend`, `3d-art/work/renders/smoke.png`, `3d-art/output/review/audit-intake.md`

**Interfaces:**
- Produces: `progress.json` in the exact contract shape (keys `run_id`, `audit_root`, `production_root`, `audit_status`, `phase`, `last_completed_phase`, `site_status`, `last_scene_checkpoint`, `image_review_capability`, `evidence`, `blockers`, `next_action`); the confirmed **blender-executable path** and **MCP tool names** every later task reuses; the ≥6-rule style table.

- [ ] **Step 1: Discover tools and record them in `work/tooling.md`.** List the actual `mcp__blender__*` tool names and schemas, Blender version, GPU backend, engine list. Run `mcp__blender__get_scene_info`.
- [ ] **Step 2: Prove path parity.** Execute `print(bpy.data.filepath)` plus a write to `3d-art/work/renders/` from Blender, and confirm the harness sees the same file at the same absolute path.
- [ ] **Step 3: Smoke scene + image round-trip.** Build an asymmetric test (sloped block, ochre sphere, teal floor), save `00-preflight.blend`, render 960×540 to `work/renders/smoke.png`, then read the PNG back through the image channel and state **where the ochre sphere appears**. Expected: a visible describable position, not "rendered successfully".
- [ ] **Step 4: Write `output/review/audit-intake.md`.** Resolve the real audit root and record its version/date. Read, don't assume: `cityrt-audit/docs/ART-BIBLE.md`, `KIT-SPEC.md`, `STYLE-MATRIX.md`, `UNKNOWNS.md`, `COVERAGE.md`, `analysis/styles/styles-static.json`, `analysis/palette/` (+ `previews-summary.json`), `analysis/geometry/observations.md`, `analysis/rendering/renderer-verdict.md`, `analysis/catalog/catalog-analysis.json`, `analysis/game/art-systems.json`, `evidence/manifest.json`, and inspect a sample of `evidence/style-previews/*.webp` plus `evidence/catalog/img/*.webp`. Table with columns `Dimension | Evidence label | Observed reference / path / digest | Coastal production rule | Test`. Minimum six rows: camera, massing, light, palette, water/edges, motion. Label every row **observed / derived / design target / unavailable**. Include an explicit **assumed → actual path map** for the four brief-named inputs that do not exist (`analysis/geometry/building-language.md`, `metrics.json`, `analysis/constants.json`, `evidence/styles/<id>/`), and name the real substitute used for each. Pick one primary observed style family plus at most one measured secondary influence, justified by `STYLE-MATRIX.md` and a preview image actually viewed.
- [ ] **Step 5: Write `work/progress.json`** atomically (temp sibling + replace). `phase: "00"`, `image_review_capability` set to what step 3 actually proved.
- [ ] **Step 6: Verify.** Re-read `progress.json` (valid JSON, required keys), re-open `saved smoke.png` dimensions. Commit nothing outside `3d-art/`.

### Task 2: Reference boards and equal blockout (phase 01)

**Files:**
- Create: `3d-art/work/scripts/blockout_<site>.py`, `3d-art/work/checkpoints/01-blockout-{kodingareng,tunda,amur}.blend`, `3d-art/work/renders/blockout/<site>_{overview,map,section,lateral}.png`, `3d-art/work/reviews/blockout-parity.png`, `3d-art/work/blockout-evidence.md`

**Interfaces:**
- Consumes: audit-intake rules + `references/places/*.md` + `references/cityrt/*.png`.
- Produces: three blockout `.blend` files with shared camera convention and stable object/collection IDs (`SITE_ORIGIN`, `ORBIT_SITE`, `ORBIT_WATERFRONT`, `TARGET_SURVEY`, `SECTION_A`, `SECTION_B`); the parity sheet the owner steers at.

- [ ] **Step 1: Per-place evidence table** in `work/blockout-evidence.md`: source file, one visible feature it supports, what is being simplified. Three places, ≥2 features each.
- [ ] **Step 2: Block out all three coasts** — silhouette, terrain/broad neighborhoods, water plane, jetty or bank, survey anchor. Topology beyond the frame for orbit/approach. Same camera convention per coast.
- [ ] **Step 3: Block out the section** per coast aligned to the same anchor; two test viewpoints against fixed world coordinates; seabed clearly illustrative.
- [ ] **Step 4: Seed the globe** from `references/globe/` (texture or `make_globe_seed.py`); verify north/east and the three anchors against the usage doc; two regional framing tests.
- [ ] **Step 5: Render clay proofs** (960×540) for overview + section on **all three** coasts; assemble `work/reviews/blockout-parity.png` with labels at equal sizes.
- [ ] **Step 6: Verify at 320 px.** Name, for each coast, its distinct shape, shore anchor and boat. If any two read as duplicates or a hard-edged cropped tile, fix the blockout and re-render before proceeding.
- [ ] **Step 7: Save checkpoints, update `progress.json`, record camera/anchor notes.**

### Task 3: Asset kit and look development (phase 02)

**Files:**
- Create: `3d-art/work/scripts/build_kit.py`, `3d-art/work/checkpoints/02-kit.blend`, `3d-art/work/reviews/lookdev-{kodingareng,tunda,amur}.png`, `3d-art/work/lookdev-log.md`

**Interfaces:**
- Produces: a shared kit collection set (roof/wall modules, shore edge, jetty/approach, rocks, vegetation, survey boat, sampling hardware, mooring/markers) with `KIT_` prefixes and documented pivots; one shared light rig `LGT_Sun_Key` + `LGT_Sky_Fill`; a named material set `MAT_<Family>_<Variant>`; the committed look recipe.

- [ ] **Step 1: Build the kit** silhouette-first: roof/wall modular components, shore edge pieces, jetty/approach, rocks, vegetation clusters, survey boat, sampling hardware, mooring/markers. Variants only where place evidence warrants.
- [ ] **Step 2: Define the shared daylight rig** (elevated key 35–50°, diagonal shadow direction, sky fill, controlled contact shadows in Eevee) and material family with original palette derived from the intake.
- [ ] **Step 3: Render three comparable material/lighting proofs** beside the relevant reference crops; log observed rule → output → translation in `lookdev-log.md`.
- [ ] **Step 4: Asset QA each kit object** — pivot, faces, normals, UVs, material IDs; render-only embellishments isolated in their own collection.
- [ ] **Step 5: Commit to one look recipe** after comparing three equally strong samples; note that changing the rig later forces re-evaluation of all three coasts.
- [ ] **Step 6: Verify.** Re-open the kit checkpoint; confirm every kit object is named, pivoted and material-assigned; probe report in `lookdev-log.md`. Update `progress.json`.

### Task 4: Finish all three coasts (phase 03)

**Files:**
- Modify: `3d-art/work/checkpoints/01-blockout-<site>.blend` → `03-coast-<site>.blend`
- Create: `3d-art/work/renders/coast/<site>_{overview,plan,approach,detail}.png`, `3d-art/work/reviews/before/<site>.png`, `3d-art/work/renders/after/<site>.png`, `3d-art/work/coast-notes.md`

**Interfaces:**
- Consumes: kit assets, look recipe, blockout anchors.
- Produces: three finished scenes with separated collections — `ENV_Land`, `ENV_Water`, `ENV_Bed`, `BLD_*`, `PROP_*`, `GUIDE_*` (art-only), and an explicit export allowlist.

- [ ] **Step 1: Finish ground/shoreline** per coast: seams, transitions, build-out beyond default frame. Kodingareng and Tunda must reflect the correct island; Amur emphasises the broad river entrance and low banks.
- [ ] **Step 2: Place the survey boat/waterfront anchor** in all three; reality-check scale and shadow at mid-distance. Preserve world positions and waterline across overhead/section variants.
- [ ] **Step 3: Separate collections** (water / bottom / land / buildings / lights / guides / export allowlist); verify the section truly cuts the same scene.
- [ ] **Step 4: Curate composition** — shore-to-water read at high oblique, legible north-up plan, mid range with parallax, no obvious foreground repetition. Moderate glare and shadow contrast.
- [ ] **Step 5: Render 960–1440 px proofs** at framing extremes; inspect all three at like sizes for boat scale, continuity, palette family, open water, landmark identity.
- [ ] **Step 6: Fix ≥1 visible flaw per coast**, record before/after paths in `coast-notes.md`; rebuild proofs.
- [ ] **Step 7: Verify** all three at equivalent finish; save `03-coast-*` checkpoints; update `progress.json`.

### Task 5: Earth, travel and cutaways (phase 04)

**Files:**
- Create: `3d-art/work/scripts/globe_build.py`, `3d-art/work/scripts/travel_animatic.py`, `3d-art/work/checkpoints/04-globe.blend`, `3d-art/work/checkpoints/04-coast-<site>.blend` (camera presets and markers added to the 03 coast scenes and saved as these), `3d-art/work/renders/animatic/<site>/frames_####.png`, `3d-art/work/reviews/filmstrip-<site>.png`

**Interfaces:**
- Produces: `globe.blend` with `GLOBE_HOME` / `GLOBE_REGION` and three markers; per coast the five camera presets, `COAST_*` datablocks, timeline markers for globe region moves; animatic frame sequences whose paths Task 6's final render reuses.

- [ ] **Step 1: Finish the Earth scene** — physically lit sphere, readable outline, space around it, verified continent orientation, three geographic anchors, original simple markers. Frame Indonesia and Primorye by globe rotation; record texture source and anchor placement.
- [ ] **Step 2: Verify globe orientation** against four checks (northern hemisphere point, Indonesian point south of equator, eastern longitude marker, texture vs geometry).
- [ ] **Step 3: Save camera presets + marker/empty set** in every coast scene: overview, plan, approach, section, detail; plus a usable opening viewport view.
- [ ] **Step 4: Animatic at 540p first** for each coast flight (5–8 s: wider context → god's-eye → deliberate move/match cut to section). Render start/middle/end film strips.
- [ ] **Step 5: Inspect and revise** camera acceleration, orientation, parallax, framing. Pitfall check: fixed water surface, no geometry pop, no unintended boat drift between variants, no clipping through foreground.
- [ ] **Step 6: Verify** the globe cut and coast shots align in heading/placement; render frames, not video, so an interruption only costs unfinished frames. Update `progress.json`.

### Task 6: Critique and final 4K renders (phase 05)

**Files:**
- Create: `3d-art/output/globe/globe-overview.png`, `3d-art/output/coasts/<site>/{godview,mapview,section}.png`, `3d-art/output/kit/asset-sheet.png`, `3d-art/output/review/parity-sheet.png`, `3d-art/output/coasts/<site>/review.md`
- Modify: scenes after revision passes

**Interfaces:**
- Consumes: finished scenes, camera presets, kit.
- Produces: all ten 4K stills at **3840×2160** verified from file bytes; the parity sheet; per-site `review.md`.

- [ ] **Step 1: First review — screen-size read.** Equal-width thumbnails; identify where each coast starts, where the boat is, what differs, where the camera can travel. Inspect 4K cutaways for continuity. Score all sites on one criteria set; name specific defects and actions.
- [ ] **Step 2: Revise highest-impact mismatches** on each site; re-render affected comparable views.
- [ ] **Step 3: Second review — production read.** Seams, clutter, lost anchors, noisy water, repetitive planting, roof tiling, scale, cutaway edges, lighting balance, motion path. Keep full-size crops where a flaw disappears at contact-sheet scale.
- [ ] **Step 4: Render all ten 4K stills** in Eevee; render the kit asset sheet; assemble final parity sheet. Also render **one contained Cycles/OptiX comparison** at 1920×1080 on the strongest coast, and record engine, device, samples, time and memory in `coast-notes.md`. Do **not** switch any final still to Cycles.
- [ ] **Step 5: Verify pixels** — read each PNG's real dimensions (not the Blender setting), confirm 3840×2160 and non-empty content; write per-site `review.md` (continuity checks, measured settings, inspection method, one visible defect + correction, remaining limits).
- [ ] **Step 6: Check investment parity** — no coast may look like a rough draft relative to the others. Update `progress.json`.

### Task 7: Export, re-import and deliver (phase 06)

**Files:**
- Create: `3d-art/output/globe/{globe.blend,globe.glb}`, `3d-art/output/coasts/<site>/{scene.blend,coast.glb,travel.mp4}`, `3d-art/output/kit/{common-kit.blend,common-kit.glb}`, `3d-art/output/coast-reel.mp4`, `3d-art/output/review/{export-check.md,handoff.md,deviations.md}`

**Interfaces:**
- Consumes: everything above.
- Produces: the 33-file delivery, `check_delivery.py` exit 0, and the handoff.

- [ ] **Step 1: Promote editable scenes** with packed images, named collections, explicit export selection; exclude cameras, lights, guides and reference art from GLBs.
- [ ] **Step 2: Export five GLBs** (globe, 3 coasts, kit) with embedded resources and a portable water material.
- [ ] **Step 3: Re-import all five GLBs** into fresh temporary scenes; compare bounds, orientation, scale, water material, object separation, texture warnings. Record axes/dimensions per model.
- [ ] **Step 4: Encode films** — `travel.mp4` per coast and `coast-reel.mp4` from resumable frame sequences with ffmpeg (H.264/MP4, 24 fps, 1920×1080); verify duration, fps, dimensions, and check for black frames.
- [ ] **Step 5: Run the checker:** `python 3d-art/tools/check_delivery.py 3d-art/output`. Expected: exit **0**, report **33/33**. Read every error before reporting completion.
- [ ] **Step 6: Write** `export-check.md` (all five re-imports + axes/dimensions + texture/material checks + water behaviour + proof paths), `deviations.md` (attempted fixes and achieved outputs), `handoff.md` (preview order, orbit instructions, camera names, anchors, attribution, GLB limits, audit state, deviations).
- [ ] **Step 7: Final verify.** `progress.json` accurate, `phase: "06"`, `last_completed_phase: "06"`. Report exact paths.

---

## Execution notes

- Each phase writes a durable checkpoint before destructive geometry changes; never let a final file be its own working copy.
- Render one job at a time on the 4060; use the saved `.blend` with the verified `blender.exe` for 4K and animation.
- If a capability is missing, record the exact gap in `progress.json.blockers`, continue any independent task, and do not relabel unfinished work as passed.
