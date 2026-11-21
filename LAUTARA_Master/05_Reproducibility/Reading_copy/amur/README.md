# Northern Amur Bay comparator

## Article-ready findings

**A river-influenced coast can produce a dramatic optical signal after a reporting blind spot.** Russia’s federal hydrometeorological service reported high water in the Razdolnaya on 9–10 August and up to five times normal water abundance in its 18–19 August 2023 bulletin. Lisina et al. (2025) reconstructed floods on 10–13, 24–27 and 30 August to 1 September. The authors discuss intense precipitation and upstream reservoir releases as interacting drivers. The article and agency bulletins establish a plausible river pathway. They do not trace any specific body of colored bay water to one input.

- Across 18 Sentinel-2 dates over 1 July–30 September 2023 on tile T52TGP, just two reached at least 90% SCL class 6 (water) in **both** fixed west/east comparison boxes: 6 and 21 September. This is a coverage rule, not an optical validation or a water quality status threshold.
- Three Sentinel-2 dates fell in the three independently reconstructed flood intervals. None passed in both boxes. On 12 August only 4.55% of the west box was classified water and 0% east. On 27 August, both were 0%. On 1 September, the east box was 100% water-classed while the west was 4.80%. This last example shows why the location requirement matters when there is a partial view.
- First two-box pass was 6 September, five calendar days after the last documented flood interval ended. The September map shows a pronounced water-color boundary extending south from the vicinity of the mouth, consistent with a spatially structured optical feature. West-minus-east median red-band reflectance was +0.0552 on 6 September (0.1094 versus 0.0542) and +0.0195 on 21 September (0.0284 versus 0.0089). On each date both boxes had 100% water-class coverage. Green contrasts were +0.0236 and +0.0228, respectively.
- Tightening from 90% to 95%, or relaxing to 80%, leaves the same two dates. At 75%, a pre-August date enters: 28 July (+0.0808 red contrast, 76.18% west and 99.57% east water-class). This larger earlier contrast is a concrete counterexample to a rule that would treat the September brightness as unique to the documented August events. November–winter ice is a separate observation regime that this July–September comparison deliberately does not test.
- ERA5 reanalysis point requested at 43.8°N, 131.85°E and returned at 43.75°N, 131.75°E records 90.9 mm on 10 August and 77.0 mm on 29 August UTC. This is a point sampled from a weather product. The independent six-request/five-distinct-grid-history IMERG corridor dataset has 53.8 mm, 44.4 mm and 97.8 mm on 10, 24 and 29 August. Different grids, spatial supports and products give different amounts. Neither is observed river discharge or a historical forecast. See the rainfall workstream for the regional CHIRPS/CPC checks.

**Design implication.** Transfer the practice of checking water coverage at the actual location and asking what other sources fit its pattern. Calibrate the viable season, optical baseline and background drivers locally. A colored pattern, even one near a river after high water, cannot certify seabed extraction or quantify exposure. The supplied products cannot establish that a similarly colored signal at Tunda comes from the same mechanism.

## Methods and sources

- Sentinel-2 Collection 1 L2A STAC: [Earth Search v1](https://earth-search.aws.element84.com/v1/collections/sentinel-2-c1-l2a). Use fixed UTM 52N squares, 1.4 × 1.4 km. Published mouth marker 131.80778°E, 43.32556°N as origin. Box offsets from that marker in kilometers, (xmin, xmax, ymin, ymax): mouth (-0.7, 0.7, -2.7, -1.3), west (-0.7, 0.7, -6.7, -5.3), east (4.3, 5.7, -6.7, -5.3). Each box contains 4,900 nominal 20 m cell centers. Red and green medians (B04/B03) use valid 10 m pixels within SCL class 6, with each 20 m cell expanded to four aligned cells, applying signed STAC band scale and offset. Red contrast is west median minus east median. Neither reflectance nor its difference measures suspended solids, salinity or reef impact. Imagery is ESA/Copernicus Sentinel-2 modified for analysis. Boxes are analytic water areas, not habitat or exposed-population boundaries.
- [Roshydromet, river conditions for 9–10 August 2023](https://www.meteorf.gov.ru/press/news/34334/) published 14 August.
- [Roshydromet, river conditions for 18–19 August 2023](https://www.meteorf.gov.ru/press/news/34448/) published 21 August.
- [Regional hydrometeorological service, 2023 flood season summary](https://dfo.meteorf.gov.ru/news/889/). Its account links regional August rainfall to cyclones, fronts and typhoons KHANUN and LAN.
- [Lisina et al. 2025, Causes of flooding in the Razdolnaya basin in 2023](https://tigdvo.ru/assets/files/publications/Pacific_Geography_journal/2025_1/73-81.pdf), DOI 10.35735/26870509_2025_21_6.
- [Semkin et al. 2022, estuary field study and year-round context](https://doi.org/10.3390/jmse10121798). Documents river influence and ice season in a different study period.
- [Mouth marker](https://www.wikidata.org/wiki/Q111852). [PICES map and estuary overview](https://meetings.pices.int/publications/presentations/PICES-2011/2011-S7/S7-1430-Tishchenko.pdf).
- [Open-Meteo historical weather API documentation](https://open-meteo.com/en/docs/historical-weather-api). ERA5 point request uses model era5, dates 26 June–30 September 2023, UTC, no downscaling inference.
- [USGS Landsat Collection 2 quality assessment](https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands).
- The 2019–2026 seasonal **catalog** baseline contains 156 target-tile dates, 33 (21.2%) with tile cloud ≤20%. The count is not local coverage. Earth Search C1 returned zero for July–September 2022, while legacy Earth Search L2A and official Copernicus Data Space STAC both listed 18 target-tile dates. The inventory uses legacy for that year. This is an archive-discovery issue rather than evidence that Sentinel-2 did not observe the site.

## Reproduce

Use Python 3 with osgeo/gdal, NumPy and Matplotlib. Run `python amur_analysis.py --only-year 2023` for 18-scene raster extraction and article figures and `python amur_catalog.py` for the seasonal archive inventory. STAC JSON files are cached next to the script. Run `python amur_landsat.py` for the historical Landsat comparison via Planetary Computer. That script requests a short-lived public SAS credential in memory and outputs unsigned source URLs. Original rasters are not bundled. Use the signed asset service when rerunning the Landsat script. The seasonal archive inventory and 2023 two-zone pixel audit have different observation definitions.

- `amur_daily_2023.csv`: target-footprint fractions, red/green summaries, timestamp, STAC item, original raster URLs.
- `amur_rainfall_daily_2023.csv`: the ERA5 point time series plus the preceding three complete UTC days.
- `amur_catalog_2019_2026.csv`, `amur_catalog_summary.csv`: seasonal inventory with catalog identity, summary by year.
- `amur_scene_comparison.png`: the three-scene source-boundary and missingness example.
- `amur_event_timeline.png`: ERA5 point rainfall, local coverage and measured optical contrast around the three published flood periods.
- `amur_optical_counterexample.png`: 28 July versus 6 September reflectance context and the same box geometry.

## Cross-mission repeat of the optical comparison

The Landsat 8/9 Microsoft Planetary Computer Collection 2 L2 surface-reflectance sample contains **12 dates**. A native 30 m QA_PIXEL screen accepts water bit 7 and rejects bits 0–5 (fill, dilated cloud, cirrus, cloud, shadow, snow). At least 90% must pass in **each** of the same west and east footprints. The Landsat and Sentinel scene masks are sensor- and product-specific. Cross-mission coverage counts are sensitivity to two observation routes, not identical QA semantics. The median is the native surface-reflectance band scale and offset among accepted water raster cells, with no aquatic retrieval or cross-sensor normalization.

- Landsat adds **three distinct passing dates**. Sentinel-2 alone passes 2/18 dates and Landsat 4/12. The combined two routes pass **5/28 unique dates**, with 6 September passing on both. There are 30 acquisitions because 28 July and 6 September occur in both records.
- Across published flood episodes, there were four observation dates from either mission (12, 13 and 27 August and 1 September), and none passed in both footprints. The first joint west/east view after the last published flood remained 6 September even with Landsat added.
- On 6 September, both sensor products classify 100% of both footprints as water under their local QA screens and see the west side brighter in red. The same-date red contrast is +0.06460 Landsat 9 (01:57:06 UTC) and +0.05520 Sentinel-2A (02:15:26 UTC), 18 minutes 20 seconds apart. This corroborates the spatial pattern across independent optical instruments and processing routes. Band response, spatial resolution, atmospheric corrections, and acquisition time differ, so the equal-sign contrast is the warranted comparison.
- On 12 July, at the stricter 90% screen, Landsat observes a bigger red contrast of +0.09614, with west 100% and east 93.71% acceptable. It precedes the documented August flood intervals. This is the stronger counterexample to using color contrast alone to identify either the flood episodes or an industrial process.
- `amur_cross_sensor_timeline.png` integrates both missions and the ERA5 point with dates of locally valid observations. Run `python amur_cross_sensor_plot.py` to regenerate it.

Run `python verify_amur.py` to check the reported acquisition, overlap, flood-interval, optical, and catalog counts from the distributed tables.
