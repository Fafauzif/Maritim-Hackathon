# Resume the local v2 DSH run

> Read `3d-art/revision-v2/CONTINUE_PROMPT.md`, `PRODUCTION_PLAN.md` and this file. Recover the latest verified v2 checkpoint and continue the full run until the teammate ZIP passes clean extraction. Inspect actual files and tools before acting.

## Durable run state

Write `3d-art/revision-v2/work/latest-run.txt` with the active run ID, and a UTF-8 `progress.json` under that run folder. Use an atomic temporary sibling rename for state updates. Keep run-relative evidence paths. Record each phase as `pending`, `active`, `pass`, `failed`, or `blocked`. Mark a phase complete only after its gate evidence exists and can be checked.

Minimum state includes the following fields.

```json
{
  "schemaVersion": 1,
  "runId": "local timestamp or unique ID",
  "baseCommit": "resolved Git commit or null",
  "blenderVersion": null,
  "toolingEvidence": null,
  "activeCheckpoint": null,
  "phaseStatus": {"0": "pending", "1": "pending", "2": "pending", "3": "pending", "4": "pending", "5": "pending", "6": "pending", "7": "pending"},
  "siteStatus": {"kodingareng": "pending", "tunda": "pending", "amur": "pending"},
  "assetStatus": {},
  "renderJobs": [],
  "gateEvidence": {},
  "blockers": [],
  "nextAction": "Run local preflight."
}
```

For a render job include scene digest, profile and shot ID, key, frame range, resolution, status, output location and log. Track the actual background job ID when one is active. If it finished while disconnected, verify output before launching another. Keep metrics and images next to the gate that references them.

## Recovery steps

1. Discover or refresh the tools, confirm paths and locate the current run. See which Blender file is active. Save any unrelated work through the appropriate user-approved path before loading a checkpoint.
2. Inspect the ledger, active Blender file, latest safe scene checkpoint and real logs. Check that the expected outputs and their hashes match. A v1 completion record does not cover v2. If the v2 ledger is missing, reconstruct it from the last independently verifiable checkpoints and outputs.
3. Perform the smallest incomplete job or diagnose the failed one. Retrieve available process status and log before retrying. Recover only the gaps in a compatible frame sequence. Treat changed scene/signature or different dimensions as a different sequence. Keep the bad output in a diagnosable run folder.
4. Reduce draft samples or isolate the heavy scene if GPU memory is exhausted. Confirm the affected quality gate from a fresh proof before returning to production. If monitoring has no output for a useful detection interval, inspect process, GPU usage or logs before terminating only your own unresponsive job. Preserve any valid frames. Switch to a proven local CLI or bounded MCP operations as needed.
5. If opener compatibility fails, locate a compatible local Blender first. Use a v2 reconstruction from portable exports and builder logic if necessary. A section or camera missing from an imported GLB needs to be rebuilt and proved. If the encoder is unavailable, recover with an existing local encoder or Blender video output. Keep frames reusable and log any failed compatibility checks.
6. At the end of each recoverable task, log the exact command, paths, open issues and next action, then continue the run. Use a new artifact version rather than deleting delivered results. A mandatory QA gate can remain blocked only when evidence or workstation capability is genuinely unavailable.
