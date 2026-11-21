# Cameras, travel and the ocean section

## The experience to prove inside Blender

Build a recognizable Earth with real continent outlines and three geographic site markers. Move into a regional view, transition to a coastal scene at the selected site, and continue navigating from above. At close range, lower the view to inspect the waterfront or reveal the water column while still recognizing the boat and shore. This is an authored Blender scene and camera demonstration. The same model files should support manual orbit, pan and zoom in Blender. Jump points and local view targets are objects, camera presets, or timeline markers.

A route travels at several scales:

| Scale | Viewer sees | Motion and framing |
|---|---|---|
| Earth | A real Earth silhouette on a sphere with place markers. Indonesia versus the Russian Far East is obvious when the globe rotates. | Orbit or smoothly recenter each marker. Use a clearly lit daylight limb, forgiving shadows, and readable coast silhouettes with labels in an optional render layer. |
| Region | Enough context to recognize the geography of Indonesia or the northern Sea of Japan before arriving at a named coast. | Approach using a camera aimed at the site's outward normal. Place names can identify the site in the globe proof. Separate close Indonesian pins with regional labels or framed callouts. Avoid fictional boundaries. |
| Coast overview | A broad bird's-eye view with coast edge, neighboring land where useful, local settlement/bank forms, jetty or landmark and survey vessel. | Give a broad viewing angle and enough space to navigate visibly around the shoreline. Use the same intent and scale class for all three coasts. |
| Waterfront approach | The same identifiable coast at mid-distance, with the boat, landing and land textures and building scales readable. | Tilt down gently while pushing closer. Target a fixed point tied to the local boat/land relationship. Show a short orbit or lateral movement at this scale to demonstrate geometry depth. |
| Section | An A–B plane through the same region, showing the water surface and illustrative bed. The viewer recognizes fixed land and boat anchors. | Ease around the section axis or switch to a matched section camera. Show a clear cutaway with the surface height fixed in the scene. Remaining overhead context anchors the depth reveal. |

The Earth is a globe visual only. Use a documented world-scale reference silhouette and a simple spherical projection. Keep oceans and land visually distinct, favor a common color palette and use an inset/close view for place identity. Leave legal boundaries, GIS infrastructure, bathymetry, model values, vessel positions from records, case data, and source retrieval pipelines outside this run.

## Scale and coordinates

- **Local coordinates:** Blender units in meters. Use +X east, +Y north and +Z up. Set the illustrative horizontal water surface at Z = 0. Keep local geometry close to its scene origin. Adopt the geographic center in the approved place reference as the indicative globe locator. This anchors north and broad position. Project scene anchors remain artistic local placement.
- **Globe coordinates:** use a separate scene scaled for comfortable viewport clipping (radius of roughly 10 Blender units as a starting choice). Use orientation +Z north, longitude 0° on +X and longitude +90° on +Y. For longitude `λ` and latitude `φ` in radians, a marker on the surface is `R*(cos φ cos λ, cos φ sin λ, sin φ)`. Lower negative latitudes belong below the equator. Positive eastern longitudes orbit past +Y from Greenwich. Stems sit just above the shell.
- **Orientation check:** verify a northern hemisphere point, an Indonesian point south of the equator, an eastern longitude marker, and the position of the globe texture or geometry against the same convention. For a north-up regional view, project global +Z onto the plane at the surface marker, with a stable fallback near poles. Keep geographic orientation understandable on entry to each coast.
- **Travel across scales:** use separate globe and local scene camera rigs. Match coast placement and approximate heading across the edit. Scale change can use a brief graphic dissolve, a cut on continuing motion, or an edited shift justified by a montage. Underlay textures, continent outlines and local meshes represent different detail levels. Set each rig’s coordinate range to the world it frames.
- **Local navigation:** give each coast named `ORBIT_SITE`, `ORBIT_WATERFRONT`, and `TARGET_SURVEY` empties with visible positions useful for framing. Permit roll-free camera orientation to those targets. Define a safely explored viewing area so the viewport starts in a strong composed view and supports natural zoom or panning without immediately clipping into the shore, showing empty edges or falling through geometry.
- **Camera limits:** calibrate clip start/end in local units according to scene extents, then inspect shadow quality, horizon and section edges. Check clipping and the focal point in the highest specified proof-resolution frame. Use a larger separate clip range for the globe. Blender camera settings reference: https://docs.blender.org/manual/en/latest/render/cameras.html

## Logical camera coverage

These names describe shot roles. Follow the main prompt's exact output and filenames. Lens lengths are proposed starting points for the coastal scenes.

