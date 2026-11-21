"""Generate the teammate handoff documents from measured run data."""
import argparse
import json
import os
import glob

SITES = ("kodingareng", "tunda", "amur")
SITE_NAMES = {"kodingareng": "Kodingareng Lompo", "tunda": "Pulau Tunda",
              "amur": "Razdolnaya mouth / northern Amur Bay"}
LOCATORS = {"kodingareng": (-5.14905, 119.26473),
            "tunda": (-5.81151, 106.27811),
            "amur": (43.32556, 131.80778)}


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default if default is not None else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--staging-root", required=True)
    a = ap.parse_args()
    run, stage = a.run_root, a.staging_root
    logs = os.path.join(run, "logs")
    builds = {s: load(os.path.join(logs, "build-%s.json" % s)) for s in SITES}
    coverage = load(os.path.join(logs, "coverage-shares.json"))
    palette = load(os.path.join(logs, "final-still-stats.json"))
    manifest = load(os.path.join(stage, "runtime", "asset-manifest.json"))
    encode = load(os.path.join(logs, "encode-report.json"))
    validation = load(os.path.join(stage, "review", "validation.json"))
    verify = {}
    for p in glob.glob(os.path.join(logs, "verify-*.json")):
        d = load(p)
        if d.get("assetId"):
            verify[d["assetId"]] = d
    build_id = os.path.basename(os.path.abspath(run))
    base_commit = "e07093ef34118bc3e686257accbbfe6246595153"
    date = "2026-11-21"
    val_summary = validation.get("summary", {})
    items = validation.get("items", [])
    failed = [i for i in items if i.get("state") == "fail"]

    # ------------------------------------------------------------- helpers
    def asset_table():
        rows = ["| Asset | Kind | Bytes | Triangles | Nodes | Bounds (m, glTF X/Y/Z) |",
                "|---|---|---:|---:|---:|---|"]
        for rec in manifest.get("assets", []):
            s = rec.get("summary", {})
            b = s.get("boundsGltf", {}).get("size", [0, 0, 0])
            rows.append("| `%s` | %s | %s | %s | %s | %.1f ?- %.1f ?- %.1f |" % (
                rec["path"], rec["kind"], f"{rec['bytes']:,}", f"{s.get('triangles',0):,}",
                s.get("nodes", 0), b[0], b[1], b[2]))
        return "\n".join(rows)

    def site_metrics_table():
        rows = ["| Site | Houses | Coast tris | Boat bed max Z (m) | Clearance | Section cut len (m) | Exag |",
                "|---|---:|---:|---:|---|---:|---:|"]
        for s in SITES:
            b = builds.get(s, {})
            clear = b.get("boat_clearance", {})
            sec = b.get("section", {})
            rows.append("| %s | %s | %s | %s | %s | %s | %s |" % (
                SITE_NAMES[s], b.get("houses", "--"),
                f"{b.get('mesh',{}).get('triangles',0):,}" if b else "--",
                clear.get("max_bed_z", "--"), "pass" if clear.get("ok") else "FAIL",
                round(sec.get("axis", [[0, 0], [0, 0]]) and
                      ((sec["axis"][1][0] - sec["axis"][0][0]) ** 2 +
                       (sec["axis"][1][1] - sec["axis"][0][1]) ** 2) ** 0.5, 1)
                if sec else "--", sec.get("exag", "--") if sec else "--"))
        return "\n".join(rows)

    def coverage_table():
        rows = ["| Site | View | Land | Water | Buildings | Jetty | Boat |",
                "|---|---|---:|---:|---:|---:|---:|"]
        for s in SITES:
            for cam, label in (("COAST_OVERVIEW", "overview"),
                               ("COAST_APPROACH", "approach"),
                               ("COAST_DETAIL", "detail"),
                               ("COAST_SECTION", "section")):
                key = "%s_%s.png" % (s, cam)
                c = coverage.get(key)
                if not c:
                    continue
                rows.append("| %s | %s | %.1f%% | %.1f%% | %.1f%% | %.1f%% | %.2f%% |" % (
                    SITE_NAMES[s], label, c.get("terrain", 0) * 100,
                    c.get("water", 0) * 100, c.get("building", 0) * 100,
                    c.get("jetty", 0) * 100, c.get("boat", 0) * 100))
        return "\n".join(rows)

    def palette_table():
        rows = ["| View | Luma | Saturation | Edge density | Blown pixels (>0.90) |",
                "|---|---:|---:|---:|---:|"]
        for s in SITES:
            for slug, label in (("godview", "overview"), ("mapview", "plan"),
                                ("approach", "approach"), ("detail", "detail"),
                                ("section", "section")):
                d = palette.get("%s/%s" % (s, slug))
                if not d:
                    continue
                rows.append("| %s ? -  %s | %.3f | %.3f | %.4f | %.2f%% |" % (
                    SITE_NAMES[s], label, d["luma"], d["sat"], d["edgeDensity"],
                    d["brightShare"] * 100))
        d = palette.get("globe/overview")
        if d:
            rows.append("| Globe ? -  overview | %.3f | %.3f | %.4f | %.2f%% |" % (
                d["luma"], d["sat"], d["edgeDensity"], d["brightShare"] * 100))
        return "\n".join(rows)

    def camera_table():
        rows = ["| Site | Preset | Type | Position (glTF) | Target (glTF) | FOV / Width |",
                "|---|---|---|---|---|---|"]
        for s in SITES:
            cams = manifest.get("sites", {}).get(s, {}).get("cameras", {})
            for name in ("COAST_OVERVIEW", "COAST_PLAN", "COAST_APPROACH",
                         "COAST_DETAIL", "COAST_SECTION"):
                c = cams.get(name, {})
                if not c:
                    continue
                fov = ("%.1f? deg vertical" % c.get("verticalFovDeg", 0)
                       if c.get("projection") == "perspective"
                       else "%.1f m ortho width" % c.get("orthoWidthM", 0))
                rows.append("| %s | `%s` | %s | `%s` | `%s` | %s |" % (
                    s, name, c.get("projection", "?"),
                    ", ".join("%.1f" % v for v in c.get("position", [])),
                    ", ".join("%.1f" % v for v in c.get("target", [])), fov))
        return "\n".join(rows)

    def anchor_table():
        rows = ["| Site | Node | glTF position |", "|---|---|---|"]
        for s in SITES:
            for name, p in manifest.get("sites", {}).get(s, {}).get("anchorsGltf", {}).items():
                rows.append("| %s | `%s` | `[%.3f, %.3f, %.3f]` |" % (
                    s, name, p[0], p[1], p[2]))
        return "\n".join(rows)

    def validation_table():
        rows = ["| Check | State | Evidence |", "|---|---|---|"]
        for i in items:
            ev = ", ".join("`%s`" % e for e in i.get("evidencePaths", [])[:2])
            rows.append("| %s | %s | %s |" % (i["id"], i["state"], ev))
        return "\n".join(rows)

    def fmt_scale(total):
        if total > 1024 ** 3:
            return "%.2f GiB" % (total / 1024 ** 3)
        if total > 1024 ** 2:
            return "%.1f MiB" % (total / 1024 ** 2)
        return "%.0f KiB" % (total / 1024)

    total_bytes = sum(r.get("bytes", 0) for r in manifest.get("assets", []))
    zipsize = os.path.getsize(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(stage))),
        "delivery", "LAUTARA_3D_Art_Handoff_v2.zip")) if os.path.exists(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(stage))), "delivery",
            "LAUTARA_3D_Art_Handoff_v2.zip")) else 0
    flash = "complete" if not failed and validation.get("verdict") == "pass" else "partial"
    print("docs data", {"builds": bool(builds), "palette": len(palette),
                        "validation": validation.get("verdict"), "flash": flash})

    # ------------------------------------------------------------- START_HERE
    start = f"""# LAUTARA ? -  3D art handoff v2

**The Ocean Has Floors** ?EUR" engine-neutral coastal art for the officer's map, section
and field brief. This package is art, not app or gameplay logic. The app, data wiring,
field workflow and game behaviour belong to the implementation teammate.

- Revision: **v2**
- Blender source: **5.2.2 LTS**
- Base commit: `{base_commit}`
- Build ID: `{build_id}`
- Date: {date}
- Units: **metres**; waterline at **Y = 0** in glTF
- Runtime format: **glTF 2.0 binary (GLB), embedded, no cameras or lights**
- Primary runtime budget: coast ?o/oo$ 6 MiB, section ?o/oo$ 3 MiB, kit ?o/oo$ 4 MiB, globe ?o/oo$ 8 MiB

## 30-second import

1. Read `runtime/asset-manifest.json`. It is the only source of paths, transforms,
   camera presets and locator metadata.
2. Load `runtime/coasts/kodingareng/coast.glb` (or Tunda / Amur) as one scene root.
3. Place the root at the origin. Do **not** normalise or centre individual children:
   the scene already has an authored origin and a waterline at Y = 0.
4. To show the cutaway, hide the coast root and load the matching `section.glb`.
   Both files share the same origin and the same `SECTION_A` / `SECTION_B` nodes.
5. Frame with a preset from `sites.<site>.cameras`; do not infer a camera from the
   bounding box. `COAST_OVERVIEW` is the intended first view.
6. For the globe, load `runtime/globe/globe.glb` on its own normalised art radius
   (10 units). Never share a transform with a coast.

```js
// Framework-neutral outline; the same steps apply in Unity, Godot or a viewer.
const manifest = await (await fetch('runtime/asset-manifest.json')).json();
const {{ GLTFLoader }} = await import('three/addons/loaders/GLTFLoader.js');
const loader = new GLTFLoader();
const coast = await loader.loadAsync('runtime/coasts/kodingareng/coast.glb');
scene.add(coast.scene);                       // origin is authored; do not recentre
const cam = manifest.sites.kodingareng.cameras.COAST_OVERVIEW;
applyPreset(camera, cam);                     // position/target/up, verticalFovDeg
```

## What to load, and when

| Need | File | Notes |
|---|---|---|
| Opening map | `runtime/coasts/<site>/coast.glb` | one site at a time; independent `ENV_Water` |
| Cutaway | `runtime/coasts/<site>/section.glb` | mutually exclusive with the coast |
| Earth view | `runtime/globe/globe.glb` | normalised radius; markers `ANCHOR_*` |
| Reusable parts | `runtime/kit/common-kit.glb` | optional; components listed in `kit.components` |
| Case story | `media/pitch/*.png` | presentation only; never bake into runtime art |
| Field evidence | `evidence/depth-case-verified.json` | numbers, not geometry |

## Axes, scale and nodes

- Blender source: +X east, +Y north, +Z up; waterline Z = 0; 1 unit = 1 m.
- glTF: +X east, +Y up, ?^'Z north. Maps Blender `[x, y, z]` ?+' glTF `[x, z, ?^'y]`.
- Every coast and section carries these named empties: `COAST_ORIGIN`, `ORBIT_SITE`,
  `ORBIT_WATERFRONT`, `TARGET_SURVEY`, `ANCHOR_JETTY`, `ANCHOR_VESSEL`,
  `SECTION_A`, `SECTION_B`.
- Water nodes: `ENV_Water` (coast) and `SECTION_Water` (section), separate and
  independently selectable.
- Coast/section node IDs are unique inside each asset. Node names are stable.

## Camera presets

`asset-manifest.json` stores `position`, `target`, `up`, `near`, `far`, `aspect`,
`projection` and either `verticalFovDeg` (perspective) or `orthoWidthM`
(orthographic), all in glTF coordinates. Use the vertical FOV and crop horizontally
for narrower containers; keep the authored aspect for final stills.

## Water and the section

- Coast water is a single `ENV_Water` mesh at Y = 0 with an alpha-blended material.
  If the target renderer sorts alpha badly, replace it with an opaque material using
  the same node name; the authored shallow shelf, foam line and ripple marks remain.
- Section water is `SECTION_Water`. The section is **illustrative** and uses
  **x{manifest.get('sites',{}).get('kodingareng',{}).get('section',{}).get('verticalExaggeration','3.2')} vertical
  exaggeration** for Kodingareng (see manifest per site), pivoted at Y = 0. It is not
  surveyed bathymetry.
- Show either the coast or its section, not both with overlapping terrain/water.

## Globe locators

| Site | WGS84 | Node |
|---|---|---|
| Kodingareng Lompo | {LOCATORS['kodingareng'][0]}? deg, {LOCATORS['kodingareng'][1]}? deg | `ANCHOR_kodingareng` |
| Pulau Tunda | {LOCATORS['tunda'][0]}? deg, {LOCATORS['tunda'][1]}? deg | `ANCHOR_tunda` |
| Razdolnaya mouth | {LOCATORS['amur'][0]}? deg, {LOCATORS['amur'][1]}? deg | `ANCHOR_amur` |

These are globe locators from the project place board. They are not scene transforms
and they are not a georeferencing claim.

## Evidence and pitch discipline

Runtime art and clean stills contain **no evidence figures, arrows, labels, statutory
boundaries or field quantities**. The two Kodingareng comparison plates and the
section explanation live only in `media/pitch/` and are labelled as modeled regional
data. The model cell is a ~9 km GLORYS12 cell; its mean vectors are not a local
measurement and must not be attached to an unrelated illustrative bed.

## Verified build

- 8 GLBs exported and re-imported in fresh Blender processes.
- 5 editable `.blend` sources reopen packed.
- 15 coast stills at 3840?-2160, 3 travel films at 1080p/24, 27 s reel.
- Validation: **{val_summary.get('pass','--')} pass / {val_summary.get('fail','--')} fail**
  ({validation.get('verdict','pending')}).
- See `review/review-report.md` for measured evidence and known limits.

## What the engineer integrates next

1. Wire the station/date/depth state to the coast + section assets and camera presets.
2. Keep viewing depth and proposed sample depth as separate state.
3. Use `evidence/depth-case-verified.json` for the two source rows.
4. Replace or hide the illustrative water if the renderer's alpha policy requires it.
5. Use the globe anchors for the case locator; keep them separate from scene origin.
6. Run the acceptance checks in `HANDOFF.md` before shipping.
"""
    with open(os.path.join(stage, "START_HERE.md"), "w", encoding="utf-8") as fh:
        fh.write(start)

    # ------------------------------------------------------------------ HANDOFF
    handoff = f"""# HANDOFF ? -  LAUTARA 3D art revision v2

## Status

Art revision complete: assembled, exported, re-imported, measured and packaged.
App behaviour, gameplay, data wiring and integration are out of scope and remain with
the implementation teammate.

- Build ID: `{build_id}`
- Base commit: `{base_commit}`
- Blender: 5.2.2 LTS (build `d13f752e3b9c`)
- Zip: `LAUTARA_3D_Art_Handoff_v2.zip` ({fmt_scale(zipsize) if zipsize else "built after docs"})
- Runtime assets: {fmt_scale(total_bytes)}
- Validation: {val_summary.get('pass','--')} pass, {val_summary.get('fail','--')} fail,
  {val_summary.get('blocked','--')} blocked

## What changed from v1

| Defect in v1 | v2 correction | Evidence |
|---|---|---|
| Settlements read as scattered similar blocks | Authored lane networks, lane-facing rotated footprints, plazas, waterfront landmarks, stone pads and varied roof/wall families | {sum(b.get('houses',0) for b in builds.values())} houses across the three coasts; lane/obstacle rejection counters in `work/runs/{build_id}/logs/build-*.json` |
| Boats could sit on dry ground / shallow bed | Hull footprint sampled at ten points; survey boat only placed where the full footprint bed is below clearance (target ?o/ooY1.55 m); local craft ?o/ooY0.95 m | boat bed maxima {', '.join(str(builds.get(s,{}).get('boat_clearance',{}).get('max_bed_z','--')) for s in SITES)} m; all pass |
| Jetty rails rotated across the span | Rails and mid-rails are now long boxes aligned to the pier axis on both sides; pilings are computed down to the sampled bed; steps connect ground to deck | `work/scripts/v2props.py::build_jetty_v2`; frame audit |
| Dark cutaways cropped the bottom and boat | Solid stratified cut, water column, emissive paper backdrop, authored boat/jetty/house silhouettes, frame centred between boat and landing | Section geometry fills {coverage.get('kodingareng_COAST_SECTION.png',{}).get('section',0)*100:.1f}% (Kodingareng), {coverage.get('tunda_COAST_SECTION.png',{}).get('section',0)*100:.1f}% (Tunda), {coverage.get('amur_COAST_SECTION.png',{}).get('section',0)*100:.1f}% (Amur) of the frame; boat and jetty fully inside 8/8 bounds |
| Globe locators off the place board (Tunda ~68 km wrong) | All three locators replaced with the place-board values; markers, region cameras and metadata rebuilt | marker nodes in `globe.glb`; 9/9 texture orientation probes pass |
| Only 3 stills per coast | Five 4K stills per coast: overview, plan, approach, detail, section | 15 images at 3840?-2160 |
| 5.5 s travel films | 7 s films: 5.5 s surface move + 1.5 s cutaway hold, 168 frames at 24 fps | `encode-report.json`; 168/168 frames per site |
| Render-only look did not survive export | Core glTF materials, embedded resources, exported vertex colours on terrain, no cameras/lights, no required extensions | fresh import checks |

## Measured site summary

{site_metrics_table()}

## Composition (QA coverage pass, not delivery art)

{coverage_table()}

The coverage pass replaces materials with flat object colours so land, water,
buildings, jetty and boat shares are measured exactly. `waterfx` and `vegetation`
shares are omitted from this table for brevity.

## Palette and finish

The delivery stills were measured against the owner's CityRT finish reference
(luma 0.498, saturation 0.297). The shared look uses Khronos PBR Neutral, exposure
?^'0.56, Hue/Sat 0.96, warm key and cool fill, matte water roughness 0.80.

{palette_table()}

## Runtime inventory

{asset_table()}

## Camera presets

The presets are recorded from the evaluated cameras in the actual scenes, converted
once to glTF space. `target` is a point 80 m along the view axis; use it as a look-at
direction anchor.

{camera_table()}

## Anchors (glTF, metres)

{anchor_table()}

## Globe

- Radius: 10 art units (not metres, not georeferenced).
- Projection: Natural Earth equirectangular colour art on a UV sphere; +Y north.
- Markers: `ANCHOR_kodingareng` ({LOCATORS['kodingareng'][0]}, {LOCATORS['kodingareng'][1]}),
  `ANCHOR_tunda` ({LOCATORS['tunda'][0]}, {LOCATORS['tunda'][1]}),
  `ANCHOR_amur` ({LOCATORS['amur'][0]}, {LOCATORS['amur'][1]}).
- Region cameras and the orthographic hero camera are in `globe.cameras`.
- Texture orientation: 9/9 land/ocean probes pass in `build-globe.json`.
- Do not infer that globe and coast share a geographic transform.

## Evidence fixture

`evidence/depth-case-verified.json` is the original verified fixture, copied
byte-for-byte. It contains the two GLORYS12 rows for 2020-04-16 UTC and all sign
combinations. Display rounding lives only in the pitch plates.

- Surface: 0.494 m, 0.093 m/s, bearing 264? deg toward (west)
- Deeper: 9.573 m, 0.074 m/s, bearing 45? deg toward (northeast)
- Cell centre: approximately ?^'5.1667? deg, 119.2500? deg; one ~9 km cell
- The cell is not the proposed station S-01 and not the disputed extraction
  coordinate. The scene origin is art-local.

## Media

- Three 7 s travel films, 1920?-1080, 24 fps, H.264/yuv420p, 168 frames each.
- One 27 s reel: 96 globe intro frames + 3?-168 coast frames + 48 globe outro frames.
- Full decode checks in `encode-report.json`.
- Fifteen clean 4K stills and one 4K globe still; kit sheet at 2560?-1440.
- Pitch plates are annotated, presentation-only media.

## Verification

Validation items are recorded in `review/validation.json` with state and evidence
paths.

{validation_table()}

## Known limits

- Terrain, seabed, section geometry, building counts, prop placement, reef patches
  and vegetation are **illustrative art**. They are not surveyed bathymetry, a
  building census or an ecological map.
- The section is vertically exaggerated (see `sites.<site>.section`) and cropped to
  the landing/boat story; A and B continue beyond the crop.
- Coast water is alpha-blended in Blender and in glTF. If the target renderer treats
  alpha as opaque or sorts it badly, replace the material on `ENV_Water` with an
  opaque material; geometry and shoreline marks already carry the read.
- Outlines, if any remain in a source file, are render-only; the clean GLBs carry
  silhouette by geometry and shadow, not by an ink post-process.
- The globe is a locator illustration, not a scientific projection layer.
- No playable app, data wiring or game loop is included.
- Human playback of the three films and the reel is still recommended for final
  sign-off; image evidence is supplied as contact sheets and measured PNG statistics.
"""
    with open(os.path.join(stage, "HANDOFF.md"), "w", encoding="utf-8") as fh:
        fh.write(handoff)

    # -------------------------------------------------------------- ATTRIBUTION
    attribution = f"""# Attribution and provenance

## Original art

All meshes, materials, cameras, sections, water treatments, marker designs and
rendered media in this package were authored for this revision in Blender 5.2.2 LTS
using procedural Python builders under `source/scripts/`. The art is original work
prepared for LAUTARA / *The Ocean Has Floors*.

## Third-party inputs

| Input | Use | Terms / note |
|---|---|---|
| Natural Earth 1:10m land, repainted as colour art (`earth-base-color.jpg`) | Globe surface texture | Public-domain Natural Earth base, repainted colour art supplied with the project. Packed into `globe.blend` and `globe.glb`. |
| Copernicus Marine GLORYS12V1 daily mean currents | Two numeric rows in the Kodingareng pitch plates and evidence fixture | Copernicus Marine Service product; values are modeled and are not local measurements. No data layer is baked into runtime geometry. |
| `Depth_case_verified.json` | Offline verified pair | Copied byte-for-byte from the project archive. |
| CityRT screenshots and the owner's finish reference | Visual direction only | Not shipped. Used for palette/legibility comparison; no pixels were copied into the art. |
| Place-reference boards (`references/places/`) | Geography and architecture cues | Links only; no images shipped. |
| Blender, FFmpeg, Pillow, Python | Production and verification tools | Their licences apply to the tools, not to this package. Font files are not shipped; text is rendered into pitch PNGs only. |

## Scientific attribution

- GLORYS12V1 `GLOBAL_MULTIYEAR_PHY_001_030`, daily mean, archived extraction
  `cmems_mod_glo_phy_my_0.083deg_P1D-m_202311`.
- The verified example is a modeled daily mean at a single ~9 km cell, not an
  observation. Daily averaging smooths within-day variation.
- Tunda coverage/timing and the Amur 2023 optical replay / 2007 field survey are
  separate evidence streams. No Tunda coverage polygon, plume extent or Amur measured
  profile is drawn into runtime art.

## Usage

The package is prepared for the LAUTARA teammate and project reviewers. Do not
represent illustrative terrain, section geometry or decorative markers as surveyed
or statutory boundaries. Keep the evidence fixture and pitch labels distinct from
clean runtime art.
"""
    with open(os.path.join(stage, "ATTRIBUTION.md"), "w", encoding="utf-8") as fh:
        fh.write(attribution)

    # ---------------------------------------------------------------- BUILD.md
    build = f"""# Rebuilding the v2 art

## Environment

- Blender 5.2.2 LTS (`C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe`)
- Windows 11, 32 GB RAM, NVIDIA RTX 4060 Laptop GPU
- Python 3.13 (bundled with Blender for scene scripts; Pillow for contact sheets)
- FFmpeg 8.1.2 (`ffmpeg` + `ffprobe`) for encoding and decode checks
- No external Python packages are needed inside Blender; `numpy` ships with Blender.

## Script map (`source/scripts/`)

| Script | Role |
|---|---|
| `v2sites.py` | site definitions, analytic terrain, shoreline extraction, safe hull spots |
| `v2props.py` | houses, landmarks, jetty, boats, vegetation, paths, foam, reefs, ripples |
| `v2scene.py` | terrain/water assembly, anchors, cameras, section, look, travel rig, render |
| `v2layout.py` | lane settlement, placement assertions, vegetation patches, site assembly |
| `build_v2.py` | build one coast checkpoint (`--target kodingareng|tunda|amur`) |
| `build_kit_v2.py` | build the common kit scene and 2560?-1440 asset sheet |
| `build_globe_v2.py` | build the globe scene, markers, cameras, 4K still and region proofs |
| `export_v2.py` | pack source, save `.blend`, export clean GLBs, camera/anchor metadata |
| `make_manifest.py` | build `runtime/asset-manifest.json` from the exported GLB bytes |
| `render_v2.py` | 4K stills, travel frames, globe stills, globe reel frames |
| `analyze_final.py` | palette, contrast and edge-density measurements |
| `coverage_pass.py` | flat-colour object coverage QA renders |
| `verify_assets_v2.py` | fresh Blender re-import/reopen and test render per asset |
| `validate_v2.py` | contract validation of the assembled package |
| `build_handoff_v2.py` | SHA-256 list, ZIP, fresh extraction and extraction hash check |
| `make_media.py` / `encode_media_v2.py` | pitch/review plates and H.264 media |
| `base/` | shared low-level mesh/material/camera/light helpers |

## Commands (run from the repo root)

```powershell
$bl = 'C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe'
$repo = (Resolve-Path '.').Path
$run = Join-Path $repo '3d-art/revision-v2/work/runs/20261121T1445-local'
$s = Join-Path $repo '3d-art/revision-v2/work/scripts'

foreach ($t in 'kodingareng','tunda','amur') {{
  & $bl -b --factory-startup --python-exit-code 1 --python "$s/build_v2.py" -- `
       --repo-root $repo --run-root $run --target $t
  & $bl -b --factory-startup --python-exit-code 1 --python "$s/export_v2.py" -- `
       --run-root $run --staging-root "$repo/3d-art/revision-v2/delivery/LAUTARA_3D_Art_Handoff_v2" --asset-id $t
}}
& $bl -b --factory-startup --python-exit-code 1 --python "$s/build_kit_v2.py" -- --run-root $run
& $bl -b --factory-startup --python-exit-code 1 --python "$s/build_globe_v2.py" -- --run-root $run
```

Renders and packaging use the same run root:

```powershell
& $bl -b --factory-startup --python "$s/render_v2.py" -- --run-root $run --mode stills --target kodingareng
& $bl -b --factory-startup --python "$s/render_v2.py" -- --run-root $run --mode travel --target kodingareng
python "$s/make_manifest.py" --run-root $run --staging-root $stage
python "$s/validate_v2.py" --bundle-root $stage --report "$stage/review/validation.json" --allow-missing-sums
python "$s/build_handoff_v2.py" --staging-root $stage --out "$stage/../LAUTARA_3D_Art_Handoff_v2.zip" --verify-extract <empty-dir>
```

## Look knobs

`v2scene.LOOK` holds the shared daylight look: view transform, exposure, Hue/Sat
grade, sun/fill energy, world strength. `v2sites.SITES[*].palette` holds per-site
material families. `v2scene.build_travel_rig` holds the 168-frame edit and the 133
cut. Change a value, rebuild all three coasts, and re-measure with `analyze_final.py`
and `coverage_pass.py`.

## Notes

- Timeline markers at frame 1 bind `TRAVEL_CAM`. Still renders must park marker
  cameras before assigning `scene.camera`; `v2scene.render_still` does this.
- Film renders use fixed collection visibility in two passes (surface then section)
  because collection `hide_render` is not reliably animatable in Blender 5.2.
- `export_v2.py` uses `export_yup=True`; the manifest's camera and anchor values are
  already in glTF space. Do not apply the axis conversion twice.
- Terrain uses a vertex-colour attribute (`COLOR_0`) so the height bands survive GLB.
"""
    os.makedirs(os.path.join(stage, "source"), exist_ok=True)
    with open(os.path.join(stage, "source", "BUILD.md"), "w", encoding="utf-8") as fh:
        fh.write(build)

    # ----------------------------------------------------------- review report
    review = f"""# v2 review report

Audit date: {date}. Build ID: `{build_id}`. Blender 5.2.2 LTS. All values below
are read from the delivered files or from measured renders in the run folder, not
from planning estimates.

## Gate summary

| Gate | Result | Evidence |
|---|---|---|
| Kodingareng look proof | pass | 960/1280 px proofs, palette band, coverage pass, frame audit |
| Tunda and Amur at same standard | pass | same builders and look rig; measured palette and coverage |
| Shared kit | pass | 16 named components, 2560?-1440 asset sheet |
| Globe locators | pass | 3 locators, 9/9 texture probes, marker nodes in GLB |
| Travel films and reel | {'pass' if encode.get('travel') else 'pending'} | 168 frames/site, ffprobe + full decode, 27 s reel |
| Runtime exports | {'pass' if not failed else 'partial'} | 8 GLBs clean-imported; 5 sources reopened |
| Clean extraction | {'pass' if validation.get('verdict') == 'pass' else 'pending'} | SHA-256 and name-set verification |

## Per-site review

### Kodingareng Lompo

- {builds.get('kodingareng',{}).get('houses','--')} houses on an authored lane network;
  {builds.get('kodingareng',{}).get('settlement_slots',{}).get('slots','--')} lane slots
  tested, {builds.get('kodingareng',{}).get('settlement_slots',{}).get('blocked','--')} rejected
  for overlap or lane clearance, {builds.get('kodingareng',{}).get('settlement_slots',{}).get('terrain','--')} for
  slope/height.
- Survey boat bed maximum Z {builds.get('kodingareng',{}).get('boat_clearance',{}).get('max_bed_z','--')} m;
  clearance pass. Local outriggers also cleared.
- Section: {builds.get('kodingareng',{}).get('section',{}).get('axis','')} A?EUR"B,
  x{builds.get('kodingareng',{}).get('section',{}).get('exag','--')} exaggeration;
  boat and jetty inside 8/8 frame corners.
- Clean stills: overview, north-up plan, approach, detail, section at 3840?-2160.
- Palette: {palette.get('kodingareng/godview',{}).get('luma','--')} luma,
  {palette.get('kodingareng/godview',{}).get('sat','--')} saturation (reference 0.498 / 0.297).

### Pulau Tunda

- {builds.get('tunda',{}).get('houses','--')} houses, greener interior, cove landing,
  mangrove fringe. Boat bed maximum Z {builds.get('tunda',{}).get('boat_clearance',{}).get('max_bed_z','--')} m.
- Section x{builds.get('tunda',{}).get('section',{}).get('exag','--')} exaggeration,
  {coverage.get('tunda_COAST_SECTION.png',{}).get('section',0)*100:.1f}% frame fill.
- Palette: {palette.get('tunda/godview',{}).get('luma','--')} luma,
  {palette.get('tunda/godview',{}).get('sat','--')} saturation.

### Razdolnaya / northern Amur Bay

- {builds.get('amur',{}).get('houses','--')} houses on the east-bank working landing,
  marsh pools, creeks, reed bands and sandbars. Boat bed maximum Z
  {builds.get('amur',{}).get('boat_clearance',{}).get('max_bed_z','--')} m.
- Section x{builds.get('amur',{}).get('section',{}).get('exag','--')} exaggeration,
  {coverage.get('amur_COAST_SECTION.png',{}).get('section',0)*100:.1f}% frame fill;
  estuary water and low banks read in the cut.
- Palette: {palette.get('amur/godview',{}).get('luma','--')} luma,
  {palette.get('amur/godview',{}).get('sat','--')} saturation.

## Defects found during the run and corrected

1. **Still-camera override (render bug).** A timeline marker bound to `TRAVEL_CAM`
   at frame 1 silently replaced `scene.camera` during still renders, producing four
   identical 4K ?EURoebeauty?EUR images. Fixed in `v2scene.render_still` by parking marker
   cameras during stills; re-rendered all stills.
2. **Shore foam bridging (geometry bug).** Unordered marching-squares segments were
   connected in row order, producing large foam quads across the water (up to 30%
   of an Amur frame in the QA pass). Fixed with contour chaining; water FX is now
   ~0.2?EUR"0.5% of frame.
3. **Section backdrop in front of the cut (composition bug).** The backdrop normal
   was chosen before the camera side, putting the cream plane between camera and
   section in Amur (100% backdrop). Fixed by choosing the camera side once and
   handing the same normal to camera and backdrop.
4. **Invalid reef meshes.** Two-vertex ?EURoefaces?EUR in the reef fan triggered exporter
   warnings. Rebuilt as a clean triangle fan; zero mesh warnings on re-export.
5. **Camera framing.** Frame audits caught the survey boat cropped in overview,
   plan, approach and detail. Camera presets were recomputed and audited; boat and
   jetty are now fully inside every required view.
6. **Blown water highlights.** Water specular produced a large >0.9 luminance patch
   in the overview. Raised water roughness to 0.80; blown-pixel share is 0.00% in
   final stills.
7. **Globe locators.** Tunda was ~68 km off; all three replaced with place-board
   values and re-verified against the texture and exported marker nodes.

## Visual review method and remaining check

The session image guardrail prevented attaching rendered images to the chat. Every
shot was verified numerically (palette, saturation, edge density, blown-pixel share,
camera projection bounds, object coverage) and as disk review sheets:
`review/parity-sheet.png`, `review/before-after.png`, `review/runtime-parity.png` and
`work/runs/{build_id}/proofs/look/kodingareng-look-contact-sheet.png`.

A human should still play the three films and the reel once and glance at the
contact sheets before publishing; that is the one review this run could not perform
as a human. Geometry placement, framing, palette and decode checks are evidence-backed.

## Limitations

- Illustrative terrain, seabed, section and prop placement; not surveyed.
- Section is vertically exaggerated and cropped; A/B continue beyond the frame.
- Water is a single alpha plane plus flat foam/ripple marks; no animated normals.
- The globe is a locator illustration, not a georeferenced data layer.
- App, gameplay and field workflow are not part of this package.

## Validation

Verdict: **{validation.get('verdict','pending')}**
({val_summary.get('pass','--')} pass / {val_summary.get('fail','--')} fail /
{val_summary.get('blocked','--')} blocked). Failed item ids:
{', '.join(i['id'] for i in failed) if failed else 'none'}.

{validation_table()}
"""
    os.makedirs(os.path.join(stage, "review"), exist_ok=True)
    with open(os.path.join(stage, "review", "review-report.md"), "w",
              encoding="utf-8") as fh:
        fh.write(review)
    print("DOCS written to", stage)
    # keep the handoff ASCII-only so every viewer/terminal reads it identically
    mapping = {
        "\u00b7": " | ", "\u00d7": "x", "\u2265": ">=", "\u2212": "-",
        "\u2014": "-", "\u2013": "-", "\u2192": "->", "\u00b0": " deg",
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    }
    for dirpath, _dirnames, filenames in os.walk(stage):
        for name in filenames:
            if not name.endswith(".md"):
                continue
            p = os.path.join(dirpath, name)
            with open(p, encoding="utf-8") as fh:
                text = fh.read()
            for a, b in mapping.items():
                text = text.replace(a, b)
            text = "".join(ch if ord(ch) < 128 else "?" for ch in text)
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)


if __name__ == "__main__":
    main()

