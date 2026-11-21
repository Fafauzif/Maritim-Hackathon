"""Render the 25-page article from the analysis figures and checked metrics."""
import argparse,json
from pathlib import Path
from layout import Article,ROOT,L,CW

refs={
1:('LAUTARA 2026 guidebook. Sections 3–6, judging criteria and programme.','https://chatgpt.com/library?file_id=libfile_a0f1f94bc47c81919f0b91c5fbf16337'),
2:('UNEP (2023). Marine Sand Watch and global dredging estimates.','https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans'),
3:('Wahyudi et al. (2023). Tunda reef survey and MIKE 21 modelling.','https://doi.org/10.2478/cjf-2023-0009'),
4:('Erftemeijer et al. (2012). Dredging and sediment effects on corals.','https://doi.org/10.1016/j.marpolbul.2012.05.008'),
5:('KKP (29 Oct 2023). Official release on the 27 Oct stop and inspection.','https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html'),
6:('KKP Loka PSPL Serang (FY2023). Performance report, p. 38.','https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf'),
7:('KKP JDIH. Regulation 5/2025 amending 30/2021, arts. 8, 19 and 28.','https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765'),
8:('Earth Search v1. Cloud-Optimized GeoTIFF catalog, Element 84.','https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/'),
9:('Copernicus. Sentinel-2 scene classifications and processing.','https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html'),
10:('USGS Landsat Collection 2. QA_PIXEL quality bands.','https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands'),
11:('Boskalis. Makassar New Port project sheet, phases 1B–1C.','https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf'),
12:('Kurniawati et al. (2021). Kodingareng fieldwork and policy evidence.','https://doi.org/10.30872/mulrev.v6i2.621'),
13:('Indonesian Police (13 Sep 2020). Report about the Taka Copong incident.','https://tribratanews.polri.go.id/blog/hukum-4/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716'),
14:('DPR Commission IV (2024). South Sulawesi visit report, pp. 5–6.','https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf'),
15:('UNEP-WCMC. Global Distribution of Coral Reefs v4.1, polygon layer.','https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1'),
16:('Natural Earth. 1:10m land polygons (public domain).','https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/'),
17:('NASA POWER. Daily point API and temporal reference.','https://power.larc.nasa.gov/docs/services/api/temporal/daily/'),
18:('NASA GES DISC. GPM IMERG Final, V07 product metadata.','https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary'),
19:('Open-Meteo. Historical weather API and reanalysis product definitions.','https://open-meteo.com/en/docs/historical-weather-api'),
20:('Open-Meteo. Marine API and model/geographic definitions.','https://open-meteo.com/en/docs/marine-weather-api'),
21:('Copernicus Marine. GLORYS12 global physical reanalysis.','https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description'),
22:('Roshydromet (21 Aug 2023). Satellite monitoring of Primorye floods.','https://www.meteorf.gov.ru/press/news/34448/'),
23:('Far Eastern Hydromet. Primorye 2023 hydrological season review.','https://dfo.meteorf.gov.ru/news/889/'),
24:('Razdolnaya/Suifen estuary study. River-influenced coastal environment.','https://doi.org/10.3390/jmse10121798'),
25:('Kemenko Infra (June 2026). Indonesia–Russia maritime working groups.','https://kemenkoinfra.go.id/detailpost/menko-ahy-pimpin-konsultasi-bilateral-indonesia-rusia-sepakat-perkuat-kerja-sama-perkapalan-dan-konektivitas-maritim'),
26:('Pacific Oceanological Institute FEB RAS. Satellite oceanography lab.','https://www.poi.dvo.ru/en/structure/lab94'),
27:('Vanhellemont (2019). Atmospheric correction for aquatic remote sensing.','https://doi.org/10.1016/j.rse.2019.03.010'),
28:('Copernicus Data Space. Official STAC catalog.','https://stac.dataspace.copernicus.eu/v1/'),
29:('Microsoft Planetary Computer. Public Landsat C2 L2 catalog.','https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2'),
30:('NASA HLS. Collection descriptions and download access.','https://hls.gsfc.nasa.gov/data-access-and-tools/'),
31:('ESA. Sentinel-1 radar for maritime context.','https://www.esa.int/media/sentinel-1-tracking-maritime-traffic'),
32:('Global Fishing Watch. Maritime data API capabilities and access.','https://globalfishingwatch.org/our-apis/'),
33:('Banten Bay regional sediment transport study, Tanjung Pontang.','https://doi.org/10.15578/jkn.v1i2.6614'),
34:('WALHI coalition (Nov 2023). Reported observations near Pulau Pari.','https://www.walhi.or.id/kapal-vox-maxima-kembali-beroperasi-di-perairan-pulau-tunda-dan-teluk-jakarta-koalisi-ngo-desak-penegakan-hukum-lingkungan'),
35:('BIG (2024). Annual report and product specifications for BATNAS.','https://www.big.go.id/uploads/content/produk/Laporan%20Tahunan%20BIG/LaporanTahunanBIGTahun2024.pdf'),
36:('GEBCO. Global gridded bathymetry and source identifier grids.','https://www.gebco.net/data-products/gridded-bathymetry-data'),
37:('Kurniawati et al. PDF. Kodingareng respondent and study details.','https://e-journal.fh.unmul.ac.id/mulrev/article/download/621/225/2203'),
38:('Prior LAUTARA coastal sediment diagnostic and embedded scene tables.','https://chatgpt.com/library?file_id=libfile_61a9ace26b688191a4897fac7ce72ee4'),
39:('Indonesia PP 26/2023. Management of sedimentation products in the sea.','https://peraturan.bpk.go.id/Details/249417/pp-no-26-tahun-2023'),
40:('Allen Coral Atlas. Methods, thematic layers and constraints.','https://www.allencoralatlas.org/methods/'),
41:('NOAA CPC. Global unified gauge-based precipitation archive.','https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html'),
42:('Copernicus Marine. Global ocean physics analysis and SMOC currents.','https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description'),
43:('WALHI and Greenpeace. Spermonde investigation and community record.','https://www.greenpeace.org/static/planet4-indonesia-stateless/2021/03/17185db9-gp-spermonde-report-v8.pdf'),
45:('Western Australia EPA. Technical guidance for marine dredging proposals, §§3.6.3–3.6.4.','https://www.epa.wa.gov.au/sites/default/files/Policies_and_Guidance/Technical_guidance_EIA_of_Marine_Dredging_Proposals.pdf'),
44:('Peer-reviewed Banten Bay TSS and reported extraction pairs, table 2.','https://doi.org/10.15578/segara.v14i1.7149'),
48:('NASA POWER. IMERG source, grid scale, and production latency.','https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/#imerg-integrated-multi-satellite-retrievals-for-gpm'),
46:('UCSB Climate Hazards Center. CHIRPS rainfall methods and data.','https://www.chc.ucsb.edu/data/chirps'),
47:('Lisina et al. (2025). Razdolnaya flood episode chronology, pp. 73–81.','https://tigdvo.ru/assets/files/publications/Pacific_Geography_journal/2025_1/73-81.pdf'),
}

