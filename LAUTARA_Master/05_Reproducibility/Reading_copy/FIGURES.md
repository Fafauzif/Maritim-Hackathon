# Exhibits

| Exhibit | Script or provenance | Main data |
|---|---|---|
| 1 Study sites | `root/make_core_figures.py` | Natural Earth and listed site anchors |
| 2 Sentinel time coverage | `root/build_facts.py` | `optical/sentinel_legacy_coverage.csv` |
| 3 Mission union timeline | `optical/summarize.py` | Matched Sentinel and Landsat masks |
| 4 Archived reef geometry and observation | `root/make_core_figures.py` and `root/habitat_audit.py` | Archived polygon and matched SCL, reported with successful-read denominators |
| 5 Optical interpretation counterexample | Prior diagnostic, reference 38 | Prior Sentinel-2 scene IDs and sector data, included in `review/` |
| 5a Tunda product clocks | `review/plot_tunda_clocks.py` | Archived STAC and product lineage metadata |
| 6 Rainfall × combined mission availability | `rain/join_multi.py` | Mission QA and the IMERG mainland proxy |
| 7 Kodingareng rainfall | `root/chart_rain_cases.py` | Multi-product prior and event series |
| 8 GLORYS12 regional seasonal and depth sensitivity | `marine/analyze_current_baseline.py` | 92,052 model vectors over study grid cells |
| 9 Assumption sensitivity for straight-line transport | `root/make_core_figures.py` | Declared speeds and horizons |
| 10 Amur Bay Sentinel imagery | `amur/amur_analysis.py` | Archived Sentinel product IDs and sampled targets |
| 11 Amur Bay flood and imagery timeline | `amur/amur_cross_sensor_plot.py` | Multi-mission coverage, dated flood history and rainfall |
