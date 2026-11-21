"""Reproduce case-window summaries and figures from bundled marine/weather tables."""
from pathlib import Path
import json
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

ROOT=Path(__file__).resolve().parent
COL={'navy':'#14344a','teal':'#007d77','red':'#ba4d38','grey':'#486374','gold':'#c08535','grid':'#dde5e8'}
OUT=ROOT
plt.rcParams.update({'axes.spines.right':False,'axes.spines.top':False,'font.family':'DejaVu Sans','font.size':9,
                      'axes.labelcolor':COL['grey'],'xtick.color':COL['grey'],'ytick.color':COL['grey'],'text.color':COL['navy']})

window={'Tunda':('2023-10-12','2023-11-11'),'Kodingareng':('2020-02-01','2020-10-31')}
ref={'Tunda':(-5.81151,106.27811),'Kodingareng':(-5.14905,119.26473)}

def angular_delta(a,b):
    return ((a-b+180)%360)-180

def vector_bearing(u,v):
    return np.rad2deg(np.arctan2(u,v)) % 360

def avg_bearing(direction,speed=None):
    ar=np.deg2rad(direction)
    if speed is None: speed=np.ones(len(ar))
    return vector_bearing(np.mean(speed*np.sin(ar)),np.mean(speed*np.cos(ar)))

def axes_fmt(ax,units):
    ax.grid(axis='y',color=COL['grid'],lw=.7)
    ax.set_ylabel(units,color=COL['grey'],fontsize=9)

def title(ax,string):
    ax.set_title(string,loc='left',fontweight='bold',pad=12,fontsize=11)

def pnum(a):
    return [round(float(x),3) for x in a]

env=pd.read_csv(ROOT/'environment_hourly.csv')
nas=pd.read_csv(ROOT/'nasa_power_daily.csv')
g=pd.read_csv(ROOT/'glorys_daily.csv')
local=dict()
utc=dict()
gs=dict()
summary={}
for s,(begin,end) in window.items():
    a=env[env.site==s]
    a=a.copy()
    a['lcalendar']=pd.to_datetime(a['local_timestamp']).dt.tz_localize(None)
    local[s]=a[(a.local_day>=begin)&(a.local_day<=end)]
    utc[s]=a[(a.utc_day>=begin)&(a.utc_day<=end)]
    s0=g[g.site==s]
    nn=s0.distance_km_from_island.min()
    z=s0.depth_m.min()
    gs[s]=s0[(s0.depth_m==z)&(s0.distance_km_from_island==nn)].copy()
    gs[s]['d']=pd.to_datetime(gs[s].utc_day)
    era=utc[s].query("model=='era5'").groupby('utc_day').precipitation.sum().rename('era5_mm')
    merra=nas[nas.site==s].set_index('utc_day').rain_mm.rename('merra2_mm')
    pair=pd.concat([era,merra],axis=1).dropna()
    pair.to_csv(OUT/f'{s.lower()}_rain_pair_utc.csv')
    gs[s]['month']=gs[s].d.dt.strftime('%Y-%m')
    q=gs[s]
    m=q.groupby('month').agg(days=('speed_m_s','size'),mean_east_m_s=('east_m_s','mean'),mean_north_m_s=('north_m_s','mean'),median_speed_m_s=('speed_m_s','median'),eastward_days=('east_m_s',lambda v:int((v>0).sum())))
    m['mean_vector_towards_deg']=vector_bearing(m.mean_east_m_s,m.mean_north_m_s)
    m.to_csv(OUT/f'{s.lower()}_glorys_monthly.csv')
    summary[s]={'num_utc_days':len(pair),'rain':{'era5_total_mm':round(era.sum(),2),'merra2_total_mm':round(merra.sum(),2),'spearman':round(float(pair.corr(method='spearman').iloc[0,1]),3),
               'era5_days_ge_5mm':int((era>=5).sum()),'merra2_days_ge_5mm':int((merra>=5).sum()),
               'both_days_ge_5mm':int(((era>=5)&(merra>=5)).sum())},
              'glorys_nearest':{'coord':pnum([q.lat.iloc[0],q.lon.iloc[0]]),'distance_km':round(nn,2),'depth_m':round(z,3),'days':len(q),
              'eastward_days':int((q.east_m_s>0).sum()),'median_speed_m_s':round(q.speed_m_s.median(),3),'months':m.round(3).to_dict(orient='index')}}

