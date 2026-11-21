# Kodingareng Lompo · site review

Compact inhabited island edge: settlement cluster on the lee shore, one jetty reaching
south-east into shallow water, survey boat held clear of the shore. Real place identity:
Makassar archipelago (globe anchor -5.09, 119.30, indicative only).

## Measured render settings

| Pass | Setting |
|---|---|
| Final stills | 3840x2160, EEVEE, 48 samples, `Khronos PBR Neutral`, exposure -0.35, Hue/Sat 1.2 |
| Proof stills | 960x540, EEVEE, 32 samples |
| Travel film | 1920x1080, EEVEE, 16 samples, 24 fps, 132 frames (5.5 s), cut at frame 109 |
| Scene scale | 1 BU = 1 m, water at Z=0, extents 340 m |
| Geometry | 179 objects, ~137 k triangles, 27 houses, 126 vegetation instances, 3 boats |

## Continuity checks (ray-cast + pixel measurement, not eyeballing)

| Check | Measured |
|---|---|
| Boat present and unclipped in every shot | overview 42x58 px, plan 19x28, approach 47x83, detail 104x109, section 129x41 |
| Same waterline in overview and section | water plane at Z=0 in both; section water body top at Z=0 |
| Jetty and boat survive the 320 px preview | boat separates from water at 320 px: dL 0.038, inner span 0.42 |
| Frame composition | overview water 37.2 % / land 51.2 % / buildings 6.5 % / kit 0.6 % / background 0 % |
| Cutaway legibility | cut fills 57.8 % of frame; background 41.4 % is sky above the land profile |
| Palette family | luma 0.609 (ref 0.554), saturation 0.362 (ref 0.362), weighted dE 13.84 |

## Visible defect found and corrected

**Defect:** the cutaway read as a thin ribbon floating in empty sky. Two causes: the section
mesh was hollow under dry land (land only above Z=0, bed only below it), and the section
camera was a distant perspective. Measured before: 12 % of the frame was cut geometry,
65-78 % background.

**Correction:** rebuilt the cut as one continuous solid block (deep rock, mid strata, soil,
grass cap, water column) and replaced the camera with a square-on orthographic rig framed
from the measured cut bounds at x4.0 vertical exaggeration. After: 57.8 % frame fill, boat
129x41 px on the waterline.

Before/after proof: `work/reviews/before/kodingareng_section_hollow.png` vs
`work/reviews/after/kodingareng_section.png`.

## Second defect: colour pipeline

The first "final" stills measured luma 0.721 / saturation 0.120 - a washed-out frame that
looked nothing like the audit reference band. Cause: colour management was written twice,
so `run_build` re-imposed AgX + exposure 0.1 after the look rig applied. Removing the
duplicate and measuring a rig sweep produced luma 0.609 / saturation 0.362.
Proof: `work/reviews/before/kodingareng_overview_oldrig.png` vs
`work/reviews/after/kodingareng_overview.png`.

## Remaining limits

* Seabed is illustrative, not surveyed; section is vertically exaggerated x4.0 and cropped to
  the boat-centred waterfront.
* 27 houses are placed by the 5 m grid + lane rule, not by a building census.
* Water is a flat alpha plane with no animated normals.
* The ink/wash pipeline is approximated (see `review/deviations.md`).
