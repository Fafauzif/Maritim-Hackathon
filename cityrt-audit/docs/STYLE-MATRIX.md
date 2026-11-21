# CityRT style matrix

Nine "personalities" is the marketing claim; the shipped client registers **14** styles and
its building catalog ships **12 style buckets + `shared`** (824 buildings). Three registered
styles — `metropolis`, `british`, `brazil` — currently have **no catalog buildings**.
Every number below is measured or quoted; every gap is labelled.

## How each column was measured

| Column | Source | Method |
|---|---|---|
| Accent pair | `evidence/scripts/public/styles-EE7sSX4o.js` | shipped record `color` / `accent` |
| Scene palette | `analysis/palette/<style>.json` | 6-colour k-means over the 1200×800 official render |
| Scene luma / saturation | same | Rec. 709 luma and HSV saturation over that render |
| Buildings | `analysis/catalog/catalog-analysis.json` | count of catalog entries per style |
| Building luma / saturation / aspect | `analysis/catalog/catalog-summary.json` | masked building pixels over 824 studio renders |
| Vocabulary | same file | term frequency in shipped descriptions (Russian) |
| Shader / simulation | — | **not observed**: client is behind login |

Scene luma is lower than building luma for every style because scenes include ground, roofs
in shade and sky; compare columns within a row, not across the two methods.

## Registered styles

| # | Style | Key | Accent / secondary | Scene luma | Scene sat | Buildings | Building luma | Building sat | Silhouette aspect | Dominant vocabulary | Rendering notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | European | `european` | `#9A5541` / `#5F6670` | 117.8 | 0.25 | 139 | 142.7 | 0.28 | 1.19 | glass, brick, towers, lanterns | Mansard slate + cream limestone + red brick; dormers, chimneys, wrought iron |
| 2 | Japanese | `japanese` | `#C46686` / `#4E4640` | 139.2 | 0.20 | 50 | 153.8 | 0.21 | 1.25 | lanterns, glass, towers, wood | Blue tile roofs, machiya, 3D kanji signage, rooftop machinery |
| 3 | Slavic | `slavic` | `#B7684F` / `#6F8661` | 139.9 | 0.29 | 116 | 153.8 | 0.25 | 1.30 | glass, brick, towers, cornices | Izba carving, merchant brick, panel blocks, courtyard yards |
| 4 | Arabic | `arabic` | `#D4A27F` / `#3F7F86` | 149.6 | 0.30 | 47 | 169.6 | 0.27 | 1.24 | towers, domes, arcades, awnings | Whitewash/ochre, mashrabiya, riad courtyards, windcatchers |
| 5 | American | `american` | `#6A9BCC` / `#C0573F` | 127.1 | 0.30 | 112 | 142.4 | 0.26 | 1.38 | brick, porches, glass, towers | Porched suburbs, brick Main Street, Art Deco, glass towers |
| 6 | Italian | `italian` | `#CC785C` / `#6F8661` | 141.3 | 0.36 | 59 | 153.0 | 0.34 | 1.25 | glass, towers, domes, porticoes | Terracotta roofs, shutters, loggias, piazzas, campaniles |
| 7 | Scandinavian | `scandinavian` | `#788C5D` / `#5E7894` | 136.7 | 0.30 | 72 | 137.9 | 0.29 | 1.27 | wood (64), glass, towers | Painted timber, steep roofs, grass roofs, copper |
| 8 | Futurist | `futurist` | `#7FA8B8` / `#E9E4D8` | 146.9 | 0.20 | 50 | 184.4 | 0.17 | 1.23 | glass (58), towers, wood, domes | Brightest, least saturated style: white shells, rings, hanging gardens |
| 9 | Cyberpunk | `cyberpunk` | `#B4507E` / `#3FA7A0` | 88.6 | 0.21 | 52 | 99.9 | 0.21 | 1.16 | neon (50), towers, signs, glass | Only dark style (luma ≈100); emissive signage dominates; roof clutter |
| 10 | Fantasy | `fantasy` | `#6A5A8C` / `#D9A94E` | 109.5 | 0.33 | 38 | 135.4 | 0.32 | 1.05 | stone, towers, lanterns, Fachwerk | Crooked overhanging floors, cap roofs, glowing crystals |
| 11 | Medieval | `medieval` | `#8F3F34` / `#41618A` | 114.1 | 0.37 | 61 | 130.4 | 0.36 | 1.04 | towers (45), stone, wood, Fachwerk | Most saturated + most vertical: gables, spires, dormer rows, walls |
| 12 | Metropolis | `metropolis` | `#3D5A78` / `#D4AF6A` | 134.0 | 0.20 | **0** | — | — | — | none shipped | Style record + hero render only; no buildings in catalog |
| 13 | British | `british` | `#9C4A36` / `#1F3A5F` | 142.4 | 0.31 | **0** | — | — | — | none shipped | Style record + hero render only; no buildings in catalog |
| 14 | Brazil | `brazil` | `#E2B04A` / `#2F5FA8` | 141.1 | 0.34 | **0** | — | — | — | none shipped | Style record + hero render only; no buildings in catalog |
| — | Shared | `shared` | — | — | — | 28 | 145.1 | 0.25 | 1.28 | towers, brick, panels | Utilities/industry shared across styles (15 util, 7 ind) |

## Catalog composition

| Bucket | Count |
|---|---|
| Shops / services (`com`) | 235 |
| Residential (`res`) | 153 |
| Industry (`ind`) | 100 |
| Services (`svc`) | 97 |
| Landmarks (`land`) | 91 |
| Parks (`parks`) | 66 |
| Offices (`off`) | 65 |
| Utilities (`util`) | 17 |
| **Total** | **824** |

Notable: `com` outnumbers `res` more than 3:2 in the shipped catalog, and landmarks + parks
(157) outnumber offices (65). A CityRT-looking city is retail- and civic-heavy, not a
residential dormitory.

## Map skins (landscape overrides)

Ten "coverings" recolor grass, leaves, soil, water, sky and apply a desaturation factor.
These are *not* city styles — they are map moods and they stack on top of a style.

| Skin | Desaturate | Signature colours |
|---|---|---|
| `meadow` | — | grass `#86AC6E` `#96B676` |
| `tropics` | 0.05 | brightest water `#6CD2C6`, sky `#8EC3E6` |
| `sakura` | 0.05 | pink leaves `#C47C98` `#D292AA` |
| `autumn` | 0.15 | leaf `#A8603F` `#BC8A4C`, sky `#B4BFD0` `#F2DDC2` |
| `desert` | 0.20 | sand grass `#C4B49A`, teal water `#86CFC6` |
| `fairy` | 0.25 | violet soil `#C2B2CE`, pink-gold leaf `#C98C9E` `#D2A85A` |
| `tundra` | 0.35 | grey-green grass `#748E80`, steel water `#45708E` |
| `mars` | 0.55 | rust soil `#B89A80`, dusty sky `#C49C80` |
| `moon` | 1.00 | neutral greys `#959BA8`, near-black sky `#252A40` |
| `blueprint` | 1.00 | monochrome blue `#4A6A91`, deep water `#1E3150` |

## What this matrix cannot tell you

- Any shader, light rig, post-processing or material parameter (client behind login).
- Simulation pacing, camera limits, day/night cycle.
- Whether the 14 registered styles map to a nine-style in-game picker, and how the three
  building-less styles are meant to be played.
