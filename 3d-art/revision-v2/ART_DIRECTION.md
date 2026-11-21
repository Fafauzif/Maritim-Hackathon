# Art direction · illustrated coastal miniature

## Reference and visual target

Open `references/CityRT_Cartoon_Finish_User_Reference.png` beside the two reference sheets in `3d-art/references/cityrt/`. The latest shot shows soft charcoal outlines at roof overlaps, structured façades, muted warm walls against cool roofs, trees built from rounded masses, light wash across flat surfaces and sparse white marks on calm water. It shows enough façades to read architecture in depth. Translate these properties into the three coastal settings with original shapes and colours. Pagoda architecture, pink blossom landscaping, reference text and UI belong to the reference image. Use the local place boards for geography and architecture.

| Apply | How to judge it |
|---|---|
| Silhouette first | Shape roofs, overhangs, stilts, bridge rails, boat cabin and foliage volumes before adding surface detail. Roof lines and building shadows remain distinct in a 320 px overview. |
| Light contour | Test restrained charcoal around silhouettes and selected creases in Blender, with natural separation from geometry in GLB. Thin edges stay visible without shimmer or haloes. Use trim meshes where they earn their keep and survive reduction. |
| Local matte palette | Warm plaster and wood, distinct local roof families, two or three vegetation values, calm blue-to-teal or low-saturation estuary water. Prefer controlled transitions and selective colour accents. |
| Readable ground plan | Set lanes and shore access before populating buildings. Orient façades to frontages. Preserve open space by design, with a distinct path to the landing and intelligible plazas, yards or marsh edges. |
| Subtle water | Use simple shoreline bands, a small number of original graphic ripple marks and coherent height. Keep overlay zones quiet. Evaluate horizon-free overview and a low viewing angle to catch alpha sorting. |
| Shadows and depth | Keep a common daylight family. Use soft contact and rim separation for buildings and boats. Water, cliff face and seabed retain a value hierarchy in section. |

Compare three matched Kodingareng stills before full production. A uses shaped geometry and matte light. B adds a light contour. C adds a restrained wash and slightly stronger contact shadows. Include one high-oblique orthographic view and the existing perspective framing side by side. Start testing around 38–45° down from horizontal, then test a steeper operational angle if the water or site layout is hard to read. Pick the strongest evidence and write a reusable look recipe. Aggregate palette distance from an Italian street preview is diagnostic, since the area covered by coast, water and buildings differs.

## Site direction and physical continuity

| Site | Composition | Signature assets and repairs |
|---|---|---|
| **Kodingareng Lompo** | Low, compact Indonesian island, dense roof pockets and a connected route from village to jetty. Reserve generous offshore space for the officer. | Distinct stilt and on-grade houses, a recognizable landing shelter, alternating roof families, coherent lane material and shallow band. Re-site the survey and local boats after full draft clearance tests. Keep the same visual survey boat in the living scene and section. |
| **Pulau Tunda** | Greener island with differentiated edges, coastline bends and a sheltered landing. The view should read as Tunda even beside Kodingareng. | Break up vegetation into coherent shore and inland patches. Use a compact landing cluster and varied local roof/timber accents. Refit the beach access and jetty to the actual authored slope. Keep case overlays separate for the coverage/provenance story. |
| **Razdolnaya / Amur Bay** | A broad river-to-bay meeting with low floodplain and asymmetric marsh banks. Keep the estuary dominant and make the accessible landing visible. | Build wetland bands, textured shore profiles and a more readable compact working landing. Use subdued timber/brick, low service buildings, cool roofs and reeds appropriate to the place boards. Add a deliberate route to the landing before filling nearby space. |

Test each full boat footprint on the final evaluated surface using draft, waterline and nearest shoreline distance. Sample along the route from dry lane to deck, along the rail and under pier supports. Record clearance failures and before/after coordinates, repair first, then regenerate nearby camera targets. For houses, use actual rotated footprint polygons, access on an authored lane, height samples at bases, and dry ground unless physically modeled as stilt foundations. Inspect for intersection, unsupported steps, accidental coplanar surfaces, z-fighting and visually misleading depth.

## Camera and section standard

| View | Delivery goal |
|---|---|
| `COAST_OVERVIEW` → `godview.png` | Bird’s-eye with roof and façade depth, boat and landing visible, room for overlays, little or no horizon. Save an orbitable starting position. |
| `COAST_PLAN` → `mapview.png` | North-up exact nadir, stable extents, water margin and deliberate empty overlay region. |
| `COAST_APPROACH` → `approach.png` | Waterfront approach with a route and multiple silhouettes visible. |
| `COAST_DETAIL` → `detail.png` | Show crafted boat, jetty and architecture; retain enough context to identify the scene. |
| `COAST_SECTION` → `section.png` | Look squarely along the normal of the A-to-B vertical cut. Show both section directions clearly in the manifest, recognizable boat and landmark, an uninterrupted waterline and enough bed to interpret the illustration. |
| `TRAVEL_CAM` → `travel.mp4` | Ease from overview through approach and lateral parallax, settle into a landmark-registered cutaway. Retain the edit and rigs in the editable source. |

Build the section from the revised coast height field and its A–B line. Give the cut solid topology, close wet and dry intervals at exact shore intersections, and avoid zero-area overlapping layers. Preserve a shared horizontal frame. Put vertical exaggeration in the visual section geometry only, keep its waterline and named landmark transforms verifiable, and record the factor and pivot (default waterline Z=0) in the manifest. Start by testing the v1 factors of 4.0, 4.0, and 3.4 and choose the smallest factor that reads. Prefer fresh framing, surface contrast and section lighting before increasing exaggeration.

## Scientific and geographic boundaries

- **Globe locator defaults** from `3d-art/references/places/Earth_and_Camera_Travel.md`, WGS84 lat, lon in degrees. Kodingareng Lompo **−5.14905, 119.26473**. Tunda **−5.81151, 106.27811**. Razdolnaya **43.32556, 131.80778**. The model cell, field station and decorative local origin have different meanings. Correct the three pins and all related cameras and media. Avoid claiming globe and illustrative scenes share a geographic transform.
- **Kodingareng opening pair** from `references/Depth_case_verified.json`. The regional GLORYS12 daily modeled mean for **2020-04-16 UTC** comes from one approximately 9 km cell at roughly **−5.1666665, 119.2500**. At **0.494 m**, speed **0.093 m/s** and bearing **264° toward**, roughly west. At **9.573 m**, **0.074 m/s**, **45° toward**, northeast. Bearings are clockwise from north. Round only display values. Fix visual camera, waterline, background pixels and model location across the two pitch states. Place the pair in a labeled regional data inset, since the model level reaches below the v1 local illustrative bed of about 7.6 m. A single native model cell supplies a single vector per depth, with no interpolated reef-level arrow field.
- **S-01** is the illustrative proposed sampling station at **−5.1550, 119.2620** WGS84. A decorative boat target is a local art anchor. A disputed reported extraction coordinate is a separate location with unresolved provenance. Separate the site locator, regional current estimate, proposal and illustrative shore. Render the field method only as an illustration. A profiler measures current, and bottles provide sediment samples. Actual safe depth and method need local field confirmation.
- **Tunda** is the coverage and timing comparison. Context cites 26 Oct 2023 broad-screen pass of 95.3% in the island ring and 75.8% in the west archived reef portion against a 90% decision threshold. The Oct 27 inspection, source allegation and missing scoped acquisition each have their own evidence. Keep water styling neutral with no inferred sediment, vessel track or confirmed extraction polygon.
- **Amur** is a different estuary and a comparison for alternate pathways and survey design. The 2023 optical replay and the 2007 field survey have separate roles and time periods. Keep them distinct. Preserve the project’s scientific appendices and treat terrain, apparent depth, props and section as illustrative.
- **App boundary.** Runtime geometry and clean stills carry no evidence figures, arrows, UI, statutory or surveyed boundaries. Deliver two separately annotated Kodingareng comparison PNGs plus a section explanation figure in `media/pitch/`. Label the imagery and identify which values are from the model. The 22–30 s art reel is a pitch asset. The official opening submission video in the master context has its own 2–5 minute English requirement.
