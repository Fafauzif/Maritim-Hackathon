#!/usr/bin/env python3
"""Build transparent daily rainfall histories, ranks, summaries and publication panels."""
from __future__ import annotations
import csv
from datetime import date,datetime,timedelta,timezone
import json
import math
from pathlib import Path
from statistics import fmean
import sys
from acquire import BASE,RAW,PROXIES

START=date(2019,1,1)
END=date(2025,12,31)
DATES=[START+timedelta(days=i) for i in range((END-START).days+1)]
EVENTS=[
    ('Tunda','2023-10-27','KKP inspection date'),
    ('Tunda','2023-11-18','Start of reported 18–22 Nov window'),
    ('Kodingareng','2020-02-13','Reported project start, WALHI'),
    ('Kodingareng','2020-10-26','Reported project end, WALHI'),
    ('Amur','2023-08-10','First documented flood window starts'),
    ('Amur','2023-08-11','Within first documented flood window'),
    ('Amur','2023-08-24','Second documented flood window starts'),
    ('Amur','2023-08-30','Third documented flood window starts'),
    ('Amur','2023-09-01','Third documented flood window ends'),
]
SOURCES=['imerg_mean','cpc','chirps']

def read_rows(site):
    meta=PROXIES[site]
    template={d:{'site':site,'date_utc':d.isoformat()} for d in DATES}
    seen_signatures=set()
    sample_ids=[]
    for i in range(len(meta['points'])):
        p=RAW/f'{site}_IMERG_p{i}.json'
        if not p.exists():
            continue
        j=json.loads(p.read_text())
        amounts=j['properties']['parameter']['IMERG_PRECTOT']
        signature=tuple(sorted(amounts.items()))
        if signature not in seen_signatures:
            sample_ids.append(i)
            seen_signatures.add(signature)
        for day,value in amounts.items():
            d=datetime.strptime(day,'%Y%m%d').date()
            if 0 <= value:
                template[d][f'imerg_p{i}']=float(value)
    for p in sorted(RAW.glob(f'{site}_CPC_*.csv')):
        for row in csv.DictReader(p.open()):
            d=date.fromisoformat(row['time'][:10])
            if not (START<=d<=END):
                continue
            try:
                precip=float(row['precip[unit="mm"]'])
            except Exception:
                continue
            if math.isfinite(precip) and precip>=0:
                template[d]['cpc']=precip
    p=RAW/f'{site}_CHIRPS.json'
    if p.exists():
        for row in json.loads(p.read_text())['data']:
            # The provider's example textual dates are ambiguous. Unix time, not text, is authoritative.
            d=datetime.fromtimestamp(float(row['epochTime']), timezone.utc).date()
            vals=[v for k,v in row.get('value',{}).items() if k=='avg' and isinstance(v,(int,float)) and v>=0]
            if d in template and vals:
                template[d]['chirps']=vals[0]
    for d in DATES:
        row=template[d]
        values=[row[f'imerg_p{i}'] for i in sample_ids if f'imerg_p{i}' in row]
        row['imerg_n']=len(values)
        if values:
            row['imerg_mean']=fmean(values)
            row['imerg_min']=min(values)
            row['imerg_max']=max(values)
        for source in SOURCES:
            for window in (1,3,7):
                previous=[template.get(d-timedelta(days=i),{}).get(source) for i in range(1,window+1)]
                if all(v is not None for v in previous):
                    row[f'{source}_prev{window}']=sum(previous)
    return template

def empirical(values, x):
    if x is None or not values:
        return None
    return 100*(sum(v<x for v in values)+0.5*sum(v==x for v in values))/len(values)

def ranks(series):
    # Use calendar month of comparison end/decision date and leave out target event year.
    output=[]
    for site,when,label in EVENTS:
        d=date.fromisoformat(when)
        rr=series[site]
        row={'site':site,'event_date_utc_analysis_anchor':when,'event':label}
        row.update({f'imerg_point{i}_prev1':rr[d-timedelta(days=1)].get(f'imerg_p{i}') for i in range(6)})
        for k in SOURCES:
            for v in (k,k+'_prev1',k+'_prev3',k+'_prev7'):
                obs=rr[d].get(v)
                comparator=[x[v] for dd,x in rr.items() if dd.month==d.month and dd.year!=d.year and x.get(v) is not None]
                row[v]=obs
                row[v+'_percentile']=empirical(comparator,obs)
                row[v+'_comparison_n']=len(comparator)
        output.append(row)
    return output