parser=argparse.ArgumentParser()
parser.add_argument('path',type=Path)
parser.add_argument('--facts',type=Path,default=ROOT/'root/facts.json')
args=parser.parse_args()
F=json.loads(args.facts.read_text()) if args.facts.exists() else {}
a=Article(args.path,refs)
def r(*ids): return a.refs_html(ids)
def T(section,title,dek):return a.start(section,title,dek)
def B(y,t):return a.body(t,y)
def H(y,t):return a.heading(t,y)
def C(y,head,t,kind='teal'):return a.call(head,t,y,kind)
def N(y,t):return a.caption(t,y)
def A(y,f,cap,limit=232):return N(a.fig(f,y,limit),cap)
def V(y,heads,rows,widths=None,sz=9.5):return a.table(heads,rows,y,widths,sz)
def E(y):a.end(y)
def D(key,default=''):return F.get(key,default)

a.anchors('Title')
a.rect(0,-10,595.28,450,'#102e35',0)
a.para('LAUTARA 2026  /  RESEARCH ARTICLE',L,48,sz=9,lead=12,font='Bold',color='#a4d8d0')
a.para('Before the plume<br/>reaches the reef',L,106,sz=41,lead=48,color='#ffffff',font='Heading')
a.para('Evidence for siting extraction, timing work, and deciding when to verify',L,242,CW-40,sz=16,lead=23,color='#e2efed')
a.para('TUNDA  /  KODINGARENG LOMPO  /  AMUR BAY',L,370,sz=9.5,lead=12,color='#acd9d1',font='Bold')
y=470
y=a.fig('study_sites.png',y,179)
y=B(y,'<b>Design prevention into coastal work.</b> Identify the receptor before operations begin, establish what conditions can move sediment toward it, and give reviewers a way to act when the available evidence is incomplete.')
y=N(y,'Comparative public-data research for the Russia–Indonesia Maritime Hackathon. 21 November 2026. Coastlines: Natural Earth. '+r(1,16))
E(y)

