# Phase 01 handoff · reference + equal blockout

Status: **complete** (verified 2026-11-21, this session). Image rule respected: 0 images attached.

## What exists

| Artifact | Path |
|---|---|
| Blockout renders (Workbench MATERIAL clay, 960×540) | `work/renders/blockout/{kodingareng,tunda,amur}_{overview,section}.png` |
| 320 px derivatives (legibility test) | `work/renders/blockout/320/*_320.png` |
| **Parity sheet (phase gate)** | `work/reviews/blockout-parity.png` — 676×746, 6 tiles, shared 320 px, captions with measured boat size |
| Beauty-stage proofs for the same cameras | `work/renders/coast/…` (see phase-03 note) |
| Checkpoint carrying the blockout camera set | `work/checkpoints/01-kodingareng.blend` |
| Machine evidence | `work/verification/shot-verify.json`, `shot-verify.txt`, `verify-320.json` |

## Verdict on each coast at 320 px (measured, not eyeballed)

| Coast | Overview boat | Boat reads | Silhouette (Otsu) |
|---|---|---|---|
| Kodingareng Lompo | 14×19 px | yes (ΔL 0.038, inner span 0.42) | two-tone split 0.44 dark |
| Pulau Tunda | 9×16 px | yes (ΔL 0.056, inner span 0.34) | split 0.60 dark |
| Razdolnaya / Amur | 11×14 px | yes (ΔL 0.048, inner span 0.30) | split 0.10 dark (open water dominant) |

Section tiles: cut fills 58 / 55 / 83 % of frame, boat 43×14 / 16×13 / 30×14 px at 320.

## What had to be fixed to get here

1. **Section geometry was hollow.** The old builder drew land only above Z=0 and bed only below it, so the cut was empty under dry land (65–78 % of frame was background). Rebuilt as one continuous solid block with strata + grass cap + water column (`scene_build.build_section`).
2. **Section camera was a distant perspective.** Replaced with a square-on orthographic camera framed from measured cut bounds (`section_fill` / `section_exag` per site).
3. **Detail cameras sat on top of the boat** (boat projected 4000 px wide, off-frame). Refit to 55–70 m distance with 38–46 mm lenses.
4. **Kodingareng approach was inside open water with no village.** Refit so buildings read (bld 0 → 7.2 %).
5. **Clay renders were unreadable.** Workbench was `SINGLE` colour; switched to `MATERIAL` + shadows + cavity so the clay proof carries colour separation.

## Open issues carried forward

- Blockout stage never had its own pre-props checkpoints for tunda/amur; `01-kodingareng.blend` is the only 01 checkpoint. The 03 checkpoints supersede it for all further work.
- No independent reviewer has seen `blockout-parity.png`; it exists for the owner's eyes only.
