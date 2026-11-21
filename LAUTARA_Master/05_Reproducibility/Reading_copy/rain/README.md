# Antecedent precipitation analysis

## What was analyzed

Three mainland rainfall proxies support the Tunda, Kodingareng Lompo and Amur Bay reconstructions. Proxy footprints are specified in `acquire.py`. They are fixed sampling footprints near plausible land runoff corridors and do not delineate watersheds, trace river outlets, or estimate precipitation at the offshore extraction sites. They also cannot be interpreted as gauge readings at the sampled coordinates.

- NASA POWER daily `IMERG_PRECTOT`, UTC, native 0.1° (~11 km north–south), Jan 1 2019–Dec 31 2025. Eighteen point histories were downloaded, six at each proxy. Identical whole-period histories caused by sampling the same native cell were deduplicated within each site before equally averaging values. The resulting site proxy means represent 6, 4 and 5 distinct sampled histories for Tunda, Kodingareng and Amur, respectively. Each mean has 2,557 complete dates. The underlying historical time series is IMERG Final per POWER's published retrospective-product cutoff. Retrieval/processing latency is about 3.5 months per POWER's methodology; these values serve retrospective interpretation and do not establish records available at the decision time.
- ClimateSERV UCSB CHIRPS daily `avg` for a defined regional land rectangle, native 0.05° (~5.6 km north–south), accessed as area aggregates. It offers 91 Tunda event-context dates (Sep–Nov 2023), 306 Kodingareng dates (15 Jan–15 Nov 2020), and 58 Amur dates (20 Jul–15 Sep 2023). The report uses its day labels from delivered epochTime UTC; CHIRPS and IMERG represent different retrievals and spatial footprints, and both incorporate some station information.
- NOAA CPC Global Unified Gauge-Based Daily Precipitation, 0.5° (~55.6 km north–south), requested from the NOAA PSL NetCDF Subset Service. Site requests return nearest grid centers 106.25°E/6.25°S, 119.75°E/5.25°S, and 131.75°E/43.75°N. This is a gauge-interpolated regional check, with local gauge assignment/coverage and daily timing uncertain. It has its own spatial support and may reflect storm peaks on an adjacent day. Date labels were left as served. Using different products probes sensitivity rather than guaranteeing complete statistical independence.

Prior one-, three- and seven-day amounts exclude the anchor day and require all days in the window. Compare each amount to the empirical distribution for the same calendar month (as labeled for the anchor date) in other years from 2019–2025, using half-weight for ties. For IMERG, typical comparison n is 180 or 186; n is explicit for each cell in `rainfall_events.csv`. Ranks summarize the selected sample window and carry no model-based significance. No CHIRPS baseline rank is reported because only event windows were retrieved. The 2019–2025 baseline means January 2019–December 2025 products are well beyond NASA's ~3.5-month historical Final cutoff when fetched.

## What the results support

