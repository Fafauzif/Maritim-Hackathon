# The Ocean Has Floors · DSH full art revision

**Decision.** Revise the entire three-coast art delivery on the owner's workstation. The owner hands a finished art ZIP to a teammate who implements the app and game behavior. This extraction contains the instructions, references and evidence fixture for that local run.

## Start the local run

1. Extract at your local **Maritim Hackathon repository root**, the folder that already contains `3d-art/`, `cityrt-audit/` and `blender-mcp/`. After extraction, this file must be at `3d-art/revision-v2/START_HERE.md`. If your unzip program creates an outer folder, merge its inner `3d-art/` into the repo root. Check for an existing `revision-v2/` before replacing anything.
2. Open that project in your DeepSeek Harness session. Keep the Blender instance with the configured MCP connection available. Save unrelated Blender work and either open your intended production scene or leave a clean instance connected.
3. Paste this into DSH.

   > Read and execute `3d-art/revision-v2/CONTINUE_PROMPT.md` from this repo root. Complete the full Blender MCP art revision on this workstation and deliver the verified teammate handoff ZIP. Start with local preflight now.

4. The target final file is `3d-art/revision-v2/delivery/LAUTARA_3D_Art_Handoff_v2.zip`. Work is resumable. Use `RESUME_PROMPT.md` in the same folder after an interruption.

## Files to read

| File | What it settles |
|---|---|
| [CONTINUE_PROMPT.md](CONTINUE_PROMPT.md) | Local authority, execution order and completion conditions |
| [BASELINE_AUDIT.md](BASELINE_AUDIT.md) | What already works and what to repair, with exact repo paths |
| [ART_DIRECTION.md](ART_DIRECTION.md) | Screenshot interpretation, site-specific design, views and scientific boundaries |
| [PRODUCTION_PLAN.md](PRODUCTION_PLAN.md) | Eight phases with acceptance checks, recovery and handoff tasks |
| [HANDOFF_CONTRACT.md](HANDOFF_CONTRACT.md) | Final bundle layout, artifact inventory, coordinates, runtime interfaces and QA |
| [RESUME_PROMPT.md](RESUME_PROMPT.md) | Substantial-run checkpoints and interruption recovery |
| [context/LAUTARA_Master_AI_Context_Updated.md](context/LAUTARA_Master_AI_Context_Updated.md) | Current project state followed by the original historical and scientific appendices |
| [references/CityRT_Cartoon_Finish_User_Reference.png](references/CityRT_Cartoon_Finish_User_Reference.png) | Owner-selected visual finish reference for local review |
| [references/Depth_case_verified.json](references/Depth_case_verified.json) | Verified offline pair for the optional app overlay input and annotated pitch plates |

V1 baseline `a0295d3e9323fe22ce05b7ed65cdba590291435a`. A newer local checkout is fine when it contains the required assets. Record its commit and any conflicts with the inventory. The plan stages all production under `3d-art/revision-v2/` and references existing artwork by path.