y=T('Abstract','Move the decision earlier','The study traces eight choices from site selection and work timing through verification and prevention of recurrence.')
y=B(y,'<b>Objective.</b> Determine what open satellite, environmental, habitat and official records can tell a reviewer before, during and after a suspected sediment event. Tunda and Kodingareng are the main study sites. Amur Bay contributes an independent, river-influenced case.')
y=B(y,'<b>Methods.</b> Reproduce earlier results, extend the observation record, compare acquisition-level and receptor-level screening, align data and event clocks, and challenge temporal and spatial interpretations with competing sources. Retrospective observations and evidence available at decision time are tracked separately.')
y=B(y,'<b>Results.</b> '+D('abstract_result','The earlier audit found that local screening could recover observations lost by whole-tile screening. The October 2023 Tunda stop fell between observations in the scoped archives.'))
y=B(y,'<b>Interpretation.</b> The lowest-regret opportunity is to establish receptor-specific evidence requirements before work starts. Distances and regional currents can guide where to check transport. Work restrictions, compliance determinations and ecological claims require different evidence.')
y=C(y,'Decision contribution','The article gives planners, operators and reviewers a way to choose among siting, timing, precaution, field verification and follow-up. It shows which questions are supported by the public record and which would benefit from a better local record.')
y=N(y,'Keywords: sea-sand extraction, optical remote sensing, sediment transport, reef exposure, marine spatial oversight, Indonesia–Russia cooperation.')
E(y)

y=T('Introduction','Plan around where sediment can go','A viable coastal decision connects an activity, its potential pathway, a receptor, and the people who can act.')
y=B(y,'Marine dredging moves billions of tonnes of sand and other sediments globally. At reefs, exposure can vary with the magnitude, duration and frequency of suspended sediment and deposition, as well as local tolerance. This makes the transport pathway and the receptor as important as identifying an activity. '+r(2,3,4))
y=B(y,'A public reconstruction can begin after a short-lived event has passed and the original conditions are difficult to recover. The October 2023 Tunda record illustrates this timing problem: there is a dated stop and inspection, but the timing and location of the reported extraction itself are uncertain. '+r(5,6))
y=V(y,['Step','Question','Evidence that earns weight'],[
('Activity','Was work documented here and when?','Georeferenced work log, report, or authoritative record.'),
('Transport','Could material reach a sensitive area?','Local observations or scale-appropriate currents, tide, waves, or modeled connectivity.'),
('Exposure','What reaches which receptor, for how long?','Receptor-specific water measurements, defensible optical context, and a local baseline.'),
('Action','Who can decide, and with what information?','Permits and mandates, timestamps, verification records, and proportional action.')],[90,166,CW-256])
y=C(y,'What prevention means here','A planning decision can reduce exposure before an event. An observation can prompt a targeted field check. A compliance finding or determination of harm calls for evidence appropriate to that decision.')
E(y)

y=T('Study geography','Use each coast to answer a different question','Two Indonesian cases establish practical relevance. The Russian case tests how easily a river-influenced signal can resemble a sediment-event lead.')
y=A(y,'study_sites.png','Figure 1. Regional locators. Marks identify study anchors, independent of permit polygons, fishing-ground boundaries, and vessel tracks. Land: Natural Earth. '+r(16),207)
y=V(y,['Case','Geographic and historical evidence'],[
('Tunda Island','Banten shelf setting. Archived reef outlines, field literature and a documented KKP stop and follow-up inquiry. Main case window: Oct–Nov 2023. '+r(3,5,6,15)),
('Kodingareng Lompo','Spermonde reef and fishing setting. A contractor documents reclamation-related extraction in Feb–Oct 2020. Fishing-area accounts supply relevant places and dates, with one disputed coordinate-distance relation. '+r(11,12,13)),
('Amur Bay','Razdolnaya estuary, Russian Far East. The 2023 flood provides an independently documented source of freshwater influence and a demanding comparator for image-based attribution. '+r(22,23,24))],[118,CW-118])
y=B(y,'Reef footprints anchor the quantitative exposure-screening comparison in Indonesia. Fishing grounds are a distinct human-use receptor. The analysis uses documented fishing context and keeps spatial confidence visible when exact boundaries are missing.')
E(y)

y=T('Study design','Keep all eight decisions on the table','Prevention gets the most space. Case replays show how evidence changes choices across the whole sequence.')
y=V(y,['Stage','Decision','Comparison'],[
('Before work','1  Where should extraction proceed?','Distance screen versus receptor and transport context.'),
('Before work','2  When should work proceed?','Compare recurring conditions and model support at useful scales.'),
('During work','3  When does a lead justify a change?','Compare sensory cue, corroborated lead, and authorization thresholds.'),
('During work','4  What exposure gets priority?','Contrast duration and recurrence with one dramatic observation.'),
('Before / during','5  Which source should be controlled?','Compare documented activity, prior rain, regional conditions and alternative explanations.'),
('Before work','6  What must be recorded upfront?','Replay cases with and without publicly evidenced early records.'),
('During / after','7  Where and when should someone verify?','Compare sensor availability over the specific receptor and case time.'),
('Afterward','8  What prevents a repeat?','Inspect dispositions, follow-up records and what changes for future work.')],[98,207,CW-305],9.1)
y=body_note=B(y,'Each result is assigned to a measurement, a documented event, a bounded interpretation, or a scenario. That distinction is what lets the paper make a strong argument without turning a screening calculation into an ecological or legal conclusion.')
E(y)

y=T('Methods','Measure the data before trusting an inference','Source resolution, timestamps and detection rules travel with every figure.')
y=V(y,['Layer','Unit and quality check','What it can establish'],[
('Sentinel-2 / Landsat','Date and sensor. Read local SCL or QA_PIXEL values and retain footprint denominators. Deduplicate catalog items before comparison.','Local classified coverage and distinct opportunities.'),
('Reef geometry','Rasterize archived polygons in local UTM. Compare with a 1.5–3 km annulus and subdivide receptor areas.','Coverage of the mapped footprint.'),
('Rain and marine conditions','Daily satellite/gauge products and regional modeled wind, wave and current fields. Record grid and time support.','Competing explanations and plausible regional conditions.'),
('Case documents','Record event, observation and publication times where documented. Retain uncertainty in location and scope.','Official actions and documented leads.'),
('Scenario stress tests','Use transparent assumptions with independently recalculated outputs and explicit sensitivity.','How a choice changes under stated conditions.')],[111,218,CW-329],9.0)
y=B(y,'The local screening rules answer a question about the imagery footprint. They do not establish sediment concentration, underwater exposure or equipment activity. Water-quality interpretation also requires care around atmospheric effects, shallow bottoms, sunglint and uneven coverage. '+r(8,9,10,15,27))
y=C(y,'Triangulation standard','Treat the same satellite scene from two catalogs as a reproducibility check. Treat a field record and an independently acquired scene as two different observations. If two modeled products share forcing or source data, preserve that dependency in the interpretation.')
E(y)

y=T('Results · Observation I','Add dates that change the observation calendar','The aim is to observe the receptor near the relevant time. More catalog hits matter only when the local screen passes.')
y=A(y,D('optical_annual_fig','habitat_disagreement.png'),D('optical_annual_cap','Figure 2. Local coverage over the study footprints.'),229)
y=B(y,D('optical_annual_text','The legacy Tunda audit identified 52 locally qualifying Sentinel-2 acquisitions versus 29 records eligible under a 20% tile-cloud cutoff across the same 110 dates. This baseline is independently reproducible.'))
y=B(y,D('optical_annual_scope','The extended archive is treated as a scene inventory. Catalog availability, local coverage and the utility of a specific return are distinct measures.'))
y=C(y,'Decision 7 · Spend field effort on the relevant ground','Use date and footprint screening to identify which areas have observations near the report time. Mark imagery gaps explicitly so they can be routed to another observation source.')
E(y)

y=T('Results · Observation II','Give a second sensor one job: close gaps','A second mission earns its place when it contributes a qualifying opportunity on a different date.')
y=A(y,D('optical_combo_fig','habitat_disagreement.png'),D('optical_combo_cap','Figure 3. Observation opportunities across the available analyses.'),225)
y=B(y,D('optical_combo_text','The cross-mission event inventory adds Landsat opportunities for selected dates. The comparison counts distinct acquisition days and separates a sensor inventory from a local image-quality pass.'))
y=B(y,D('optical_rain_join',''))
y=B(y,'Landsat QA_PIXEL flags and Sentinel-2 SCL class codes are different screening systems. A joint calendar can use a common coverage threshold after each mission applies its own quality screen. Optical color comparisons require separate harmonization. '+r(9,10,29,30))
y=C(y,'Decision 6 · Set the baseline before the incident','A receptor-specific baseline benefits from dates with known observations, weather, and activity context. Few views in a critical season justify planning additional ways to observe, especially when the operational response window is short.')
E(y)

y=T('Results · Receptor geography','Score the place people actually need to see','An island-wide score can miss the habitat a reviewer would choose to protect or visit.')
y=A(y,'habitat_disagreement.png','Figure 4. Broad SCL classes 2, 4, 5 and 6, annulus versus archived reef polygon within 3 km. Plotted historical and baseline subsets use the available cached target-tile COG roster. Dashed lines mark the 90% screen. The all-years Tunda tally is separate. '+r(8,9,15),218)
y=B(y,D('habitat_text','The habitat audit compares readability over a fixed annulus and an archived reef footprint. Discordant dates show when the choice of footprint changes the result.'))
y=B(y,'The previous-day Tunda example illustrates the physical implication. On 26 October 2023 the broad ring score was 95.3%, but the western half of the archived reef footprint scored 75.8%. That footprint establishes a geographic sensitivity example. Contemporary reef condition and sediment dose require different evidence. '+r(38))
y=C(y,'Decisions 4 and 7 · Put the receptor in the denominator','Track coverage over the reef or documented fishing area that matters to the actual decision. A fixed-radius overview can remain useful for context.')
E(y)