t=local['Tunda']
e=t.loc[t.local_day=='2023-10-27']
event={m:{v:pnum(x[v].agg(['min','median','max'])) for v in ['wave_height','wave_direction','wave_period','ocean_current_velocity','ocean_current_direction','wind_speed_10m','precipitation'] if x[v].notna().any()}
       for m,x in e.groupby('model')}
for dataset in ['meteofrance_wave','era5_ocean']:
    current=e[e.model==dataset]
    wave=current.wave_period.dropna()
    event[dataset]['wavelength_deep_water_approx_m_min_median_max']=pnum((9.80665*wave**2/(2*np.pi)).agg(['min','median','max']))
    event[dataset]['circular_mean_wave_from_deg']=round(float(avg_bearing(current.wave_direction.dropna())),1)
    src=t[t.model==dataset].groupby('local_day').wave_height.max()
    event[dataset]['event_day_max_wave_height_rank_from_highest']=int(src.rank(method='min',ascending=False).loc['2023-10-27'])
    event[dataset]['max_daily_significant_wave_height_range_m']=pnum([src.min(),src.max()])
d=e.pivot(index='local_timestamp',columns='model',values='wave_direction')
event['abs_era5_mfwam_wave_from_direction_difference_deg_min_median_max']=pnum(abs(angular_delta(d['era5_ocean'],d['meteofrance_wave'])).agg(['min','median','max']))
current=e[e.model=='best_match']
event['best_match']['current_vector_mean_towards_deg']=round(float(avg_bearing(current.ocean_current_direction,current.ocean_current_velocity)),1)
event['best_match']['westward_hours']=int((np.sin(np.deg2rad(current.ocean_current_direction))<0).sum())
event['best_match']['eastward_hours']=24-event['best_match']['westward_hours']
nn=gs['Tunda']
q=nn[nn.utc_day=='2023-10-27']
event['glorys_2023_10_27_utc_daily_nearest']={x:round(float(q[x].iloc[0]),3) for x in ('speed_m_s','towards_deg','east_m_s','north_m_s')}
sub=g[(g.site=='Tunda')&(g.utc_day=='2023-10-27')&(g.depth_m==nn.depth_m.iloc[0])]
event['glorys_spatial']={'event_9cells_speed_min_median_max':pnum(sub.speed_m_s.agg(['min','median','max'])),'event_9cells_towards_bearings':pnum(sub.towards_deg), 'event_9cells_distances_km':pnum(sub.distance_km_from_island)}
for site, sx in g.groupby('site'):
    sensitivity={}
    for depth,sx0 in sx.groupby('depth_m'):
        q=sx0.pivot(index='utc_day',columns=['lat','lon'],values='east_m_s')
        assert q.shape[1]==9 and q.notnull().all().all()
        east_counts=(q>0).sum(axis=1)
        sensitivity[f'{depth:.3f}_m']={'mixed_direction_days':int(((east_counts>0)&(east_counts<9)).sum()),
                                   'utc_days':len(q),'eastward_days_range_across_cells':[int((q>0).sum().min()),int((q>0).sum().max())]}
    summary[site]['glorys_3x3_sensitivity']=sensitivity
    summary[site]['glorys_depth_nearest']={f'{d:.3f}_m':{'eastward_days':int((sq.east_m_s>0).sum()), 'n':len(sq)}
            for d,sq in sx[sx.distance_km_from_island==sx.distance_km_from_island.min()].groupby('depth_m')}
