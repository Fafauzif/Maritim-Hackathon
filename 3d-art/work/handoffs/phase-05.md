# Phase 05 handoff · review, revise, final renders

Status: **complete.** Image rule respected: 0 images attached.

## Delivered finals

| Output | Source render | Size |
|---|---|---|
| `output/coasts/kodingareng/godview.png` | `work/renders/final-4k/kodingareng_godview.png` | 3840x2160, 9.37 MB |
| `output/coasts/kodingareng/mapview.png` | `..._mapview.png` | 3840x2160, 9.16 MB |
| `output/coasts/kodingareng/section.png` | `..._section.png` | 3840x2160, 7.51 MB |
| `output/coasts/tunda/*.png` | same triple | 8.75 / 8.97 / 7.37 MB |
| `output/coasts/amur/*.png` | same triple | 8.76 / 8.43 / 7.21 MB |
| `output/globe/globe-overview.png` | `final-4k/globe_overview.png` | 3840x2160, 8.53 MB |
| `output/review/parity-sheet.png` | nine 4K stills, 1200 px tiles | 3648x2249, 4.13 MB |
| `output/kit/asset-sheet.png` | kit sheet | 1920x1080, 2.16 MB |

Render settings, all ten stills: EEVEE, 48-64 samples, 3840x2160, `Khronos PBR Neutral`,
exposure -0.35, Hue/Sat 1.2. Measured wall time for the Kodingareng triple was 33.5 s
including Blender startup (10 s per still).

## Review method (no human, no images in the conversation)

* Ray-cast framing per camera: water/land/buildings/vegetation/survey-kit/background share and
  the survey boat's projected pixel box (`work/verification/shot-verify.json`).
* 320 px legibility: boat contrast against a surrounding ring + Otsu silhouette split
  (`work/verification/verify-320.json`).
* Palette: k-means 6-colour palette, luma, saturation and weighted CIE76 dE against the audit
  reference (`work/verification/palette-coast.json`).
* Before/after proofs per coast in `work/reviews/before|after/` (old colour rig vs measured
  rig; hollow cut vs solid cut).
* Pixel statistics on every final file: `work/scripts/contact_sheet.py stats` (luma, content
  fraction, edge contact, dead-frame detection).

## Scores (equal criteria, all three sites)

| Criterion | Kodingareng | Tunda | Amur |
|---|---|---|---|
| Overview boat survives 320 px | yes (14x19 px, dL 0.038) | yes (9x16 px, dL 0.056) | yes (11x14 px, dL 0.048) |
| Cutaway legible | 57.8 % frame fill | 54.8 % | 83.2 % |
| Palette luma / sat vs ref | 0.609 / 0.362 | 0.586 / 0.357 | 0.598 / 0.294 |
| Water in overview | 37.2 % | 26.1 % | 66.7 % |
| Background in beauty frame | 0.0 % | 0.0 % | 0.0 % |

## Defects raised and corrected (one per coast, minimum)

1. **Kodingareng** - hollow cutaway + distant perspective section camera -> solid cut + ortho
   rig (frame fill 12 % -> 57.8 %).
2. **Tunda** - approach camera inside the village (41.3 % buildings, boat half out of frame)
   -> re-aimed over water (28.6 % buildings, boat 191x104 px inside frame).
3. **Amur** - section was 9.2 % frame fill in 90.7 % empty background -> 83.2 % fill.
4. **All coasts** - colour management applied twice (AgX override) producing luma 0.70-0.72 /
   saturation 0.11-0.13; removed the duplicate, measured rig to 0.586-0.609 / 0.294-0.362.

## Remaining limits

* No independent human reviewer saw the finals; the review is measurement-based and that is
  stated in `output/review/deviations.md`.
* Amur village reads sparse at overview scale.
* GLB water reads flatter than the render (glTF has no alpha blend equivalent).
