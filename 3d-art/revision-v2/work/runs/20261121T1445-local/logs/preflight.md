# Phase 0 preflight report

Run ID: `20261121T1445-local`
Repo root: resolved to the current checkout; Git HEAD `e07093ef34118bc3e686257accbbfe6246595153`.
Tracked v1 output: unchanged (33 files, 131,680,327 bytes, SHA-256 list recomputed clean).
Only `3d-art/revision-v2/work/` and `3d-art/revision-v2/delivery/` are new/untracked.

## Tools found

| Tool | Path / version |
|---|---|
| Blender CLI + MCP | `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, 5.2.2 LTS, build `d13f752e3b9c` |
| Live Blender session | v1 checkpoint `3d-art\work\checkpoints\04-travelB-amur.blend`, dirty unsaved state; left untouched |
| FFmpeg / FFprobe | 8.1.2 full build, `C:\Users\fauzi\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe` |
| Python for media | workspace runtime Python 3.13 with Pillow 12.3 and NumPy 2.3.5 |
| GPU | NVIDIA RTX 4060 Laptop, 8 GB; EEVEE |
| Disk / RAM | ~190 GB free on C:, 32 GB RAM |

## Path parity

- Blender MCP wrote `work/runs/20261121T1445-local/tmp/parity-from-blender.json`;
  the harness read it with the exact expected content.
- The harness wrote `tmp/parity-from-dsh.json`; Blender read and returned it.
- Both directions use one Windows path space.

## Smoke test

- Opened v1 `output/coasts/kodingareng/scene.blend` in a fresh 5.2 factory process:
  179 objects, 5 cameras, EEVEE, clean open.
- Rendered 480x270 / 8 samples: 5.03 s.
- Exported a GLB (2.97 MB) and re-imported it: 159 meshes, 13 materials, 0 cameras,
  0 lights, `ENV_Water` present.
- Full 4K / 32-sample overview timing: 7.62 s. This made 15 final 4K stills practical.

## Visual route under the image guardrail

No raster image was attached to the conversation. The review route used:
1. programmatic pixel metrics on every final PNG (luma, saturation, edge density,
   blown-pixel share, object coverage);
2. camera projection audits for boat/jetty/landing bounds;
3. tiled contact sheets saved to disk, with one final parity sheet reserved for the
   owner's human sign-off.

This is recorded as a limitation in the review report: the run itself did not perform
a human visual playback of the films.

## Baseline protection

- Original `3d-art/output` and `3d-art/work/checkpoints` tracked files are unchanged.
- The live Blender session's unsaved v1 work was not saved or cleared.
- All production used factory-startup background processes against v2 checkpoints.
