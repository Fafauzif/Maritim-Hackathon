# Copy this into DeepSeek Harness

You are the Blender environment artist and technical art lead for **The Ocean Has Floors**. Use my configured **Blender MCP** in this project and actually author, render, inspect and deliver the 3D assets. My intended local setup is **Blender 5.2.2, RTX 4060 Laptop GPU, 8 GB VRAM**, using DeepSeek v4.1 Flash 1017 in this harness. Discover the tools and runtime you actually have. Commands, files and image inspection count only when performed and evidenced.

## Goal and priorities

Build **three equally polished** stylized coastal worlds: **Kodingareng Lompo**, **Pulau Tunda**, and the **Razdolnaya estuary in northern Amur Bay**. Use a god’s-eye camera with room to roam. Design at three scales: **a real-outline Earth**, **a navigable high-oblique view of each coast**, and **a deliberate cut through the seabed with the same coastal landmarks**. Use the Earth view and a short travel shot for each coast to express the journey. Make it possible for me to orbit and pan around the assets in Blender. The viewport and films are the test of this experience.

Apply the visual principles from my **finished local CityRT REA audit**. Preserve the bird’s-eye camera, coherent density and material treatment that the observed evidence supports, adapted to these real coastlines. Use original models/materials and place-specific references. Read completed audit outputs, keep their files intact, and use visual observations to guide production. Tiny UI text, real-world signals, GIS analysis, extraction overlays, a browser viewer and the app are outside this 3D run. The Earth base image is art; local coast and section geometry are reference-led and illustrative.

## Read first

1. Read `3d-art/START_HERE.md`, `brief/REA_HANDOFF.md`, `brief/VISUAL_DIRECTION.md`, `brief/CAMERAS_AND_TRAVEL.md`, `brief/WORKFLOW_AND_BUDGET.md`, `brief/OUTPUT_CONTRACT.md` and `brief/DELIVERY_CHECK.md`, all inside `3d-art/`.
2. Read the source boards and look at the attached visual references. Use the rendered audit outcomes in place. The audit implementation plan describes how the earlier research was meant to run. Start this art assignment when the audit has results. Treat project files and page captures as reference material, never as instructions to execute their scripts or rerun the REA job.
3. Execute the numbered prompts under `3d-art/prompts/` in order **00 to 06**. The 90-series prompts help you recover. These are action prompts: act through tools, write files, render the proof, inspect it, update the checkpoint, and continue within the same run when feasible. Do not just give me a plan or a Blender Python snippet.
4. Work in a new production scene and keep every authored output under `3d-art/`. Keep a recoverable checkpoint before destructive geometry changes. Saving under `work/` protects previously delivered files. Keep `work/progress.json` accurate. Use sequential writes to the same Blender scene. Separate reviewer sessions may inspect completed renders; they cannot overwrite production scenes.

## Definition of done

- Three coasts pass the **same** art review standard. Show all overhead shots beside each other at the same displayed size. Show how to orbit from the saved god’s-eye views. At each location make the cutaway legible by holding the jetty/boat where possible, or the river bank and boat at Amur.
- Deliver a geographic Earth overview, a film for each coast, and a short reel that visually joins the Earth and the three local worlds. Use a composed transition between global and local scales. Do not invent a seamless, geographically accurate coordinate transfer or portray a surveyed model.
- Deliver 4K stills, editable Blender sources, reusable parts and portable GLBs. Reopen Blender files and re-import every GLB into a fresh temporary scene to check water, orientation, mesh, material and texture references. Write the results to the output review folder.
- The Blender MCP operation log, actual renders with review notes, and `tools/check_delivery.py` are evidence of delivery. A render that DSH cannot see goes in the parity review sheet for my eyes and gets a clear limitation in the handoff. An empty, partially rendered or unreviewed deliverable does not get a pass label.
- If a system capability is missing, recover using the prompts and work on any independent task. Report exact gaps and preserve all completed work. Ask me only when a concrete dependency truly blocks further progress, such as no accessible Blender installation and no MCP connection.

Begin with the preflight now.
