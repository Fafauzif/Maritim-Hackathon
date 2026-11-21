# Handoff index · The Ocean Has Floors

One note per phase boundary, plus the rules a new session needs before touching anything.

## Read these first (in this order)

1. `3d-art/output/review/handoff.md` — how to open and navigate the delivered scenes.
2. `3d-art/work/progress.json` — the live ledger (phase, checkpoints, look rig, delivery).
3. `3d-art/work/handoffs/phase-01.md` ... `phase-06.md` — what is actually done, what broke,
   what is measured.
4. `3d-art/work/tooling.md` — real Blender/MCP/paths facts of this workstation.
5. `3d-art/brief/*` — the run's contract (all numbered prompts 00-06 have now been executed).

## Image policy (non-negotiable in this project)

- **Images attached across the entire run: 0 of 20.** Hard stop at 15 was never approached.
- Every render is written to `3d-art/work/renders/**` or `3d-art/output/**` and judged from
  PNG bytes with:
  - `work/scripts/verify_shot.py` — ray-cast coverage + boat pixel projection per camera
  - `work/scripts/verify_320.py` — 320 px boat contrast + Otsu silhouette split
  - `work/scripts/palette_check.py` — luma/saturation/dE against the audit palette
  - `work/scripts/contact_sheet.py` — one tiled sheet per checkpoint, on disk
  - `work/scripts/ascii_probe.py` — luminance map as text, for shape debugging
  - `work/scripts/encode_media.py` — ffprobe on every delivered film
- For a human review, open the single sheet for that checkpoint; do not attach per-camera files.

## Final state

| Phase | State | Evidence |
|---|---|---|
| 00 preflight | done | `work/checkpoints/00-preflight.blend`, `work/renders/smoke.png` |
| 01 blockout | done | `work/reviews/blockout-parity.png`, `work/verification/verify-320.json` |
| 02 kit + lookdev | done | `output/kit/*`, `work/renders/kit/material-*.png`, `work/scripts/look_rig.py` |
| 03 finish | done | `work/checkpoints/03-*.blend`, `work/reviews/before|after/` |
| 04 globe + travel | done | `output/globe/*`, `output/coasts/*/travel.mp4`, `output/coast-reel.mp4` |
| 05 critique + 4K | done | ten 3840x2160 stills, `output/review/parity-sheet.png` |
| 06 export + handoff | done | `tools/check_delivery.py` -> 33/33 |

## How to resume in a fresh session

```text
Read 3d-art/output/review/handoff.md, 3d-art/work/progress.json and
3d-art/work/handoffs/README.md. The delivery is complete (33/33). If further work is
requested, open the relevant 03-<site>.blend checkpoint, confirm the five cameras and the
look rig in work/scripts/look_rig.py, and verify renders numerically with work/scripts/*.
Never attach images.
```

Blender must be open with the MCP add-on. The working tree keeps every checkpoint; the
delivery lives in `3d-art/output/` and is complete as of 2026-11-21.
