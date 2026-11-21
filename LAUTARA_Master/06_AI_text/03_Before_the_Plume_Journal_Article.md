# 03_Before_the_Plume_Journal_Article

Extracted text by printed PDF file page. Use the original for tables, reading order, diagrams and page geometry.

## PDF page 1

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
ORIGINAL RESEARCH
BEFORE THE PLUME REACHES THE REEF
Satellite observation, sediment pathways and coastal work decisions in Indonesia
and the Russian Far East
Comparative coastal sediment study
Prepared for the LAUTARA 2026 Russia–Indonesia Maritime Hackathon
ARTICLE INFO
ABSTRACT
Study areas
Tunda Island, Banten
Kodingareng Lompo, South Sulawesi
Amur Bay, Russian Far East
Study period
Indonesian optical archive, January
2019–October 2026
Historical case windows, 2020 and
2023
Keywords
Sea-sand extraction
Coral reef exposure
Satellite observation
Sediment transport
Coastal management
Coastal managers need evidence at the scale of the habitat they
seek to protect and at a time when they can still change work. This
study examined whether public imagery, environmental series and
official records can support eight decisions about sediment risk
before, during and after coastal operations.
The Indonesian inventory included 1,178 Sentinel-2 site-dates, with
1,177 readable quality masks, and 799 readable Landsat products.
During January 2025–October 2026, Landsat added 15 qualifying
dates at Tunda and 25 at Kodingareng. Across both islands in
November–December 2025, either mission passed the local screen
on only one of 72 site-days with mainland rainfall of at least 10 mm.
At Tunda, switching from an island annulus to an archived reef
footprint changed the screening result on 34 of 587 dates.
Two optical missions also observed the same west–east contrast at
Amur Bay after documented flooding. A qualifying pre-flood image
showed a stronger contrast. The findings support identifying the
habitat, observation coverage and backup verification route before
work begins. Exact extraction footprints, reef-scale transport and
sediment dose remained unresolved.
Data and code Scene inventories, analysis scripts and verification checks accompany the study in the reproducibility
archive.
Before the plume reaches the reef
1

## PDF page 2

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
INTRODUCTION
Sea-sand extraction can resuspend fine material.
Whether this becomes an ecological concern
depends on where the material travels and the
intensity, duration and frequency of exposure at a
particular reef. Turbidity, deposition and biological
response are distinct quantities. A local study of
Tunda using reef surveys and MIKE 21 modelling
provides a physical and ecological starting point.1,2,3
This study addresses a related decision problem. It
asks 
what 
can 
be 
established 
from 
public
observations in time to assess siting, work timing,
precautionary changes, exposure, source control,
baseline records, field verification and recurrence.
STUDY AREAS
Tunda Island. The Banten case combines an
archived reef map with a documented October 2023
inspection. 
Kodingareng 
Lompo. 
The 
South
Sulawesi case combines project records, reported
fishing concerns and a disputed location in the public
incident record.4,5,6,7,8,9,10
Amur Bay. The Razdolnaya estuary provides an
independent, 
river-influenced 
comparator. 
Three
documented flood intervals in August–September
2023 provide a timeline for examining what an optical
signal can establish about potential sediment
sources.11,12,13,14
Fig. 1. Regional locations of the three study anchors. Points mark the observation areas. Coastlines are from Natural Earth.15
Table 1. Roles and periods in the comparative study.
Case
Primary analysis
Historical reference
Tunda
Reef-level visibility and evidence timing
27 October 2023 inspection
Kodingareng Lompo
Fishing receptor geography and regional
transport
February–October 2020 project period
Amur Bay
Optical interpretation under documented river
influence
July–September 2023 observation
window
Before the plume reaches the reef
2

Links embedded on this page

- https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans
- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- https://doi.org/10.30872/mulrev.v6i2.621
- https://tribratanews.polri.go.id/blog/hukum-4/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716
- https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- https://www.meteorf.gov.ru/press/news/34448/
- https://dfo.meteorf.gov.ru/news/889/
- https://doi.org/10.3390/jmse10121798
- https://tigdvo.ru/assets/files/publications/Pacific_Geography_journal/2025_1/73-81.pdf
- https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/

