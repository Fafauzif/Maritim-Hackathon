#!/usr/bin/env python3
"""Draw the fully audited Tunda/Kodingareng discovery and held-out period figure."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

HERE=Path(__file__).resolve().parent
from summarize import B_COL,S_COL,L_COL,DARK,GRID,date_sets,row_summary

l=pd.read_csv(HERE/"landsat_coverage.csv",parse_dates=["date"])
s=pd.read_csv(HERE/"sentinel_pilot_input.csv",parse_dates=["date"])
d=pd.concat([s,l],ignore_index=True); d["date"]=pd.to_datetime(d.date)
summary=row_summary(d)
wmain=["jun_sep_2025","nov_feb_2025_26"]
summary=summary[summary.window.isin(wmain)]
summary.to_csv(HERE/"matched_pilot_window_summary.csv",index=False)
fig,axes=plt.subplots(2,2,figsize=(9.7,4),sharex="col",layout="constrained")
for i,site in enumerate(["Tunda","Kodingareng Lompo"]):
    for j,window in enumerate(wmain):
        row=summary[(summary.site==site)&(summary.window==window)&(summary.metric=="clear_pct") & (summary.threshold==90)].iloc[0]
        q=d[(d.site==site)&d.date.between(row.start,row.end)]
        sens=date_sets(q[q.sensor=="Sentinel-2"],90)
        land=date_sets(q[q.sensor=="Landsat 8/9"],90)
        ax=axes[i,j]
        ax.set(xlim=(pd.Timestamp(row.start),pd.Timestamp(row.end)),ylim=(-0.2,2.9), yticks=[0.45,1.55],yticklabels=['Landsat-only','Sentinel-2'])
        ax.scatter(sorted(sens),[1.55]*len(sens),s=68,marker="|",color=S_COL,lw=1.6)
        ax.scatter(sorted(land-sens),[.45]*len(land-sens),s=68,marker="|",color=L_COL,lw=1.6)
        ax.tick_params(axis="y",length=0); ax.grid(axis="x",color=GRID)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax.text(.017,.93,f"{site} • {len(sens)} + {len(land-sens)} added",transform=ax.transAxes,fontweight="semibold")
        if i==0:
            ax.set_title(["Jun–Sep 2025","Nov 2025–Feb 2026"][j],loc="left",fontweight="bold")
fig.supxlabel("UTC acquisition date • at least 90% of the 1.5–3.0 km ring passed local quality flags",fontsize=9)
out=HERE.parent/"figures"
out.mkdir(exist_ok=True)
fig.savefig(out/"optical_pilot_windows.png",dpi=230)
