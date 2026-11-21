# Completed optical audit notes

## 1. Set the observation path before work begins

From 2019-01-01 to 2026-10-31, we measured 1,177 of 1,178 deduplicated Sentinel-2 site-dates and all 799 Landsat 8/9 scene products across the two Indonesian rings. Landsat contributes 282 Tunda dates and 280 Kodingareng dates after resolving multiple same-day overlapping products. One Kodingareng Sentinel-2 entry, 5 Nov 2022, exposed only an unavailable JP2 quality asset. The older dates are included, with unavailable coverage explicit.

At Tunda, Jan–Feb reached 90% broad local quality on 5/93 acquisitions (5.4%), versus 87/156 (55.8%) in Jul–Sep. Kodingareng reached 13/95 (13.7%) versus 95/155 (61.3%). Calendar groupings repeat across years, but these archives and masks are an observation study, not a sediment or rainfall climatology. The historical graph shades the uncertainty envelope due to missing quality rasters; only Kodingareng November has an unread raster. Main figure: `optical_monthly.png`.

## 2. Build a contingency for long visibility gaps

Use Jan 2025–Oct 2026 for the cleanest complete two-mission comparison, with both missions and footprints fully assessed over the exact same period. Tunda had 62 qualifying Sentinel-2 dates at 90%; 23 Landsat dates qualified, eight on an already qualifying Sentinel date and fifteen new, giving a 77-date union. Kodingareng had 63 Sentinel dates and 30 Landsat, five overlap and twenty-five additional, giving an 88-date union. Both gains persist at 80% and 95% and with strict water classification. Tunda has fewer Landsat gains under the 90% water-only label, eleven rather than fifteen. Kodingareng remains twenty-five.

Adding Landsat increases the fraction of calendar dates with a qualifying same-day or future observation within seven days from 51.21% to 57.70% (Tunda) and 48.19% to 55.59% (Kodingareng). It changes the longest fully qualified-observation-free stretch only 132 to 131 days and 162 to 158 days respectively. For Kodingareng at 95%, the worst 162-day stretch does not improve. Neither sensor added a qualifying date to Tunda's single 1 Nov pass nor Kodingareng's zero passes during Nov 2025–Feb 2026. This motivates a field- or records-based observation path that still works when optical visibility fails.

The entire 2019–Oct 2026 interval also shows material gain. Tunda 175 S2 passes, 77 Landsat passes, 16 overlap, 236 union (61 added). Kodingareng 239 confirmed S2 passes, 115 Landsat passes, 21 overlap, 333 confirmed union (94 added); one classified date remains unknown. Historical launch and platform changes alter the roster, so report matched 2025–26 for direct gap comparisons. Main figure: `optical_union_timeline.png`; optional window insert: `optical_pilot_windows.png`.

## 3. Make the reef the unit of the visibility decision

Tunda’s full historical Sentinel-2 roster has 34 disagreements between the ring and archival reef footprint at the same 90% rule (of 587 dates, 5.8%). Ten dates passed the ring and failed the reef; twenty-four dates passed the reef and failed the ring. On 30 Sep 2025 the ring gave 67.128% and the archival reef 95.137%. Thus target-specific screening gives both blind-spot warnings and usable leads. Use archival reef context rather than contemporary extent. Main figure: `optical_reef_disagreement.png`.

## 4. Preserve the time of evidence, not just the date on a reconstructed picture

No exact-day Sentinel-2 or Landsat acquisition exists in the named archives on the 27 Oct 2023 Tunda patrol-stop date. Sentinel-2 passed on 26 and 31 Oct, Landsat on 23 and 31 Oct. This is a retrospective raster check over the island ring, not contemporaneous product delivery, a source observation, or proof other sensors and people lacked evidence. Tunda 18–22 Nov coalition passage interval had one Sentinel observation date in the Tunda ring, on 20 Nov, close to zero broad coverage, and zero Landsat dates. The fishers' location was Pulau Pari, distinct from the Tunda ring.

No same-day named optical acquisition exists on the reported 13 Feb 2020 Kodingareng onset (coalition report) or numeric 12 Sep 2020 official police date. Sentinel-2 qualified one day after the former, or one day before and four days after the latter. Landsat's closest qualifying dates for 12 Sep are 5 and 21 Sep. Across the Feb–Oct 2020 contractor month-scale deployment envelope, all 54 Sentinel and 17 Landsat site-dates were measured, with 26 and 10 broad passes respectively. These are observation opportunities near the island, not validated observations of the quarry or sand transport. Use `optical_event_window_summary.csv`.

## Reproducibility checks

All 116 earlier Tunda/Kodingareng site-dates from the two common pilot windows reproduced their local broad and water QA fractions to <0.000001 percentage point (rounding precision). Across 939 paired same-site, day, platform and capture-time observations within ±2 minutes, legacy and Collection 1 differ on 17 operational pass decisions; median absolute coverage difference is zero and p95 is 7.50 pp. Use legacy where observed and same-acquisition Collection 1 recovery for a single missing QA case. QA agreement reflects comparable processing and raster extraction, not independent validation of the water-quality signal.
