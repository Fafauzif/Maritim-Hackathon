# The_Ocean_Has_Floors

Extracted text by printed PDF file page. Use the original for tables, reading order, diagrams and page geometry.

## PDF page 1

LAUTARA   /   THE OCEAN HAS FLOORS
TEAM CONCEPT BRIEF
THE PROBLEM
Coastal observation  /  Russia × Indonesia
1 / 7
The Ocean Has Floors
A survey-planning workspace for government coastal monitoring teams
An officer reviewing proposed sand extraction needs a survey plan before work
begins. In this internal 3D map, the officer inspects water currents at different
depths, checks available observations and tells the crew where to sample, how
deep to go and why.
KODINGARENG  /  FEBRUARY–OCTOBER 2020
Days with an eastward component in the regional current model
Near surface · 0.5 m
139 / 274 days
Deeper layer · 9.6 m
230 / 274 days
Matching the two layers day by day reveals 96 days when the deeper layer had an
eastward component and the surface layer had a westward one. A crew choosing a
depth could be asking a materially different question about the same place.
These daily counts describe one model cell roughly 9 km across. Testing whether sediment reached a
particular reef would also require local observations and a dated record of the work.
Team research article, p. 7 · Copernicus GLORYS12 product

Links embedded on this page

- https://chatgpt.com/library?file_id=libfile_a8a03db5ba0c81919c3c2cf5df53d7c5&account_id=personal
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description

## PDF page 2

LAUTARA   /   THE OCEAN HAS FLOORS
TEAM CONCEPT BRIEF
PROPOSED OPERATOR INTERFACE
Coastal observation  /  Russia × Indonesia
2 / 7
The case opens on the coast
The officer opens a proposed works case and sees the whole area from above. Select a
station, change the viewing depth, then decide what to ask the field crew to measure.
COASTAL MONITORING    /    Kodingareng
Draft case  ·  KR-01
S-01
N
STATION  S-01
Viewing depth
0.5 m
9.6 m
Model date
16 Apr 2020  ·  UTC
GLORYS12  /  daily mean
0.093 m/s   ·   264°
Regional cell  ·  ~9 km
+ Request field check
MAP KEY
Station
Proposed works
Reef outline
Modeled current
Overhead view
Draw section A–B
Compare depths
Design mockup. The island, reef, station and work boundary illustrate the interface. The dated current reading is from the
archived regional model.
What does “viewing depth” change?
The coast stays in place. Selecting a deeper layer shows how the water there was estimated to
move on the chosen date. An officer can compare layers from above, then draw a section
wherever the shape of the seabed matters to the sampling plan.

## PDF page 3

LAUTARA   /   THE OCEAN HAS FLOORS
TEAM CONCEPT BRIEF
TWO STATES OF THE SAME OPERATOR SCREEN
Coastal observation  /  Russia × Indonesia
3 / 7
Change the depth. Keep the date.
Kodingareng · 16 April 2020. Both views use the same camera, proposed station and
regional model cell. The selected depth changes the current reading.
VIEWING DEPTH     0.5 m
S-01
N
MODELED CURRENT   /   DAILY MEAN
0.093 m/s   ·   264°
Toward the west
VIEWING DEPTH     9.6 m
S-01
N
MODELED CURRENT   /   DAILY MEAN
0.074 m/s   ·   045°
Toward the northeast
The surface estimate would point the officer west. At 9.6 m the estimate points
northeast. To check whether this change occurs locally, select Request field check and
ask for a current profile at S-01.
~9 km cell
How local is the arrow?
One arrow summarizes the whole grid cell, centered at 5.1667° S, 119.2500° E. The
dot marks the illustrative station inside it. A current profiler can test the model at
the station.
Source archive · marine/glorys_daily.csv. Bearings are clockwise from north.

Links embedded on this page

- https://chatgpt.com/library?file_id=libfile_b8704091df1c819189fa17cf61011304&account_id=personal

## PDF page 4

LAUTARA   /   THE OCEAN HAS FLOORS
TEAM CONCEPT BRIEF
SECTION VIEW AND FIELD REQUEST
Coastal observation  /  Russia × Indonesia
4 / 7
Take a slice through the station
Draw A–B through S-01. The camera turns along that line and keeps the jetty on the left. In
section view, the officer sets a proposed sampling depth and saves it in the case.
S-01
A
B
N
Proposed sample depth    9.6 m
A
B
Overhead   /   Select section A–B
Section A–B   /   Set target depth
The two drawings show the proposed interaction. The section in the working app would use the selected line and a
bathymetry grid to draw the seabed.
From model evidence to a field action
A current profiler records motion at depth. A bottle supplies water for sediment analysis. The requested
instrument follows the question the officer needs to answer.
Select the site, date
and sampling question
Compare modeled cur-
rents at two depths
Matching local measurement?
Compare the recorded value
with the mod-
el at that depth
Choose the
depth, instrument
and time for a field check
Save the evidence
and next action
in the crew’s field brief
Yes
No

## PDF page 5