y=T('Results · Image interpretation','Demand a second clue before naming a source','A strong-looking color contrast can fail an elementary physical check.')
y=A(y,'tunda_legacy_optical.png','Figure 5. Modified Copernicus Sentinel-2 examples, 22 and 24 Jul 2025. In the latter image the conspicuous brightness crosses land and water. This earlier example is reused as a negative check on source attribution. '+r(38),215)
y=B(y,'The prior analysis found an east-to-west brightness contrast that changed direction across dates, with its strongest example extending over land. This is compatible with an atmospheric or surface artifact and weakens a sediment-only interpretation. It remains useful as a quality-control example for the expanded study.')
y=B(y,'Natural causes are plausible too. Regional Banten Bay modeling illustrates river-sediment transport. A separate Banten Bay field dataset reported elevated suspended solids on a date with zero production recorded for the operator under study. Neither case identifies the source of a particular Tunda signal. '+r(33,44))
y=C(y,'Decision 5 · Separate source hypotheses from actions','A visual clue can justify checking vessel or environmental context. Source-specific control needs evidence tying the activity, pathway, and receptor together.')
E(y)

y=T('Results · Tunda event','Build the record before the response clock starts','The 27 October 2023 government action is documented. The public record leaves the sediment release time and location open.')
y=A(y,'tunda_event_three_clocks.png','Figure 5a. Public sensor inventory and two product lineages for the 26 Oct Sentinel-2 acquisition. '+r(8,28,29,30),192)
y=V(y,['Date / clock','Evidence','Meaning for a reviewer'],[
('27 Oct','KKP reported a stop and inspection. About 24,000 m³ of sand was aboard.','Confirmed inspection and cargo observation. Origin and permit issues were described as suspected.'),
('29 Oct','KKP published its release.','Public documentation of the agency account followed the action by two calendar days.'),
],[83,211,CW-294],8.8)
y=B(y,'The scoped inventory returned six Sentinel-2, four Landsat and three Sentinel-1 dates. None was 27 Oct. Earth Search metadata identify a 26 Oct archived version. Today’s Copernicus product was reprocessed later. Neither establishes receipt by a reviewer. '+r(5,6,28,29,31))
y=C(y,'Decisions 3 and 6 · Specify evidence that can arrive in time','Record work location and time as operations happen. Give a reviewer an independent path to assess location-specific leads while a contemporaneous image is unavailable.')
E(y)

y=T('Results · Tunda environment','Check whether rain offers a competing pathway','Weather context should change the order in which explanations are checked. Transport and source still depend on local evidence.')
y=A(y,'rainfall_multisensor.png','Figure 6. Tunda and Kodingareng, full 2025 and Nov–Dec subset. Site-days with mainland IMERG proxy rain ≥10 mm. Broad local screen ≥90% on either mission. '+r(8,10,17,18,41,46),200)
y=B(y,D('tunda_rain_text','Public environmental records supply antecedent rainfall context. Unlike an extraction log, precipitation identifies a potential input to a transport pathway.'))
y=B(y,'On 4 Nov, all three products indicated at least 24 mm of regional rain. Activity that day is unresolved. Across both islands in Nov–Dec 2025, only <b>1 of 72</b> higher-rain site-days qualified with either optical mission. Of the rest, 49 had no acquisition in these inventories and 22 had acquisitions below the local screen. In 2025, acquisition rates were similar on higher- and lower-rain days (31.5% and 30.7%). Among dates with an acquisition, 16.0% and 35.9% passed respectively.')
y=C(y,'Decision 5 · Treat weather as a discriminating question','Ask whether the anomaly makes sense after regional rain, wind or wave changes, and where a river-linked pattern would appear. Keep an activity-linked hypothesis alive when the record supports it.')
E(y)

y=T('Results · South Sulawesi case','Protect the fishing place people actually use','Kodingareng shows why historical project scope, fishing activity and geolocation have to be recorded separately.')
y=V(y,['Evidence','What it establishes','Consequence for analysis'],[
('Boskalis project record','Approx. 11 million m³ transported for phases 1B–1C. Contractor dates marine extraction Feb–Oct 2020.','Supports a project-period comparison. Daily release times and precise borrow geometry need separate evidence.'),
('Fisher and community records','Fieldwork and community accounts document contested access and reported effects.','Identify fishing use as a separate receptor and preserve the accounts as qualitative evidence.'),
('12–13 Sep reported incident','The published police account gives a point about 2.24 km from the island anchor and a narrative distance of 11 miles. Its weekday and date also disagree.','Keep the disputed coordinate out of source-to-receptor transport distances.'),
('DPR visit report, 2024','Reports SDKP investigated, examined firms and heard fishers. It records no violation found in the reported follow-up.','Regulatory disposition has a defined scope. Ecological and livelihood outcomes require their own evidence.')],[116,191,CW-307],9.1)
y=B(y,'A near-reef analysis can be spatially tidy while the actual point of concern is a fishing ground farther away. This case preserves that distinction. It supports a request for dated, bounded fishing-use evidence before ranking which fishing area could be affected. '+r(11,12,13,14,43))
y=C(y,'Decisions 1 and 8 · Retain the receptor and the follow-up scope','Spatial planning needs a defensible receptor location. Incident closure needs a clear statement of what was investigated, what was established and which consequences were outside that finding.')
E(y)

