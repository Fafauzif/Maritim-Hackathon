# v2 review report

Audit date: 2026-11-21. Build ID: `20261121T1445-local`. Blender 5.2.2 LTS. All values below
are read from the delivered files or from measured renders in the run folder, not
from planning estimates.

## Gate summary

| Gate | Result | Evidence |
|---|---|---|
| Kodingareng look proof | pass | 960/1280 px proofs, palette band, coverage pass, frame audit |
| Tunda and Amur at same standard | pass | same builders and look rig; measured palette and coverage |
| Shared kit | pass | 16 named components, 2560x1440 asset sheet |
| Globe locators | pass | 3 locators, 9/9 texture probes, marker nodes in GLB |
| Travel films and reel | pass | 168 frames/site, ffprobe + full decode, 27 s reel |
| Runtime exports | pass | 8 GLBs clean-imported; 5 sources reopened |
| Clean extraction | pass | SHA-256 and name-set verification |

## Per-site review

### Kodingareng Lompo

- 34 houses on an authored lane network;
  112 lane slots
  tested, 24 rejected
  for overlap or lane clearance, 12 for
  slope/height.
- Survey boat bed maximum Z -6.695 m;
  clearance pass. Local outriggers also cleared.
- Section: [[12.985111570629968, -175.85111570629968], [0.049628097900107804, 13.5037190209989]] A-B,
  x3.2 exaggeration;
  boat and jetty inside 8/8 frame corners.
- Clean stills: overview, north-up plan, approach, detail, section at 3840x2160.
- Palette: 0.5599 luma,
  0.3055 saturation (reference 0.498 / 0.297).

### Pulau Tunda

- 40 houses, greener interior, cove landing,
  mangrove fringe. Boat bed maximum Z -7.396 m.
- Section x3.2 exaggeration,
  52.1% frame fill.
- Palette: 0.5382 luma,
  0.3074 saturation.

### Razdolnaya / northern Amur Bay

- 22 houses on the east-bank working landing,
  marsh pools, creeks, reed bands and sandbars. Boat bed maximum Z
  -6.6 m.
- Section x3.0 exaggeration,
  56.6% frame fill;
  estuary water and low banks read in the cut.
- Palette: 0.4972 luma,
  0.2598 saturation.

## Defects found during the run and corrected

1. **Still-camera override (render bug).** A timeline marker bound to `TRAVEL_CAM`
   at frame 1 silently replaced `scene.camera` during still renders, producing four
   identical 4K "beauty" images. Fixed in `v2scene.render_still` by parking marker
   cameras during stills; re-rendered all stills.
2. **Shore foam bridging (geometry bug).** Unordered marching-squares segments were
   connected in row order, producing large foam quads across the water (up to 30%
   of an Amur frame in the QA pass). Fixed with contour chaining; water FX is now
   ~0.2-0.5% of frame.
3. **Section backdrop in front of the cut (composition bug).** The backdrop normal
   was chosen before the camera side, putting the cream plane between camera and
   section in Amur (100% backdrop). Fixed by choosing the camera side once and
   handing the same normal to camera and backdrop.
4. **Invalid reef meshes.** Two-vertex "faces" in the reef fan triggered exporter
   warnings. Rebuilt as a clean triangle fan; zero mesh warnings on re-export.
5. **Camera framing.** Frame audits caught the survey boat cropped in overview,
   plan, approach and detail. Camera presets were recomputed and audited; boat and
   jetty are now fully inside every required view.
6. **Blown water highlights.** Water specular produced a large >0.9 luminance patch
   in the overview. Raised water roughness to 0.80; blown-pixel share is 0.00% in
   final stills.
7. **Globe locators.** Tunda was ~68 km off; all three replaced with place-board
   values and re-verified against the texture and exported marker nodes.

## Visual review method and remaining check

The session image guardrail prevented attaching rendered images to the chat. Every
shot was verified numerically (palette, saturation, edge density, blown-pixel share,
camera projection bounds, object coverage) and as disk review sheets:
`review/parity-sheet.png`, `review/before-after.png`, `review/runtime-parity.png` and
`work/runs/20261121T1445-local/proofs/look/kodingareng-look-contact-sheet.png`.

