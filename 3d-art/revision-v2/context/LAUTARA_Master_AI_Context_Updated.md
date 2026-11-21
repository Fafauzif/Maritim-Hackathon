# The Ocean Has Floors
## LAUTARA 2026 · Master AI context pack · 21 November 2026 · 3D production handoff revision

### Start with the officer's decision

An Indonesian coastal monitoring officer receives a proposal to extract sand near a reef. Before work begins, the officer needs a baseline. A dot on a map tells the skipper where to stop. It leaves the crew with a second question: how far down should they measure? **The Ocean Has Floors** is a proposed internal web app that helps the officer answer that question. The officer opens a bird’s-eye map, selects a station and date, and changes the viewing depth. A current arrow at the surface can point west while the arrow farther down points northeast. The officer can see where those estimates come from, look for a matching local measurement and request the measurements that would settle the question. A supervisor issues the plan, and the crew brings its readings back to the same case. Indonesia and Russia can use that same process at different coasts and compare what each team would do.

**Project state.** The research, source snapshots, analysis scripts, figures, seven-page product brief and static operator mockups exist in this context pack. The separate [Maritim-Hackathon repository](https://github.com/Fafauzif/Maritim-Hackathon) contains a completed first 3D art pass for Kodingareng Lompo, Pulau Tunda and the Razdolnaya estuary in northern Amur Bay, plus a globe and shared kit. Its art checker passed 33 of 33 file checks at commit `a0295d3`. The next work is a full art revision in the owner's local DeepSeek Harness with Blender MCP. The production plan is ready for that run. The revised art and final friend handoff are pending local execution. The teammates own the app and game behavior. Agency adoption, field validation and partner commitments remain proposed. The seven-page PDF in `01_Product/` is the product specification. Pages 2–5 show the intended flow from opening the case to issuing the field brief.

**Routing for the next collaborator.** For art execution, extract the DSH planning ZIP at the local repository root and open `3d-art/revision-v2/START_HERE.md` and `CONTINUE_PROMPT.md`. For app implementation, use the product brief for the operator flow and the final art manifest produced by DSH for import paths, transforms and anchors. For scientific claims, use the original data and Appendix D. The archived mockups, first art delivery and future runtime scene are independently versioned.

**If an AI can accept one document:** upload this Markdown. It includes the handoff, case logic, competition constraints, implementation notes, source and decision ledgers, and a page-by-page text appendix for the seven-page brief and all three team research reports. With file access, open the PDFs alongside it for figures and the original archive for data. The individual text companions retain links that ordinary PDF copy-and-paste can drop.

### How the team arrived here

| Stage | Question or correction | What carried forward |
|---|---|---|
| Competition framing | Is marine sand extraction a big enough problem? Could an Indonesian case travel? | Establish global relevance with scoped figures, investigate one place closely, and test claims against other coasts. Never generalize a case into national prevalence. |
| Partnership framing | Can the concept stand on its own and gain something concrete from bilateral cooperation? | Indonesian teams can use it themselves. A Russian counterpart can independently rerun evidence checks and compare survey choices in a river-influenced bay. |
| Initial audit | Which observations let a reviewer check a site? | Actual reef coverage, event chronology and missing field data matter. The pilot found an observation constraint. It did not diagnose every institutional delay. |
| Expanded research | Can we act before an incident, and are there decisions beyond dispatching inspectors? | Eight decisions span siting, timing, intervention, exposure, source control, upfront records, verification and follow-up. Keep the evidence base broader than the selected product. |
| Brainstorm | What can judges discover for themselves? | Five design concepts, international benchmarks and an early combination explored the full arc. The desired reaction was “I just saw something I’d never noticed before.” |
| Selection | How could “the ocean has floors” work with realistic data and a memorable interaction? | Make the vertical dimension visible. Fix the date and location, switch native model depths, and let the difference change the question a field crew receives. |
| Product correction | “First and foremost a government/internal kind of thing.” | Use an agency case, an evidence record, a supervisor and a field crew. Preserve the inviting visual style and direct manipulation. |
| Interface correction | The operator should see the coast from above and be able to play with the depth. | The overhead map is the landing screen and the primary work surface. A section is a deliberate second action. The latest PDF shows before/after operator states and a specimen field brief. |

### Competition and audience

LAUTARA is the Russia–Indonesia Maritime Hackathon. The official guide names Russian House Jakarta, Maritim Muda Nusantara and Generasi Energi Bersih (GenB) Indonesia. Its main theme is the future of maritime affairs of Russia and Indonesia. The best fit is **Sub-theme 1, Promoting Sustainable Maritime Solutions of Young Generations**, particularly marine environmental protection and maritime technology and innovation. Sub-theme 2 is Russia–Indonesia maritime security cooperation. Environmental monitoring is a description of this project’s focus.

The guide asks the initial video to answer **“What do you think is the most important challenge facing maritime affairs today, and why?”** Teams consist of 4–6 Indonesian participants, aged 16–25, representing the same eligible institution or organisation. The video is 2–5 minutes, entirely in English, accessible to anyone with the link. The supplied guide schedules registration for 3–22 November 2026, six finalists for 2 December, and the in-person final for 12 December at Russian House Jakarta. Use its actual dates and distinguish a competition entry from a commissioned government deployment. An English product walkthrough alone would leave the first-round question unanswered.

| Proposed weight in the supplied guide | How to earn it with this project |
|---|---|
| Issue analysis and understanding · 30% | Start with the consequence of sending one crew to one depth. Show an actual same-day model pair. Ask what information would change the plan. |
| Originality and innovation · 25% | Let the judge change depth in the same scene and translate the discovery into a field request. A photogenic map by itself cannot show this. |
| Potential impact and relevance · 25% | Show the crew brief, review and return of field readings. Describe improvements that a pilot could measure and the specific role of each coast. |
| English communication and presentation · 20% | One plain question per scene. Say “which way the water moves” before “daily modeled velocity.” Keep units, source and uncertainty visible. |

The guide calls these weights proposed and subject to committee confirmation. Its recommended video structure moves from team and challenge through evidence and causes to an initial direction and closing. The guide’s instructions outrank general innovation or business-case coaching.

### Problem analysis and evidence boundaries

Sand extraction can place fine material into the water. Whether it reaches a reef or fishing area depends on the disturbed material, actual location and timing, water movement, settling, duration and background sources. Showing that an activity occurred, that a vessel had cargo, that the water looked bright, and that a reef experienced a damaging dose are four different evidentiary steps. A government team can improve how it plans the next measurement even when some steps remain open.

UNEP’s global estimate cited in the diagnostic is roughly 4–8 billion tonnes of sand and other sediments dredged from marine and coastal environments per year. This covers more than sand mining and more than unlawful operations. The contractor’s approximately 11 million cubic metres for two phases of Makassar New Port is a project volume. The figures answer different questions and use different units. Tunda is valuable because it permits a close reconstruction of an observation problem. The case does not estimate how often extraction occurs nationally or what fraction is illegal.

| Issue-tree branch | What the team established | What would test the unresolved part | Design consequence |
|---|---|---|---|
| Exposure | Regional models change with depth, location and date. Reefs and fishing grounds are spatially specific. | Verified source geometry and activity time, local flow, sediment characteristics, baseline and follow-up samples. | Give the officer a depth-aware, receptor-specific survey plan. |
| Observation | A scene can pass an island-level quality screen and fail over the reef. Some dates lack a qualifying acquisition even across missions. | Field or independent observations at that footprint, time and depth. | Show observed, screened out and unobserved separately. Let the officer request a field check. |
| Attribution | Russian flood and pre-flood images can produce similar-looking west/east brightness patterns. Indonesian public accounts leave location ambiguities. | Independent activity logs, river/tide/weather context, calibrated observations, matched controls. | Keep competing explanations open and record the evidence that could distinguish them. |
| Response and follow-up | Public actions and document dates can be reconstructed for some cases. Actual agency receipt, dispatch delay, recovery and closure are often unobserved. | Case intake, decision and field logs with owners, times and dispositions. | Keep an auditable case and return measurements to it. Test operational value with real officers. |

Validated here means a defined calculation or source constraint survived a check on these data. The root cause of local reef damage, the prevalence of agency workflow failures, willingness to adopt, and the reason a particular officer acted are separate research questions. The independent-source issue matters: two public copies of one acquisition or two related ocean models may reinforce a consistency check but provide limited independent corroboration.

### Eight decisions preserved from the expanded audit

| # | Decision | Forward action and evidence boundary |
|---|---|---|
| 1 | Where should extraction proceed? | Compare verified boundaries, protected places, fishing use and plausible pathways. Escalate disputed coordinates for verification before spatial joins. A mapped distance alone cannot certify a safe site. |
| 2 | When should work proceed? | Compare seasonal conditions, multiple depths and neighboring cells. Obtain local baselines and locally authorized operating criteria before naming a work window. |
| 3 | When should a lead change operations? | Tie corroboration and named decision authority to graduated actions. A plausible cue can trigger a check well before evidence supports a regulatory conclusion. |
| 4 | Which exposure deserves attention first? | Protect the receptor that matters and measure duration and recurrence. A single bright frame or a large cargo tells little about the dose a reef received. |
| 5 | Which source should be controlled? | Check plausible extraction, river, rainfall and resuspension pathways against dated evidence. Keep the alternative that still fits. |
| 6 | What must be recorded before work? | Capture activity footprint and clock, baseline stations and depths, measurement method, source versions and responsible people. Recovery of these details after a dispute can be difficult. |
| 7 | Where and when should someone verify? | Ask whether the target itself has a qualifying observation. Use a location and depth where a measurement could distinguish explanations. |
| 8 | What prevents a recurrence? | Connect field findings to responsible action, return conditions and a follow-up date. Track environmental recovery separately from administrative case closure. |

The product concentrates on decisions 4, 6 and 7 and contributes evidence to the others. A contactable field team, supervisor and useful export are operating assumptions for the design. Validate these with the intended offices.

### Tunda · the day before an inspection

On 27 October 2023 KKP documented stopping and inspecting *Vox Maxima*. Its 29 October release reported approximately 24,000 m³ of sand aboard and a suspected source near Tunda. The stop, cargo observation, source allegation, activity location and legal disposition have different evidentiary status. The source release provides no confirmed extraction polygon or exact extraction clock. Keep the records for the Jakarta-water inspection and the suspected Tunda source geographically distinct.

On 26 October the broad Sentinel-2 screen passed on 95.3% of the island-ring footprint; it passed on 75.8% of the west portion of the archived reef footprint. With a 90% screen, an officer would make a different coverage judgment depending on the area reviewed. Across 587 readable dates the full ring and archived reef differed on 34, including 10 ring-only and 24 reef-only passes. That finding changes a practical requirement: name the protected place before calculating coverage. An archived reef polygon serves as a test geometry and needs local updates for operational use.

The scoped Sentinel-2, Sentinel-1 and Landsat 8/9 catalog queries had no acquisition dated 27 October at the study footprint. The prior-day scene exists in different processing versions. Acquisition, processing/publication, agency receipt and intervention each need their own timestamp. A modern archive can reconstruct the first two under specific conditions. It cannot reconstruct who read a scene on that day. The project’s own archive stores the event register, lineage tables and seven original catalog responses; see the review folder inside the ZIP.

The initial pilot used a **water-only classification** over a 1.5–3 km ring. In June–September 2025 Tunda passed on 17/30 dates and in November 2025–February 2026 on 1/27. Kodingareng passed on 10/31 and 0/28 in those windows. The expanded audit also used a **broad quality screen** of multiple Sentinel classification codes. Numbers using those definitions are not interchangeable. The reported physical coral and sediment results in Wahyudi et al. are local field or modeling results from a different study period. They establish a reason to care about that reef; they cannot be attached to the 2023 inspection as measured effects.

### Kodingareng Lompo · the same date, two depths

This is the best opening scene. The contractor’s February–October 2020 project window supplies historical context. The public police account’s printed coordinate is 2.244 km from the study island anchor, while the written account describes a distance of 11 miles southwest. Neither provides a verified extraction polygon. Do not attach sediment trajectories to that pin. Kodingareng Keke and Kodingareng Lompo are different islands. Fisher accounts identify resource use and concerns; verifying catch or income effects requires its own evidence.

For GLORYS12 the comparison uses daily eastward and northward velocity components from a roughly 9 km regional grid. The selected cell is centered at about 5.1667° S, 119.2500° E. Across all 274 dates, 139 near-surface values and 230 deeper values had an eastward component. Rejoining the two series by UTC day yields **96 dates with westward surface component and eastward deeper component**. Subtracting 139 from 230 yields 91, a difference between marginal totals, not the paired count. The opposite strict combination occurred on six days; five other days had a zero in one layer. The file `05_Reproducibility/Depth_case_verified.json` retains every sign combination and the full two source rows for the demonstration.

| 16 April 2020 · modeled daily mean | u east, m/s | v north, m/s | Speed, m/s | Bearing toward, clockwise from north |
|---|---:|---:|---:|---:|
| 0.494 m below surface | −0.092166 | −0.009766 | 0.092682 | 263.95°, west |
| 9.573 m below surface | +0.052492 | +0.052492 | 0.074235 | 45.00°, northeast |

Two officers can verify the example with the ZIP and a Python interpreter. The component sign describes east versus west, not necessarily a full reversal of the two-dimensional vector. Daily averages also smooth variations during the day. The surrounding nine surface cells disagreed on the east/west sign on 92/274 dates, and the deeper cells on 94/274. A smooth field of arrows inside a single native model cell would suggest more spatial detail than the source provides. Use an arrow or a clearly indicated cell footprint and label its resolution.

### Amur Bay · what travels between coasts

Use Amur Bay and the Razdolnaya estuary for two different comparisons. First, in the July–September **2023** optical replay, documented flood windows and substantial river inputs give reviewers an alternative sediment pathway. Eighteen Sentinel-2 dates and twelve Landsat dates gave 28 distinct dates. Five distinct dates qualified in the two analysis boxes across missions. None of the four distinct acquisition dates during the flood intervals qualified under the paired screen. On 6 September both missions observed greater western red reflectance about 18 minutes apart (west-minus-east approximately +0.0552 and +0.0646). A pre-flood Landsat date, 12 July, had a larger contrast (about +0.0961). Two sensors support the optical pattern, yet neither identifies the material’s source.

Second, the **2007** Amur field survey described in a later publication supplies a practical comparison for survey design. It used 99 stations and sampled near the surface and above the bed, alongside instrument profiles. “Above the bed” and “below the surface” are different vertical references. Pair the local sampling purposes; choose depths using actual local water depth. A published method establishes precedent for sampling at more than one level. The local raw profiles and a matching date, position and variable would have to be confirmed before drawing them as measured values. Do not combine the 2007 station work and 2023 imagery into one event.

### How much do additional data sources really buy?

The expanded archive contains 1,178 Sentinel-2 site-dates (1,177 readable) and 799 Landsat site-dates in the inventories. On a matched January 2025–October 2026 window, Landsat added 15 qualifying dates at Tunda (62 to 77) and 25 at Kodingareng (63 to 88) to the Sentinel broad screen. Yet the longest no-pass calendar runs changed only from 132 to 131 days at Tunda and from 162 to 158 at Kodingareng. Select a second sensor for the particular gap it closes.

In November–December 2025, only 1 of 72 study site-days with mainland regional IMERG proxy rainfall ≥10 mm passed the combined optical screen. Of the 71 remaining site-days, 49 had no acquisition and 22 had an acquisition that failed the screen. This split affects the response: a better cloud mask cannot recover a date that neither mission acquired. Regional rainfall is also an imperfect proxy for discharge or local reef exposure. When comparing precipitation series, label UTC versus WIB/WITA, grid, aggregation and which river or mainland area the sample represents.

### Russia–Indonesia cooperation that changes the work

The 2026 bilateral consultation reported in the diagnostic identified working groups covering marine resources and industry and people, research and training. The earlier partnership review also discussed ASEAN–Russia search-and-rescue training and ORRUDA exercises as precedents for coordination; their subject and participating institutions differ from environmental survey planning. The 15-page diagnostic, page 13 and its linked references, is the starting point for the research channel. Do not imply a navy exercise commissioned this app.

Indonesia contributes a concrete coastal management question, dated public cases, mapped reefs, proposed stations and knowledge of local field practice. A prospective Russian contributor can independently replay the same evidence rules in a bay influenced by a large river, and explain how it would choose different depths or reference stations. The Pacific Oceanological Institute FEB RAS is a relevant potential scientific counterpart; Indonesian marine researchers and agency practitioners are prospective reviewers. Programme organisers, data providers, candidate research contacts and end users occupy different roles. No partner commitment is recorded here.

**Proposed exchange artifact.** Each office gets a case packet containing the same definitions of activity, observation and receipt; a footprint and vertical datum; model source and resolution; planned sampling method; and a place to record what the team would change and why. Compare answers on Tunda/Amur for attribution and coverage, and Kodingareng/Amur for depth selection. Retain local thresholds, habitats, weather regimes, authority and access rules in each jurisdiction. A useful bilateral outcome would be an independently reproduced finding and a documented change in survey design.

### What a reviewer actually sees and does

1. **Open a case above the coast.** The first view is a lightly stylized three-dimensional coastline with a boat, jetty, reef outline, station, north indicator and case status. Retain enough relief, shadow and color to distinguish the shore, shallows and offshore water. Aim for the legibility of CityRT’s screenshots: compact buildings, clear silhouettes, an original cartoon-like finish with soft colour blocks, restrained contours, and an oblique view that still works as a map. Keep the date, selected station, layer, units and source visible around the map.
2. **Select a station and viewing depth.** Keep the camera, water surface, station and date fixed. Change the selected layer from about 0.5 m to 9.6 m. The arrow and value change together, and the user can see the native cell they represent. Provide both a direct control and a keyboard-accessible numeric or layer selection. The “sea-level” language in the brainstorm referred to exploring depth. Moving the tide or draining the whole bay would answer a different question.
3. **Inspect a vertical section.** Draw line A–B through the station. Pivot around that line, using the same boat or jetty to orient the viewer. Read depths against the surface and the seabed along that line. In an implemented version, derive the bottom profile from known terrain resolution and datum. The current cutaway is illustrative artwork. Graphic precision cannot substitute for surveyed topography.
4. **Choose what to ask the crew.** “Viewing depth” selects the model evidence. “Proposed sample depth” belongs to the field plan. Changing one should never silently overwrite the other. A current profiler measures water movement. A water bottle supplies material for sediment analysis; it cannot verify current direction. State which measurement is missing and which instrument could provide it.
5. **Review, issue, return.** An officer saves a draft. A supervisor reviews and versions the issued field brief. A field lead checks local feasibility, logs actual time, location, depth, instrument/sample ID and units, and attaches results to the same case. If measurements cannot be obtained, preserve the gap and its reason. A colleague should be able to reopen the case and reproduce the reason for each depth.

**Illustrative KR-01 field handoff.** Proposed station S-01 is at 5.1550° S, 119.2620° E (WGS84). Proposed visit 08:00–10:00 WITA, date and feasible depths to be confirmed by the field lead. Request a current profile and, if feasible, bottles at the two target depths. The date on the evidence card is **16 April 2020**, the date of the modeled example. The proposed visit, illustrated station and sampling requests are hypothetical. They are distinct from the model cell center, the disputed activity coordinate and any historical permit. Never turn the specimen into field-deployment instructions for this real place.

### What the five ideas contributed

These are records of alternatives, ordered here by the role they played. The early council considered a judge’s first impression, a prospective buyer’s justification for use, the operator’s next action, the bilateral partner’s distinct contribution and a skeptical scientist’s counterexample. The set of five was generated before the government-workspace correction. It records design exploration and feedback. It does not record interviews or official endorsements.

| Idea | What a person could do | What survives the selection |
|---|---|---|
| **The Ocean Has Floors** | Stay over the same place, change the depth and discover water moving a different way. Then decide where to sample. | Selected product and signature gesture. Keep the overhead map, optional section and concrete crew brief. |
| **Coast Swap** | Apply one evidence rule on two different coasts and see which conclusions change. | Reuse as a comparison or training exercise. It gives each country analytical work. It need not open the operator’s daily workflow. |
| **One Boat, Two Samples** | Place scarce sampling effort where two measurements could distinguish explanations. | Make station, target depths, instruments and expected value explicit. The number two is illustrative, not a permanent field quota. |
| **Evidence Loom** | Bring dated strands of imagery, field evidence and activity records together to examine what supports an account. | Reuse provenance and clickable evidence history in the case file. Keep event, source and decision clocks separate. |
| **The Map That Refuses to Pin** | Open a reported location and see where competing descriptions agree or conflict. | Keep the printed coordinate, calculated distance and uncertainty visible. An early image mistakenly implied confirmation; the corrected image is identified in the gallery. |

An intermediate recommendation combined Coast Swap, One Boat Two Samples and an unfolding evidence pin. Later discussion selected the depth interaction. The earlier fusion remains available for later design decisions. Other ideas such as Gaussian splatting and an immersive “god’s-eye” view were suggestions about means. The team selected the camera perspective and visual legibility. Capturing real volumetric imagery or reproducing CityRT’s physics was never established as a requirement.

### References that shaped the visual and pitch

| Prior reference | Element the team valued | Translation into this product |
|---|---|---|
| NASA Space Apps 2024, Eco-Metropolis, Most Inspirational | A person occupies a role, makes a choice and understands a scientific idea through its consequence. | Cast the user as the officer preparing the baseline. The visible consequence is a different field request. |
| Ocean Hackathon’s FeedRight and Ocean Drift | A focused interaction tied to a specific marine decision. | A single date-depth switch can explain why a planning team should care about regional currents. |
| Ocean Hackathon’s Penang jellyfish project and Seascape Game | An island-specific problem can travel. A game format on its own supplies little evidence of local value. | Give the comparison coast a real test and let reviewers see the planning output. |
| ESA/NASA/JAXA Earth observation hackathon, CleverChart | Make scientific evidence navigable and traceable. | Allow inspection of a source row behind an arrow. |
| Google Immersive Geospatial Challenge, Geospatial Solar | Direct interaction with a recognizable spatial object can explain an analytical result. | Select a station in place and change one control; keep the camera stable. |
| CityRT | Detailed but legible models, restrained colors, fixed spatial landmarks and a bird’s-eye camera. | Use comparable visual vocabulary for an Indonesian or Russian coast. The two original screenshot sheets and the later waterfront screenshot guide the finish. The latter shows shaped vegetation, textured water accents and illustrated contours. The coastal architecture, textures, and composition are original. Generated concept art illustrates intended views. |
| God’s Eye View; Superpowers; REA | Layered spatial exploration, disciplined planning and a possible route for studying interaction design. | These are external references. A later repository audit records available CityRT references and technical observations, with incomplete capture and validation. The art revision uses observed visual principles and the user’s screenshots. Simulation and rendering internals are optional context. |

Public reference links retained from earlier work. These are starting points for future reference checks; no third-party application, repository, or full web archive is shipped as part of the team’s software.

- NASA award announcement: https://www.nasa.gov/learning-resources/stem-engagement-at-nasa/nasa-international-space-apps-challenge-announces-2024-global-winners/
- Eco-Metropolis project repository: https://github.com/j-shafeeqa/Eco-Metropolis-Sustainable-City-Simulation---NASA-Space-App
- Campus mondial de la mer, Ocean Hackathon: https://www.campusmer.fr/Home-4185-0-0-0.html
- Ocean Hackathon 2022 grand finale: https://www.campusmer.fr/news-ocean-hackathon-2022-a-look-back-at-the-international-grand-finale-3537-635-0-0.html
- ESA Earth observation hackathon: https://www.esa.int/Applications/Observing_the_Earth/Announcing_Earth_observation_hackathon_winners
- Google Geospatial Challenge: https://developers.googleblog.com/congratulations-to-the-winners-of-googles-immersive-geospatial-challenge/
- CityRT: https://cityrt.com/en/
- God’s Eye View: https://github.com/bilawalsidhu/gods-eye-view
- Superpowers: https://github.com/obra/superpowers
- REA: https://github.com/morluto/rea

### Implementation map

The following is a suggested architecture carried forward from the brief. The offline analysis scripts are working research artifacts. They do not constitute a deployed web app.

| Layer | Proposed components | Job |
|---|---|---|
| Operator interface | React + TypeScript | Keep case, station, evidence date, viewing depth and proposed sample depths in explicit state. Present keyboard controls and an accessible numeric alternative to the graphic. |
| Spatial view | Three.js + React Three Fiber | Integrate the packaged coast and optional standalone cutaway GLBs. Teammates own camera and interaction state, station selection, data overlays, the fixed-camera native depth switch, A–B behavior, model-cell resolution and no-data states. |
| Art production | Local DeepSeek Harness, configured Blender MCP and local Blender, glTF 2.0 GLB | Revise the globe, three coasts and cutaways, shared kit, camera presets, 4K stills, travel films and combined reel. Deliver editable scenes, clean assets and an engine-neutral manifest. |
| Scientific preparation | Python, Xarray, Rasterio; GDAL where required by archive scripts | Subset source variables by date, bounding box and native depth. Apply footprint-level QA; preserve bad/absent/missing classifications. Package small dated layers for a responsive browser. |
| Case service | FastAPI + PostgreSQL; agency authentication, roles, revision IDs | Store proposals, evidence manifests, issues, sign-off, sample IDs and returned results. Bind an issued brief to the exact evidence version. |
| Research handoff | Original reproducibility ZIP, claim crosswalks, checksums and Python verification | Separate re-running a fixed archive from refreshing live services. Record versions and new timestamps on refresh. |

| Data / access route | Role in the product | Status and scale to preserve |
|---|---|---|
| Copernicus Marine GLORYS12V1, GLOBAL_MULTIYEAR_PHY_001_030; Toolbox subset API; archived extraction cmems_mod_glo_phy_my_0.083deg_P1D-m_202311 | Daily modeled eastward/northward currents at native depths. | Used and checked. 1/12° grid, ~9 km here. Respect wet/dry/fill masks, depth sign, time averaging and degrees toward. |
| Sentinel-2 L2A via Earth Search / Copernicus Data Space STAC; Landsat 8/9 Collection 2 via USGS or archived Planetary Computer workflow | Surface observation availability, footprints, optical comparison. | Used in the audit. Pixel classification, band scaling and atmospheric correction differ by product. Keep sensor, acquisition ID, QA definition and receptor. |
| Sentinel-1 GRD catalog; related multi-source observation records | Check acquisition timing in the scoped event. | Queried for the Tunda clock audit. A matching timestamp alone supplies no verified observation of dredging. |
| NASA IMERG / NASA POWER; CHIRPS; CPC; ERA5; Open-Meteo Historical Weather/Marine; MFWAM where applicable | Check rain, waves, temporal alignment and rival explanations. | Specific archived extracts were used. Separate reanalysis from a historical operational forecast. Product families can share inputs. |
| BIG BATNAS (6 arc-seconds); GEBCO 2025 (15 arc-seconds) | Section terrain and regional bottom context. | Proposed app layers. Verify coverage and vertical datum, mask land, check use conditions, label horizontal scale. Use local sounding for operational sample feasibility. |
| Archived habitat polygons; Allen Coral Atlas where coverage permits | Define the receptor before screening a scene. | Archived reef geometry was analyzed. Current habitat boundaries require local confirmation. |
| NOAA WODselect; Global Ocean Currents Database (GOCD); agency or field records | Search for matched profiles and current measurements. | Proposed lookup routes. A catalog hit can be for the wrong depth, date or variable. Raw Amur turbidity profiles have not been confirmed. |
| NASA GPM data via earthaccess; GloFAS discharge where the basin is represented; ERA5 wind/waves | Add catchment or coastal context to a future case. | Confirm basin, scale, time base and data access. Even a matched river estimate cannot independently identify a particular plume. |
| KKP, provincial, police, contractor, scientific and fisher/community material | Reconstruct activity, location, reports, intervention, governance and operational constraints. | Attribute each claim to the specific record. Separate allegation, documented action, verified geometry and final disposition. The dated register stores the distinct claims. |

Direct data links are embedded in page 7 of the team brief and its Markdown extract. The archived research bibliography has 48 numbered entries in `05_Reproducibility/Reading_copy/source_manifest.csv`. Reuse the original API paths and identifiers in the workstream scripts when reproducing an exact historical result.

### Questions for an actual pilot

These are validation questions, not evidence that a partner or field pilot has agreed to them.

| Open question | Who or what can resolve it? | What would change the design? |
|---|---|---|
| Who proposes, checks, issues and closes this type of survey? | Interview an officer, supervisor and field lead; map an actual anonymized brief. | Different roles or approvals would change the queue, form and sign-off. |
| Is the regional depth contrast useful for selecting a local check? | Match a dated local current profile to the model cell, actual depth and time; inspect disagreement. | If regional context misleads at a reef edge, make a local profile or prior survey the primary comparison. |
| Can the crew obtain paired samples at the proposed station? | Confirm the chart datum, local sounding, access, safe field method and equipment with the lead. | Move the station, change the depths or use fewer samples and record why. |
| Does the interface reduce explanation and rework? | Give an officer the case without narration. Ask for source type, water-depth interpretation, sampling method and what can be issued. | If the officer thinks the arrow is a reef measurement, redesign the layer label before adding more features. |
| Does a partner really learn something new from the comparison coast? | Have teams independently review the same schema and exchange signed explanations of differences. | If both simply repeat the same answer, pick a comparison that tests a competing cause or different field method. |
| What operational benefit is measurable? | Compare time to a complete brief, share of stations with source/depth/instrument rationale, reopened cases and field results matched to a station. | Establish the baseline and trial result before claiming efficiency, enforcement or ecological impact. |

**Pitch discipline.** Start with the officer’s job and the 16 April view. Show the change in the arrow, let a person choose the instrument, and end with the brief the crew receives. Say what is modeled, what is measured and what remains to collect. The single biggest communication risk found through the revisions was mistaking a beautiful concept image for the actual work surface. The supplied independent reader-style critique was an AI review. A real coastal officer and field crew have yet to validate this workflow.

### How a new teammate or AI should work with the pack

- For a pitch, read the competition prompt, the seven-page product brief and this handoff. For scientific claims, go directly to the primary source, archive table and definitions. The polished journal-style PDF is an internal research manuscript; its format does not imply peer review.
- For design, use the four rendered operator pages and the latest brief as the functional reference. The CityRT screenshots and generated scenes guide art direction. Labels in early posters carry little scientific weight.
- For the art revision, use the DSH plan and delivered v1 files. Start with the Kodingareng look proof, then apply the approved visual rules to all three coasts, the globe and kit. Track what was rendered, watched, reopened or imported with separate evidence. 
- For app implementation, reproduce the two source rows, wire both to the same map and test switching, then test a missing measurement and a versioned field request. Distinguish implemented behavior from proposed behavior in any subsequent handoff.
- For research, use `CLAIMS.md` and `FIGURES.md` in the original archive. Match the denominator and spatial footprint before reporting a percentage. Confirm the unit, vertical reference and time basis before comparing two measurements.
- The user prefers plain English, direct explanations and findings phrased as actions with owners. When asked to plan and clarify first, preserve that sequence. The requested “wow” is something a judge discovers by interacting with evidence. Give difficult claims an independent critical read and distinguish AI review from human usability evidence.
- The material below reproduces the text of key team documents. Some older conclusions or priorities reflect earlier stages. The latest product decision is recorded above and in the seven-page brief. For figures, exact table alignment or a discrepancy in text extraction, open the linked original PDF.

### Current 3D production decision · full local revision

The user's role ends with the 3D handoff. The next DSH run is authorized to improve every production asset in the v1 handoff, including the three complete coasts, original parts and materials, globe and pins, camera rigs, cutaways, stills, travel films and reel. The first Kodingareng look proof sets the shared visual language within that run. Tunda and Amur will receive the same quality checks and retain their own coastal character. The owner asked to use the screenshot’s slightly cartoonish finish. The target is a small, readable coastal world with shaped silhouettes, light contour accents, matte materials, deliberate shadow and calm water marks. Each scene should still leave room for the officer to read the evidence.

The plan targets the actual local DeepSeek Harness session with Blender MCP, plus its available Blender background executable for long renders. The original work notes report Blender 5.2.2 on Windows. DSH must verify the local version, tool schema and path sharing before editing. The audit environment's Blender 4.3.2 imported all five v1 GLBs and rejected the Kodingareng editable scene header. The correct recovery is a compatible local Blender or a documented geometry rebuild from the GLB and procedural sources.

The app engine is undecided. The default handoff uses core glTF 2.0 GLBs, separate coast and section assets per site, independent visual water meshes, named anchors and a plain JSON manifest. Clean production geometry and renders carry no scientific claims. A separate annotated pitch comparison may show the archived Kodingareng pair. Teammates own evidence overlays, interaction, data and field workflow. The DSH run ends with a tested, self-contained art delivery ZIP containing runtime exports, source, pitch media, import instructions, attribution and verification.

Use the repository’s place-reference board for the revised globe locators. Kodingareng Lompo is 5.14905° S, 119.26473° E, Tunda is 5.81151° S, 106.27811° E, and Razdolnaya is 43.32556° N, 131.80778° E. These geographic locators are distinct from the decorative scene origin, proposed S-01 sampling station and native GLORYS12 model-cell centre. Each cutaway is illustrative. Record its vertical exaggeration and keep the same local shore, jetty or bank and boat landmarks across views.

## Appendix A · User direction and approval history

# User direction, in sequence

This is an editorial record of the maritime project conversation. Quoted phrases preserve wording as supplied. Summaries condense longer exchanges. This file does not claim to be a verbatim export of the chat or the individual agent deliberations.

| Turn / phase | What the user asked for | What a successor should carry forward |
|---|---|---|
| Theme discovery | Start with problem statements for each sub-theme; explore exploitation of sand. | State the underlying maritime challenge before choosing features. |
| Partnership | Investigate what past partnerships did, how, and what each country has. “A standalone idea that can be supported by the russia-indonesia cooperation.” | Demonstrate domestic value and a specific bilateral contribution. |
| Analytical method | Find public secondary data, GIS and APIs capable of original maritime analysis; the coastal-observation angle felt promising. | Make computations traceable and use multiple independent kinds of evidence. |
| Case scope | Ask if Tunda is large/prevalent enough. “learn-from-x or made for x but can be used anywhere.” Explicitly asked to stay in planning at that stage. | Explain transfer through a comparison coast. Avoid a national prevalence estimate unsupported by case evidence. |
| First audit | Request a BCC-style issue tree, investigation of root causes, strategic directions and a readable 10–15-page PDF with maps/charts. | Preserve the first diagnostic as the history of the hypotheses and the original data. |
| Critique | Request the supplied skill, independent critique and a self-improvement loop. | Record checks, revision evidence and the limits of review. |
| Interpretation | Ask for simple, actionable, solution-directed insights, e.g. “XYZ needs to...” and “We need to consider XYZ when..”. | State the decision maker, action and evidence that would change the answer. |
| Open the decision space | Challenge “is there enough evidence to check this place now, and if so, where should they look?” Ask for prevention and other decisions. | Keep all eight decisions in the research. |
| Expand the audit | Ask for 20–25 pages, rich public API coverage inspired by God’s Eye View and NASA, original triangulation, research-article structure, charts and accessible writing. Ask clarifying questions before running. | Keep the comprehensive research plus the original reproducibility ZIP. |
| Method choice and delivery | Request Superpowers, a larger run, selling the final idea, PDF plus reproducibility bundle. Approve broad analysis; no external human support. | Preserve which results were produced with public evidence and which still require fieldwork. |
| Scientific version | Request a proper journal-style article layout using the attached paper as a visual reference. | Keep the distinct 11-page manuscript and 9-page external paper. |
| Explanatory questions | Ask for key insights, a realistic illustrative case, safe locations, unlawful extraction, readiness for a hackathon solution. | Replays support a practical decision, while siting, source attribution and enforcement require independent evidence. |
| Creative planning | Explore ambitious mechanisms and overseas winning entries, weigh rubric, visual design and possible Gaussian splatting, consider investor/judge/agency perspectives. Explicitly ask for plan and clarifications first. | Preserve the sequence on future tasks. Generating alternatives before clarification previously frustrated the user. |
| Brainstorm authorization | “I just saw something I’d never noticed before”; “explore the full arc”; let a judge use the same evidence rules in Tunda and Amur Bay and see what changes. | Demonstrate a discovery a person can make; give both countries analytical responsibility. |
| Visualize and benchmark | Ask for GPT Image explanations of all five alternatives, international hackathon comparisons and inspiration from NASA’s Eco-Metropolis. | Retain concept images and the rationale for selecting a mechanism. |
| Product selection | Ask for a deeper explanation of “the ocean has floors” and the data needed to make it realistic. | Anchor the interaction to real archived model values and locally verifiable measurements. |
| Art direction | Specify CityRT and supply two screenshots. Ask for an overhead, interactive ocean view with a playful but professional style. Ask whether REA could be used; “still planning, dont run it yet.” | Keep the visual inspiration. There is no recorded CityRT implementation/physics audit. |
| Team brief | Request ~5–7 pages, one page of problem/relevant analysis, GPT Image illustrations, minimal research-style LaTeX/TikZ diagram, features and web stack, potentially Blender/Blender MCP. Use plain English. | Use the latest seven-page briefing as the current design reference. |
| Technical additions | Request exact APIs and datasets and allow another page if needed. | Every major layer should have a practical retrieval route and an evidence label. |
| Audience correction | “first and foremost a government/internal kind of thing, that coincientlly is shaped like a game for easy understanding.” | Give priority to officer, supervisor, field lead and field brief. |
| Screen correction | GPT images are visualizations; the operator should get a god’s-eye view, explore the level and understand what the product does. Ask for an independent readability review and authorize revision. | Final operator states, section and versioned field handoff take precedence over early illustrations. |
| Consolidation | Ask for one paragraph explaining the solution, then one detailed master AI context pack with files. | The pack is both a briefing and a portable source collection. |


## Appendix B · Four original team documents in reading order


### The Ocean Has Floors


Extracted text by printed PDF file page. Use the original for tables, reading order, diagrams and page geometry.

#### PDF page 1

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

#### PDF page 2

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

#### PDF page 3

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

#### PDF page 4

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

#### PDF page 5

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

#### PDF page 6

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

#### PDF page 7

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



### 01 Coastal Sediment Diagnostic


Extracted text by printed PDF file page. Use the original for tables, reading order, diagrams and page geometry.

#### PDF page 1

LAUTARA 2026 / RESEARCH BRIEF
When can a
coast be seen?
Sea-sand extraction, satellite coverage and coastal verification at Tunda
Island and Kodingareng Lompo
21 NOVEMBER 2026 / INDONESIA–RUSSIA MARITIME HACKATHON
Local image screening recovers locally qualifying views in
some periods. Months of sparse coverage can still leave an
event unobserved by this archive.
17 / 30
Tunda local screening passes,
Jun–Sep 2025
1 / 27
Tunda local screening passes,
Nov 2025–Feb 2026
0 / 28
Kodingareng local screening
passes, same second window
Original Sentinel-2 analysis establishes an observation constraint in the sampled archive. In Tunda’s
first window, the island-scale screen retained seven dates that a tile-wide 20% cloud ceiling would
have rejected. The longest interval between locally qualifying observations still reached 20 days.
A documented October 2023 inspection makes the stakes concrete. Satellite scenes bracket the
intervention date, leaving the activity on that day to other evidence. For LAUTARA, the immediate
strategic decision is which part of coastal verification the team can improve and defend with evidence.
Screening pass = ≥90% of a 1.5–3 km ring classified as water by Sentinel-2. The ring is a comparison footprint. See pp. 5–9 for
conditions and interpretation. [1] [5] [8] [9]
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
01 / 15

Links embedded on this page

- https://chatgpt.com/library?file_id=libfile_a0f1f94bc47c81919f0b91c5fbf16337
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html

#### PDF page 2

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
WHY THIS MATTERS
Tunda makes a global pressure
concrete
Marine dredging is widespread. A small island lets us see what it takes to investigate a
particular event.
4–8 bn t
Global annual estimate for sand
and other marine/coastal
sediments dredged
11m m³
Sand transported for Makassar
New Port, Boskalis-reported,
phases 1B–1C
27 Oct
Date of the Tunda-linked KKP
case in 2023
UNEP’s global range covers sand and other sediments and includes multiple forms of dredging. It
establishes the scale of material movement. The Makassar figure is a contractor-reported project
volume for a separate site. It establishes the physical scope of a documented project and uses a
different unit. Neither estimates the prevalence of illegal extraction in Indonesia. [2] [11]
Why sediment matters to reef users
Dredging can resuspend sediment. The ecological effect depends on sediment type, concentration,
duration, recurrence and the condition of the reef. Catch and livelihood effects require their own
evidence. These are separate links in a chain, with different measurements at each step. [3] [14]
What makes this a LAUTARA problem
An event may warrant checking even when its source is uncertain. The challenge is knowing when the
available evidence can justify that decision. A local case sharpens the task, and a second coast tests
how far the diagnosis travels.
Competition fit: sustainable maritime solutions and data-driven coastal management. The guide’s initial video asks teams to
justify why the chosen maritime challenge matters. [1]
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
02 / 15

Links embedded on this page

- https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans
- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://chatgpt.com/library?file_id=libfile_a0f1f94bc47c81919f0b91c5fbf16337

#### PDF page 3

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
STUDY GEOGRAPHY
Two islands, one comparable
question
Tunda anchors the diagnosis. Kodingareng Lompo tests whether the observation pattern is
peculiar to one island.
Figure 1. Site anchors and regional context. Coastlines © Natural Earth (public domain). Ring centers: Tunda 106.27811°E,
5.81151°S and Kodingareng Lompo 119.26473°E, 5.14905°S. [18] [19] [20]
Site
Why it is in the study
What the geographic comparison
measures
Tunda, Banten
Published reef transects, sediment
modelling and a dated official
enforcement case.
Same fixed ring and calendar windows,
plus a case-specific review around the
dated intervention.
Kodingareng
Lompo, South
Sulawesi
Separate sand-extraction case with
contractor documentation and fisher
interviews.
The same visibility screening. The ring is
centered on the island and does not
represent the 2020 marine borrow area.
The islands share an evidence problem worth testing. They differ in shoreline geometry, local
hydrodynamics and the timing of reported extraction. The comparison therefore tests the portability
of an observation diagnosis, with site-specific evidence kept separate. [3] [5] [10] [11]
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
03 / 15

Links embedded on this page

- https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/
- https://mapcarta.com/15591682
- https://mapcarta.com/16118912
- https://doi.org/10.2478/cjf-2023-0009
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://doi.org/10.30872/mulrev.v6i2.621
- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf

#### PDF page 4

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
ISSUE TREE
Four ways the evidence can break
Start with the decision facing a coastal reviewer: is there enough evidence to justify
investigating this place and time?
Can the event be investigated?
Exposure
Observation
Attribution
Response
Link
Testable failure
Rival explanation or falsifier
1. Exposure
Sediment reaches reef habitat at
consequential duration or frequency.
Matched reef and reference samples
show no unusual sediment
concentration or duration.
2. Observation
A view is missed by screening, or no
sufficiently clear acquisition exists.
A looser tile threshold recovers the
same view, or a nearby footprint
passes under a small change in
geometry.
3. Attribution
Multiple sources plausibly explain an
optical change near the island.
An independently documented source
aligns in time and location and
competing sources fit materially worse.
4. Response
The evidence available at a handoff
delays or prevents field verification.
The action occurred promptly, or
staffing, jurisdiction, or an unrelated
constraint explains timing better.
This tree follows the decision sequence. The exposure question concerns what happened in the
water. The observation branch concerns what could be recorded. Attribution concerns what produced
the signal. Response concerns what people did with it.
The hypothesis the numbers can resolve
The archive can test screening losses and poor local coverage directly. A documented event can show
whether observation and action lined up. Quantifying recurring reef exposure, causal sources and
operational delay would require additional evidence matched to those claims.
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
04 / 15

#### PDF page 5

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
METHOD
Count observation opportunities
by date
The unit is one UTC acquisition date at one site. Pixel counts describe how much of each fixed
footprint passes screening.
Component
Decision and interpretation
Catalog
Earth Search Sentinel-2 L2A. Compare matched dates in Jun–Sep 2025 and Nov
2025–Feb 2026. Additional Tunda windows cover Mar–May and Jun–Sep 2026.
Local footprint
Use the 1.5–3.0 km annulus around each island, in local UTM. It samples
island-adjacent waters without treating the island center as a target. It is a geometric
footprint.
Local screen
Primary reported metric: percentage of 20 m Scene Classification Layer (SCL) pixels in
class 6 (water). Pass at ≥90%. Compare with scene classes 2, 4, 5 and 6, alternate
radii, and 80% / 95% cutoffs.
Tile screen
Catalog eo:cloud_cover ≤20%. This is a deliberately simple comparator for whole-tile
selection. Check 30% and 50% for sensitivity.
Event
reconstruction
Use timestamps and official records to locate observations around 27 Oct 2023.
Where no exact-day scene exists, report the date mismatch explicitly.
A pixel labeled water by SCL can still carry sunglint, adjacency effects, bottom reflectance or
uncertainty from atmospheric correction. The screen measures classified-water coverage rather than
whether a scene supports a specific water-quality decision. A lower pass rate can also reflect
unclassified pixels. [8] [9] [13]
Primary geographic and counting conventions are recorded on pp. 3 and 15. All headline counts use the same 1.5–3.0 km ring
and 90% local cutoff.
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
05 / 15

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://doi.org/10.1016/j.rse.2019.03.010

#### PDF page 6

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
FINDING 1 / OBSERVATION
Local screening adds dates. Long
gaps persist.
At Tunda, a 20% tile-wide cutoff drops qualifying local views in every sampled window. The
gain is uneven.
Figure 2. Local water-class fraction per date in Tunda’s first two windows. The dashed line marks the 90% screening threshold.
June–September and November–February are separate sampling windows. [8] [9]
Tunda window
Dates
Tile pass
Local pass
Local only
Jun–Sep 2025
30
10
17
7
Nov 2025–Feb 2026
27
0
1
1
Mar–May 2026
22
6
8
2
Jun–Sep 2026
31
13
26
13
Four-window total
110
29
52
23
In Jun–Sep 2025 the maximum interval between local passes was 20 days, the same as the tile screen.
In the Nov–Feb window, 1 Nov was the sole pass. The remaining 119 calendar days of that window
had no additional pass. SCL labeled at least 90% of the ring as cloud or cirrus on 25 of the 27
acquisition dates in that window. That makes cloud classification, alongside the viewing opportunity,
central to that result.
Same-month replication: 26/31 local versus 13/31 tile in Jun–Sep 2026. At a 40% tile ceiling the four-window totals both equal
52, yet the two screens disagree on ten dates. These are analyst comparisons with a hypothetical catalog filter.
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
06 / 15

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html

#### PDF page 7

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
FINDING 2 / OPTICAL INTERPRETATION
A passing scene can still mislead
The first screen tells us whether there is a broad view. It leaves sector-level coverage and
image interpretation open.
Figure 3. Modified Copernicus Sentinel-2 L2A, 7 and 14 Jun 2025. Orange shows excluded SCL classes. This illustration uses
classes 2, 4, 5 and 6 as the broad mask. The primary headline counts use water class 6. Study rings are geometric. [8] [9]
Figure 4. Modified Copernicus Sentinel-2, Tunda, 22 and 24 Jul 2025. The conspicuous bright region on 24 Jul extends over
land and water. These images depict reflectance and true-color appearance. [8] [13]
Across 18 early-window dates with ≥90% SCL-water coverage, the east-minus-west median red-band
contrast was positive on 10 dates and negative on eight. On 24 Jul the whole ring was 91.6%
water-classed, while the east sector was 79.7%. The largest contrast coincided with a bright feature
that crossed the island. That scene alone cannot distinguish sediment from atmospheric or other
optical effects.
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
07 / 15

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://doi.org/10.1016/j.rse.2019.03.010

#### PDF page 8

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
FINDING 3 / EVENT RECONSTRUCTION
The documented inspection fell
between scenes
The October case grounds the monitoring question in an actual decision with a date.
Date
What the record shows
What the analysis can infer
21 Oct 2023
Sentinel-2 classified 99.9% of the ring in the
broad screening classes.
An earlier broad view.
26 Oct 2023
The previous acquisition put 95.3% of the ring
in the broad screening classes.
A pre-stop image gives no assurance of a
no-dredging baseline.
27 Oct 2023
KKP reports a stop and inspection of MV Vox
Maxima, and an interagency
information-gathering action linked to Tunda.
Official action is documented. No
same-day Sentinel-2 scene was returned
by the Earth Search query.
31 Oct 2023
The next catalog scene put 99.0% of the ring
in the broad screening classes.
This image follows the reported stop by
four days.
18–22 Nov 2023
Fishers reportedly saw a loaded vessel pass
Pulau Pari. The 20 Nov scene had roughly 0%
broad coverage at Tunda.
A lower-confidence lead. A sighting at
Pulau Pari cannot locate extraction at
Tunda.
KKP reported about 24,000 m³ of sand aboard at inspection and described the reported origin and
permitting issues as suspicions at the time. The agency documents establish a response and a cargo
observation. They provide no time-matched optical or ecological measurement at the reported
extraction site. [5] [6] [17]
The counterexample matters
The published record shows that a field action can occur on a day with no cataloged scene. An
analysis centered on clear adjacent dates cannot reconstruct the conditions at the time of that
action.
Search windows: 12 Oct–11 Nov (6 returned dates) and 12–27 Nov (3 dates). This historical screen uses the broad mask SCL
2/4/5/6, rounded. It supports the timeline and is a separate analysis from the 2025–26 windows. [8] [9]
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
08 / 15

Links embedded on this page

- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://www.walhi.or.id/kapal-vox-maxima-kembali-beroperasi-di-perairan-pulau-tunda-dan-teluk-jakarta-koalisi-ngo-desak-penegakan-hukum-lingkungan
- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html

#### PDF page 9

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
FINDING 4 / HABITAT AND ATTRIBUTION
A clear ring can hide a cloudy reef
sector
The surface view needs to be judged over the specific habitat or water area that matters to
the decision.
Figure 5. Modified Copernicus Sentinel-2 L2A and UNEP-WCMC archival reef geometry. The underlying reef record was dated
1999–2002 and marked unvalidated. The outline provides historical spatial context. [8] [32]
On 26 October 2023, broad classified coverage reached 95.3% in the ring and 90.8% on the
historical reef footprint within 3 km. The footprint’s western half retained 75.8% versus 98.4% in its
eastern half. Only 43.4% of the archival footprint’s raster cells fell inside the ring. The two geographies
answer visibly different questions.
The 2025–26 coverage series shows the same scale issue from another direction. On 19 Dec 2025 only
the northeast quadrant passed the broad 90% screen. The full ring was 38.7%. That partial view falls
inside the 119-day interval with no full-ring pass.
A locally observed signal can still reflect river runoff, dredging, seabed or atmospheric effects.
Regional research models river sediment delivery to Tanjung Pontang. A separate Banten Bay study
measured 102 mg/L suspended solids on a date with zero reported production for the operator it
tracked. Neither finding assigns a source to a Tunda scene. [3] [12] [13] [27]
Field transects from Tunda document heterogeneity by sector and depth. The studies use different stations and
measurement designs, so the report uses them as ecological context. Exposure duration, source and coral response remain
separate questions. [3] [4] [14] [23] [29]
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
09 / 15

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1/7554
- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.15578/jkn.v1i2.6614
- https://doi.org/10.1016/j.rse.2019.03.010
- https://doi.org/10.15578/segara.v14i1.7149
- https://doi.org/10.22373/kenanga.v5i2.8470
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://dlhk.bantenprov.go.id/storage/dlhk/upload/article/2023/Analisis_Dampak_Tambang_Pasir_Laut_Terhadap_Ekosistem_Terumbu_Karang_di_Perairan_Pulau_Tunda.pdf
- https://ejournal.undip.ac.id/index.php/ijms/article/view/28649

#### PDF page 10

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
RESPONSE PATHWAY
Indonesia already has a route from
a signal to inspection
The strategic question is what evidence helps an existing reviewer act.
Step
What current rules or cases show
01 Observe
Marine spatial oversight includes indirect observation through satellite or
spatial monitoring reports. Community reports also appear in PSDKP
records.
02 Assess and inspect
An indication can trigger field inspection. Relevant checks include location,
approvals, standards, testimony and documentation, with sampling where
needed.
03 Record and follow
up
The supervision report records chronology, findings and supporting
evidence. The competent authority follows up under its mandate.
Present regulatory baseline: KKP Regulation 30/2021 as amended by 5/2025, arts. 8, 19 and 28. It identifies the current
process. The October 2023 case is separately sourced. [7]
Three records show different levels of evidence
Tunda. KKP documents a vessel inspection and a parallel information-gathering step on the same
day. The reviewed records do not provide the original intake timestamp, a final case disposition or a
matched reef sample. [5] [6]
Tulang Bawang. KKP records a community sand-mining report followed by a field visit that found no
activity at the site at the time of inspection. The visit’s result leaves the original report unresolved. [24]
Karimun. In a distinct tin-sand case, officials used georeferenced vessel logbook entries and the
approved spatial area to report operations beyond the approved polygon. That demonstrates the
evidentiary value of precise activity records for a location claim. [28]
Benchmark for originality
UNEP Marine Sand Watch already uses vessel signals to track dredging. Indonesia already names
satellite information as a supervision input. The evidence points toward the narrower question of
what makes a date and location worth verifying.
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
10 / 15

Links embedded on this page

- https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://www.kkp.go.id/download-pdf-akuntabilitas-kinerja/akuntabilitas-kinerja-pelaporan-kinerja-laporan-kinerja-direktorat-pemantauan-dan-operasi-armada-tahun-2020.pdf
- https://kkp.go.id/djpsdkp/kkp-hentikan-pengerukan-pasir-timah-tak-sesuai-pkkprl-di-kepri65c3055e50ef8/detail.html

#### PDF page 11

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
INDEPENDENT CHALLENGE
What survived the attempt to
overturn it
The conclusion is strongest at the observation step. Exposure, source and response require
different evidence.
Candidate root cause
Finding after challenge
Strength for this report
Tile metadata can discard
local views
At Tunda, 23 of 52 local passes fail the 20%
comparison cutoff. Raising the cutoff to 40%
alters which dates disagree. Kodingareng
shows misses in both directions at 20%.
Demonstrated screening
mechanism under the
stated thresholds.
Coverage gaps constrain
reconstruction
Low classified-water coverage persisted in
both islands’ Nov–Feb sample. At Tunda,
archive checks support the same date
inventory and reproduce the pixel counts.
Demonstrated for the
sampled dates, footprints
and optical archive.
Recurring sediment
exposure harms reefs
Published transects show habitat
heterogeneity. The archival footprint and
2023 event cannot establish repeated
source-linked exposure or impact.
Exposure and harm
unresolved for the event.
Dredging caused a
repeated local anomaly
The strongest optical contrast overlaps land.
Direction varies across dates, and
documented sources are not matched to
each acquisition.
Plausible hazard. Specific
repeated causation remains
unresolved.
A weak institutional
handoff delayed action
The October case includes a documented
action. The record available for this study
does not establish intake-to-action timing or
why a delay would occur.
No case-level causal finding
on delay.
What changed after independent review
The review independently reproduced the main counts from another catalog collection, checked the
class histograms, and challenged the headline against looser tile cutoffs and tighter local thresholds.
The resulting claim is about screening and reconstruction, with an explicit distinction between
classifier output and optical suitability.
At a 95% water-class threshold, Tunda’s four-window local counts are 11, 1, 6 and 21. At 90%, an alternate 1.5–2.5 km footprint
adds one qualifying Jun–Sep 2026 date. The main finding and its period dependence survive these checks. [8] [9] [30] [31]
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
11 / 15

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://stac.dataspace.copernicus.eu/v1/
- https://earth-search.aws.element84.com/v1/collections/sentinel-2-c1-l2a

#### PDF page 12

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
TRANSFER TEST
The second island changes the
screening story
Kodingareng shares the scarcity in the second window. Its June–September screening
disagreement goes both ways.
Tunda / Jun–Sep 2025
10 tile / 17 local / 30 dates
Kodingareng Lompo / Jun–Sep 2025
11 tile / 10 local / 31 dates
Tunda / Nov 2025–Feb 2026
0 tile / 1 local / 27 dates
Kodingareng Lompo / Nov 2025–Feb 2026
0 tile / 0 local / 28 dates
Figure 6. Gray = tile cloud ≤20%. Teal = local SCL class 6 ≥90%. Labels include the denominator for each row. Counts overlap
within each sample.
Figure 7. Modified Copernicus Sentinel-2 L2A, Kodingareng Lompo, 2 Jul and 27 Sep 2025. SCL flagged thin cirrus over much of
the apparently clear second scene. The first shows faint visible wisps even though the ring passed. [8] [9]
In Jun–Sep, one Kodingareng date passed only locally and two passed only the tile cutoff. In Nov–Feb,
no date reached 90% locally. The second site therefore supports the need for local interpretation
while showing that a local screen can add or remove dates depending on the site. Its dredging history
dates to 2020. The 2025–26 image sample is a transfer test of the observation method. [10] [11]
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
12 / 15

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://doi.org/10.30872/mulrev.v6i2.621
- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf

#### PDF page 13

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
BILATERAL RESEARCH FIT
Independent replication is a
concrete Russian role
Indonesia’s case stands on its own. A paired analysis helps determine which conclusions
travel.
Who
A concrete contribution
What would count as evidence
Indonesian
researchers and
coastal practitioners
Reconstruct more Indonesian events
and map which recorded
information would support local
inspection or field observation.
Dated events, precise geography where
public, explicit reference dates, and
consistent observation rules.
Possible Russian
research counterpart
Pacific Oceanological Institute FEB
RAS has a satellite oceanography lab.
Amur Bay and the Razdolnaya
estuary are candidate settings for an
independent coastal replication.
A separate date series and source
context. A supported contrast showing
which interpretation survives when
background inputs and coastal
conditions differ.
Joint research and
training channel
The June 2026 bilateral consultation
agreed on a working group for
people, research, and training,
alongside marine resources and
industry work.
A reproducible method and an agreed
comparison protocol. Institutional
participation would need separate
confirmation.
A comparison at a coast with documented river input has a scientific purpose. It makes it harder for
the Indonesian analysis to mistake any bright feature or sediment-bearing plume for extraction. A
Russian partner could independently apply the same screening definitions and explain which
variables need local interpretation. [15] [16] [25] [26]
Share the question and the evidence rules
Keep the requirements for dates, footprints, imagery screening and independent source evidence
portable. Treat tides, rainfall and discharge, water optics, habitat and the available public records as
site-specific inputs.
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
13 / 15

Links embedded on this page

- https://kemenkoinfra.go.id/detailpost/menko-ahy-pimpin-konsultasi-bilateral-indonesia-rusia-sepakat-perkuat-kerja-sama-perkapalan-dan-konektivitas-maritim
- https://www.poi.dvo.ru/en/structure/lab94
- https://interfax.com/newsroom/top-stories/117869/
- https://meetings.pices.int/Publications/Presentations/PICES-2017/S13-Pavlova.pdf

#### PDF page 14

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
STRATEGIC DIRECTION
Prioritize evidence for the
verification decision
For LAUTARA, the strongest lead is the gap between a possible event and what a reviewer can
establish about it.
Decision
Evidence-based direction
What could reverse it
Lead problem
Use Tunda to show that observation
availability and source attribution
constrain event reconstruction. Show
the dated inspection as the concrete
case.
Time-matched evidence showing the
events of interest are already
routinely visible and reliably
attributed in practice.
What the approach
must eventually do
Account for local coverage and the
timing of the sighting. Preserve
uncertainty about the source and point
clearly to the evidence needed for a field
decision.
Operational evidence that the main
constraint instead sits in a later step,
such as field availability or authority.
Scope and transfer
Use Kodingareng to show where the
method travels and where the pattern
changes. Give a prospective Russian
counterpart responsibility for
independent replication.
An independently rerun comparison
showing the same rules measure a
different phenomenon or miss
critical local conditions.
An argument the team can defend
For documented coastal sediment events, the immediate challenge is assembling evidence that can
guide verification. An enforcement decision draws on its own inspection record and legal authority. At
Tunda, screening the actual area recovers views that a whole-tile rule would discard, but there are still
long stretches without a broadly qualifying view. In 2023 an official inspection happened between
cataloged acquisitions. Kodingareng shows the same second-window scarcity, while its earlier
screening disagreements differ.
The report establishes the limits of the observation chain and identifies a real verification decision. To
go further into source attribution, the decisive missing evidence is an independently dated activity
footprint with a credible transport context and matched controls. To go further into operational delay,
it is a timestamped intake-to-action record.
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
14 / 15

#### PDF page 15

LAUTARA 2026 / COASTAL SEDIMENT DIAGNOSTIC
SOURCES AND REPRODUCIBILITY
Trace every major claim to its
evidence
Numbered references are clickable. The PDF also includes the scene-level tables and the
optical sector measurements as attachments.
Archive specification. Tunda query bounding box [106.20, −5.86, 106.32, −5.76], tile T48MXU (EPSG:32748). Kodingareng tile
T50MQV (EPSG:32750). Pixel centers between radii 1,500 and 3,000 m are included, with all ring pixels in the denominator.
Time windows use inclusive UTC dates. Each site and window returned one item per analyzed date. Rasters were read from
Earth Search with GDAL and calculated in Python. Independent checks compared Collection 1 and official Copernicus matches
for the four Tunda windows, and reread Collection 1 SCL assets. The separate historical event screen uses classes 2, 4, 5 and 6.
The two-site comparison covers the first two windows only.
Optical check. Four fixed cardinal sectors. Median red and green L2A band values were sampled on the 10 m grid in
water-classed pixels on 18 dates in the first two windows. The acquisition is the observation unit. An optical contrast flags a
scene for scrutiny. It does not identify a pollutant concentration or its source.
[1] LAUTARA 2026 official participant guidebook, chapters 3–6
[2] UNEP (2023). Marine Sand Watch and global marine
dredging estimates
[3] Wahyudi et al. (2023). Tunda reef survey and MIKE 21
modelling
[4] Fatmawati et al. (2025). Tunda reef transects collected in
2021–22
[5] KKP (2023). Stop and inspection of reported dredging
activity, 27 October
[6] KKP Loka PSPL Serang FY2023 performance report, p. 38
[7] KKP JDIH. Regulation 5/2025 amending 30/2021, arts. 8, 19
and 28
[8] Element 84. Earth Search v1 and Sentinel-2
Cloud-Optimized GeoTIFFs
[9] Copernicus. Sentinel-2 classification codes and processing
outputs
[10] Kurniawati et al. (2021). Kodingareng fishers, fieldwork
and policy evidence
[11] Boskalis. Makassar New Port project sheet,
contractor-reported scope
[12] Banten Bay regional sediment transport study, Tanjung
Pontang
[13] Vanhellemont (2019). Aquatic atmospheric correction for
Landsat and Sentinel-2
[14] Erftemeijer et al. (2012). Sediment disturbances and
corals: a review
[15] Kemenko Infra (1 June 2026). Bilateral maritime working
groups
[16] Pacific Oceanological Institute FEB RAS. Satellite
oceanography lab
[17] WALHI coalition (November 2023). Reported observations
near Pulau Pari
[18] Natural Earth. 1:10m land polygons
[19] Mapcarta. Tunda Island geographic anchor
[20] Mapcarta. Kodingareng Lompo geographic anchor
[21] Allen Coral Atlas. Reef habitat and geomorphic mapping
data
[22] Copernicus Data Space. Sentinel-2 mission and products
[23] Banten DLHK archive. Local transects and potential
pressures on reefs
[24] KKP PSDKP (2020). Monitoring and fleet operations, table
7
[25] Interfax (June 2026). Russian leads and joint action plan
[26] PICES (2017). Razdolnaya River estuary research setting
[27] Ernas et al. (2018). Banten Bay TSS and reported
extraction pairs, table 2
[28] KKP (2023). Karimun tin-sand inspection and spatial
compliance case
[29] Mujiyanto et al. (2020). Tunda reef condition by sector and
depth
[30] Copernicus Data Space Ecosystem. STAC catalog
[31] Earth Search. Sentinel-2 Collection 1 L2A STAC collection
[32] UNEP-WCMC. Global Distribution of Coral Reefs, v4.1
historic polygon 7554
LAUTARA 2026 / RESEARCH BRIEF / 21 NOVEMBER 2026
15 / 15

Links embedded on this page

- https://chatgpt.com/library?file_id=libfile_a0f1f94bc47c81919f0b91c5fbf16337
- https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans
- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.22373/kenanga.v5i2.8470
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765
- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://doi.org/10.30872/mulrev.v6i2.621
- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- https://doi.org/10.15578/jkn.v1i2.6614
- https://doi.org/10.1016/j.rse.2019.03.010
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://kemenkoinfra.go.id/detailpost/menko-ahy-pimpin-konsultasi-bilateral-indonesia-rusia-sepakat-perkuat-kerja-sama-perkapalan-dan-konektivitas-maritim
- https://www.poi.dvo.ru/en/structure/lab94
- https://www.walhi.or.id/kapal-vox-maxima-kembali-beroperasi-di-perairan-pulau-tunda-dan-teluk-jakarta-koalisi-ngo-desak-penegakan-hukum-lingkungan
- https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/
- https://mapcarta.com/15591682
- https://mapcarta.com/16118912
- https://allencoralatlas.com/resources/
- https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-missions/sentinel-2
- https://dlhk.bantenprov.go.id/storage/dlhk/upload/article/2023/Analisis_Dampak_Tambang_Pasir_Laut_Terhadap_Ekosistem_Terumbu_Karang_di_Perairan_Pulau_Tunda.pdf
- https://www.kkp.go.id/download-pdf-akuntabilitas-kinerja/akuntabilitas-kinerja-pelaporan-kinerja-laporan-kinerja-direktorat-pemantauan-dan-operasi-armada-tahun-2020.pdf
- https://interfax.com/newsroom/top-stories/117869/
- https://meetings.pices.int/Publications/Presentations/PICES-2017/S13-Pavlova.pdf
- https://doi.org/10.15578/segara.v14i1.7149
- https://kkp.go.id/djpsdkp/kkp-hentikan-pengerukan-pasir-timah-tak-sesuai-pkkprl-di-kepri65c3055e50ef8/detail.html
- https://ejournal.undip.ac.id/index.php/ijms/article/view/28649
- https://stac.dataspace.copernicus.eu/v1/
- https://earth-search.aws.element84.com/v1/collections/sentinel-2-c1-l2a
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1/7554



### 02 Before the Plume Reaches the Reef


Extracted text by printed PDF file page. Use the original for tables, reading order, diagrams and page geometry.

#### PDF page 1

LAUTARA 2026 / RESEARCH ARTICLE
Before the plume
reaches the reef
Evidence for siting extraction, timing work, and deciding when
to verify
TUNDA / KODINGARENG LOMPO / AMUR BAY
Design prevention into coastal work. Identify the receptor before operations begin, establish what
conditions can move sediment toward it, and give reviewers a way to act when the available evidence
is incomplete.
Comparative public-data research for the Russia–Indonesia Maritime Hackathon. 21 November 2026. Coastlines: Natural
Earth. [1] [16]
LAUTARA 2026 / COASTAL SEDIMENT STUDY
01 / 25

Links embedded on this page

- https://chatgpt.com/library?file_id=libfile_a0f1f94bc47c81919f0b91c5fbf16337
- https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/

#### PDF page 2

BEFORE THE PLUME REACHES THE REEF
ABSTRACT
Move the decision earlier
The study traces eight choices from site selection and work timing through verification and
prevention of recurrence.
Objective. Determine what open satellite, environmental, habitat and official records can tell a
reviewer before, during and after a suspected sediment event. Tunda and Kodingareng are the main
study sites. Amur Bay contributes an independent, river-influenced case.
Methods. Reproduce earlier results, extend the observation record, compare acquisition-level and
receptor-level screening, align data and event clocks, and challenge temporal and spatial
interpretations with competing sources. Retrospective observations and evidence available at decision
time are tracked separately.
Results. The Indonesian Sentinel-2 catalog inventory spans 1,178 site-dates from 2019 through
October 2026. Over the complete matched 2025–26 window, Landsat adds 15 qualifying Tunda dates
and 25 Kodingareng dates. In Nov–Dec 2025 only one of 72 higher-rain site-days cleared the local
screen using either sensor. At Amur Bay both missions independently saw the same direction of
optical contrast on 6 September 2023, while a qualified pre-flood Landsat scene showed an even
stronger contrast.
Interpretation. The lowest-regret opportunity is to establish receptor-specific evidence requirements
before work starts. Distances and regional currents can guide where to check transport. Work
restrictions, compliance determinations and ecological claims require different evidence.
Decision contribution
The article gives planners, operators and reviewers a way to choose among siting, timing, precaution,
field verification and follow-up. It shows which questions are supported by the public record and
which would benefit from a better local record.
Keywords: sea-sand extraction, optical remote sensing, sediment transport, reef exposure, marine spatial oversight,
Indonesia–Russia cooperation.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
02 / 25

#### PDF page 3

BEFORE THE PLUME REACHES THE REEF
INTRODUCTION
Plan around where sediment can
go
A viable coastal decision connects an activity, its potential pathway, a receptor, and the
people who can act.
Marine dredging moves billions of tonnes of sand and other sediments globally. At reefs, exposure can
vary with the magnitude, duration and frequency of suspended sediment and deposition, as well as
local tolerance. This makes the transport pathway and the receptor as important as identifying an
activity. [2] [3] [4]
A public reconstruction can begin after a short-lived event has passed and the original conditions are
difficult to recover. The October 2023 Tunda record illustrates this timing problem: there is a dated
stop and inspection, but the timing and location of the reported extraction itself are uncertain. [5] [6]
Step
Question
Evidence that earns weight
Activity
Was work documented here and
when?
Georeferenced work log, report, or authoritative
record.
Transport
Could material reach a sensitive
area?
Local observations or scale-appropriate currents,
tide, waves, or modeled connectivity.
Exposure
What reaches which receptor, for
how long?
Receptor-specific water measurements, defensible
optical context, and a local baseline.
Action
Who can decide, and with what
information?
Permits and mandates, timestamps, verification
records, and proportional action.
What prevention means here
A planning decision can reduce exposure before an event. An observation can prompt a targeted field
check. A compliance finding or determination of harm calls for evidence appropriate to that decision.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
03 / 25

Links embedded on this page

- https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans
- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf

#### PDF page 4

BEFORE THE PLUME REACHES THE REEF
STUDY GEOGRAPHY
Use each coast to answer a
different question
Two Indonesian cases establish practical relevance. The Russian case tests how easily a
river-influenced signal can resemble a sediment-event lead.
Figure 1. Regional locators. Marks identify study anchors, independent of permit polygons, fishing-ground boundaries, and
vessel tracks. Land: Natural Earth. [16]
Case
Geographic and historical evidence
Tunda Island
Banten shelf setting. Archived reef outlines, field literature and a documented KKP
stop and follow-up inquiry. Main case window: Oct–Nov 2023. [3] [5] [6] [15]
Kodingareng Lompo
Spermonde reef and fishing setting. A contractor documents reclamation-related
extraction in Feb–Oct 2020. Fishing-area accounts supply relevant places and dates,
with one disputed coordinate-distance relation. [11] [12] [13]
Amur Bay
Razdolnaya estuary, Russian Far East. The 2023 flood provides an independently
documented source of freshwater influence and a demanding comparator for
image-based attribution. [22] [23] [24]
Reef footprints anchor the quantitative exposure-screening comparison in Indonesia. Fishing grounds
are a distinct human-use receptor. The analysis uses documented fishing context and keeps spatial
confidence visible when exact boundaries are missing.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
04 / 25

Links embedded on this page

- https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/
- https://doi.org/10.2478/cjf-2023-0009
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- https://doi.org/10.30872/mulrev.v6i2.621
- https://tribratanews.polri.go.id/blog/hukum-4/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716
- https://www.meteorf.gov.ru/press/news/34448/
- https://dfo.meteorf.gov.ru/news/889/
- https://doi.org/10.3390/jmse10121798

#### PDF page 5

BEFORE THE PLUME REACHES THE REEF
STUDY DESIGN
Keep all eight decisions on the
table
Prevention gets the most space. Case replays show how evidence changes choices across the
whole sequence.
Stage
Decision
Comparison
Before work
1 Where should extraction proceed?
Distance screen versus receptor and
transport context.
Before work
2 When should work proceed?
Compare recurring conditions and model
support at useful scales.
During work
3 When does a lead justify a change?
Compare sensory cue, corroborated lead,
and authorization thresholds.
During work
4 What exposure gets priority?
Contrast duration and recurrence with
one dramatic observation.
Before / during
5 Which source should be controlled?
Compare documented activity, prior rain,
regional conditions and alternative
explanations.
Before work
6 What must be recorded upfront?
Replay cases with and without publicly
evidenced early records.
During / after
7 Where and when should someone verify?
Compare sensor availability over the
specific receptor and case time.
Afterward
8 What prevents a repeat?
Inspect dispositions, follow-up records
and what changes for future work.
Each result is assigned to a measurement, a documented event, a bounded interpretation, or a
scenario. That distinction is what lets the paper make a strong argument without turning a screening
calculation into an ecological or legal conclusion.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
05 / 25

#### PDF page 6

BEFORE THE PLUME REACHES THE REEF
METHODS
Measure the data before trusting
an inference
Source resolution, timestamps and detection rules travel with every figure.
Layer
Unit and quality check
What it can establish
Sentinel-2 / Landsat
Date and sensor. Read local SCL or QA_PIXEL
values and retain footprint denominators.
Deduplicate catalog items before comparison.
Local classified coverage and distinct
opportunities.
Reef geometry
Rasterize archived polygons in local UTM.
Compare with a 1.5–3 km annulus and
subdivide receptor areas.
Coverage of the mapped footprint.
Rain and marine
conditions
Daily satellite/gauge products and regional
modeled wind, wave and current fields. Record
grid and time support.
Competing explanations and
plausible regional conditions.
Case documents
Record event, observation and publication
times where documented. Retain uncertainty in
location and scope.
Official actions and documented
leads.
Scenario stress tests
Use transparent assumptions with
independently recalculated outputs and explicit
sensitivity.
How a choice changes under stated
conditions.
The local screening rules answer a question about the imagery footprint. They do not establish
sediment concentration, underwater exposure or equipment activity. Water-quality interpretation also
requires care around atmospheric effects, shallow bottoms, sunglint and uneven coverage. [8] [9] [10]
[15] [27]
Triangulation standard
Treat the same satellite scene from two catalogs as a reproducibility check. Treat a field record and an
independently acquired scene as two different observations. If two modeled products share forcing or
source data, preserve that dependency in the interpretation.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
06 / 25

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- https://doi.org/10.1016/j.rse.2019.03.010

#### PDF page 7

BEFORE THE PLUME REACHES THE REEF
RESULTS · OBSERVATION I
Add dates that change the
observation calendar
The aim is to observe the receptor near the relevant time. More catalog hits matter only
when the local screen passes.
Figure 2. Annual Indonesian Sentinel-2 inventory, readable rasters and broad local screen passes. Acquisition dates are UTC.
Readability and quality are separately encoded. The 2026 window ends on 31 October. [8, 9]
Of 1,178 Sentinel-2 site-dates, 1,177 had readable QA. The Landsat series adds 799 scene records
with readable QA, spanning 282 unique Tunda dates and 280 Kodingareng dates. Some Landsat paths
overlap on the same date. The one unresolved Sentinel-2 mask remains unknown in the denominator.
Across the series, Tunda passed on 5 of 93 January–February dates and 87 of 156 July–September
dates. Kodingareng passed on 13 of 95 and 95 of 155 respectively. Among 939 paired legacy and
Collection 1 masks, 17 passed the 90% broad rule in only one product version.
Decision 7 · Spend field effort on the relevant ground
Use date and footprint screening to identify which areas have observations near the report time.
Mark imagery gaps explicitly so they can be routed to another observation source.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
07 / 25

#### PDF page 8

BEFORE THE PLUME REACHES THE REEF
RESULTS · OBSERVATION II
Give a second sensor one job:
close gaps
A second mission earns its place when it contributes a qualifying opportunity on a different
date.
Figure 3. Combined scene-screen opportunities, 1 Jan 2025–31 Oct 2026. Accepted dates have at least 90% broad local QA
retention over the site annulus.
Adding Landsat raised the qualifying date count at Tunda from 62 to 77 and at Kodingareng from 63 to
88. Among 662 candidate dates per site with full follow-up, the share with a qualifying observation on
the same day or within seven days rose from 51.2% to 57.7% at Tunda and 48.2% to 55.6% at
Kodingareng.
The longest calendar run without a qualifying view, including window edges, changed from 132 to 131
days at Tunda and 162 to 158 at Kodingareng. The second mission improves routine opportunities
while long periods still call for a separate observation route.
Landsat QA_PIXEL flags and Sentinel-2 SCL class codes are different screening systems. A joint calendar
can use a common coverage threshold after each mission applies its own quality screen. Optical color
comparisons require separate harmonization. [9] [10] [29] [30]
Decision 6 · Set the baseline before the incident
A receptor-specific baseline benefits from dates with known observations, weather, and activity
context. Few views in a critical season justify planning additional ways to observe, especially when the
operational response window is short.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
08 / 25

Links embedded on this page

- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands
- https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- https://hls.gsfc.nasa.gov/data-access-and-tools/

#### PDF page 9

BEFORE THE PLUME REACHES THE REEF
RESULTS · RECEPTOR GEOGRAPHY
Score the place people actually
need to see
An island-wide score can miss the habitat a reviewer would choose to protect or visit.
Figure 4. Broad SCL classes 2, 4, 5 and 6, annulus versus archived reef polygon within 3 km. Plotted historical and baseline
subsets use the available cached target-tile COG roster. Dashed lines mark the 90% screen. The all-years Tunda tally is
separate. [8] [9] [15]
Across Tunda’s 587 readable dates, 34 decisions differed by footprint: 10 passed only the annulus
and 24 passed only the archived reef. The annulus covered 43.4% of mapped reef pixels within the 3
km disc. Kodingareng had 109/109 readable dates in the bounded habitat sample, with 0 annulus-only
and 8 reef-only passes. The fixed annulus included 5.7% of the mapped reef pixels inside 3 km.
The previous-day Tunda example illustrates the physical implication. On 26 October 2023 the broad
ring score was 95.3%, but the western half of the archived reef footprint scored 75.8%. That footprint
establishes a geographic sensitivity example. Contemporary reef condition and sediment dose require
different evidence. [38]
Decisions 4 and 7 · Put the receptor in the denominator
Track coverage over the reef or documented fishing area that matters to the actual decision. A
fixed-radius overview can remain useful for context.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
09 / 25

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- https://chatgpt.com/library?file_id=libfile_61a9ace26b688191a4897fac7ce72ee4

#### PDF page 10

BEFORE THE PLUME REACHES THE REEF
RESULTS · IMAGE INTERPRETATION
Demand a second clue before
naming a source
A strong-looking color contrast can fail an elementary physical check.
Figure 5. Modified Copernicus Sentinel-2 examples, 22 and 24 Jul 2025. In the latter image the conspicuous brightness
crosses land and water. This earlier example is reused as a negative check on source attribution. [38]
The prior analysis found an east-to-west brightness contrast that changed direction across dates, with
its strongest example extending over land. This is compatible with an atmospheric or surface artifact
and weakens a sediment-only interpretation. It remains useful as a quality-control example for the
expanded study.
Natural causes are plausible too. Regional Banten Bay modeling illustrates river-sediment transport. A
separate Banten Bay field dataset reported elevated suspended solids on a date with zero production
recorded for the operator under study. Neither case identifies the source of a particular Tunda signal.
[33] [44]
Decision 5 · Separate source hypotheses from actions
A visual clue can justify checking vessel or environmental context. Source-specific control needs
evidence tying the activity, pathway, and receptor together.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
10 / 25

Links embedded on this page

- https://chatgpt.com/library?file_id=libfile_61a9ace26b688191a4897fac7ce72ee4
- https://doi.org/10.15578/jkn.v1i2.6614
- https://doi.org/10.15578/segara.v14i1.7149

#### PDF page 11

BEFORE THE PLUME REACHES THE REEF
RESULTS · TUNDA EVENT
Build the record before the
response clock starts
The 27 October 2023 government action is documented. The public record leaves the
sediment release time and location open.
Figure 5a. Public sensor inventory and two product lineages for the 26 Oct Sentinel-2 acquisition. [8] [28] [29] [30]
Date / clock
Evidence
Meaning for a reviewer
27 Oct
KKP reported a stop and inspection. About
24,000 m³ of sand was aboard.
Confirmed inspection and cargo observation.
Origin and permit issues were described as
suspected.
29 Oct
KKP published its release.
Public documentation of the agency account
followed the action by two calendar days.
The scoped inventory returned six Sentinel-2, four Landsat and three Sentinel-1 dates. None was 27
Oct. Earth Search metadata identify a 26 Oct archived version. Today’s Copernicus product was
reprocessed later. Neither establishes receipt by a reviewer. [5] [6] [28] [29] [31]
Decisions 3 and 6 · Specify evidence that can arrive in time
Record work location and time as operations happen. Give a reviewer an independent path to assess
location-specific leads while a contemporaneous image is unavailable.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
11 / 25

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://stac.dataspace.copernicus.eu/v1/
- https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- https://hls.gsfc.nasa.gov/data-access-and-tools/
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://www.esa.int/media/sentinel-1-tracking-maritime-traffic

#### PDF page 12

BEFORE THE PLUME REACHES THE REEF
RESULTS · TUNDA ENVIRONMENT
Check whether rain offers a
competing pathway
Weather context should change the order in which explanations are checked. Transport and
source still depend on local evidence.
Figure 6. Tunda and Kodingareng, full 2025 and Nov–Dec subset. Site-days with mainland IMERG proxy rain ≥10 mm. Broad
local screen ≥90% on either mission. [8] [10] [17] [18] [41] [46]
On the UTC date before the inspection anchor, NASA IMERG’s mainland proxy mean was 16.1 mm
(87th percentile of same-month outside-year reference dates). Its input pixels ranged from 0 to 30.1
mm. CHIRPS estimated 2.0 mm and CPC 0.0 mm for the same labeled date. Across the preceding three
days, the IMERG estimate was near its 60th percentile.
On 4 Nov, all three products indicated at least 24 mm of regional rain. Activity that day is unresolved.
Across both islands in Nov–Dec 2025, only 1 of 72 higher-rain site-days qualified with either optical
mission. Of the rest, 49 had no acquisition in these inventories and 22 had acquisitions below the local
screen. In 2025, acquisition rates were similar on higher- and lower-rain days (31.5% and 30.7%).
Among dates with an acquisition, 16.0% and 35.9% passed respectively.
Decision 5 · Treat weather as a discriminating question
Ask whether the anomaly makes sense after regional rain, wind or wave changes, and where a
river-linked pattern would appear. Keep an activity-linked hypothesis alive when the record supports
it.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
12 / 25

Links embedded on this page

- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands
- https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary
- https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html
- https://www.chc.ucsb.edu/data/chirps

#### PDF page 13

BEFORE THE PLUME REACHES THE REEF
RESULTS · SOUTH SULAWESI CASE
Protect the fishing place people
actually use
Kodingareng shows why historical project scope, fishing activity and geolocation have to be
recorded separately.
Evidence
What it establishes
Consequence for analysis
Boskalis project record
Approx. 11 million m³ transported for
phases 1B–1C. Contractor dates marine
extraction Feb–Oct 2020.
Supports a project-period comparison.
Daily release times and precise borrow
geometry need separate evidence.
Fisher and community
records
Fieldwork and community accounts
document contested access and
reported effects.
Identify fishing use as a separate receptor
and preserve the accounts as qualitative
evidence.
12–13 Sep reported
incident
The published police account gives a
point about 2.24 km from the island
anchor and a narrative distance of 11
miles. Its weekday and date also
disagree.
Keep the disputed coordinate out of
source-to-receptor transport distances.
DPR visit report, 2024
Reports SDKP investigated, examined
firms and heard fishers. It records no
violation found in the reported follow-up.
Regulatory disposition has a defined
scope. Ecological and livelihood outcomes
require their own evidence.
A near-reef analysis can be spatially tidy while the actual point of concern is a fishing ground farther
away. This case preserves that distinction. It supports a request for dated, bounded fishing-use
evidence before ranking which fishing area could be affected. [11] [12] [13] [14] [43]
Decisions 1 and 8 · Retain the receptor and the follow-up scope
Spatial planning needs a defensible receptor location. Incident closure needs a clear statement of
what was investigated, what was established and which consequences were outside that finding.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
13 / 25

Links embedded on this page

- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- https://doi.org/10.30872/mulrev.v6i2.621
- https://tribratanews.polri.go.id/blog/hukum-4/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716
- https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf
- https://www.greenpeace.org/static/planet4-indonesia-stateless/2021/03/17185db9-gp-spermonde-report-v8.pdf

#### PDF page 14

BEFORE THE PLUME REACHES THE REEF
RESULTS · SOUTH SULAWESI ENVIRONMENT
Give historical comparisons a
season-matched baseline
The project period spans multiple weather conditions. Compare candidate episodes with
ordinary conditions from the same parts of the year.
Figure 7. Regional daily precipitation during the documented project period. The early reported start and September incident
are separate chronology markers. [11, 13, 17, 41, 43, 46]
At the reported 13 February start, prior three-day precipitation was 22.6 mm from IMERG, 58.9 mm
from CHIRPS and 21.3 mm from CPC. The IMERG result was near the 37th percentile of same-month
outside-year conditions. On 5 March, all three products showed 47.6–53.1 mm for the product day.
During Feb–Oct 2020, 54 Sentinel-2 and 17 Landsat island-footprint QA dates were measured, with 26
and 10 broad passes respectively. The reported 12 Sep incident date had no acquisition in either
scoped inventory. Because the published day is uncertain and the project envelope is not a daily log,
the views cannot confirm whether imagery captured a particular work period.
Decisions 2 and 5 · Require the operating clock
For work-window screening, join the conditions to the actual operating date, time and location. Until
that record is available, use historical distributions to identify which conditions merit closer local
analysis.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
14 / 25

#### PDF page 15

BEFORE THE PLUME REACHES THE REEF
RESULTS · MARINE CONDITIONS
Use regional currents to decide
where to look closer
The two Indonesian cases contain directional information at regional scales. Local pathways
need finer or field-supported evidence.
Figure 8. Monthly share of daily regional GLORYS12 current vectors with an eastward component, 2019–25. Study-year
emphasis is labeled in the panels. [21]
At the Kodingareng reference cell, 139 of 274 days had an eastward component at 0.494 m modeled
depth versus 230 of 274 at 9.573 m. Nearby surface cells disagreed on the east–west sign on 92 days.
Conversely, all nine Tunda neighborhood cells in the 31-day event window had westward components
at both depths. The SMOC hourly surface series was also westward through the Tunda inspection date
in WIB. The two Tunda current products are related model evidence.
The 92,052-vector reference series covers both sites, nine cells, two depths and 2,557 UTC dates. At
Kodingareng, June 2020 near-surface and deeper eastward shares were 13.3% and 86.7%;
comparison-year June medians were 41.7% and 83.3%. The grid can guide local checks. It cannot set
reef-scale boundaries. [3] [4] [20] [21] [42]
Decisions 1 and 2 · Spend local modeling effort where it changes the choice
Use the regional pattern to screen alternative sites or periods. Prioritize local pathway checks where
changing assumptions would reverse the ordering.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
15 / 25

Links embedded on this page

- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://open-meteo.com/en/docs/marine-weather-api
- https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description

#### PDF page 16

BEFORE THE PLUME REACHES THE REEF
RESULTS · TRANSPARENT SCENARIOS
Test whether “nearest reef first”
is robust
A simple transport scenario exposes the decision sensitivity before anyone spends effort on
a detailed model.
Figure 9. Analyst-designed kinematic scenarios. Panel A multiplies a constant speed by elapsed time. Panel B uses fictional
geometry to illustrate how distance and direction can rank receptors differently.
At 0.10 m/s a parcel would travel 2.16 km in six hours under a constant straight-line assumption. At
0.25 m/s the distance is 5.40 km. That 3.24 km difference is already larger than the width of the 1.5–3
km annulus used for observation screening. It shows how a convenient observation footprint can
diverge from a plausible transport scale.
The figure is a stress test only. It omits mixing, settling, return flows, and the relationship between
surface velocity and exposure near a reef. The source and receptors in the geometry panel are
fictional. The Kodingareng coordinate conflict prevents a corresponding real source-to-receptor
calculation.
Decision 1 · Keep a transport check in siting
Ask whether a plausible current direction puts a more distant receptor on-path. Use a model or
measurements with defensible nearshore support before translating this question into setbacks or
operating conditions.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
16 / 25

#### PDF page 17

BEFORE THE PLUME REACHES THE REEF
RESULTS · AMUR BAY
Use a river-influenced coast to
challenge attribution
The Russian case lets the team check its reasoning in a setting with independently
documented high river flow.
Figure 10. Sentinel-2 true-color views, Amur Bay, August–September 2023. Fixed western and eastern water squares are
used for relative optical context. Modified Copernicus data. [8, 9, 22, 47]
On 6 September, Sentinel-2 and Landsat 9 acquired scenes about 18 minutes apart. The western zone
was brighter in the red band in both missions, with west-minus-east differences of +0.0552 and
+0.0646 under their respective processing. A qualifying 12 July Landsat scene, before the August flood
episodes, showed a stronger difference of +0.0961.
The flood and optical contrast are separate observations. A later visible contrast in the bay can be
consistent with a river-influenced event while leaving source apportionment and concentration open.
The case offers a useful alternative explanation to carry into the Indonesian analysis. [22] [23] [24] [27]
Decision 5 · Compare plausible explanations across coasts
Record rainfall or river conditions alongside the image and inspect how the signal sits relative to land,
river outlets and reference water. Apply the same evidence questions to suspected dredging events.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
17 / 25

Links embedded on this page

- https://www.meteorf.gov.ru/press/news/34448/
- https://dfo.meteorf.gov.ru/news/889/
- https://doi.org/10.3390/jmse10121798
- https://doi.org/10.1016/j.rse.2019.03.010

#### PDF page 18

BEFORE THE PLUME REACHES THE REEF
RESULTS · RUSSIA COMPARISON
Keep strict screens and partial
observations visible
Changing the coverage rule can change which story the image series appears to tell.
Figure 11. Independent optical mission acquisition, qualifying local views, official/literature flood windows, and retrospective
rainfall context. [8–10, 22, 23, 29, 47]
From July through September 2023, two of 18 Sentinel-2 dates and four of 12 Landsat dates passed the
≥90% water rule in both zones. The union was five qualifying dates across 28 unique acquisition dates.
Four acquisition dates fell within the three published flood intervals and none passed both zones.
The seasonal Sentinel-2 catalog audit found 156 July–September dates in 2019–26 after restoring 18
historic 2022 dates from a legacy archive. The local raster result refers to 2023. On 29 August 2023, the
three precipitation products showed 38.5–138.5 mm across their differing regional proxies,
independently supporting a wet period and leaving optical source attribution open.
Decision 7 · Use a partial observation for the part it covers
Preserve the individual zone result when a whole-area rule fails. A reviewer can use that view to
narrow a check and state which area still needs independent evidence.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
18 / 25

#### PDF page 19

BEFORE THE PLUME REACHES THE REEF
RESULTS · EVIDENCE REPLAYS
Give a lead the next step it can
support
The same information can justify checking a place while leaving a pause, violation or impact
determination unresolved.
Case and information
What becomes possible
What remains open
Tunda: official stop, cargo
observation, no exact-day
date in the scoped sensor
inventory
Record the inspection and assign
follow-up to a documented location and
responsible authority.
When and where the reported
extraction occurred. Whether the
closest image would have reached
the reviewer.
Kodingareng: project-period
record, fisher reports and
conflicting printed incident
location
Record the fishing concern and prioritize
reconciling geography and work records.
Which mapped path leads from a
verified borrow area to a specified
fishing ground.
Amur Bay: high-water
documentation, rainfall
corroboration and later
optical contrast
Use the contrast to examine freshwater
influence and quality-screen limits.
Whether a specific visible feature
can be quantitatively apportioned
among sources.
A graduated decision sequence
An observation can create a time-stamped lead. A corroborated lead can focus field verification. A
temporary operating change belongs with the actor who has authority and a documented basis. A
formal finding requires the applicable evidence and procedure. A public satellite image can contribute
at several points in this sequence.
The current Indonesian framework describes indirect supervision, field examination and supporting
records. The historical cases were interpreted under their dated context. As a design comparison,
Western Australia’s dredging guidance illustrates staged monitoring and management responses. The
report does not import a numerical trigger or jurisdiction. [7] [39] [45]
Decision 3 · Specify an action before specifying a threshold
Decide which action a signal can support. Associate the rule with a known owner and required
corroboration, including what would restore confidence or allow normal work to resume.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
19 / 25

Links embedded on this page

- https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765
- https://peraturan.bpk.go.id/Details/249417/pp-no-26-tahun-2023
- https://www.epa.wa.gov.au/sites/default/files/Policies_and_Guidance/Technical_guidance_EIA_of_Marine_Dredging_Proposals.pdf

#### PDF page 20

BEFORE THE PLUME REACHES THE REEF
DISCUSSION · PREVENTION CHOICES
Make prevention a set of choices
people can own
The four upstream decisions define what coastal teams can change before exposure or
escalation.
Decision
Act on this
Evidence gap that matters
1 · Siting
Verify the source geography, locate the
receptor, and screen connectivity before
comparing distance setbacks.
Verified work polygon and local
transport evidence. The Kodingareng
coordinate disagreement changes
what can be mapped.
2 · Work timing
Compare work periods under relevant
environmental conditions and identify where
scheduling might alter receptor connectivity.
Time-stamped activities and locally
informative current, tide and wind
measures. Regional direction changes
alone cannot set a schedule.
3 · Precaution
Use a graduated lead, verification and
authorization sequence. Specify what
prompts review, who can act, and when to
reassess.
Case-level evidence of authority,
standards and a practical route to act
while the event is still relevant.
4 · Exposure priority
Design records around a receptor-specific
history of intensity, duration and recurrence.
Pair satellite opportunities with another
observation path where needed.
A defensible field or local optical
measure and an ecological baseline.
Percentages that describe image
coverage cannot establish sediment
dose.
These choices can reinforce one another. A verified polygon makes transport screening possible. An
operating clock makes timing analysis possible. A clear escalation process allows a reviewer to respond
to uncertainty. Receptor-specific observations let someone later distinguish visibility from exposure.
Start with the prerequisite that multiple decisions share
A trustworthy record of place, time, receptor and decision authority improves siting, scheduling,
precaution and exposure assessment together.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
20 / 25

#### PDF page 21

BEFORE THE PLUME REACHES THE REEF
DISCUSSION · VERIFICATION AND RECURRENCE
Make the next case easier to
resolve
Four further decisions concern the quality of the record and the action it supports.
Decision
Act on this
Evidence gap that matters
5 · Source control
Keep activity, river inputs, weather, seabed
and optical effects as explicit explanations.
Prioritize a control action where the
mechanism is consequential and supported.
Spatially and temporally matched
evidence tying an input to transport
and receptor exposure.
6 · Baseline records
Save work and observation clocks, the
footprint, baseline conditions and decision
owner before the work period. Version
important data layers.
Earlier availability, especially original
product and operator records. Current
catalog metadata can describe a later
reprocessed item.
7 · Field verification
Use the exact area of concern and closest
defensible observations. Bring another
source to the specific blind spot.
Local visibility or alternative
observation availability, plus the
practical inspection route.
8 · Recurrence
Track regulatory disposition, work changes
and ecological or livelihood conditions on
separate timelines.
Comparable follow-up measures. A
decision in one track can leave the
other two unresolved.
Tunda and Kodingareng show different documented action histories. The Tunda account gives a dated
stop and investigation step. The Kodingareng record contains a later follow-up disposition reported to
Parliament. A judge can use each to understand the relevant decision without inferring an outcome
the source does not measure. [5] [6] [14]
Preserve what would change the next decision
The useful archive connects the concern, affected place, contemporaneous evidence, decision,
reason, and any subsequent measurement or work change.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
21 / 25

Links embedded on this page

- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf

#### PDF page 22

BEFORE THE PLUME REACHES THE REEF
DISCUSSION · TECHNOLOGY AND BILATERAL FIT
Share the method. Calibrate the
coast.
Indonesia can use the approach on its own. A Russian counterpart gives the method an
independent transfer test.
Portable across sites
Requires local input
Explicit definitions for activity, observation,
product availability and decision time.
The clock at which an agency, operator or community
actually receives reliable information.
Footprint-level visibility and comparable scene
checks, including the area of interest and
independent observations.
Current habitat boundaries, documented fishing
grounds and site-specific viewing limitations.
A consistent way to separate a lead, source
corroboration and authorization.
Operating rules, relevant authority, tolerance, tidal
effects and baseline measurements.
The proposed bilateral research role is to agree on a comparable observation protocol and
independently rerun the source-ambiguity checks at a river-influenced coast. The governments’
maritime research and training agenda offers a relevant policy channel. The Pacific Oceanological
Institute has relevant ocean-color and remote sensing expertise. The Amur Bay analysis in this study
uses public evidence and does not depend on a partnership agreement. [22] [24] [25] [26]
Existing tools already cover useful parts of the problem. UNEP Marine Sand Watch contributes
vessel-linked dredging context. Radar contributes independent surface observations. NASA and
Copernicus archives supply repeatable imagery and modeled context. Value for a coastal reviewer
comes from joining those inputs to the choice and the receptor. [2] [28] [30] [31] [32]
Bilateral research success
An independent analyst starts from the same data definitions, reproduces the observation result, and
explains a meaningful difference in interpretation or decision at their coast.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
22 / 25

Links embedded on this page

- https://www.meteorf.gov.ru/press/news/34448/
- https://doi.org/10.3390/jmse10121798
- https://kemenkoinfra.go.id/detailpost/menko-ahy-pimpin-konsultasi-bilateral-indonesia-rusia-sepakat-perkuat-kerja-sama-perkapalan-dan-konektivitas-maritim
- https://www.poi.dvo.ru/en/structure/lab94
- https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans
- https://stac.dataspace.copernicus.eu/v1/
- https://hls.gsfc.nasa.gov/data-access-and-tools/
- https://www.esa.int/media/sentinel-1-tracking-maritime-traffic
- https://globalfishingwatch.org/our-apis/

#### PDF page 23

BEFORE THE PLUME REACHES THE REEF
CONCLUSION
Give reviewers evidence while
they can still act
Coastal sediment management improves when monitoring is designed around the action it
serves.
The strongest direct evidence concerns observation and reconstruction: where coverage was available,
what a second satellite added, how receptor footprints changed which scenes passed, and which
records existed around the time of a known event. That is enough to demand a better evidence design
before marine work begins.
The prevention questions point to decisions worth comparing. Siting depends on verified locations and
plausible transport toward receptors. Scheduling depends on the operating clock and reliable local
conditions. Escalation depends on what a signal establishes and who has authority. Follow-up depends
on preserving what happened and which outcomes were actually measured.
Important uncertainties are specific. The public sources yield no verified extraction footprint for the
Tunda stop and no reconciled point for the reported Kodingareng incident. The regional grids leave
reef-scale transport unresolved. Optical signals and stakeholder reports matter as evidence with their
own scope, including where an alternative explanation survives.
The proposition for LAUTARA
Make prevention decisions at the scale of the place people want to protect. Set the observation and
record requirements before work starts. When a lead arrives, connect it to a proportionate action and
keep a traceable record for the next event.
The article leaves the eventual product or intervention open. The eight decisions can now be compared from the same
evidence base.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
23 / 25

#### PDF page 24

BEFORE THE PLUME REACHES THE REEF
REPRODUCIBILITY AND REFERENCES
Follow the claims back to the
data
The companion bundle contains source URLs, inventories, figure data, scripts, and a map
from headline claims to files.
Start with README.md and CLAIMS.md in the companion archive. The figure crosswalk lists the input
and script for each exhibit. The included data tables preserve date, site, and sensor or product where
applicable. The source manifest records the core endpoints and key exclusions. Scripts use published
APIs or cached data as noted in the bundle.
Study bounds: use the exact geographic definitions and dates in the inventories. Some archive
products are reprocessed. Historic reef polygons represent mapped footprints. Raster quality flags
describe observation support. The work uses no proprietary extraction log, confidential field record, or
validated reef-concentration time series.
Core study and observation sources
[1] LAUTARA 2026 guidebook. Sections 3–6, judging criteria
and programme.
[2] UNEP (2023). Marine Sand Watch and global dredging
estimates.
[3] Wahyudi et al. (2023). Tunda reef survey and MIKE 21
modelling.
[4] Erftemeijer et al. (2012). Dredging and sediment effects
on corals.
[5] KKP (29 Oct 2023). Official release on the 27 Oct stop and
inspection.
[6] KKP Loka PSPL Serang (FY2023). Performance report, p.
38.
[7] KKP JDIH. Regulation 5/2025 amending 30/2021, arts. 8,
19 and 28.
[8] Earth Search v1. Cloud-Optimized GeoTIFF catalog,
Element 84.
[9] Copernicus. Sentinel-2 scene classifications and
processing.
[10] USGS Landsat Collection 2. QA_PIXEL quality bands.
[11] Boskalis. Makassar New Port project sheet, phases
1B–1C.
[12] Kurniawati et al. (2021). Kodingareng fieldwork and
policy evidence.
[13] Indonesian Police (13 Sep 2020). Report about the Taka
Copong incident.
[14] DPR Commission IV (2024). South Sulawesi visit report,
pp. 5–6.
[15] UNEP-WCMC. Global Distribution of Coral Reefs v4.1,
polygon layer.
[16] Natural Earth. 1:10m land polygons (public domain).
[17] NASA POWER. Daily point API and temporal reference.
[18] NASA GES DISC. GPM IMERG Final, V07 product
metadata.
[19] Open-Meteo. Historical weather API and reanalysis
product definitions.
[20] Open-Meteo. Marine API and model/geographic
definitions.
[21] Copernicus Marine. GLORYS12 global physical
reanalysis.
[22] Roshydromet (21 Aug 2023). Satellite monitoring of
Primorye floods.
[23] Far Eastern Hydromet. Primorye 2023 hydrological
season review.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
24 / 25

Links embedded on this page

- https://chatgpt.com/library?file_id=libfile_a0f1f94bc47c81919f0b91c5fbf16337
- https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans
- https://doi.org/10.2478/cjf-2023-0009
- https://doi.org/10.1016/j.marpolbul.2012.05.008
- https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765
- https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands
- https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- https://doi.org/10.30872/mulrev.v6i2.621
- https://tribratanews.polri.go.id/blog/hukum-4/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716
- https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf
- https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/
- https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary
- https://open-meteo.com/en/docs/historical-weather-api
- https://open-meteo.com/en/docs/marine-weather-api
- https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- https://www.meteorf.gov.ru/press/news/34448/
- https://dfo.meteorf.gov.ru/news/889/

#### PDF page 25

BEFORE THE PLUME REACHES THE REEF
REFERENCES
Connect the literature to the
decision
Clickable references identify the records, methodological sources, and policy context used in
the study.
[24] Razdolnaya/Suifen estuary study. River-influenced
coastal environment.
[25] Kemenko Infra (June 2026). Indonesia–Russia maritime
working groups.
[26] Pacific Oceanological Institute FEB RAS. Satellite
oceanography lab.
[27] Vanhellemont (2019). Atmospheric correction for aquatic
remote sensing.
[28] Copernicus Data Space. Official STAC catalog.
[29] Microsoft Planetary Computer. Public Landsat C2 L2
catalog.
[30] NASA HLS. Collection descriptions and download access.
[31] ESA. Sentinel-1 radar for maritime context.
[32] Global Fishing Watch. Maritime data API capabilities and
access.
[33] Banten Bay regional sediment transport study, Tanjung
Pontang.
[34] WALHI coalition (Nov 2023). Reported observations near
Pulau Pari.
[35] BIG (2024). Annual report and product specifications for
BATNAS.
[36] GEBCO. Global gridded bathymetry and source identifier
grids.
[37] Kurniawati et al. PDF. Kodingareng respondent and
study details.
[38] Prior LAUTARA coastal sediment diagnostic and
embedded scene tables.
[39] Indonesia PP 26/2023. Management of sedimentation
products in the sea.
[40] Allen Coral Atlas. Methods, thematic layers and
constraints.
[41] NOAA CPC. Global unified gauge-based precipitation
archive.
[42] Copernicus Marine. Global ocean physics analysis and
SMOC currents.
[43] WALHI and Greenpeace. Spermonde investigation and
community record.
[44] Peer-reviewed Banten Bay TSS and reported extraction
pairs, table 2.
[45] Western Australia EPA. Technical guidance for marine
dredging proposals, §§3.6.3–3.6.4.
[46] UCSB Climate Hazards Center. CHIRPS rainfall methods
and data.
[47] Lisina et al. (2025). Razdolnaya flood episode
chronology, pp. 73–81.
[48] NASA POWER. IMERG source, grid scale, and production
latency.
Data reuse
Use the product IDs and provenance in the companion archive to obtain source assets directly.
Cached CSVs are documented derivatives. Original public imagery and habitat sources retain provider
attribution and access terms.
LAUTARA 2026 / COASTAL SEDIMENT STUDY
25 / 25

Links embedded on this page

- https://doi.org/10.3390/jmse10121798
- https://kemenkoinfra.go.id/detailpost/menko-ahy-pimpin-konsultasi-bilateral-indonesia-rusia-sepakat-perkuat-kerja-sama-perkapalan-dan-konektivitas-maritim
- https://www.poi.dvo.ru/en/structure/lab94
- https://doi.org/10.1016/j.rse.2019.03.010
- https://stac.dataspace.copernicus.eu/v1/
- https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- https://hls.gsfc.nasa.gov/data-access-and-tools/
- https://www.esa.int/media/sentinel-1-tracking-maritime-traffic
- https://globalfishingwatch.org/our-apis/
- https://doi.org/10.15578/jkn.v1i2.6614
- https://www.walhi.or.id/kapal-vox-maxima-kembali-beroperasi-di-perairan-pulau-tunda-dan-teluk-jakarta-koalisi-ngo-desak-penegakan-hukum-lingkungan
- https://www.big.go.id/uploads/content/produk/Laporan%20Tahunan%20BIG/LaporanTahunanBIGTahun2024.pdf
- https://www.gebco.net/data-products/gridded-bathymetry-data
- https://e-journal.fh.unmul.ac.id/mulrev/article/download/621/225/2203
- https://chatgpt.com/library?file_id=libfile_61a9ace26b688191a4897fac7ce72ee4
- https://peraturan.bpk.go.id/Details/249417/pp-no-26-tahun-2023
- https://www.allencoralatlas.org/methods/
- https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html
- https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description
- https://www.greenpeace.org/static/planet4-indonesia-stateless/2021/03/17185db9-gp-spermonde-report-v8.pdf
- https://doi.org/10.15578/segara.v14i1.7149
- https://www.epa.wa.gov.au/sites/default/files/Policies_and_Guidance/Technical_guidance_EIA_of_Marine_Dredging_Proposals.pdf
- https://www.chc.ucsb.edu/data/chirps
- https://tigdvo.ru/assets/files/publications/Pacific_Geography_journal/2025_1/73-81.pdf
- https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/#imerg-integrated-multi-satellite-retrievals-for-gpm



### 03 Before the Plume Journal Article


Extracted text by printed PDF file page. Use the original for tables, reading order, diagrams and page geometry.

#### PDF page 1

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

#### PDF page 2

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

#### PDF page 3

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

#### PDF page 4

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

#### PDF page 5

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

#### PDF page 6

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

#### PDF page 7

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

#### PDF page 8

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

#### PDF page 9

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

#### PDF page 10

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

#### PDF page 11

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



## Appendix C · Claim and figure crosswalks, decision memo, sources


### CLAIMS.md

# Claim-to-data crosswalk

| Claim | Files and calculations | Interpretation |
|---|---|---|
| Matched mission gains at Tunda and Kodingareng | `optical/multisensor_summary.csv`, all_matched, 90, clear_pct. Union = Sentinel + Landsat minus common pass. Compare inclusive no-pass calendar runs. | Optical opportunities after a deliberately defined QA threshold. |
| 1 of 72 higher-rain site-days in Nov–Dec 2025 passed either mission | `rain/rainfall_multisensor_summary.csv`; 10 mm threshold. `rain/rainfall_multisensor_days.csv` where available. | Sampled proxy associations, not proof of clouds or extraction activity. Distinguish no acquired view from acquired but failed screen. |
| Rain products disagree around Tunda inspection | `rain/rainfall_events.csv`, Tunda event, preceding one-day and preceding three-day amounts. Independent `review/rain_observation_decomposition.csv` treats observation opportunity by site-month. | Regionally averaged precipitation proxies with varied grid and date conventions. Neither measures Tunda runoff. |
| Receptor geometry changes screening | `root/tunda_habitat_scl.csv`, `root/kodingareng_habitat_scl.csv`, and `root/habitat_summary.json`. Prior 26 Oct Tunda result documented in the prior diagnostic, reference 38. | Archived outline and data-readable work sample. Raster cell fractions do not establish modern reef extent. |
| Scoped Tunda mission observations and product lineage | `review/tunda_event_sensor_clocks.csv`, `review/tunda_product_lineage.csv`, and archived catalog responses. | Current item publications and available version metadata cannot establish observer receipt. |
| Kodingareng location conflict | `events/coordinate_conflict.json`, `events/event_register.csv`, official police report. | A comparison of public descriptions from the island anchor. Neither the printed coordinate nor narrative distance was adopted as borrow-area geometry. |
| Kodingareng currents differ by depth and model cell | `marine/marine_summary.json`, `marine/marine_baseline_summary.json`, and underlying normalized tables. | Daily regional model estimates. The current direction thresholds are comparative, not permit or reef-exposure rules. |
| Amur multi-mission optical confirmation and pre-flood counterexample | `amur/amur_daily_2023.csv`, `amur/amur_landsat_daily_2023.csv`, `amur/verify_amur.py`. | Same-sign west–east red band contrasts are optical evidence. Later and earlier differences do not quantify sediment or attribute a source. |
| Hypothetical straight-line distance at different speeds | `root/travel_scenarios.csv`, speed times hours times 3.6. | An analytic sensitivity calculation with no mixing, settling, route boundaries or source-specific inference. |


### FIGURES.md

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


### events/memo.md

# Public evidence for eight coastal sediment decisions

## Findings that change the design

**Make a location verify itself before using it to decide where work can proceed.** The September 2020 police account prints S05°09.470′ E119°14.789′ while describing an operation/conflict location as 11 mil southwest of Kodingareng. Direct conversion gives −5.15783333°, 119.24648333°. From the study island anchor −5.14905°, 119.26473°, this is **2.244 km (1.212 nautical miles)** WSW, initial bearing **244.2°**. WALHI independently places the relevant fishing area approximately 9 mil away, with wording and definitions that may differ. The distance discrepancy excludes the printed point from transport or zoning joins. It may be an error, a point describing a different event, or a different operational reference. No correction was assumed. A false geometry would propagate into every downstream exposure estimate. Sources: [Polri, 13 Sep 2020](https://tribratanews.polri.go.id/article/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716), [WALHI/Greenpeace p. 23 ff](https://www.greenpeace.org/static/planet4-indonesia-stateless/2021/03/17185db9-gp-spermonde-report-v8.pdf), [island anchor](https://mapcarta.com/16118912). Calculation: `create_manifest.py` and `coordinate_conflict.json`.

**Keep source, cargo, receptor, and authority separate through verification.** KKP’s 29 October 2023 release publicly describes the 27 October HIU 06 stop of VOX MAXIMA, ~24,000 m³ of sand observed onboard, and the launch of further investigation. It described the reported Tunda source and Tanjung Priok destination as suspected and reports a preliminary permit finding. There is no exact public extraction clock or footprint in the release. The 2023 LPSPL performance report records an inter-agency monitoring/evidence-gathering action on 27 October. These are two official records about the same broad intervention, not two independently detected extraction events. The prior incident audit identifies Sentinel-2 observations on 26 October and 31 October and no exact-day Earth Search acquisition. Airborne, proprietary and other satellite imagery are outside this specific statement. 18–22 November reports concern sighting a loaded vessel near **Pulau Pari**, a different observed location. The coalition’s Tunda-origin inference remains distinct. Sources: [KKP release](https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html), [LPSPL 2023 report, p. 38](https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf), [WALHI coalition, dated 22 November](https://www.walhi.or.id/kapal-vox-maxima-kembali-beroperasi-di-perairan-pulau-tunda-dan-teluk-jakarta-koalisi-ngo-desak-penegakan-hukum-lingkungan).

**Measure what changes after an intervention through separate regulatory and recovery tracks.** In South Sulawesi, the 2024 DPR Commission IV field-visit report relays that Satwas SDKP examined three sand-mining and two reclamation businesses, heard fishers and found no violations in that specific regulatory follow-up, with conflict-reduction steps also described. It does not specify threshold measurements, exact polygons, a catch counterfactual or recovery evidence. The same record therefore supports a completed administrative follow-up without resolving ecological or social exposure. A 2023 WALHI statement discusses alleged price-setting irregularities involving two firms, a different inquiry with distinct questions. For Tunda, local media quoted the district revenue official in March 2024 on a combined approx. IDR 4.5 billion tax payment from two firms for January–February; the tax reporting does not dispose of the KKP vessel inquiry or establish restoration. The public materials reviewed did not resolve the final outcome of the Tunda vessel case. Sources: [DPR report, May 6–10 visit, printed pp. 5–6](https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf), [WALHI statement about separate pricing investigation](https://walhisulsel.or.id/4037-pernyataan-pers-atas-dugaan-praktik-penyimpangan-penetapan-harga-jual-hasil-pertambangan-pasir-laut-tahun-2020-di-perairan-galesong-kabupaten-takalar/), [Banten Raya interview, March 26](https://www.bantenraya.com/daerah/12277769/perusahaan-tambang-pasir-di-kabupaten-serang-cicil-pembayaran-pajak-rp45-miliar).

## Eight decisions and the strongest defensible next direction

| Decision | Evidence and owner context | Design direction |
|---|---|---|
| 1. Site the work | The 2020 Sulsel zoning vintage was Perda 2/2019. Perda 3/2022 effective 22 April 2022 repeals it. Banten’s provincial plan is Perda 1/2023. The reviewed case material does not supply authenticated event-specific extraction or permit polygons. | Date every geometry, ask planning/permit owner to confirm the polygon and activity period, then pair it with reef/fishing use or transport. Keep the named quarry without polygon status visible. |
| 2. Set the work window | The Kodingareng police account reports a departure at 06:00 WITA and arrival at 07:00 WITA on the disputed September chronology; Boskalis reports February–October deployment and ~11m m³ transported within Makassar New Port 1B–1C. Tunda event hour is absent. | Ask operators to log actual activity start/finish separately from vessel movement and agency action. Use environmental fields at their real time scale. Work-hour comparisons have much tighter input requirements than seasonal conditions. |
| 3. Change/stop operations | Tunda official action is observed, but what officials knew at the original intake time is not public. Western Australia EPA’s technical guidance describes escalating the response from early pressure indicators through biological-response indicators. | Build levels that link an observed condition to a named authority and feasible actions, and specify what additional evidence unlocks the next level. Compare investigation/monitoring, pressure reduction and stronger action. Do not import a numerical threshold or another jurisdiction’s authority. |
| 4. Prioritize exposure | Wahyudi et al. 2023 combines July–Dec 2021 coral survey and hydrodynamic scenarios; Fatmawati et al. 2025 reports four stations sampled Nov 2021–Jan 2022 (mean live coral 16.92%). Across studies, sampling design, strata and dates differ. Coral sediment review distinguishes intensity, duration and frequency. | Design for a receptor and an exposure history, including what remained unobserved. Use only comparable field data to estimate a change in coral state. |
| 5. Decide what to control | Tunda vessel/cargo account is not a confirmed source footprint. The regional Tanjung Pontang paper provides a physically plausible Banten Bay river-sediment rival. Banten Bay operator data shows 102 mg/L TSS on a day one recorded operator reported zero production. | Keep runoff and other sources on the map. Require a coincident work trace, hydrodynamic plausibility and contrasted reference context before assigning the source. |
| 6. Record before work | Candidate dates have missing or nonpublic source geometry, extracted-material time, sensor availability, inspection intake, local baseline and case closure records. Tunda October reporting had event and publication on different dates. | Require a timestamped activity footprint, conditions/baseline and reference sites plus a record of who had evidence and when. A real-time prevention rule can only use information available at the decision time. |
| 7. Verify in a blind spot | KKP records show patrol and community information can be available when an Earth Search Sentinel-2 acquisition is absent; Kodingareng sources describe differing named grounds and conflicting figures. | Review target-specific coverage and use verified coordinates and dated independent leads to narrow a field check. Geographic ambiguity is a reason to verify the location first. |
| 8. Prevent a recurrence | Tunda’s public record leaves final case outcome and recovery unresolved. DPR records a narrower institutional outcome for Kodingareng. Neither source closes the exposure record at receptor level. | Require incident-to-action, reopening conditions and receptor trend as separately tracked fields. Add an explicit follow-up deadline with named actor. |

### External benchmark, Indonesian regime and research references

- [Western Australia EPA marine dredging technical guidance, §3.6.3–3.6.4](https://www.epa.wa.gov.au/sites/default/files/Policies_and_Guidance/Technical_guidance_EIA_of_Marine_Dredging_Proposals.pdf): reference monitoring outside predicted influence where possible, risk-tiered monitoring and management linked to both pressure and biological response, and site-specific thresholds. Good template for designing graduated actions, not a local legal standard.
- [Great Barrier Reef dredge material management report, Trigger Values and Management Responses](https://elibrary.gbrmpa.gov.au/jspui/bitstream/11017/2852/1/gbr-dredge-material-management.pdf): discuss indicator distributions, background and ecological responses. Do not transfer operational thresholds without site validation.
- Current Indonesian context: [KKP spatial planning Permen 28/2021](https://jdih.kkp.go.id/Homedev/DetailPeraturan/954), [spatial oversight amendment Permen 5/2025 to 30/2021](https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765), [sea sediment PP 26/2023](https://peraturan.bpk.go.id/Details/249417/pp-no-26-tahun-2023), [implementation amendment Permen 3/2025](https://jdih.kkp.go.id/Homedev/DetailPeraturan/6767), [Sulsel Perda 2/2019 historical as applicable to the 2020 timeline](https://peraturan.bpk.go.id/Details/162528/perda-prov-sulawesi-selatan-no-2-tahun-2019), [Sulsel Perda 3/2022 current zoning vintage](https://peraturan.bpk.go.id/Details/218611/perda-prov-sulawesi-selatan-no-3-tahun-2022), [Banten Perda 1/2023 2023–2043 RTRW](https://jdih.bantenprov.go.id/produkhukum/peraturan-daerah-provinsi/peraturan-daerah-provinsi-banten-nomor-1-tahun-2023-tentang-rencana-tata-ruang-wilayah-provinsi-banten-tahun-2023-2043). Current law answers contemporary workflow questions and is not evidence of requirements in 2020.
- [Wahyudi et al., 2023 Tunda reef survey and modeled sediment](https://doi.org/10.2478/cjf-2023-0009), [Fatmawati et al. Tunda reef transects](https://doi.org/10.22373/kenanga.v5i2.8470), [Tunda habitat by station/depth Mujiyanto et al.](https://ejournal.undip.ac.id/index.php/ijms/article/view/28649), [Tanjung Pontang sediment pathways](https://doi.org/10.15578/jkn.v1i2.6614), [Ernas et al. Banten Bay four-date operator records, table 2](https://doi.org/10.15578/segara.v14i1.7149), [Erftemeijer et al. corals pressure/response review](https://doi.org/10.1016/j.marpolbul.2012.05.008), [Kurniawati, Nur & Thiodores 2021 Kodingareng field legal study](https://doi.org/10.30872/mulrev.v6i2.621). Fisher interviews comprise a documented impact hypothesis and a case of affected resource use. Catch or income causality would need measured effort, catch and a credible comparison design.
- Kodingareng operational scope and geography: [Boskalis project factsheet](https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf) attributes ~11m m³ transported to phase 1B–1C during vessel deployment and does not provide a borrow polygon. [Coalition retrospective](https://www.walhi.or.id/uploads/buku/Policy%20Paper%20-%20Jaring%20Nusa%20KTI%20%281%29.pdf) dates reported end to 26 October. Treat it as an advocate-sourced day and the contractor’s February–October range as the independently corroborated month-scale timing.
- [Parenden, Jompa & Rani 2021, field observations around Spermonde](https://doi.org/10.1088/1755-1315/921/1/012060) measured turbidity and underwater photo transects at three islands, with laboratory turbidity of 0.32 NTU for **Kodingareng Keke**. Keke is a different island from the Lompo case anchor. It supports the regional reef receptor rationale but cannot characterize 2020 conditions at Copong Lompo, calibrate the satellite proxy at Lompo, or validate an effect of extraction. Treat this as an example of why receptor names and coordinates must be confirmed.


### README.md

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

- [1] LAUTARA 2026 guidebook. Sections 3–6, judging criteria and programme. — https://chatgpt.com/library?file_id=libfile_a0f1f94bc47c81919f0b91c5fbf16337
- [2] UNEP (2023). Marine Sand Watch and global dredging estimates. — https://www.unep.org/en/news-and-stories/press-release/unep-marine-sand-watch-reveals-massive-extraction-worlds-oceans
- [3] Wahyudi et al. (2023). Tunda reef survey and MIKE 21 modelling. — https://doi.org/10.2478/cjf-2023-0009
- [4] Erftemeijer et al. (2012). Dredging and sediment effects on corals. — https://doi.org/10.1016/j.marpolbul.2012.05.008
- [5] KKP (29 Oct 2023). Official release on the 27 Oct stop and inspection. — https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html
- [6] KKP Loka PSPL Serang (FY2023). Performance report, p. 38. — https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf
- [7] KKP JDIH. Regulation 5/2025 amending 30/2021, arts. 8, 19 and 28. — https://jdih.kkp.go.id/Homedev/DetailPeraturan/6765
- [8] Earth Search v1. Cloud-Optimized GeoTIFF catalog, Element 84. — https://element84.com/geospatial/introducing-earth-search-v1-new-datasets-now-available/
- [9] Copernicus. Sentinel-2 scene classifications and processing. — https://s2.pages.eopf.copernicus.eu/msi/s2msi/1.3.0/sum/payload-l2a.html
- [10] USGS Landsat Collection 2. QA_PIXEL quality bands. — https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands
- [11] Boskalis. Makassar New Port project sheet, phases 1B–1C. — https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf
- [12] Kurniawati et al. (2021). Kodingareng fieldwork and policy evidence. — https://doi.org/10.30872/mulrev.v6i2.621
- [13] Indonesian Police (13 Sep 2020). Report about the Taka Copong incident. — https://tribratanews.polri.go.id/blog/hukum-4/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716
- [14] DPR Commission IV (2024). South Sulawesi visit report, pp. 5–6. — https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf
- [15] UNEP-WCMC. Global Distribution of Coral Reefs v4.1, polygon layer. — https://data-gis.unep-wcmc.org/server/rest/services/HabitatsAndBiotopes/Global_Distribution_of_Coral_Reefs/FeatureServer/1
- [16] Natural Earth. 1:10m land polygons (public domain). — https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/
- [17] NASA POWER. Daily point API and temporal reference. — https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- [18] NASA GES DISC. GPM IMERG Final, V07 product metadata. — https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary
- [19] Open-Meteo. Historical weather API and reanalysis product definitions. — https://open-meteo.com/en/docs/historical-weather-api
- [20] Open-Meteo. Marine API and model/geographic definitions. — https://open-meteo.com/en/docs/marine-weather-api
- [21] Copernicus Marine. GLORYS12 global physical reanalysis. — https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030/description
- [22] Roshydromet (21 Aug 2023). Satellite monitoring of Primorye floods. — https://www.meteorf.gov.ru/press/news/34448/
- [23] Far Eastern Hydromet. Primorye 2023 hydrological season review. — https://dfo.meteorf.gov.ru/news/889/
- [24] Razdolnaya/Suifen estuary study. River-influenced coastal environment. — https://doi.org/10.3390/jmse10121798
- [25] Kemenko Infra (June 2026). Indonesia–Russia maritime working groups. — https://kemenkoinfra.go.id/detailpost/menko-ahy-pimpin-konsultasi-bilateral-indonesia-rusia-sepakat-perkuat-kerja-sama-perkapalan-dan-konektivitas-maritim
- [26] Pacific Oceanological Institute FEB RAS. Satellite oceanography lab. — https://www.poi.dvo.ru/en/structure/lab94
- [27] Vanhellemont (2019). Atmospheric correction for aquatic remote sensing. — https://doi.org/10.1016/j.rse.2019.03.010
- [28] Copernicus Data Space. Official STAC catalog. — https://stac.dataspace.copernicus.eu/v1/
- [29] Microsoft Planetary Computer. Public Landsat C2 L2 catalog. — https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- [30] NASA HLS. Collection descriptions and download access. — https://hls.gsfc.nasa.gov/data-access-and-tools/
- [31] ESA. Sentinel-1 radar for maritime context. — https://www.esa.int/media/sentinel-1-tracking-maritime-traffic
- [32] Global Fishing Watch. Maritime data API capabilities and access. — https://globalfishingwatch.org/our-apis/
- [33] Banten Bay regional sediment transport study, Tanjung Pontang. — https://doi.org/10.15578/jkn.v1i2.6614
- [34] WALHI coalition (Nov 2023). Reported observations near Pulau Pari. — https://www.walhi.or.id/kapal-vox-maxima-kembali-beroperasi-di-perairan-pulau-tunda-dan-teluk-jakarta-koalisi-ngo-desak-penegakan-hukum-lingkungan
- [35] BIG (2024). Annual report and product specifications for BATNAS. — https://www.big.go.id/uploads/content/produk/Laporan%20Tahunan%20BIG/LaporanTahunanBIGTahun2024.pdf
- [36] GEBCO. Global gridded bathymetry and source identifier grids. — https://www.gebco.net/data-products/gridded-bathymetry-data
- [37] Kurniawati et al. PDF. Kodingareng respondent and study details. — https://e-journal.fh.unmul.ac.id/mulrev/article/download/621/225/2203
- [38] Prior LAUTARA coastal sediment diagnostic and embedded scene tables. — https://chatgpt.com/library?file_id=libfile_61a9ace26b688191a4897fac7ce72ee4
- [39] Indonesia PP 26/2023. Management of sedimentation products in the sea. — https://peraturan.bpk.go.id/Details/249417/pp-no-26-tahun-2023
- [40] Allen Coral Atlas. Methods, thematic layers and constraints. — https://www.allencoralatlas.org/methods/
- [41] NOAA CPC. Global unified gauge-based precipitation archive. — https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html
- [42] Copernicus Marine. Global ocean physics analysis and SMOC currents. — https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description
- [43] WALHI and Greenpeace. Spermonde investigation and community record. — https://www.greenpeace.org/static/planet4-indonesia-stateless/2021/03/17185db9-gp-spermonde-report-v8.pdf
- [44] Peer-reviewed Banten Bay TSS and reported extraction pairs, table 2. — https://doi.org/10.15578/segara.v14i1.7149
- [45] Western Australia EPA. Technical guidance for marine dredging proposals, §§3.6.3–3.6.4. — https://www.epa.wa.gov.au/sites/default/files/Policies_and_Guidance/Technical_guidance_EIA_of_Marine_Dredging_Proposals.pdf
- [46] UCSB Climate Hazards Center. CHIRPS rainfall methods and data. — https://www.chc.ucsb.edu/data/chirps
- [47] Lisina et al. (2025). Razdolnaya flood episode chronology, pp. 73–81. — https://tigdvo.ru/assets/files/publications/Pacific_Geography_journal/2025_1/73-81.pdf
- [48] NASA POWER. IMERG source, grid scale, and production latency. — https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/#imerg-integrated-multi-satellite-retrievals-for-gpm

## Appendix D · Verified Kodingareng example, machine-readable

```json
{
  "source": "marine/glorys_daily.csv",
  "days": 274,
  "start": "2020-02-01",
  "end": "2020-10-31",
  "eastward_component_sign_surface_then_deeper": {
    "E / E": 133,
    "E / W": 6,
    "W / W": 34,
    "W / E": 96,
    "W / zero": 4,
    "zero / E": 1
  },
  "example": {
    "0.494": {
      "site": "Kodingareng",
      "utc_day": "2020-04-16",
      "depth_m": "0.49402499198913574",
      "lat": "-5.166666507720947",
      "lon": "119.25",
      "distance_km_from_island": "2.5494338809682118",
      "east_m_s": "-0.09216589853167534",
      "north_m_s": "-0.009765923023223877",
      "speed_m_s": "0.09268185423612654",
      "towards_deg": "263.9514933389994",
      "time_index": "9967",
      "depth_index": "49",
      "lat_index": "898",
      "lon_index": "3591"
    },
    "9.573": {
      "site": "Kodingareng",
      "utc_day": "2020-04-16",
      "depth_m": "9.572997093200684",
      "lat": "-5.166666507720947",
      "lon": "119.25",
      "distance_km_from_island": "2.5494338809682118",
      "east_m_s": "0.05249183624982834",
      "north_m_s": "0.05249183624982834",
      "speed_m_s": "0.07423466673837491",
      "towards_deg": "45.0",
      "time_index": "9967",
      "depth_index": "42",
      "lat_index": "898",
      "lon_index": "3591"
    }
  }
}

```

## Appendix E · Retrieval map for the original files

# LAUTARA • The Ocean Has Floors

**One-minute orientation.** A coastal officer planning a sand-extraction baseline can compare the same place at two modeled depths, then ask a crew to measure the water where the evidence matters. The deliverable is a versioned survey brief with the station, depths, instruments and rationale. The selected design is an internal government tool with a CityRT-inspired overhead map. The static mockups show how the proposed app would work.

| If you have… | Open first | Next |
|---|---|---|
| One upload slot | LAUTARA_Master_AI_Context.md | Contains the curated handoff, all four team document texts and selected evidence appendices. |
| Five minutes | 01_Product/The_Ocean_Has_Floors.pdf, pp. 2–5 | See the operator screen, a same-place depth change, the A–B section and the field brief. |
| A team discussion | 02_Research/03_Before_the_Plume_Journal_Article.pdf | Use the 25-page report for extended methods, limits and the full eight decisions. |
| A build task | 05_Reproducibility/Depth_case_verified.json and the team brief pp. 6–7 | Use the actual two vectors. Open 04_Visuals/Visual_guide.md to distinguish current screens from concept art. |
| A scientific challenge | 05_Reproducibility/Reading_copy/CLAIMS.md | Open the exact CSV and reproduce it with the appropriate script. The full extracted tree and unchanged original analysis ZIP are included. |
| A competition submission | 03_Competition_and_methods/LAUTARA_2026_Official_Guide.pdf | The opening video has its own question, date, duration and language. |
| A revision question | 07_Design_history/User_direction_record.md | Two reconstructed earlier drafts and working materials show what the user changed. |
| A provenance or file question | 08_Index/Original_file_map.csv, File_inventory.csv and SHA256SUMS.txt | Research source links, document page text, and PDF-embedded datasets are retained. |

**In plain English for a new AI:** Read LAUTARA_Master_AI_Context.md. Use the current product brief for design and the archived tables for numbers. Continue from the user’s latest instruction. Keep the full eight decisions in the research and the government survey workflow in the product. Label modeled results, field observations, assumptions and artistic illustrations wherever the distinction changes a decision.

**Scope.** Includes recovered files from this maritime project, plus clearly marked derived access copies and draft reconstructions. The decision record summarizes the available conversation. No verbatim export of every prior assistant turn or council exchange was available. External repositories, benchmarks, provider catalogs and original imagery/model archives remain linked. The packaged regional extracts, inputs, results and scripts allow selected offline checks. Earlier draft PDFs were reconstructed using surviving project sources; the current brief is the actual delivered PDF. Only binary-identical duplicate report and art aliases were collapsed. This is a team handoff; source materials retain their original authorship and terms.