## PDF page 3

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
MATERIALS AND METHODS
Optical inventory and screening
Sentinel-2 and Landsat scenes were inventoried from
public catalogs. Images of the two Indonesian sites
were evaluated within a 1.5–3 km annulus. For the
broad screen, Sentinel-2 scene classification (SCL)
codes 2, 4, 5 and 6 were retained. Landsat
QA_PIXEL excluded fill, dilated cloud, cirrus, cloud,
shadow and snow. A date qualified when at least 90%
of the footprint passed. An unreadable product was
treated as unknown.16,17,18,19,20
Same-day 
or 
seven-day 
opportunity 
measures
included 662 candidate dates per Indonesian site in
the matched January 2025–October 2026 window. A
mission contributed an additional date when it passed
the screen on a day without a pass from the other
mission.
Habitat geometry and optical contrast
Archived reef polygons were rasterized in local UTM
and compared with annular scores. The Amur case
compared fixed western and eastern water zones
using mission-specific screening. Relative red-band
reflectance was compared within each scene.
Atmospheric, surface and shallow-water effects
remain possible.10,21
Environmental context
Daily precipitation context used NASA POWER
IMERG, CHIRPS and NOAA CPC. The products differ
in grid spacing and daily reporting conventions. For
IMERG, event values were ranked against the same
calendar month in other years during 2019–2025.
Mainland proxies describe regional rain and do not
measure offshore runoff or discharge.22,23,24,25,26
Daily Copernicus GLORYS12 vectors were examined
in nine cells per site at modeled depths of 0.494 m
and 9.573 m. Regional direction was compared by
date, month and depth. A separate straight-line travel
calculation was used as a sensitivity test.27,28,29
Historical evidence and claim strength
Dated records distinguish the reported event,
observation and source availability. Current catalog
entries can represent later reprocessing. Source
locations 
with 
unresolved 
contradictions 
were
withheld from site-specific transport inference.
The analysis is descriptive. Image-screen scores
measure observation support. Regional currents,
optical contrast and official actions each address a
different part of the activity-to-impact chain.
Table 2. Key analytical units and the quantities they support.
Evidence
Unit
Supports
Optical quality flags
Scene / site-date
Observable area and revisit opportunity
Habitat overlay
Reef footprint / sector
Target-specific observation support
Meteorology and currents
Product grid / day
Regional context and sensitivity
Agency and project
documents
Dated record / case
Documented action and evidence timing
Before the plume reaches the reef
3

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands
- https://stac.dataspace.copernicus.eu/v1/
- https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- https://doi.org/10.1016/j.rse.2019.03.010
- https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary
- https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html
- https://www.chc.ucsb.edu/data/chirps
- https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/#imerg-integrated-multi-satellite-retrievals-for-gpm
- https://open-meteo.com/en/docs/marine-weather-api
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description

## PDF page 4

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
RESULTS
Optical coverage and complementary missions
Fig. 2. Sentinel-2 acquisition inventory, readable quality masks and locally qualifying site-dates. Asterisk denotes 2026 through
October.
Fig. 3. Matched Sentinel-2 and Landsat observation opportunities, 1 January 2025–31 October 2026. A pass retains ≥90% of the
local annulus under the broad screen.
Table 3. Incremental optical opportunities and remaining gaps. Longest runs include window boundaries.
Site
Sentinel-2 passes
Combined passes
Longest run without a pass,
days
Tunda
62
77
132 → 131
Kodingareng Lompo
63
88
162 → 158
The share of eligible origin dates with a same-day to seven-day qualifying view rose from 51.2% to 57.7% at
Tunda and from 48.2% to 55.6% at Kodingareng. The gains improved routine revisit relative to the long periods
without a qualifying full-ring view.
Before the plume reaches the reef
4

