#!/usr/bin/env python3
"""Summarize the extracted quality masks by site, sensor, date and threshold."""
import argparse
import calendar
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DEFAULT_FIGURES = ROOT.parent / "figures"
SITES = ["Tunda","Kodingareng Lompo"]
S_COL = "#147f87"
L_COL = "#ca751e"
B_COL = "#173967"
DARK = "#233d4e"
GRID = "#dae5e9"
CUTOFFS = [80, 90, 95]
START = "2025-01-01"
END = "2026-10-31"
WINDOWS = {"all_matched":(START,END), "jun_sep_2025":("2025-06-01","2025-09-30"),
           "nov_feb_2025_26":("2025-11-01","2026-02-28"),"jun_sep_2026":("2026-06-01","2026-09-30")}

plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"text.color":DARK,"axes.labelcolor":DARK,
    "axes.edgecolor":GRID,"xtick.color":DARK,"ytick.color":DARK,"axes.spines.top":False,
    "axes.spines.right":False,"figure.facecolor":"white","savefig.facecolor":"white"})


def read(input_path):
    d = pd.read_csv(input_path,parse_dates=["date"])
    return d


def next_wait(pass_dates,days):
    """Inclusive UTC calendar alignment, exact future date or missing."""
    targets = pd.DatetimeIndex(pass_dates).sort_values().values.astype("datetime64[D]")
    bins = days.values.astype("datetime64[D]")
    if len(targets)==0:
        return np.full(len(bins), np.inf)
    ind = np.searchsorted(targets,bins,side="left")
    ok = ind < len(targets)
    wait = np.full(len(bins), np.inf)
    wait[ok] = (targets[ind[ok]] - bins[ok]).astype(int)
    return wait


def date_sets(d, cut, metric="clear_pct"):
    return set(d.loc[(d.status=="ok") & (d[metric]>=cut),"date"])


def row_summary(data):
    out=[]
    for site in SITES:
        for window,(start,end) in WINDOWS.items():
            d = data[(data.site==site)&data.date.between(start,end)]
            s=d[d.sensor=="Sentinel-2"]
            l=d[d.sensor=="Landsat 8/9"]
            eligible_dates = pd.date_range(start,pd.Timestamp(end)-pd.Timedelta(days=7))
            for metric in ["clear_pct","water_pct"]:
                for cut in CUTOFFS:
                    a,b=date_sets(s,cut,metric),date_sets(l,cut,metric)
                    base=dict(site=site,window=window,start=start,end=end,threshold=cut,metric=metric,
                              sentinel_catalog=s.date.nunique(),sentinel_read=s.loc[s.status=="ok","date"].nunique(),
                              landsat_catalog=l.date.nunique(),landsat_read=l.loc[l.status=="ok","date"].nunique(),
                              sentinel_pass=len(a),landsat_pass=len(b),common_pass=len(a&b),landsat_added=len(b-a))
                    for label, dates in [("sentinel",a),("landsat",b),("combined",a|b)]:
                        ordered=sorted(dates)
                        left_anchored=[pd.Timestamp(start)-pd.Timedelta(days=1),*ordered,pd.Timestamp(end)+pd.Timedelta(days=1)]
                        gap=max([(r-p).days-1 for p,r in zip(left_anchored,left_anchored[1:])],default=np.nan)
                        wait=next_wait(ordered,eligible_dates)
                        base[f"{label}_max_unqualified_run_days"]=gap
                        base[f"{label}_within3_pct"]=round(float((wait<=3).mean())*100,2)
                        base[f"{label}_within7_pct"]=round(float((wait<=7).mean())*100,2)
                    out.append(base)
    return pd.DataFrame(out)


def chart_monthly(s, outdir):
    z=s.assign(month=s.date.dt.month, ok=s.status.eq("ok"), passed=s.status.eq("ok")&s.clear_pct.ge(90))
    tbl=z.groupby(["site","month"]).agg(passes=("passed","sum"),measured=("ok","sum"),catalog=("id","size")).reset_index()
    tbl["pass_low_pct"] = 100*tbl.passes/tbl.catalog
    tbl["pass_high_pct"] = 100*(tbl.passes+tbl.catalog-tbl.measured)/tbl.catalog
    tbl.to_csv(ROOT/"monthly_sentinel_summary.csv",index=False)
    fig, ax = plt.subplots(figsize=(9.6,3.85), layout="constrained")
    for site,c,m in zip(SITES,[S_COL,L_COL],["o","s"]):
        site_z = tbl[tbl.site==site]
        ax.fill_between(site_z.month,site_z.pass_low_pct,site_z.pass_high_pct,color=c,alpha=.13)
        ax.plot(site_z.month,site_z.pass_low_pct,color=c,marker=m,lw=2.4,ms=5.5,label=site)
        for p in site_z.itertuples():
            label_offset = 9 if site=="Tunda" else -10
            ax.annotate(f"{p.passes}/{p.catalog}",(p.month,p.pass_low_pct),xytext=(0,label_offset),textcoords="offset points",
                        color=c,ha="center",va="center",fontsize=6.7)
    ax.grid(axis="y",color=GRID)
    ax.set_axisbelow(True)
    ax.set(xlim=(.6,12.4),ylim=(-6,106),ylabel="Catalog dates passing local screen (%)",
           xticks=np.arange(1,13),xticklabels=list(calendar.month_abbr)[1:])
    ax.legend(frameon=False,ncol=2,loc="upper left")
    fig.savefig(outdir/"optical_monthly.png",dpi=210)
    plt.close(fig)