summary['Tunda_event_local_day']=event
summary['Tunda_event_rain']={'local_daily_sum':round(float(e[e.model=='era5'].precipitation.sum()),3),
                            'preceding_3_local_days':pnum(t[(t.model=='era5')&(t.local_day>='2023-10-24')&(t.local_day<='2023-10-26')].groupby('local_day').precipitation.sum()),'era5_wind_max_rank':int(t[t.model=='era5'].groupby('local_day').wind_speed_10m.max().rank(ascending=False,method='min').loc['2023-10-27'])}
summary['assumptions']={'rain_big_day_threshold_mm':5,'glorys_daily_surface_layer_m':float(g.depth_m.min()),'wave_length':'deep-water heuristic gT^2/(2π), missing point depth makes nearshore wavelength unresolved'}
(ROOT/'marine_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))

# Article graphics, daily timestamps local for waves and standardized UTC for rain pairs.
fig,axs=plt.subplots(3,1,figsize=(8.15,6.3),sharex=True)
td=pd.read_csv(OUT/'tunda_rain_pair_utc.csv',parse_dates=['utc_day'])
wx=pd.to_datetime('2023-10-27')
axs[0].bar(td.utc_day-pd.Timedelta(hours=4),td.era5_mm,width=.33,color=COL['teal'],label='ERA5')
axs[0].bar(td.utc_day+pd.Timedelta(hours=4),td.merra2_mm,width=.33,color=COL['gold'],label='NASA POWER/MERRA‑2')
title(axs[0],'A  |  Regional rain estimates'); axes_fmt(axs[0],'mm / UTC day')
axs[0].legend(loc='upper left',ncol=2,frameon=False,fontsize=8)
for model,color,label in [('era5_ocean',COL['gold'],'ERA5–Ocean (~55 km)'),('meteofrance_wave',COL['teal'],'MFWAM (~9 km)')]:
    a=t[t.model==model].groupby('local_day').wave_height.agg(['median','max'])
    rd=pd.to_datetime(a.index)
    axs[1].plot(rd,a['max'],color=color,lw=1.7,label=label)
    axs[1].fill_between(rd,a['median'],a['max'],color=color,alpha=.14)
title(axs[1],'B  |  Daily peak significant wave height'); axes_fmt(axs[1],'m / WIB day')
axs[1].legend(loc='upper left',ncol=2,frameon=False,fontsize=8)
cur=t[t.model=='best_match'].copy()
cur['east_ms']=cur.ocean_current_velocity*np.sin(np.deg2rad(cur.ocean_current_direction))
axs[2].plot(cur.lcalendar,cur.east_ms,color=COL['grey'],alpha=.36,lw=.7,label='SMOC hourly, WIB')
axs[2].plot(pd.to_datetime(cur.local_day.unique())+pd.Timedelta(hours=12),
            cur.groupby('local_day').east_ms.mean(),color=COL['teal'],lw=1.8,label='SMOC daily mean, WIB')
axs[2].plot(nn.d,nn.east_m_s,color=COL['gold'],lw=1.4,label='GLORYS daily, UTC')
axs[2].axhline(0,lw=.8,color=COL['grey'])
title(axs[2],'C  |  East–west surface current component'); axes_fmt(axs[2],'m / s')
axs[2].legend(loc='upper left',ncol=3,frameon=False,fontsize=8)
for ax in axs:
    ax.axvline(wx,ls='--',lw=1.1,color=COL['red'])
    ax.set_xlim(pd.Timestamp('2023-10-11'),pd.Timestamp('2023-11-12'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
fig.suptitle('Tunda  |  The inspection day in its regional context',x=.09,y=.993,ha='left',fontweight='bold',fontsize=15)
fig.text(.09,.949,'12 Oct–11 Nov 2023  ·  dashed line: recorded 27 Oct inspection date',fontsize=8.5,color=COL['grey'])
fig.tight_layout(rect=(0,.01,1,.929),h_pad=1.4)
fig.savefig(OUT/'tunda_conditions.png',dpi=230,facecolor='white')
plt.close(fig)

fig,axs=plt.subplots(3,1,figsize=(8.15,6.3),sharex=True)
kd=pd.read_csv(OUT/'kodingareng_rain_pair_utc.csv',parse_dates=['utc_day'])
for k,c,l in [('era5_mm',COL['teal'],'ERA5'),('merra2_mm',COL['gold'],'NASA POWER/MERRA‑2')]:
    axs[0].plot(kd.utc_day,kd[k].rolling(7,min_periods=7).sum(),color=c,lw=1.5,label=l)
title(axs[0],'A  |  Regional rainfall over preceding 7 UTC days'); axes_fmt(axs[0],'mm')
axs[0].legend(loc='upper left',ncol=2,frameon=False,fontsize=8)
a=local['Kodingareng'].query("model=='era5_ocean'").groupby('local_day').wave_height.agg(['median','max'])
rd=pd.to_datetime(a.index)
axs[1].fill_between(rd,a['median'],a['max'],color=COL['teal'],alpha=.14)
axs[1].plot(rd,a['max'],color=COL['teal'],lw=1.1)
title(axs[1],'B  |  Daily peak significant wave height, offshore ERA5–Ocean grid'); axes_fmt(axs[1],'m / WITA day')
x=gs['Kodingareng']
axs[2].plot(x.d,x.east_m_s,color=COL['grey'],alpha=.5,lw=.65)
axs[2].plot(x.d,x.east_m_s.rolling(7,min_periods=7).mean(),color=COL['teal'],lw=1.55,label='7-day mean')
axs[2].axhline(0,lw=.8,color=COL['grey'])
title(axs[2],'C  |  East–west daily mean surface current, nearest GLORYS cell'); axes_fmt(axs[2],'m / s')
axs[2].legend(loc='upper left',frameon=False,fontsize=8)
for ax in axs:
    ax.set_xlim(pd.Timestamp('2020-02-01'),pd.Timestamp('2020-11-01'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
fig.suptitle('Kodingareng  |  Marine conditions shifted across the case months',x=.09,y=.993,ha='left',fontweight='bold',fontsize=14)
fig.text(.09,.949,'Feb–Oct 2020  ·  selected case months and gridded conditions  ·  vessel activity is not resolved by day',fontsize=8.5,color=COL['grey'])
fig.tight_layout(rect=(0,.01,1,.929),h_pad=1.4)
fig.savefig(OUT/'kodingareng_conditions.png',dpi=230,facecolor='white')
plt.close(fig)

fig, ax=plt.subplots(figsize=(7.65,4.05))
kd=g[g.site=='Kodingareng'].copy()
kd['month']=kd.utc_day.str[:7]
kd['eastward']=kd.east_m_s>0
m=kd.groupby(['month','depth_m','lat','lon']).eastward.mean().reset_index()
envelope=m.groupby(['month','depth_m']).eastward.agg(['min','median','max']).reset_index()
envelope.to_csv(OUT/'kodingareng_glorys_cell_sensitivity.csv',index=False)
for i,(depth,row) in enumerate(envelope.groupby('depth_m')):
    dates=pd.to_datetime(row.month+'-01')
    color=COL['teal'] if i==0 else COL['gold']
    ax.fill_between(dates,row['min']*100,row['max']*100,color=color,alpha=.19)
    ax.plot(dates,row['median']*100,color=color,marker='o',ms=3.5,label=f'{depth:.2f} m layer • median and 9-cell range')
ax.axhline(50,ls='--',color=COL['grey'],lw=.75)
ax.set_ylim(-2,102)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.legend(loc='lower left',frameon=False,fontsize=8.25,ncol=1)
axes_fmt(ax,'Days with eastward component (%)')
ax.set_title('Kodingareng | Modeled flow shifts with month and depth',x=0,ha='left',pad=20,fontsize=13.2,fontweight='bold')
fig.text(.12,.035,'Daily GLORYS12V1 model samples, 1/12° grid. Eastward component > 0 m/s. No near-reef particle paths.',fontsize=7.8,color=COL['grey'])
fig.tight_layout(rect=(.015,.08,.99,.99))
fig.savefig(OUT/'kodingareng_current_envelope.png',dpi=230,facecolor='white')
plt.close(fig)
