# Razdolnaya mouth, northern Amur Bay · site review

Flat estuary with wide water and low banks: the river opening and its sideways flow establish
the plan view; a hand-built working landing and one generic survey boat anchor the camera
renders. Real place identity: northern Amur Bay, Primorye (globe anchor 43.25, 131.80,
indicative only).

## Measured render settings

| Pass | Setting |
|---|---|
| Final stills | 3840x2160, EEVEE, 48 samples, `Khronos PBR Neutral`, exposure -0.35, Hue/Sat 1.2 |
| Proof stills | 960x540, EEVEE, 32 samples |
| Travel film | 1920x1080, EEVEE, 16 samples, 24 fps, 132 frames (5.5 s), cut at frame 109 |
| Scene scale | 1 BU = 1 m, water at Z=0, extents 460 m |
| Geometry | 468 objects, ~146 k triangles, 34 houses, 410 vegetation instances, 1 boat |

## Continuity checks (ray-cast + pixel measurement)

| Check | Measured |
|---|---|
| Boat present and unclipped in every shot | overview 34x41 px, plan 13x20, approach 99x58, detail 136x90, section 91x43 |
| Same waterline in overview and section | water plane at Z=0 in both; section water body top at Z=0 |
| Jetty and boat survive the 320 px preview | boat separates from water at 320 px: dL 0.048, inner span 0.30 |
| Frame composition | overview water 66.7 % / land 28.0 % / buildings 4.8 % / kit 0.5 % / background 0 % |
| Cutaway legibility | cut fills 83.2 % of frame - the estuary channel is the subject, so the whole water column stays in frame |
| Palette family | luma 0.598 (ref 0.554), saturation 0.294 (ref 0.362), weighted dE 11.46 |

## Visible defect found and corrected

**Defect:** this site's cutaway was the worst of the three before the fix - a distant
perspective camera turned the 170 m x 37 m A-B cut into a thin band: only 9.2 % of the frame
was cut geometry, and 90.7 % was empty background.

**Correction:** rebuilt the cut as a continuous solid block and moved the camera to a
square-on orthographic rig framed from the measured bounds (fill factor 0.95 because the
river channel is the subject). After: 83.2 % frame fill, 16.3 % background, boat 91x43 px on
the waterline.

Before/after proof for colour: `work/reviews/before/amur_overview_oldrig.png` vs
`work/reviews/after/amur_overview.png` (saturation 0.108 -> 0.294, luma 0.714 -> 0.598).

## Remaining limits

* The village cluster reads sparse at overview scale; it is 34 houses on the 5 m grid and the
  shortest improvement path is a denser lane mask around the landing, not more geometry.
* Land is deliberately empty beyond the bank; no city skyline, per the place card.
* 4.9 % of the approach frame is sky above the low horizon - intended for a flat estuary, but
  it is the least filled frame of the nine stills.
* Water is a flat alpha plane with no animated normals; the GLB version reads flatter.
* Seabed/channel are illustrative, vertically exaggerated x3.4.