y=T('Results · South Sulawesi environment','Give historical comparisons a season-matched baseline','The project period spans multiple weather conditions. Compare candidate episodes with ordinary conditions from the same parts of the year.')
y=A(y,D('koding_rain_fig','habitat_disagreement.png'),D('koding_rain_cap','Figure 7. Historical and baseline contrasts around Kodingareng.'),222)
y=B(y,D('koding_rain_text','Rainfall observations and regional forcing provide plausible competing environmental context. Contractor month ranges establish activity at project scale and leave individual dates unresolved.'))
y=B(y,'During Feb–Oct 2020, 54 Sentinel-2 and 17 Landsat island-footprint QA dates were measured, with 26 and 10 broad passes respectively. The reported 12 Sep incident date had no acquisition in either scoped inventory. Because the published day is uncertain and the project envelope is not a daily log, the views cannot confirm whether imagery captured a particular work period.')
y=C(y,'Decisions 2 and 5 · Require the operating clock','For work-window screening, join the conditions to the actual operating date, time and location. Until that record is available, use historical distributions to identify which conditions merit closer local analysis.')
E(y)

y=T('Results · Marine conditions','Use regional currents to decide where to look closer','The two Indonesian cases contain directional information at regional scales. Local pathways need finer or field-supported evidence.')
y=A(y,'marine_current_seasonal.png','Figure 8. Monthly share of daily regional GLORYS12 current vectors with an eastward component, 2019–25. Study-year emphasis is labeled in the panels. '+r(21),216)
y=B(y,D('marine_text','Currents can vary across dates and nearby grid cells. A regional result can establish a context for local measurement.'))
y=B(y,'The 92,052-vector reference series covers both sites, nine cells, two depths and 2,557 UTC dates. At Kodingareng, June 2020 near-surface and deeper eastward shares were 13.3% and 86.7%; comparison-year June medians were 41.7% and 83.3%. The grid can guide local checks. It cannot set reef-scale boundaries. '+r(3,4,20,21,42))
y=C(y,'Decisions 1 and 2 · Spend local modeling effort where it changes the choice','Use the regional pattern to screen alternative sites or periods. Prioritize local pathway checks where changing assumptions would reverse the ordering.')
E(y)

y=T('Results · Transparent scenarios','Test whether “nearest reef first” is robust','A simple transport scenario exposes the decision sensitivity before anyone spends effort on a detailed model.')
y=A(y,'transport.png','Figure 9. Analyst-designed kinematic scenarios. Panel A multiplies a constant speed by elapsed time. Panel B uses fictional geometry to illustrate how distance and direction can rank receptors differently.',214)
y=B(y,'At 0.10 m/s a parcel would travel 2.16 km in six hours under a constant straight-line assumption. At 0.25 m/s the distance is 5.40 km. That 3.24 km difference is already larger than the width of the 1.5–3 km annulus used for observation screening. It shows how a convenient observation footprint can diverge from a plausible transport scale.')
y=B(y,'The figure is a stress test only. It omits mixing, settling, return flows, and the relationship between surface velocity and exposure near a reef. The source and receptors in the geometry panel are fictional. The Kodingareng coordinate conflict prevents a corresponding real source-to-receptor calculation.')
y=C(y,'Decision 1 · Keep a transport check in siting','Ask whether a plausible current direction puts a more distant receptor on-path. Use a model or measurements with defensible nearshore support before translating this question into setbacks or operating conditions.')
E(y)

y=T('Results · Amur Bay','Use a river-influenced coast to challenge attribution','The Russian case lets the team check its reasoning in a setting with independently documented high river flow.')
y=A(y,D('amur_scene_fig','transport.png'),D('amur_scene_cap','Figure 10. Amur Bay analysis.'),239)
y=B(y,D('amur_scene_text','The Razdolnaya estuary provides an independently documented flood context for optical observations.'))
y=B(y,'The flood and optical contrast are separate observations. A later visible contrast in the bay can be consistent with a river-influenced event while leaving source apportionment and concentration open. The case offers a useful alternative explanation to carry into the Indonesian analysis. '+r(22,23,24,27))
y=C(y,'Decision 5 · Compare plausible explanations across coasts','Record rainfall or river conditions alongside the image and inspect how the signal sits relative to land, river outlets and reference water. Apply the same evidence questions to suspected dredging events.')
E(y)