| Case or date | Original result | Implication |
|---|---|---|
| **Tunda, 27 Oct 2023 inspection** | Prior UTC date Oct 26 combined IMERG mean **16.1 mm** (P87), local proxy input-cell range **0–30.1 mm**, vs CHIRPS **2.0 mm** and CPC **0.0 mm**. Prior three days **20.5 mm** IMERG (P60.2), **12.4 mm** CHIRPS, **5.7 mm** CPC. | A single pixel's high daily value is not robust regional event evidence. Allow rain/runoff as a potential competing pathway, but the proxy data do not establish discharge, offshore transport, or sediment source. |
| **Tunda, weather reference 4 Nov 2023** | IMERG **48.4 mm**, CHIRPS **24.0 mm**, CPC **28.8 mm**. Three materially different spatial samples and techniques capture a regional wet period. | Stronger wet-day weather comparator. Case records do not verify what vessels were doing that day, so the date does not establish a known source or “no dredging” control. |
| **Tunda, reported 18–22 Nov window** | During date labels 18–22 Nov inclusive IMERG **18.7 mm**, CHIRPS **21.1 mm**, CPC **12.3 mm** (rounded). On window start 18 Nov, antecedent 3-day **26.8 mm** IMERG (P49.4), **15.7 mm** CHIRPS, **22.5 mm** CPC. | Ordinary multi-day wetness for this particular IMERG proxy. Evidence remains incomplete about actual local runoff, vessel activity and source. |
| **Kodingareng, reported 13 Feb 2020 start** | Prior 1/3/7 days **3.8 / 22.6 / 130.6 mm** IMERG (P33.7/P37.3/P69.2). Three-day CHIRPS and CPC **58.9 / 21.3 mm**. Later **5 Mar** (reported operation window) agreement **52.8 / 53.1 / 47.6 mm**, IMERG/CHIRPS/CPC, respectively. | The project-period record includes wet days, and “start day” results depend heavily on product and lookback. Compare observations against season and an explicit rain history before attributing a coastal change. This does not establish daily extraction presence or source. |
| **Kodingareng, reported 26 Oct 2020 end** | IMERG mean **0.3 mm** on the anchor, CHIRPS **8.0 mm**, CPC **26.7 mm**; preceding 3 days **9.2 / 2.5 / 16.0 mm**. | Endpoint day alone has less value for attribution than dated operating observations and a multiday view. |
| **Amur, 10–13 Aug 2023 flood window** | On Aug 10 IMERG **53.8 mm** (P98.9), CHIRPS **52.1 mm**. CPC proxy returns **8.6 mm** that day and **100.4 mm** Aug 11. | Multiple products corroborate a wet period with mismatched day-level peaks, while field hydrometeorological literature independently identifies a flood. |
| **Amur, 24–27 Aug 2023 flood window** | Aug 24 IMERG **44.4 mm** (P97.8), CHIRPS **36.9 mm**. CPC **66.9 mm** Aug 23, **0.8 mm** Aug 24, **48.4 mm** Aug 25. | Evidence of major regional forcing in adjoining day slots. Do not align exact peaks or infer causality from one daily timestamp. |
| **Amur, 30 Aug–1 Sep 2023 flood window** | Aug 29 IMERG **97.8 mm** (greater than all 186 selected outside-year August comparison days), CHIRPS **138.5 mm**, CPC **38.5 mm**. Prior three days as of Aug 30 **128.5 / 172.5 / 39.0 mm**. | A credible external check for a wet-river coastal interpretation. The design still requires separate evidence of estuary transport and water field conditions. |

Important clock convention: a complete UTC day for Oct 26 ends at 07:00 WIB on Oct 27. The local incident date is a date-level alignment only. CPC gauge reporting periods may differ within nominal day labels. The study does not impute incident hours.

## Reproduce

Run `python acquire.py` to fetch direct subsets and archive provider responses with URL and SHA256, then `python analyze.py` to regenerate the CSVs and Matplotlib figures. Existing raw files are reused. The scraper can optionally be restricted to one source with `--only`. An initial NOAA API rate limit delayed two baseline files, which were recovered through sequential retries. All CPC site-years are included. Runtime depends on provider and cache. `analyze.py` needs Python 3, NumPy and Matplotlib. The CSV and plot analyses are deterministic on the included raw bytes.

- `rainfall_daily.csv`: site × daily panel, each sample history, mean/range, and 1-, 3-, 7-day preceding amounts. `imerg_n` counts unique histories available that day; blanks are missing and zero is a returned dry estimate.
- `rainfall_events.csv`: case anchors and matched empirical ranks.
- `rainfall_comparison.png`, `.svg`: all three event-centered time series. The differing date axes are intentional.
- `raw/`: provenance-preserving original downloads and query specs.

## Sources

- NASA POWER daily API: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- NASA POWER methods, including UTC, IMERG grid and release lag: https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/#imerg-integrated-multi-satellite-retrievals-for-gpm
- NASA GPM IMERG: https://gpm.nasa.gov/data/imerg
- CHIRPS methods and access: https://www.chc.ucsb.edu/data/chirps and https://climateserv.servirglobal.net/develop-api
- NOAA CPC metadata: https://www.psl.noaa.gov/data/gridded/data.cpc.globalprecip.html
- Local Banten literature on a separate Ciujung sediment pathway in Tanjung Pontang/Banten Bay, not contemporary Tunda source attribution: https://doi.org/10.15578/jkn.v1i2.6614
- WALHI reported Kodingareng 13 Feb start and 26 Oct cessation: https://www.walhi.or.id/uploads/buku/TLH_2021_edited_2.pdf and https://www.walhi.or.id/uploads/buku/Policy%20Paper%20-%20Jaring%20Nusa%20KTI%20%281%29.pdf
- Amur event windows from Lisina, Vasilevsky & Vasileskaya (2025), independent local hydrometeorological history: https://doi.org/10.35735/26870509_2025_21_6 and https://tigdvo.ru/assets/files/publications/Pacific_Geography_journal/2025_1/73-81.pdf

