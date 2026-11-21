# Attribution and provenance

## Original art

All meshes, materials, cameras, sections, water treatments, marker designs and
rendered media in this package were authored for this revision in Blender 5.2.2 LTS
using procedural Python builders under `source/scripts/`. The art is original work
prepared for LAUTARA / *The Ocean Has Floors*.

## Third-party inputs

| Input | Use | Terms / note |
|---|---|---|
| Natural Earth 1:10m land, repainted as colour art (`earth-base-color.jpg`) | Globe surface texture | Public-domain Natural Earth base, repainted colour art supplied with the project. Packed into `globe.blend` and `globe.glb`. |
| Copernicus Marine GLORYS12V1 daily mean currents | Two numeric rows in the Kodingareng pitch plates and evidence fixture | Copernicus Marine Service product; values are modeled and are not local measurements. No data layer is baked into runtime geometry. |
| `Depth_case_verified.json` | Offline verified pair | Copied byte-for-byte from the project archive. |
| CityRT screenshots and the owner's finish reference | Visual direction only | Not shipped. Used for palette/legibility comparison; no pixels were copied into the art. |
| Place-reference boards (`references/places/`) | Geography and architecture cues | Links only; no images shipped. |
| Blender, FFmpeg, Pillow, Python | Production and verification tools | Their licences apply to the tools, not to this package. Font files are not shipped; text is rendered into pitch PNGs only. |

## Scientific attribution

- GLORYS12V1 `GLOBAL_MULTIYEAR_PHY_001_030`, daily mean, archived extraction
  `cmems_mod_glo_phy_my_0.083deg_P1D-m_202311`.
- The verified example is a modeled daily mean at a single ~9 km cell, not an
  observation. Daily averaging smooths within-day variation.
- Tunda coverage/timing and the Amur 2023 optical replay / 2007 field survey are
  separate evidence streams. No Tunda coverage polygon, plume extent or Amur measured
  profile is drawn into runtime art.

## Usage

The package is prepared for the LAUTARA teammate and project reviewers. Do not
represent illustrative terrain, section geometry or decorative markers as surveyed
or statutory boundaries. Keep the evidence fixture and pitch labels distinct from
clean runtime art.