A human should still play the three films and the reel once and glance at the
contact sheets before publishing; that is the one review this run could not perform
as a human. Geometry placement, framing, palette and decode checks are evidence-backed.

## Limitations

- Illustrative terrain, seabed, section and prop placement; not surveyed.
- Section is vertically exaggerated and cropped; A/B continue beyond the frame.
- Water is a single alpha plane plus flat foam/ripple marks; no animated normals.
- The globe is a locator illustration, not a georeferenced data layer.
- App, gameplay and field workflow are not part of this package.

## Validation

Verdict: **pass**
(38 pass / 0 fail /
0 blocked). Failed item ids:
none.

| Check | State | Evidence |
|---|---|---|
| doc-start_here.md | pass | `START_HERE.md` |
| doc-handoff.md | pass | `HANDOFF.md` |
| doc-attribution.md | pass | `ATTRIBUTION.md` |
| inventory-sums | pass |  |
| inventory-clean | pass |  |
| manifest | pass | `runtime/asset-manifest.json` |
| manifest-no-private-paths | pass | `runtime/asset-manifest.json` |
| glb-runtime/globe/globe.glb | pass | `runtime/globe/globe.glb` |
| glb-runtime/kit/common-kit.glb | pass | `runtime/kit/common-kit.glb` |
| glb-runtime/coasts/kodingareng/coast.glb | pass | `runtime/coasts/kodingareng/coast.glb` |
| glb-runtime/coasts/kodingareng/section.glb | pass | `runtime/coasts/kodingareng/section.glb` |
| glb-runtime/coasts/tunda/coast.glb | pass | `runtime/coasts/tunda/coast.glb` |
| glb-runtime/coasts/tunda/section.glb | pass | `runtime/coasts/tunda/section.glb` |
| glb-runtime/coasts/amur/coast.glb | pass | `runtime/coasts/amur/coast.glb` |
| glb-runtime/coasts/amur/section.glb | pass | `runtime/coasts/amur/section.glb` |
| asset-globe | pass | `runtime/globe/globe.glb` |
| asset-kit | pass | `runtime/kit/common-kit.glb` |
| asset-coast_kodingareng | pass | `runtime/coasts/kodingareng/coast.glb` |
| asset-section_kodingareng | pass | `runtime/coasts/kodingareng/section.glb` |
| asset-coast_tunda | pass | `runtime/coasts/tunda/coast.glb` |
| asset-section_tunda | pass | `runtime/coasts/tunda/section.glb` |
| asset-coast_amur | pass | `runtime/coasts/amur/coast.glb` |
| asset-section_amur | pass | `runtime/coasts/amur/section.glb` |
| anchors-kodingareng | pass | `runtime/coasts/kodingareng/coast.glb`, `runtime/coasts/kodingareng/section.glb` |
| anchors-tunda | pass | `runtime/coasts/tunda/coast.glb`, `runtime/coasts/tunda/section.glb` |
| anchors-amur | pass | `runtime/coasts/amur/coast.glb`, `runtime/coasts/amur/section.glb` |
| camera-presets | pass | `runtime/asset-manifest.json` |
| clean-stills | pass | `media/coasts` |
| image-media/globe/globe-overview.png | pass | `media/globe/globe-overview.png` |
| image-media/kit/asset-sheet.png | pass | `media/kit/asset-sheet.png` |
| motion | pass | `media/coasts`, `media/coast-reel.mp4` |
| pitch-plates | pass | `media/pitch` |
| evidence | pass | `evidence/depth-case-verified.json` |
| review-review/before-after.png | pass | `review/before-after.png` |
| review-review/parity-sheet.png | pass | `review/parity-sheet.png` |
| review-review/runtime-parity.png | pass | `review/runtime-parity.png` |
| review-review/review-report.md | pass | `review/review-report.md` |
| editable-sources | pass | `source` |
