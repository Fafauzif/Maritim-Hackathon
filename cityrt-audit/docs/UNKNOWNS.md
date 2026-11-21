# Unknowns

Everything below was attempted and could not be determined in this run. Each entry names the
blocker and the cheapest next probe. No value was invented to fill a gap.

## Blocked by CityRT's authentication outage

On 2026-11-21 the site's own OAuth callback returned `Server error. Try again` after Google
consent, from both an automated and a normal Chrome. `/api/auth/google/start` returns a
server-side error, and `/api/changes?page=1` returns HTTP 500. The user independently confirmed
login failure on their normal setup and reported that other users see the same.

| # | Unknown | Why it matters | Cheapest probe |
|---|---|---|---|
| U1 | Renderer family (Three.js / Babylon / custom / wasm) | decides whether shaders can be ported or only imitated | re-run `tools/browser/probe.js` attach after login; `WEBGL_debug_renderer_info` is verified working on this host |
| U2 | Shader sources, post-processing chain, outline/AO technique | the difference between "looks similar" and "matches" | capture `shaderSource` pre-navigation (hook already built) |
| U3 | Light rig, shadow technique, tone mapping, exposure | night/day matching and shadow softness | `getParameter` + shader inspection once connected |
| U4 | Building triangle counts, LOD tiers, texture usage | kit budget realism (currently assumption) | network capture of model payloads |
| U5 | Simulation cadence: tick rate, traffic speeds, construction time, day cycle, camera easing | the "physics/feel" brief item | 60 s passive time-series of rAF + screenshots (method written in plan Task 16) |
| U6 | Whether the nine-style marketing claim maps to a nine-entry in-game picker | affects how many styles a kit must ship | observe the in-game style picker |
| U7 | Why `metropolis`, `british`, `brazil` have zero catalog buildings | three registered styles cannot be rebuilt from catalog data | watch those styles in-game, or find a later catalog version |
| U8 | Meaning of the third value in skin `sky` arrays (e.g. `["#B4BFD0","#F2DDC2",0.25]`) | one palette parameter (likely sky mix/opacity) | read the client chunk that consumes it after login |
| U9 | Absolute grid size (5 m is inferred from "~5 m of frontage") | kit scale correctness | measure a known building's footprint against a known model bound |

## Blocked by tooling

| # | Unknown | Why | Cheapest probe |
|---|---|---|---|
| U10 | Desktop shell type (Electron / NW.js / WebView2) and its payload | `winget` could not install 7-Zip (needs admin elevation; installer exited 1602) | `7z l CityRT-Windows.exe` on a machine with 7-Zip, or `7z x` into `evidence/installer/payload/` |

## Deliberately not attempted

| # | Item | Reason |
|---|---|---|
| U11 | Paying for the Anti-Bot Pass | it is a paid product ($5.99/yr, $10.99 lifetime per `/api/config`); purchasing is the user's decision, not the agent's |
| U12 | Bypassing the anti-bot gate | out of scope by the audit's constraints |
| U13 | Redistributing extracted art | licensed material; audit keeps evidence local |

## What would change the most with one successful login

A single authenticated session would convert U1–U5 from unknown to measured, which is the
difference between this audit's "art direction with honest limits" and a full technical style
specification. Everything else in the deliverables stands on its own.
