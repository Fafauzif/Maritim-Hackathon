# CityRT 3D style audit

Evidence-cited audit of the CityRT browser client's 3D style. Plan:
`docs/superpowers/plans/2026-11-21-cityrt-3d-style-audit.md`.

- `tools/` analysis and browser tooling (Node 24, no third-party deps except playwright-core, which ships inside the REA install)
- `evidence/` captures; `evidence/manifest.json` indexes them by SHA-256
- `analysis/` measurements derived from evidence
- `docs/` deliverables: STYLE-MATRIX, ART-BIBLE, KIT-SPEC, UNKNOWNS, COVERAGE

Run tests: `node --test cityrt-audit/tests`
