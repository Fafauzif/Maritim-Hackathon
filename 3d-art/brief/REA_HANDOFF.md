# Ingest the completed CityRT audit

The existing project already contains the REA run. This pack assumes there will be useful results under `cityrt-audit/`. The attached Superpowers plans name the expected paths below. These are locators to verify in the actual project. If the audit moved its outputs, locate the finished `ART-BIBLE.md` and its sibling files, then confirm their shared root before using them. Never substitute the planning documents for observed captures.

| Open in this order | Use in Blender |
|---|---|
| `cityrt-audit/docs/ART-BIBLE.md` | Look, camera hypotheses, lighting, palette, material and silhouette principles. Identify which evidence actually supports the views closest to the user’s references. |
| `cityrt-audit/docs/KIT-SPEC.md` | Measured geometry language and proposed asset budgets. Translate the grid and dimensions into local coastal architecture. Copying game names, geometry, textures or code would not help with local identity. |
| `cityrt-audit/docs/STYLE-MATRIX.md` | Contrast observed styles. Pick one primary style family for all three coasts, with at most one measured secondary influence. Prefer the observed high-oblique reference style closest to the user’s screenshots. |
| `cityrt-audit/docs/UNKNOWNS.md`, `COVERAGE.md` | Find gaps, contradictions and incomplete styles before treating a statement as measured. |
| `cityrt-audit/evidence/manifest.json` | Follow evidence paths and check recorded hashes when available. Confirm the relevant file before labelling it audit-backed. |
| `cityrt-audit/evidence/styles/<style-id>/{overview,mid,street,night}.png` | Inspect the validated high-oblique and mid-altitude frames. Use them as local-only visual reference. Prioritize useful images over raw captures. |
| `cityrt-audit/analysis/palette/`, `geometry/`, `rendering/`, `constants.json`, `simulation/` | Cross-check light/value range, building proportions, fog, and easing only where documented. A pixel sample is a display-referred color reference; it is not the Blender base-color input. |

## What to write in `output/review/audit-intake.md`

Record the resolved audit root, date or version found, selected style name/ID and two or three style anchors. For each production rule, name the observed reference, actual repo-relative file and hash if available, what you saw, what will change in these coastal scenes, and what render tests it. Record the decision as **observed**, **derived**, **design target**, or **unavailable**. Distinguish video or motion observations from inferences from stills. A good intake has at least six actionable rules: camera, massing, light, palette, water/edges, and motion. Camera and light matter more than matching a palette swatch exactly.

Example format, with deliberately fictional inputs:

| Dimension | Evidence label | Observed reference / actual path / digest | Coastal production rule | Test |
|---|---|---|---|---|
| Camera | design target | operator brief page 2 | start high enough to read the village layout and leave open water | compare 960 px and 320 px proofs without labels |
| Palette | unavailable | palette summary missing | choose a restrained proposed palette from the user's supplied visual reference; label it provisional | compare all three views in like lighting |

If `ART-BIBLE.md` or `KIT-SPEC.md` is missing, check for an equivalent completed deliverable and make the gap explicit. A partial audit permits preflight, visual-source review and provisional blockouts using the user screenshots. If usable evidence still has not arrived, mark style sign-off pending and keep chasing the actual output while doing independent work. Do not mark the result as a finished-audit implementation until you can point to evidence. Do not import extracted CityRT assets or shader code. Keep the audit file tree unmodified even when a measured value needs interpretation.