def out_csv(name,arr):
    keys=list(dict.fromkeys(k for row in arr for k in row))
    with (BASE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,keys)
        w.writeheader()
        for r in arr:
            w.writerow({k:round(v,5) if isinstance(v,float) else v for k,v in r.items()})

def plot(series):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    import matplotlib.dates as mdates
    import numpy as np

    specs=[
        ('Tunda','2023-10-17','2023-11-24',[('2023-10-27','27 Oct inspection')],'Tunda / Banten mainland proxy'),
        ('Kodingareng','2020-01-31','2020-10-31',[('2020-02-13','13 Feb'),('2020-10-26','26 Oct')],'Kodingareng / Makassar mainland proxy'),
        ('Amur','2023-08-01','2023-09-07',[('2023-08-11','11 Aug'),('2023-08-24','24 Aug'),('2023-08-30','30 Aug')],'Amur Bay / Lower Razdolnaya corridor proxy'),
    ]
    fig,axs=plt.subplots(3,1,figsize=(12,8.0),layout='constrained')
    fig.patch.set_facecolor('white')
    colors={'imerg_mean':'#0d6370','chirps':'#b6512e','cpc':'#654f78'}
    for ax,(site,start,end,markers,title) in zip(axs,specs):
        ss=series[site]; a=date.fromisoformat(start); b=date.fromisoformat(end)
        days=[x for x in DATES if a<=x<=b]
        def vector(v):
            return [np.nan if ss[d].get(v) is None else ss[d][v] for d in days]
        ax.fill_between(days,vector('imerg_min'),vector('imerg_max'),color='#a3cbc8',alpha=.55,
                        lw=0,label='IMERG point range',zorder=1)
        for k,l in [('chirps','CHIRPS box mean'),('cpc','CPC gauge-analysis cell')]:
            v=vector(k)
            if np.isfinite(v).any():
                ax.plot(days,v,color=colors[k],lw=1,alpha=.83,label=l,zorder=2)
        ax.plot(days,vector('imerg_mean'),color=colors['imerg_mean'],lw=1.65,
                label='IMERG unique-cell mean',zorder=3)
        ymax=max(ax.get_ylim()[1],1)
        for ms,ml in markers:
            dt=date.fromisoformat(ms)
            ax.axvline(dt,color='#213645',lw=1,linestyle='--',alpha=.73,zorder=0)
            ax.text(dt,ymax*1.04,ml,ha='center',va='bottom',fontsize=9,color='#213645')
        if site=='Amur':
            for x,y in [('2023-08-10','2023-08-13'),('2023-08-24','2023-08-27'),('2023-08-30','2023-09-01')]:
                ax.axvspan(date.fromisoformat(x),date.fromisoformat(y),color='#c6d8e2',alpha=.33,zorder=-1)
        ax.set_title(title,loc='left',fontweight=600,color='#19343b',pad=10)
        ax.set_ylabel('mm/day')
        ax.set_ylim(0,ymax*1.21)
        ax.set_xlim(days[0]-timedelta(days=1),days[-1]+timedelta(days=1))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=4,maxticks=9))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        ax.spines[['top','right','left']].set_visible(False)
        ax.spines['bottom'].set_color('#bdc4c8')
        ax.grid(axis='y',color='#e4e9e9',zorder=-2)
        ax.tick_params(axis='both',length=0,labelsize=9)
    handles,labels=axs[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='outside lower center',ncol=4,frameon=False,fontsize=10)
    fig.savefig(BASE/'rainfall_comparison.png',dpi=220)
    fig.savefig(BASE/'rainfall_comparison.svg')

def main():
    series={site:read_rows(site) for site in PROXIES}
    for site,ss in series.items():
        summary={k:sum(r.get(k) is not None for r in ss.values()) for k in SOURCES}
        sample_count=max(r['imerg_n'] for r in ss.values())
        print(site,summary,'unique IMERG series',sample_count,'complete IMERG days',sum(r['imerg_n']==sample_count for r in ss.values()))
    rr=ranks(series)
    out_csv('rainfall_events.csv',rr)
    out_csv('rainfall_daily.csv',[row for ss in series.values() for row in ss.values()])
    plot(series)
    for r in rr:
        s=[(k,round(r[k],1),round(r[k+'_percentile'],1) if r[k+'_percentile'] is not None else None) for k in r if k in {'imerg_mean','imerg_mean_prev1','imerg_mean_prev3','imerg_mean_prev7','chirps','chirps_prev1','chirps_prev3','cpc','cpc_prev1','cpc_prev3'} and r[k] is not None]
        print(r['site'],r['event_date_utc_analysis_anchor'],*s)

if __name__=='__main__': main()