## Rain timing interacts with optical viewing gaps

A separate descriptive join uses the two sites' archived pilot Sentinel-2 scene masks on exactly the months for which the rainfall series overlaps: Jun–Sep and Nov–Dec 2025. A high-rain-proxy day is defined as a UTC calendar date with ≥10 mm mean IMERG in the site's mainland sampling proxy. A qualifying optical calendar day has at least one cataloged scene with ≥90% of the original island ring in SCL classes 2, 4, 5, or 6. This join tests descriptive coincidence and is neither a causal cloud model nor an offshore rain, plume, or sensor-allocation forecast.

| Site and dates | ≥10 mm days | No catalog acquisition | Acquisition, below local 90% | Qualifying optical date |
|---|---:|---:|---:|---:|
| Tunda, Jun–Sep 2025 | 35 | 28 | 4 | 3 |
| Tunda, Nov–Dec 2025 | 34 | 26 | 7 | 1 |
| Kodingareng, Jun–Sep 2025 | 20 | 14 | 5 | 1 |
| Kodingareng, Nov–Dec 2025 | 38 | 27 | 11 | 0 |

In Nov–Dec, only 1 of 72 higher-rain site-days supplied a qualifying Sentinel-2 view. No acquisition was found for 53 site-days, while 18 had at least one acquisition below the original broad-coverage threshold. A ≥5 mm cutoff still gives 1 of 92 higher-rain site-days; ≥20 mm gives 0 of 30. A site-day is allowed to appear at both locations and cannot be treated as an independent event. Different collection searches, Landsat or taskable sensors could change catalog/availability counts. The "missing" class means no scene within the original queried inventory, not proof of no launch, overpass or possible observation. The lesson for prevention is to log those two distinct shortfalls and specify what evidence should drive the next decision before weather narrows the optical window.

Reproduce with `python join_coverage.py --tunda prior/tunda.csv --kodingareng prior/kodingareng.csv` followed by `python plot_rainfall_visibility.py`. The two prior inventories are included. Output: `rainfall_optical_days.csv`, `rainfall_optical_summary.csv`, `rainfall_visibility.png/.svg`.

### Adding Landsat across the full 2025 window

`join_multi.py` combines the full 2025 Sentinel-2 and Landsat QA results from the optical workstream with the IMERG calendar dates above. At least one readable scene ≥90% broad clear is enough to mark a mission-date or an either-mission date as qualifying; the result is a site-day union, so same-date duplicates do not count twice. Masks differ by mission and are equivalent in use rather than in individual classification flags.

Among 257 site-days with ≥10 mm IMERG mainland proxy rain across the two sites in full 2025, Sentinel-2 had 59 acquisition dates and 9 qualifying dates; Landsat 31 and 4; the union had 81 and 13, respectively. Among 473 lower-rain site-days, Sentinel had 39 qualifying dates, so the union increased to 52. The difference compares observational opportunity within these samples; mainland precipitation and offshore mask coverage are not co-located cloud observations. Seasonal and acquisition-selection structure both affect the margins.

In November–December, Landsat increased combined higher-rain acquisition opportunities from 19 to 23 of 72 site-days, but the combined number of ≥90% qualifying dates stayed at exactly one. The combined sensor failure counts are 49 days without an acquisition in the selected inventories and 22 with at least one acquisition that did not meet the broad coverage criterion. This qualifies the idea of passive multisensor monitoring: reserve non-optical or field verification capacity for cases that can arrive during extended cloud-affected periods. It does not estimate detection probability for an actual plume.

Run `python join_multi.py --sentinel ../optical/sentinel_legacy_coverage.csv --landsat ../optical/landsat_coverage.csv`, using the report's bundled input inventories or their updated canonical paths, then `python plot_multisensor.py`. Output: `rainfall_multisensor_days.csv`, `rainfall_multisensor_summary.csv`, `rainfall_multisensor.png/.svg`.

### What a longer follow-up window recovers

`lag_to_view.py` asks whether at least one ≥90% qualifying site view appears on the ≥10 mm proxy rain day or within 1, 3, and 7 following calendar dates. Horizon-specific denominators exclude origins too close to 31 December to observe the whole horizon. Overlapping windows and common regional conditions make these descriptive counts rather than independent trials. A delayed qualifying image is an opportunity to review the site, not evidence that a short-lived sediment signal would still be present.
