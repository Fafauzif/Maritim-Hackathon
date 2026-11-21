# Coverage against the brief

Brief: `docs/superpowers/specs/2026-11-21-cityrt-style-audit-brief.md`

## Success criteria

| Criterion | Status | Where |
|---|---|---|
| 1. Each style has a named matrix row; every cell measured or explicitly unobserved with a reason | **Met (superset)** | `docs/STYLE-MATRIX.md` — 14 registered styles + `shared`; no blank cells |
| 2. Every quantitative claim traces to a hashed evidence file | **Met** | `evidence/manifest.json`; analysis files cite their source paths |
| 3. A reader can rebuild a convincing original building set from `KIT-SPEC.md` alone | **Partially met** | `docs/KIT-SPEC.md` covers grid, footprints, materials, hierarchy, budgets, tests; heights and tri budgets are labelled assumptions because the client was unreachable |
| 4. `UNKNOWNS.md` states what could not be determined and why | **Met** | `docs/UNKNOWNS.md` — 13 unknowns with blockers and next probes |

## Brief scope items

| Scope item | Status | Evidence / deliverable |
|---|---|---|
| Rendering: tone mapping, lighting, fog, shadows, post | **Not observed** | `analysis/rendering/renderer-verdict.md`; output-level observations only |
| Nine style personalities as visual systems | **Met, 14 shipped** | `docs/STYLE-MATRIX.md`, `analysis/styles/styles-static.json` |
| Palette per style | **Met** | `analysis/palette/*.json` (14 hero renders) + `analysis/catalog/catalog-summary.json` (824 studio renders) |
| Materials | **Met at output level** | `docs/ART-BIBLE.md` §5 — rules derived from renders; shader params unknown |
| Building language: grid, massing, proportions, budgets | **Partially met** | grid 5 m inferred; footprints measured from shipped text; proportions measured (silhouette aspect); tri budgets are assumptions |
| Simulation/feel | **Not observed** | `analysis/simulation/observations.md`; only public genre facts |
| Art bible | **Met** | `docs/ART-BIBLE.md` |
| Kit specification | **Met** | `docs/KIT-SPEC.md` |
| No Blender execution | **Respected** | no Blender call in the run |
| No anti-bot bypass | **Respected** | Gate A stopped the run and escalated to the user |
| Read-only on CityRT | **Respected** | only public GETs; no account, no writes |

## Review Focus items from the plan

| Focus item | Outcome |
|---|---|
| Challenge page captured as the game | **Prevented** — `classifyPage` returned `challenge` and the run stopped (Task 7 test covers it) |
| Marketing hero captured instead of the 3D client | **Confirmed real** — the public site *is* only the marketing shell; recorded rather than mistaken for the game |
| Blank or software-rendered frames | **Prevented** — blank gate + renderer assertion implemented; never triggered because no in-game frames were captured |
| Capture before the scene populates | **Prevented** — `sceneReady` predicate implemented with tests |
| Style never changes due to persisted state | **Prevented by design** — fresh context per style; not exercised live because login failed |

## Automated evidence check

`node cityrt-audit/tools/coverage.js cityrt-audit` scans every deliverable for cited
repository paths and verifies each one exists and matches its digest in
`evidence/manifest.json`. Latest run: **27 claims, 20 file references checked, 0 missing,
0 unregistered, 0 hash mismatches.** The manifest itself holds **907** registered artefacts.

## Honest limits of this audit

- The single largest gap is the authenticated client (U1–U5). Everything about shaders,
  physics and live feel is unknown, not approximated.
- Building "palette" measurements include the studio plot ground; they are used as relative
  comparisons between styles, not as absolute material colours.
- The 14-vs-9 style discrepancy is documented, not resolved.
