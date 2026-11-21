#!/usr/bin/env python3
"""Create Tunda's event-acquisition-release clock audit from retrieved STAC records."""
import csv
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
rows = list(csv.DictReader((root/"tunda_event_sensor_clocks.csv").open()))
def local_date(row):
    return datetime.fromisoformat(row["acquisition"].replace("Z","+00:00")).date()

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color":"#17324a",
                     "axes.labelcolor":"#17324a", "xtick.color":"#17324a","ytick.color":"#17324a"})
fig=plt.figure(figsize=(14,8.1), facecolor="#f8faf9")
ax=fig.add_axes([0.15,0.45,0.81,0.36],facecolor="#f8faf9")
colors={3:"#166e68",2:"#3b6395",1:"#7162a2"}
bands=[
    ("Sentinel-2 L2A","copernicus-s2",3,{"sentinel-2a","sentinel-2b"}),
    ("Landsat 8/9 L2","mpc-l89",2,{"landsat-8","landsat-9"}),
    ("Sentinel-1 GRD","copernicus-s1",1,{"sentinel-1a","sentinel-1b"}),
]
d=lambda x: datetime.fromisoformat(x)
event=d("2023-10-27")
published=d("2023-10-29")
for label,name,y,platforms in bands:
    ds=sorted({local_date(r) for r in rows if r["query"]==name and r["platform"] in platforms})
    ax.scatter(ds,[y]*len(ds),s=78,color=colors[y],edgecolor="white",linewidths=1.3,zorder=3)
    ax.axhline(y, color="#d4dedd",lw=.8,zorder=0)
ax.axvline(event,color="#c95d37",lw=2,zorder=2)
ax.axvline(published,color="#c95d37",lw=1.5,ls="--",zorder=2)
ax.text(event,3.67,"27 OCT • STOP",color="#ac4725",weight="bold",ha="right",va="center",fontsize=11)
ax.text(published,3.67,"29 OCT • KKP RELEASE",color="#ac4725",weight="bold",ha="left",va="center",fontsize=11)
ax.set_xlim(d("2023-10-11"),d("2023-11-12"))
ax.set_ylim(.53,3.9)
ax.set_yticks([a[2] for a in bands],labels=[a[0] for a in bands])
ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.spines[["top","left","right"]].set_visible(False)
ax.spines["bottom"].set_color("#a6b8b6")
ax.tick_params(axis="both",length=0,pad=9)
fig.text(.055,.925,"Check publication time before using imagery in an event replay.",
         fontsize=22,weight="bold",color="#102e46")
fig.text(.055,.876,"Acquisitions around the 27 October 2023 inspection at Tunda Island",fontsize=15,color="#47677a")
fig.text(.055,.365,"THE 26 OCT ACQUISITION HAS TWO DOCUMENTED PRODUCT LINEAGES",fontsize=12,
         weight="bold",color="#166e68")
fig.text(.055,.290,"EARTH SEARCH LEGACY   •   N0509",fontsize=12,weight="bold",color="#166e68")
fig.text(.055,.242,"26 Oct 2023, 06:21 UTC\nProduct generated",fontsize=12,va="top")
fig.text(.34,.239,"→",fontsize=18,weight="bold",color="#166e68",ha="left",va="top")
fig.text(.38,.242,"26 Oct 2023, 11:34 UTC\nSCL asset last modified",fontsize=12,va="top")
fig.text(.68,.239,"→",fontsize=18,weight="bold",color="#166e68",ha="left",va="top")
fig.text(.72,.242,"26 Oct 2023, 11:35 UTC\nCatalog item created",fontsize=12,va="top")
fig.text(.055,.172,"COPERNICUS DATA SPACE   •   N0510 REPROCESSING",fontsize=12,weight="bold",color="#3b6395")
fig.text(.055,.126,"7 Nov 2024\nReprocessing timestamp",fontsize=12,va="top")
fig.text(.34,.123,"→",fontsize=18,weight="bold",color="#3b6395",ha="left",va="top")
fig.text(.38,.126,"25 Apr 2025\nCatalog publication stamp",fontsize=12,va="top")
fig.text(.055,.012,"Scope: 12 Oct–11 Nov 2023. Dots show acquisitions returned for the study bounding box. Acquisition dates use UTC. KKP dates follow the source. Publication and asset timestamps do not establish agency receipt.\nSources: Copernicus Data Space, Earth Search, Microsoft Planetary Computer, and KKP release SP.402/SJ.5/X/2023.",
         fontsize=9.4,color="#4b6778",linespacing=1.5)
fig.savefig(root/"tunda_event_three_clocks.png",dpi=180,bbox_inches="tight",pad_inches=.25)
