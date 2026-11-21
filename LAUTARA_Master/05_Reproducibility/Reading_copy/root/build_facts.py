"""Extract article metrics from the analysis tables and write the annual inventory plot."""
import csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent.parent
def rows(name):
    with (ROOT/name).open() as f:return list(csv.DictReader(f))

obs=rows('optical/sentinel_longitudinal.csv')
land=rows('optical/landsat_longitudinal.csv')
land_sites={r['site']:len({x['date'] for x in land if x['site']==r['site'] and x['status']=='ok'}) for r in land}
if len({(r['site'],r['date']) for r in obs})!=len(obs):
    raise ValueError('duplicate site-date')
combo=[r for r in rows('optical/multisensor_summary.csv') if r['window']=='all_matched' and r['metric']=='clear_pct' and r['threshold']=='90']
assert len(combo)==2
t,k=combo
assert t['site']=='Tunda' and k['site']=='Kodingareng Lompo'
opt_counts={}
fig,axes=plt.subplots(1,2,figsize=(10.2,3.65),sharey=True,layout='constrained')
years=range(2019,2027)
for name,ax in zip(('Tunda','Kodingareng Lompo'),axes):
    series=[r for r in obs if r['site']==name]
    catalog=[sum(row['date'][:4]==str(yr) for row in series) for yr in years]
    read=[sum(row['date'][:4]==str(yr) and row['status']=='ok' for row in series) for yr in years]
    clear=[sum(row['date'][:4]==str(yr) and row['status']=='ok' and float(row['clear_pct'])>=90 for row in series) for yr in years]
    ax.bar(list(years),catalog,color='#d6e3e3',label='Catalog dates')
    ax.bar(list(years),read,color='#7babaa',label='Readable QA raster')
    ax.bar(list(years),clear,color='#13786f',label='Local screen passes')
    ax.set_title(name,loc='left',weight='bold')
    ax.set_xticks(list(years),[str(i)[2:]+'*' if i==2026 else str(i)[2:] for i in years])
    ax.set_xlabel('Year (2026 through October)')
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    opt_counts[name]={'catalog':sum(catalog),'read':sum(read),'pass':sum(clear)}
axes[0].set_ylabel('Distinct Sentinel-2 dates')
axes[1].legend(loc='lower center',bbox_to_anchor=(.5,-.28),ncol=2,frameon=False,fontsize=8)
fig.savefig(ROOT/'figures/inventory.png',dpi=205,bbox_inches='tight',pad_inches=.12)
plt.close(fig)

def additions(v):
    return (int(v['sentinel_pass']),int(v['landsat_added']),int(v['sentinel_pass'])+int(v['landsat_added']))

habitat_path=ROOT/'root/habitat_summary.json'
hab=json.loads(habitat_path.read_text()) if habitat_path.exists() else {}
habsum=[]
for name,sub in hab.items():
    rd=sum(v['read'] for v in sub.values())
    requested=sum(v['planned'] for v in sub.values())
    reef_only=sum(v['reef_only'] for v in sub.values())
    ring_only=sum(v['ring_only'] for v in sub.values())
    footprints=[v['overlap_median'] for v in sub.values() if v['overlap_median'] is not None]
    if rd and footprints:
        fmt=f'{name} had {rd}/{requested} readable dates in the bounded habitat sample, with {ring_only} annulus-only and {reef_only} reef-only passes. The fixed annulus included {footprints[0]:.1f}% of the mapped reef pixels inside 3 km.'
        habsum.append(fmt)
tunda=[x for x in obs if x['site']=='Tunda' and x['status']=='ok' and x['reef_clear_pct']]
ring_only=sum(float(x['clear_pct'])>=90>float(x['reef_clear_pct']) for x in tunda)
reef_only=sum(float(x['reef_clear_pct'])>=90>float(x['clear_pct']) for x in tunda)
habitat_text=(f'Across Tunda’s {len(tunda)} readable dates, <b>{ring_only+reef_only} decisions differed by footprint</b>: {ring_only} passed only the annulus and {reef_only} passed only the archived reef. The annulus covered 43.4% of mapped reef pixels within the 3 km disc. '+next((t for t in habsum if t.startswith('Kodingareng ')),''))