LAUTARA   /   THE OCEAN HAS FLOORS
TEAM CONCEPT BRIEF
CASE HANDOFF
Coastal observation  /  Russia × Indonesia
5 / 7
What goes to the field crew?
A supervisor reviews the proposed station and issues a versioned brief. When the boat
returns, the field lead attaches the readings and sample IDs to the same case.
EXAMPLE FIELD BRIEF    /    DRAFT FOR REVIEW
KR-01 Kodingareng baseline survey
Station
S-01 · 5.1550° S, 119.2620° E (illustrative WGS84 waypoint).
When
Proposed pre-work visit, 08:00–10:00 WITA. Field lead confirms the date and local
water depth before deployment.
Current check
Run a current profiler at S-01. Compare readings near 0.5 m and 9.6 m below
surface where both depths are submerged.
Sediment baseline
Collect paired water bottles at the two target depths if feasible. Log actual depth,
time and sample ID for each bottle.
Review and return
Coastal monitoring supervisor reviews the plan. Field lead returns the profile and
lab results to case KR-01.
Planning example only. Coordinates and field instructions illustrate the handoff. Model evidence attached: GLORYS12 daily
mean, 16 April 2020, reference cell on page 3.
How two offices could use the same workflow
An Indonesian reviewer could share the Kodingareng plan. An Amur Bay reviewer could compare its
depth choices with a published local survey that sampled near the surface and above the bed. Each
office records what it would change and why. Tunda offers a further case for planning a reef baseline
before proposed work.
Tunda reef survey · Amur Bay sampling methods

Links embedded on this page

- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.3390/jmse9090953

## PDF page 6

LAUTARA   /   THE OCEAN HAS FLOORS
TEAM CONCEPT BRIEF
SUGGESTED WEB ARCHITECTURE
Coastal observation  /  Russia × Indonesia
6 / 7
How the browser experience works
Prepare dated coastal layers in advance for fast inspection. Keep case records and
review decisions in an access-controlled service. The map and case file share the
selected station, depth and source.
Web interface
React + TypeScript
Display the case, station, date, evidence and draft plan. Offer both
the cable gesture and keyboard depth entry.
3D scene
Three.js + React Three Fiber
Switch depth layers in the overhead view. Pivot around A–B, clip
the water and draw the exposed section, with the boat anchored
to its map position.
Art assets
Blender  →  glTF / GLB
Model low-detail boats, jetties and buildings. Optional Blender
MCP support helps artists place or revise objects during
production. Export approved meshes to the web app.
Scientific processing
Python + Xarray + Rasterio
Keep native grid cells and depth levels. Convert selected model
dates, local terrain and image masks into compact assets with
source and units attached.
Case records
FastAPI + PostgreSQL
Use agency sign-in and role-based access. Version survey plans,
record sign-off, attach field results and export the issued brief with
its evidence sources.
First build test
Can a colleague open an issued brief, recover its exact source and depths, and attach measured
results to the correct station?
React Three Fiber · Community Blender MCP integration

Links embedded on this page

- https://r3f.docs.pmnd.rs/getting-started/introduction
- https://github.com/ahujasid/mcp-for-blender

## PDF page 7

LAUTARA   /   THE OCEAN HAS FLOORS
TEAM CONCEPT BRIEF
IMPLEMENTATION REFERENCE
Coastal observation  /  Russia × Indonesia
7 / 7
The datasets behind the scene
Fetch public data when preparing the case layers. Bundle the source ID, acquisition date, units,
grid size, quality flags and access terms with each layer. Linked documentation below is the
starting point for integration.
Currents by depth
Copernicus Marine Toolbox subset API · GLORYS12 daily means. Select uo and
vo (m/s) by time, depth and bounding box. Dataset:
cmems_mod_glo_phy_my_0.083deg_P1D-m.
Seabed and habitat
BIG BATNAS · Indonesian bathymetry, 6 arc-seconds. GEBCO 2025 · bilateral
terrain, 15 arc-seconds. Use Allen Coral Atlas mapped reef extent where
coverage permits. Check depth datum before joining layers.
Satellite surface view
Copernicus Data Space STAC for Sentinel-2 and USGS Landsat STAC for Landsat
8/9. Search the reef footprint and date, then screen cloud, shadow and glint over
that footprint.
Local measurements
NOAA WODselect for profiles and NOAA GOCD for acoustic current records.
Match variable, coordinates, depth and date. Raw turbidity profiles from the
Amur survey still need verification.
Rain, runoff and
waves
NASA GPM IMERG via earthaccess for catchment rain. Compare GloFAS
discharge where the river is represented and ERA5 wind and waves to
investigate other explanations for surface brightness.
FIRST DATA CHECK
Pick one Kodingareng day and two wet model depths. Reproduce both current vectors from the
source file. Then query for a nearby current profile and record the match or the gap. This gives
the team one complete, traceable scene to build around.

Links embedded on this page

- https://help.marine.copernicus.eu/en/articles/8283072-copernicus-marine-toolbox-api-subset
- https://big.go.id/en/content/product/demnas
- https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2025-grid
- https://allencoralatlas.org/methods/
- https://documentation.dataspace.copernicus.eu/APIs/STAC.html
- https://www.usgs.gov/landsat-missions/spatiotemporal-asset-catalog-stac
- https://www.ncei.noaa.gov/access/world-ocean-database-select/dbsearch.html
- https://www.ncei.noaa.gov/access/search/datasets/standard-product-global-ocean-currents-database/
- https://gpm.nasa.gov/data/imerg
- https://earthaccess.readthedocs.io/en/latest/
- https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical?tab=overview
- https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels

