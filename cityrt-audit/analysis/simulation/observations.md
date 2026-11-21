# Simulation and feel observations

**Status: partial.** The authenticated client bundles were captured, so the timing system is
now readable in code. The city simulation modules (`newgame`, `launch`, `lens`) returned HTTP 500
before download, so tick-level constants remain open.

## Measured from the client

| Item | Value | Source |
|---|---|---|
| Day length | **24 real minutes default**, user range 4–120 min | `evidence/game-bundles/daylight-xoA8egPB.js` |
| Time model | `sky` is an hour 0–24; advances by `dt * speed * 24 / (dayMinutes*60)` | same |
| Day/night toggle | `dayNight` pref (default on) | `prefs-Dk13dMkm.js` |
| Speed control | multiplier with ×3 available; pauses with simulation/menu | `prefs`, shipped tips |
| Idle render policy | ~30 FPS while the camera is still; full refresh while moving | shipped UI text (`en-C1arqVDc.js`) |
| Camera smoothing | `camSlow` default 0.25 (slow-camera filming mode) | `prefs-Dk13dMkm.js` |
| Pause on menu | `menuPause` default on | same |
| Autosave | every ~60 s; `Ctrl+S` quicksave | shipped tips |
| Undo | full refund on construction undo | shipped tips |

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