def chart_combined(d, outdir):
    fig, axes = plt.subplots(2,1,figsize=(9.7,4.4),layout="constrained",sharex=True)
    eligible = pd.date_range(START,pd.Timestamp(END)-pd.Timedelta(days=7))
    for ax, site in zip(axes,SITES):
        q = d[(d.site==site)&d.date.between(START,END)]
        s = date_sets(q[q.sensor=="Sentinel-2"],90)
        l = date_sets(q[q.sensor=="Landsat 8/9"],90)
        ax.scatter(sorted(s),np.ones(len(s)),marker="|",s=80,color=S_COL,linewidths=1.3, label="Sentinel-2 pass")
        ax.scatter(sorted(l-s),np.ones(len(l-s))*0.25,marker="|",s=80,color=L_COL,linewidths=1.3, label="Landsat-only pass")
        ax.set_ylim(-.14,1.43)
        ax.set_yticks([.25,1],["Landsat-only","Sentinel-2"])
        ax.vlines(pd.to_datetime("2025-11-01"),-.1,1.4,color=GRID,lw=0.7)
        ax.axvspan(pd.to_datetime("2025-11-01"),pd.to_datetime("2026-03-01"),color=GRID,alpha=.4,zorder=-2)
        ax.set_title(f"{site} • {len(s)} Sentinel-2 dates, {len(l-s)} added by Landsat",loc="left",fontweight="semibold")
    axes[-1].set_xlim(pd.Timestamp(START)-pd.Timedelta(days=2),pd.Timestamp(END)+pd.Timedelta(days=4))
    axes[-1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    axes[-1].set_xlabel("Acquisition date (UTC)")
    fig.savefig(outdir/"optical_union_timeline.png",dpi=210)
    plt.close(fig)


def chart_reef(s,outdir):
    z=s[(s.site=="Tunda") & (s.status=="ok") & s.reef_clear_pct.notna()].copy()
    if z.empty:
        return
    fig,ax=plt.subplots(figsize=(7.3,4.6),layout="constrained")
    both=(z.clear_pct>=90)&(z.reef_clear_pct>=90)
    disagree=(z.clear_pct>=90)^(z.reef_clear_pct>=90)
    ax.scatter(z.loc[~both & ~disagree,"clear_pct"],z.loc[~both & ~disagree,"reef_clear_pct"],s=13,alpha=.34,color=B_COL,label="Both below gate")
    ax.scatter(z.loc[both,"clear_pct"],z.loc[both,"reef_clear_pct"],s=13,alpha=.45,color=S_COL,label="Both pass")
    ax.scatter(z.loc[disagree,"clear_pct"],z.loc[disagree,"reef_clear_pct"],s=26,alpha=.88,color=L_COL,label="Ring and reef disagree")
    ax.axhline(90,zorder=-1,color=DARK,ls="--",lw=.9)
    ax.axvline(90,zorder=-1,color=DARK,ls="--",lw=.9)
    ax.plot([0,100],[0,100],zorder=-1,lw=.75,color="#a4b1ba")
    ax.set(xlim=(-2,103),ylim=(-2,103),xlabel="Island ring available (%)",ylabel="Historical reef footprint available (%)")
    ax.legend(frameon=True,loc="lower right",facecolor="white",edgecolor="#dae5e9",framealpha=.95)
    fig.savefig(outdir/"optical_reef_disagreement.png",dpi=210)
    plt.close(fig)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,default=DEFAULT_FIGURES)
    p.add_argument("--sentinel",type=Path,default=ROOT/"sentinel_legacy_coverage.csv")
    p.add_argument("--landsat",type=Path,default=ROOT/"landsat_coverage.csv")
    args=p.parse_args()
    args.outdir.mkdir(exist_ok=True)
    s=read(args.sentinel)
    l=read(args.landsat)
    d=pd.concat([s,l],ignore_index=True)
    summaries=row_summary(d)
    summaries.to_csv(ROOT/"multisensor_summary.csv",index=False)
    s=s.assign(pass_local=(s.clear_pct>=90)&(s.status=="ok"),pass_tile=s.catalog_cloud_pct<=20,
               pass_reef=s.reef_clear_pct>=90)
    years=s.groupby([s.site,s.date.dt.year]).agg(catalog=('id','size'),read=('status',lambda x:(x=="ok").sum()),
        local=('pass_local','sum'),tile=('pass_tile','sum'),reef=('pass_reef','sum')).reset_index()
    years.to_csv(ROOT/"annual_sentinel_summary.csv",index=False)
    chart_monthly(s,args.outdir)
    chart_combined(d,args.outdir)
    chart_reef(s,args.outdir)
    print(years.to_string(index=False))
    print(summaries.loc[(summaries.metric=="clear_pct")&(summaries.threshold==90)].to_string(index=False))
    tunda=s[(s.site=="Tunda") & (s.status=="ok") & s.reef_clear_pct.notna()]
    print("reef discordant at 90%", len(tunda), int((tunda.pass_local & ~tunda.pass_reef).sum()), int((~tunda.pass_local & tunda.pass_reef).sum()))


if __name__ == "__main__":
    main()
