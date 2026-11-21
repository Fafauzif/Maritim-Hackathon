# Pulau Tunda · site review

Vegetated island with one settlement cluster and a separate vegetation mass. The landing and
shallow basin are the anchor; roofs sit modest and red-toned among deep green. Real place
identity: Banten coast (globe anchor -5.79, 105.66, indicative only).

## Measured render settings

| Pass | Setting |
|---|---|
| Final stills | 3840x2160, EEVEE, 48 samples, `Khronos PBR Neutral`, exposure -0.35, Hue/Sat 1.2 |
| Proof stills | 960x540, EEVEE, 32 samples |
| Travel film | 1920x1080, EEVEE, 16 samples, 24 fps, 132 frames (5.5 s), cut at frame 109 |
| Scene scale | 1 BU = 1 m, water at Z=0, extents 380 m |
| Geometry | 243 objects, ~166 k triangles, 37 houses, 180 vegetation instances, 3 boats |

## Continuity checks (ray-cast + pixel measurement)

| Check | Measured |
|---|---|
| Boat present and unclipped in every shot | overview 28x47 px, plan 16x25, approach 191x104, detail 186x89, section 47x39 |
| Same waterline in overview and section | water plane at Z=0 in both; section water body top at Z=0 |
| Jetty and boat survive the 320 px preview | boat separates from water at 320 px: dL 0.056, inner span 0.34 |
| Frame composition | overview water 26.1 % / land 66.5 % / buildings 6.0 % / kit 0.5 % / background 0 % |
| Cutaway legibility | cut fills 54.8 % of frame; background 44.5 % is sky above the land profile |
| Palette family | luma 0.586 (ref 0.554), saturation 0.357 (ref 0.362), weighted dE 13.70 |

## Visible defect found and corrected

**Defect:** the approach camera was buried inside the village. Measured before: 41.3 % of the
approach frame was buildings, the boat's projected box ran off the bottom edge
(y0 = -39 px), so the shot read as a wall of roofs instead of a waterfront approach.

**Correction:** pulled the camera out over open water (-178, -112, 48) and re-aimed at the
landing basin; buildings fell to 28.6 %, water rose to 55.2 %, and the boat now sits inside
frame at 191x104 px. Same fix applied to this site's detail camera, which had been sitting on
top of the boat (416x272 px, half of it off-frame) - now 186x89 px with the village behind.

Before/after proof for colour: `work/reviews/before/tunda_overview_oldrig.png` vs
`work/reviews/after/tunda_overview.png` (saturation 0.127 -> 0.358, luma 0.703 -> 0.586).

## Remaining limits

* The green interior and its scrub are procedural scatter, not mapped vegetation; individual
  species are design choices.
* 37 houses are placed by the 5 m grid + lane rule, not by a building census.
* Seabed is illustrative and the section is vertically exaggerated x4.0.
* Water is a flat alpha plane with no animated normals.
