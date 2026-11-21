"""Plot the published proxy series with explicit dated case anchors."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
B=Path(__file__).resolve().parent.parent
data=pd.read_csv(B/'rain/rainfall_daily.csv',parse_dates=['date_utc'])
units={'imerg_mean':('NASA IMERG proxy mean','#13786f'),'chirps':('CHIRPS area mean','#c46e39'),'cpc':('NOAA CPC cell','#506f99')}
spec=[
 ('Tunda','2023-10-15','2023-11-24',[('2023-10-27','KKP inspection'),('2023-11-04','Wet reference')],'tunda_rain.png'),
 ('Kodingareng','2020-02-01','2020-10-31',[('2020-02-13','Reported start'),('2020-03-05','Wet reference'),('2020-09-12','Incident account')],'koding_rain.png')
]
for site,date0,date1,anchors,name in spec:
    fig,ax=plt.subplots(figsize=(9.8,3.4),layout='constrained')
    sub=data[(data.site==site)&(data.date_utc>=date0)&(data.date_utc<=date1)]
    for k,(lab,color) in units.items():
        ax.plot(sub.date_utc,sub[k],lw=1.1,marker='o' if site=='Tunda' else None,ms=2.3,color=color,label=lab,alpha=.82)
    for dt,lab in anchors:
        d=pd.Timestamp(dt);ax.axvline(d,color='#405b60',ls='--',lw=.9)
        ax.annotate(lab,(d,1),xycoords=('data','axes fraction'),xytext=(3,-4),textcoords='offset points',ha='left',va='top',fontsize=8.3,
                    bbox={'facecolor':'white','edgecolor':'none','alpha':.86})
    ax.set_ylabel('Daily precipitation (mm)')
    ax.set_xlabel('Product date label')
    ax.set_xlim(pd.Timestamp(date0)-pd.Timedelta(days=1),pd.Timestamp(date1)+pd.Timedelta(days=1))
    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b' if site=='Tunda' else '%b'))
    ax.tick_params(axis='x',labelsize=8)
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.21),ncol=3,frameon=False,fontsize=8.1)
    fig.savefig(B/'figures'/name,dpi=220,bbox_inches='tight')
    plt.close(fig)
