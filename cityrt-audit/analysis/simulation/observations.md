# Simulation and feel observations

**Status: blocked.** The game loop is behind authentication and no client bundle containing
it is served anonymously, so no tick rate, movement speed, construction timing, day/night
period, or camera easing constant was observed or extracted.

## What is established from public material

| Item | Value | Source |
|---|---|---|
| Genre | City builder with roads, districts, schools, hospitals, city budget | site meta description, `evidence/pages/*.html` |
| Multiplayer | "on your own or online with friends" | site copy |
| Client | Browser, no install | site copy |
| Entry | `/en/login?next=play` (gated) | live probe |
| URL parameters understood by the client | `map`, `scenario`, `room`, `host` | `evidence/scripts/public/registry-DDDDnwVQ.js` |
| Session markers | `cityrt.go`, `cityrt.play` storage keys | same chunk |
| "Coverings" (map skins) | 10 palettes with `desat` factors 0.05–1.0 | `analysis/skins-static.json` |

## What the twelve-hour plan wanted and could not get

- Tick/step interval and simulation cadence.
- Vehicle/pedestrian speeds and traffic rules.
- Construction duration and growth cadence.
- Day/night cycle length and colour keyframes.
- Camera zoom limits and easing constants.
- Pause/speed controls and their multipliers.

## Cheapest next probes (when auth works)

1. `requestAnimationFrame` cadence plus draw calls sampled every 2 s (already written as
   Task 16's method).
2. Sky-region colour sampled per tick to recover the day/night period.
3. HUD readouts sampled over 60 s to derive budget/population cadence.
4. Construction of one building timed from placement to completion.

All four are passive observations of normal play; none requires memory tampering.
