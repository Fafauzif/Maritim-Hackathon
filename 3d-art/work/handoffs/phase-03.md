# Phase 03 handoff · finish all three coasts

Status: **complete.** Superseded by phase-05.md (4K stills, parity sheet) and phase-06.md (export).
Updated 2026-11-21. Image rule respected: 0 images attached; every claim below came from PNG bytes or ray casts on disk.

## Checkpoints (open these to resume)

| Scene | Path | Contents |
|---|---|---|
| Kodingareng | `work/checkpoints/03-kodingareng.blend` | 179 objects, ~137 k tris, 27 houses, 126 plants, 3 boats |
| Tunda | `work/checkpoints/03-tunda.blend` | 243 objects, ~166 k tris, 37 houses, 180 plants, 3 boats |
| Amur | `work/checkpoints/03-amur.blend` | 468 objects, ~146 k tris, 34 houses, 410 plants, 1 boat |

All three carry the same collections (`ENV_Land, ENV_Water, BLD_Village, PROP_Survey, VEG_Scatter, SEC_Section, CAM_Rigs, LGT_Rig`), the same five cameras and the same look rig. `SEC_Section` is hidden in beauty shots and shown only for `COAST_SECTION`.

## Shot contracts (measured with `work/scripts/verify_shot.py`)

Camera names are stable; use them in the handoff and in the travel rigs.

| Camera | Lens/type | Measured framing (water / land / buildings / kit / background, boat px @960) |
|---|---|---|
| `COAST_OVERVIEW` | 58/55/58 mm, high oblique ≈40° | K 37/51/6.5/0.6/0 — boat 42×58; T 26/67/6/0.5/0 — 28×47; A 67/28/4.8/0.5/0 — 34×41 |
| `COAST_PLAN` | ortho 330/380/460, nadir north-up | K 65/31/1.6/0.1 — 19×28; T 50/47/1.8/0.2 — 16×25; A 33/66/1.1/0.1 — 13×20 |
| `COAST_APPROACH` | 50/70/74 mm, 25–40° down | K 46/40/7.2/1.3 — 47×83; T 55/11/28.6/5 — 191×104; A 81/10/2.6/1.3 — 99×58 |
| `COAST_DETAIL` | 40/40/38 mm, waterfront close-up | K 38/26/5/3.2 — 104×109; T 50/9/16.4/3.6 — 186×89; A 58/6/3.9/2.8 — 136×90 |
| `COAST_SECTION` | ortho 54–96, square-on A–B | cut fills K 58 % / T 55 % / A 83 %; boat 129×41 / 47×39 / 91×43 |

No shot clips the boat out of frame. Only the Amur approach/section and the two island sections show >3 % background (sky above a low bank or above the land profile) — that is the intended composition, not a gap.

## Look rig (single source of truth: `work/scripts/look_rig.py`)

`Khronos PBR Neutral`, look `None`, exposure −0.35, sun 5.4, sky fill 150, world 0.28, compositor Hue/Sat 1.2.
Measured against `cityrt-audit/analysis/palette/italian.json`:

| Render | luma (ref 0.554) | saturation (ref 0.362) | weighted ΔE (target 6) |
|---|---|---|---|
| kodingareng overview | 0.609 | 0.362 | 13.84 |
| tunda overview | 0.586 | 0.357 | 13.70 |
| amur overview | 0.598 | 0.293 | 11.46 |

ΔE stays over target because the reference frame is a dense city street (plaster walls, timber shadows make up 44 % + 16 % of its palette) while these frames are landscape-dominant. Luma and saturation bands match; the ΔE shortfall must be written into `output/review/deviations.md` at phase 06, not hidden.

## Defects fixed this phase (with evidence)

1. Section cut was a hollow silhouette → continuous solid block; frame fill 12 % → 58/55/83 %.
2. Section camera was a far perspective ribbon → square-on ortho framed from measured cut bounds.
3. Detail cameras were inside the boat (4000 px projected bbox, off-frame) → refit; boat now 104–186 px wide, in frame.
4. Tunda approach was buried in buildings → moved out over water (buildings 41 % → 29 %, boat in frame).
5. Kodingareng approach had no readable village → widened lens and re-aimed (buildings 0 % → 7.2 %).
6. **Colour management was set twice**: `run_build` re-imposed AgX/exposure 0.1 after the look rig applied, so the first "final" renders measured luma 0.68 / sat 0.20 instead of the tuned 0.61/0.36. Removed the duplicate; `look_rig.py` is now the only writer.
7. Blender 5.2 **compositor output node does not exist** (`CompositorNodeComposite` undefined): the grade tree had a dangling Hue/Sat with no output, so the grade never applied in earlier renders. Rebuilt with a `NodeGroupOutput` plus an `Image` output socket on the group interface.

## Open issues (next session)

- **Before/after review per site** with a named visible defect and its correction is not written yet (phase 03 item 4, phase 05 item 2). The proof pairs exist for a first "after"; a genuine "before" needs one deliberate regression/rebuild cycle per site, or honest wording that the before state is the pre-fix render already on disk.
- No `review.md` per coast yet; those are phase 05/06 artifacts (`output/coasts/<site>/review.md`).
- Water is a flat alpha Principled plane at Z=0; brief wants a distinct export-safe water object (exists: `ENV_Water`) and a calm surface cue. No ripple/normal treatment yet — phase 03 item 1 leaves this open.
- House counts (27/37/34) come from the 5 m grid + lane mask, not from reference density; the audit's grid rule passes but the villages may read sparse at overview scale. Needs a 320 px check on the beauty renders, not just the clay.
