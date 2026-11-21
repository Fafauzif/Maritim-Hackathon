"""Summarize seasonal GLORYS current directions by month, depth and site (2019–2025)."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

P=Path(__file__).resolve().parent
source=P/'glorys_daily_baseline.csv'
d=pd.read_csv(source if source.exists() else source.with_suffix('.csv.gz'))
d['year']=d.utc_day.str[:4].astype(int)
d['month']=d.utc_day.str[5:7].astype(int)
d['eastward']=d.east_m_s>0
d['cal_day']=pd.to_datetime(d.utc_day)
d['eastward_non_neutral']=d.east_m_s>0.025
d['westward_non_neutral']=d.east_m_s< -0.025
s=d.groupby(['site','year','month','depth_m','lat','lon'],as_index=False).agg(
    n=('east_m_s','size'),eastward_days=('eastward','sum'),eastward_days_non_neutral=('eastward_non_neutral','sum'),
    westward_days_non_neutral=('westward_non_neutral','sum'),distance_km=('distance_km_from_island','first'),
    meaneast=('east_m_s','mean'),meannorth=('north_m_s','mean'))
s['eastward_frac']=s.eastward_days/s.n
s['eastward_frac_non_neutral']=s.eastward_days_non_neutral/(s.eastward_days_non_neutral+s.westward_days_non_neutral)
s.to_csv(P/'glorys_month_cell_baseline.csv',index=False)
stat={}
f,ax=plt.subplots(2,2,figsize=(8,5.3),sharex=True,sharey=True)
col={'teal':'#007d77','gold':'#c08535','navy':'#14344a','light':'#dde5e8'}
for j,site in enumerate(['Tunda','Kodingareng']):
    case_year=2023 if site=='Tunda' else 2020
    block=s[s.site==site]
    nearest=block[block.distance_km==block.distance_km.min()]
    for i,(dep,subset) in enumerate(nearest.groupby('depth_m')):
        panel=ax[j,i]
        ref=subset[subset.year!=case_year]
        monthly=ref.groupby('month').eastward_frac.agg(['min','median','max'])
        panel.fill_between(monthly.index,monthly['min']*100,monthly['max']*100,color=col['teal'],alpha=.22,label='Six other years, min–max')
        panel.plot(monthly.index,monthly['median']*100,color=col['teal'],lw=1.7,label='Six other years, median')
        cc=subset[subset.year==case_year]
        panel.plot(cc.month,cc.eastward_frac*100,ls='--',lw=1.2,color=col['gold'],marker='o',ms=4,label='Case-year pattern')
        panel.axhline(50,color='#777777',lw=.55,ls=':')
        panel.set_title(f'{site} · {dep:.2f} m depth',fontsize=10.2,loc='left',fontweight='bold')
        for z in ['right','top']: panel.spines[z].set_visible(False)
        panel.set_xticks([1,3,5,7,9,11],labels=['Jan','Mar','May','Jul','Sep','Nov'])
        panel.set_xlim(1,12)
        panel.set_ylim(-2,102)
        panel.grid(axis='y',color=col['light'],alpha=.75,lw=.6)
        panel.set_yticks([0,50,100])
        if i==0: panel.set_ylabel('Eastward days (%)',fontsize=9)
        k=f'{site}_{dep:.3f}m'
        stat[k]={'case_year':case_year,'case_year_monthly':{str(m):round(float(v),3) for m,v in zip(cc.month,cc.eastward_frac)},
                 'other_years_at_nearest':monthly.round(3).to_dict(orient='index'),
                 'case_year_monthly_non_neutral':{str(m):round(float(v),3) for m,v in zip(cc.month,cc.eastward_frac_non_neutral)}}
f.legend(*ax[0,0].get_legend_handles_labels(),loc='lower center',ncol=3,frameon=False,fontsize=8,
         bbox_to_anchor=(.5,.013))
f.suptitle('Regional currents vary with season and depth',x=.08,ha='left',fontweight='bold',fontsize=14,color=col['navy'])
f.tight_layout(rect=(.02,.08,1,.92))
f.savefig(P/'marine_current_seasonal.png',dpi=230,facecolor='white')
plt.close(f)
(P/'marine_baseline_summary.json').write_text(json.dumps(stat,indent=2))
print('input',len(d),'derived',len(s))
for k,z in stat.items():
    print(k,z['case_year_monthly'])
    print('baseline median', {m:a['median'] for m,a in z['other_years_at_nearest'].items()})
