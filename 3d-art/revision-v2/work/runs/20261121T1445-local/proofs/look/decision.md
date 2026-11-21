# Phase 1 look decision

## Reference measurements

The owner's CityRT finish reference is 480x640 and measures luma 0.498,
saturation 0.297, edge density 0.125, blown pixels 6.0%. The two earlier CityRT
sheets measure luma 0.504 / 0.427 and saturation 0.277 / 0.275. The family is
warm, matte, mid-key and clearly lined.

V1 coast overviews measured luma 0.586-0.609 and edge density 0.003-0.007: brighter,
flatter and less defined than the reference.

## Chosen recipe

- Khronos PBR Neutral, exposure -0.56, Hue/Sat grade 0.96.
- Warm key sun 4.3 with 3.4 deg angular size; cool sky fill; low warm water bounce.
- Matte water (roughness 0.80) plus cream shoreline ribbon and sparse graphic ripple
  strokes, so the water reads as calm illustrated surface instead of a blown specular.
- Warm plaster wall families, terracotta / teal / timber roof families, olive-green
  foliage, low-saturation teal estuary water.
- Shaped geometry first: lane hierarchies, varied roof profiles, eaves, porches,
  stilt foundations, jetty rails, boat cabins and rigging, separate foliage masses.
- No render-only ink post-process in the shipped GLBs; silhouette comes from geometry,
  roof overlap and contact shadow.

## Proof gate

| Measure | Result |
|---|---|
| Kodingareng overview luma / saturation | 0.560 / 0.305 |
| Kodingareng approach | 0.560 / 0.292 |
| Kodingareng detail | 0.547 / 0.258 |
| Kodingareng section | 0.550 / 0.188 |
| Blown-pixel share (all Kodingareng stills) | 0.00-0.01% |
| Boat fully inside overview / plan / approach / detail | 8/8 corners each |
| Jetty fully inside the same views | 8/8 corners each |
| 320 px review | boat 353 px, jetty 546 px, buildings 2,595 px in the overview |

The same recipe was applied to Tunda and Amur; their measured luma is 0.497-0.607
and saturation 0.176-0.324 across the five views. The look is consistent while the
site palettes stay distinct.

## Decision

Carry this recipe into all three coasts, the kit, the section and the globe. Rejected
alternatives: heavier ink outline (does not survive core glTF), stronger saturation
(1.10 measured 0.343-0.381, above the reference family), and glossier water (produced
a 5-8% blown highlight patch).
