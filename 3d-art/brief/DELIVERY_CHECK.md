# Check the Blender delivery

From the parent project folder, use a regular Python 3.9+ installation.

```sh
python 3d-art/tools/check_delivery.py 3d-art/output
```

On Windows, `py -3` works in place of `python` when the Python launcher is available. The script defaults to the `output` folder beside the rest of this pack. To check another run, pass that run's output folder. Add `--json` for a detailed per-file record. An exit code of 1 identifies an incomplete or malformed delivery.

The script expects 33 files. It checks that all three coasts have the same named deliverables, the globe and all nine coastal stills are 3840 × 2160, and the two contact sheets have valid PNG structure. It verifies PNG chunk checksums, MP4 container bounds, GLB 2.0 headers and chunk bounds, embedded-resource references, mesh presence, binary buffer and buffer-view ranges, and that each review file has readable text. It reports any cameras and punctual lights in each GLB. Extras metadata may contain reference URLs. Keep the actual meshes and textures self-contained. Only the required paths are checked.

## Check the result in Blender

File checks cover structure and completeness. Open each saved `.blend` and import each `.glb` in a fresh scene to check appearance, geometry, maps, scale and orientation. Reopening an older file with the source scene still present does not test the export. A complete delivery includes the following review work.

1. **Open from disk.** Verify that scenes and linked assets resolve under the project's art folder. Confirm portable assets pack required images or use documented relative paths. Check renders for missing materials and outlines. Review the globe and all three coasts.
2. **Review the same frame sizes.** Put each coast's god view, map view and section in the corresponding row of the parity sheet. Inspect both at thumbnail size and 100%. Judge each coast on silhouette, focal hierarchy, distinctive place cues, color and light, and polish at the waterline.
3. **Test the moves.** Scrub each travel clip for pan, orbit, approach and overhead-to-section continuity. The boat and jetty should stay anchored through the camera change. Play the full reel and check its cuts, black frames and playback. A camera handoff between globe and local scene should preserve direction and place.
4. **Compare the GLBs.** Check axes, units, front/back surfaces, material names and visibly missing objects. Inspect the export camera/light counts and document any deliberate inclusion. Export-friendly water can look simpler. Compare the portable version deliberately and record any material behavior that depends on Blender.
5. **Review the limits.** Confirm every section depicts an illustrative seabed. Journal local reference evidence and artistic decisions so someone reopening the scene knows which features vary from reality. Label image inspection as human or model-based and record unverified checks in `output/review/deviations.md`.