num=len(obs)
nread=sum(r['status']=='ok' for r in obs)
s1,s2,s3=additions(t)
k1,k2,k3=additions(k)
facts={
'abstract_result':f'The Indonesian Sentinel-2 catalog inventory spans {num:,} site-dates from 2019 through October 2026. Over the complete matched 2025–26 window, Landsat adds {s2} qualifying Tunda dates and {k2} Kodingareng dates. In Nov–Dec 2025 only one of 72 higher-rain site-days cleared the local screen using either sensor. At Amur Bay both missions independently saw the same direction of optical contrast on 6 September 2023, while a qualified pre-flood Landsat scene showed an even stronger contrast.',
'optical_annual_fig':'inventory.png',
'optical_annual_cap':'Figure 2. Annual Indonesian Sentinel-2 inventory, readable rasters and broad local screen passes. Acquisition dates are UTC. Readability and quality are separately encoded. The 2026 window ends on 31 October. [8, 9]',
'optical_annual_text':f'Of <b>{num:,} Sentinel-2 site-dates</b>, {nread:,} had readable QA. The Landsat series adds {len(land)} scene records with readable QA, spanning {land_sites["Tunda"]} unique Tunda dates and {land_sites["Kodingareng Lompo"]} Kodingareng dates. Some Landsat paths overlap on the same date. The one unresolved Sentinel-2 mask remains unknown in the denominator.',
'optical_annual_scope':'Across the series, Tunda passed on 5 of 93 January–February dates and 87 of 156 July–September dates. Kodingareng passed on 13 of 95 and 95 of 155 respectively. Among 939 paired legacy and Collection 1 masks, 17 passed the 90% broad rule in only one product version.',
'optical_combo_fig':'optical_union_timeline.png',
'optical_combo_cap':'Figure 3. Combined scene-screen opportunities, 1 Jan 2025–31 Oct 2026. Accepted dates have at least 90% broad local QA retention over the site annulus.',
'optical_combo_text':f'Adding Landsat raised the qualifying date count at Tunda from <b>{s1} to {s3}</b> and at Kodingareng from <b>{k1} to {k3}</b>. Among 662 candidate dates per site with full follow-up, the share with a qualifying observation on the same day or within seven days rose from {float(t["sentinel_within7_pct"]):.1f}% to {float(t["combined_within7_pct"]):.1f}% at Tunda and {float(k["sentinel_within7_pct"]):.1f}% to {float(k["combined_within7_pct"]):.1f}% at Kodingareng.',
'optical_rain_join':f'The longest calendar run without a qualifying view, including window edges, changed from {t["sentinel_max_unqualified_run_days"]} to {t["combined_max_unqualified_run_days"]} days at Tunda and {k["sentinel_max_unqualified_run_days"]} to {k["combined_max_unqualified_run_days"]} at Kodingareng. The second mission improves routine opportunities while long periods still call for a separate observation route.',
'habitat_text':habitat_text or 'The paired comparison is limited to dates whose archived footprint and QA product could both be read.',
'tunda_rain_fig':'tunda_rain.png',
'tunda_rain_cap':'Figure 6. Regional precipitation proxies around the Tunda inspection. Products use different spatial footprints and daily reporting conventions. [17, 18, 41, 46]',
'tunda_rain_text':'On the UTC date before the inspection anchor, NASA IMERG’s mainland proxy mean was <b>16.1 mm</b> (87th percentile of same-month outside-year reference dates). Its input pixels ranged from 0 to 30.1 mm. CHIRPS estimated 2.0 mm and CPC 0.0 mm for the same labeled date. Across the preceding three days, the IMERG estimate was near its 60th percentile.',
'tunda_weather_text':'A stronger wet-weather comparison is 4 November. All three products indicated at least 24 mm of regional daily rain. The records do not establish whether extraction occurred that day. Inspection time within 27 October is unresolved, and daily proxy values cannot locate offshore sediment sources.',
'koding_rain_fig':'koding_rain.png',
'koding_rain_cap':'Figure 7. Regional daily precipitation during the documented project period. The early reported start and September incident are separate chronology markers. [11, 13, 17, 41, 43, 46]',
'koding_rain_text':'At the reported 13 February start, prior three-day precipitation was 22.6 mm from IMERG, 58.9 mm from CHIRPS and 21.3 mm from CPC. The IMERG result was near the 37th percentile of same-month outside-year conditions. On 5 March, all three products showed 47.6–53.1 mm for the product day.',
'marine_fig':'kodingareng_current_envelope.png',
'marine_cap':'Figure 8. Daily Copernicus GLORYS12 eastward component around Kodingareng, Feb–Oct 2020. Cell-envelope and depth sensitivity are estimates at regional scale. [21]',
'marine_text':'At the Kodingareng reference cell, <b>139 of 274 days</b> had an eastward component at 0.494 m modeled depth versus <b>230 of 274</b> at 9.573 m. Nearby surface cells disagreed on the east–west sign on 92 days. Conversely, all nine Tunda neighborhood cells in the 31-day event window had westward components at both depths. The SMOC hourly surface series was also westward through the Tunda inspection date in WIB. The two Tunda current products are related model evidence.',
'amur_scene_fig':'amur_scene_comparison.png',
'amur_scene_cap':'Figure 10. Sentinel-2 true-color views, Amur Bay, August–September 2023. Fixed western and eastern water squares are used for relative optical context. Modified Copernicus data. [8, 9, 22, 47]',
'amur_scene_text':'On 6 September, Sentinel-2 and Landsat 9 acquired scenes about 18 minutes apart. The western zone was brighter in the red band in both missions, with west-minus-east differences of +0.0552 and +0.0646 under their respective processing. A qualifying 12 July Landsat scene, before the August flood episodes, showed a stronger difference of +0.0961.',
'amur_timeline_fig':'amur_cross_sensor_timeline.png',
'amur_timeline_cap':'Figure 11. Independent optical mission acquisition, qualifying local views, official/literature flood windows, and retrospective rainfall context. [8–10, 22, 23, 29, 47]',
'amur_timeline_text':'From July through September 2023, two of 18 Sentinel-2 dates and four of 12 Landsat dates passed the ≥90% water rule in both zones. The union was five qualifying dates across 28 unique acquisition dates. Four acquisitions fell within the three published flood intervals and none passed both zones.',
'amur_archive_text':'The seasonal Sentinel-2 catalog audit found 156 July–September dates in 2019–26 after restoring 18 historic 2022 dates from a legacy archive. The local raster result refers to 2023. On 29 August 2023, the three precipitation products showed 38.5–138.5 mm across their differing regional proxies, independently supporting a wet period and leaving optical source attribution open.',
}
(ROOT/'root/facts.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2))
print(json.dumps({'archive':opt_counts,'habitat_text':habitat_text,'gains':[additions(t),additions(k)]}))