## PDF page 5

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
Habitat-specific observation and optical interpretation
Fig. 4. Annulus versus archived reef coverage for cached historical and baseline subsets. Dashed lines mark the broad 90%
local screen. Archived footprints represent mapped habitat context.10
Fig. 5. Modified Sentinel-2 imagery at Tunda, 22 and 24 July 2025. The strongest contrast shown extends across land and
water, weakening a sediment-only interpretation.30
Across the full Tunda series, 10 dates passed the
annulus only and 24 passed the archived reef only.
Within the 3 km disc, the annulus captured 43.4% of
mapped reef pixels. At Kodingareng, eight of 109
dates in the bounded footprint comparison passed the
reef only.
The 26 October 2023 Tunda scene passed the broad
ring at 95.3%, while the western half of the archived
reef footprint scored 75.8%. A reviewer’s choice of
receptor changes which observation counts.
A passing scene still requires interpretation. In the
July example, brightness over both land and water is
compatible with imaging or atmospheric effects. This
limits the strength of a source claim even when the
image appears striking.21,30
A river-transport study in Banten Bay provides a
separate mechanism to consider. Another regional
field series recorded elevated suspended solids on a
date with zero reported output for its tracked
operator.31,32
Before the plume reaches the reef
5

Links embedded on this page

- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- https://chatgpt.com/library?file_id=libfile_61a9ace26b688191a4897fac7ce72ee4
- https://doi.org/10.1016/j.rse.2019.03.010
- https://doi.org/10.15578/jkn.v1i2.6614
- https://doi.org/10.15578/segara.v14i1.7149

## PDF page 6

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
Evidence timing and rainfall at Tunda
Fig. 6. Acquisition dates and archival lineages around the Tunda inspection. The display distinguishes overpass, processing,
catalog and reported action dates.4,16,19,20,33,34
Fig. 7. Optical observation outcomes on Indonesian site-days with mainland IMERG rainfall ≥10 mm, for 2025 and the
November–December subset.22,23,24,25
The 27 October 2023 KKP stop and inspection is
documented. The release reports approximately
24,000 m³ of sand aboard and describes its reported
origin and permit issues as suspected. None of the
scoped Sentinel-2, Landsat 8/9 or Sentinel-1 catalogs
returned an acquisition dated 27 October.4,5
The 26 October Sentinel-2 acquisition has both an
older Earth Search version with same-day archival
metadata and a later Copernicus reprocessing.
Neither record establishes when a reviewer actually
received the image.
The previous UTC day’s mainland precipitation
estimates were 16.1 mm from IMERG, 2.0 mm from
CHIRPS and 0.0 mm from CPC. On 4 November, all
three estimates were at least 24 mm. These products
provide regional context. Activity on that comparison
day remained unresolved.22,24,25
Across both islands in November–December 2025,
only 1 of 72 higher-rain site-days had a qualifying
local view from either optical mission. On 49 days
there was no cataloged acquisition. On 22 days
available imagery did not pass the screen.
Before the plume reaches the reef
6

Links embedded on this page

- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://stac.dataspace.copernicus.eu/v1/
- https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- https://hls.gsfc.nasa.gov/data-access-and-tools/
- https://www.esa.int/media/sentinel-1-tracking-maritime-traffic
- https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary
- https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html
- https://www.chc.ucsb.edu/data/chirps
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf

## PDF page 7

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
Project geography, rainfall and depth-dependent flow
Fig. 8. Regional rainfall estimates during the documented Kodingareng project period. Markers distinguish a reported start, a wet
comparison day and the September incident account.6,8,22,24,25,35
Fig. 9. Seasonal share of GLORYS12 daily vectors with an eastward component around Tunda and Kodingareng, at two
modeled depths. Values describe regional grid cells, not measured reef-scale currents.28
The contractor reported moving approximately 11
million m³ during phases 1B–1C from February
through October 2020. Of 54 Sentinel-2 and 17
Landsat dates in that period, 26 and 10 passed the
broad local screen respectively. These observations
describe the island footprint and the project period.6,7
The printed police coordinate was 2.24 km from the
island anchor, while the account described a distance
of 11 miles. Because these descriptions conflict, the
coordinate was excluded from source-to-receptor
calculations.8
The model reference series contained 92,052 vectors
over nine cells per site, two depths and 2,557 days. At
the 
Kodingareng 
reference 
cell, 
an 
eastward
component appeared on 139 of 274 study-period
days at 0.494 m and 230 at 9.573 m. Nearby surface
cells disagreed on its sign on 92 days.28
Across Tunda’s 31-day event window, the selected
neighboring cells had a westward component at both
depths. A separate regional surface-current series
also indicated westward flow on the local inspection
date. These products offer regional context for local
checks.27,28,29
Before the plume reaches the reef
7

