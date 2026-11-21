# LAUTARA - 3D art handoff v2

**The Ocean Has Floors** - engine-neutral coastal art for the officer's map, section
and field brief. This package is art, not app or gameplay logic. The app, data wiring,
field workflow and game behaviour belong to the implementation teammate.

- Revision: **v2**
- Blender source: **5.2.2 LTS**
- Base commit: `e07093ef34118bc3e686257accbbfe6246595153`
- Build ID: `20261121T1445-local`
- Date: 2026-11-21
- Units: **metres**; waterline at **Y = 0** in glTF
- Runtime format: **glTF 2.0 binary (GLB), embedded, no cameras or lights**
- Primary runtime budget: coast <= 6 MiB, section <= 3 MiB, kit <= 4 MiB, globe <= 8 MiB

## 30-second import

1. Read `runtime/asset-manifest.json`. It is the only source of paths, transforms,
   camera presets and locator metadata.
2. Load `runtime/coasts/kodingareng/coast.glb` (or Tunda / Amur) as one scene root.
3. Place the root at the origin. Do **not** normalise or centre individual children:
   the scene already has an authored origin and a waterline at Y = 0.
4. To show the cutaway, hide the coast root and load the matching `section.glb`.
   Both files share the same origin and the same `SECTION_A` / `SECTION_B` nodes.
5. Frame with a preset from `sites.<site>.cameras`; do not infer a camera from the
   bounding box. `COAST_OVERVIEW` is the intended first view.
6. For the globe, load `runtime/globe/globe.glb` on its own normalised art radius
   (10 units). Never share a transform with a coast.

```js
// Framework-neutral outline; the same steps apply in Unity, Godot or a viewer.
const manifest = await (await fetch('runtime/asset-manifest.json')).json();
const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
const loader = new GLTFLoader();
const coast = await loader.loadAsync('runtime/coasts/kodingareng/coast.glb');
scene.add(coast.scene);                       // origin is authored; do not recentre
const cam = manifest.sites.kodingareng.cameras.COAST_OVERVIEW;
applyPreset(camera, cam);                     // position/target/up, verticalFovDeg
```

## What to load, and when

| Need | File | Notes |
|---|---|---|
| Opening map | `runtime/coasts/<site>/coast.glb` | one site at a time; independent `ENV_Water` |
| Cutaway | `runtime/coasts/<site>/section.glb` | mutually exclusive with the coast |
| Earth view | `runtime/globe/globe.glb` | normalised radius; markers `ANCHOR_*` |
| Reusable parts | `runtime/kit/common-kit.glb` | optional; components listed in `kit.components` |
| Case story | `media/pitch/*.png` | presentation only; never bake into runtime art |
| Field evidence | `evidence/depth-case-verified.json` | numbers, not geometry |

## Axes, scale and nodes

- Blender source: +X east, +Y north, +Z up; waterline Z = 0; 1 unit = 1 m.
- glTF: +X east, +Y up, -Z north. Maps Blender `[x, y, z]` -> glTF `[x, z, -y]`.
- Every coast and section carries these named empties: `COAST_ORIGIN`, `ORBIT_SITE`,
  `ORBIT_WATERFRONT`, `TARGET_SURVEY`, `ANCHOR_JETTY`, `ANCHOR_VESSEL`,
  `SECTION_A`, `SECTION_B`.
- Water nodes: `ENV_Water` (coast) and `SECTION_Water` (section), separate and
  independently selectable.
- Coast/section node IDs are unique inside each asset. Node names are stable.

## Camera presets

`asset-manifest.json` stores `position`, `target`, `up`, `near`, `far`, `aspect`,
`projection` and either `verticalFovDeg` (perspective) or `orthoWidthM`
(orthographic), all in glTF coordinates. Use the vertical FOV and crop horizontally
for narrower containers; keep the authored aspect for final stills.

## Water and the section

- Coast water is a single `ENV_Water` mesh at Y = 0 with an alpha-blended material.
  If the target renderer sorts alpha badly, replace it with an opaque material using
  the same node name; the authored shallow shelf, foam line and ripple marks remain.
- Section water is `SECTION_Water`. The section is **illustrative** and uses
  **x3.2 vertical
  exaggeration** for Kodingareng (see manifest per site), pivoted at Y = 0. It is not
  surveyed bathymetry.
- Show either the coast or its section, not both with overlapping terrain/water.

## Globe locators

| Site | WGS84 | Node |
|---|---|---|
| Kodingareng Lompo | -5.14905 deg, 119.26473 deg | `ANCHOR_kodingareng` |
| Pulau Tunda | -5.81151 deg, 106.27811 deg | `ANCHOR_tunda` |
| Razdolnaya mouth | 43.32556 deg, 131.80778 deg | `ANCHOR_amur` |

These are globe locators from the project place board. They are not scene transforms
and they are not a georeferencing claim.

## Evidence and pitch discipline

Runtime art and clean stills contain **no evidence figures, arrows, labels, statutory
boundaries or field quantities**. The two Kodingareng comparison plates and the
section explanation live only in `media/pitch/` and are labelled as modeled regional
data. The model cell is a ~9 km GLORYS12 cell; its mean vectors are not a local
measurement and must not be attached to an unrelated illustrative bed.

## Verified build

- 8 GLBs exported and re-imported in fresh Blender processes.
- 5 editable `.blend` sources reopen packed.
- 15 coast stills at 3840x2160, 3 travel films at 1080p/24, 27 s reel.
- Validation: **38 pass / 0 fail**
  (pass).
- See `review/review-report.md` for measured evidence and known limits.

## What the engineer integrates next

1. Wire the station/date/depth state to the coast + section assets and camera presets.
2. Keep viewing depth and proposed sample depth as separate state.
3. Use `evidence/depth-case-verified.json` for the two source rows.
4. Replace or hide the illustrative water if the renderer's alpha policy requires it.
5. Use the globe anchors for the case locator; keep them separate from scene origin.
6. Run the acceptance checks in `HANDOFF.md` before shipping.