y=T('Results · Russia comparison','Keep strict screens and partial observations visible','Changing the coverage rule can change which story the image series appears to tell.')
y=A(y,D('amur_timeline_fig','transport.png'),D('amur_timeline_cap','Figure 11. Amur Bay event timeline.'),227)
y=B(y,D('amur_timeline_text','Coverage and event timing are audited independently.').replace('Four acquisitions fell','Four acquisition dates fell'))
y=B(y,D('amur_archive_text','A cross-coast result transfers as an interpretation pattern. It does not transfer an absolute water-color threshold between sites.'))
y=C(y,'Decision 7 · Use a partial observation for the part it covers','Preserve the individual zone result when a whole-area rule fails. A reviewer can use that view to narrow a check and state which area still needs independent evidence.')
E(y)

y=T('Results · Evidence replays','Give a lead the next step it can support','The same information can justify checking a place while leaving a pause, violation or impact determination unresolved.')
y=V(y,['Case and information','What becomes possible','What remains open'],[
('Tunda: official stop, cargo observation, no exact-day date in the scoped sensor inventory','Record the inspection and assign follow-up to a documented location and responsible authority.','When and where the reported extraction occurred. Whether the closest image would have reached the reviewer.'),
('Kodingareng: project-period record, fisher reports and conflicting printed incident location','Record the fishing concern and prioritize reconciling geography and work records.','Which mapped path leads from a verified borrow area to a specified fishing ground.'),
('Amur Bay: high-water documentation, rainfall corroboration and later optical contrast','Use the contrast to examine freshwater influence and quality-screen limits.','Whether a specific visible feature can be quantitatively apportioned among sources.')],[142,189,CW-331],9.1)
y=H(y,'A graduated decision sequence')
y=B(y,'An observation can create a time-stamped lead. A corroborated lead can focus field verification. A temporary operating change belongs with the actor who has authority and a documented basis. A formal finding requires the applicable evidence and procedure. A public satellite image can contribute at several points in this sequence.')
y=B(y,'The current Indonesian framework describes indirect supervision, field examination and supporting records. The historical cases were interpreted under their dated context. As a design comparison, Western Australia’s dredging guidance illustrates staged monitoring and management responses. The report does not import a numerical trigger or jurisdiction. '+r(7,39,45))
y=C(y,'Decision 3 · Specify an action before specifying a threshold','Decide which action a signal can support. Associate the rule with a known owner and required corroboration, including what would restore confidence or allow normal work to resume.')
E(y)

y=T('Discussion · Prevention choices','Make prevention a set of choices people can own','The four upstream decisions define what coastal teams can change before exposure or escalation.')
y=V(y,['Decision','Act on this','Evidence gap that matters'],[
('1 · Siting','Verify the source geography, locate the receptor, and screen connectivity before comparing distance setbacks.','Verified work polygon and local transport evidence. The Kodingareng coordinate disagreement changes what can be mapped.'),
('2 · Work timing','Compare work periods under relevant environmental conditions and identify where scheduling might alter receptor connectivity.','Time-stamped activities and locally informative current, tide and wind measures. Regional direction changes alone cannot set a schedule.'),
('3 · Precaution','Use a graduated lead, verification and authorization sequence. Specify what prompts review, who can act, and when to reassess.','Case-level evidence of authority, standards and a practical route to act while the event is still relevant.'),
('4 · Exposure priority','Design records around a receptor-specific history of intensity, duration and recurrence. Pair satellite opportunities with another observation path where needed.','A defensible field or local optical measure and an ecological baseline. Percentages that describe image coverage cannot establish sediment dose.')],[112,208,CW-320],9.2)
y=B(y,'These choices can reinforce one another. A verified polygon makes transport screening possible. An operating clock makes timing analysis possible. A clear escalation process allows a reviewer to respond to uncertainty. Receptor-specific observations let someone later distinguish visibility from exposure.')
y=C(y,'Start with the prerequisite that multiple decisions share','A trustworthy record of place, time, receptor and decision authority improves siting, scheduling, precaution and exposure assessment together.')
E(y)

y=T('Discussion · Verification and recurrence','Make the next case easier to resolve','Four further decisions concern the quality of the record and the action it supports.')
y=V(y,['Decision','Act on this','Evidence gap that matters'],[
('5 · Source control','Keep activity, river inputs, weather, seabed and optical effects as explicit explanations. Prioritize a control action where the mechanism is consequential and supported.','Spatially and temporally matched evidence tying an input to transport and receptor exposure.'),
('6 · Baseline records','Save work and observation clocks, the footprint, baseline conditions and decision owner before the work period. Version important data layers.','Earlier availability, especially original product and operator records. Current catalog metadata can describe a later reprocessed item.'),
('7 · Field verification','Use the exact area of concern and closest defensible observations. Bring another source to the specific blind spot.','Local visibility or alternative observation availability, plus the practical inspection route.'),
('8 · Recurrence','Track regulatory disposition, work changes and ecological or livelihood conditions on separate timelines.','Comparable follow-up measures. A decision in one track can leave the other two unresolved.')],[112,208,CW-320],9.2)
y=B(y,'Tunda and Kodingareng show different documented action histories. The Tunda account gives a dated stop and investigation step. The Kodingareng record contains a later follow-up disposition reported to Parliament. A judge can use each to understand the relevant decision without inferring an outcome the source does not measure. '+r(5,6,14))
y=C(y,'Preserve what would change the next decision','The useful archive connects the concern, affected place, contemporaneous evidence, decision, reason, and any subsequent measurement or work change.')
E(y)

