"""Generate core figures from the archived-footprint analysis and declared scenarios."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

B=Path(__file__).parent.parent
F=B/'figures'
F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'text.color':'#1b3439','axes.labelcolor':'#1b3439',
                     'axes.spines.top':False,'axes.spines.right':False})
TEAL='#117c73'; GOLD='#c66e33'; INK='#183b43'; BLUE='#416a92'
def save(fig,name):
    fig.savefig(F/name,dpi=210,facecolor='white',bbox_inches='tight',pad_inches=.13)
    plt.close(fig)

def locations():
    data=json.loads((B/'root/natural_earth_land.geojson').read_text())
    sites=[('Tunda',106.27811,-5.81151,(98,113,-11,1),'Banten, Indonesia'),
           ('Kodingareng Lompo',119.26473,-5.14905,(112,126,-11,1),'South Sulawesi, Indonesia'),
           ('Amur Bay',131.75,43.27,(123,140,37,50),'Russian Far East')]
    fig,ax=plt.subplots(1,3,figsize=(10.4,3.35),layout='constrained')
    for a,(name,lon,lat,bounds,label) in zip(ax,sites):
        x0,x1,y0,y1=bounds
        patches=[]
        for f in data['features']:
            g=f['geometry']
            for p in g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]:
                ring=np.array(p[0])
                if ring[:,0].min()>x1 or ring[:,0].max()<x0 or ring[:,1].min()>y1 or ring[:,1].max()<y0:continue
                patches.append(Polygon(ring,closed=True))
        a.set_facecolor('#e4efef')
        a.add_collection(PatchCollection(patches,facecolor='#b8d2bc',edgecolor='#7aa293',lw=.4))
        a.set(xlim=(x0,x1),ylim=(y0,y1),aspect='equal')
        a.scatter(lon,lat,s=82,facecolor=GOLD,edgecolor='white',lw=1.4,zorder=5)
        a.plot([lon,lon],[lat,min(lat+2.3,y1)],lw=.85,color=INK)
        a.set_title(name+ '\n'+label,loc='left',fontsize=10,color=INK,weight='bold')
        a.grid(color='white',lw=.55)
        a.tick_params(length=0,labelsize=7)
        a.set_xlabel('Longitude (°E)',fontsize=8)
        if a==ax[0]:a.set_ylabel('Latitude (°)',fontsize=8)
    save(fig,'study_sites.png')

def transport():
    speeds=np.array([.05,.10,.15,.20,.25,.35])
    hours=np.array([2,4,6,8,12])
    km=3.6*speeds[:,None]*hours[None,:]
    with (B/'root/travel_scenarios.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['constant_speed_m_per_s','hours','kinematic_distance_km'])
        for i,speed in enumerate(speeds):
            for j,hr in enumerate(hours):
                w.writerow([speed,hr,round(km[i,j],3)])
    fig,axs=plt.subplots(1,2,figsize=(10.3,3.4),gridspec_kw={'width_ratios':[1.35,1]},layout='constrained')
    a=axs[0]
    a.imshow(km,cmap='GnBu',vmin=0,vmax=15,aspect='auto')
    a.set(xticks=range(len(hours)),xticklabels=[str(h) for h in hours],yticks=range(len(speeds)),yticklabels=[f'{v:.2f}' for v in speeds],xlabel='Time (hours)',ylabel='Assumed steady speed (m/s)')
    a.set_title('A   Travel distance (km)',loc='left',weight='bold')
    for i in range(len(speeds)):
        for j in range(len(hours)):
            a.text(j,i,f'{km[i,j]:.1f}',va='center',ha='center',color='white' if km[i,j]>8 else INK,fontsize=9)
    a=axs[1]
    a.set(xlim=(-.3,4.4),ylim=(-.2,4.3),aspect='equal')
    a.axis('off')
    a.set_title('B   The nearer receptor can sit off-path',loc='left',weight='bold')
    a.annotate('',xy=(4.2,.9),xytext=(.6,.9),arrowprops={'arrowstyle':'-|>','lw':3,'color':TEAL})
    a.scatter([.6,1.45,3.65],[.9,2.02,.9],s=[120,89,99],c=[BLUE,GOLD,GOLD],edgecolors='white',zorder=5)
    a.text(.6,.5,'Source',ha='center',fontsize=9)
    a.text(1.45,2.22,'A  /  1.4 km',ha='center',fontsize=9)
    a.text(3.65,.49,'B  /  3.1 km',ha='center',fontsize=9)
    a.text(2.8,1.1,'assumed straight path',ha='center',fontsize=7.5,color=TEAL,weight='bold')
    save(fig,'transport.png')

def load(s):
    return list(csv.DictReader((B/'root'/f'{s.lower()}_habitat_scl.csv').open()))
def habitat():
    fig,axes=plt.subplots(1,2,figsize=(10.3,3.65),layout='constrained',sharex=True,sharey=True)
    summary={}
    for site,a in zip(['Tunda','Kodingareng'],axes):
        all_records=load(site)
        rec=[r for r in all_records if r['status']=='read' and r['reef_broad_pct']]
        out={}
        for period,marker,clr in [('historical','o',TEAL),('baseline_check','s',GOLD)]:
            sub=[r for r in rec if r['group']==period]
            nums=[(float(r['ring_broad_pct']),float(r['reef_broad_pct'])) for r in sub]
            hist=np.array(nums)
            if len(hist):
                a.scatter(hist[:,0],hist[:,1],s=15,marker=marker,c=clr,edgecolors='white',alpha=.5,lw=.25,label=f'{period.replace("_"," ")} (n={len(hist)})')
            out[period]={'read':len(sub),'planned':sum(x['group']==period for x in all_records),
                         'ring_only':sum(x>=90 and y<90 for x,y in nums),'reef_only':sum(y>=90 and x<90 for x,y in nums),
                         'both':sum(y>=90 and x>=90 for x,y in nums),'neither':sum(y<90 and x<90 for x,y in nums),
                         'overlap_median':float(np.median([float(q['reef_overlap_ring_pct']) for q in sub])) if sub else None,
                         'west_below_reef_pass':sum(float(q['reef_broad_pct'])>=90 and float(q['west_broad_pct'])<90 for q in sub)}
        summary[site]=out
        a.plot([0,100],[0,100],color='#89a6a2',lw=.75)
        a.axhline(90,color=INK,ls='--',alpha=.55,lw=.7);a.axvline(90,color=INK,ls='--',alpha=.55,lw=.7)
        a.set(xlim=(-2,103),ylim=(-2,103),xlabel='Annulus retained (%)')
        a.set_title(site,loc='left',weight='bold')
        a.legend(loc='upper left',bbox_to_anchor=(0,.85),fontsize=7.7,frameon=False)
    axes[0].set_ylabel('Archived reef footprint retained (%)')
    save(fig,'habitat_disagreement.png')
    (B/'root/habitat_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary))
if __name__=='__main__':
    locations()
    transport()
    if (B/'root/tunda_habitat_scl.csv').exists() and (B/'root/kodingareng_habitat_scl.csv').exists():
        habitat()