Links embedded on this page

- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- https://tribratanews.polri.go.id/blog/hukum-4/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716
- https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html
- https://www.chc.ucsb.edu/data/chirps
- https://www.greenpeace.org/static/planet4-indonesia-stateless/2021/03/17185db9-gp-spermonde-report-v8.pdf
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- https://doi.org/10.30872/mulrev.v6i2.621
- https://open-meteo.com/en/docs/marine-weather-api
- https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description

## PDF page 8

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
Transfer test in a river-influenced coastal system
Fig. 10. Modified Sentinel-2 true-color imagery of Amur Bay, August–September 2023. Boxes identify analysis zones used to
compare red-band reflectance.
Fig. 11. Acquisition dates, local observation opportunities, documented flood intervals and retrospective rainfall context. The
three flood windows are from published hydrometeorological evidence.11,12,14
From July through September 2023, Sentinel-2
qualified on 2 of 18 dates and Landsat on 4 of 12
dates. The combined inventory yielded five qualifying
dates among 28 unique observation dates. All four
acquisition dates during documented flood intervals
failed the two-zone screen.
On 6 September, acquisitions approximately 18
minutes apart showed a brighter western zone in both
Sentinel-2 and Landsat 9. The red-band differences
were +0.0552 and +0.0646 within their respective
scenes.
A qualifying 12 July Landsat scene, before the
documented August flood intervals, showed a larger
west-minus-east contrast of +0.0961. Optical contrast
supports 
a 
spatial 
observation. 
Timing 
and
independent evidence remain necessary for source
attribution.13,21
The seasonal catalog contained 156 July–September
Sentinel-2 dates in 2019–2026 after restoring 18
dates from the legacy collection for 2022. The
footprint-level result above refers to the 2023 case
window.16,19
Before the plume reaches the reef
8

Links embedded on this page

- https://www.meteorf.gov.ru/press/news/34448/
- https://dfo.meteorf.gov.ru/news/889/
- https://tigdvo.ru/assets/files/publications/Pacific_Geography_journal/2025_1/73-81.pdf
- https://doi.org/10.3390/jmse10121798
- https://doi.org/10.1016/j.rse.2019.03.010
- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://stac.dataspace.copernicus.eu/v1/

## PDF page 9

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
DISCUSSION
Fig. 12. Scenario sensitivity to speed, time and receptor direction. The illustrated locations and straight-line paths are
hypothetical. No concentrations or local plume boundaries were estimated.
Where and when work matters
A straight-line calculation illustrates the scale of the
uncertainty. A parcel moving at 0.10 m/s for six hours
would travel 2.16 km. At 0.25 m/s it would travel 5.40
km. The scenario helps identify which assumptions
can reverse a screening decision. Real pathways
depend on local currents, settling, mixing and
geometry.
The Kodingareng depth and cell comparisons show
why a single regional vector is a weak basis for a
project rule. A verified work polygon and locally
supported transport estimate matter when candidate
sites or work windows rank differently.2,3,28,36,37
What an observation can support
Observation 
coverage, 
source 
attribution 
and
regulatory action call for different evidence. Satellite
imagery can add context to a lead. A field check can
clarify 
location 
and 
relevant 
conditions. 
Work
restrictions and formal findings depend on the
authority and evidentiary requirements for the
particular decision.38,39,40
The proposed Indonesia–Russia comparison is a way
to test transferability. A shared observation protocol
can travel across sites. Habitat tolerance, river
influence, source geometry and authorization need
local evidence.41,42
Before the plume reaches the reef
9

Links embedded on this page

- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- https://www.big.go.id/uploads/content/produk/Laporan%20Tahunan%20BIG/LaporanTahunanBIGTahun2024.pdf
- https://www.gebco.net/data-products/gridded-bathymetry-data
- https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765
- https://peraturan.bpk.go.id/Details/249417/pp-no-26-tahun-2023
- https://www.epa.wa.gov.au/sites/default/files/Policies_and_Guidance/Technical_guidance_EIA_of_Marine_Dredging_Proposals.pdf
- https://kemenkoinfra.go.id/detailpost/menko-ahy-pimpin-konsultasi-bilateral-indonesia-rusia-sepakat-perkuat-kerja-sama-perkapalan-dan-konektivitas-maritim
- https://www.poi.dvo.ru/en/structure/lab94

## PDF page 10

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
Decision implications across the work cycle
Table 4. Eight coastal decisions, candidate evidence and the unresolved requirement.
Decision
Evidence-supported implication
Requirement for stronger inference
1. Siting
Screen transport to a verified receptor as well
as distance.
Verified work polygon and local transport
evidence.
2. Timing
Examine date, depth and location when
comparing windows.
Actual operating times and local
conditions.
3. Precaution
Match the intervention to corroboration and
authority.
Case-specific authority and decision basis.
4. Exposure
Build a history of receptor-specific magnitude,
duration and recurrence.
Field-supported concentration or
deposition and a baseline.
5. Source control
Retain activity, river, seabed and optical
alternatives until tested.
Independent evidence matching location
and time.
6. Baseline records
Preserve product versions and event,
observation and release clocks.
Actual historical access or receipt where
relevant.
7. Verification
Screen the exact receptor and plan a backup
observation route.
On-the-ground or independent
observations during blind periods.
8. Recurrence
Track regulatory outcomes and habitat or
livelihood outcomes separately.
Comparable follow-up measures for each
outcome.
CONCLUSION
Local 
coverage, 
evidence 
timing 
and 
source
corroboration determine which coastal action public
data can support. Landsat improved revisit coverage,
while late-year gaps remained long. Screening the
actual reef recovered observations missed by an
island-wide rule. The Amur comparison shows why
dated 
environmental 
context 
matters 
before
attributing an optical signal.
STUDY LIMITATIONS
The public record leaves exact extraction footprints,
reef-scale transport and sediment dose unresolved.
Archived reef geometry and regional grids support
geographic screening. Monitoring gaps and project
timelines should be interpreted at the resolution and
dates actually examined.
Before the plume reaches the reef
10

## PDF page 11

LAUTARA 2026  |  Research manuscript
Coastal sediment decisions
DATA AND CODE AVAILABILITY
Derived data, scene inventories, analysis scripts and verification checks are included in the LAUTARA Coastal
Sediment Reproducibility archive. This manuscript uses the analysis documented in the earlier study. Satellite
imagery and habitat sources retain their provider attributions. The Kodingareng regulatory follow-up is recorded
separately from ecological and livelihood outcomes.9,30
REFERENCES
[1] UNEP (2023). Marine Sand Watch and global dredging
estimates.
[2] Wahyudi et al. (2023). Tunda reef survey and MIKE 21
modelling.
[3] Erftemeijer et al. (2012). Dredging and sediment effects
on corals.
[4] KKP (29 Oct 2023). Official release on the 27 Oct stop
and inspection.
[5] KKP Loka PSPL Serang (FY2023). Performance report,
p. 38.
[6] Boskalis. Makassar New Port project sheet, phases
1B–1C.
[7] Kurniawati et al. (2021). Kodingareng fieldwork and
policy evidence.
[8] Indonesian Police (13 Sep 2020). Report about the Taka
Copong incident.
[9] DPR Commission IV (2024). South Sulawesi visit report,
pp. 5–6.
[10] UNEP-WCMC. Global Distribution of Coral Reefs v4.1,
polygon layer.
[11] Roshydromet (21 Aug 2023). Satellite monitoring of
Primorye floods.
[12] Far Eastern Hydromet. Primorye 2023 hydrological
season review.
[13] Razdolnaya/Suifen estuary study. River-influenced
coastal environment.
[14] Lisina et al. (2025). Razdolnaya flood episode
chronology, pp. 73–81.
[15] Natural Earth. 1:10m land polygons (public domain).
[16] Earth Search v1. Cloud-Optimized GeoTIFF catalog,
Element 84.
[17] Copernicus. Sentinel-2 scene classifications and
processing.
[18] USGS Landsat Collection 2. QA_PIXEL quality bands.
[19] Copernicus Data Space. Official STAC catalog.
[20] Microsoft Planetary Computer. Public Landsat C2 L2
catalog.
[21] Vanhellemont (2019). Atmospheric correction for
aquatic remote sensing.
[22] NASA POWER. Daily point API and temporal
reference.
[23] NASA GES DISC. GPM IMERG Final, V07 product
metadata.
[24] NOAA CPC. Global unified gauge-based precipitation
archive.
[25] UCSB Climate Hazards Center. CHIRPS rainfall
methods and data.
[26] NASA POWER. IMERG source, grid scale, and
production latency.
[27] Open-Meteo. Marine API and model/geographic
definitions.
[28] Copernicus Marine. GLORYS12 global physical
reanalysis.
[29] Copernicus Marine. Global ocean physics analysis and
SMOC currents.
[30] Prior LAUTARA coastal sediment diagnostic and
embedded scene tables.
[31] Banten Bay regional sediment transport study, Tanjung
Pontang.
[32] Peer-reviewed Banten Bay TSS and reported
extraction pairs, table 2.
[33] NASA HLS. Collection descriptions and download
access.
[34] ESA. Sentinel-1 radar for maritime context.
[35] WALHI and Greenpeace. Spermonde investigation and
community record.
[36] BIG (2024). Annual report and product specifications
for BATNAS.
[37] GEBCO. Global gridded bathymetry and source
identifier grids.
[38] KKP JDIH. Regulation 5/2025 amending 30/2021, arts.
8, 19 and 28.
[39] Indonesia PP 26/2023. Management of sedimentation
products in the sea.
[40] Western Australia EPA. Technical guidance for marine
dredging proposals, §§3.6.3–3.6.4.
[41] Kemenko Infra (June 2026). Indonesia–Russia
maritime working groups.
[42] Pacific Oceanological Institute FEB RAS. Satellite
oceanography lab.
Before the plume reaches the reef
11

