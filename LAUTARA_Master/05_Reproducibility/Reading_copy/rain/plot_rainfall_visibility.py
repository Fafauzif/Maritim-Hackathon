#!/usr/bin/env python3
"""Visualize the date-joined exploratory rainfall/optical observability check."""
import csv
from pathlib import Path
from matplotlib import pyplot as plt

BASE=Path(__file__).resolve().parent
rows=[r for r in csv.DictReader((BASE/'rainfall_optical_summary.csv').open())
      if r['proxy_nominal_wet_threshold_mm']=='10' and r['rain_group']=='above_or_equal']
order=[('Tunda','Jun'),('Tunda','Nov'),('Kodingareng','Jun'),('Kodingareng','Nov')]
rows=[next(r for r in rows if r['site']==s and r['period'].startswith(m)) for s,m in order]
fig,ax=plt.subplots(figsize=(11,4.05),layout='constrained')
fig.patch.set_facecolor('white')
labels=['Catalog acquisition missing','Acquisition below local 90%','Qualifying view']
cols=['catalog_acquisition_missing_days','acquisition_below_threshold_days','qualifying_acquisition_days']
colors=['#b5c8d1','#b96042','#276963']
used=[0]*len(rows)
for lab,col,color in zip(labels,cols,colors):
    nums=[int(r[col]) for r in rows]
    ax.barh(range(len(rows)),nums,left=used,color=color,label=lab,height=.63,zorder=3)
    for y,(x,n) in enumerate(zip(used,nums)):
        if n>0 and n>=3:
            ax.text(x+n/2,y,f'{n}',ha='center',va='center',color='#233744' if color==colors[0] else 'white',fontsize=12,fontweight='bold')
        elif n>0:
            ax.plot([x+n,x+n+.8],[y,y],color='#233744',linewidth=.7,zorder=4)
            ax.text(x+n+1,y,f'{n}',ha='left',va='center',color='#233744',fontsize=10,fontweight='bold')
    used=[a+b for a,b in zip(used,nums)]
ax.set_yticks(range(len(rows)),[f"{r['site']} · {r['period']}" for r in rows])
ax.invert_yaxis()
ax.set_xlabel('Rain-proxy days with ≥10 mm in the selected UTC calendar windows')
ax.set_xlim(0,42)
ax.set_xticks(range(0,41,5))
ax.set_axisbelow(True)
ax.grid(axis='x',color='#e4ebec')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.tick_params(axis='both',length=0,labelsize=10)
ax.legend(loc='upper left',bbox_to_anchor=(0,-.18),ncol=3,frameon=False,fontsize=10)
fig.savefig(BASE/'rainfall_visibility.png',dpi=220)
fig.savefig(BASE/'rainfall_visibility.svg')
