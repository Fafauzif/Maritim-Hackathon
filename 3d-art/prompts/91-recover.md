# DSH recovery prompt

Use this only for an actual failure. Read `brief/WORKFLOW_AND_BUDGET.md` with paths relative to `3d-art/`. Record what failed, the actual command or tool name, the short error, the checkpoint and expected output. Preserve evidence. Then use the specific recovery.

| Failure | Recovery |
|---|---|
| Wrong project folder or no finished audit | Discover the actual art bible or alternate root and check its scope. Start independent place references and provisional blockouts when appropriate. Revisit style when evidence arrives. Never infer finished audit results from either plan. |
| Tool name unavailable, MCP disconnected, save path invalid | Refresh connected tools and schemas. Check active Blender instance and local filesystem namespace. Use a second instance or explicit Blender binary for background operations if available. Do not edit unsaved user scenes. |
| MCP operation times out after state change | Inspect Blender scene and actual output before retrying. Reopen latest known checkpoint if needed. Retry an idempotent bounded operation or save a new version. |
| Harness receives an image pathname with no pixels | Use a documented screenshot/render view route or the harness’s actual image attachment path. Open an existing small preview. If access still fails, preserve the proof sheet for human review and accurately limit review claims. |
| Black or flat rendering | Check active camera, render visibility, material view, GPU support, lights, render layers and clip distance with a small test. Verify an actual PNG at low resolution before repeating the expensive render. |
| 8 GB VRAM pressure / render failure | Load only one coast, instance repeats, simplify procedural or volumetric effects, reduce unused textures and draft resolution, try Eevee or a verified CPU still fallback. Return to full resolution for final stills when feasible. |
| GLB missing texture or losing material | Inspect export selection and embedded image references. Bake or replace Blender-only nodes with a supported equivalent and re-import. Keep editable originals and record acceptable appearance differences. |
| Movie compilation fails | Validate individual frames and paths. Assemble surviving frames with an available encoder or Blender. Keep completed frames, save a VSE checkpoint and report the remaining output precisely. |

Resume the interrupted phase from the earliest unverified operation. Do not claim a blocker is resolved because an error disappeared. Verify the end artifact relevant to the failure.
