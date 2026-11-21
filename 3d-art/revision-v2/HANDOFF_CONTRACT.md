# Final v2 handoff contract

## Production paths and recipients

Resolve `V2` as `<repo-root>/3d-art/revision-v2`. Put new reusable builders under `V2/work/scripts/`. Put temporary material under `V2/work/runs/<run-id>/` with separate logs, checkpoints, proofs, renders and imports. Put the final package under `V2/delivery/`. Use repo-relative paths in source and package-relative paths in the teammate manifest. Preserve the original work and delivery directories. The extraction plan here is for the initial DSH ZIP. The layout below is for the distinct ZIP produced by DSH after production.

```text
V2/delivery/LAUTARA_3D_Art_Handoff_v2.zip
  LAUTARA_3D_Art_Handoff_v2/
    START_HERE.md
    HANDOFF.md
    ATTRIBUTION.md
    SHA256SUMS.txt
    runtime/
      asset-manifest.json
      globe/globe.glb
      kit/common-kit.glb
      coasts/{kodingareng,tunda,amur}/coast.glb
      coasts/{kodingareng,tunda,amur}/section.glb
    source/
      globe/globe.blend
      kit/common-kit.blend
      coasts/{kodingareng,tunda,amur}/scene.blend
      scripts/...
      BUILD.md
    media/
      globe/globe-overview.png
      kit/asset-sheet.png
      coasts/{kodingareng,tunda,amur}/{godview,mapview,approach,detail,section}.png
      coasts/{kodingareng,tunda,amur}/travel.mp4
      coast-reel.mp4
      pitch/{kodingareng-surface,kodingareng-deeper,kodingareng-section}.png
    evidence/depth-case-verified.json
    review/
      before-after.png
      parity-sheet.png
      runtime-parity.png
      review-report.md
      validation.json
```

## Exact required core inventory

| Asset family | Minimum expectation |
|---|---|
| Blender source | Five openable, packed primary scenes, one per site plus globe and kit. Each coast includes an editable travel rig, the A/B edit recipe or timeline, exact derived shot settings and keyframes. Three per-site review sections in `review/review-report.md` record the scene and export checks. If extra editable shot files are essential for the edit and cannot be regenerated, carry them under that coast’s source folder and record paths in the manifest. |
| Core GLB | Eight files, one globe, one kit, three coasts and three separate sections. glTF 2.0 binary files, embedded resources, no camera/light nodes. Do not require Draco, Meshopt, KTX2, or a custom decoder. Optional compressed exports are unnecessary for the first handoff. |
| Clean art | Fifteen 3840×2160 coast PNGs, one 3840×2160 globe PNG and one named kit sheet (minimum 1920×1080). Use stable views and filenames above. Case labels and numbers live in pitch media. |
| Motion | Three improved 6–8 second coast films and one 22–30 second combined reel. Default 7 s each at 24 fps/1080p for matching comparison, and 4 s Earth entrance plus 2 s end for a 27 s reel. H.264 MP4, yuv420p, even dimensions, progressive, stable cadence. Silent art exports. |
| Pitch and review | Three annotated 1920×1080 or larger Kodingareng plates, shared before/after, equal-scale all-site sheet, and source-to-import comparison. Validation records what was actually seen and tested. |
| Reproduction and integration | Exact version and reopen steps, named controls, runtime manifest, validation report, rebuild scripts or rates needed to regenerate the final outputs, provenance and hash list. Starter guidance should let a teammate load a coast even if they never open Blender. |

## Runtime identifiers and transforms

