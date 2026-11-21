# Earth and camera travel

## Source ladder

| ID | Source | What to borrow | Reuse |
|---|---|---|---|
| GL-01 | [Bilawal Sidhu's God's Eye View](https://github.com/bilawalsidhu/gods-eye-view) | The legible progression from whole planet to a named place you can approach. Compare rhythm, scale change, and continuity of the camera. | Link only for the visual benchmark. Repository code licensing and third-party media rights differ. No tile data or example footage enters this pack. |
| GL-02 | [Natural Earth terms and source](https://www.naturalearthdata.com/about/terms-of-use/) | A geographically real continent/large-island outline for the stylized Earth. Open the credit sheet with the supplied offline globe texture for its exact source and processing. | Provider publishes its map data in the public domain. Credit for this project: Made with Natural Earth. |
| GL-03 | [NASA Earth Observatory, Blue Marble Next Generation base map](https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/base-map/) and [July global 2:1 JPEG](https://assets.science.nasa.gov/content/dam/science/esd/eo/images/bmng/bmng-base/july/world.200407.3x5400x2700.jpg) | Optional natural-color visual reference or separate globe material variant. Study coast recognition, ocean roughness, and land/water separation. The supplied offline art is the primary input. | [NASA Earth image FAQ](https://science.nasa.gov/earth/faq/) and [image use guidance](https://www.nasa.gov/nasa-brand-center/images-and-media/). Credit NASA Earth Observatory, Blue Marble Next Generation, July 2004. Leave the NASA marks out of the render. |

## Shot language

1. Begin in a readable Asia-Pacific three-quarter view. Three clean place locators are enough. Use separate Blender empties for the place locators. Give Tunda and Lompo staggered labels or leaders when they would overlap. Control horizon falloff so the land/water silhouette remains readable without a strong atmosphere bloom.
2. Use one deliberate approach shot per coast. Orient the planet toward the selected place, then hold the shot long enough for a viewer to read a reference land shape. At an altitude where the offline texture stops resolving coastline detail, cut or dissolve to the local high-oblique scene. Preserve coast direction and screen position at the cut.
3. In the local scene, prevent confusion about camera controls with three useful views from the same coast: contextual oblique, near top-down inspection, and a cutaway around an authored line. The boat and landing act as spatial anchors. A dolly/orbit or set of saved cameras can demonstrate the proposed feel of moving around. Express the globe-to-coast progression with Blender cameras and frames.
4. Keep Earth materials independent of local art. A globe texture covers the planet; it does not place individual roofs, reefs or jetties. The local coast and illustrative seabed are separately authored, so view transitions should read as an intentional change of scale without implying uninterrupted geographic fidelity.

**Review frame:** Without either country in large display text, can you recognize the Earth, find the chosen coast after focus changes, and still understand where the operator is on arrival? Correct marker orientation, camera staging and landmark placement first.

## Globe locator defaults

Use latitude and longitude in degrees. These approximate art/navigation pins come from the existing project references. They mark places at global scale and do not fix the local scene origin, model an event, or locate a survey station.

| Scene folder | Label | Latitude | Longitude | Source |
|---|---|---:|---:|---|
| `kodingareng` | Kodingareng Lompo | −5.14905 | 119.26473 | Existing LAUTARA diagnostic, Fig. 1 island anchor. [Mapcarta](https://mapcarta.com/16118912) |
| `tunda` | Pulau Tunda | −5.81151 | 106.27811 | Existing LAUTARA diagnostic, Fig. 1 island anchor. [Wargasara tourism listing](https://jadesta.kemenpar.go.id/desa/pulau_tunda) |
| `amur` | Razdolnaya / Amur Bay | 43.32556 | 131.80778 | Existing Amur replay, river-mouth anchor. [Wikidata Q111852](https://www.wikidata.org/wiki/Q111852) |

In the Earth-opening shot, distinguish the two Indonesian markers with short offset leaders or a dedicated regional view. Verify the latitude sign visually before recording travel.
