"""Draw the aligned two-mission event timeline from bundled CSVs."""
import csv
from datetime import date
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from amur_analysis import BASE,set_style

LABEL = {'Sentinel-2':'#13746f','Landsat 8/9':'#985270'}
MARK = {'Sentinel-2':'o','Landsat 8/9':'s'}
COLLECTIONS = {
    'Sentinel-2':'amur_daily_2023.csv',
    'Landsat 8/9':'amur_landsat_daily_2023.csv',
}

def read(name):
    with open(BASE/name,newline='') as f:
        return list(csv.DictReader(f))
def points(rows, key):
    return [date.fromisoformat(row['date']) for row in rows], [float(row[key]) for row in rows]
def main():
    set_style()
    fig, axes = plt.subplots(3,1,figsize=(10,7.1),sharex=True,layout='constrained',
                  gridspec_kw={'height_ratios':[1,1.02,1.13]})
    for ax in axes:
        for start,end in ((date(2023,8,10),date(2023,8,14)),(date(2023,8,24),date(2023,8,28)),
                          (date(2023,8,30),date(2023,9,2))):
            ax.axvspan(start,end,color='#e0e9ec',alpha=.8,lw=0)
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.25)
    rain=read('amur_rainfall_daily_2023.csv')
    ax=axes[0]
    ax.bar([date.fromisoformat(r['date_utc']) for r in rain],
           [float(r['precipitation_mm']) for r in rain],color='#5f8393',width=.87)
    ax.set_ylabel('Rainfall (mm)')
    ax.set_title('Amur Bay | Two missions added clear dates outside the flood intervals',loc='left')
    ax.text(date(2023,7,2),85,'ERA5 point  •  Shaded: published flood intervals',ha='left',va='top',fontsize=9)
    aq=axes[1]
    ap=axes[2]
    ap.axhline(0,color='#557789',alpha=.6,lw=1)
    aq.axhline(90,color='#557789',alpha=.6,lw=1,ls='--')
    for label,file in COLLECTIONS.items():
        rows=read(file)
        assert not any(row['error'] for row in rows)
        for row in rows:
            row['coverage']=min(float(row['west_water_pct']),float(row['east_water_pct']))
            if row['coverage']>=90:
                row['contrast']=float(row['west_red'])-float(row['east_red'])
        aq.scatter(*points(rows,'coverage'),marker=MARK[label],c=LABEL[label],s=29,label=label,
                    linewidths=.7,edgecolors='white',alpha=.88,zorder=4)
        qualifying=[row for row in rows if row['coverage']>=90]
        ap.scatter(*points(qualifying,'contrast'),marker=MARK[label],c=LABEL[label],s=44,
                    linewidths=.7,edgecolors='white',zorder=4)
    aq.set_ylabel('Lower of two\nzone QA passes (%)')
    aq.set_ylim(-5,108)
    aq.legend(loc='upper left',ncol=2,frameon=False,fontsize=9)
    ap.set_ylabel('West minus east\nred-band reflectance')
    ap.annotate('12 Jul: stronger pre-flood contrast', (date(2023,7,12),.09614),
                  xytext=(4,-12),textcoords='offset points',fontsize=9)
    ap.annotate('6 Sep: first joint view\nafter final flood interval', (date(2023,9,6),.064598),
                  xytext=(5,2),textcoords='offset points',fontsize=9)
    ap.set_ylim(-.005,.113)
    ap.set_xlim(date(2023,7,1),date(2023,9,30))
    ap.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO,interval=2))
    ap.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ap.set_xlabel('Date (UTC), 2023')
    fig.savefig(BASE/'amur_cross_sensor_timeline.png',dpi=240)
    plt.close(fig)
if __name__=='__main__':
    main()
