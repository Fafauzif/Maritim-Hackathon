# Earth globe art starter

`earth-base-color.jpg` is a 4096 × 2048 sRGB equirectangular texture of Earth. Recognizable continent shapes are the geography. The teal water, sandy land, and coast accents are painted color choices. The map carries zero location markers, political borders, labels, elevation, bathymetry, or imagery tiles. Shading at the coastline is decorative and should stay out of any scientific display. Scale is appropriate for the world view, with each local coastline modeled from its own visual references.

## Put it on a globe

- The image's left edge is −180° longitude, its right edge is +180°. North is at the top.
- Set `U = (lon + 180)/360` and `V = (lat + 90)/180` on the mesh. Blender's V increases upward. UV seams should split per face at the antimeridian, on the −X side. Avoid using generated coordinates as a UV substitute.
- For a sphere of radius R and geographic longitude λ, latitude φ in radians, set `XYZ = R × (cos φ cos λ, cos φ sin λ, sin φ)`. The northern pole is +Z and 0° longitude is on +X. 90° east is on +Y. Position globe locators with this same mapping and a small positive height above the sphere. Keep globe coordinates separate from the local coast meshes.
- Use a Principled BSDF with the image linked to Base Color. Keep the texture set to sRGB and the color grain subtle under your lighting. No external geoservices are required.

`make_globe_seed.py` is optional. It saves a fresh editable sphere with explicit UVs, a packed image, initial lights, and a camera looking toward the western Pacific. Set the final globe presentation after reviewing the three coasts. From the project root, replace the example command or executable with your installed Blender path when needed.

```powershell
blender -b --factory-startup --python-exit-code 1 --python "3d-art/references/globe/make_globe_seed.py" -- --radius 10 --output "3d-art/work/globe-seed.blend"
```

The script accepts a new output path only. Use the seed as a working scene or append its globe mesh and packed material to another file. The number 10 is a convenient Blender scene radius, with no real-world units implied. Use a separate focused preview or cut when moving from globe scale to local coast scale.

## Source and use

Made with Natural Earth. Its public-domain **1:10m Land** layer is already cited in the LAUTARA research pack. The image here was repainted using the land outlines in that pack's `root/natural_earth_land.geojson`. The ZIP includes just the color art and generator for the Blender scene. Shape checks sampled North America, Eurasia, South America, Australia, Antarctica and two oceans. The texture wraps the antimeridian and places the northern hemisphere at the top. Public release may include this texture with the source credit below. Keep the credit with derived export art.

- [Natural Earth 1:10m Land](https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/)
- [Natural Earth public-domain terms](https://www.naturalearthdata.com/about/terms-of-use/)

`earth-seed-preview.jpg` shows the optional seed from a local Blender 4.3.2 smoke render. The check verified outward-facing polygons, antimeridian UV split, longitude axes and texture packing. Run the project preflight on the target system before rendering the production globe.
