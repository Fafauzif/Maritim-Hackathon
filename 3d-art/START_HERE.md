# The Ocean Has Floors · Blender production handoff

**Extract at the root of your completed REA project.** The resulting layout should be:

```text
your-project/
  cityrt-audit/              existing REA results, read in place
  3d-art/                    everything in this ZIP
    DSH_START_PROMPT.md
    prompts/
    brief/
    references/
    tools/
    work/                    DSH creates this for drafts, scripts and logs
    output/                  DSH creates this for delivery
```

1. Let the REA audit finish. Start a new DSH session in the **same project** with Blender MCP available and Blender open. Save any other work before beginning. Keep the REA project present where the harness can read it.
2. Copy the text of **DSH_START_PROMPT.md** into the harness, or give it this one-liner from the project root:

   > Read and execute 3d-art/DSH_START_PROMPT.md. Use my finished CityRT REA audit in this project, discover my actual Blender MCP tools, and complete the three-coast Blender art run. Start with preflight and continue through renders and exports.

3. Inspect the first equal-status contact sheet at `3d-art/work/reviews/blockout-parity.png`. You can steer the look at this stage. After an interruption, paste `prompts/90-resume.md`. Each phase has a paste-ready standalone prompt. Open named camera presets or timeline markers to jump between prebuilt views.
4. Finished work belongs at `3d-art/output/`. For the view from above, start with `globe/globe-overview.png` and `coast-reel.mp4`. Open any `coasts/<site>/scene.blend` and use the saved perspective or press Numpad 0 for the active render camera. Escape camera view or orbit in the viewport to explore freely inside Blender. Camera names and colors are documented in the handoff.

## What this produces

Three equally polished worlds: **Kodingareng Lompo**, **Pulau Tunda**, and **Razdolnaya / northern Amur Bay**. Each gets a god’s-eye render, a north-up map view, a matching underwater cutaway, a short camera flight, an editable scene, and a GLB. A real-outline Earth overview and a connected reel show how you get from planet scale to these places. There is also an editable prop and material kit.

Real locations guide the silhouette and prominent visible features. The underwater terrain and sampling props are illustrative. The production run uses Blender 5.2.2 and Blender MCP; your RTX 4060 Laptop GPU has 8 GB VRAM. The Blender files, short films, material tests and GLBs are the run’s destinations. The ZIP itself is the production kit.

## Which references to read

- **Style:** the actual finished `cityrt-audit/docs/ART-BIBLE.md` and `KIT-SPEC.md`, backed by the audit’s images and evidence. The two planning docs you attached explain the expected artifacts. Their proposed values and planned checks do not establish results.
- **Travel:** your God’s Eye View reference illustrates the feeling of moving from the globe down to a real place. See `brief/CAMERAS_AND_TRAVEL.md`.
- **Art:** your screenshots are under `references/cityrt/`. The project illustrations in `references/project/` illustrate the intended framing and interaction.
- **Geography:** see `references/places/` for sourced visual boards and `references/globe/` for a ready-to-use Earth texture, preview, and optional Blender sphere starter.

The two CityRT screenshots in this ZIP are the user’s reference images. Keep them as reference only. The new production must use original meshes, shaders, textures and compositions designed for these coasts. The audit remains a local source of general visual principles.
