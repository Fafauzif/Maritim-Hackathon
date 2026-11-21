# Independent verification and Tunda’s evidence clocks

The original 15-page audit’s embedded acquisitions reproduce when inspected with PyMuPDF:

```sh
python reproduce_previous.py /path/to/LAUTARA_2026_Coastal_Sediment_Diagnostic.pdf
```

Run `python cross_sensor_clock_audit.py` to rebuild the sensor-clock table from the seven bundled STAC responses. Use `--refresh` to retrieve the same bounding box and UTC interval from the current public catalog services. Run `python plot_tunda_clocks.py` to rebuild the timeline graphic. Matplotlib is needed for the graphic.

The single acquisition’s lineage files are `tunda_product_lineage.csv`, an Earth Search legacy item snapshot, the relevant STAC results and `audit_product_lineage.py`. The latter makes live HTTP HEAD requests to verify the currently served object headers. The CSV retains the historical response. This can be verified offline:

- Earth Search legacy [scene](https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/S2B_48MXU_20231026_0_L2A) gives original product baseline N0509, processing 26 Oct 06:21:26Z and STAC created 11:35:09.414Z.
- Its open [SCL asset](https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/48/M/XU/2023/10/S2B_48MXU_20231026_0_L2A/SCL.tif) returned Last-Modified 26 Oct 11:34:57Z. The RGB and red assets separately returned 26 Oct 11:23:09Z and 11:28:22Z.
- A different bucket’s [Collection 1 item](https://earth-search.aws.element84.com/v1/collections/sentinel-2-c1-l2a/items/S2B_T48MXU_20231026T031004_L2A) refers to the same original SAFE and generation stamp but has a 5 Jan 2024 asset and catalog stamp.
- [Copernicus Data Space](https://stac.dataspace.copernicus.eu/v1/collections/sentinel-2-l2a/items/S2B_MSIL2A_20231026T025809_N0510_R032_T48MXU_20241107T122501) lists N0510 and explicitly reports processing:datetime 7 Nov 2024 and published 25 Apr 2025. This is a later processing lineage. The different catalog datetime convention for the same acquisition date also limits hour-level interchangeability.
- [KKP press release SP.402/SJ.5/X/2023](https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html) dates the stop and inspection to 27 Oct and that release to 29 Oct. The release date represents this document, and other coverage may predate it.

The directly queried Landsat 8/9, Sentinel-2 L2A and Sentinel-1 GRD products list no acquisition dated 27 Oct for the specified bounding box. This is an archive result scoped to the queried products. HLS returns alternate processing of some of those same acquisitions. Object and catalog stamps document product lineage, rather than agency receipt or historical access terms. The preceding scene has no demonstrated association with the inspected material.

The raw Landsat catalog also returns one overlapping Landsat 7 date, 18 Oct. The article and the chart use Landsat 8/9 only. When reproducing the four-date count, apply the platform filter in `plot_tunda_clocks.py`; the broad CSV retains all catalog candidates. None of these candidates was acquired on 27 Oct.