y=T('Discussion · Technology and bilateral fit','Share the method. Calibrate the coast.','Indonesia can use the approach on its own. A Russian counterpart gives the method an independent transfer test.')
y=V(y,['Portable across sites','Requires local input'],[
('Explicit definitions for activity, observation, product availability and decision time.','The clock at which an agency, operator or community actually receives reliable information.'),
('Footprint-level visibility and comparable scene checks, including the area of interest and independent observations.','Current habitat boundaries, documented fishing grounds and site-specific viewing limitations.'),
('A consistent way to separate a lead, source corroboration and authorization.','Operating rules, relevant authority, tolerance, tidal effects and baseline measurements.')],[CW*.48,CW*.52])
y=B(y,'The proposed bilateral research role is to agree on a comparable observation protocol and independently rerun the source-ambiguity checks at a river-influenced coast. The governments’ maritime research and training agenda offers a relevant policy channel. The Pacific Oceanological Institute has relevant ocean-color and remote sensing expertise. The Amur Bay analysis in this study uses public evidence and does not depend on a partnership agreement. '+r(22,24,25,26))
y=B(y,'Existing tools already cover useful parts of the problem. UNEP Marine Sand Watch contributes vessel-linked dredging context. Radar contributes independent surface observations. NASA and Copernicus archives supply repeatable imagery and modeled context. Value for a coastal reviewer comes from joining those inputs to the choice and the receptor. '+r(2,28,30,31,32))
y=C(y,'Bilateral research success','An independent analyst starts from the same data definitions, reproduces the observation result, and explains a meaningful difference in interpretation or decision at their coast.')
E(y)

y=T('Conclusion','Give reviewers evidence while they can still act','Coastal sediment management improves when monitoring is designed around the action it serves.')
y=B(y,'The strongest direct evidence concerns observation and reconstruction: where coverage was available, what a second satellite added, how receptor footprints changed which scenes passed, and which records existed around the time of a known event. That is enough to demand a better evidence design before marine work begins.')
y=B(y,'The prevention questions point to decisions worth comparing. Siting depends on verified locations and plausible transport toward receptors. Scheduling depends on the operating clock and reliable local conditions. Escalation depends on what a signal establishes and who has authority. Follow-up depends on preserving what happened and which outcomes were actually measured.')
y=B(y,'Important uncertainties are specific. The public sources yield no verified extraction footprint for the Tunda stop and no reconciled point for the reported Kodingareng incident. The regional grids leave reef-scale transport unresolved. Optical signals and stakeholder reports matter as evidence with their own scope, including where an alternative explanation survives.')
y=C(y,'The proposition for LAUTARA','Make prevention decisions at the scale of the place people want to protect. Set the observation and record requirements before work starts. When a lead arrives, connect it to a proportionate action and keep a traceable record for the next event.')
y=N(y,'The article leaves the eventual product or intervention open. The eight decisions can now be compared from the same evidence base.')
E(y)

y=T('Reproducibility and references','Follow the claims back to the data','The companion bundle contains source URLs, inventories, figure data, scripts, and a map from headline claims to files.')
y=B(y,'Start with <b>README.md</b> and <b>CLAIMS.md</b> in the companion archive. The figure crosswalk lists the input and script for each exhibit. The included data tables preserve date, site, and sensor or product where applicable. The source manifest records the core endpoints and key exclusions. Scripts use published APIs or cached data as noted in the bundle.')
y=B(y,'Study bounds: use the exact geographic definitions and dates in the inventories. Some archive products are reprocessed. Historic reef polygons represent mapped footprints. Raster quality flags describe observation support. The work uses no proprietary extraction log, confidential field record, or validated reef-concentration time series.')
y=H(y,'Core study and observation sources')
y=a.refs_columns(list(range(1,24)),y)
E(y)

y=T('References','Connect the literature to the decision','Clickable references identify the records, methodological sources, and policy context used in the study.')
y=a.refs_columns(list(range(24,49)),y)
y=C(y,'Data reuse','Use the product IDs and provenance in the companion archive to obtain source assets directly. Cached CSVs are documented derivatives. Original public imagery and habitat sources retain provider attribution and access terms.',y)
E(y)
assert a.idx==25
a.c.save()
