# CityRT 3D Style Audit — Brief

**Date:** 2026-11-21
**Requester:** hackathon workspace owner (`Maritim Hackathon`)
**Trigger:** `CityRT-Windows.exe` (111 MB) placed in the workspace.

## What the target actually is

The supplied file is not the game. Forensics on the PE32 executable show a
**Nullsoft Install System v3.04** installer (electron-builder's format) whose
version resource reads:

| Field | Value |
|---|---|
| ProductName | `CityRT` |
| CompanyName | `CityRT.com` |
| Description | `CityRT for Windows and macOS: a window onto cityrt.com, updates come from the site` |

So the desktop build is a shell around the website. `https://cityrt.com` is a
browser city-builder that advertises **nine style personalities** and **more than
600 buildings** (Russian copy: "Больше 600 домов, парков и башен"). The 3D
content is served by the site, not carried in the installer.

## Decisions taken by the requester

| # | Question | Decision |
|---|---|---|
| 1 | Analysis target | **Live site** — browser + WebGL + network capture |
| 2 | Style coverage | **All nine styles**, documented separately |
| 3 | Dimensions in scope | Art direction (palette, lighting, materials, post-FX); shaders and rendering technique; physics/simulation feel |
| 4 | End deliverable | Art bible + **original-inspired** modular Blender kit (not a copy of shipped models) |
| 5 | Blender | Blender 5.2 + Blender MCP addon, glTF export — but **not in this run** |
| 6 | Permissions | May install 7-Zip and record `cityrt.com` traffic |

## Scope of this run

**In scope (audit and analysis only):**

- How CityRT renders: renderer, tone mapping, lighting rig, fog, shadows, post-processing, shaders.
- The nine style personalities as distinct visual systems: palette, materials, silhouette, mood.
- The building language: module grid, massing, proportions, roof/facade vocabulary, triangle budgets — measured from served models where possible.
- The simulation/feel layer: tick rates, movement speeds, construction timing, day/night cycle, camera limits and easing.
- A normative **art bible** and a **kit specification** that a later Blender run can implement.

**Out of scope for this run:**

- Any Blender execution, Blender MCP call, or 3D asset authoring.
- Gameplay cloning, netcode, economy balance, backend APIs.
- Redistribution of extracted models, textures, or shaders.
- Bypassing the site's anti-bot pass, or any paywall/registration on the user's behalf.

## Constraints

- **No anti-bot circumvention.** If a challenge appears, a human may clear it in a visible browser window; the harness resumes with that same profile.
- **Read-only on the live service.** No writes to other players' cities, no account creation, no purchases. If sign-in is required, stop and ask the requester.
- **Original output.** The art bible may describe technique; the future kit must be original geometry that shares a visual language, not reproduced assets.
- **Local evidence only.** Captures stay under `cityrt-audit/evidence/`; nothing is uploaded.
- **Polite capture.** One page at a time, ≥2 s between style loads, no parallel crawling.

## Success criteria

1. Nine styles each have a named entry in a style matrix, every cell either measured or explicitly marked unobserved with a reason.
2. Every quantitative claim (colour, size, rate, triangle count) traces to a file in `evidence/manifest.json` by SHA-256.
3. A reader who has never seen CityRT can rebuild a convincing, original building set from `KIT-SPEC.md` alone, with measurable acceptance tests.
4. `UNKNOWNS.md` states what could not be determined and why — no silent gaps.

## Open questions to resolve during execution

- Are all nine styles reachable from a fresh anonymous session, or gated behind progression/login?
- Are building models served as glTF/GLB, Draco-compressed glTF, or baked into a custom binary/wasm format?
- Is the scene rendered by Three.js, Babylon.js, Playwright-hostile custom WebGL, or a wasm engine (Unity/Godot)?
- Does the site require a "pass" before the game canvas becomes interactive for automation?