| Camera | Initial setup | Accept when |
|---|---|---|
| `GLOBE_HOME` | Slight perspective with an Earth-scale orbit target. Start wide and feature both relevant areas across the shot. | Earth looks round and recognizable when shrunk. Marker placement, local roll, labels and daylit focus make sense. |
| `GLOBE_REGION` | Stable north-up or mildly rotated view aimed at each selected region. | Indonesian sites resolve separately if shown together. The Russian marker lands at the northern bay instead of central Vladivostok. |
| `COAST_OVERVIEW` | High oblique, roughly 50–65° above horizon. Try 50–70 mm perspective with a 36 mm sensor. Pull back with a longer lens to preserve the proportions of the dock and houses. Start with a north-up composition and introduce modest azimuth offset only if necessary. | The image reads from top to bottom as a place one can explore. Boat, landing or bank, land silhouette and open water survive a low-resolution preview. |
| `COAST_PLAN` | Orthographic near-nadir or exactly nadir north-up. Set orientation explicitly to east horizontal +right. Include the same reference indices in working markup across cameras. | Recognizable outline, same anchor positions, and enough margin for viewing and potential overlays. |
| `COAST_APPROACH` | 25–40° down, medium focal length. Move closer to the boat and landing without losing the coast context. | Roof, dock and vessel have believable scale. A short lateral move reveals parallax and maintains a sensible horizon. |
| `COAST_SECTION` | Align side view into the vertical plane defined by A–B, looking approximately perpendicular to the horizontal A–B direction with a small overhead offset when useful. Match the relative position of key anchors to the approach or overhead view. | The cut face, water surface, bed, descent and boat all read. The selected cut has a corresponding position in the overview proof. |
| `COAST_DETAIL` | Lower mid-range angle toward one distinctive local feature. | Local materials and workmanship explain how this shore is used. |

In preview playback start with roughly 1–2 seconds to settle at each important position, and approximately 2–4 seconds per dramatic transition. Use ease in/ease out on the position and target together. Avoid overshoot and tie camera roll to a stable up reference. Inspect the viewport or animatic at key frames and midpoints. Camera movement should maintain context and demonstrate navigability. Reserve pacing and polish for reaching places and discovering the cutaway, with a quiet hold at the reveal.

## Section construction

1. Place A and B as fixed local empties that define the vertical plane. Choose a line that intersects the target under the boat and keeps an identifiable land anchor on the retained side. Store route/story annotations separately from any export geometry.
2. Duplicate only the necessary land/water context into a section view or use non-destructive collection/view-layer controls. Clip or slice the illustrative solid bed mesh along A–B. Add a clean cap with a distinctive material. Keep original terrain available in the other views. Preserve the water plane at Z = 0 throughout.
3. Construct a clear underwater volume between the illustrative bed and the surface. Prefer a small number of clear contour shapes and shallow-to-deep color changes. Provide a lightly colored infill or visible section edge instead of obscuring the boat and bed in an opaque blue mass. Use compositor or render-only transparency as required. Test the silhouette with the volume temporarily hidden, and inspect for z-fighting, loose Boolean faces, transparent sorting and glare.
4. Use a simple cable, lowered instrument, and visual layer positions when needed to explain inspection at depth. Keep the instrument meaningful at close range. Keep station data and numerical overlays out of the authoring scene. A clean layer and an explanatory storyboard may share the same camera.
5. Configure a short reveal using a view-layer switch/timed wipe, a single moving masking plane, layered model visibility, or a matched shot edit. Coastline and boat positions stay fixed. Compare screenshots from both sides by pointing to the same boat and dry land feature. Show an illustrative section description in accompanying docs. The illustrative seabed communicates the spatial idea.
6. Keep clear export boundaries. The environment mesh, simplified water, survey kit and any approved illustrative section mesh have independent names and pivots. Store Blender view-layer arrangements, camera rigs and reveal effects with the editable authoring file. Exported GLBs follow the agreed material/validation rules.

## Review and parity checklist

- [ ] Each site has the same useful camera set and comparably polished 4K proof frames.
- [ ] Each location opens overhead. Nearby land and water remain visible before a camera move.
- [ ] A viewer can travel from Earth to a region and into each coast in the Blender camera demonstration, then inspect the place by panning and orbiting in Blender.
- [ ] Landmarks, boat and water surface line up in the before/after cutaway. Section position can be pointed out on the plan.
- [ ] Earth and globe locators are correctly oriented against references. Local scenes identify real places and keep stylization legible.
- [ ] Geography and scene IDs match the reference board, including the distinction between Kodingareng Lompo and Keke.
- [ ] Any mismatched shadows, motion clipping or camera-signature changes have been checked across regular and cutaway renders. Results are documented alongside the shot files.