Links embedded on this page

- https://chatgpt.com/library?file_id=libfile_b8704091df1c819189fa17cf61011304
- https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf
- https://chatgpt.com/library?file_id=libfile_61a9ace26b688191a4897fac7ce72ee4
- https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans
- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- https://doi.org/10.30872/mulrev.v6i2.621
- https://tribratanews.polri.go.id/blog/hukum-4/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- https://www.meteorf.gov.ru/press/news/34448/
- https://dfo.meteorf.gov.ru/news/889/
- https://doi.org/10.3390/jmse10121798
- https://tigdvo.ru/assets/files/publications/Pacific_Geography_journal/2025_1/73-81.pdf
- https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/
- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands
- https://stac.dataspace.copernicus.eu/v1/
- https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- https://doi.org/10.1016/j.rse.2019.03.010
- https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary
- https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html
- https://www.chc.ucsb.edu/data/chirps
- https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/#imerg-integrated-multi-satellite-retrievals-for-gpm
- https://open-meteo.com/en/docs/marine-weather-api
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description
- https://doi.org/10.15578/jkn.v1i2.6614
- https://doi.org/10.15578/segara.v14i1.7149
- https://hls.gsfc.nasa.gov/data-access-and-tools/
- https://www.esa.int/media/sentinel-1-tracking-maritime-traffic
- https://www.greenpeace.org/static/planet4-indonesia-stateless/2021/03/17185db9-gp-spermonde-report-v8.pdf
- https://www.big.go.id/uploads/content/produk/Laporan%20Tahunan%20BIG/LaporanTahunanBIGTahun2024.pdf
- https://www.gebco.net/data-products/gridded-bathymetry-data
- https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765
- https://peraturan.bpk.go.id/Details/249417/pp-no-26-tahun-2023
- https://www.epa.wa.gov.au/sites/default/files/Policies_and_Guidance/Technical_guidance_EIA_of_Marine_Dredging_Proposals.pdf
- https://kemenkoinfra.go.id/detailpost/menko-ahy-pimpin-konsultasi-bilateral-indonesia-rusia-sepakat-perkuat-kerja-sama-perkapalan-dan-konektivitas-maritim
- https://www.poi.dvo.ru/en/structure/lab94

