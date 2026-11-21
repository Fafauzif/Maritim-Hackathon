# Deviations · The Ocean Has Floors

Everything here is measured or observed in this run. Nothing is claimed as audit-backed
where it is a design choice, and nothing is excused silently.

## 1. Ink-and-wash post pipeline approximated, not ported

The CityRT audit's signature layer is a Three.js ink/wash post pipeline (hand-drawn ink
edges, line boil, hatching, paper `#F3ECE0`, warm vignette). A full port is out of scope for
an Eevee delivery, so the look is approximated with: a paper-toned sky gradient, matte
Principled materials (metallic 0, roughness 0.85-1.0 on walls/roofs), an inverted-hull
outline modifier on the survey boat and kit houses, and a global Hue/Sat grade.

Measured shortfall: no animated line boil, no hatching, no per-edge ink response. Outlines
survive at 960 px but are removed from every GLB (render trick, not art geometry).

## 2. Palette match: luma/saturation on target, weighted dE over target

Measured with `work/scripts/palette_check.py` against
`cityrt-audit/analysis/palette/italian.json` (reference luma 0.554, saturation 0.362),
on the 960 x 540 overview proofs:

| Coast | luma | dluma | saturation | dsat | weighted dE (target <= 6) |
|---|---|---|---|---|---|
| Kodingareng | 0.609 | +0.055 | 0.362 | 0.000 | 13.84 |
| Tunda | 0.586 | +0.032 | 0.357 | -0.005 | 13.70 |
| Amur | 0.598 | +0.044 | 0.293 | -0.069 | 11.46 |

The dE target was set for a city-street reference whose palette is 44 % olive plus 16 %
timber and 11 % dark brown; these frames are landscape-dominant, so the light-plaster and
dark-timber families have nothing to land on. Luma and saturation were brought onto the
reference band by a measured rig sweep (`work/verification/lookdev-*.json`), and the dE
shortfall is accepted rather than faked by desaturating the landscape.

## 3. Sections are illustrative and vertically exaggerated

* Seabed and land profiles come from the same procedural height field as the beauty shots:
  they are **not** surveyed bathymetry and carry no depth data.
* Vertical exaggeration is x4.0 for the two islands and x3.4 for the Amur cut
  (`section_exag` in `work/scripts/site_build.py`). At true scale a 7 m water column in a
  130 m cut is unreadable; this is an illustration convention and is labelled as such in
  the handoff.
* The cut is framed as a 16:9 crop centred on the survey boat; the island cuts crop the
  deepest bed tip out of frame by design.

## 4. Globe anchors are indicative art positions

| Coast | Latitude | Longitude | Basis |
|---|---|---|---|
| Kodingareng Lompo | -5.09 | 119.30 | Makassar archipelago, place-identity anchor |
| Pulau Tunda | -5.79 | 105.66 | Banten coast, place-identity anchor |
| Razdolnaya mouth | 43.25 | 131.80 | northern Amur Bay, river-mouth anchor |

These are globe locators, not survey coordinates, and the markers are original designs.
Texture orientation was verified by sampling nine known land/ocean points through the
texture's own UV convention (`work/scripts/globe_build.py::texture_probe`): Sahara, Siberia,
Australia, North America, Central Pacific, Indian Ocean, North Atlantic, equatorial Atlantic,
and the painted Antarctic: all 9 land/ocean expectations pass. The supplied art paints
Antarctica in the same sand tone as other land; that is an art property, not an orientation
error.

## 5. Village density is rule-driven, not reference-counted

Houses are placed on the audit's 5 m cell ladder with a lane mask: 27 (Kodingareng),
37 (Tunda), 34 (Amur). Footprints come from the 4-variant ladder (5x5, 6x5, 10x5, 15x10).
Exact building counts and current pier geometry are explicitly illustrative in the place
cards. At overview scale the Amur village reads sparse; that is the honest remaining
weakness of that frame.

## 6. Renderer: Eevee only, no Cycles/OptiX comparison

All stills and films are Eevee (`BLENDER_EEVEE`), 32-64 samples for stills, 16-24 for
animation. The brief offered a Cycles/OptiX comparison as an option; it was not run, so no
claim is made that Eevee is better: only that it is the tested, consistent renderer across
all three coasts and the globe.

## 7. Films are two-shot edits

Each `travel.mp4` is 5.5 s at 24 fps: an animated travel camera (overview -> approach ->
20 m lateral move with parallax -> push toward the boat) and then a hard cut at frame 109 to
the square-on orthographic section camera, which holds for 1 s. That is an editorial match
cut, not a continuous single-camera move from the sky into the water column.

`coast-reel.mp4` is an editorial concat: 3 s globe orbit -> three 5.5 s coast films -> 1 s
globe return. The globe-to-coast transition is a cut on continuing motion, not a continuous
coordinate zoom; the two worlds use separate cameras, clipping ranges and scales as the
travel brief requires.

## 8. Water

A single opaque-ish alpha Principled plane at Z = 0 (`ENV_Water`), roughness 0.16, no
animated normals: the calm-surface rule from the audit intake. It is a distinct, separately
named, export-safe object in every scene and in every GLB. Because glTF has no equivalent of
the Blender alpha blend used for the render, the GLB water reads flatter than the render; it
is exported as authored with embedded materials and no external textures.