- Blender local coast frame is right-handed. Blender +X east, +Y north, +Z up. 1 unit is 1 metre for coast and props. Illustrative heights and section scale are recorded. Waterline is Blender Z=0. glTF coordinates use +X east, +Y up, −Z north. Map Blender vector `[x, y, z]` to glTF `[x, z, -y]`. Verify named, asymmetrical axis probes through actual import and apply the transform only once. A Blender re-import will reconstruct Blender axes. Compare in the correct frame.
- Each coast and its section share an identical origin and basis. Never independently centre the section, normalize object sizes, or apply a GLB-specific origin offset without declaring it. The default origin is art-local, and `georeferenced` is false. Globe has a normalized art radius. Keep that scale separate and document projection and orientation. Give `lat` then `lon` in degrees for locator metadata. Preserve globe north at +Y and verify its texture orientation after export.
- Require named empties `COAST_ORIGIN`, `ORBIT_SITE`, `ORBIT_WATERFRONT`, `TARGET_SURVEY`, `ANCHOR_JETTY`, `ANCHOR_VESSEL`, `SECTION_A`, and `SECTION_B` in each coast and section GLB. The plan and section use the same base A/B transforms. Record separate visible boat and jetty landmark positions if a shot duplicates or crops them. Use `ART_` for optional decorative stakes or scene markers. Keep the independent `ENV_Water` on each coast and `SECTION_Water` on each section. Keep section terrain and strata independently selectable. For a shared kit, stable names such as `KIT_BOAT_SURVEY` and sensible origins allow component reuse. Keep `ANCHOR_kodingareng`, `ANCHOR_tunda`, `ANCHOR_amur` for globe locators.
- More than one GLB can contain the same node name because each is a separate world or view variant. Within an asset, required IDs are exact and unique. Named empties must survive export as glTF nodes. A standalone section is a view asset that can be shown by replacing or hiding the coast. Avoid displaying overlapping terrain/water in both variants together. Derive section camera target and direction directly by orthogonal projection to A–B and explicitly record which side is visible.
- Camera presets live in JSON. Record glTF-space `position`, `target`, `up`, `near`, `far`, original `aspect`, `projection` and either `verticalFovDeg` or `orthoWidthM`. Compute vertical FOV and ortho width from actual renderer settings, preview dimensions and sensor fit. Convert width to height by its specified aspect. Match view within a documented tolerance at original aspect. Provide fit guidance for narrower containers. Keep separately positioned globe cameras in the globe preset group.
- A friendly initial budget per primary coast is ≤6 MiB and ≤200k triangles counted over rendered instances. Section ≤3 MiB and ≤125k triangles. Kit ≤4 MiB, globe ≤8 MiB. These are provisional web targets. Record any justified size increase and actual loading behaviour. Prefer instancing and clean material sharing, simplify land off camera and reduce texture size or draw calls before cutting semantic landmarks. Preserve an accessible core GLB. Report payload, mesh/node/material counts, instantiated triangles, textures and largest bounds in meters.

## Manifest fields

Use `schemaVersion: 1`, `revision: "v2"`, `baseCommit`, `buildId`, `blenderVersion`, `axisConvention`, `units`, `georeferenced`, `assets`, `sites`, `globe`, `kit` and `evidencePath` at the top level.

| Location | Required values |
|---|---|
| `assets[]` | Unique `id`, exact package-relative `path`, `kind`, `bytes`, `sha256`, and applicable mesh/triangle/material/texture/bounds summary. No absolute or parent-traversal paths. |
| `sites.<site>` | `coastAssetId`, `sectionAssetId`, `sourcePath`, `siteLocatorWgs84` object with `lat`/`lon` and role, `originGltf`, `waterlineUpM`, `waterNode`, `sectionWaterNode`, `anchorsGltf` keyed by exact node name, `cameras` keyed by preset, `section` and `artNotes`. |
| `sites.<site>.section` | `fromNode: "SECTION_A"`, `toNode: "SECTION_B"`, `lookDirectionGltf`, `verticalExaggeration`, `verticalPivotUpM`, `illustrative: true` and instructions to mutually exclude coast/section at runtime. |
| `globe` | `assetId`, `radiusArtUnits`, `markers` keyed by site with verified WGS84 locator and local node/position, `cameras`. |
| `kit` | `assetId`, `components` array of required exact node names, recommended pivots/origin rules. |
| `evidencePath` | `evidence/depth-case-verified.json`. Preserve the original verified fixture bytes. Keep source/proposal coordinates distinct in notes. |

Each validation item should include `id`, `state` (`pass`, `fail`, `blocked`, or `not-applicable`), `evidencePaths`, and `notes`. Store version strings and audit date. Record engine-neutral runtime validation as Blender clean import plus manifest checks. If the teammate loader is available locally and safe to use, also record a direct import check using that loader. Only claim the environments exercised.

Include exact start instructions, 30-second import steps, camera/origin table, texture and water override guidance, site comparison and what the engineer integrates next. Include Natural Earth attribution and provenance for all third-party inputs used, original art authorship and usage notes. Omit raw audit captures, source screenshot, tokenized logs, app code, personal paths, private runtime state, existing Git objects, frame sequences, caches, old work, unapproved assets and backup files.
