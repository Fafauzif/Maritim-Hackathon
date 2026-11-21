# Rebuilding the v2 art

## Environment

- Blender 5.2.2 LTS (`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`)
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
| `build_kit_v2.py` | build the common kit scene and 2560x1440 asset sheet |
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
$bl = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$repo = (Resolve-Path '.').Path
$run = Join-Path $repo '3d-art/revision-v2/work/runs/20261121T1445-local'
$s = Join-Path $repo '3d-art/revision-v2/work/scripts'

foreach ($t in 'kodingareng','tunda','amur') {
  & $bl -b --factory-startup --python-exit-code 1 --python "$s/build_v2.py" -- `
       --repo-root $repo --run-root $run --target $t
  & $bl -b --factory-startup --python-exit-code 1 --python "$s/export_v2.py" -- `
       --run-root $run --staging-root "$repo/3d-art/revision-v2/delivery/LAUTARA_3D_Art_Handoff_v2" --asset-id $t
}
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

## Globe reproduction inputs

`source/scripts/globe/` contains `make_globe_seed.py` and `earth-base-color.jpg`; `build_globe_v2.py` prefers that local folder. If both are absent, copy them from the project `3d-art/references/globe/` folder.
