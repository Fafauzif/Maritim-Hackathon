# Before the Plume Reaches the Reef

Reproducibility companion to the 25-page LAUTARA 2026 research article. Analysis uses public sources. Original providers retain rights and attribution. Public catalog URLs and scene identifiers are included. The archive contains results and scripts, with the raw products needed for selected offline checks. It does not mirror full satellite imagery or global model archives.

## Start here

1. Read `CLAIMS.md` for the headline evidence table and `FIGURES.md` for inputs and figure scripts.
2. In the extracted directory, run `python verify.py` with Python 3.10 or later. Standard library only. This verifies the reconciled headline counts and key claims against the packaged data.
3. Run `python -m pip install -r requirements.txt` for offline figure reproduction. You also need Open Sans and DejaVu Serif for the article. To regenerate the final article from the packaged tables and figures, run `python root/build_facts.py` and `python root/article.py regenerated.pdf`. The regenerated PDF is expected to match the findings and layout. PDF timestamps and object metadata may differ.
4. For optional live raster retrieval, use Python with matching system GDAL bindings, NumPy, and network access. Some archive assets are read through temporary public signing. Refresh only when needed and preserve the packaged snapshot for exact historical comparisons. Service catalog contents, URL availability and product versions can change.

## Contents and workstream commands

| Directory | Contents and optional steps |
|---|---|
| `optical/` | Complete queried site-date inventories for Sentinel-2 and Landsat. Some older raster reads failed and are marked as unknown. Curated source/processing tables and scripts. Run `python optical/summarize.py` for matched-window tables and figures. See `optical/methodology.md` for full date ranges and flag definitions. |
| `rain/` | Analyzed NASA POWER/IMERG, CHIRPS and CPC subsets, plus checksummed raw responses. Run `python rain/analyze.py` for rainfall results, then `python rain/join_multi.py --sentinel optical/sentinel_legacy_coverage.csv --landsat optical/landsat_coverage.csv` for rainfall × optical coverage. See `rain/README.md` for follow-up horizons. |
| `marine/` | Daily Copernicus GLORYS currents, marine-condition series, versioned manifests, and study-window summaries. Run `python marine/analyze_environment.py` and `python marine/analyze_current_baseline.py` against the cached tables. See `marine/README.md` for direct product retrieval. |
| `amur/` | Three flood windows, regional rain, catalog inventory, measured 2023 Sentinel and Landsat windows, figures and a standalone verification. Run `python amur/verify_amur.py`. |
| `events/` | Dated claims, source URLs, evidence scopes, link to official dispositions and coordinate-conflict computation. Run `python events/create_manifest.py` to rebuild the register. |
| `review/` | Independent verification notes, original audit summary tables, archival clocks and comparison inventory. Run `python review/cross_sensor_clock_audit.py` from this directory tree, followed by `python review/plot_tunda_clocks.py` if desired. The clock audit works offline against packaged catalog responses. |
| `root/` and `figures/` | Report narrative and layout, archived reef footprint analysis, reusable figure inputs and publication copies. Figures inherited from the prior LAUTARA audit are identified in the article and crosswalk. |

Coordinates in geographic files are in WGS84 unless indicated. Sensor dates are UTC date labels. Control and weather classifications are analytical labels. All default thresholds are the study's thresholds. The cross-archive analysis does not establish a historical authorization, verified sediment dose, or operational effect.

Reference links appear in the PDF and in `source_manifest.csv`. The package inventory and hashes are in `SHA256SUMS.txt`.
