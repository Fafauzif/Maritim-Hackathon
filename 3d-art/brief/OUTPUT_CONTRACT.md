# Output contract

All paths below are relative to `3d-art/`. Create folders as needed. Existing project sources and audit results are read-only in this run. If `output/` already contains a previous run, put this run under a new versioned folder and pass that location to the checker explicitly. Save ongoing work under `work/`. Keep durable phase checkpoints as separate Blender files. Never use a final file as the only working copy.

```text
work/
  progress.json
  tooling.md
  evidence.md
  scripts/                     recorded build scripts used during the run
  checkpoints/                 resumable phases
  renders/                     image sequences and drafts
  reviews/
    blockout-parity.png
    before/                    3 coasts, common grid
    after/                     3 coasts, same grid
output/
  globe/
    globe.blend
    globe.glb
    globe-overview.png         3840 × 2160
  coasts/
    kodingareng/
    tunda/
    amur/
      scene.blend              each of these folders contains the same files
      coast.glb
      godview.png              3840 × 2160
      mapview.png              3840 × 2160, north up
      section.png              3840 × 2160
      travel.mp4               1920 × 1080, 24 fps target
      review.md
  kit/
    common-kit.blend
    common-kit.glb
    asset-sheet.png
  coast-reel.mp4               1920 × 1080, 24 fps target
  review/
    audit-intake.md
    parity-sheet.png
    handoff.md
    export-check.md
    deviations.md
```

## What counts as complete

- Kodingareng, Tunda and Amur receive the same kinds of shots and the same standards for detail, color, scale, render size, navigation and export. The Earth overview is a separate scene with real continent outlines. The world-scale and local assets can be opened separately and are tied together by the reel, camera presets and handoff.
- Each coast flight shows, in roughly 5–8 seconds, wider coast context, god’s-eye exploration and a deliberate move or match cut to the section. Use an animatic first. The overall reel starts on Earth, includes all three places for comparable durations and returns to Earth or finishes on a three-coast comparative frame. A roughly 22–30 second reel is a target, not an encoded duration requirement. Deliver a proof even if a final encoding fails, label the gap and keep the resumable frames.
- Pack images and any required textures inside each final `.blend`; either append reused meshes or verify the delivered files open with the output folder copied elsewhere. Bake or simplify materials for export. Each GLB uses included/embedded resources and can be inspected separately. Keep a separate, configurable water object, a usable art-only seabed and stable anchor nodes in Blender. Exports include authored geometry and supported materials with explicit manifest notes for render-only extras. Exclude Blender camera and light objects from exported meshes.
- `review/audit-intake.md` ties art choices to actual audit outputs. `review/parity-sheet.png` shows the three sites side-by-side with overhead, map or cutaway crops at equal scale in the sheet. For each site, `review.md` lists continuity checks, measured render settings, inspection method, one visible defect and its correction, and remaining limits. `export-check.md` records all five GLB re-imports plus axes/dimensions, texture/material checks, water behavior and proof paths. `deviations.md` records attempted fixes and achieved outputs. `handoff.md` names camera presets and collections, how to orbit the scene, file-version/units/export notes, attribution and important limitations.
- Do not describe a file as validated by Blender or visually reviewed if only its existence was checked. See `brief/DELIVERY_CHECK.md`.

## Checkpoint record

A plain JSON object in `work/progress.json`, updated after every phase or recovery. Write to a temporary sibling and replace atomically. Start with this shape:

```json
{
  "run_id": "local-time-or-other-unique-id",
  "audit_root": null,
  "production_root": "3d-art/output",
  "audit_status": "pending",
  "phase": "00",
  "last_completed_phase": null,
  "site_status": {"kodingareng": "pending", "tunda": "pending", "amur": "pending"},
  "last_scene_checkpoint": null,
  "image_review_capability": "unknown",
  "evidence": [],
  "blockers": [],
  "next_action": "Discover the MCP tools and audit outputs."
}
```

Use relative paths in the progress, log and product handoff where portability matters. Record live evidence as a file path and, where useful, its dimensions/hash. Never paste secrets, authenticated session files, or raw HAR request headers into a new handoff.
